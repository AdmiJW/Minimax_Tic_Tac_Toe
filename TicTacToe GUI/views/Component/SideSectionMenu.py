import tkinter as tk
import tkinter.ttk as ttk

#   The Base for Side section Menu for in-game view
#
#   Somethings to be done in inherited class:
#
#       >   The label in stats are not provided. Please add the labels in stat yourself.
#               1.  Add labels into self.labels, Suggested params:
#                       (self.statusFrame, text='val', style='SideSectionLabel.TLabel')
#               2.  Add fields into self.fields, Suggested params:
#                       (self.statusFrame, text='val', style='SideSectionValue.TLabel')
#               3.  call .grid() on each labels in self.labels. Suggested: (row=i, column=0, sticky=tk.E, pady=3 )
#               4.  call .grid() on each fields in self.fields. Suggested: (row=i, column=1, sticky=tk.W, pady=3 )
#
#       >   The buttons may vary, so is not provided. Please add that
#               1.  Add buttons into self.btns, with master as self.buttonFrame, style of 'SideSection.TButton'
#               2.  call .pack() on each buttons in self.btns. Suggested: (side=tk.TOP, fill=tk.X, ipady=5, pady=2)
#
############################
#     Side Section Menu
############################
class SideSectionMenu(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        ############
        # Logo
        ############
        ttk.Style().configure('SideSectionLogo.TLabel', font=('Courier New', 35, 'bold') )
        ttk.Style().configure('SideSectionSmart.TLabel', font=('Courier New', 15, 'bold'))
        self.logoFrame = tk.Frame(self)
        self.logoFrame.grid_columnconfigure((0,1,2), weight=1)
        self.logos = [
            ttk.Label(self.logoFrame, text='Tic', style='SideSectionLogo.TLabel', foreground='#e67e22'),
            ttk.Label(self.logoFrame, text='Tac', style='SideSectionLogo.TLabel', foreground='#2980b9'),
            ttk.Label(self.logoFrame, text='Toe', style='SideSectionLogo.TLabel', foreground='#27ae60'),
        ]
        for i, logo in enumerate(self.logos):
            logo.grid(row=0, column=i, padx=5, pady=10)
        self.smartlogo = ttk.Label(self.logoFrame, text='Smart', style='SideSectionSmart.TLabel', foreground='#8e44ad')
        self.smartlogo.place(x=230, y=55, relheight=.4, relwidth=.25)
        self.logoFrame.pack(side=tk.TOP, pady=30)

        ##########
        # Status
        ##########
        ttk.Style().configure('SideSectionLabel.TLabel', font=('Verdana', 10))
        ttk.Style().configure('SideSectionValue.TLabel', font=('Verdana', 10, 'bold'))
        self.statusFrame = tk.Frame(self, relief=tk.GROOVE, bd=5)
        self.statusFrame.pack(side=tk.TOP, fill=tk.X, pady=10)


        ##########
        # Buttons
        ##########
        ttk.Style().configure('SideSection.TButton', font=('Verdana', 10) )
        self.buttonFrame = ttk.Frame(self)
        self.buttonFrame.pack(side=tk.TOP, fill=tk.X)


