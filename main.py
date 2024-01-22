from tkinter import *
from windows.login import LoginWindow
from flappy_bat import FlappyBatGame
from db.repository import Repository

repository = Repository(db_file_name='db/players.db')


def main():

    root = Tk()
    root.geometry("315x150+600+400")
    root.resizable(False, False)
    root.wm_iconphoto(False, PhotoImage(file='images/bat.png'))
    login_window = LoginWindow(root, repository)
    root.mainloop()

    if login_window.authenticated_user:
        FlappyBatGame(window_height=700, window_width=551,
                      player=login_window.authenticated_user, repository=repository).display_menu()


if __name__ == '__main__':
    main()
