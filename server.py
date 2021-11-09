# imports
import socket

# Implements the utilities for the server
class Server:
    
    # constructor
    def __init__(self, host='', port=4000):
        """Constructor: Initalizes the server with given hostname and port"""
        self.__host = host
        self.__port = port
        self.__socket = None
        self.__server_running = False
             

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
            # return true when the server is connected
            return True
        except Exception as e:
            # print the error message
            print('Failed to connect')
            print(str(e))
            # return false when the server is not connected
            return False

    
    # send details to the client
    def __client(self, data, addr):
        print('client addr={} sent data={}'.format(addr, data.decode('utf-8')))
        self.__socket.sendto('Hello client'.encode('utf-8'), addr)
         
         
    # runs the server and wait for the connection
    def run(self):
        self.__server_running = True
        while (self.__server_running):
            # get the data from the client
            data, addr = self.__socket.recvfrom(1024)
            # process the client
            self.__client(data, addr)
            
   
# creat
server = Server()
# process if server is connected
if(server.connect()):
    server.run()

