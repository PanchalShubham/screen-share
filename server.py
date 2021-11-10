# imports
import socket
from util import random_key, share_screen
import threading

# Implements the utilities for the server
class Server:
    
    # constructor
    def __init__(self, host='', port=4000, is_public=False):
        """Constructor: Initalizes the server with given hostname and port"""
        self.__host = host
        self.__port = port
        self.__socket = None
        self.__key = None
        self.__is_public = is_public
             

    # initializes a connection with server
    def connect(self):
        """Initializes the socket instance and binds it
        to given host and port
        @return True when the server is binded otherwise returns False"""
        # initialize the socket instance
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # try bind the socket 
        try:
            # bind the socket
            self.__socket.bind((self.__host, self.__port))
            # notify the user
            print('Server runinng at host=\'{}\' on port={}'.format(self.__host, self.__port))
            # check if server is private
            if not self.__is_public:
                # random key
                self.__key = random_key(10)
                # print the key to console
                print('Use key {} to connect to this server.'.format(self.__key))            
            else:
                # public server
                self.__key = ''
                print('Server is running publicly and can be used to connect without a key.')
            # return true when the server is connected
            return True
        except Exception as e:
            # print the error message
            print('Failed to connect')
            print(str(e))
            # return false when the server is not connected
            return False

    
    # share the screen with this client
    def __share_screen(self, addr):
        # create a new thread to share screen with this client
        thread = threading.Thread(target=share_screen, args=(self.__socket, addr))
        # kill the thread if program terminates
        thread.setDaemon(True)
        # start the thread
        thread.start()
         
         
    # runs the server and wait for the connection
    def run(self):
        # server runs indefinitely
        while True:
            # get the data from the client
            data, addr = self.__socket.recvfrom(1024)            
            # decode the data and verify
            print('Received connection={}. Verifying key...'.format(addr))
            key = data.decode('utf-8')
            # check if server is private and key is mismatch
            if key != self.__key and not self.__is_public:
                # key verification failed so client cannot access
                print('KeyError: Key mismatch for client={}'.format(addr))
                self.__socket.sendto('KeyError'.encode('utf-8'), addr)
            else:
                # let client access the screen
                print('Key matched. Sharing screen with client={}'.format(addr))
                self.__socket.sendto('OK'.encode('utf-8'), addr)
                self.__share_screen(addr)
            
