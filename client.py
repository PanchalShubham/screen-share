# imports
import socket

# Implements the utilities for the client
class Client:
    
    # constructor
    def __init__(self, host='127.0.0.1', port=4040):
        # initialize the properties
        self.__host = host
        self.__port = port
        self.__socket = None

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


    # sends the given message to server
    def send(self, msg:str):
        # send message to server
        self.__socket.sendto(msg.encode('utf-8'), self.__server)
        # wait for server's response
        data, addr = self.__socket.recvfrom(1024)
        print(data.decode('utf-8'))
        

    # closes the socket 
    def close(self):
        # close the connection to the socket connection
        self.__socket.close()



client = Client()
if(client.connect()):
    client.send('Hello server!')
    client.close()