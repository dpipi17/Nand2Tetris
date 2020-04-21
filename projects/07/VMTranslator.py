import sys

#Code Writer Class
class CodeWriter:

    def __init__(self, file, file_name):
        self.file = file
        self.file_name = file_name
        self.addresses_dict = {'local' : 'LCL', 'argument' : 'ARG', 'this' : 'THIS', 'that' : 'THAT', 'pointer' : 3, 'temp' : 5, 'static' : 16}
        self.operations_dict = {'add' : 'M=M+D', 'sub' : 'M=M-D', 'neg' : 'M=-M', 'eq' : 'D;JEQ', 'gt' : 'D;JGT', 'lt' : 'D;JLT', 'and' : 'M=M&D', 'or' : 'M=M|D', 'not' : 'M=!M'}
        self.label_count = 0

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
        if 'push' in self.curr_command:
            return 'C_PUSH'

        if 'pop' in self.curr_command:
            return 'C_POP'

        if any(s in self.curr_command for s in ('add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not')):
            return 'C_ARITHMETIC'

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
    if '.vm' not in argv[0]:
        return

    file_name = argv[0][:argv[0].index('.vm')]
    input_file = open(file_name + '.vm', 'r')
    output_file = open(file_name + '.asm', 'w')

    parser = Parser(input_file)
    code_writer = CodeWriter(output_file, file_name.split('/')[-1])

    while parser.has_more_commands():
        curr_command = parser.advance()
        command_type = parser.command_type()
        
        code_writer.write_command_comment('// ' + curr_command)
        if command_type == 'C_ARITHMETIC':
            code_writer.write_arithmetic(curr_command)
        elif command_type in {'C_PUSH', 'C_POP'}:
            code_writer.write_push_pop(command_type, parser.arg1(), parser.arg2())

    parser.close()
    code_writer.close()


if __name__ == "__main__":
    main(sys.argv[1:])





    
