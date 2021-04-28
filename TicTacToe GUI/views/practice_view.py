
import tkinter as tk
import tkinter.ttk as ttk

import CONST
# Components
from views.Component.TicTacToeGrid import TicTacToeGrid
from views.Component.SideSectionMenu import SideSectionMenu


####################################
#     Side Section Menu (Inherited)
####################################
class PracticeSideSectionMenu(SideSectionMenu):
    def __init__(self, master=None, controller=None):
        super().__init__(master)
        self.controller = controller

        # Stats Window - Labels and Values
        self.labels = [
            ttk.Label(self.statusFrame, text='Name:', style='SideSectionLabel.TLabel'),
            ttk.Label(self.statusFrame, text='Game Mode:', style='SideSectionLabel.TLabel'),
            ttk.Label(self.statusFrame, text='Turn:', style='SideSectionLabel.TLabel'),
            ttk.Label(self.statusFrame, text='O wins:', style='SideSectionLabel.TLabel'),
            ttk.Label(self.statusFrame, text='O losses:', style='SideSectionLabel.TLabel'),
            ttk.Label(self.statusFrame, text='X wins:', style='SideSectionLabel.TLabel'),
            ttk.Label(self.statusFrame, text='X losses:', style='SideSectionLabel.TLabel'),
            ttk.Label(self.statusFrame, text='Ties:', style='SideSectionLabel.TLabel'),
        ]
        self.fields = [
            ttk.Label(self.statusFrame, text='val', style='SideSectionValue.TLabel'),
            ttk.Label(self.statusFrame, text='Practice Mode', style='SideSectionValue.TLabel'),
            ttk.Label(self.statusFrame, text='val', style='SideSectionValue.TLabel'),
            ttk.Label(self.statusFrame, text='val', style='SideSectionValue.TLabel'),
            ttk.Label(self.statusFrame, text='val', style='SideSectionValue.TLabel'),
            ttk.Label(self.statusFrame, text='val', style='SideSectionValue.TLabel'),
            ttk.Label(self.statusFrame, text='val', style='SideSectionValue.TLabel'),
            ttk.Label(self.statusFrame, text='val', style='SideSectionValue.TLabel'),
        ]
        for i, (label, field) in enumerate( zip(self.labels, self.fields) ):
            label.grid(row=i, column=0, sticky=tk.E, pady=3 )
            field.grid(row=i, column=1, sticky=tk.W, pady=3 )

        # Buttons
        self.btns = [
            ttk.Button(self.buttonFrame, text='Vs CPU', style='SideSection.TButton',
                       command=lambda: self.controller.changeScreen(CONST.LOC_LOCAL_CPU) ),
            ttk.Button(self.buttonFrame, text='Reset', style='SideSection.TButton',
                       command=lambda: self.controller.clear_practice_board() ),
            ttk.Button(self.buttonFrame, text='Save', style='SideSection.TButton',
                       command=lambda: self.controller.saveGame() ),
            ttk.Button(self.buttonFrame, text='Load', style='SideSection.TButton',
                       command=lambda: self.controller.loadGame() ),
            ttk.Button(self.buttonFrame, text='Exit to Menu', style='SideSection.TButton',
                       command=lambda: self.controller.changeScreen(CONST.LOC_MAIN_MENU) ),
            ttk.Button(self.buttonFrame, text='Quit Game', style='SideSection.TButton',
                       command=lambda: self.controller.saveBeforeQuit() )
        ]
        for i, btn in enumerate( self.btns ):
            btn.pack(side=tk.TOP, fill=tk.X, ipady=5, pady=2)

    def update_stats(self, state):
        self.fields[0]['text'] = state.name
        self.fields[2]['text'] = 'O' if state.isOTurn else 'X'
        self.fields[3]['text'] = state.practice_Owins
        self.fields[4]['text'] = state.practice_Olosses
        self.fields[5]['text'] = state.practice_Olosses
        self.fields[6]['text'] = state.practice_Owins
        self.fields[7]['text'] = state.practice_ties


############################################
#      Game Window - Consists of all stuff
############################################
class PracticeView(ttk.Frame):
    def __init__(self, master=None, controller=None, state=None):
        super().__init__(master)
        self.controller = controller
        self.state = state

        self.grid_columnconfigure(0, weight=2, uniform='gameview')
        self.grid_columnconfigure(1, weight=1, uniform='gameview')
        self.grid_rowconfigure(0, weight=1)

        self.tooltip = ttk.Label(self, text='Tooltip goes here...', relief=tk.SUNKEN, background='#dddddd')
        self.tooltip.grid_propagate(0)
        self.tooltip.grid(row=1, column=0, columnspan=2, sticky=tk.E+tk.W+tk.S, ipady=8)

        self.tictactoegrid = TicTacToeGrid(self, controller)
        self.tictactoegrid.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W, padx=(20,5) )

        # Add Event Listener to TicTacToeGrid Buttons
        for i, btn in enumerate(self.tictactoegrid.btns):
            btn['command'] = (lambda idx: lambda: self.controller.practice_button_press(idx) )(i)

        self.sideSection = PracticeSideSectionMenu(self, controller)
        self.sideSection.grid(row=0, column=1, sticky=tk.N+tk.S+tk.E+tk.W, padx=(5,20))

    ###############################
    #   Rendering Methods
    ###############################
    def update_all(self):
        self.tictactoegrid.update_board(self.state.practice_board)
        self.sideSection.update_stats(self.state)

    def draw(self):
        self.update_all()
        self.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

