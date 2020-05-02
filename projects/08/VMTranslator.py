import sys
import os
from os import walk

#Code Writer Class
class CodeWriter:

    def __init__(self, file):
        self.file = file
        self.file_name = None
        self.addresses_dict = {'local' : 'LCL', 'argument' : 'ARG', 'this' : 'THIS', 'that' : 'THAT', 'pointer' : 3, 'temp' : 5, 'static' : 16}
        self.operations_dict = {'add' : 'M=M+D', 'sub' : 'M=M-D', 'neg' : 'M=-M', 'eq' : 'D;JEQ', 'gt' : 'D;JGT', 'lt' : 'D;JLT', 'and' : 'M=M&D', 'or' : 'M=M|D', 'not' : 'M=!M'}
        self.label_count = 0
        self.count = 0

    def write_arithmetic(self, operation):
        if operation not in {'neg', 'not'}:
            self.__pop_from_stack_to_D()
        self.__sp_up()

        self.__save_sp_value_to_A()
        if operation in {'add', 'sub', 'neg', 'and', 'or', 'not'}:
            self.__write_line(self.operations_dict[operation])
        
        elif operation in {'eq', 'gt', 'lt'}: 
            self.__write_line('D=M-D')
            self.__write_brunching_statement(self.operations_dict[operation])
            self.label_count += 1
        
        self.__sp_down()
            
    def __write_brunching_statement(self, jump_statement):
        self.__write_line('@TRUELABEL' + str(self.label_count))
        self.__write_line(jump_statement)

        self.__save_sp_value_to_A()
        self.__write_line('M=0')
        self.__write_line('@FALSELABEL' + str(self.label_count))
        self.__write_line('0;JMP')

        self.__write_line('(TRUELABEL' + str(self.label_count) + ')')
        self.__save_sp_value_to_A()
        self.__write_line('M=-1')

        self.__write_line('(FALSELABEL' + str(self.label_count) + ')')

    def write_push_pop(self, command, segment, index):
        if segment == 'constant':
            self.__write_line('@' + str(index))
        elif segment in {'local', 'argument', 'this', 'that'}:
            self.__write_line('@' + self.addresses_dict.get(segment)) 
            self.__write_line('D=M')
            self.__write_line('@' + str(index))
            self.__write_line('A=D+A') 
        elif segment == 'static':
            self.__write_line('@' + self.file_name + '.' + str(index))
        elif segment in ['pointer', 'temp']:
            self.__write_line('@R' + str(self.addresses_dict.get(segment) + index))

        if command == 'C_POP': 
            self.__pop()
        elif command == 'C_PUSH':
            self.__push(segment)
    
    def close(self):
        self.file.close()

    def write_command_comment(self, comment):
        self.__write_line(comment) 

    def set_file_name(self, file_name):
        self.file_name = file_name

    def write_init(self):
        # SP = 256
        # call sys.init 0
        self.__write_line('@256')
        self.__write_line('D=A')
        self.__write_line('@SP')
        self.__write_line('M=D')
        self.write_call('Sys.init', 0)
    
    def write_label(self, label):
        self.__write_line('(' + label + ')')
    
    def write_go_to(self, label):
        self.__write_line('@' + label)
        self.__write_line('0; JMP')

    def write_if(self, label):
        self.__pop_from_stack_to_D()
        self.__write_line('@' + label)
        self.__write_line('D; JNE')

    def write_function(self, function_name, num_vars):
        self.__write_line('(' + function_name + ')')
        while True:
            if num_vars <= 0:
                break
            
            self.__save_sp_value_to_A()
            self.__write_line('M=0')
            self.__sp_down()
            num_vars -= 1

    def write_call(self, function_name, num_args):
        return_addr_label = function_name + '&ret' + str(self.count)

        # push retAddrLabel
        self.__write_line('@' + return_addr_label)
        self.__write_line('D=A')
        self.__push_from_D_to_stack()

        # push LCL
        self.__write_line('@LCL')
        self.__write_line('D=M')
        self.__push_from_D_to_stack()

        # push ARG
        self.__write_line('@ARG')
        self.__write_line('D=M')
        self.__push_from_D_to_stack()

        # push THIS
        self.__write_line('@THIS')
        self.__write_line('D=M')
        self.__push_from_D_to_stack()

        # push THAT
        self.__write_line('@THAT')
        self.__write_line('D=M')
        self.__push_from_D_to_stack()

        # ARG = SP-5-nArgs
        self.__save_sp_value_to_A()
        self.__write_line('D=A')
        self.__write_line('@' + str(num_args))
        self.__write_line('D=D-A')
        self.__write_line('@5')
        self.__write_line('D=D-A')
        self.__write_line('@ARG')
        self.__write_line('M=D')

        # LCL = SP
        self.__save_sp_value_to_A()
        self.__write_line('D=A')
        self.__write_line('@LCL')
        self.__write_line('M=D')

        # goto functionName
        self.__write_line('@' + function_name)
        self.__write_line('0;JMP')

        # (retAddrLabel)
        self.__write_line('(' + return_addr_label +')')
        self.count += 1

    def write_return(self):
        # endframe = LCL
        self.__write_line('@LCL')
        self.__write_line('D=M')
        self.__write_line('@endframe')
        self.__write_line('M=D')

        # retAddr = *(endframe - 5)
        self.__write_line('@endframe')
        self.__write_line('D=M')
        self.__write_line('@5')
        self.__write_line('D=D-A')
        self.__write_line('A=D')
        self.__write_line('D=M')
        self.__write_line('@retAddr')
        self.__write_line('M=D')

        # *ARG = pop()
        self.__pop_from_stack_to_D()
        self.__write_line('@ARG')
        self.__write_line('A=M')
        self.__write_line('M=D')

        # SP = ARG + 1
        self.__write_line('@ARG')
        self.__write_line('D=M')
        self.__write_line('@SP')
        self.__write_line('M=D+1')

        # THAT = *(endframe - 1)
        self.__write_line('@endframe')
        self.__write_line('D=M')
        self.__write_line('D=D-1')
        self.__write_line('A=D')
        self.__write_line('D=M')
        self.__write_line('@THAT')
        self.__write_line('M=D')

        # THIS = *(endframe - 2)
        self.__write_line('@endframe')
        self.__write_line('D=M')
        self.__write_line('@2')
        self.__write_line('D=D-A')
        self.__write_line('A=D')
        self.__write_line('D=M')
        self.__write_line('@THIS')
        self.__write_line('M=D')

        # ARG = *(endframe - 3)
        self.__write_line('@endframe')
        self.__write_line('D=M')
        self.__write_line('@3')
        self.__write_line('D=D-A')
        self.__write_line('A=D')
        self.__write_line('D=M')
        self.__write_line('@ARG')
        self.__write_line('M=D')

        # LCL = *(endframe - 4)
        self.__write_line('@endframe')
        self.__write_line('D=M')
        self.__write_line('@4')
        self.__write_line('D=D-A')
        self.__write_line('A=D')
        self.__write_line('D=M')
        self.__write_line('@LCL')
        self.__write_line('M=D') 

        # goto retAddr
        self.__write_line('@retAddr')
        self.__write_line('A=M')
        self.__write_line('0; JMP')

    def __pop(self):
        # store address into R15 register
        self.__write_line('D=A')
        self.__write_line('@R15')
        self.__write_line('M=D')

        self.__pop_from_stack_to_D()

        # save D register value into address which is stored in R15
        self.__write_line('@R15')
        self.__write_line('A=M')
        self.__write_line('M=D')

    def __push(self, segment):
        if segment != 'constant':
            self.__write_line('D=M')
        else:
            self.__write_line('D=A')
        self.__push_from_D_to_stack()

    def __push_from_D_to_stack(self):
        self.__save_sp_value_to_A()
        self.__write_line('M=D')
        self.__sp_down()

    def __pop_from_stack_to_D(self):
        self.__sp_up()
        self.__write_line('A=M')
        self.__write_line('D=M')

    def __sp_down(self):
        self.__write_line('@SP')
        self.__write_line('M=M+1')

    def __sp_up(self):
        self.__write_line('@SP')
        self.__write_line('M=M-1')

    def __save_sp_value_to_A(self):
        self.__write_line('@SP')
        self.__write_line('A=M')
    
    def __write_line(self, line):
        self.file.write(line + '\n')

