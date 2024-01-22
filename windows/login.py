from tkinter.ttk import Frame, Button, Style
import tkinter as tk
from tkinter import Tk, Frame, Label, Entry, Button, LEFT, RIGHT, BOTH, X
from db.repository import Repository, DbError


class LoginWindow(Frame):

    def __init__(self, root: Tk, repository: Repository):
        super().__init__()
        self.root = root
        self.repository = repository
        self.authenticated_user = None
        self.error = tk.StringVar()

        self.initUI()

    def initUI(self):
        self.master.title("Flappy Bat")
        self.style = Style()
        self.style.theme_use("default")

        self.pack(fill=BOTH, expand=True, padx=7, pady=7)

        name_frame = Frame(self)
        name_frame.pack(fill=X)

        name_label = Label(name_frame, text="Username:", width=7)
        name_label.pack(side=LEFT, padx=7, pady=7)

        name_entry = Entry(name_frame)
        name_entry.pack(fill=X, padx=5, expand=True)

        password_frame = Frame(self)
        password_frame.pack(fill=X)

        password_label = Label(password_frame, text="Password:", width=7)
        password_label.pack(side=LEFT, padx=7, pady=7)

        password_entry = Entry(password_frame, show="*")
        password_entry.pack(fill=X, padx=5, expand=True)

        error_frame = Frame(self)
        error_frame.pack(fill=X)

        error_label = Label(error_frame, textvariable=self.error, fg="#ff4d4d")
        error_label.pack(fill=X, side=RIGHT, padx=7)

        login_btn = Button(self, text="Login", command=lambda: self.__authenticate_user(
            name_entry.get(), password_entry.get()))
        login_btn.pack(side=RIGHT, padx=5, pady=3)

        register_btn = Button(self, text="Register", command=lambda: self.__register_user(
            name_entry.get(), password_entry.get()))
        register_btn.pack(side=RIGHT)

    def __authenticate_user(self, username, password):
        if (username and password):
            error = self.repository.validate_user(username, password)
            if error:
                match error:
                    case DbError.UserDoesNotExist:
                        self.error.set("User does not exist")
                    case DbError.PasswordDoesNotMatch:
                        self.error.set("Password does not match")
                    case _:
                        self.error.set(str(error))
            else:
                self.authenticated_user = self.repository.get_player(username)
                self.root.destroy()
        else:
            self.__display_blank_fields_error(username, password)

    def __register_user(self, username, password):
        if (username and password):
            error = self.repository.register_user(username, password)
            if error:
                match error:
                    case DbError.UserAlreadyExists:
                        self.error.set("User already exists")
                    case _:
                        self.error.set(str(error))
            else:
                self.authenticated_user = self.repository.get_player(username)
                self.root.destroy()
        else:
            self.__display_blank_fields_error(username, password)

    def __display_blank_fields_error(self, username, password):
        s = ""
        if not username:
            s += "Username "
        if not password:
            s += "Password " if not s else "and Password "
        s += "cannot be blank"
        self.error.set(s)
