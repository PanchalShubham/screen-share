# imports
import pyautogui
import cv2
import numpy as np
from io import BytesIO
import sys
import zlib



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

# displays the screen to user
def display_screen(obj):
    # get the socket instance from the obj
    socket = obj.get_socket()
    # receive data from server as long as we are capturing screen
    while obj.is_capturing_screen():
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
