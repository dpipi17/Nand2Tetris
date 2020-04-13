import sys

symbol_table = {"R0" : 0, "R1" : 1, "R2" : 2, "R3" : 3, "R4" : 4, "R5" : 5, 
                "R6" : 6, "R7" : 7, "R8" : 8, "R9" : 9, "R10" : 10, "R11" : 11, 
                "R12" : 12, "R13" : 13, "R14" : 14, "R15" : 15, "KBD": 24576, "SCREEN": 16384, 
                "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4}

dest_dict = {"null": "000", "M": "001", "D": "010", "A": "100",
            "MD": "011", "AM": "101", "AD": "110", "AMD": "111"}

comp_dict = {"0": "0101010", "1": "0111111", "-1": "0111010", "D": "0001100", "A": "0110000", "!D": "0001101", "!A": "0110001", 
            "-D": "0001111", "-A": "0110011", "D+1": "0011111", "A+1": "0110111", "D-1": "0001110", "A-1": "0110010", "D+A": "0000010", 
            "D-A": "0010011", "A-D": "0000111", "D&A": "0000000", "D|A": "0010101", "M": "1110000", "!M": "1110001", "-M": "1110011", 
            "M+1": "1110111", "M-1": "1110010", "D+M": "1000010", "D-M": "1010011", "M-D": "1000111", "D&M": "1000000", "D|M": "1010101"}

jump_dict = {"null": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
            "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"}

variable_value_counter = 16


def a_instruction_to_binary(instruction):
    variable = instruction[1:]
    variable_value = 0
    if variable.isdigit():
        variable_value = int(variable)
    else:
        variable_value = symbol_table[variable]
    
    return '{0:016b}'.format(variable_value) + '\n'

def c_instruction_to_binary(instruction):
    comp_key = instruction

    dest_key = "null"
    if '=' in instruction:
        dest_key = instruction[: instruction.index('=')]
        comp_key = comp_key[comp_key.index('=') + 1:]
    
    jump_key = "null"
    if ";" in instruction:
        jump_key = instruction[instruction.index(';') + 1:]
        comp_key = comp_key[:comp_key.index(';')]
    
    return '111' + comp_dict[comp_key] + dest_dict[dest_key] + jump_dict[jump_key] + '\n'

def translate_to_binary(lines):
    binary_code_lines = []
    for line in lines:
        if line.startswith('@'):
            variable = line[1:]
            if not variable.isdigit() and variable not in symbol_table:
                global variable_value_counter
                symbol_table[variable] = variable_value_counter
                variable_value_counter += 1
            binary_code_lines.append(a_instruction_to_binary(line))
        else:
            binary_code_lines.append(c_instruction_to_binary(line))
    
    return binary_code_lines

def parse_input_file(input_file):
    lines = []
    line_index = 0

    while True:
        line = input_file.readline()
        if not line: 
            break
        
        line = line.strip()
        line = line.replace(" ", "")
        if not line or line.startswith('//'):
            continue
        
        if '//' in line:
            line = line[0 : line.index('//')]
        
        if line.startswith('('):
            label = line[1 : len(line) - 1]
            if label not in symbol_table:
                symbol_table[label] = line_index
            continue

        lines.append(line)
        line_index += 1

    return lines

def main(argv):
    if '.asm' not in argv[0]:
        return

    file_name = argv[0][:argv[0].index('.asm')]
    input_file = open(file_name + '.asm', 'r')
    lines = parse_input_file(input_file)
   
    binary_code_lines = translate_to_binary(lines)
    output_file = open(file_name + '.hack', 'w')
    output_file.writelines(binary_code_lines)

if __name__ == "__main__":
    main(sys.argv[1:])