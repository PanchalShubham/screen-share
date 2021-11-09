# displays the screen to user
def display_screen(obj):
    # get the socket instance from the obj
    socket = obj.get_socket()
    # receive data from server as long as we are capturing screen
    while obj.is_capturing_screen():
        data, _ = socket.recvfrom(1024)
        print(data.decode('utf-8'))
