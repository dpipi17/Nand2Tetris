//---------------------ProgramFlow/FibonacciSeries/FibonacciSeries.vm Hack code-----------------
// push argument 1
@ARG
D=M
@1
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// pop pointer 1
@R4
D=A
@R15
M=D
@SP
M=M-1
A=M
D=M
@R15
A=M
M=D
// push constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop that 0
@THAT
D=M
@0
A=D+A
D=A
@R15
M=D
@SP
M=M-1
A=M
D=M
@R15
A=M
M=D
// push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop that 1
@THAT
D=M
@1
A=D+A
D=A
@R15
M=D
@SP
M=M-1
A=M
D=M
@R15
A=M
M=D
// push argument 0
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// push constant 2
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
// sub
@SP
M=M-1
A=M
D=M
@SP
M=M-1
@SP
A=M
M=M-D
@SP
M=M+1
// pop argument 0
@ARG
D=M
@0
A=D+A
D=A
@R15
M=D
@SP
M=M-1
A=M
D=M
@R15
A=M
M=D
// label MAIN_LOOP_START
(MAIN_LOOP_START)
// push argument 0
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// if-goto COMPUTE_ELEMENT
@SP
M=M-1
A=M
D=M
@COMPUTE_ELEMENT
D; JNE
// goto END_PROGRAM
@END_PROGRAM
0; JMP
// label COMPUTE_ELEMENT
(COMPUTE_ELEMENT)
// push that 0
@THAT
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// push that 1
@THAT
D=M
@1
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// add
@SP
M=M-1
A=M
D=M
@SP
M=M-1
@SP
A=M
M=M+D
@SP
M=M+1
// pop that 2
@THAT
D=M
@2
A=D+A
D=A
@R15
M=D
@SP
M=M-1
A=M
D=M
@R15
A=M
M=D
// push pointer 1
@R4
D=M
@SP
A=M
M=D
@SP
M=M+1
// push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
// add
@SP
M=M-1
A=M
D=M
@SP
M=M-1
@SP
A=M
M=M+D
@SP
M=M+1
// pop pointer 1
@R4
D=A
@R15
M=D
@SP
M=M-1
A=M
D=M
@R15
A=M
M=D
// push argument 0
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
// sub
@SP
M=M-1
A=M
D=M
@SP
M=M-1
@SP
A=M
M=M-D
@SP
M=M+1
// pop argument 0
@ARG
D=M
@0
A=D+A
D=A
@R15
M=D
@SP
M=M-1
A=M
D=M
@R15
A=M
M=D
// goto MAIN_LOOP_START
@MAIN_LOOP_START
0; JMP
// label END_PROGRAM
(END_PROGRAM)
