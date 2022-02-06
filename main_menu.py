from tkinter import *
from pymsgbox import alert
from online_game import OnlineGame
from game import Game


class MainMenu(Toplevel):

    def __init__(self, master, client):
        super().__init__(master=master)
        self.title("Glavni Meni")
        self.geometry("900x900")
        self.configure(background="#eb345f")
        self.resizable(False, False)

        self.client = client
        self.username = self.client.username
        self.game_name = StringVar()

        f_label = Frame(self, height=100, width=900)
        f_label.pack_propagate(0)
        f_label.place(x=0, y=0)
        label_title = Label(f_label, text='Mrežni šah: Glavni Meni', font=("Tahoma", 24))
        label_title.pack(fill=BOTH, expand=1)

        self.show_stats()

        f_game_name_kabel = Frame(self, height=50, width=900)
        f_game_name_kabel.pack_propagate(0)
        f_game_name_kabel.place(x=0, y=250)
        game_name_kabel = Label(f_game_name_kabel, text='Kreiraj igru naziva:', font=("Tahoma", 18), background="#e3073b")
        game_name_kabel.pack(fill=BOTH, expand=1)

        f_game_name_entry = Frame(self, height=50, width=900)
        f_game_name_entry.pack_propagate(0)
        f_game_name_entry.place(x=0, y=320)
        game_name_entry = Entry(f_game_name_entry, textvariable=self.game_name, font=('Tahoma', 18), justify='center')
        game_name_entry.pack(fill=BOTH, expand=1)

        f_login_button = Frame(self, height=50, width=900)
        f_login_button.pack_propagate(0)
        f_login_button.place(x=0, y=390)
        button_login = Button(f_login_button, text="Kreiraj", command=self.create_game, font=("Tahoma", 18))
        button_login.pack(fill=BOTH, expand=1)

        self.show_playing_games()

        f_back_button = Frame(self, height=50, width=900)
        f_back_button.pack_propagate(0)
        f_back_button.place(x=0, y=820)
        button_back = Button(f_back_button, text="Odjava", command=self.back, font=("Tahoma", 18))
        button_back.pack(fill=BOTH, expand=1)


    def back(self):
        self.master.deiconify()
        self.destroy()

    def show_stats(self):
        user = self.client.send(msg="get_user", data=self.username, return_response=True)
        won = str(user.games_won)
        lost = str(user.games_lost)
        stats_label_text = f"STATISTIKA: POBIJEĐENO: {won}, IZGUBLJENO - {lost}"
        
        s_label = Frame(self, height=70, width=700)
        s_label.pack_propagate(0)
        s_label.place(x=0, y=150)
        label_title = Label(s_label, text=stats_label_text, font=("Tahoma", 18))
        label_title.pack(fill=BOTH, expand=1)

    def show_playing_games(self):       
        playing_games = self.client.send(msg="get_playing_games", data=None, return_response=True)
        if playing_games:
            for i, playing_game in enumerate(playing_games.values()):
                game_label = "PRIDRUŽI SE IGRI NAZIVA: " + playing_game.game_name
                f_join_button = Frame(self, height=70, width=900)
                f_join_button.pack_propagate(0)
                f_join_button.place(x=0, y=470+i*90)
                join_button = Button(f_join_button, text=game_label, command=lambda: self.join_game(playing_game), font=("Tahoma", 18))
                join_button.pack(fill=BOTH, expand=1)

    def join_game(self, game):
        self.client.send(msg="set_game_ready", data=game.game_name, return_response=False)
        online_game = OnlineGame(self.client, game, white_player=False)
        online_game.start()
        self.withdraw()
        self.back()


    def create_game(self):
        game_name = self.game_name.get()
        if len(game_name) == 0:
            alert("Ime igre ne smije biti prazno.", "Greška")
            return
        new_game = Game(game_name, self.client.username)
        self.client.send(msg="insert_new_game", data=new_game, return_response=False)
        online_game = OnlineGame(self.client, new_game, white_player=True)
        online_game.start()
        self.withdraw()
        self.back()