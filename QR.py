'''This is a Python script for generating a QR code of a website. The user speaks the name of the website,which is
then passed through the Google search API to get the website URL. The URL is then used to generate a QR code using 
the qrcode library, which is saved and displayed in a matplotlib format. The script also uses the pyttsx3 library
to give verbal feedback to the user during the process.
'''
from tkinter import PhotoImage
import tkinter as tk
import customtkinter
from customtkinter import *
from CTkMessagebox import CTkMessagebox

import os.path
import re
from PIL import Image,ImageTk
import time
import qrcode
import requests
import matplotlib.pyplot as plt

import smtplib
import random
import mysql.connector
import webbrowser


switch_value = True
theme= True

paybut = None
link1 = None


def mode():
    global switch_value
    if switch_value == True:
        # Changes the window to dark theme
        customtkinter.set_appearance_mode("dark")  
        switch_value = False
    else: 
        # Changes the window to light theme
        customtkinter.set_appearance_mode("light")  
        switch_value = True



# --------------------------------------------------------------------Register Page-----------------------------------------------------------------#

def testreg():
    global topreg
    customtkinter.set_default_color_theme("dark-blue")   # green,blue,dark-blue
    # customtkinter.set_appearance_mode("dark")      # system,light,dark
    customtkinter.set_widget_scaling(1.3)
    customtkinter.set_window_scaling(1.0)

    def get_otp():
        a=random.randint(10000, 99999)
        return str(a)

    def otpp():
        global otp
        global email
        email=user_emailid.get()
        otp=get_otp()
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.ehlo()
        server.login('abcd@gmail.com', 'app password')
        server.sendmail('abcd@gmail.com', email, otp)
        print('message sent',otp)
        CTkMessagebox(title="status",message="Successfully Sent OTP", icon="check", option_1="Thanks",fade_in_duration=(2)) 

    def register_status():
        register.configure(state=DISABLED)
        emai=id_check.get()
        db = mysql.connector.connect(host="hostname", user="username", password="******", database="databasename")
        cur = db.cursor()
        query = "SELECT * FROM tablename WHERE Name = %s AND Email_id = %s AND Password = %s AND Retype_Pswd = %s"
        name = user_entry.get()
        email = user_emailid.get()
        password = pswd_entry.get()
        retype=retype_entry.get()
        params = (name, email, password, retype)
        cur.execute(query, params)
        result = cur.fetchall()
        topreg.destroy()
        if len(result) == 0 and emai==otp and password==retype :
            ins = "INSERT INTO tablename(Name, Email_id, Password, Retype_Pswd) VALUES (%s, %s, %s, %s)"
            val = (name, email, password,retype)
            cur.execute(ins, val)
            db.commit()
            CTkMessagebox(title="Status",message= "Details successfully registered", icon="check", option_1="Thanks",fade_in_duration=(2))
            return testlogin()
        else:
            CTkMessagebox(title="Status",message= "Entered details are already registered", icon="warning", option_1="Ok",fade_in_duration=(2))
            cur.execute("rollback")
            return testreg()
    
    def Already_registered_button_clicked():
        # Perform register logic
        # Destroy the tophom window
        topreg.destroy()
        testlogin()

    def home_button_clicked1():
        # Perform register logic
        # Destroy the tophom window
        topreg.destroy()
        testhome()
    
    topreg=CTkToplevel()
    topreg.title("Register")
    # topreg.geometry("650x450")
    topreg.attributes('-fullscreen', True)
    # top.config(background='blue')

    # Register Page !!!
    display=CTkLabel(topreg,text="Register Page",fg_color="#4444FF",corner_radius=8,font=("New Roman",30))
    display.grid(row=1,column=0,padx=10,pady=5)
    
    # regpic=ImageTk.PhotoImage(Image.open("home.png").resize((20,20),Image.ANTIALIAS))
    regpic = CTkImage(light_image=Image.open("home.png"), size=(20, 20))

    hombut1 = CTkButton(topreg, image=regpic, text="Home Page", command=home_button_clicked1,fg_color="#4444FF",text_color="black",corner_radius=8,font=("New Roman",20))
    hombut1.place(x=30,y=50)

    # Switch !!!
    # switch_var = StringVar(value="on")
    # switch = CTkSwitch(top, text="Mode", command=mode, variable=switch_var) 
    # switch.grid(row=1, column=2)

    # User Name
    user_name=CTkLabel(topreg,text="Name",font=("New Roman",30))
    user_name.place(x=270,y=108)
    user_entry=CTkEntry(topreg, placeholder_text="Enter The Name",width=400,height=50,justify=CENTER,font=("New Roman",25))
    user_entry.place(x=420,y=100)

    # User Email-id
    user_email=CTkLabel(topreg,text="Email id",font=("New Roman",30))
    user_email.place(x=255,y=175)
    user_emailid=CTkEntry(topreg,placeholder_text="Enter the Email id",width=400,height=50,justify=CENTER,font=("New Roman",25))
    user_emailid.place(x=420,y=165)

    # Enter OTP
    id_check=CTkEntry(topreg,placeholder_text="Enter the OTP",width=210,justify=CENTER,font=("New Roman",25))
    id_check.place(x=515,y=225)

    # send OTP
    Email_check=CTkButton(topreg,text="Send OTP",command=otpp,width=50,height=35,corner_radius=50,font=("New Roman",15),fg_color="#4444FF")
    Email_check.place(x=830,y=173)

    # User Password
    user_pswd=CTkLabel(topreg,text="Password",font=("New Roman",30))
    user_pswd.place(x=240,y=285)
    pswd_entry=CTkEntry(topreg,placeholder_text="Enter the Password",width=400,height=50,justify=CENTER,font=("New Roman",25))
    pswd_entry.place(x=420,y=275)

    retype_pswd=CTkLabel(topreg,text="Re-type Pswd",font=("New Roman",30))
    retype_pswd.place(x=210,y=350)
    retype_entry=CTkEntry(topreg,placeholder_text="Re-Type Password",width=400,height=50,justify=CENTER,font=("New Roman",25))
    retype_entry.place(x=420,y=340)

    # Login Button
    login=CTkButton(topreg,text="Already Registered ?",command=Already_registered_button_clicked,width=100,height=40,corner_radius=50,font=("New Roman",20),fg_color="#4444FF")
    login.place(x=400,y=435)

    # Register Button
    register=CTkButton(topreg,text="New Register ✔",command=register_status,width=100,height=40,corner_radius=50,font=("New Roman",20),fg_color="#4444FF")
    register.place(x=650,y=435)
    
    topreg.mainloop()



