import socket
import select
import sys

HEADER_LENGTH = 10

IP = "192.168.240.65"
PORT = 1234

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))

server_socket.listen()

sockets_list = [server_socket]

clients = {}

client_name_list = []

print(f'Listening for connections on {IP}:{PORT}...')

def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)

        if not len(message_header):
            return False

        message_length = int(message_header.decode('utf-8').strip())

        return {'header': message_header, 'data': client_socket.recv(message_length)}

    except:
        return False

try:
    while True:

    # Calls Unix select() system call or Windows select() WinSock call with three parameters:
    #   - rlist - sockets to be monitored for incoming data
    #   - wlist - sockets for data to be send to (checks if for example buffers are not full and socket is ready to send some data)
    #   - xlist - sockets to be monitored for exceptions (we want to monitor all sockets for errors, so we can use rlist)
    # Returns lists:
    #   - reading - sockets we received some data on (that way we don't have to check sockets manually)
    #   - writing - sockets ready for data to be send thru them
    #   - errors  - sockets with some exceptions
    # This is a blocking call, code execution will "wait" here and "get" notified in case any action should be taken
        read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)


    # Iterate over notified sockets
        for notified_socket in read_sockets:

        # If notified socket is a server socket - new connection, accept it
            if notified_socket == server_socket:

            # Accept new connection
            # That gives us new socket - client socket, connected to this given client only, it's unique for that client
            # The other returned object is ip/port set
                client_socket, client_address = server_socket.accept()

            # Client should send his name right away, receive it
                user = receive_message(client_socket)

            # If False - client disconnected before he sent his name
                if user is False:
                    continue

            # Add accepted socket to select.select() list
                sockets_list.append(client_socket)

            # Also save username and username header
                clients[client_socket] = user

                print('Accepted new connection from {}:{}, username: {}'.format(*client_address, user['data'].decode('utf-8')))

                clist = [client_address, user['data'].decode('utf-8')]

                client_name_list.append(clist)

                #print(client_name_list)

                for client_name in client_name_list:
                    #print(client_name)
                    client_socket.send((str(client_name[0][0]) + ',' + str(client_name[0][1]) + ': ' + client_name[1]).encode('utf-8'))

        # Else existing socket is sending a message
            else:

            # Receive message
                message = receive_message(notified_socket)

            # If False, client disconnected, cleanup
                if message is False:
                    print('Closed connection from: {}'.format(clients[notified_socket]['data'].decode('utf-8')))

                # Remove from list for socket.socket()
                    sockets_list.remove(notified_socket)

                # Remove from our list of users
                    del clients[notified_socket]

                    continue

            # Get user by notified socket, so we will know who sent the message
                user = clients[notified_socket]

                print(f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')

            # Iterate over connected clients and broadcast message
                for client_socket in clients:

                # But don't sent it to sender
                    if client_socket != notified_socket:

                    # Send user and message (both with their headers)
                    # We are reusing here message header sent by sender, and saved username header send by user when he connected
                        client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

    # It's not really necessary to have this, but will handle some socket exceptions just in case
        for notified_socket in exception_sockets:

        # Remove from list for socket.socket()
            sockets_list.remove(notified_socket)

        # Remove from our list of users
            del clients[notified_socket]

            print(client_name_list[0])

except KeyboardInterrupt:
    server_socket.close()
