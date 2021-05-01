import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as tkm

import CONST
import views.main_menu_view as V_menu
import views.Component.MenuBar as V_menubar
import views.practice_view as V_practice
import views.vs_cpu_view as V_vsCpu
import views.stats_view as V_stats
from model.state import State

import pygame.mixer as mx



######################################
#   Controller
######################################
class Controller(ttk.Frame):
    def __init__(self, root=None, master=None):
        super().__init__(master)
        self.master = master
        self.root = root

        # State
        self.state = State()

        # Views
        # Make the top level window to be resizable, and take up entire available width
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.menu_bar = V_menubar.GameViewMenuBar(self, self)
        self.main_menu = V_menu.MainMenu(self, self)
        self.practice_view = V_practice.PracticeView(self, self, self.state)
        self.vsCpu_view = V_vsCpu.VsCpuView(self, self, self.state)
        self.stats_view = V_stats.StatsView(self, self)

        self.main_menu.draw()
        self.grid(sticky=tk.N + tk.S + tk.E + tk.W)

        # Music
        mx.init()
        mx.music.load('./resources/music.mp3')
        mx.music.play(loops=-1)
        mx.music.set_volume(0.07)
        self.key_sound = mx.Sound('./resources/Keyboard Sounds_Cherry Clear.mp3')

        # Initiate Playtime counting
        self.incrementPlayTime()


    def incrementPlayTime(self):
        self.state.playtime += 1
        self.stats_view.drawPlayTime(self.state.playtime)
        root.after(1000, self.incrementPlayTime)

    def clear_practice_board(self):
        State.clear_board(self.state.practice_board)
        self.practice_view.update_all()

    def play_sound(self):
        self.key_sound.play()

    ############################################################
    # GUI Related Functions
    ############################################################
    # Exit program, but check for unsaved changes first
    def saveBeforeQuit(self):
        if self.state.promptSave():
            root.quit()

    # If is_visible is True, show the menu bar, else hide the menu bar
    def show_menu(self, is_visible: bool = True):
        assert isinstance(is_visible, bool)
        self.root.configure(menu=(self.menu_bar if is_visible else ''))


    # Refreshes the boards and game stats window. Done after loading game especially in game view
    def refresh_boards(self):
        self.practice_view.update_all()
        self.vsCpu_view.update_all()

    # Changes the window view to either Main Menu, or Game View
    def changeScreen(self, screen_code: int):
        assert screen_code in CONST.LOC, "Invalid changeScreen() call. Argument must be in State.LOC"
        self.main_menu.grid_forget()
        self.practice_view.grid_forget()
        self.vsCpu_view.grid_forget()
        self.stats_view.grid_forget()

        if screen_code == CONST.LOC_MAIN_MENU:
            self.show_menu(False)
            self.main_menu.draw()
        elif screen_code == CONST.LOC_LOCAL_VS:
            self.show_menu()
            self.practice_view.draw()
        elif screen_code == CONST.LOC_LOCAL_CPU:
            self.show_menu()
            self.vsCpu_view.draw()
        elif screen_code == 4:
            self.show_menu(False)
            self.stats_view.updateStats(self.state)
            self.stats_view.draw()

    @staticmethod
    def show_practice_winner(winner):
        assert winner in (-1,0,1)
        if winner == 0:
            tkm.showinfo("A Tie", "The game ends in a tie!")
        else:
            token = 'O' if winner == 1 else 'X'
            tkm.showinfo(f"{token} wins",
                         f"Congratulations {token} for winning against your enemy!")

    @staticmethod
    def show_cpu_winner(winner, isPlayerFirstMove):
        assert winner in (-1,0,1)
        if winner == 0:
            tkm.showinfo("A Tie", "A tie against CPU!")
        elif winner == 1 and isPlayerFirstMove:
            tkm.showinfo("Victory", "You win against CPU? How???!!!")
        else:
            tkm.showinfo("Defeat", "You lose. It's expected")


    #######################################################
    #   Game Core Logic
    #######################################################
    def practice_button_press(self, index):
        assert index in range(9)

        # 1 - Adds token to the tic tac toe board
        if not self.state.add_token(CONST.LOC_LOCAL_VS, index): return
        token = 'X' if self.state.isOTurn else 'O'
        self.practice_view.update_tooltip(f'{token} had made his move at grid {index}!')
        self.play_sound()
        self.refresh_boards()

        # 2 - Checks for winning state, and set state, show winner if someone does win
        winner = State.checkWinningState( self.state.practice_board )
        if winner is None: return
        self.state.game_set(CONST.LOC_LOCAL_VS, winner)
        Controller.show_practice_winner(winner)
        self.practice_view.update_tooltip('A new game has begun')
        self.refresh_boards()


    def cpu_button_press(self, index):
        assert index in range(9)

        # Adds token to the tic tac toe board
        if not self.state.add_token(CONST.LOC_LOCAL_CPU, index): return
        self.vsCpu_view.update_tooltip(f'You had made your move at grid {index}!')
        self.play_sound()
        self.refresh_boards()

        # Checks for winning
        winner = State.checkWinningState(self.state.cpu_board)
        # Player wins, or tied
        if winner is not None:
            Controller.show_cpu_winner(winner, self.state.isPlayerFirst)
            self.state.game_set(CONST.LOC_LOCAL_CPU, winner)
            self.vsCpu_view.update_tooltip(f'A new game has begin')
            self.refresh_boards()

            # After refresh, check if CPU moves first
            if not self.state.isPlayerFirst:
                move = self.state.cpu_moves()
                self.play_sound()
                self.refresh_boards()
                self.vsCpu_view.update_tooltip(f'CPU had made its move at grid {move}!')
                return

        # Player moves but not yet deterministic. CPU moves and check state
        move = self.state.cpu_moves()
        self.play_sound()
        self.refresh_boards()
        self.vsCpu_view.update_tooltip(f'CPU had made its move at grid {move}!')
        winner = State.checkWinningState(self.state.cpu_board)
        # Tie or CPU wins
        if winner is not None:
            Controller.show_cpu_winner(winner, self.state.isPlayerFirst)
            self.state.game_set(CONST.LOC_LOCAL_CPU, winner)
            self.refresh_boards()
            self.vsCpu_view.update_tooltip('A new game has begin')

            # After refresh, check if CPU moves first
            if not self.state.isPlayerFirst:
                move = self.state.cpu_moves()
                self.play_sound()
                self.refresh_boards()
                self.vsCpu_view.update_tooltip(f'CPU had made its move at grid {move}!')







    ###################################################################
    #   Saving and Loading Operations
    ###################################################################
    def saveGame(self):
        self.state.saveGame()

    def loadGame(self):
        if self.state.loadGame():
            self.refresh_boards()



#######################################################################################################
# Driver code
#######################################################################################################
if __name__ == '__main__':
    root = tk.Tk()
    window = Controller(root, root)

    root.protocol('WM_DELETE_WINDOW', window.saveBeforeQuit )
    root.title('TicTacToe')
    root.iconbitmap('resources/tic-tac-toe.ico')
    root.mainloop()