#-----------------------------------------------------------------------Login Page-------------------------------------------------------------------#

def testlogin():    
    global toplog
    customtkinter.set_default_color_theme("dark-blue")   # green,blue,dark-blue
    # customtkinter.set_appearance_mode("dark")      # system,light,dark
    customtkinter.set_widget_scaling(1.3)
    customtkinter.set_window_scaling(1.0)

    def login_status():
        global id
        id=user_entry.get()
        db = mysql.connector.connect(host="hostname", user="username", password="*****", database="database name")
        cur = db.cursor()
        query = "SELECT * FROM tablename WHERE Email_id = %s  AND Password = %s"
        email = user_entry.get()
        password = pswd_entry.get()
        params = (email, password)
        cur.execute(query, params)
        result = cur.fetchall()
        toplog.destroy()
        if len(result) > 0:
            CTkMessagebox(title="Status",message= "Successfully Logined.",icon="check",option_1="Thanks",fade_in_duration=(2))
            return testqr()
        else:
            CTkMessagebox(title="Status", message="Login Failed, please enter valid Email-id and password.",icon="cancel",option_1="ok",fade_in_duration=(2))
            cur.execute("rollback")
            return testlogin()
        
    def forgot_button_click():
        # Perform register logic
        # Destroy the tophom window
        toplog.destroy()
        testforgot()
        
    def home_button_clicked2():
        # Perform register logic
        # Destroy the tophom window
        toplog.destroy()
        testhome()

    def register_button_clicked():
        # Perform register logic
        # Destroy the tophom window
        toplog.destroy()
        testreg()
    
    toplog = CTkToplevel()
    toplog.title('Login')
    toplog.geometry('590x260')
    toplog.attributes('-fullscreen', True)
    # top.config(background='blue')

    # Login Page !!!
    display=CTkLabel(toplog,text="Login Page",fg_color="#4444FF",corner_radius=8,font=("New Roman",30))
    display.grid(row=1,column=0,padx=10,pady=5)

    # Home button
    # logpic1=ImageTk.PhotoImage(Image.open("home.png").resize((20,20),Image.ANTIALIAS))
    logpic1 = CTkImage(light_image=Image.open("home.png"), size=(20, 20))

    hombut2 = CTkButton(toplog, image=logpic1, text="Home Page", command=home_button_clicked2,fg_color="#4444FF",text_color="black",corner_radius=8,font=("New Roman",20))
    hombut2.place(x=30,y=50)

    # Register button
    # logpic2=ImageTk.PhotoImage(Image.open("register.png").resize((20,20),Image.ANTIALIAS))
    logpic2 = CTkImage(light_image=Image.open("register.png"), size=(20, 20))

    regbut = CTkButton(toplog, image=logpic2, text="Register Page", command=register_button_clicked,fg_color="#4444FF",text_color="black",corner_radius=8,font=("New Roman",20))
    regbut.place(x=30,y=85)    

    # Switch !!!
    # switch_var = StringVar(value="on")
    # switch = CTkSwitch(top, text="Mode", command=mode, variable=switch_var) 
    # switch.grid(row=1, column=2)

    # Email id
    # User Label
    user = CTkLabel(toplog, text="Email id",font=("New Roman",30))
    user.place(x=255,y=195)
    # User Entry
    user_entry = CTkEntry(toplog, placeholder_text="Enter the Email id",width=400,height=50,justify=CENTER,font=("New Roman",25))
    user_entry.place(x=420,y=185)

    # Password
    # Password Label
    pswd = CTkLabel(toplog, text="Password",font=("New Roman",30))
    pswd.place(x=240,y=260)
    # Password Entry
    pswd_entry = CTkEntry(toplog, placeholder_text="Enter the Password",width=400,height=50,justify=CENTER,font=("New Roman",25))
    pswd_entry.place(x=420,y=252)
    pswd_entry.configure(show="*")

    # Forgot Password Button for login
    userbtn = CTkButton(toplog, text="Forgot Password ?", command=forgot_button_click,corner_radius=50,width=150,height=40,font=("New Roman",20),fg_color="#4444FF")
    userbtn.place(x=420,y=350)

    # Submit Button for login
    userbtn = CTkButton(toplog, text="Submit ✔", command=login_status,corner_radius=50,width=150,height=40,font=("New Roman",20),fg_color="#4444FF")
    userbtn.place(x=650,y=350)
    
    toplog.mainloop()



