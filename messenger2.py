import socket
import threading
 
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
                            #print('\n')
                            print(self.friend_user + full_message.strip())
                            #print('\n')
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
        try:
            while True:
                message = input(my_username + ": ")
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
