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
    # return the frame
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
    frame = np.load(BytesIO(image))['frame']
    # Convert it from BGR to RGB
    frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # return the frame
    return frame

# shares the screen to the user
def share_screen(conn:socket.socket):
    # send data to client indefinitely
    while True:
        # capture the frame
        frame = get_frame()
        # convert the frame to bytes
        data:bytes = frameToString(frame)
        # send the frame as to the client
        conn.send(data)
        # wait for 0.01s to send the next frame
        time.sleep(0.01)

    
# displays the screen to user
def display_screen(socket:socket.socket, window:str):
    # create a named window
    cv2.namedWindow(window, cv2.WINDOW_NORMAL)
    # cv2.resizeWindow(window, 480, 270)
    # displays the screen
    display = True
    # receive data from server indefinitely
    while display:
        # receive the data from server
        data:bytes = socket.recv(CHUNK_SIZE)
        try:
            # try to parse the image
            cv2.imshow(window, parse_frame(data))
            if (cv2.waitKey(0) == 27):
                # terminate the process
                display = False
        except Exception as e:
            # do nothing if receieved an invalid data
            print(e)
            pass
        finally:
            # close the connection once done!
            socket.close()

        # # decode the data
        # if (decode(data_bytes) == 'FRAME START'):
        #     # receive the chunks of the frame
        #     chunks = []
        #     while True:
        #         # get the data
        #         chunk = socket.recv(CHUNK_SIZE)
        #         # decode the data
        #         if decode(chunk) == 'FRAME END':
        #             # received all the thunks from the server
        #             break
        #         else:
        #             # add the chunk to list of chunks
        #             chunks.append(chunk)
        #     # join chunks to form image
        #     print('received {} chunks'.format(len(chunks)))
        #     img = b''.join(chunks)
        #     # display the image
        #     try:
        #         # try to parse the image
        #         cv2.imshow(window, parse_frame(img))
        #         if (cv2.waitKey(0) == 27):
        #             # terminate the process
        #             display = False
        #     except Exception as e:
        #         # do nothing if receieved an invalid data
        #         print(e)
        #         pass
        #     finally:
        #         # close the connection once done!
        #         socket.close()
    # destory all windows
    cv2.destroyAllWindows()
