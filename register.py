from tkinter import *
from pymsgbox import alert
from user import User
from main_menu import MainMenu

class RegisterScreen(Toplevel):

    def __init__(self, master, client):
        super().__init__(master=master)
        self.title("Registracija")
        self.geometry("900x900")
        self.configure(background="#eb345f")
        self.resizable(False, False)

        self.client = client
        self.username = StringVar()
        self.passw = StringVar()

        f_label = Frame(self, height=100, width=900)
        f_label.pack_propagate(0)
        f_label.place(x=0, y=0)
        label_title = Label(f_label, text='Mrežni šah: Registracija', font=("Tahoma", 24))
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
        button_login = Button(f_login_button, text="Registracija", command=self.register_user, font=("Tahoma", 18))
        button_login.pack(fill=BOTH, expand=1)

        f_back_button = Frame(self, height=50, width=900)
        f_back_button.pack_propagate(0)
        f_back_button.place(x=0, y=720)
        button_back = Button(f_back_button, text="Natrag", command=self.back, font=("Tahoma", 18))
        button_back.pack(fill=BOTH, expand=1)

    def register_user(self):
        username = self.username.get()
        password = self.passw.get()
        user = User(username, password)
        if not self.check_registration_fields(username, password):
            return
        self.client.send(msg="register_user", data=user, return_response=False)
        self.client.set_username(username)
        self.withdraw()
        MainMenu(self.master, self.client)


    def check_registration_fields(self, username, password):
        if len(username) == 0:
            alert(title="Greška", text="Polje korisničkog imena je prazno", button="Ok")
            return False
        if len(password) < 6:
            alert(title="Greška", text="Lozinka mora imati najmanje 6 znakova", button="Ok")
            return False
        username_exists = self.client.send(msg="username_exists", data=username, return_response=True)
        if username_exists:
            alert(title="Greška", text="Uneseno korisničko ime već postoji", button="Ok")
            return False
        return True

    def back(self):
        self.master.deiconify()
        self.destroy()