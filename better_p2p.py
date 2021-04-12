import socket
import threading
 
ENCODING = 'utf-8'
 
 
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

        while True:
            connection, client_address = sock.accept()
            try:
                full_message = ""
                while True:
                    data = connection.recv(16)
                    full_message = full_message + data.decode(ENCODING)
                    if not data and self.friend_user == '':
                        self.friend_user = full_message

                    elif not data:
                        print('\n')
                        print("{}: {}".format(self.friend_user, full_message.strip()))
                        print('\n')
                        break
            finally:
                connection.shutdown(2)
                connection.close()
 
    def run(self):
        self.listen()
 
 
class Sender(threading.Thread):
 
    def __init__(self, my_friends_host, my_friends_port, username):
        threading.Thread.__init__(self, name="messenger_sender")
        self.host = my_friends_host
        self.port = my_friends_port
        self.user = username
 
    def run(self):
        try:
            while True:
                message = input('')
                if message == '':
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((self.host, self.port))
                    s.sendall(self.user.encode(ENCODING))
                    s.shutdown(2)
                    s.close()

                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((self.host, self.port))
                s.sendall(message.encode(ENCODING))
                s.shutdown(2)
                s.close()
        except KeyboardInterrupt:
            s.close()
        except Exception as e:
            print(e)
 
def main():
    my_username = input("What is your username? ")
    my_host = input("which is my host? ")
    my_port = int(input("which is my port? "))
    receiver = Receiver(my_host, my_port)
    my_friends_host = input("what is your friend's host? ")
    my_friends_port = int(input("what is your friend's port? "))
    sender = Sender(my_friends_host, my_friends_port, my_username)
    treads = [receiver.start(), sender.start()]
 
 
if __name__ == '__main__':
    main()
