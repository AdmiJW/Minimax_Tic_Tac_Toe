import random
import tkinter.messagebox as tkm
import tkinter.filedialog as tkf
import tkinter.simpledialog as tkin
import os
import json
import jsonschema
import csv

import CONST

#############################################
# Initialization
#############################################
# Ensure that there is a savedir directory
dirpath = os.path.dirname(__file__)
savedir = os.path.join(dirpath, '..', 'save')
try:
    os.mkdir(savedir)
except FileExistsError:
    pass

FIRST_MOVER_AI = {}
SECOND_MOVER_AI = {}
# Load in the smart, impossible to beat AI (Aka minimax algorithm generated states)
with open('states_no_heuristic.csv', 'r') as file:
    reader = csv.DictReader(file)
    for entry in reader:
        state = tuple( map(int, entry['state'][1:-1].split(',') ) )
        first_mover_opt_move = tuple( map(int, entry['first_mover_opt_move'][1:-1].split(',') ) )
        second_mover_opt_move = tuple(map(int, entry['second_mover_opt_move'][1:-1].split(',')))
        FIRST_MOVER_AI[ state ] = first_mover_opt_move
        SECOND_MOVER_AI[ state ] = second_mover_opt_move



############################
#   State Class
############################
class State:
    # TicTacToe Winning Positions
    WINNING_POS = (
        (0,1,2), (3,4,5), (6,7,8),
        (0,3,6), (1,4,7), (2,5,8),
        (0,4,8), (2,4,6)
    )
    # Validator for player save data
    SAVE_DATA_SCHEMA = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "playtime": {"type": "number"},
            "cpu_board": {"type": "array", "minItems": 9, "maxItems": 9},
            "isPlayerFirst": {"type": "boolean"},
            "vscpu_wins": {"type": "number"},
            "vscpu_losses": {"type": "number"},
            "vscpu_ties": {"type": "number"},
            "practice_board": {"type": "array", "minItems": 9, "maxItems": 9},
            "isOFirst": {"type": "boolean"},
            "isOTurn": {"type": "boolean"},
            "practice_Owins": {"type": "number"},
            "practice_Olosses": {"type": "number"},
            "practice_ties": {"type": "number"},
        },
        "minProperties": 12,
        "additionalProperties": False
    }

    ##############################
    # Game State Constructor
    ##############################
    def __init__(self):
        self.name = "Guest"
        self.playtime = 0
        self.fileloc = None

        # Vs CPU States
        self.cpu_board = [0] * 9
        self.isPlayerFirst = True
        self.vscpu_wins = 0
        self.vscpu_losses = 0
        self.vscpu_ties = 0

        # Practice Board States
        self.practice_board = [0] * 9
        self.isOFirst = True
        self.isOTurn = True
        self.practice_Owins = 0
        self.practice_Olosses = 0
        self.practice_ties = 0


    ##################################
    #   Game Core Logics
    ##################################
    # Adds Token, and change player turn if successful.
    # If add attempt is unsuccessful, returns False
    def add_token(self, game_mode, position):
        assert game_mode in (CONST.LOC_LOCAL_VS, CONST.LOC_LOCAL_CPU)
        assert position in range(9)

        board = self.practice_board if game_mode == CONST.LOC_LOCAL_VS else self.cpu_board
        turn = self.isOTurn if game_mode == CONST.LOC_LOCAL_VS else self.isPlayerFirst

        if board[position]: return False
        board[position] = 1 if turn else -1
        if game_mode == CONST.LOC_LOCAL_VS:
            self.isOTurn = not self.isOTurn
        return True


    # Cpu makes a move
    def cpu_moves(self):
        board = tuple(self.cpu_board)
        moves = SECOND_MOVER_AI[ board ] if self.isPlayerFirst else FIRST_MOVER_AI[ board ]
        choice = random.choice(moves)

        self.cpu_board[choice] = -1 if self.isPlayerFirst else 1


    # Called when a game is set. Sets appropriate states
    def game_set(self, game_mode, winner):
        assert game_mode in (CONST.LOC_LOCAL_VS, CONST.LOC_LOCAL_CPU)
        assert winner in (-1,0,1)

        # Clears the board
        board = self.practice_board if game_mode == CONST.LOC_LOCAL_VS else self.cpu_board
        State.clear_board(board)

        if game_mode == CONST.LOC_LOCAL_VS:
            self.practice_Owins += 1 if winner == 1 else 0
            self.practice_Olosses += 1 if winner == -1 else 0
            self.practice_ties += 1 if not winner else 0
            self.isOFirst = self.isOTurn = not self.isOFirst
        else:
            self.vscpu_wins += 1 if winner == 1 and self.isPlayerFirst else 0
            self.vscpu_losses += 1 if winner == 1 and not self.isPlayerFirst else 0
            self.vscpu_ties += 1 if winner == 0 else 0
            self.isPlayerFirst = not self.isPlayerFirst


    ################################
    #   Save and Load Games
    ################################
    # Prompt to save if have unsaved changes
    def promptSave(self):
        if self.name == 'Guest':
            return True
        ans = tkm.askyesnocancel('Unsaved Changes', "Do you want to save your game first?")
        if ans:
            self.saveGame()
        return ans is not None


    # Saving
    def saveGame(self):
        # Player haven't entered their names. Ask to set their name
        if self.name == 'Guest':
            tkm.showinfo("Name is not set", "You haven't set a name for yourself. Simply Enter your name in the next"
                                            "window", icon=tkm.INFO)
            name = tkin.askstring("Set Name", "Enter your name: ")
            if not isinstance(name, str) or not len(name):
                tkm.showwarning("Invalid Name", "Your name is Invalid. Game is not saved...", icon=tkm.WARNING)
                return False
            self.name = name

        # No previously saved file. Ask for save file location
        if self.fileloc is None or not os.path.isfile(self.fileloc):
            tkm.showinfo("Select Save Location", "Select a file location and filename to save your game", icon=tkm.INFO)
            fileloc = tkf.asksaveasfilename(title='Select Save', initialdir=savedir, filetypes=(('JSON', '*.json'),),
                                  defaultextension='.json', )
            if not os.path.isfile(fileloc):
                tkm.showwarning("Invalid Destination", "Save file destination Invalid. Game is not saved...",
                                icon=tkm.WARNING)
                return False
            self.fileloc = fileloc

        # Save the file
        with open(self.fileloc, 'w') as savefile:
            json.dump(self.getSaveDict(), savefile)
        tkm.showinfo("Save success", f'[{self.name}] - Game saved!', icon=tkm.INFO)
        return True


    # Loading
    def loadGame(self):
        # If there are unsaved data, prompt to save first
        if self.name != 'Guest' and not self.promptSave():
            return False

        # Pop up file explorer window to select a file path
        save_path = tkf.askopenfilename(title='Open save file...', initialdir=savedir, filetypes=(('JSON', '*.json'),))
        if not save_path.endswith('.json'):
            if len(save_path):
                tkm.showerror('Invalid File', "Unable to load the save file specified. The save "
                                              "should be a json file", icon=tkm.ERROR)
            return False

        # Tries to read from the selected save file
        try:
            with open(save_path, 'r') as save:
                save_data = json.load(save)
                jsonschema.validate(save_data, State.SAVE_DATA_SCHEMA)
        except (jsonschema.ValidationError, IOError) as e:
            tkm.showerror("Invalid Save File", "The data in the save file is corrupted. Have you selected the wrong"
                                               "save?", icon=tkm.ERROR)
            return False

        # Loads save.
        self.fileloc = save_path
        self.loadSave(save_data)
        tkm.showinfo("Game Loaded", f'Welcome back {save_data["name"]}')
        return True


    #################################
    # Utilities Functions
    #################################
    # Used to load save file in dict (Parsed JSON) format
    def loadSave(self, state: dict):
        for key in state.keys():
            if hasattr(self, key):
                setattr(self, key, state[key] )

    # Returns the game state in Dictionary format for saving into json file
    def getSaveDict(self):
        return {
            "name": self.name,
            "playtime": self.playtime,
            "cpu_board": self.cpu_board,
            "isPlayerFirst": self.isPlayerFirst,
            "vscpu_wins": self.vscpu_wins,
            "vscpu_losses": self.vscpu_losses,
            "vscpu_ties": self.vscpu_ties,
            "practice_board": self.practice_board,
            "isOFirst": self.isOFirst,
            "isOTurn": self.isOTurn,
            "practice_Owins": self.practice_Owins,
            "practice_Olosses": self.practice_Olosses,
            "practice_ties": self.practice_ties,
        }

    # Time increment
    def tickTime(self):
        self.playtime += 1


    # Given a State, checks if whoever is winning, a tie, or simply non-deterministic state
    # Returns   None if non-determinstic state
    #           1 if O (Represented in board as '1') wins
    #           -1 if -1 (Represented in board as '-1') wins
    #           0 if tie
    @staticmethod
    def checkWinningState(board):
        for pos in State.WINNING_POS:
            if board[pos[0]] == board[pos[1]] == board[pos[2]] and board[pos[0]] != 0:
                return 1 if board[pos[0]] == 1 else -1
        return 0 if all(board) else None


    # Given a board reference, clears the board
    @staticmethod
    def clear_board(board):
        for i in range(9):
            board[i] = 0


    def __repr__(self):
        return f'''
        =======================================
                    Game State
        =======================================
        Name:        : {self.name} - {type(self.name)}
        Save File    : {self.fileloc} - {type(self.fileloc)}
        
        =======================================
                        Vs CPU
        =======================================
        Board        : {self.cpu_board} - {type(self.cpu_board)}
        isPlayerFirst: {self.isPlayerFirst} - {type(self.isPlayerFirst)}
        Wins         : {self.vscpu_wins} - {type(self.vscpu_wins)}
        Losses       : {self.vscpu_losses} - {type(self.vscpu_losses)}
        Ties:        : {self.vscpu_ties} - {type(self.vscpu_ties)}
        
        =======================================
                      Practice
        =======================================
        Board        : {self.practice_board} - {type(self.practice_board)}
        O's Turn     : {self.isOTurn} - {type(self.isOTurn)}
        Wins:        : {self.practice_Owins} - {type(self.practice_Owins)}
        Losses       : {self.practice_Olosses} - {type(self.practice_Olosses)}
        Ties         : {self.practice_ties} - {type(self.practice_ties)}
        '''
