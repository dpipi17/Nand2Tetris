// The game of life world consists of 2D grid 16x32, the grid is mapped in memory:
// RAM[100] == grid(0, 0)
// RAM[132] == grid(1, 0)
// RAM[611] == grid(16, 31)
//
// RAM[99] contains number of generations to iterate over the Game of life world (aka grid)
//
// Iteration rules:
// For a space that is 'populated':
// * Each cell with one or no neighbors dies, as if by solitude.
// * Each cell with four or more neighbors dies, as if by overpopulation.
// * Each cell with two or three neighbors survives.
//
// For a space that is 'empty' or 'unpopulated'
// * Each cell with three neighbors becomes populated.
//
// initial values are set by test. The are only two values allowed:
// 1 -- the cell is populated
// 0 -- the cell is empty


// ----------------PSEUDO CODE-----------------------
// iterations = M[99]
// matrix_size = 511
// main_loop_counter = 1

// arr_base = 100
// arr_end = arr_base + matrix_size
// temp_arr_base = 700
// temp_arr_end = temp_arr_base + matrix_size
// base_diff = temp_arr_base - arr_base

// JMP to (DRAWLOOPSTART)

// MAINLOOP:
// 	if main_loop_counter > iterations JMP to MAINLOOPEND	

// curr_index = temp_arr_base
// COPYLOOP:
//     if curr_index > temp_arr_end JMP to COPYLOOPEND
//     temp_arr[curr_index] = arr[curr_index - base_diff]


//     curr_index += 1;
//     JMP to COPYLOOP
// COPYLOOPEND

//     curr_index = temp_arr_base
//     i = 0
//     LOOPI:
//         if i > 15 JMP to LOOPIEND
//         j = 0

//         LOOPJ:
//             if j > 31 JMP to LOOPJEND
//             alive_neighbours = 0


//             up_left_index = curr_index - 33
//             up_index = curr_index - 32
//             up_right_index = curr_index - 31
//             left_index = curr_index - 1;
//             right_index = curr_index + 1;
//             down_left_index = curr_index + 31;
//             down_index = curr_index + 32;
//             down_right_index = curr_index + 33;

//             if (i != 0) {
//                 alive_neighbours += temp_arr[up_index]

//                 if (j != 0) {
//                     alive_neighbours += temp_arr[up_left_index]
//                 }

//                 if (j != 31) {
//                     alive_neighbours += temp_arr[up_right_index]
//                 }
//             }


//             if (i != 15) {
//                 alive_neighbours += temp_arr[down_index]

//                 if (j != 0) {
//                     alive_neighbours += temp_arr[down_left_index]
//                 }

//                 if (j != 31) {
//                     alive_neighbours += temp_arr[down_right_index]
//                 }
//             }

//             if (j != 0) {
//                 alive_neighbours += temp_arr[left_index]
//             }
            
//             if (j != 31) {
//                 alive_neighbours += temp_arr[right_index]
//             }

//             if (temp_arr[curr_index] == 1) {
//                 if (alive_neighbours < 2) {
//                     arr[curr_index - base_diff] = 0
//                 }

//                 if (alive_neighbours > 3) {
//                     arr[curr_index - base_diff] = 0
//                 }
//             }
            
//             if (temp_arr[curr_index] == 0) {
//                 if (alive_neighbours == 3) {
//                     arr[curr_index - base_diff] = 1
//                 }
//             }
        
        
//             curr_index += 1;
        
//             j = j + 1
//             JMP to LOOPJ
//         (LOOPJEND)

//         i = i + 1
//         JMP to LOOPI
//     (LOOPIEND)


// 	main_loop_counter = main_loop_counter + 1
// -------------------------------------SECOND PART------------------------------------

// screen_index = SCREEN
// screen_raw_counter = 0
// arr_index_for_screen = 0

// SCREENLOOP:
// if screen_index >= KBD JMP to SCREENLOOPEND

// matrix_index = arr_index_for_screen + arr_base

// set_bit = -1
// if (M[matrix_index] == 0) {
//     set_bit = 0
// }


// temp_screen_index = screen_index

// temp_screen_index_i = 0
// TEMPSCREENINDEXLOOP:
//     if temp_screen_index_i > 15 JMP to TEMPSCREENINDEXLOOPEND

//     M[temp_screen_index] = set_bit
//     temp_screen_index += 32
//     temp_screen_index_i += 1

//     JMP to TEMPSCREENINDEXLOOP
// (TEMPSCREENINDEXLOOPEND)

// screen_index += 1
// screen_raw_counter += 1

// if (screen_raw_counter == 32) {
//     screen_raw_counter = 0
//     screen_index += 480
// }
// arr_index_for_screen += 1
// JMP to SCREENLOOP
// (SCREENLOOPEND)

// --------------------------------------------------------------------
// 	JMP to MAINLOOP

// MAINLOOPEND


// END:
// JMP to END



//--------------HACK CODE---------------------
// iterations = M[99]
@99
D=M
@iterations
M=D

// matrix_size = 511
@511
D=A
@matrix_size
M=D

// main_loop_counter = 1
@1
D=A
@main_loop_counter
M=D

