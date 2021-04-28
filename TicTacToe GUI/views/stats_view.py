import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk

import CONST


# Side Bar for Title, Logo and Return Button
class SideBar(ttk.Frame):
    def __init__(self, master=None, controller=None):
        super().__init__(master)

        self.grid_rowconfigure(0, weight=1)
        # If the images haven't loaded yet, load in the stats logo
        if not hasattr(SideBar, 'LOGO_IMG'):
            SideBar.STATS_LOGO = ImageTk.PhotoImage(Image.open('./resources/analytics.png'))

        # Widgets
        ttk.Style().configure('StatsTitle.TLabel', font=('Verdana', 32, 'bold'))
        ttk.Style().configure('StatsTitle.TButton', font=('Verdana', 12))
        self.title = ttk.Label(self, text='Stats', style='StatsTitle.TLabel')
        self.img = ttk.Label(self, image=SideBar.STATS_LOGO)
        self.returnBtn = ttk.Button(self, text='Return to Main Menu', style='StatsTitle.TButton',
                                    command=lambda: controller.changeScreen(CONST.LOC_MAIN_MENU))

        # Positioning
        self.title.pack(side=tk.TOP, pady=20)
        self.img.pack(side=tk.TOP)
        self.returnBtn.pack(side=tk.TOP, ipadx=10, ipady=5, pady=20)
        self.grid(row=0, column=0, sticky=tk.N+tk.S)


