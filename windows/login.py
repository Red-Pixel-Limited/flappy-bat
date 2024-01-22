from tkinter.ttk import Frame, Button, Style
from tkinter import *
from db.repository import Repository

class LoginWindow(Frame):

    def __init__(self, root: Tk, repository: Repository):
        super().__init__()
        self.root = root
        self.repository = repository
        self.authenticated_user = None

        self.initUI()

    def initUI(self):

        self.master.title("Flappy Bat")
        self.style = Style()
        self.style.theme_use("default")

        self.pack(fill=BOTH, expand=True, padx=7, pady=7)

        name_frame = Frame(self)
        name_frame.pack(fill=X)

        name_lbl = Label(name_frame, text="Username:", width=7)
        name_lbl.pack(side=LEFT, padx=7, pady=7)

        name_entry = Entry(name_frame)
        name_entry.pack(fill=X, padx=5, expand=True)

        password_frame = Frame(self)
        password_frame.pack(fill=X)

        password_lbl = Label(password_frame, text="Password:", width=7)
        password_lbl.pack(side=LEFT, padx=7, pady=7)

        password_entry = Entry(password_frame)
        password_entry.pack(fill=X, padx=5, expand=True)

        error_frame = Frame(self)
        error_frame.pack(fill=X)

        error_lbl = Label(error_frame, text="", fg="red")
        error_lbl.pack(fill=X, expand=True)

        login_btn = Button(self, text="Login", command=self.root.destroy)
        login_btn.pack(side=RIGHT, padx=5, pady=3)

        register_btn = Button(self, text="Register")
        register_btn.pack(side=RIGHT)
