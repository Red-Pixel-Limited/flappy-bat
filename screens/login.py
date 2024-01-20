# ------
# what is ur name?
# [___]


# |continue|
# ------


from tkinter import *

def register_user():
    if not username_entry.get() or not password_entry.get():
        Label(window1, text = "Username and password is required", fg = "red", font=("calibri", 11)).pack()
    
    else:
        Label(window1, text = "Registration Sucessful!", fg = "green", font=("calibri", 11)).pack()
    
def register():
    global window1, username, password, username_entry, password_entry
    window1 = Toplevel(window)
    window1.title("Register")
    window1.geometry("300x250")
    
    username = StringVar()
    password = StringVar()
    
    Label(window1, text = "Please enter details").pack()
    Label(window1, text = "").pack()
    
    Label(window1, text = "Username *").pack()
    username_entry = Entry(window1, textvariable = username)
    username_entry.pack()
    
    Label(window1, text = "Password *").pack()
    password_entry = Entry(window1, textvariable = password)
    password_entry.pack()
    Label(window1, text= "").pack()
    
    Button(window1, text = "Register", width = 10, height = 1, command = register_user).pack()
    
def login_user():
    if not username_verify.get() or not password_verify.get():
        Label(window2, text = "Username and password is required", fg = "red", font=("calibri", 11)).pack()
        
    
def login():
    global window2, username_verify, password_verify, username_entry1, password_entry1
    
    window2 = Toplevel(window)
    window2.title("Login")
    window2.geometry("300x250")
    Label(window2, text = "Please enter details").pack()
    Label(window2, text = "").pack()
    
    username_verify = StringVar()
    password_verify = StringVar()
    
    Label(window2, text = "Username *").pack()
    username_entry1 = Entry(window2, textvariable = username_verify)
    username_entry1.pack()
    
    Label(window2, text = "Password *").pack()
    password_entry1 =Entry(window2, textvariable = password_verify)
    password_entry1.pack()
    Label(window2, text = "").pack()
    
    Button(window2, text = "Log in", width = 10, height = 1, command = login_user).pack()

def main_window():
    global window
    window = Tk()
    window.geometry("300x250")
    window.title("Flappy bat")
    Label(text = "Welcome!", bg = "#7393B3", width = "300", height = "2", font = ("Calibri", 13)).pack()
    Label(text = "").pack()
    Button(text = "Login", height = "2", width = "30", command = login).pack()
    Label(text = "").pack()
    Button(text = "Register", height = "2", width = "30", command = register).pack()
    
    window.mainloop()

main_window()