# Parser Class
class Parser:

    def __init__(self, file):
        self.file = file
        self.commands = []
        self.command_index = 0
        self.__parse()
        
    def __parse(self):
        while True:
            line = self.file.readline()
            if not line: 
                break
            
            line = line.strip()
            if not line or line.startswith('//'):
                continue
            
            if '//' in line:
                line = line[0 : line.index('//')]
            command = line.strip()
            self.commands.append(command)

    def has_more_commands(self):
        return self.command_index < len(self.commands)

    def advance(self):
        self.curr_command = self.commands[self.command_index]
        self.command_index += 1
        return self.curr_command

    def command_type(self):
        if self.curr_command.startswith('push'):
            return 'C_PUSH'

        if self.curr_command.startswith('pop'):
            return 'C_POP'

        if any(self.curr_command.startswith(s) for s in ('add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not')):
            return 'C_ARITHMETIC'

        if self.curr_command.startswith('label'):
            return 'C_LABEL'

        if self.curr_command.startswith('if-goto'):
            return 'C_IF'

        if self.curr_command.startswith('goto'):
            return 'C_GOTO'

        if self.curr_command.startswith('function'):
            return 'C_FUNCTION'

        if self.curr_command.startswith('return'):
            return 'C_RETURN'

        if self.curr_command.startswith('call'):
            return 'C_CALL'

    def arg1(self):
        assert(self.command_type() != 'C_RETURN')
        if self.command_type() == 'C_ARITHMETIC':
            return self.curr_command

        return self.curr_command.split(" ")[1]

    def arg2(self):
        assert(self.command_type() in {'C_PUSH', 'C_POP', 'C_FUNCTION', 'C_CALL'})
        return int(self.curr_command.split(" ")[2])

    def close(self):
        self.file.close()

