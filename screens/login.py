
# ------
# what is ur name?
# [___]


# |continue|
# ------

# 2. 

from tkinter import *

def register_user():
    username_data = username.get()
    password_data = password.get()
    
    with open(username_data+".txt", "w")as file:
        file.write(username_data+"\n")
        file.write(password_data)
        
    username_entry.delete(0, END)
    password_entry.delete(0, END)
        
    Label(window1, text = "Registration Sucessful!", fg = "green", font=("calibri", 11)).pack()
    
def register():
    global window1
    window1 = Toplevel(window)
    window1.title("Register")
    window1.geometry("300x250")
    
    global username
    global password
    global username_entry
    global password_entry
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
    
def login():
    print("Login session started")

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