// arr_base = 100
@100
D=A 
@arr_base
M=D 

// arr_end = arr_base + matrix_size
@matrix_size
D=M
@arr_base
D=D+M
@arr_end
M=D

// temp_arr_base = 700
@700
D=A 
@temp_arr_base
M=D

// temp_arr_end = temp_arr_base + matrix_size
@temp_arr_base
D=M 
@matrix_size
D=D+M
@temp_arr_end
M=D

// base_diff = temp_arr_base - arr_base
@temp_arr_base
D=M 
@arr_base
D=D-M
@base_diff
M=D

// JMP to (DRAWLOOPSTART)
@DRAWLOOPSTART
0; JMP

// MAINLOOP:
(MAINLOOP)

// if main_loop_counter > iterations JMP to MAINLOOPEND
@main_loop_counter
D=M
@iterations
D=D-M
@MAINLOOPEND
D;JGT

// curr_index = temp_arr_base
@temp_arr_base
D=M 
@curr_index
M=D 

// COPYLOOP:
(COPYLOOP)

// if curr_index > temp_arr_end JMP to COPYLOOPEND
@curr_index
D=M
@temp_arr_end
D=D-M
@COPYLOOPEND
D; JGT

// temp_arr[curr_index] = arr[curr_index - base_diff]
@curr_index
D=M 
@base_diff
D=D-M
A=D
D=M
@curr_index
A=M
M=D

// curr_index += 1;
@curr_index
M=M+1

// JMP to COPYLOOP
@COPYLOOP
0; JMP

// COPYLOOPEND
(COPYLOOPEND)

// curr_index = temp_arr_base
@temp_arr_base
D=M 
@curr_index
M=D 

// i = 0
@i 
M=0

// LOOPI:
(LOOPI)

// if i > 15 JMP to LOOPIEND
@i 
D=M 
@15
D=D-A 
@LOOPIEND
D; JGT

// j = 0
@j
M=0

// LOOPJ:
(LOOPJ)

// if j > 31 JMP to LOOPJEND
@j
D=M 
@31
D=D-A 
@LOOPJEND
D; JGT

// alive_neighbours = 0
@alive_neighbours
M=0

// up_left_index = curr_index - 33
@curr_index
D=M 
@33 
D=D-A 
@up_left_index 
M=D 

// up_index = curr_index - 32
@curr_index
D=M 
@32
D=D-A 
@up_index 
M=D 

// up_right_index = curr_index - 31
@curr_index
D=M 
@31 
D=D-A 
@up_right_index 
M=D

// left_index = curr_index - 1;
@curr_index
D=M 
D=D-1 
@left_index 
M=D 

// right_index = curr_index + 1;
@curr_index
D=M 
D=D+1
@right_index 
M=D 

// down_left_index = curr_index + 31;
@curr_index
D=M 
@31
D=D+A 
@down_left_index 
M=D 

// down_index = curr_index + 32;
@curr_index
D=M 
@32
D=D+A 
@down_index 
M=D 

// down_right_index = curr_index + 33;
@curr_index
D=M 
@33
D=D+A 
@down_right_index 
M=D 

// if (i != 0) {
@i
D=M 
@INOTZEROBRANCHEND
D; JEQ

// alive_neighbours += temp_arr[up_index]
@up_index
D=M 
A=D 
D=M 
@alive_neighbours 
M=M+D

// if (j != 0) {
@j 
D=M 
@JNOTZEROBRANCHFIRSTEND
D; JEQ

// alive_neighbours += temp_arr[up_left_index]
@up_left_index
D=M
A=D 
D=M 
@alive_neighbours
M=M+D 

(JNOTZEROBRANCHFIRSTEND)

// if (j != 31) {
@j 
D=M 
@31
D=D-A 
@JNOT31BRANCHFIRSTEND
D; JEQ

// alive_neighbours += temp_arr[up_right_index]
@up_right_index
D=M 
A=D 
D=M 
@alive_neighbours
M=M+D

(JNOT31BRANCHFIRSTEND)

(INOTZEROBRANCHEND)

// if (i != 15) {
@i
D=M
@15 
D=D-A 
@INOT15BRANCHEND
D; JEQ

// alive_neighbours += temp_arr[down_index]
@down_index
D=M 
A=D 
D=M 
@alive_neighbours
M=M+D

// if (j != 0) {
@j 
D=M 
@JNOTZEROBRANCHSECONDEND
D; JEQ

// alive_neighbours += temp_arr[down_left_index]
@down_left_index
D=M 
A=D 
D=M 
@alive_neighbours
M=M+D

(JNOTZEROBRANCHSECONDEND)


// if (j != 31) {
@j 
D=M 
@31
D=D-A 
@JNOT31BRANCHSECONDEND
D; JEQ

// alive_neighbours += temp_arr[down_right_index]
@down_right_index
D=M 
A=D 
D=M 
@alive_neighbours
M=M+D

(JNOT31BRANCHSECONDEND)

(INOT15BRANCHEND)

// if (j != 0) {
@j 
D=M 
@JNOTZEROBRANCHTHIRDEND
D; JEQ