def main(argv):
    file_names = []
    consol_input = argv[0]

    if '.vm' in consol_input:
        file_names.append(consol_input)
        output_file_name = file_names[0] + '.asm'
    elif os.path.isdir(consol_input):
        for (dirpath, _, filenames) in walk(consol_input):
            file_names.extend(filter(lambda x: '.vm' in x, [(dirpath + ('/' if dirpath[-1] != '/' else '') + filename) for filename in filenames]))
            output_file_name = dirpath + ('/' + consol_input.split('/')[-1] if dirpath[-1] != '/' else consol_input.split('/')[-2]) + '.asm'
            break
    else:
        print('please enter .vm file or directory with .vm files')
        return

    output_file = open(output_file_name, 'w')
    code_writer = CodeWriter(output_file)

    if (any('Sys.vm' in s for s in file_names)):
        code_writer.write_init()

    for file_name in file_names:
        code_writer.write_command_comment('//---------------------' + file_name + ' Hack code-----------------')
        
        code_writer.set_file_name(file_name.split('/')[-1].split('.vm')[-2])
        input_file = open(file_name, 'r')
        parser = Parser(input_file)
        while parser.has_more_commands():
            curr_command = parser.advance()
            command_type = parser.command_type()
            
            code_writer.write_command_comment('// ' + curr_command)
            if command_type == 'C_ARITHMETIC':
                code_writer.write_arithmetic(curr_command)
            elif command_type in {'C_PUSH', 'C_POP'}:
                code_writer.write_push_pop(command_type, parser.arg1(), parser.arg2())
            elif command_type == 'C_CALL':
                code_writer.write_call(parser.arg1(), parser.arg2())
            elif command_type == 'C_FUNCTION':
                code_writer.write_function(parser.arg1(), parser.arg2())
            elif command_type == 'C_RETURN':
                code_writer.write_return()
            elif command_type == 'C_IF':
                code_writer.write_if(parser.arg1())
            elif command_type == 'C_LABEL':
                code_writer.write_label(parser.arg1())
            elif command_type == 'C_GOTO':
                code_writer.write_go_to(parser.arg1())

            input_file.close()

    code_writer.close()

if __name__ == "__main__":
    main(sys.argv[1:])

# run from project/08/ directory
# python3 VMTranslator.py FunctionCalls/SimpleFunction/
# python3 VMTranslator.py FunctionCalls/FibonacciElement/
# python3 VMTranslator.py FunctionCalls/NestedCall/
# python3 VMTranslator.py FunctionCalls/StaticsTest/
# python3 VMTranslator.py ProgramFlow/BasicLoop/
# python3 VMTranslator.py ProgramFlow/FibonacciSeries/


    