class StatsFrame(tk.Frame):
    TITLES_STYLE = { "columnspan": 4, "padx": 10, "pady": 15 }
    LABELS_STYLE = { "sticky": tk.E, "padx": 10, "pady": 5 }
    VALUES_STYLE = { "sticky": tk.W, "padx": 10, "pady": 5 }


    def __init__(self, master=None, controller=None):
        super().__init__(master)

        self.grid_columnconfigure( tuple(range(4) ), weight=1)
        self.grid_rowconfigure(tuple(range(11)), weight=1)
        ttk.Style().configure('StatsFrameTitle.TLabel', font=('Verdana', 18, 'bold'))
        ttk.Style().configure('StatsFrameLabel.TLabel', font=('Verdana', 12, 'bold') )
        ttk.Style().configure('StatsFrameValue.TLabel', font=('Verdana', 12) )
        self['relief'], self['bd'] = tk.SUNKEN, 4

        #################
        #   Labels
        #################
        self.name_l = ttk.Label(self, text='Name:', style='StatsFrameLabel.TLabel')
        self.playtime_l = ttk.Label(self, text='Play Time:', style='StatsFrameLabel.TLabel')
        self.savef_l = ttk.Label(self, text='Save file:', style='StatsFrameLabel.TLabel')
        self.vs_cpu_t = ttk.Label(self, text='VS CPU', style='StatsFrameTitle.TLabel', foreground='#e74c3c')
        self.wins_cpu_l = ttk.Label(self, text='Wins:', style='StatsFrameLabel.TLabel')
        self.loss_cpu_l = ttk.Label(self, text='Losses:', style='StatsFrameLabel.TLabel')
        self.ties_cpu_l = ttk.Label(self, text='Ties:', style='StatsFrameLabel.TLabel')
        self.practice_t = ttk.Label(self, text='Practice Mode', style='StatsFrameTitle.TLabel', foreground='#2980b9')
        self.o_wins_l = ttk.Label(self, text='O Wins:', style='StatsFrameLabel.TLabel')
        self.o_losses_l = ttk.Label(self, text='O Losses:', style='StatsFrameLabel.TLabel')
        self.x_wins_l = ttk.Label(self, text='X Wins:', style='StatsFrameLabel.TLabel')
        self.x_loss_l = ttk.Label(self, text='X Losses:', style='StatsFrameLabel.TLabel')
        self.ties_l = ttk.Label(self, text='Ties:', style='StatsFrameLabel.TLabel')

        self.name_l.grid(row=0, column=1, **StatsFrame.LABELS_STYLE)
        self.playtime_l.grid(row=1, column=1, **StatsFrame.LABELS_STYLE)
        self.savef_l.grid(row=2, column=1, **StatsFrame.LABELS_STYLE)
        self.vs_cpu_t.grid(row=3, column=0, **StatsFrame.TITLES_STYLE)
        self.wins_cpu_l.grid(row=4, column=1, **StatsFrame.LABELS_STYLE)
        self.loss_cpu_l.grid(row=5, column=1, **StatsFrame.LABELS_STYLE)
        self.ties_cpu_l.grid(row=6, column=1, **StatsFrame.LABELS_STYLE)
        self.practice_t.grid(row=7, column=0, **StatsFrame.TITLES_STYLE)
        self.o_wins_l.grid(row=8, column=0, **StatsFrame.LABELS_STYLE)
        self.o_losses_l.grid(row=9, column=0, **StatsFrame.LABELS_STYLE)
        self.x_wins_l.grid(row=8, column=2, **StatsFrame.LABELS_STYLE)
        self.x_loss_l.grid(row=9, column=2, **StatsFrame.LABELS_STYLE)
        self.ties_l.grid(row=10, column=1, **StatsFrame.LABELS_STYLE)

        #################
        #   Values
        #################
        self.name_v = ttk.Label(self, text='TestVal', style='StatsFrameValue.TLabel')
        self.playtime_v = ttk.Label(self, text='TestVal', style='StatsFrameValue.TLabel')
        self.savef_v = ttk.Label(self, text='TestVal', style='StatsFrameValue.TLabel', wraplength=350)
        self.wins_cpu_v = ttk.Label(self, text='TestVal', style='StatsFrameValue.TLabel')
        self.loss_cpu_v = ttk.Label(self, text='TestVal', style='StatsFrameValue.TLabel')
        self.ties_cpu_v = ttk.Label(self, text='TestVal', style='StatsFrameValue.TLabel')
        self.o_wins_v = ttk.Label(self, text='TestVal', style='StatsFrameValue.TLabel')
        self.o_losses_v = ttk.Label(self, text='TestVal', style='StatsFrameValue.TLabel')
        self.x_wins_v = ttk.Label(self, text='TestVal', style='StatsFrameValue.TLabel')
        self.x_loss_v = ttk.Label(self, text='TestVal', style='StatsFrameValue.TLabel')
        self.ties_v = ttk.Label(self, text='TestVal', style='StatsFrameValue.TLabel')

        self.name_v.grid(row=0, column=2, **StatsFrame.VALUES_STYLE)
        self.playtime_v.grid(row=1, column=2, **StatsFrame.VALUES_STYLE)
        self.savef_v.grid(row=2, column=2, **StatsFrame.VALUES_STYLE)
        self.wins_cpu_v.grid(row=4, column=2, **StatsFrame.VALUES_STYLE)
        self.loss_cpu_v.grid(row=5, column=2, **StatsFrame.VALUES_STYLE)
        self.ties_cpu_v.grid(row=6, column=2, **StatsFrame.VALUES_STYLE)
        self.o_wins_v.grid(row=8, column=1, **StatsFrame.VALUES_STYLE)
        self.o_losses_v.grid(row=9, column=1, **StatsFrame.VALUES_STYLE)
        self.x_wins_v.grid(row=8, column=3, **StatsFrame.VALUES_STYLE)
        self.x_loss_v.grid(row=9, column=3, **StatsFrame.VALUES_STYLE)
        self.ties_v.grid(row=10, column=2, **StatsFrame.VALUES_STYLE)

        self.grid(row=0, column=1, sticky=tk.N+tk.S+tk.E+tk.W, padx=20, ipadx=10)

class StatsView(ttk.Frame):
    def __init__(self, master=None, controller=None):
        super().__init__(master)

        self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = SideBar(self, controller)
        self.stats_frame = StatsFrame(self, controller)

    def updateStats(self, state):
        self.stats_frame.name_v['text'] = state.name
        self.stats_frame.savef_v['text'] = state.fileloc
        self.stats_frame.wins_cpu_v['text'] = state.vscpu_wins
        self.stats_frame.loss_cpu_v['text'] = state.vscpu_losses
        self.stats_frame.ties_cpu_v['text'] = state.vscpu_ties
        self.stats_frame.o_wins_v['text'] = state.practice_Owins
        self.stats_frame.o_losses_v['text'] = state.practice_Olosses
        self.stats_frame.x_wins_v['text'] = state.practice_Olosses
        self.stats_frame.x_loss_v['text'] = state.practice_Owins
        self.stats_frame.ties_v['text'] = state.practice_ties

    def drawPlayTime(self, time):
        hrs, mins, secs = time // 3600, time // 60, time % 60
        self.stats_frame.playtime_v['text'] = f'{hrs} Hour(s) {mins} Minute(s) {secs} Second(s)'


    def draw(self):
        self.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W, padx=30, pady=30)