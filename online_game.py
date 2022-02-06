import time
from pymsgbox import alert
from functions import *
import chess


class OnlineGame:
    def __init__(self, client, game, white_player):
        self.client = client
        self.game = game
        self.white_player = white_player
        self.width = 900
        self.height = 900
        self.square_size = self.width // 8
        self.game_display = pg.display.set_mode((self.width, self.height))
        self.background = pg.Surface((self.width, self.height))
        self.running = True

    def start(self):
        print("Čekam protivnika...")
        while self.running and not self.game.ready:
            self.game = self.client.send(msg="get_game", data=self.game.game_name, return_response=True)
            time.sleep(0.5)
        print("Pronađen je protivnik, igra može započeti.")

        clock = pg.time.Clock()
        self.change_board(clock)
        while self.running and self.game.ready:
            if self.is_my_turn():
                from_x, from_y = 0, 0
                to_x, to_y = 0, 0
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        self.quit_game()
                    if event.type == pg.MOUSEBUTTONDOWN:
                        pos = pg.mouse.get_pos()
                        from_x, from_y = convert_coordinates_to_array(pos[0], pos[1], self.square_size)
                        move_from = array_to_move(from_x, from_y)
                        mouse_pressed = False
                        while not mouse_pressed:
                            for new_event in pg.event.get():
                                if new_event.type == pg.QUIT:
                                    self.quit_game()
                                if new_event.type == pg.MOUSEBUTTONDOWN:
                                    pos = pg.mouse.get_pos()
                                    mouse_pressed = True
                                    to_x, to_y = convert_coordinates_to_array(pos[0], pos[1], self.square_size)
                                    move_to = array_to_move(to_x, to_y)
                                    move = str(move_from) + str(move_to)
                                    if chess.Move.from_uci(move) in self.game.board.legal_moves: 
                                        self.game.board.push_san(move)
                                        print(self.game.board)
                if not self.is_my_turn():
                    self.client.send(msg="update_board", data=self.game, return_response=False)
                    if self.game.board.checkmate:
                        self.running = False
                        self.client.send(msg="set_winer", data=self.client.username, return_response=False)
                        alert(text="Šahmat, pobijedili ste!", button="Ok")
                pg.display.flip()
                clock.tick(30)
            else:
                self.change_board(clock)
                time.sleep(0.5)
        pg.quit()


    def is_my_turn(self):
        return self.white_player == self.game.board.turn

    def change_board(self, clock):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit_game()
                return
        self.game = self.client.send(msg="get_game", data=self.game.game_name, return_response=True)
        if self.game is None:
            alert(text="Protivnik je odustao od igre.", button="Ok")
            self.running = False
            return
        if self.game.board.is_checkmate():
            self.running = False
            self.client.send(msg="set_loser", data=self.client.username, return_response=False)
            alert(text="Šahmat, izgubili ste!", button="Ok")
            self.quit_game()
            return
        pg.display.flip()
        clock.tick(30)

    def quit_game(self):
        self.client.send(msg="set_loser", data=self.client.username, return_response=False)
        self.client.send(msg="remove_game", data=self.game.game_name, return_response=False)
        self.running = False
        alert(text="Odustali ste od igre!", button="Ok")
