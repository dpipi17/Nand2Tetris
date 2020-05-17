import sys
from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine
import os
from os import walk


def main(argv):
    file_names = []
    consol_input = argv[0]

    if '.jack' in consol_input:
        file_names.append(consol_input)
    elif os.path.isdir(consol_input):
        for (dirpath, _, filenames) in walk(consol_input):
            file_names.extend(filter(lambda x: '.jack' in x, [(dirpath + ('/' if dirpath[-1] != '/' else '') + filename) for filename in filenames]))
    else:
        print('please enter .jack file or directory with .jack files')
        return
    

    for file_name in file_names:
        tokenizer = JackTokenizer(file_name)
        
        output_file_name = file_name[:file_name.index('.jack')] + 'MY.xml'
        output_file = open(output_file_name, 'w')
        compile_engine = CompilationEngine(tokenizer, output_file)

        compile_engine.compile_class()
        output_file.close()

        
        
   

if __name__ == "__main__":
    main(sys.argv[1:])

# python3 JackAnalyzer.py ArrayTest/
# python3 JackAnalyzer.py ExpressionLessSquare/
# python3 JackAnalyzer.py Square/

# ./TextComparer.sh /home/deme/Documents/Nand/projects2020spring-dpipi17/projects/10/ArrayTest/Main.xml /home/deme/Documents/Nand/projects2020spring-dpipi17/projects/10/ArrayTest/MainMY.xml
# ./TextComparer.sh /home/deme/Documents/Nand/projects2020spring-dpipi17/projects/10/ExpressionLessSquare/Main.xml /home/deme/Documents/Nand/projects2020spring-dpipi17/projects/10/ExpressionLessSquare/MainMY.xml 
# ./TextComparer.sh /home/deme/Documents/Nand/projects2020spring-dpipi17/projects/10/ExpressionLessSquare/Square.xml /home/deme/Documents/Nand/projects2020spring-dpipi17/projects/10/ExpressionLessSquare/SquareMY.xml 
# ./TextComparer.sh /home/deme/Documents/Nand/projects2020spring-dpipi17/projects/10/ExpressionLessSquare/SquareGame.xml /home/deme/Documents/Nand/projects2020spring-dpipi17/projects/10/ExpressionLessSquare/SquareGameMY.xml
# ./TextComparer.sh /home/deme/Documents/Nand/projects2020spring-dpipi17/projects/10/Square/Main.xml /home/deme/Documents/Nand/projects2020spring-dpipi17/projects/10/Square/MainMY.xml 
# ./TextComparer.sh /home/deme/Documents/Nand/projects2020spring-dpipi17/projects/10/Square/Square.xml /home/deme/Documents/Nand/projects2020spring-dpipi17/projects/10/Square/SquareMY.xml 
# ./TextComparer.sh /home/deme/Documents/Nand/projects2020spring-dpipi17/projects/10/Square/SquareGame.xml /home/deme/Documents/Nand/projects2020spring-dpipi17/projects/10/Square/SquareGameMY.xml