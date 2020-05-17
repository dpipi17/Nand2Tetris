import re
import sys
import itertools

class JackTokenizer: 

    def __init__(self, input_file_path):
        if (not input_file_path.endswith('.jack')):
            print('jack tokenizer only works for jack files')
            return

        file = open(input_file_path,'r')
        content = file.read()
        file.close()

        content = self.__without_comments(content)
        self.tokens_tuple = self.__get_tokens_array(content)
        self.index = -1

    def has_more_tokens(self):
        return self.index < len(self.tokens_tuple) - 1

    def advance(self):
        self.index = self.index + 1

    def token_type(self):
        return self.tokens_tuple[self.index][1]

    def keyword(self):
        return self.tokens_tuple[self.index][0]

    def symbol(self):
        return self.tokens_tuple[self.index][0]

    def identifier(self):
        return self.tokens_tuple[self.index][0]

    def int_val(self):
        return self.tokens_tuple[self.index][0]

    def string_val(self):
        return self.tokens_tuple[self.index][0]

    # ------ private methods ------

    def __without_comments(self, content):
        block_pattern = re.compile(r'((/\*).*(\*/))')
        in_line_patthern = re.compile(r'(//.*)')
        api_block_pathern = re.compile(r'((/\*{2}).*(\*/))', flags=re.S)
        
        res = re.sub(block_pattern, '', content)
        res = re.sub(in_line_patthern, '', res)
        res = re.sub(api_block_pathern, '', res)
        
        return res

    def __get_tokens_array(self, content):
        re_keyword = re.compile(r'(class|constructor|function|method|field|static|var|int|char|boolean|void|true|false|null|this|let|do|if|else|while|return)')
        re_symbol  = re.compile(r'([{}()[\].,;+\-*/&|<>=~])')
        re_integer_constant = re.compile(r'(\d+)')
        re_string_constant = re.compile(r'"(.*)"')
        re_identifier = re.compile(r'([a-zA-Z_]\w*)')

        regexes = [re_keyword, re_symbol, re_integer_constant, re_string_constant, re_identifier]
        pattern_combined = '|'.join(x.pattern for x in regexes)
        re_combined = re.compile(pattern_combined)

        all_matches = re_combined.findall(content)
        flat_matches = list(itertools.chain(*all_matches))
        tokens = [match for match in flat_matches if match]

        tokens_tuple = []
        for token in tokens:
            if re_keyword.match(token):
                tokens_tuple.append((token, 'keyword'))
            elif re_symbol.match(token):
                tokens_tuple.append((token, 'symbol'))
            elif re_integer_constant.match(token):
                tokens_tuple.append((token, 'integerConstant'))
            elif token in re_string_constant.findall(content):
                tokens_tuple.append((token, 'stringConstant')) 
            elif re_identifier.match(token):
                tokens_tuple.append((token, 'identifier')) 

        return tokens_tuple



def main(argv):
    tokenizer = JackTokenizer(argv[0])
    file_path = argv[0][:argv[0].index('.jack')]
   
    output_file = open(file_path + 'TMY.xml', 'w')
    lines = ['<tokens>\n']
    xml_formatter = {'<' : '&lt;', '>' : '&gt;', '"' : '&quot;', '&' : '&amp;'}

    while tokenizer.has_more_tokens():
        tokenizer.advance()
        token_type = tokenizer.token_type()
        
        if token_type == 'keyword':
            lines.append('<{}> {} </{}>\n'.format(token_type, tokenizer.keyword(), token_type))
        elif token_type == 'symbol':
            token = tokenizer.symbol()
            if token in xml_formatter:
                token = xml_formatter[token]
            lines.append('<{}> {} </{}>\n'.format(token_type, token, token_type))
        elif token_type == 'integerConstant':
            lines.append('<{}> {} </{}>\n'.format(token_type, tokenizer.int_val(), token_type))
        elif token_type == 'stringConstant':
            lines.append('<{}> {} </{}>\n'.format(token_type, tokenizer.string_val(), token_type))
        elif token_type == 'identifier':
            lines.append('<{}> {} </{}>\n'.format(token_type, tokenizer.identifier(), token_type))

    lines.append('</tokens>\n')
    output_file.writelines(lines)
    output_file.close()

if __name__ == "__main__":
    main(sys.argv[1:])


# python3 JackTokenizer.py ArrayTest/Main.jack
# python3 JackTokenizer.py ExpressionLessSquare/Main.jack 
# python3 JackTokenizer.py ExpressionLessSquare/Square.jack
# python3 JackTokenizer.py ExpressionLessSquare/SquareGame.jack
# python3 JackTokenizer.py Square/Main.jack
# python3 JackTokenizer.py Square/Square.jack 
# python3 JackTokenizer.py Square/SquareGame.jack

# ./TextComparer.sh /home/deme/Documents/Nand/projects2020spring-dpipi17/projects/10/ArrayTest/MainT.xml /home/deme/Documents/Nand/projects2020spring-dpipi17/projects/10/ArrayTest/MainTMY.xml
# ./TextComparer.sh /home/deme/Documents/Nand/projects2020spring-dpipi17/projects/10/ExpressionLessSquare/MainT.xml /home/deme/Documents/Nand/projects2020spring-dpipi17/projects/10/ExpressionLessSquare/MainTMY.xml 
# ./TextComparer.sh /home/deme/Documents/Nand/projects2020spring-dpipi17/projects/10/ExpressionLessSquare/SquareT.xml /home/deme/Documents/Nand/projects2020spring-dpipi17/projects/10/ExpressionLessSquare/SquareTMY.xml 
# ./TextComparer.sh /home/deme/Documents/Nand/projects2020spring-dpipi17/projects/10/ExpressionLessSquare/SquareGameT.xml /home/deme/Documents/Nand/projects2020spring-dpipi17/projects/10/ExpressionLessSquare/SquareGameTMY.xml
# ./TextComparer.sh /home/deme/Documents/Nand/projects2020spring-dpipi17/projects/10/Square/MainT.xml /home/deme/Documents/Nand/projects2020spring-dpipi17/projects/10/Square/MainTMY.xml 
# ./TextComparer.sh /home/deme/Documents/Nand/projects2020spring-dpipi17/projects/10/Square/SquareT.xml /home/deme/Documents/Nand/projects2020spring-dpipi17/projects/10/Square/SquareTMY.xml 
# ./TextComparer.sh /home/deme/Documents/Nand/projects2020spring-dpipi17/projects/10/Square/SquareGameT.xml /home/deme/Documents/Nand/projects2020spring-dpipi17/projects/10/Square/SquareGameTMY.xml