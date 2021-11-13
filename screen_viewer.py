# imports
from tkinter.constants import BOTH, YES
import numpy as np
import tkinter as tk
from util import get_frame, parse_frame
from PIL import Image, ImageTk
import time
import threading 

class ScreenViewer:
    # constructor
    def __init__(self, title:str):
        self.__window = tk.Tk()
        self.__window.title(title)
        self.__window.geometry('1000x800')
        self.__image = None
        self.__image_panel = None        
     
    # loads the display screen with defualt background    
    def init_display(self):
        """Loads the display screen with default background"""
        self.__image = Image.open('./images/background.jpg')
        imgComp = ImageTk.PhotoImage(self.__image)
        self.__image_panel = tk.Label(self.__window, image=imgComp)
        self.__image_panel.pack(fill=BOTH, expand=YES)
        self.__image_panel.bind('<Configure>', self.__resize_image)
        # self.__window.bind('<<ImageUpdate>>', self.__display_image)
        self.__window.mainloop()
        
    # displays the image on the window
    def __display_image(self, event=None):
        """Displays a specific image to the screen"""
        imageComp = ImageTk.PhotoImage(self.__image)
        self.__image_panel.configure(image=imageComp)
        print(self.__image)
        self.__window.mainloop()
        
    def display_image(self, imgArr:np.ndarray):
        self.__image = Image.fromarray(imgArr)
        self.__window.after(0, self.__display_image)        
        # self.__window.event_generate('<<ImageUpdate>>')

    # displays a specific image to the screen
    def __resize_image(self, event):
        """Resizes the image when window is resized"""
        new_width = event.width
        new_height = event.height
        image = self.__image.copy().resize((new_width, new_height))
        imageComp = ImageTk.PhotoImage(image)
        self.__image_panel.configure(image=imageComp)
        self.__window.mainloop()
        
        
        
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