#------------------------------------------------------------------Forgot Password Page--------------------------------------------------------------#

def testforgot():
    global topforg
    customtkinter.set_default_color_theme("dark-blue")   # green,blue,dark-blue
    # customtkinter.set_appearance_mode("dark")      # system,light,dark
    customtkinter.set_widget_scaling(1.3)
    customtkinter.set_window_scaling(1.0)

    def get_otp():
        a=random.randint(10000, 99999)
        return str(a)

    def otpp():
        button1.configure(state=DISABLED)
        global otp
        email=type_email.get()
        otp=get_otp()
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.ehlo()
        server.login('abcd@gmail.com', 'app password')
        server.sendmail('abcd@gmail.com', email, otp)
        print('message sent',otp)
        CTkMessagebox(title="status",message= "Successfully Sent OTP",icon="check",option_1="Thanks",fade_in_duration=(2)) 

    def verify():
        otp_ori=otp
        otp_typ=type_otp.get()

        # Mysql
        db = mysql.connector.connect(host="hostname", user="username", password="*****", database="database name")
        cur=db.cursor()
        sel="select * from tablename where Email_id = %s"
        val=type_email.get()
        cur.execute(sel, (val,))
        result=cur.fetchall()
        if len(result)>0 and otp_ori == otp_typ:
            query="update tablename set Password = %s ,Retype_Pswd = %s"
            value=(change.get(),change.get())
            cur.execute(query,value)
            db.commit()
            CTkMessagebox(title="status", message="Password Successfully changed.", icon="check", option_1="Thanks",fade_in_duration=(2))
            topforg.destroy()
            return testlogin()
        else:
            CTkMessagebox(title="status", message="Invaild OTP, please try again", icon="cancel", option_1="Ok",fade_in_duration=(2))
            cur.execute("rollback")
            topforg.destroy()
            return testforgot()
    
    def home_button_clicked3():
        # Perform register logic
        # Destroy the tophom window
        topforg.destroy()
        testhome()

    def register_button_clicked1():
        # Perform register logic
        # Destroy the tophom window
        topforg.destroy()
        testreg()

    topforg=CTkToplevel()
    topforg.title("Forgot Password")
    topforg.geometry('530x300')
    topforg.attributes('-fullscreen', True)
    # top.config(background="blue")

    # Forgot Password Page !!!
    display=CTkLabel(topforg,text="Forgot Password Page",fg_color="#4444FF",corner_radius=8,font=("New Roman",30))
    display.grid(row=1,column=0,padx=10,pady=5)

    # Home button
    # logpic1=ImageTk.PhotoImage(Image.open("home.png").resize((20,20),Image.ANTIALIAS))
    forpic1 = CTkImage(light_image=Image.open("home.png"), size=(20, 20))

    hombut3 = CTkButton(topforg, image=forpic1, text="Home Page", command=home_button_clicked3,fg_color="#4444FF",text_color="black",corner_radius=8,font=("New Roman",20))
    hombut3.place(x=30,y=50)

    # Register button
    # logpic2=ImageTk.PhotoImage(Image.open("register.png").resize((20,20),Image.ANTIALIAS))
    logpic2 = CTkImage(light_image=Image.open("register.png"), size=(20, 20))

    regbut = CTkButton(topforg, image=logpic2, text="Register Page", command=register_button_clicked1,fg_color="#4444FF",text_color="black",corner_radius=8,font=("New Roman",20))
    regbut.place(x=30,y=85)    

    # User Email-id 
    email_lab=CTkLabel(topforg,text="Email id",font=("New Roman",30))
    email_lab.place(x=220,y=175)
    type_email=CTkEntry(topforg,placeholder_text="Enter the Email",width=400,height=50,justify=CENTER,font=("New Roman",25))
    type_email.place(x=400,y=165)

    # Enter OTP 
    type_otp=CTkEntry(topforg,placeholder_text="Enter the OTP",width=210,justify=CENTER,font=("New Roman",25))
    type_otp.place(x=495,y=225)

    # Send OTP
    button1=CTkButton(topforg,text="Send OTP",command=otpp,width=50,height=35,corner_radius=50,font=("New Roman",15),fg_color="#4444FF")
    button1.place(x=810,y=173)

    # Re-send OTP
    button2=CTkButton(topforg,text="Re-send OTP",command=otpp,width=50,height=35,corner_radius=50,font=("New Roman",15),fg_color="#4444FF")
    button2.place(x=800,y=225)

    # New Password
    chan_pswd=CTkLabel(topforg,text="New Password",font=("New Roman",30))
    chan_pswd.place(x=180,y=290)
    change=CTkEntry(topforg,placeholder_text="Enter New Password",width=400,height=50,justify=CENTER,font=("New Roman",25))
    change.place(x=400,y=282)

    # Change Password
    button4=CTkButton(topforg,text="Change Password",command=verify,width=100,height=40,corner_radius=50,font=("New Roman",20),fg_color="#4444FF")
    button4.place(x=500,y=380)

    topforg.mainloop()



