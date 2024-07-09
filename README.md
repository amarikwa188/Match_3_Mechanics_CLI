This terminal program recreates the basic mechanics of a match three game on a 4x4 grid.
The cells are numbered from 1 to 16 starting from the top-left to the bottom-right. 
The user is prompted to enter a cell number as well as a letter representing one of 4 directions(W -> up, A -> left, S -> down, D -> right).
The program then swaps the letters in the two relevant positions and checks for whether a line of at least three matching letters has been made.
The matched letters are removed from the board, the floating letters are dropped down into the appropriate position and empty cell spaces are filled with new random letters.
The user is then prompted again and the loop continues until 'exit' is entered.

*NOTE: This is not a proper game and has no win condition, time limit or score system.
