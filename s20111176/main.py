import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from tkinter import *
import tkinter.ttk as ttk
import threading
from s20111176 import *
from datetime import datetime
import subprocess
from samples_and_snippets import simple_mqtt_pub

class main_frame():

    def __init__(self):
        self.current_parking = 0

        # Setup Tkinter
        self.root = Tk()
        self.root.title("Smart car park")
        self.root.resizable(False, False)


        # Title Label
        self.title_frame = Frame(self.root)
        self.title_frame.pack(side="top")
        self.title_label = Label(text="❇ SMART CAR PARK ❇", font=("Arial", 50))
        self.title_label.pack(fill="x", expand=True)
        self.title_label_newline = Label(text="   ", font=("Arial", 15))
        self.title_label_newline.pack(fill="x", expand=True)

        # Middle frame
        self.middle_frame = LabelFrame(self.root)
        self.middle_frame.pack(side="top")

        # Display left view
        self.left_view_frame = Frame(self.middle_frame)
        self.left_view_frame.pack(side="left", fill="both", expand=True, )

        # Display right view
        self.right_view_frame = Frame(self.middle_frame)
        self.right_view_frame.pack(side="left")

        # Status view
        self.status_view_frame = Frame(self.root)
        self.status_view_frame.pack(side="top")
        self.status_view_frame_label = Label(self.status_view_frame, text="status comment")
        self.status_view_frame_label.pack(side="bottom")

        # Display information
        self.display_frame = Frame(self.left_view_frame)
        self.display_frame.pack(side="top", fill="both")

        # Display sub frame for capacity
        self.capacity_sub_frame = LabelFrame(self.display_frame)
        self.capacity_sub_frame.pack(side="left", fill="both", expand=True)
        self.capacity_sub_frame_label_current_bays = Label(self.capacity_sub_frame, text=" 🅿️ : ", font=("Arial", 40))
        self.capacity_sub_frame_label_current_bays.pack(side="left")
        self.capacity_sub_frame_label_current = Label(self.capacity_sub_frame, text=f"{self.current_parking:0>3}", font=("Arial", 50))
        self.capacity_sub_frame_label_current.pack(side="left")
        self.capacity_sub_frame_label_max_self_capacity = Label(self.capacity_sub_frame, text=" / 150 ", font=("Arial", 50))
        self.capacity_sub_frame_label_max_self_capacity.pack(side="left")

        # Display sub frame for weather
        self.weather_sub_frame = LabelFrame(self.display_frame)
        self.weather_sub_frame.pack(side="left", fill="both")
        self.weather_sub_frame_label_image = Label(self.weather_sub_frame, image="")
        self.weather_sub_frame_label_image.pack(side="left")
        self.weather_sub_frame_label_temp_weather = Label(self.weather_sub_frame, text="☀️ ", font=("Arial", 30))
        self.weather_sub_frame_label_temp_weather.pack(side="left") 
        self.weather_sub_frame_label_temp_current = Label(self.weather_sub_frame, text="28", font=("Arial", 30))
        self.weather_sub_frame_label_temp_current.pack(side="left")
        self.weather_sub_frame_label_temp_celsius = Label(self.weather_sub_frame, text="°C ", font=("Arial", 30))
        self.weather_sub_frame_label_temp_celsius.pack(side="left") 

        # Progress Bar 
        self.p_var = DoubleVar()
        self.progressbar = ttk.Progressbar(self.left_view_frame, maximum=150, variable=self.p_var)
        self.progressbar.pack(side="top", fill='both')


        self.p_var.set(self.current_parking)
        self.progressbar.update()



        # ListBox
        self.list_frame = Frame(self.left_view_frame)
        self.list_frame.pack(side="top", fill="both")
        self.scrollbar = Scrollbar(self.list_frame)
        self.scrollbar.pack(side="right", fill="y")
        self.list_file = Listbox(self.list_frame, selectmode="extended", height=15, width=50, yscrollcommand=self.scrollbar.set)
        self.list_file.pack(side="left", fill="both", expand=True)
        self.scrollbar.config(command=self.list_file.yview)




        # Setup option
        self.setup_frame = LabelFrame(self.right_view_frame, text="SETUP")
        self.setup_frame.pack(side='top', pady=10, fill='both')
        self.setup_frame_button_MQTT_BROKER = Button(self.setup_frame, text="🔴 MQTT BROKER OFF", command=self.mqtt_broker_on_off)
        self.setup_frame_button_MQTT_BROKER.pack(fill=BOTH, anchor=CENTER)
        self.setup_frame_button_MQTT_SUB = Button(self.setup_frame, text="🔴 MQTT SUB OFF", command=self.mqtt_sub_on_off)
        self.setup_frame_button_MQTT_SUB.pack(fill=BOTH, anchor=CENTER)

        # Publisher
        self.publisher_frame = LabelFrame(self.right_view_frame, text="PUBLISHER")
        self.publisher_frame.pack(side='top', pady=10, fill='both')
        self.publisher_frame_label_plate_number = Label(self.publisher_frame, text="PLATE NUMBER")
        self.publisher_frame_label_plate_number.pack()
        self.publisher_frame_entry = Entry(self.publisher_frame)
        self.publisher_frame_entry.pack()
        self.publisher_frame_button_car_in = Button(self.publisher_frame, height=2, text="🚘 Incoming Car", cursor="right_side", command=self.incoming_car)
        self.publisher_frame_button_car_in.pack(fill=BOTH, anchor=CENTER)
        self.publisher_frame_button_car_out = Button(self.publisher_frame, height=2, text="Outgoing Car 🚘", cursor="bottom_left_corner", command=self.outgoing_car)
        self.publisher_frame_button_car_out.pack(fill=BOTH, anchor=CENTER)


        # Test Mode
        self.testmode_frame = LabelFrame(self.right_view_frame, text="TEST MODE")
        self.testmode_frame.pack(side='top', pady=10, fill='both')
        self.testmode_frame_button_on_off = Button(self.testmode_frame, text="🔴 OFF", command=self.testmode_on_off)
        self.testmode_frame_button_on_off.pack(anchor=CENTER, fill=BOTH)

        self.root.mainloop()


    def mqtt_broker_on_off(self):
        self.checkvalue = self.setup_frame_button_MQTT_BROKER.cget("text")
        if (self.checkvalue == "🟢 MQTT BROKER ON "):
            self.setup_frame_button_MQTT_BROKER.config(text="🔴 MQTT BROKER OFF")
            subprocess.run(['osascript', '-e', 'tell application "Terminal" to close first window'])
        else:
            self.setup_frame_button_MQTT_BROKER.config(text="🟢 MQTT BROKER ON ")
            self.current_directory = subprocess.check_output('pwd', shell=True, text=True).strip()
            subprocess.run(['osascript', '-e', 'tell application "Terminal" to do script "/opt/homebrew/opt/mosquitto/sbin/mosquitto -c /opt/homebrew/etc/mosquitto/mosquitto.conf"'])

    def mqtt_sub_on_off(self):
        self.checkvalue =  self.setup_frame_button_MQTT_SUB.cget("text")
        if (self.checkvalue == "🟢 MQTT SUB ON "):
            self.setup_frame_button_MQTT_SUB.config(text="🔴 MQTT SUB OFF")
            subprocess.run(['osascript', '-e', 'tell application "Terminal" to close first window'])
        else:
            self.setup_frame_button_MQTT_SUB.config(text="🟢 MQTT SUB ON ")
            self.current_directory = subprocess.check_output('pwd', shell=True, text=True).strip()
            subprocess.run(['osascript', '-e', f'tell application "Terminal" to do script "python3 {self.current_directory}/samples_and_snippets/simple_mqtt_sub.py"'])


    def incoming_car(self):
    # TODO: implement this method to publish the detection via MQTT
        self.current_time = datetime.now().time()   
        self.formatted_time = self.current_time.strftime("%H:%M:%S")
        self.temp = f"{self.weather_sub_frame_label_temp_weather.cget('text')} {self.weather_sub_frame_label_temp_current.cget('text')} {self.weather_sub_frame_label_temp_celsius.cget('text')}"
        self.get_entry_info = self.publisher_frame_entry.get()
        if len(self.get_entry_info) == 0:
            return
        if len(self.get_entry_info) >= 8:
            self.get_entry_info = self.get_entry_info[:8]
        if len(self.get_entry_info) <= 2:
            self.get_entry_info = self.get_entry_info + "　　　"
        self.incoming_msg = f"  {self.get_entry_info:<10}  \t| {self.formatted_time}\t|  {self.temp}  "

        # publish mqtt
        simple_mqtt_pub.mqtt_broker(f"car in  [{self.current_parking:0>3}/150] : [{self.incoming_msg}]")
        self.current_parking += 1
        print(self.current_parking)
        
        # add to list
        self.list_file.insert(END, self.incoming_msg)
        self.update_progressbar()
        self.update_label_current_number()
    
    def outgoing_car(self):
        # TODO: implement this method to publish the detection via MQTT
        
        # publish mqtt

        self.out_car = self.list_file.curselection()
        if not self.out_car:
            return
        simple_mqtt_pub.mqtt_broker(f"car out [{self.current_parking:0>3}/150] : [{self.list_file.selection_get()}]")
        
        if self.out_car == -1:
            return
        self.list_file.delete(self.out_car)
        if self.current_parking == 0:
            return
        else:
            self.current_parking -= 1
            print(self.current_parking)
        self.update_progressbar()
        self.update_label_current_number()
        

    def testmode_on_off(self):
        self.checkvalue = self.testmode_frame_button_on_off.cget("text")
        if (self.checkvalue == "🟢 ON "):
            self.testmode_frame_button_on_off.config(text="🔴 OFF")
        else:
            self.testmode_frame_button_on_off.config(text="🟢 ON ")

        
    # update to app
    def update_progressbar(self):
        self.p_var.set(self.current_parking)
        self.progressbar.update()

    # update current parking numbrer label
    def update_label_current_number(self):
        self.capacity_sub_frame_label_current.config(text=f"{self.current_parking:0>3}")


if __name__ == "__main__":
    main_frame()