#-------------------------------------------------------------------------QR Page--------------------------------------------------------------------#

def testqr():
    global val
    global topqr
    def gen():
        user = weben.get()
        print("The entered website is " + user)
        
        # Getting the Url of the input Site
        query = user
        api_key ="API key"
        cx = "custom search engine"
        url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={api_key}&cx={cx}&num=4"
        
        # Response
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            websites = {}
            for item in data["items"]:
                title = item["title"]
                link = item["link"]
                websites[title] = link
        else:
            print("Failed to fetch data.!!!")
        
        # Adding regular expression to handle KeyError
        try:
            match = next((title for title in websites if re.search(user, title, re.IGNORECASE)), None)
            if match is not None:
                QR_link = websites[match]
            else:
                raise KeyError
        except KeyError:
            print("No match found for: " + user)

        print(websites[match])

        # Deleting the existing image file if it exists
        if os.path.exists('QR.png'):
            os.remove('QR.png')

        # Creating and saving QR_Code.
        QR_link = websites[match]
        QR = qrcode.make(QR_link,box_size=8)
        QR.save('QR.png')
        print("Successfully created the QR of " + user)
        CTkMessagebox(title="QR Created",message="Successfully created the QR for:\n\t" + user,icon="check",option_1="Thanks",fade_in_duration=(2))

        # Updating the image of the picbut button
        new_image = PhotoImage(file='QR.png')
        picbut.configure(image=new_image)
        picbut.image = new_image  # Assign the image to a property to avoid garbage collection

        # Displaying the QR_Code in matplotlib format.
        img = plt.imread('QR.png')
        fig, ax = plt.subplots(figsize=(6, 6), dpi=60)
        ax.imshow(img)
        ax.set_title(user, fontsize=20)
        plt.axis('off')
        plt.tight_layout()

    def home_button_clicked3():
        # Perform register logic
        # Destroy the tophom window
        topqr.destroy()
        testhome()

    def logout_button_clicked():
        # Perform register logic
        # Destroy the tophom window
        msg=CTkMessagebox(title="Logout",message= "Do you want to logout?", icon="question", option_1="No",option_2="Yes",fade_in_duration=(2))
        response=msg.get()
        if response=="Yes":
            topqr.destroy()
        else:
            topqr.destroy()
            testqr()

    def del_account():
        msg=CTkMessagebox(title="Delete account",message= "Do you want to delete account?", icon="question", option_1="No",option_2="Yes",fade_in_duration=(2))
        response=msg.get()
        if response=="Yes":
            print(id+" account got deleted")
            db = mysql.connector.connect(host="hostname", user="username", password="*****", database="database name")
            cur = db.cursor()
            query = "DELETE FROM tablename WHERE Email_id = %s "
            cur.execute(query, (id,))
            db.commit()
            # result = cur.fetchall()
            msg1=CTkMessagebox(title="Deleted",message= "Account deleted successfully", icon="check", option_1="Ok",fade_in_duration=(2))
            res=msg1.get()
            if res=="Ok":
                topqr.destroy()
                testhome()
        else:
            topqr.destroy()
            testqr()


    def msg():
        CTkMessagebox(title="Support Request",message="If you are interested in supporting the  project or would like more information,\n contact us directly at: \n\n botminds.co@gmail.com",width=450,height=250,icon="info",option_1="Ok",fade_in_duration=(2))

    def callback(url):
        webbrowser.open("https://mail.google.com/mail/u/0/#inbox?compose=lqrslzLsqksxskCXLMLFsfxdzMckwCBxVBjBzPSXNgRwQgwsXnXqsCXbQNMQqRpZHVjWkKZTHPmWPNXJK")


    def support():
        global paybut,link1
        a=random.randint(0,1)
        if check_var.get()=="on":
            if a==0:
                # Display the payment picture
                paypic = CTkImage(light_image=Image.open("pankeshpayment.png"), size=(250, 300))
                paybut = CTkButton(topqr, image=paypic, text="", command=msg,fg_color="green",width=100,height=300)
                paybut.place(x=720,y=130)
            else:
                # Display the payment picture
                paypic = CTkImage(light_image=Image.open("anuragpayment.png"), size=(250, 300))
                paybut = CTkButton(topqr, image=paypic, text="", command=msg,fg_color="green",width=100,height=300)
                paybut.place(x=720,y=130)
            
            # Remove the link1 label if it exits
            if link1 is not None:
                link1.place_forget()
        else:
            # Remove the link1 label if it exits
            if paybut is not None:
                paybut.place_forget()

            link1 = CTkLabel(topqr, text="pankesh167@gmail.com",text_color="#4444FF", cursor="hand2",font=("New Roman",25))
            link1.place(x=700,y=130)
            link1.bind("<Button-1>", callback)
    
    customtkinter.set_default_color_theme("dark-blue")
    customtkinter.set_widget_scaling(1.3)
    customtkinter.set_window_scaling(1.0)


    topqr = CTkToplevel()
    topqr.title("QR-Page")
    topqr.geometry("450x300")
    topqr.attributes("-fullscreen", True)

    qrla = CTkLabel(topqr,text="QR Page",fg_color="#4444FF",corner_radius=8,font=("New Roman",30))
    qrla.grid(row=1, column=1, padx=10, pady=5)

    # Home button
    # logpic1=ImageTk.PhotoImage(Image.open("home.png").resize((20,20),Image.ANTIALIAS))
    qrpic1 = CTkImage(light_image=Image.open("home.png"), size=(20, 20))

    hombut4 = CTkButton(topqr, image=qrpic1, text="Home", command=home_button_clicked3,fg_color="#4444FF",width=100,text_color="black",corner_radius=8,font=("New Roman",20))
    hombut4.place(x=30,y=50)

    # Logout button
    # logpic2=ImageTk.PhotoImage(Image.open("register.png").resize((20,20),Image.ANTIALIAS))
    qrpic2 = CTkImage(light_image=Image.open("logout.png"), size=(20, 20))

    logbut = CTkButton(topqr, image=qrpic2, text="Logout", command=logout_button_clicked,fg_color="#4444FF",width=100,text_color="black",corner_radius=8,font=("New Roman",20))
    logbut.place(x=30,y=85) 

    # Delete account
    qrpic3=CTkImage(light_image=Image.open("delete.png"),size=(20,20))

    delbut = CTkButton(topqr, image=qrpic3, text="Account",command=del_account,fg_color="#4444FF",width=100,text_color="black",corner_radius=8,font=("New Roman",20))
    delbut.place(x=30,y=120)

    # Enter
    weben = CTkEntry(topqr, placeholder_text="Enter the website name ", font=("New Roman", 20), width=350, height=60,justify=CENTER)
    weben.place(x=350,y=50)

    webpic = CTkImage(light_image=Image.open("QR.png"), size=(200, 200))

    # weblab=CTkLabel(top,text="QR-code of" + weben.get(),font=("New Roman",20),corner_radius=8)
    # weblab.grid(row=8,column=2)

    picbut = CTkButton(topqr, image=webpic, text="", command=gen,fg_color="#4444FF")
    picbut.place(x=385,y=130)

    # check1=CTkCheckBox(topqr,text="Support",command=support,width=200,height=100)
    check_var = StringVar()
    check1 = CTkCheckBox(topqr, text="Want to support us?", command=support,variable=check_var, onvalue="on", offvalue="off")
    check1.place(x=720,y=68)

    # Payment pic
    # paypic = CTkImage(light_image=Image.open("pankeshpayment.png"), size=(250, 300))

    # weblab=CTkLabel(top,text="QR-code of" + weben.get(),font=("New Roman",20),corner_radius=8)
    # weblab.grid(row=8,column=2)

    # paybut = CTkButton(topqr, image=paypic, text="", command=support,fg_color="green",width=100,height=300)
    # paybut.place(x=720,y=130)

    topqr.mainloop()



