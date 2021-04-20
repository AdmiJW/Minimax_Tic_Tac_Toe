import csv
import os
import random

state_first_mover_move = {}
state_second_mover_move = {}

# Read the generated states from csv file
print("Loading Smart Tic Tac Toe AI...")
with open('states_no_heuristic.csv', 'r', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for entry in reader:
        state = tuple( map(int, entry['state'][1:-1].split(',') ) )
        if entry['first_mover_opt_move']:
            state_first_mover_move[state] = tuple( map(int, entry['first_mover_opt_move'][1:-1].split(',') ) )
        if entry['second_mover_opt_move']:
            state_second_mover_move[state] = tuple( map(int, entry['second_mover_opt_move'][1:-1].split(',') ) )
print("Loading Done!")
os.system('cls')

# ==================================
#       Helper Functions
# ==================================
win_positions = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6)
)


# Return 1 if first mover (O) wins, Returns -1 if second mover (X) wins, Returns 0 if tie
# Returns None otherwise
def checkWinning(state):
    for pos in win_positions:
        if state[pos[0]] == state[pos[1]] == state[pos[2]] and state[pos[0]] != 0:
            return 1 if state[pos[0]] == 1 and game_state['isPlayerFirstMove'] else -1
    if all(state):
        return 0
    return None


def printTicTacToeBoard( board ):
    def mapper(token):
        return 'O' if token == 1 else 'X' if token == -1 else ' '

    board = tuple( map(lambda x: mapper(x), board) )
    board = [ board[i:i+3] for i in range(0, 9, 3)]

    for row in board:
        print('', *row, '', sep=' | ')


def getInput( prompt='', values=None ):
    res = input(prompt)
    while values is not None and res not in values:
        print("Invalid input. Please Try again")
        res = input(prompt)
    return res


# ========================================
#                   Game
# ========================================
# Game state
game_state = {
    "isPlayerFirstMove": True,
    "wins": 0,
    "losses": 0,
    "ties": 0
}


# How to Play Screen
def howToPlay():
    os.system('cls')
    os.system('color 0C')
    print('=============================')
    print("         How to Play")
    print("=============================")
    print("The game starts with either you or computer first moves")
    print("Every turn, the game will print out the tic tac toe board. Example:")
    print("| 0 | 1 | 2 |")
    print("| 3 | 4 | 5 |")
    print("| 6 | 7 | 8 |")
    print("\nAs you can see, every grid is numbered from 0 to 8. When it is your turn, you will")
    print("be prompted to input one of the available numbers to make your move\n")
    print("The first player to move will always be 'O', while the second player to move will be 'X'")
    print("First player to put 3 of their tokens aligned vertically, horizontally or diagonally, will win\n")
    getInput("Press Enter to Continue...")


# Player's Turn
def player_turn(board):
    print('=========================')
    print('       Your Turn!')
    print('=========================')
    printTicTacToeBoard(board)
    while True:
        choice = int( getInput("Please Enter a grid [0-8] to fill in your token: ", set(map(str, range(9) ) ) ) )
        if board[choice] == 0:
            board[choice] = 1 if game_state['isPlayerFirstMove'] else -1
            print("You inserted at grid", choice)
            break
        else:
            print("Occupied grid. Enter again")
    printTicTacToeBoard(board)
    getInput("\nPress Enter to Continue...\n")

# Computer's Turn
def cpu_turn(board):
    print('=========================')
    print('       CPU\'S Turn!')
    print('=========================')
    choice = state_second_mover_move[tuple(board)] if game_state['isPlayerFirstMove'] \
        else state_first_mover_move[tuple(board)]
    choice = int( random.choice(choice) )

    board[choice] = -1 if game_state['isPlayerFirstMove'] else 1
    print("Computer Inserted at grid", choice)
    printTicTacToeBoard(board)
    getInput("\nPress Enter to Continue...\n")


# Game Screen
def playGame():
    while True:
        os.system('cls')
        os.system('color 0E')
        print("==============================")
        print("          GAME START")
        print("==============================\n")

        if game_state['isPlayerFirstMove']:
            print("\nFor this game, you are the first to move. You are token 'O'!")
        else:
            print("\nFor this game, computer first moves. You are token 'X'!")
        getInput('Press Enter to continue...\n')

        isPlayerTurn = game_state['isPlayerFirstMove']
        board = [0] * 9

        # Loop rounds
        while checkWinning(tuple(board)) is None:
            os.system('cls')
            if isPlayerTurn:
                player_turn(board)
            else:
                cpu_turn(board)
            isPlayerTurn = not isPlayerTurn

        # A game concluded
        os.system('cls')
        printTicTacToeBoard(board)
        print('Game Ended...')
        result = checkWinning(tuple(board))
        if result == 1:
            print("===================================")
            print("   You've won. Congratulations")
            print("===================================")
            game_state['wins'] += 1
        elif result == -1:
            print("===================================")
            print("     Oops! You've lost to CPU")
            print("===================================")
            game_state['losses'] += 1
        else:
            print("===================================")
            print("      The game ended in a Tie")
            print("===================================")
            game_state['ties'] += 1

        game_state['isPlayerFirstMove'] = not game_state['isPlayerFirstMove']

        print("1 - Rematch")
        print("2 - Back to Main Menu")
        choice = getInput("Enter your choice: ", ("1", "2") )
        if choice == '2': break


# Main Game Loop
while True:
    os.system('cls')
    os.system('color 0f')
    print("==============================")
    print("     SMARTER TIC TAC TOE")
    print("==============================")

    print("1 - How to Play")
    print("2 - Vs Smart Computer")
    print("3 - Exit")

    selection = getInput("Enter your choice: ", ("1", "2", "3") )
    if selection == "1":
        howToPlay()
    elif selection == "2":
        playGame()
    else:
        os.system('cls')
        os.system('color 03')
        print('=============================')
        print('            Summary')
        print(f'You won: {game_state["wins"]} time(s)')
        print(f'You lost: {game_state["losses"]} time(s)')
        print(f'You tie: {game_state["ties"]} time(s)')
        print("      Thanks for playing")
        print("=============================")
        break
