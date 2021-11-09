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
        self.__capturing_screen = False
        
        
    # accessors
    def is_capturing_screen(self):
        # check is screen is being captured
        return self.__capturing_screen
    
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
            # return true when the server is connected
            return True
        except Exception as e:
            # print the error message
            print('Failed to connect')
            print(str(e))
            # return false when the server is not connected
            return False


    # captures the screen of the client
    def capture_server_screen(self):
        # check if screen is already being captured
        if self.__capturing_screen: 
            # inform the client
            print('You are already capturing server\'s screen.')
            # do not proceed further
            return
        # start capturing server screen
        self.__capturing_screen = True
        # create a new thread to capture screen
        thread = threading.Thread(target=display_screen, args=(self,))
        # kill the thread when process terminates
        thread.setDaemon(True)
        # start the thread
        thread.start()
        

    # stops capturing server screen
    def stop_capturing_server_screen(self):
        # stop capturing screen
        self.__capturing_screen = False
        
        
        
        
    # sends the given message to server
    def send(self, msg:str):
        # send message to server
        print('Sending \'{}\' to {}'.format(msg, self.__server))
        # send a message to server
        try:
            # send the message
            self.__socket.sendto(msg.encode('utf-8'), self.__server)
            # return true when the message is sent successfully
            return True
        except Exception as e:
            # notify the user
            print('Failed to send msg=\'{}\' to {}'.format(msg, self.__server))
            print(str(e))
            # return false when message send fails
            return False
    
    # performs a handshake with the client
    def handshake(self):
        # send a message to the server and return status
        return self.send('hello server!')

    # disconnects the communication 
    def disconnect(self):
        # notify the server about the disconnection
        # close the connection to the socket connection
        self.__socket.close()




# host='127.0.0.1'
# server_ip='127.0.0.1'
# server_port=4000

# # host='192.168.137.1'
# # server_ip='192.168.137.246'
# # server_port=4000

# client = Client(host)
# if(client.connect(server_ip, server_port)):
#     if(client.handshake()):
#         client.capture_server_screen()
#         user_inp = ''
#         while user_inp != 'quit':
#             user_inp = input('>> ')
#             print(user_inp)
#             if (user_inp == 'stop capture'):
#                 client.stop_capturing_server_screen()
#             elif (user_inp == 'exit'):
#                 client.stop_capturing_server_screen()
#                 break
#         client.disconnect()
