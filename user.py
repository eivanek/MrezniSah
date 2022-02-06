from persistent import Persistent


class User(Persistent):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.games_won = 0
        self.games_lost = 0
