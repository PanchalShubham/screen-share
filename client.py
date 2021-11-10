# imports
import socket
import threading
from util import display_screen

# Implements the utilities for the client
class Client:
    
    # constructor
    def __init__(self, host='127.0.0.1', port=4040):
        # initialize the properties
        self.__host = host
        self.__port = port
        self.__socket = None
        self.__server = None        
        
    # accessor for socket
    def get_socket(self):
        # returns a copy of the socket instance
        return self.__socket

    # connects to the server
    def connect(self, server_ip='127.0.0.1', server_port=4000):
        # store properties of server
        self.__server = (server_ip, server_port)
        # initialize the socket
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # try bind the socket 
        try:
            # bind the socket
            self.__socket.bind((self.__host, self.__port))
            # notify the user
            print('Client runinng at host=\'{}\' on port={}'.format(self.__host, self.__port))
            print('Client connected with server at ip=\'{}\' on port={}'.format(server_ip, server_port))
            # return true when the server is connected
            return True
        except Exception as e:
            # print the error message
            print('Failed to connect')
            print(str(e))
            # return false when the server is not connected
            return False


    # sends key to the server and validate
    def validate_key_and_capture(self, key:str, title:str):
        # send the key to the server
        self.__socket.sendto(key.encode('utf-8'), self.__server)
        # wait for the server to respond
        print('Waiting for server to verify key...')
        data, _ = self.__socket.recvfrom(1024)
        # get server's response
        response = data.decode('utf-8')
        # check if there was any error
        if response != 'OK':
            # inform the user
            print('The key {} is rejected by server.'.format(key))
            # disconnect the connection
            self.disconnect()
            # terminate the application
            exit(0)
        # connection to server succeeded
        print('Connected to server successfully.')
        # decide the title
        title = str(self.__server) if title == '' else title
        # start capturing screen
        self.__capture_server_screen(title)

    # disconnects the communication 
    def disconnect(self):
        # notify the server about the disconnection
        # close the connection to the socket connection
        self.__socket.close()
        
        
    # captures the screen of the client
    def __capture_server_screen(self, title):
        # create a new thread to capture screen
        thread = threading.Thread(target=display_screen, args=(self.__socket, title))
        # kill the thread when process terminates
        thread.setDaemon(True)
        # start the thread
        thread.start()
        # wait for the thread to finish
        thread.join()
