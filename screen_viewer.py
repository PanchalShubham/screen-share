# imports
from tkinter.constants import BOTH, YES
import numpy as np
import tkinter as tk
from tkinter import Event
from util import get_frame, parse_frame
from PIL import Image, ImageTk
import time
import threading 

class ScreenViewer:
    # constructor
    def __init__(self, title:str):
        self.__window = tk.Tk()
        self.__window.title(title)
        self.__window.geometry('600x500')
        self.__image = None
        self.__image_panel = None        

    # performs the cleanup task when window is closed
    def __on_closing(self):
        """Cleanup when window is closed"""
        exit(0)
        
    
    # captures the key-press event
    def __on_key_press(self, event:Event):
        """Captures the key press event and take appropriate action"""
        if event.keycode  == 95:
            # for F11 - full screen mode
            old_status = self.__window.attributes('-fullscreen')
            self.__window.attributes('-fullscreen', not old_status)
        if event.char:
            # transmit the event
            print(event.char)

    # loads the display screen with defualt background    
    def init_display(self):
        """Loads the display screen with default background"""
        self.__image = Image.open('./images/background.jpg')
        imgComp = ImageTk.PhotoImage(self.__image)
        self.__image_panel = tk.Label(self.__window, image=imgComp)
        self.__image_panel.pack(fill=BOTH, expand=YES)
        self.__image_panel.bind('<Configure>', self.__resize_image)
        self.__window.bind('<KeyPress>', self.__on_key_press)
        self.__window.protocol('WM_DELETE_WINDOW', self.__on_closing)
        self.__window.mainloop()
        
    # displays a specific image to the screen
    def __resize_image(self, event):
        """Resizes the image when window is resized"""
        new_width = event.width
        new_height = event.height
        image = self.__image.copy().resize((new_width, new_height))
        imageComp = ImageTk.PhotoImage(image)
        self.__image_panel.configure(image=imageComp)
        self.__window.mainloop()


    # displays the image on the window
    def __display_image(self):
        """Displays a specific image to the screen"""
        imageComp = ImageTk.PhotoImage(self.__image)
        self.__image_panel.configure(image=imageComp)
        self.__window.mainloop()
        


    # displays the image on the window
    def display_image(self, imgArr:np.ndarray):
        """Displays a specific image to the screen"""
        self.__image = Image.fromarray(imgArr)
        self.__window.after(0, self.__display_image)        





        
        
        
def present_screen(screen:ScreenViewer):
    time.sleep(2)
    while True:
        screen.display_image(parse_frame(get_frame()))
        time.sleep(1)

screen = ScreenViewer('screen-share')
thread = threading.Thread(target=present_screen, args=(screen, ))
thread.setDaemon(True)
thread.start()
screen.init_display()    