#------------------------------------------------------------------------Home Page------------------------------------------------------------------#

def testhome():    
    global tophom
    customtkinter.set_default_color_theme("dark-blue")   # green,blue,dark-blue
    # customtkinter.set_appearance_mode("dark")      # system,light,dark
    customtkinter.set_widget_scaling(1.3)
    customtkinter.set_window_scaling(1.0)
    
    def flag():
        tophom.destroy()
        testindex()
    
    tophom=CTkToplevel()
    tophom.title("Home")
    # tophom.geometry("750x1200")
    tophom.attributes('-fullscreen', True)

    # Home Page !!!
    display=CTkLabel(tophom,text="Home Page",fg_color="#4444FF",corner_radius=8,font=("New Roman",30))
    display.grid(row=1,column=1,padx=10,pady=5)

    # Start pic
    startpic = CTkImage(light_image=Image.open("start.png"), size=(20, 20))

    startbut1 = CTkButton(tophom, image=startpic, text="Index Page", command=flag,fg_color="#4444FF",text_color="black",corner_radius=8,font=("New Roman",20))
    startbut1.place(x=20,y=50)

    # Switch !!!
    switch_var = StringVar(value="on")
    switch = CTkSwitch(tophom, text="Mode", command=mode, variable=switch_var) 
    switch.place(x=490,y=30)

    # Welcome !!!
    txt="Welcome to QR-Automation"
    text = ""
    count = 0
    display=CTkLabel(tophom,text=text,fg_color="#4444FF",font=("New Roman",70),height=120,corner_radius=10)
    display.place(x=80,y=150)

    def ani():
        nonlocal count, text
        if count >= len(txt):
            count = 0
            text = ""
        else:
            text = text + txt[count]
            count += 1
        display.configure(text=text)
        display.after(100, ani)

    def start_animation():
        nonlocal count, text
        count = 0
        text = ""
        ani()

    def register_button_clicked():
        # Perform register logic
        # Destroy the tophom window
        tophom.destroy()
        testreg()

    def login_button_clicked():
        # Perform login logic
        # Destroy the tophom window
        tophom.destroy()
        testlogin()

    # Register button !!!
    homereg=CTkButton(tophom,text="Register",corner_radius=10,command=register_button_clicked,width=150,height=40,font=("New Roman",20),fg_color="#4444FF")
    homereg.place(x=340,y=350)

    # Login button !!!
    homelog=CTkButton(tophom,text="Login",corner_radius=10,command=login_button_clicked,width=150,height=40,font=("New Roman",20),fg_color="#4444FF")
    homelog.place(x=550,y=350)

    tophom.after(0, start_animation)
    tophom.mainloop()



