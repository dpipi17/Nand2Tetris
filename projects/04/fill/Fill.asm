// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.


//	while(true) {
//		setbits = 0
//		if M[KBD] == 0:
//			setbits = -1
//		
//		for (i = SCREEN; i < KBD; i++) {
//			M[i] = setbits
//		}
//	}



(WHILETRUE)
@setbits
M=-1  // setbits = -1

@KBD
D=M   
@POSITIVE
D; JGT   // if kbd_value > 0 jmp to positive

@setbits
M=0   // setbits = 0

(POSITIVE)
@SCREEN
D=A
@i	// i = SCREEN
M=D

(LOOP)
@i
D=M	
@KBD
D=D-A	// temp = i - KBD

@LOOPEND
D;JEQ  // if temp == 0 jump to LOOPEND

@setbits
D=M
@i
A=M	
M=D	//M[i] = setbits

@i
M=M+1  // i++

@LOOP
0; JMP // jump to LOOP
(LOOPEND)

@WHILETRUE
0;JMP
