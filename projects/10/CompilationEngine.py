from JackTokenizer import JackTokenizer

class CompilationEngine: 

    def __init__(self, input : JackTokenizer, output):
        self.tokenizer = input
        self.output_file = output
        self.curr_token = ''
        self.curr_token_type = ''
        self.depth = 0
        self.xml_formatter = {'<' : '&lt;', '>' : '&gt;', '"' : '&quot;', '&' : '&amp;'}

    def compile_class(self):
        self.__write_open('class')

        self.__write_next_token() # class
        self.__write_next_token() # className
        self.__write_next_token() # {

        self.__next_token()
        while self.curr_token == 'static' or self.curr_token == 'field':
            self.compile_class_var_dec()

        while self.curr_token == 'constructor' or self.curr_token == 'function' or self.curr_token == 'method':
            self.compile_subroutine_dec()
        
        self.__write_next_token()
        self.__write_close('class')

    def compile_class_var_dec(self):
        self.__write_open('classVarDec')

        self.__write_curr_token() # (static|field)
        
        while (self.curr_token != ';'):
            self.__write_next_token()
        
        self.__next_token()
        self.__write_close('classVarDec')
        

    def compile_subroutine_dec(self):
        self.__write_open('subroutineDec')

        self.__write_curr_token() # (constructor|function|method)
        self.__write_next_token() # (void|type)
        self.__write_next_token() # subroutineName
        self.__write_next_token() # '('

        self.__next_token()
        self.compile_parameter_list()
        self.__write_curr_token() # ')'
        
        self.compile_subroutine_body()

        self.__write_close('subroutineDec')

    def compile_parameter_list(self):
        self.__write_open('parameterList')

        if self.curr_token != ')':
            while self.curr_token != ')':
                self.__write_curr_token()
                self.__next_token()

        self.__write_close('parameterList')

    def compile_subroutine_body(self):
        self.__write_open('subroutineBody')

        self.__write_next_token() # {
        self.__next_token()

        while self.curr_token == 'var':
            self.compile_var_dec()

        self.compile_statements()
        self.__write_curr_token() # }
        self.__next_token()

        self.__write_close('subroutineBody')

    def compile_var_dec(self):
        self.__write_open('varDec')

        self.__write_curr_token() # var
        self.__write_next_token() # type
        self.__write_next_token() # varName
        
        self.__next_token()
        while self.curr_token != ';':
            self.__write_curr_token() # ,
            self.__write_next_token() # varName
            self.__next_token()

        self.__write_curr_token() # ;
        self.__next_token()

        self.__write_close('varDec') 

    def compile_statements(self):
        self.__write_open('statements')

        while True:
            if self.curr_token == 'let':
                self.compile_let()
            elif self.curr_token == 'if':
                self.compile_if()
            elif self.curr_token == 'while':
                self.compile_while()
            elif self.curr_token == 'do':
                self.compile_do()
            elif self.curr_token == 'return':
                self.compile_return()
            else:
                break

        self.__write_close('statements')

    def compile_let(self):
        self.__write_open('letStatement')

        self.__write_curr_token() # let
        self.__write_next_token() # varName

        self.__next_token()
        if self.curr_token == '[':
            self.__write_curr_token() # [
            self.__next_token()
            self.compile_expression()
            self.__write_curr_token() # ]
            self.__next_token()

        self.__write_curr_token() # =
        self.__next_token()
        self.compile_expression()
        self.__write_curr_token() # ;
        self.__next_token()

        self.__write_close('letStatement')

    def compile_if(self):
        self.__write_open('ifStatement')

        self.__write_curr_token() # if
        self.__write_next_token() # (
        self.__next_token()
        self.compile_expression()
        self.__write_curr_token() # )
        self.__write_next_token() # {
        
        self.__next_token()
        self.compile_statements()
        self.__write_curr_token() # }

        self.__next_token()

        if self.curr_token == 'else':
            self.__write_curr_token() # else
            self.__write_next_token() # {
            
            self.__next_token()
            self.compile_statements()
            self.__write_curr_token() # }
            self.__next_token()


        self.__write_close('ifStatement') 

    def compile_while(self):
        self.__write_open('whileStatement')

        self.__write_curr_token() # while
        self.__write_next_token() # (
        self.__next_token()
        self.compile_expression()
        self.__write_curr_token() # )
        self.__write_next_token() # {
        
        self.__next_token()
        self.compile_statements()
        self.__write_curr_token() # }

        self.__next_token()

        self.__write_close('whileStatement') 

    def compile_do(self):
        self.__write_open('doStatement')

        self.__write_curr_token() # do
        self.__write_next_token() # (subroutineName | className | varName)

        self.__next_token()
        if self.curr_token == '.':
            self.__write_curr_token() # .
            self.__write_next_token() # subroutineName
            self.__next_token()
        
        self.__write_curr_token() # (
        self.__next_token()
        self.compile_expression_list()
        self.__write_curr_token() # )
        self.__write_next_token() # ;
        self.__next_token()

        self.__write_close('doStatement') 

    def compile_return(self):
        self.__write_open('returnStatement')

        self.__write_curr_token() # return
        self.__next_token()

        if self.curr_token != ';':
            self.compile_expression()

        self.__write_curr_token() # ;
        self.__next_token()

        self.__write_close('returnStatement') 

    def compile_expression(self):
        self.__write_open('expression')

        self.compile_term()

        while self.curr_token in {'+', '-', '*', '/', '&', '|', '<', '>', '='}:
            self.__write_curr_token()
            self.__next_token()
            self.compile_term() 

        self.__write_close('expression')

    def compile_term(self):
        self.__write_open('term')
        
        if self.curr_token == '(':
            self.__write_curr_token() # (
            self.__next_token()
            self.compile_expression()
            self.__write_curr_token() # )
            self.__next_token()
        elif self.curr_token in {'-', '~'}:
            self.__write_curr_token() # (-|~)
            self.__next_token()
            self.compile_term()
        else:

            self.__write_curr_token()

            self.__next_token()
            if self.curr_token == '[':
                self.__write_curr_token() # [
                self.__next_token()
                self.compile_expression()
                self.__write_curr_token() # ]
                self.__next_token()
            elif self.curr_token == '(':
                self.__write_curr_token() # (
                self.__next_token()
                self.compile_expression_list()
                self.__write_curr_token() # )
                self.__next_token()
            elif self.curr_token == '.':
                self.__write_curr_token() # .
                self.__write_next_token() # subroutineName
                self.__write_next_token() # (
                self.__next_token()
                self.compile_expression_list()
                self.__write_curr_token() # )
                self.__next_token()
        
        self.__write_close('term')

    def compile_expression_list(self):
        self.__write_open('expressionList')

        if self.curr_token != ')':
            self.compile_expression()
        
        while self.curr_token != ')':
            self.__write_curr_token() # ,
            self.__next_token()
            self.compile_expression()

        self.__write_close('expressionList') 

    #-----------private methods----------------
    def __write_curr_token(self):
        self.__write_token(self.curr_token_type, self.curr_token)

    def __write_next_token(self):
        self.__next_token()
        self.__write_curr_token()

    def __next_token(self):
        if self.tokenizer.has_more_tokens():
            self.tokenizer.advance()
        self.curr_token_type = self.tokenizer.token_type()
        self.curr_token = self.tokenizer.keyword()

    def __write_token(self, token_type, token):
        if (token in self.xml_formatter):
            token = self.xml_formatter[token]
        self.output_file.write('{}<{}> {} </{}>\n'.format('  ' * self.depth, token_type, token, token_type))

    def __write_open(self, name):
        self.output_file.write('{}<{}>\n'.format('  ' * self.depth, name))
        self.depth = self.depth + 1

    def __write_close(self, name):
        self.depth = self.depth - 1
        self.output_file.write('{}</{}>\n'.format('  ' * self.depth, name))
