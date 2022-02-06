from tkinter import *
from pymsgbox import alert
from user import User
from main_menu import MainMenu

class LoginScreen(Toplevel):

    def __init__(self, master, client):
        super().__init__(master=master)
        self.title("Prijava")
        self.geometry("900x900")
        self.configure(background="#eb345f")
        self.resizable(False, False)

        self.client = client
        self.username = StringVar()
        self.passw = StringVar()

        f_label = Frame(self, height=100, width=900)
        f_label.pack_propagate(0)
        f_label.place(x=0, y=0)
        label_title = Label(f_label, text='Mrežni šah: Prijava', font=("Tahoma", 24))
        label_title.pack(fill=BOTH, expand=1)

        f_label_username = Frame(self, height=50, width=900)
        f_label_username.pack_propagate(0)
        f_label_username.place(x=0, y=300)
        label_login = Label(f_label_username, text='Korisničko ime', font=("Tahoma", 18), background="#e3073b")
        label_login.pack(fill=BOTH, expand=1)

        f_username_entry = Frame(self, height=50, width=900)
        f_username_entry.pack_propagate(0)
        f_username_entry.place(x=0, y=370)
        login_entry = Entry(f_username_entry, textvariable=self.username, font=('Tahoma', 18), justify='center')
        login_entry.pack(fill=BOTH, expand=1)

        f_label_passw = Frame(self, height=50, width=900)
        f_label_passw.pack_propagate(0)
        f_label_passw.place(x=0, y=470)
        label_login = Label(f_label_passw, text='Lozinka', font=("Tahoma", 18), background="#e3073b")
        label_login.pack(fill=BOTH, expand=1)

        f_passw_entry = Frame(self, height=50, width=900)
        f_passw_entry.pack_propagate(0)
        f_passw_entry.place(x=0, y=540)
        login_entry = Entry(f_passw_entry, textvariable=self.passw, font=('Tahoma', 18), justify='center', show="*")
        login_entry.pack(fill=BOTH, expand=1)

        f_login_button = Frame(self, height=50, width=900)
        f_login_button.pack_propagate(0)
        f_login_button.place(x=0, y=640)
        button_login = Button(f_login_button, text="Prijava", command=self.login_user, font=("Tahoma", 18))
        button_login.pack(fill=BOTH, expand=1)

        f_back_button = Frame(self, height=50, width=900)
        f_back_button.pack_propagate(0)
        f_back_button.place(x=0, y=720)
        button_back = Button(f_back_button, text="Natrag", command=self.back, font=("Tahoma", 18))
        button_back.pack(fill=BOTH, expand=1)


    def login_user(self):
        username = self.username.get()
        password = self.passw.get()
        user = User(username, password)
        user_exists = self.client.send(msg="login_user", data=user, return_response=True)
        if user_exists:
            self.client.set_username(username)
            MainMenu(self.master, self.client)
            self.withdraw()
        else:
            alert(title="Error", text="Ne postoji korisnik sa unesenim podacima", button="OK")

    def back(self):
        self.master.deiconify()
        self.destroy()
