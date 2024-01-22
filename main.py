from tkinter import *
from windows.login import LoginWindow
# from flappy_bird import FlappyBird
from db.repository import Repository
from player import *

repository = Repository(db_file_name='db/players.db')

def main():
    root = Tk()
    root.geometry("315x150+600+400")
    root.resizable(False, False)
    root.wm_iconphoto(False, PhotoImage(file = 'images/bat.png'))
    login_window = LoginWindow(root, repository)
    root.mainloop()

    login_window.authenticated_user

    # FlappyBird(player=player, repository=repository).display_menu()

if __name__ == '__main__':
    main()
