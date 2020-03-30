// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.


// n = M[R0]
// mult = 0
// i = 1
//
//
//LOOP:
//	if i > n JMP to LOOPEND	
//	mult = mult + M[R1]
//	i = i + 1
//	JMP to LOOP
//
//LOOPEND
//
//	M[R2] = mult
//	while(true)


@R0
D=M
@n
M=D

@mult
M=0

@i
M=1

(LOOP)
@i
D=M
@n
D=D-M
@LOOPEND
D;JGT

@R1
D=M
@mult
M=M+D

@i
M=M+1

@LOOP
0;JMP

(LOOPEND)
@mult
D=M
@R2
M=D

(END)
@END
0;JMP





