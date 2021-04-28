import tkinter as tk
from PIL import ImageTk, Image


############################
#       Tic Tac Toe Grid
############################
class TicTacToeGrid(tk.Frame):
    BTN_STYLE = {
        'relief': tk.RIDGE,
        'borderwidth': 4,
        'width': 20,
        'height': 10
    }

    def __init__(self, master=None, controller=None):
        super().__init__(master)
        self.controller = controller

        self.grid_columnconfigure((0,1,2), weight=1, uniform="tictactoegrid")
        self.grid_rowconfigure((0,1,2), weight=1, uniform="tictactoegrid")
        self['relief'] = tk.SUNKEN
        self['bd'] = 15

        # If the images haven't loaded yet, load in the cross and round images
        if not hasattr(TicTacToeGrid, 'CROSS_IMG'):
            TicTacToeGrid.CROSS_IMG = ImageTk.PhotoImage(Image.open('./resources/cross.png'))
            TicTacToeGrid.ROUND_IMG = ImageTk.PhotoImage(Image.open('./resources/round.png'))

        # Create the buttons for O and X
        self.btns = [ tk.Button(self, text='', **TicTacToeGrid.BTN_STYLE) for i in range(9) ]
        for i, btn in enumerate(self.btns):
            btn.grid(row=i//3, column=i % 3, sticky=tk.N+tk.E+tk.S+tk.W)


    def update_board(self, board):
        for i, token in enumerate(board):
            self.btns[i]['image'] = TicTacToeGrid.CROSS_IMG if token == -1 \
                else TicTacToeGrid.ROUND_IMG if token == 1 else ''


