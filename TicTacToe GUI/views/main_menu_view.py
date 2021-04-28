import tkinter as tk
import tkinter.ttk as ttk
from PIL import ImageTk,Image

import CONST
from model.state import State


class Title(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.tic = ttk.Label(self, text='Tic', font=('Courier', 58, 'bold'), foreground='#e67e22')
        self.tic.pack(side=tk.LEFT, padx=10)
        self.tac = ttk.Label(self, text='Tac', font=('Courier', 58, 'bold'), foreground='#2980b9')
        self.tac.pack(side=tk.LEFT, padx=10)
        self.toe = ttk.Label(self, text='Toe', font=('Courier', 58, 'bold'), foreground='#27ae60')
        self.toe.pack(side=tk.LEFT, padx=10)
        self.smart = ttk.Label(self, text='Smart', font=('Verdana', 24), foreground='#8e44ad')
        self.smart.pack(side=tk.BOTTOM)


class ButtonList(ttk.Frame):
    def __init__(self, master=None, controller=None):
        super().__init__(master)
        self.master = master
        self.controller = controller

        def onMouseEnter(event):
            if not event.widget['text'].endswith(' »'):
                event.widget['text'] += ' »'
        def onMouseOut(event):
            if event.widget['text'].endswith(' »'):
                event.widget['text'] = event.widget['text'][:-2]

        ttk.Style().configure('Menu.TButton', font=('Verdana', 18) )
        self.btns = (
            ttk.Button(self, text='Start game', style='Menu.TButton',
                       command=lambda: self.controller.changeScreen(CONST.LOC_LOCAL_VS) ),
            ttk.Button(self, text='Load game', style='Menu.TButton', command=lambda: self.controller.loadGame() ),
            ttk.Button(self, text='Stats', style='Menu.TButton',
                       command=lambda: self.controller.changeScreen( CONST.LOC_STATS) ),
            ttk.Button(self, text='Exit', style='Menu.TButton', command=controller.saveBeforeQuit)
        )

        for i, btn in enumerate(self.btns):
            btn.bind('<Enter>', onMouseEnter )
            btn.bind('<Leave>', onMouseOut )
            btn.pack(pady=10, ipadx=10, ipady=5)




class MainMenu(ttk.Frame):
    def __init__(self, master=None, controller=None):
        super().__init__(master)
        self.master = master
        self.controller = controller

        self.title = Title(self)
        self.title.pack(side=tk.TOP, pady=10, padx=30)

        self.image = ImageTk.PhotoImage(Image.open('./resources/tictactoe_img.png') )
        self.imageLabel = ttk.Label(self, image=self.image)
        self.imageLabel.pack(side=tk.LEFT)

        self.btnMenu = ButtonList(self, controller)
        self.btnMenu.pack(side=tk.RIGHT, padx=10)

    def draw(self):
        self.grid(row=0, column=0, sticky=tk.N+tk.S, padx=30, pady=30)
