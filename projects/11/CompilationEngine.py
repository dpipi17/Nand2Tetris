from JackTokenizer import JackTokenizer
from VMWriter import VMWriter
from SymbolTable import SymbolTable

class CompilationEngine: 

    DEBUG = False
    
    translate_dict = {
        '+': 'add',
        '-': 'sub',
        '=': 'eq',
        '>': 'gt',
        '<': 'lt',
        '&': 'and',
        '|': 'or',
        'unary-': 'neg',
        'unary~': 'not',
        'argument': 'argument',
        'static': 'static',
        'var': 'local',
        'field': 'this',
        '*' : 'Math.multiply',
        '/' : 'Math.divide'
    }

    def __init__(self, input : JackTokenizer, output_file_path):
        self.tokenizer = input
        self.vmwriter = VMWriter(output_file_path)
        self.symbol_table = SymbolTable()

        self.label_index = 0
        self.curr_token = ''
        self.curr_token_type = ''
        self.depth = 0

    def compile_class(self):
        self.print_open('compile_class')
        self.__next_token() # class
        self.__next_token() # className
        self.class_name = self.curr_token
        self.__next_token() # {

        self.__next_token()
        while self.curr_token == 'static' or self.curr_token == 'field':
            self.compile_class_var_dec()

        while self.curr_token == 'constructor' or self.curr_token == 'function' or self.curr_token == 'method':
            self.compile_subroutine_dec()
        
        self.__next_token() # after }
        self.vmwriter.close()
        self.print_close('compile_class_end')
        

    def compile_class_var_dec(self):
        self.print_open('compile_class_var_dec')
        kind = self.curr_token # (static|field)

        self.__next_token() 
        var_type = self.curr_token # type

        self.__next_token()
        var_name = self.curr_token # varName

        self.symbol_table.define(var_name, var_type, self.translate_dict[kind])
        
        self.__next_token() # , or ;
        while (self.curr_token != ';'):
            self.__next_token() 
            var_name = self.curr_token # varName
            self.symbol_table.define(var_name, var_type, self.translate_dict[kind])
            self.__next_token() # , or ;

        self.__next_token() # after ;
        self.print_close('compile_class_var_dec_end')
        

    def compile_subroutine_dec(self):
        self.print_open('compile_subroutine_dec')
        self.symbol_table.start_subroutine()

        kind = self.curr_token # (constructor|function|method)

        self.__next_token()
        var_type = self.curr_token # (void|type)

        self.__next_token()
        subroutine_name = self.curr_token # subroutineName

        self.__next_token() # '('

        if kind == 'method':
            self.symbol_table.define('this', self.class_name, 'argument')
        
        self.__next_token()
        self.compile_parameter_list()
       
        self.__next_token() # after ')'
        
        self.compile_subroutine_body(kind, var_type, subroutine_name)
        self.print_close('compile_subroutine_dec_end')

    def compile_parameter_list(self):
        self.print_open('compile_parameter_list')
        while self.curr_token != ')':
            if self.curr_token == ',':
                self.__next_token()

            var_type = self.curr_token # type
            
            self.__next_token()
            var_name = self.curr_token # varName

            self.symbol_table.define(var_name, var_type, 'argument')
            self.__next_token()
        self.print_close('compile_parameter_list_end')

    def compile_subroutine_body(self, kind, var_type, subroutine_name): 
        self.print_open('compile_subroutine_body')
        self.__next_token() # after '{'
        while self.curr_token == 'var':
            self.compile_var_dec()

        self.vmwriter.write_function(self.class_name + '.' + subroutine_name, self.symbol_table.var_count('local'))

        if kind == 'method':
            self.vmwriter.write_push('argument', 0)
            self.vmwriter.write_pop('pointer', 0)
        elif kind == 'constructor':
            self.vmwriter.write_push('constant', self.symbol_table.var_count('this'))
            self.vmwriter.write_call('Memory.alloc', 1)
            self.vmwriter.write_pop('pointer', 0)

        self.compile_statements()
        self.__next_token() # after '}'

        self.print_close('compile_subroutine_body_end')

    def compile_var_dec(self):
        self.print_open('compile_var_dec')
        # curr token is var

        self.__next_token()
        var_type = self.curr_token # type
        
        self.__next_token()
        var_name = self.curr_token # varName

        self.symbol_table.define(var_name, var_type, 'local')
        
        self.__next_token() # , or ;
        while self.curr_token != ';':
            self.__next_token() 
            self.symbol_table.define(self.curr_token, type, 'local')
            self.__next_token()

        self.__next_token() # after ;

        self.print_close('compile_var_dec_end')

    def compile_statements(self):
        self.print_open('compile_statements')
        while True:
            if self.curr_token == 'let':
                self.compile_let()
            elif self.curr_token == 'if':
                self.compile_if()
            elif self.curr_token == 'while':
                self.compile_while()
            elif self.curr_token == 'do ':
                self.compile_do()
            elif self.curr_token == 'return':
                self.compile_return()
            else:
                break
        self.print_close('compile_statements_end')

    def compile_let(self):
        self.print_open('compile_let')
        # curr_token is let
        self.__next_token()
        var_name = self.curr_token # varName
        kind = self.symbol_table.kind_of(var_name)
        index = self.symbol_table.index_of(var_name)

        self.__next_token()
        if self.curr_token == '[':
            # push arr
            self.vmwriter.write_push(kind, index)

            # VM code for computing and pushing the value of expression1
            self.__next_token()
            self.compile_expression()
            self.__next_token()

            # add
            self.vmwriter.write_arithmetic('add')

            # VM code for computing and pushing the value of expression2
            self.__next_token() # after = 
            self.compile_expression()
            self.__next_token() # after ;

            # pop temp 0
            self.vmwriter.write_pop('temp', 0)

            # pop pointer 1
            self.vmwriter.write_pop('pointer', 1)

            # push temp 0
            self.vmwriter.write_push('temp', 0)

            # pop that 0
            self.vmwriter.write_pop('that', 0)
        else:
            self.__next_token() # after =
            self.compile_expression()
            self.__next_token() # after ;

            self.vmwriter.write_pop(kind, index)
        self.print_close('compile_let_end')

    def compile_if(self):
        self.print_open('compile_if')
        # curr_token is if

        index_l = self.__next_label_index()

        self.__next_token() # (
        self.__next_token() # after (
        self.compile_expression()
        self.vmwriter.write_arithmetic('not')
        self.__next_token() # ) --> {

        self.__next_token() # { --> ?
        self.vmwriter.write_if('L1' + str(index_l))
        self.compile_statements()
        self.vmwriter.write_go_to('L2' + str(index_l))
        self.__next_token() # } --> ?

        self.vmwriter.write_label('L1' + str(index_l))
        
        if self.curr_token == 'else':
            self.__next_token() # else --> {
            
            self.__next_token() # { --> ?
            self.compile_statements()
            self.__next_token() # } --> ?

        self.vmwriter.write_label('L2' + str(index_l))
        self.print_close('compile_if_end')

    def compile_while(self):
        self.print_open('compile_while')
        # curr_token is while
        index = self.__next_label_index()

        self.vmwriter.write_label('L1' + str(index))
        self.__next_token() # while --> (
        self.__next_token() # ( --> ?
        self.compile_expression()
        self.__next_token() # ) --> {
        
        self.vmwriter.write_arithmetic('not')
        self.vmwriter.write_if('L2' + str(index))
        
        self.__next_token() # { --> ?
        self.compile_statements()
        self.__next_token() # } --> ?
        self.vmwriter.write_go_to('L1' + str(index))

        self.vmwriter.write_label('L2' + str(index))
        self.print_close('compile_while_end')

    def compile_do(self):
        self.print_open('compile do')
        # curr_token is do
        self.__next_token() # do --> (subroutineName | className | varName)
        self.subroutine_call()
        self.vmwriter.write_pop('temp', 0) # because of void call
        self.__next_token() # ; --> ?
        self.print_close('compile do_end')
    
    def subroutine_call(self, skipped = False, arg_name = ''):
        self.print_open('subroutine_call')
        name = ''
        if skipped:
            name = arg_name
        else :
            name = self.curr_token # (subroutineName | className | varName)
            self.__next_token()
        
        function = name
        args = 0
        if self.curr_token == '(':
            function = self.class_name + '.' + name
            self.vmwriter.write_push('pointer', 0)
            args = 1
        elif self.curr_token == '.':
            self.__next_token() # . --> subroutine_name
            subroutine_name = self.curr_token

            kind = self.symbol_table.kind_of(name)
            if kind == None:
                function = name + '.' + subroutine_name
            else:
                var_type = self.symbol_table.type_of(name)
                function = var_type + '.' + subroutine_name
                self.vmwriter.write_push(kind, self.symbol_table.index_of(name))
                args = 1
            self.__next_token() # subroutine_name --> (
        
        self.__next_token() # ( --> ?
        expression_list_len = self.compile_expression_list()
        self.__next_token() # ) --> ;

        self.vmwriter.write_call(function, args + expression_list_len)
        # self.__next_token() # ; --> ?
        self.print_close('subroutine_call_end')

    def compile_return(self):
        self.print_open('compile_return')
        # curr_token is return

        self.__next_token() # return --> ?

        if self.curr_token != ';':
            self.compile_expression()
        else:
            self.vmwriter.write_push('constant', 0)

        self.__next_token() # ; --> ?
        self.vmwriter.write_return()
        self.print_close('compile_return_end')


    def compile_expression(self):
        self.print_open('compile_expression')
        self.compile_term()

        while self.curr_token in {'+', '-', '*', '/', '&', '|', '<', '>', '='}:
            op = self.curr_token
            self.__next_token()
            self.compile_term()

            if op in ['*', '/']:
                self.vmwriter.write_call(self.translate_dict[op], 2)
            else:
                if op in self.translate_dict:
                    self.vmwriter.write_arithmetic(self.translate_dict[op])
        
        self.print_close('compile_expression_end')

    def compile_term(self):
        self.print_open('compile_term')
        if self.curr_token == '(':
            self.__next_token() # ( --> ?
            self.compile_expression()
            self.__next_token() # ) --> ?
        elif self.curr_token in {'-', '~'}:
            op = self.curr_token # (-|~)
            self.__next_token() # (-|~) --> ?
            self.compile_term()
            self.vmwriter.write_arithmetic(self.translate_dict['unary' + op])
        else:
            if self.curr_token_type == 'stringConstant':
                self.vmwriter.write_push('constant', len(self.curr_token))
                self.vmwriter.write_call('String.new', 1)

                for ch in self.curr_token:
                    self.vmwriter.write_push('constant', ord(ch))
                    self.vmwriter.write_call('String.appendChar', 2)
                
                self.__next_token()

            elif self.curr_token_type == 'integerConstant':
                self.vmwriter.write_push('constant', self.curr_token)
                self.__next_token()
            elif self.curr_token_type == 'keyword':
                if self.curr_token == 'this':
                    self.vmwriter.write_push('pointer', 0)
                else:
                    self.vmwriter.write_push('constant', 0)

                    if self.curr_token == 'true':
                        self.vmwriter.write_arithmetic('not')
                
                self.__next_token()
            else:
                temp = self.curr_token
                self.__next_token()
                if self.curr_token == '[':
                    self.vmwriter.write_push(self.symbol_table.kind_of(temp), self.symbol_table.index_of(temp))

                    self.__next_token() # [ --> ?
                    self.compile_expression()
                    self.__next_token() # ] --> ?

                    # add
                    self.vmwriter.write_arithmetic('add')

                    # pop pointer 1
                    self.vmwriter.write_pop('pointer', 1)

                    # push that 0
                    self.vmwriter.write_push('that', 0)
                    
                elif self.curr_token in ['(', '.']:
                    self.subroutine_call(True, temp)
                else:
                    # var_name
                    self.vmwriter.write_push(self.symbol_table.kind_of(temp), self.symbol_table.index_of(temp))
                    # self.__next_token()

        self.print_close('compile_term_end')

    def compile_expression_list(self):
        self.print_open('compile_expression_list')
        count = 0
        
        while self.curr_token != ')':
            if self.curr_token == ',':
                self.__next_token()
            self.compile_expression()
            count += 1
        
        self.print_close('compile_expression_list_end')
        return count


    #-----------private methods----------------
    def __next_token(self):
        if self.DEBUG:
            print('  ' * self.depth + 'curr_token: ' + self.curr_token)
        
        if self.tokenizer.has_more_tokens():
            self.tokenizer.advance()
        self.curr_token_type = self.tokenizer.token_type()
        self.curr_token = self.tokenizer.keyword()
        

    def __next_label_index(self):
        index = self.label_index
        self.label_index += 1
        return index

    def print_open(self, string):
        if self.DEBUG:
            print('  ' * self.depth + string)
            self.depth += 1
    
    def print_close(self, string):
        if self.DEBUG:
            self.depth -= 1
            print('  ' * self.depth + string)
