# ❌ Smart Tic Tac Toe ⭕️

## Introduction

Coding up a tic tac toe is simple, but coding up its AI requires knowledge in data structures and algorithms.

One might think that it is nothing but if else statements. However, the approach is vulnerable to logical error and hard to debug.

The appropriate AI algorithm for tic tac toe is __Minimax Algorithm__, which calculates possible future game states ahead of time. Topics included:
* Trees
* Depth First Search
* Backtracking
* Dynamic Programming

Credits to [Gaurav Sen's Youtube Video on Minimax algorithm](https://www.youtube.com/watch?v=KU9Ch59-4vw)

Therefore, solid foundation on data structures and algorithms is a must

---

## Usage

### 1.0 - ❌ Command Line Tic Tac Toe ⭕️

To play command line tic tac toe, you will only need:
* cmd_tictactoe.py
* states_no_heuristic.csv

Ensure that your machine has python installed, open cmd and run the following:
```
> python cmd_tictactoe.py
```

### 1.1 - ❌ GUI Tic Tac Toe ⭕️

To be constructed

### 1.2 - States.csv

The csv file `states.csv` and `states_no_heuristic.csv` consists of the game states and the best moves to make by the first and second player to move at that particular state.

The game board is nothing but tuple of size 9: (0,1,2,3,4,5,6,7,8). The token used by the first player to move is represented by integer 1, while the token used by the other player is represented by integer -1. Empty grid is represented by 0.

The column `state_heuristic` is an floating point number, representing the state's heuristic used in generation of the optimal moves. A positive value indicates the first player is at advantage, while a negative value indicates the second player is at advantage.

The column `first_mover_opt_move` and `second_mover_opt_move` is an array of indices of the tic tac toe board that stores the optimal moves to be made by the first player and second player respectively.