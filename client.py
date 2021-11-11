# imports
import socket
import threading
from util import display_screen, input_key, decode
import time

# Implements the utilities for the client
class Client:
    
    # constructor
    def __init__(self, host='127.0.0.1', port=4040, title='screen-share'):
        # initialize the properties
        self.__host = host
        self.__port = port
        self.__socket = None
        self.__server = None
        self.__title = title
        
        
    # accessor for socket
    def get_socket(self):
        # returns a copy of the socket instance
        return self.__socket
    
    # connects to the server
    def connect(self, server_ip='127.0.0.1', server_port=4000):
        # store properties of server
        self.__server = (server_ip, server_port)
        # try bind the socket 
        try:
            # initialize the socket
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # bind the socket
            self.__socket.bind((self.__host, self.__port))
            # notify the user
            print('Client runinng at host=\'{}\' on port={}'.format(self.__host, self.__port))
            # establish a connection with the server
            self.__socket.connect(self.__server)
            # notify the user
            print('Client connected with server at host=\'{}\' on port={}'.format(server_ip, server_port))
            # once the connection is established validate the key
            self.__validate_key()
        except Exception as e:
            # inform the client
            print(str(e))


    # validates the key with the server
    def __validate_key(self):
        # wait for the server to tell its status
        msg = self.__socket.recv(1024).decode('utf-8')
        # check if key is required
        if msg == 'KEY REQUIRED':
            # prompt the user for key
            client_key = input_key()
            # validate key with server
            self.__socket.send(client_key.encode('utf-8'))
            print('Key sent for verification. Waiting for response...')
            # wait for server to respond
            response = self.__socket.recv(1024).decode('utf-8')
            # check server's response
            if response == 'INVALID KEY':
                # notify the user
                print('The key {} is rejected by server.'.format(client_key))
                # close the connection
                self.__socket.close()
                # terminate the program
                exit(0)
        # got access
        print('You have got access to the server')
        # server will repeatedly send the data - capture and display it
        thread = threading.Thread(target=display_screen, args=(self.__socket, self.__title, ))
        # kill the thread when application terminates
        thread.setDaemon(True)
        # start the thread
        thread.start()
        # wait for the thread to finish
        thread.join()

    
    # disconnect the client from the server
    def disconnect(self):
        # close the connection
        self.__socket.close()