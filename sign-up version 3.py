import customtkinter as ctk
import tkinter as tk
from customtkinter import *
import sqlite3


####----(Account database)----####

conn = sqlite3.connect('Account database.db')
c = conn.cursor()

#c.execute("""CREATE TABLE Accounts (
#          Account_ID text,
#          Username text,
#          Password text
#          )""")

#conn.commit()

#conn.close()

####----(multi-purpose subroutines)----####

def isMinimum(data_input, minimum):
    numOfCharacters = len(data_input)
    if numOfCharacters < minimum:
        return False
    else:
        return True
    
def hashing():
    pass

####----(Start of account GUI)----####

account = ctk.CTk()
account.geometry('400x500')
account.resizable(False,False)
account.title('Account')
set_appearance_mode('light')


####----(Switching between pages of log in and sign up page)----####

sign_in = ctk.CTkFrame(account, width=400,height=360,fg_color='#EBEBEB')
sign_in.place(x=0,y=70)

Log_in = ctk.CTkFrame(account, width=400,height=360,fg_color='#EBEBEB')
Log_in.place(x=0,y=70)


log_or_sign = ctk.StringVar()
log_or_sign.set('Create an account?')

top_label_text = ctk.StringVar()
top_label_text.set('Log in')

def switch():
    if top_label_text.get() == 'Log in':
        top_label_text.set('Register')
        log_or_sign.set('Log in')
        sign_in.tkraise()
        sign_username.set('')
        sign_password.set('')
        sign_re_password.set('')
        message.configure(text='')
    else:
        top_label_text.set('Log in')
        log_or_sign.set('Create an account?')
        Log_in.tkraise()
        log_username.set('')
        log_password.set('')

top_label = ctk.CTkLabel(account, textvariable=top_label_text, font=('Arial',35,'bold'))
top_label.place(x=50, y=30)

switch = ctk.CTkButton(account, textvariable=log_or_sign,
                       font=('Arial',15,'underline'),
                       text_color='#005FBF',
                       fg_color='#EBEBEB',
                       hover_color='#EBEBEB',
                       width=0,
                       command=switch)
switch.place(relx=0.5,rely=0.9, anchor=CENTER)

####----(Log in page)----####

#username input

log_username = ctk.StringVar()
log_username.set('')

log_username_label = ctk.CTkLabel(Log_in,
                                text='Username',
                                font=('Arial', 15),
                                )
log_username_label.place(x=65, y=10)

log_username_input = ctk.CTkEntry(Log_in,
                            font=('Arial', 15),
                            width=300,
                            height=40,
                            textvariable=log_username)
log_username_input.place(relx=0.5,y=55, anchor=CENTER)


#password input


log_password = ctk.StringVar()
log_password.set('')

log_passwrd = ctk.CTkLabel(Log_in,
                       text='Password',
                       font=('Arial', 15),
                       )
log_passwrd.place(x=65, y=100)

log_passwrd_inp = ctk.CTkEntry(Log_in,
                           font=('Arial', 15),
                           width=300,
                           height=40,
                           textvariable=log_password)
    
log_passwrd_inp.place(relx=0.5,y=145, anchor=CENTER)

#log in submit

def log_submit_func():
    print('it works')

log_submit = ctk.CTkButton(Log_in,
                           text='Log in',
                           font=('Arial',15,'bold'),
                           fg_color='#005FBF', height=40 ,width=300,
                           command=log_submit_func)
log_submit.place(relx=0.5,y=335, anchor=CENTER)


####----(Sign up page)----####


#Username

sign_username = ctk.StringVar()
sign_username.set('')

Sign_username_label = ctk.CTkLabel(sign_in,
                                text='Username',
                                font=('Arial', 15),
                                )
Sign_username_label.place(x=65, y=10)

Sign_username_input = ctk.CTkEntry(sign_in,
                            font=('Arial', 15),
                            width=300,
                            height=40,
                            textvariable=sign_username)
Sign_username_input.place(relx=0.5,y=55, anchor=CENTER)

#password

sign_password = ctk.StringVar()
sign_password.set('')

Sign_password = ctk.CTkLabel(sign_in,
                       text='Password',
                       font=('Arial', 15),
                       )
Sign_password.place(x=65, y=100)

Sign_passwrd_inp = ctk.CTkEntry(sign_in,
                           font=('Arial', 15),
                           width=300,
                           height=40,
                           textvariable=sign_password)
    
Sign_passwrd_inp.place(relx=0.5,y=145, anchor=CENTER)

#re-enter password

sign_re_password = ctk.StringVar()
sign_re_password.set('')

Sign_re_passwrd = ctk.CTkLabel(sign_in,
                       text='Re-enter password',
                       font=('Arial', 15),
                       )
Sign_re_passwrd.place(x=65, y=190)

Sign_re_passwrd_inp = ctk.CTkEntry(sign_in,
                           font=('Arial', 15),
                           width=300,
                           height=40,
                           textvariable=sign_re_password)
    
Sign_re_passwrd_inp.place(relx=0.5,y=235, anchor=CENTER)

# submitting

def password_character_check(password):

    special_characters = [ '!', '"', '#', '$', '%', '&', '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=' '>', '?', '@', '[', ']', '^', '_','{', '|', ' }', '~']

    minimum_characters = False; has_lower = False; has_upper = False; has_digit = False; has_special = False
    
    if isMinimum(password,12):
        minimum_characters = True
    
    for char in range(0,len(password)):
        if password[char].isupper():
            has_upper = True

        elif password[char].islower():
            has_lower = True

        elif password[char].isdigit():
            has_digit = True

        for i in range(0,len(special_characters)):
            if password[char] == special_characters[i]:
                has_special = True

    if has_special == False or minimum_characters == False or has_lower == False or has_upper == False or has_digit == False:
        return False
    else:
        return True
    
def username_duplicates():
    pass

def register():
    username = Sign_username_input.get()
    password = Sign_passwrd_inp.get()
    c.execute(f"""INSERT INTO Accounts VALUES ('0','{username}','{password}')""")
    conn.commit()
    conn.close()

    

def sign_submit_func():

    correct = False

    if Sign_passwrd_inp.get() == '' or Sign_re_passwrd_inp.get() == '' or Sign_username_input.get() == '':
        message.configure(text='Please fully fill out all fields.')
    
    elif isMinimum(Sign_username_input.get(),3) == False:
        message.configure(text='Username should be at least 3 characters.')

    elif Sign_passwrd_inp.get() != Sign_re_passwrd_inp.get():
        message.configure(text='Passwords do not match.')

    elif password_character_check(Sign_passwrd_inp.get()) == False:
        message.configure(text='Password must contain at least 12 characters,\na symbol, a number, a lower and uppercase letter.',)

    else:
        register()

    

message = ctk.CTkLabel(sign_in,
                       text='',
                       font=('Arial',15),
                       text_color='red')
message.place(relx=0.5, y=285,anchor=CENTER)

sign_submit = ctk.CTkButton(sign_in, text='Sign-in',
                       font=('Arial',15,'bold'), fg_color='#005FBF', height=40 ,width=300,
                        command=sign_submit_func)
sign_submit.place(relx=0.5,y=335, anchor=CENTER)





account.mainloop()

