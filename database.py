import transaction
from persistent.dict import PersistentDict
from persistent.list import PersistentList
from db_connection import DBConnection
from ZODB.POSException import ConflictError
import time

class Database:
    def __init__(self, database_name, address, port):
        db = DBConnection(database_name=database_name, address=address, port=port)
        self.db_connection, self.root = db.create_connection()

    def username_exists(self, username):
        try:
            exists = len([user for user in self.root['users'] if user.username == username]) > 0
            return exists
        except KeyError:
            self.root['users'] = PersistentList()
            return False

    def user_exists(self, login_user):
        try:
            user_exists = len([user for user in self.root['users'] if
                        user.username == login_user.username and user.password == login_user.password]) > 0
            return user_exists
        except KeyError:
            self.root['users'] = PersistentList()
            return False

    def register_user(self, user):
        transaction.begin()
        try:
            self.root['users'].extend([user])
        except KeyError:
            self.root['users'] = PersistentList()
            self.root['users'].extend([user])
        transaction.commit()

    def update_board(self, game):
        while True:
            try:
                transaction.begin()
                try:
                    self.root['games_playing'][game.game_name].board = game.board
                except Exception as e:
                    print("Error:", str(e))
                transaction.commit()
            except ConflictError or ValueError:
                transaction.abort()
                time.sleep(1)
                pass
            else:
                break

    def insert_new_game(self, game):
        transaction.begin()
        try:
            self.root['games_playing'][game.game_name] = game
        except KeyError:
            self.root['games_playing'] = PersistentDict()
            self.root['games_playing'][game.game_name] = game
        transaction.commit()

    def get_user(self, username):
        try:
            user = [user for user in self.root['users'] if user.username == username][0]
            return user
        except KeyError:
            return

    def get_game(self, game_name):
        self.db_connection.sync()
        try:
            return self.root['games_playing'][game_name]
        except KeyError:
            return

    def get_playing_games(self):
        self.db_connection.sync()
        try:
            return self.root['games_playing']
        except KeyError:
            transaction.begin()
            self.root['games_playing'] = PersistentDict()
            transaction.commit()

    def set_game_ready(self, game_name):
        transaction.begin()
        try:
            self.root['games_playing'][game_name].ready = True
        except Exception as e:
            print("Error:", str(e))
        transaction.commit()

    def remove_game(self, game_name):
        self.db_connection.sync()
        transaction.begin()
        try:
            del self.root['games_playing'][game_name]
        except KeyError:
            return
        transaction.commit()

    def set_winner(self, username):
        transaction.begin()
        user = self.get_user(username)
        user.games_won += 1
        try:
            for i, user in enumerate(self.root['users']):
                if user.username == username:
                    self.root['users'][i] = user
        except Exception as e:
            print("Error:", str(e))
        transaction.commit()

    def set_loser(self, username):
        transaction.begin()
        user = self.get_user(username)
        user.games_lost += 1
        try:
            for i, user in enumerate(self.root['users']):
                if user.username == username:
                    self.root['users'][i] = user
        except Exception as e:
            print("Error:", str(e))
        transaction.commit()
