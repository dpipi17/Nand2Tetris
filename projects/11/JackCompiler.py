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
        
        output_file_name = file_name[:file_name.index('.jack')] + '.vm'
        compile_engine = CompilationEngine(tokenizer, output_file_name)
        compile_engine.compile_class()

if __name__ == "__main__":
    main(sys.argv[1:])


# python3 JackCompiler.py Average/
# python3 JackCompiler.py ComplexArrays/
# python3 JackCompiler.py ConvertToBin/
# python3 JackCompiler.py Pong/
# python3 JackCompiler.py Seven/
# python3 JackCompiler.py Square/
