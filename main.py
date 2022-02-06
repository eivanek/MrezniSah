from tkinter import *
from login import LoginScreen
from register import RegisterScreen
import pygame as pg
from client import Client


def login_clicked():
    LoginScreen(root, client)
    root.withdraw()

def register_clicked():
    RegisterScreen(root, client)
    root.withdraw()

def exit_game_clicked():
    exit()


def main():
    WIDTH = 900
    HEIGHT = 900
    root.configure(background="#eb345f")
    root.resizable(False, False)
    root.title("Mrežni šah")
    root.geometry("900x900")
    back = Frame(master=root, bg='#eb345f')
    back.pack_propagate(0)

    f_label = Frame(root, height=100, width=WIDTH)
    f_label.pack_propagate(0)
    f_label.place(x=0, y=0)
    label = Label(f_label, text='Mrežni šah', font=("Tahoma", 24))
    label.pack(fill=BOTH, expand=1)

    f_b1 = Frame(root, height=100, width=WIDTH)
    f_b1.pack_propagate(0)
    f_b1.place(x=0, y=300)
    button_login = Button(f_b1, text="Prijava", command=login_clicked, font=("Tahoma", 18))
    button_login.pack(fill=BOTH, expand=1)

    f_b2 = Frame(root, height=100, width=WIDTH)
    f_b2.pack_propagate(0)
    f_b2.place(x=0, y=450)
    button_register = Button(f_b2, text="Registracija", command=register_clicked, font=("Tahoma", 18))
    button_register.pack(fill=BOTH, expand=1)

    f_b3 = Frame(root, height=100, width=WIDTH)
    f_b3.pack_propagate(0)
    f_b3.place(x=0, y=600)
    button_exit = Button(f_b3, text="Izlaz", command=exit_game_clicked, font=("Tahoma", 18))
    button_exit.pack(fill=BOTH, expand=1)

    root.mainloop()


if __name__ == '__main__':
    pg.init()
    root = Tk()
    global client
    client = Client()
    main()
