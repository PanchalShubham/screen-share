# imports
import socket
from util import random_key, share_screen
import threading
from util import decode

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
        # keeps track of the thread running
        self.__clients = set()
             
    # getter for socket
    def get_socket(self):
        # return the instance of the socket
        return self.__socket
    
    # returns true if the given client has access
    def has_access(self, addr):
        # a client has access if it is in client list
        return addr in self.__clients

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
        # check if client is already getting access
        if addr in self.__clients:
            print('Client addr={} is already connected.'.format(addr))
            # do not allow multiple connections
            return
        # add the client to set of clients
        self.__clients.add(addr)
        # create a new thread to share screen with this client
        thread = threading.Thread(target=share_screen, args=(self, addr))
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
            # decode the message
            msg = decode(data)
            # check if it is a quit
            if msg == 'QUIT':
                # client with address `addr` quit the connection
                self.remove_client(addr)
                # continue to next iteration
                continue
            # check if the client
            # decode the data and verify
            print('Received connection={}. Verifying key...'.format(addr))
            key = msg
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
            

    # removes the client
    def remove_client(self, addr):
        # check if client exist
        if addr in self.__clients:
            # remove the client from list of clients
            self.__clients.remove(addr)
            # notify the user
            print('Client addr={} closed connection'.format(addr))
            