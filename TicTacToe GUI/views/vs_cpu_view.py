
import tkinter as tk
import tkinter.ttk as ttk

import CONST

# Components
from views.Component.TicTacToeGrid import TicTacToeGrid
from views.Component.SideSectionMenu import SideSectionMenu


####################################
#     Side Section Menu (Inherited)
####################################
class VsCPUSideSectionMenu(SideSectionMenu):
    def __init__(self, master=None, controller=None, state=None):
        super().__init__(master)
        self.controller = controller
        self.state = state

        # Stats Window - Labels and Values
        self.labels = [
            ttk.Label(self.statusFrame, text='Name:', style='SideSectionLabel.TLabel'),
            ttk.Label(self.statusFrame, text='Game Mode:', style='SideSectionLabel.TLabel'),
            ttk.Label(self.statusFrame, text='Wins:', style='SideSectionLabel.TLabel'),
            ttk.Label(self.statusFrame, text='Losses:', style='SideSectionLabel.TLabel'),
            ttk.Label(self.statusFrame, text='Ties:', style='SideSectionLabel.TLabel'),
        ]
        self.fields = [
            ttk.Label(self.statusFrame, text='val', style='SideSectionValue.TLabel'),
            ttk.Label(self.statusFrame, text='Vs CPU', style='SideSectionValue.TLabel'),
            ttk.Label(self.statusFrame, text='val', style='SideSectionValue.TLabel'),
            ttk.Label(self.statusFrame, text='val', style='SideSectionValue.TLabel'),
            ttk.Label(self.statusFrame, text='val', style='SideSectionValue.TLabel'),
        ]
        for i, (label, field) in enumerate( zip(self.labels, self.fields) ):
            label.grid(row=i, column=0, sticky=tk.E, pady=3 )
            field.grid(row=i, column=1, sticky=tk.W, pady=3 )

        # Buttons
        self.btns = [
            ttk.Button(self.buttonFrame, text='Practice Mode', style='SideSection.TButton',
                       command=lambda: self.controller.changeScreen(CONST.LOC_LOCAL_VS) ),
            ttk.Button(self.buttonFrame, text='Save', style='SideSection.TButton',
                       command=lambda: self.controller.saveGame()),
            ttk.Button(self.buttonFrame, text='Load', style='SideSection.TButton',
                       command=lambda: self.controller.loadGame()),
            ttk.Button(self.buttonFrame, text='Exit to Menu', style='SideSection.TButton',
                       command=lambda: self.controller.changeScreen(CONST.LOC_MAIN_MENU)),
            ttk.Button(self.buttonFrame, text='Quit Game', style='SideSection.TButton',
                       command=lambda: self.controller.saveBeforeQuit())
        ]
        for i, btn in enumerate( self.btns ):
            btn.pack(side=tk.TOP, fill=tk.X, ipady=5, pady=2)


    def update_stats(self, state):
        self.fields[0]['text'] = state.name
        self.fields[2]['text'] = state.vscpu_wins
        self.fields[3]['text'] = state.vscpu_losses
        self.fields[4]['text'] = state.vscpu_ties


############################################
#      Game Window - Consists of all stuff
############################################
class VsCpuView(ttk.Frame):
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
        for i, btns in enumerate(self.tictactoegrid.btns):
            btns['command'] = (lambda idx: lambda: self.controller.cpu_button_press(idx) )(i)

        self.sideSection = VsCPUSideSectionMenu(self, controller)
        self.sideSection.grid(row=0, column=1, sticky=tk.N+tk.S+tk.E+tk.W, padx=(5,20))

    ################################
    #   Rendering Methods
    ################################
    def update_all(self):
        self.tictactoegrid.update_board( self.state.cpu_board )
        self.sideSection.update_stats( self.state )

    def update_tooltip(self, tip):
        self.tooltip['text'] = ' ' + tip

    def draw(self):
        self.update_all()
        self.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

