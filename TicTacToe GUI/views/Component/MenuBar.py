import tkinter as tk

import CONST

############################
#       Menu Bar
############################
class GameViewMenuBar(tk.Menu):
    def __init__(self, master=None, controller=None):
        super().__init__(master)
        self.master = master
        self.controller = controller

        self.options = tk.Menu(self, tearoff=0)
        self.options.add_command(label='Save', command=lambda: controller.saveGame() )
        self.options.add_command(label='Load', command=lambda: controller.loadGame() )
        self.options.add_separator()
        self.options.add_command(label='Back to Main Menu',
                                 command=lambda: controller.changeScreen(CONST.LOC_MAIN_MENU) )
        self.options.add_command(label='Exit', command=lambda: controller.saveBeforeQuit() )
        self.add_cascade(menu=self.options, label='Options')
        self.add_command(label='About')
