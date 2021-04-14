import socket
import select
import errno
import sys
import threading
from messenger2 import *

class Client(threading.Thread):

    def __init__(self, my_username):
        threading.Thread.__init__(self, name="messenger_client")
        self.host = "192.168.240.65"
        self.port = 1234
        self.user = my_username

    def client(self):

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.host, self.port))
        client_socket.setblocking(False)

        _username = self.user.encode('utf-8')
        _username_header = f"{len(_username):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(_username_header + _username)

        confirm = input('There are new users. \nPlease press "enter" to continue...\n')

        if not confirm:
            while True:
                try:
                    message_header = client_socket.recv(4096)
                    print(str(message_header.decode('utf-8')))
                    print('\n')
                finally:
                    break

    def run(self):
        self.client()

def main():
    username = input("Username: ")
    c = Client(username)
    c_tread = c.start()

    my_host = input("which is my host? ")
    my_port = int(input("which is my port? "))
    receiver = Receiver(my_host, my_port)
    my_friends_host = input("what is your friend's host? ")
    my_friends_port = int(input("what is your friend's port? "))
    sender = Sender(my_friends_host, my_friends_port, username)
    treads = [receiver.start(), sender.start()]


if __name__ == '__main__':
    main()

