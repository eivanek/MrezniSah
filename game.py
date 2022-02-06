from chess import Board
from persistent import Persistent


class Game(Persistent):
    def __init__(self, game_name, player_name):
        self.board = Board()
        self.game_name = game_name
        self.ready = False
        self.player_name = player_name