#------------------------------------------------------------------------Index Page------------------------------------------------------------------#

def testindex():
    global topind
    customtkinter.set_default_color_theme("dark-blue")   # green,blue,dark-blue
    # customtkinter.set_appearance_mode("dark")      # system,light,dark
    customtkinter.set_widget_scaling(1.3)
    customtkinter.set_window_scaling(1.0)
    
    def ind():
        topind.destroy()
        testhome()

    topind=CTkToplevel()
    topind.title("Index")
    # topind.geometry("750x1200")
    topind.attributes('-fullscreen', True)

    # Switch !!!
    switch_var = StringVar()
    switch = CTkSwitch(topind, text="Mode", command=mode, variable=switch_var) 
    switch.place(x=490,y=30)

    # Index Page !!!
    inddis=CTkLabel(topind,text="Index Page",fg_color="#4444FF",corner_radius=8,font=("New Roman",30))
    inddis.grid(row=1,column=1,padx=10,pady=5)

    # Index pic
    indpic = CTkImage(light_image=Image.open("index.png"), size=(700, 150))
    indbut = CTkButton(topind, image=indpic, text="", command=ind,fg_color="#4444FF",width=700,height=180,corner_radius=10)
    indbut.place(x=160,y=190)

    topind.mainloop()

testindex()
