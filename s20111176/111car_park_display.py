import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import threading
import time
from datetime import datetime
import tkinter as Tk
from typing import Iterable
from tkinter import *
import tkinter.ttk as ttk
import yaml

class car_park_display():
    def __init__(self, bay, weather):
        # Global
        self.available_bay = bay
        self.weather = weather
        self.config = self.load_config_yaml()
        
        # Setup Tkinter
        self.root = Tk()
        self.root.title(self.config['car_park_display']['title'])
        self.root.geometry('800x400')
        self.root.resizable(False, False)

        # Welcome frame
        self.welcome_frame = Frame(self.root)
        self.welcome_frame.pack(side="top")
        self.welcome_msg = Label(text=self.config['car_park_display']['welcome_msg'], pady=10, font=(self.config['title_frame']['title_font'], self.config['car_park_display']['welcome_font_size']))
        # self.welcome_msg.pack(fill="both", expand=True)

        # Customer info frame
        
        self.customer_info_frame = Frame(self.root)
        self.customer_info_frame.pack(side="top")

        # customer info sub frame
        self.available_bay_frame = Frame(self.customer_info_frame)
        self.available_bay_frame.pack(side='top')
        self.available_bay = Label(self.available_bay_frame, text=f"{self.config['car_park_display']['available_bay']}: {self.available_bay:0>3}", font=(self.config['title_frame']['title_font'], self.config['title_frame']['title_font_size']))
        self.available_bay.pack(side='top', fill="x", expand=True)

        # customer info sub frame 
        self.time_and_weather = Frame(self.customer_info_frame)
        self.time_and_weather.pack(side='bottom', fill='x', expand=True)

        # real time info
        self.current_time = datetime.now().time()   
        self.formatted_time = self.current_time.strftime("%H:%M:%S")
        self.time_frame_label = Label(self.time_and_weather, text=f"time", font=(self.config['weather']['font'], 50))
        self.time_frame_label.pack(side='left')
        self.update_current_time() 
        
        # weather info
        self.weather_and_time = Label(self.time_and_weather, text=f"{self.config['car_park_display']['at']}: {self.weather} ", font=(self.config['title_frame']['title_font'], self.config['title_frame']['title_font_size']))
        self.weather_and_time.pack(side='left')
        

        self.root.mainloop()

    def update_current_time(self):
        self.current_time = datetime.now().time()
        self.formatted_time = self.current_time.strftime("%H:%M:%S")
        self.time_frame_label.config(text=f"⏰ {self.formatted_time}   ")
        self.root.after(1000, self.update_current_time)

    def update_bay_and_weather(self, bay, weather):
        pass

    # load yaml file
    def load_config_yaml(self):
        with open('./s20111176/config.yaml', 'r') as file:
            config: dict = yaml.safe_load(file)
        return config


