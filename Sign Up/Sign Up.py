# Packages are imported
import tkinter as tk
from tkinter import *
from PIL import Image,ImageTk
import mysql.connector
import re

# Database Connection
dbConnect = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            passwd = '',
            database = 'Admin'
            )

mydb = dbConnect.cursor()

# Parent Widget is created
window = tk.Tk()
window.geometry('400x580')
window.resizable(width=False, height=False)
window.title('Registration Form')
window.configure(background='white')

# Variables are defined
fn = StringVar()
ln = StringVar()
em = StringVar()
id = StringVar()
pw1 = StringVar()
pw2 = StringVar()


# Image of the Company
img = Image.open('Company.png')
logo = ImageTk.PhotoImage(img)

# Widget for image in tkinter
logoPlace = Label(image=logo,width=100,height=90)
logoPlace.place(x=145,y=5)

# Widgets
label1 =tk.Label(window,text='Create an Account',fg='black',bg='white',relief='flat',font=('Times New Roman',16,'bold'),borderwidth=0,padx=0,pady=0)
label1.place(x=110,y=105)

label2 = tk.Label(window,text="It's quick and easy",fg='black',bg='white',relief='flat',font=('Times New Roman',14),borderwidth=0,padx=0,pady=0)
label2.place(x=120,y=135)

labelfn = tk.Label(window,text="First Name :",fg='black',bg='white',relief='flat',font=('Times New Roman',14),borderwidth=2,padx=0,pady=0)
labelfn.place(x=50,y=180)

entryfn = tk.Entry(window,textvar=fn,relief='solid')
entryfn.place(x=200,y=180)

labelln = tk.Label(window,text="Last Name :",fg='black',bg='white',relief='flat',font=('Times New Roman',14),borderwidth=2,padx=0,pady=0)
labelln.place(x=50,y=215)

entryln = tk.Entry(window,textvar=ln,relief='solid')
entryln.place(x=200,y=215)

labelem = tk.Label(window,text="Email or Phone :",fg='black',bg='white',relief='flat',font=('Times New Roman',14),borderwidth=2,padx=0,pady=0)
labelem.place(x=50,y=250)

entryem = tk.Entry(window,textvar=em,relief='solid')
entryem.place(x=200,y=250)

labelid = tk.Label(window,text="User Name :",fg='black',bg='white',relief='flat',font=('Times New Roman',14),borderwidth=2,padx=0,pady=0)
labelid.place(x=50,y=285)

entryid = tk.Entry(window,textvar=id,relief='solid')
entryid.place(x=200,y=285)

labelpw1 = tk.Label(window,text="Password :",fg='black',bg='white',relief='flat',font=('Times New Roman',14),borderwidth=2,padx=0,pady=0)
labelpw1.place(x=50,y=320)

entrypw1 = tk.Entry(window,textvar=pw1,relief='solid')
entrypw1.place(x=200,y=320)

labelpw2 = tk.Label(window,text="Password :",fg='black',bg='white',relief='flat',font=('Times New Roman',14),borderwidth=2,padx=0,pady=0)
labelpw2.place(x=50,y=355)

entrypw2 = tk.Entry(window,textvar=pw2,relief='solid')
entrypw2.place(x=200,y=355)

msg = tk.Label(window,text='',fg='brown',bg='white',relief='flat',font=('Times New Roman',14,'italic bold'),borderwidth=2,padx=0,pady=0)
msg.place(x=110,y=510)


# Function for Password Submission
def validate(passwd):
    while True:
        if len(passwd) < 6:
            msg.config(text='Make sure your password is\n at least 6 letters')
            msg.place(x=80,y=510)
            return False
        elif re.search('[0-9]',passwd) is None:
            msg.config(text='Make sure your password has\n a number in it')
            msg.place(x=80,y=510)
            return False
        elif re.search('[A-Z]',passwd) is None: 
            msg.config(text='Make sure your password has\n a capital letter in it')
            msg.place(x=80,y=510)
            return False
        elif re.search('[a-z]',passwd) is None: 
            msg.config(text='Make sure your password has\n a lowercase letter in it')
            msg.place(x=80,y=510)
            return False
        else:
            return True
            break

# Function for Submission
def submit():
    msg.config(text=' ')
    fname = fn.get()
    lname = fn.get()
    email = em.get()
    userid = id.get()
    passwd = pw1.get()
    conpwd = pw2.get()



    if(fname == '' or lname == '' or email == '' or userid == '' or passwd == '' or conpwd == ''):
        msg.config(text='All Fields Required')
        msg.place(x=115,y=510)

    else:
        if(passwd != conpwd):
            msg.config(text='Passwords do not match')
            msg.place(x=110,y=510)
        else:
            if validate(passwd):          
                count=0
                mydb.execute('SELECT * FROM SignUp')
                result = mydb.fetchall()
                for i in range(0,len(result),1):
                    if(result[i][3] == email):
                        msg.config(text='Email already Registered\nTry Login')
                        msg.place(x=105,y=510)
                        count=1
                        break
                
                    elif(result[i][4] == userid):
                        msg.config(text='User ID already registered\nTry another User ID')
                        msg.place(x=100,y=510)
                        count=1
                        break
                
                if count==0:
                    sql = "INSERT INTO SignUp (FirstName,LastName,Email,UserID,Password) VALUES (%s,%s,%s,%s,%s)"
                    val = (fname,lname,email,userid,passwd)
                    mydb.execute(sql,val)
                    dbConnect.commit()
                    msg.config(text='Registration successful\nConfirm your email')
                    msg.place(x=105,y=510)
                    print('Registrations Successful')

                else:
                    pass


# Function for resetting the form
def reset():
    msg.config(text=' ')
    entryfn.delete(0,END)
    entryln.delete(0,END)
    entryem.delete(0,END)
    entryid.delete(0,END)
    entrypw1.delete(0,END)
    entrypw2.delete(0,END)

def forgot():
    pass


forgotpwd = Button(window,text='Forgot Password',font=('arial',14),bg='white',fg='brown',relief='flat',padx=5,pady=4,width=16,height=1,command=forgot)
forgotpwd.place(x=100,y=470)

buttonsub = Button(window,text='Register',font=('arial',16,'bold'),bg='brown',fg='white',relief='solid',padx=5,pady=4,width=8,height=1,command=submit)
buttonsub.place(x=50,y=400)

buttonreset = Button(window,text='Reset',font=('arial',16,'bold'),bg='brown',fg='white',relief='solid',padx=5,pady=4,width=8,height=1,command=reset)
buttonreset.place(x=200,y=400)


window.mainloop()
