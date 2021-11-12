# imports
import pyautogui
import cv2
import numpy as np
from io import BytesIO
import sys
import secrets
import string
import time
import json
import socket
from struct import pack, unpack
from PIL import Image
import io

# define the size of the chunk
CHUNK_SIZE = 4096

# generates a random key of given length
def random_key(length:int):
    # generate a random string of given length
    return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(length))

# inputs a key from the console
def input_key():
    key = input('Enter key: ')
    return key


# decodes the given data
def decode(data):
    # try to decode the data
    try:        return data.decode('utf-8')
    except:     return data


# captures a screenshot and returns the frame as bytes
def get_frame():
    # Take screenshot using PyAutoGUI
    img = pyautogui.screenshot()
    # Convert it from BGR to RGB
    img_frame = np.array(cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB))
    # create an instance of BytesIO
    file = BytesIO()
    # compress using numpy
    np.savez_compressed(file, frame=img_frame)
    # seek to starting position
    file.seek(0)
    # read and return the data
    return file.read()




# parses the compressed data to numpy `ndarray`
def parse_frame(data:bytes):
    # create a file instance
    file = BytesIO(data)
    # seek to the beginning
    file.seek(0)
    # load the data
    frame = np.load(file)['frame']
    # convert the frame to image
    # img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # return the image
    return frame





# shares the screen to the user
def share_screen(conn:socket.socket):
    # send data to client indefinitely
    while True:
        # capture the frame
        data:bytes = get_frame()
        # send the frame as to the client
        length = pack('>Q', len(data))
        # first send the length of the data
        conn.sendall(length)
        # send the actual data
        conn.sendall(data)
        # wait for 0.01s to send the next frame
        time.sleep(0.01)

    
# displays the screen to user
def display_screen(socket:socket.socket, window:str):
    # create a named window
    cv2.namedWindow(window, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(window, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.resizeWindow(window, 480, 270)
    cv2.setWindowTitle(window, window)
    # displays the screen
    display = True
    # receive data from server indefinitely
    while display:
        # first receive the length of the data
        data = socket.recv(8)
        (length, ) = unpack('>Q', data)
        # receive the actual data
        data = b''
        while len(data) < length:
            to_read = length - len(data)
            data += socket.recv(4096 if to_read > 4096 else to_read)
        # display the image
        try:
            cv2.setWindowProperty(window, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            cv2.setWindowTitle(window, window)
            cv2.imshow(window, parse_frame(data))
            cv2.waitKey(10)
        except Exception as e:
            # log the error
            print(e)

    # destory all windows
    cv2.destroyAllWindows()