// alive_neighbours += temp_arr[left_index]
@left_index
D=M 
A=D 
D=M 
@alive_neighbours
M=M+D

(JNOTZEROBRANCHTHIRDEND)

// if (j != 31) {
@j 
D=M 
@31
D=D-A 
@JNOT31BRANCHTHIRDEND
D; JEQ

// alive_neighbours += temp_arr[right_index]
@right_index
D=M 
A=D 
D=M 
@alive_neighbours
M=M+D

(JNOT31BRANCHTHIRDEND)

// if (temp_arr[curr_index] == 1) {
@curr_index
D=M 
A=D
D=M
D=D-1 
@ALIVEBRANCH 
D; JNE

// if (alive_neighbours < 2) {
@alive_neighbours
D=M 
@2
D=D-A
@ALIVENEIGHBOURSLT2
D; JGE

// arr[curr_index - base_diff] = 0
@curr_index
D=M 
@base_diff 
D=D-M 
A=D 
M=0

(ALIVENEIGHBOURSLT2)

// if (alive_neighbours > 3) {
@alive_neighbours
D=M 
@3
D=D-A 
@ALIVENEIGHBOURSGT3
D; JLE

// arr[curr_index - base_diff] = 0
@curr_index
D=M 
@base_diff 
D=D-M 
A=D 
M=0

(ALIVENEIGHBOURSGT3)

(ALIVEBRANCH)

// if (temp_arr[curr_index] == 0) {
@curr_index
D=M 
A=D
D=M
@NOTALIVEBRANCH 
D; JNE

// if (alive_neighbours == 3) {
@alive_neighbours
D=M 
@3
D=D-A 
@ALIVENEIGHBOURSEQ3
D; JNE

// arr[curr_index - base_diff] = 1
@curr_index
D=M 
@base_diff 
D=D-M 
A=D 
M=1

(ALIVENEIGHBOURSEQ3)

(NOTALIVEBRANCH)


// curr_index += 1;
@curr_index
M=M+1

// j = j + 1
@j 
M=M+1

// JMP to LOOPJ
@LOOPJ
0; JMP

// (LOOPJEND)
(LOOPJEND)

// i = i + 1
@i
M=M+1

// JMP to LOOPI
@LOOPI
0; JMP

// (LOOPIEND)
(LOOPIEND)


// main_loop_counter = main_loop_counter + 1
@main_loop_counter
M=M+1

// -------------------------------------SECOND PART------------------------------------
(DRAWLOOPSTART)
// screen_index = SCREEN
@SCREEN
D=A 
@screen_index
M=D

// screen_raw_counter = 0
@screen_raw_counter
M=0

// arr_index_for_screen = 0
@arr_index_for_screen
M=0

// SCREENLOOP:
(SCRENLOOP)

// if screen_index >= KBD JMP to SCREENLOOPEND
@screen_index
D=M 
@KBD
D=D-A 
@SCRENLOOPEND
D; JGE

//matrix_index = arr_index_for_screen + arr_base
@arr_index_for_screen
D=M 
@arr_base
D=D+M 
@matrix_index
M=D 

// set_bit = -1
@set_bit
M=-1

// if (M[matrix_index] == 0) {
@matrix_index
D=M 
A=D 
D=M
@MATRIXINDEXCHECK
D; JNE

// set_bit = 0
@set_bit
M=0

(MATRIXINDEXCHECK)

// temp_screen_index = screen_index
@screen_index
D=M
@temp_screen_index
M=D

// temp_screen_index_i = 0 
@temp_screen_index_i
M=0

// TEMPSCREENINDEXLOOP:
(TEMPSCRENINDEXLOOP)

// if temp_screen_index_i > 15 JMP to TEMPSCREENINDEXLOOPEND
@temp_screen_index_i
D=M 
@15 
D=D-A 
@TEMPSCRENINDEXLOOPEND
D; JGT

// M[temp_screen_index] = set_bit
@set_bit
D=M 
@temp_screen_index
A=M
M=D 

// temp_screen_index += 32
@32
D=A 
@temp_screen_index
M=M+D

// temp_screen_index_i += 1
@temp_screen_index_i
M=M+1

// JMP to TEMPSCREENINDEXLOOP
@TEMPSCRENINDEXLOOP
0; JMP

(TEMPSCRENINDEXLOOPEND)

// screen_index += 1
@screen_index
M=M+1

// screen_raw_counter += 1
@screen_raw_counter
M=M+1

// if (screen_raw_counter == 32) {
@screen_raw_counter
D=M 
@32
D=D-A
@SCRENRAWCOUNTERNEQ32 
D; JNE

// screen_raw_counter = 0
@screen_raw_counter
M=0

//  screen_index += 480
@480
D=A
@screen_index
M=M+D

(SCRENRAWCOUNTERNEQ32)

// arr_index_for_screen += 1
@arr_index_for_screen
M=M+1

// JMP to SCREENLOOP
@SCRENLOOP
0; JMP

(SCRENLOOPEND)

// -------------------------------------------------------------------------------

// JMP to MAINLOOP
@MAINLOOP
0;JMP

// MAINLOOPEND
(MAINLOOPEND)

(END)
@END
0;JMP