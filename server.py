import pickle
import socket
from threading import Thread
from database import Database


def new_thread(connection):
    database = Database(database_name, database_adr, database_port)
    while True:
        try:
            request = connection.recv(8192 * 3)
            if not request:
                break
            else:
                data_request = pickle.loads(request)
                database_request = data_request.msg
                if database_request == "username_exists":
                    username = data_request.data
                    username_exists = database.username_exists(username)
                    response = pickle.dumps(username_exists)
                    connection.sendall(response)
                elif database_request == "login_user":
                    user = data_request.data
                    user_exists = database.user_exists(user)
                    response = pickle.dumps(user_exists)
                    connection.sendall(response)
                elif database_request == "register_user":
                    new_user = data_request.data
                    database.register_user(new_user)
                    connection.sendall(b"200")
                elif database_request == "update_board":
                    database.update_board(data_request.data)
                    connection.sendall(b"200")
                elif database_request == "insert_new_game":
                    database.insert_new_game(data_request.data)
                    connection.sendall(b"200")
                elif database_request == "get_game":
                    game_name = data_request.data
                    game = database.get_game(game_name)
                    response = pickle.dumps(game)
                    connection.sendall(response)
                elif database_request == "get_playing_games":
                    all_games = database.get_playing_games()
                    response = pickle.dumps(all_games)
                    connection.sendall(response)
                elif database_request == "set_game_ready":
                    game_name = data_request.data
                    database.set_game_ready(game_name)
                    connection.sendall(b"200")
                elif database_request == "remove_game":
                    game_name = data_request.data
                    database.remove_game(game_name)
                    connection.sendall(b"200")
                elif database_request == "set_winner":
                    username = data_request.data
                    database.set_winner(username)
                    connection.sendall(b"200")
                elif database_request == "set_loser":
                    username = data_request.data
                    database.set_loser(username)
                    connection.sendall(b"200")
                elif database_request == "get_user":
                    username = data_request.data
                    user = database.get_user(username)
                    response = pickle.dumps(user)
                    connection.sendall(response)
        except Exception as e:
            print(e)
    connection.close()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server = "10.0.2.15"
port = 2700

database_port = 2709
database_adr = 'localhost'
database_name = 'baza.fs'

try:
    s.bind((server, port))
except socket.error as e:
    print("Gre??ka:", str(e))

s.listen()
current_total_conn = 0
print("??ekam konekciju.")


while True:
    if current_total_conn < 8:
        conn, addresponses = s.accept()
        current_total_conn += 1
        print("Spojena je nova konekcija...trenutno konekcija: ", current_total_conn)
        thread = Thread(target=new_thread, args=(conn, addresponses))
        thread.setDaemon(True)
        thread.start()
