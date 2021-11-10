# imports
import pyautogui
import cv2
import numpy as np
from io import BytesIO
import sys
import zlib
import secrets
import string
import time


# generates a random key of given length
def random_key(length:int):
    # generate a random string of given length
    return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(length))

# inputs a key from the console
def input_key():
    key = input('Enter key: ')
    return key


# Specify resolution
resolution = (1920, 1080)

# Specify video codec
codec = cv2.VideoWriter_fourcc(*"XVID")

# Specify frames rate. We can choose any
# value and experiment with it
fps = 60.0

# # Create an Empty window
# cv2.namedWindow("Live", cv2.WINDOW_NORMAL)

# # Resize this window
# cv2.resizeWindow("Live", 480, 270)



# shares the screen to the user
def share_screen(socket, addr):
    # send data to client indefinitely
    while True:
        # send the data to the client
        socket.sendto('hello world'.encode('utf-8'), addr)
        time.sleep(2)

    
# displays the screen to user
def display_screen(socket):
    # receive data from server indefinitely
    while True:
        # receive the data from server
        data_bytes, _ = socket.recvfrom(65535)
        print(data_bytes)



# captures a screenshot and returns the frame
def get_frame():
    # Take screenshot using PyAutoGUI
    img = pyautogui.screenshot()
    # Convert the screenshot to a numpy array
    frame = np.array(img)
    # Convert it from BGR to RGB
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Convert the screenshot to a numpy array
    frame = np.array(img)
    #  return the frame
    print(type(frame))
    return frame

# converts the frame to string
def frameToString(image:np.ndarray):
    # create an instance of BytesIO
    f = BytesIO()
    # compress using numpy
    np.savez_compressed(f, frame=image)
    # seek to starting position
    f.seek(0)
    # read and return the data
    return f.read()

# parses the compressed data to numpy `ndarray`
def parse_frame(image:bytes):
    # load and return the frame
    return np.load(BytesIO(image))['frame']


# displays the frame
def display_frame(window, frame):
    # parse the frame
    image = parse_frame(frame)
    # display the image
    cv2.imshow(window, image)
