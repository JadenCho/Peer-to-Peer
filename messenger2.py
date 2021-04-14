import socket
import threading
import sqlite3
from sqlite3 import Error
import select
import sys
 
ENCODING = 'utf-8'
my_username = input("What is your username? ")
HEADER_LENGTH = 10

class Receiver(threading.Thread):
 
    def __init__(self, my_host, my_port):
        threading.Thread.__init__(self, name="messenger_receiver")
        self.host = my_host
        self.port = my_port
        self.friend_user = ''
 
    def listen(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.host, self.port))    
        sock.listen(10)

        database = r"C:\sqlite\db\pythonsqlite.db"
        con = sqlite3.connect(database)
        connect = con.cursor()

        users = '''CREATE TABLE chat_users_recv(
            username text,
            message text)'''

        try:
            connect.execute(users)

        except Error as t:
            print('')

        sql = '''INSERT INTO chat_users_recv(username, message) VALUES(?,?)'''

        while True:
            connection, client_address = sock.accept()
            try:
                full_message = ""
                while True:
                    user = connection.recv(4096).decode(ENCODING)
                    self.friend_user = user 
                    if not user: break

                    while True:
                        data = connection.recv(4096)
                        full_message = full_message + data.decode(ENCODING)

                        if not data and self.friend_user == '':
                            self.friend_user = user
                            break

                        elif not data:
                            print('\n')
                            print(self.friend_user + full_message.strip())
                            print('--------------------------------\n')

                            connect.execute(sql, (self.friend_user, full_message.strip()))
                            con.commit()
                            break
            finally:
                connection.shutdown(2)
                connection.close()

    def recv_one(sock):
        lengthbuf = recvall(sock, 4)
        length = struct.unpack('!', lengthbuf)
        return recvall(sock, length)
 
    def run(self):
        self.listen()
 
 
class Sender(threading.Thread):
 
    def __init__(self, my_friends_host, my_friends_port, my_username):
        threading.Thread.__init__(self, name="messenger_sender")
        self.host = my_friends_host
        self.port = my_friends_port
        self.user = my_username
 
    def run(self):
        database = r"C:\sqlite\db\pythonsqlite.db"
        con = sqlite3.connect(database)
        connect = con.cursor()

        users = '''CREATE TABLE chat_users_send(
            username text,
            message text)'''
        try:
            connect.execute(users)

        except Error as t:
            print('')

        sql = '''INSERT INTO chat_users_send(username, message) VALUES(?,?)'''

        try:
            while True:
                message = input(my_username + ": ")

                connect.execute(sql, (my_username, message))
                con.commit()

                my_username2 = my_username + ": "
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((self.host, self.port))
                user_send = my_username2.encode(ENCODING) + message.encode(ENCODING)
                s.send(user_send)
                s.shutdown(2)
                s.close()
        except KeyboardInterrupt:
            s.close()
        except Exception as e:
            print(e)

    def send_one(s, data):
        length = len(data)
        s.sendall(struct.pack('!I', length))
        s.sendall(data)
 
def main():
    my_host = input("which is my host? ")
    my_port = int(input("which is my port? "))
    receiver = Receiver(my_host, my_port)
    my_friends_host = input("what is your friend's host? ")
    my_friends_port = int(input("what is your friend's port? "))
    sender = Sender(my_friends_host, my_friends_port, my_username)
    treads = [receiver.start(), sender.start()]
 
 
if __name__ == '__main__':
    main()
