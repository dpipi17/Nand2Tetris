@256
D=A
@SP
M=D
@Sys.init&ret0
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
A=M
D=A
@0
D=D-A
@5
D=D-A
@ARG
M=D
@SP
A=M
D=A
@LCL
M=D
@Sys.init
0;JMP
(Sys.init&ret0)
//---------------------FunctionCalls/FibonacciElement/Sys.vm Hack code-----------------
// function Sys.init 0
(Sys.init)
// push constant 4
@4
D=A
@SP
A=M
M=D
@SP
M=M+1
// call Main.fibonacci 1
@Main.fibonacci&ret1
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
A=M
D=A
@1
D=D-A
@5
D=D-A
@ARG
M=D
@SP
A=M
D=A
@LCL
M=D
@Main.fibonacci
0;JMP
(Main.fibonacci&ret1)
// label WHILE
(WHILE)
// goto WHILE
@WHILE
0; JMP
//---------------------FunctionCalls/FibonacciElement/Main.vm Hack code-----------------
// function Main.fibonacci 0
(Main.fibonacci)
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
// lt
@SP
M=M-1
A=M
D=M
@SP
M=M-1
@SP
A=M
D=M-D
@TRUELABEL0
D;JLT
@SP
A=M
M=0
@FALSELABEL0
0;JMP
(TRUELABEL0)
@SP
A=M
M=-1
(FALSELABEL0)
@SP
M=M+1
// if-goto IF_TRUE
@SP
M=M-1
A=M
D=M
@IF_TRUE
D; JNE
// goto IF_FALSE
@IF_FALSE
0; JMP
// label IF_TRUE
(IF_TRUE)
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
// return
@LCL
D=M
@endframe
M=D
@endframe
D=M
@5
D=D-A
A=D
D=M
@retAddr
M=D
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D
@ARG
D=M
@SP
M=D+1
@endframe
D=M
D=D-1
A=D
D=M
@THAT
M=D
@endframe
D=M
@2
D=D-A
A=D
D=M
@THIS
M=D
@endframe
D=M
@3
D=D-A
A=D
D=M
@ARG
M=D
@endframe
D=M
@4
D=D-A
A=D
D=M
@LCL
M=D
@retAddr
A=M
0; JMP
// label IF_FALSE
(IF_FALSE)
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
// call Main.fibonacci 1
@Main.fibonacci&ret2
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
A=M
D=A
@1
D=D-A
@5
D=D-A
@ARG
M=D
@SP
A=M
D=A
@LCL
M=D
@Main.fibonacci
0;JMP
(Main.fibonacci&ret2)
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
// call Main.fibonacci 1
@Main.fibonacci&ret3
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
A=M
D=A
@1
D=D-A
@5
D=D-A
@ARG
M=D
@SP
A=M
D=A
@LCL
M=D
@Main.fibonacci
0;JMP
(Main.fibonacci&ret3)
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
// return
@LCL
D=M
@endframe
M=D
@endframe
D=M
@5
D=D-A
A=D
D=M
@retAddr
M=D
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D
@ARG
D=M
@SP
M=D+1
@endframe
D=M
D=D-1
A=D
D=M
@THAT
M=D
@endframe
D=M
@2
D=D-A
A=D
D=M
@THIS
M=D
@endframe
D=M
@3
D=D-A
A=D
D=M
@ARG
M=D
@endframe
D=M
@4
D=D-A
A=D
D=M
@LCL
M=D
@retAddr
A=M
0; JMP