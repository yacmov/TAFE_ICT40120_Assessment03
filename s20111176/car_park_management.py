import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from datetime import datetime
import random
import platform
from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
import subprocess
from s20111176.car_detector import CarDetector
from s20111176.plate_generator import plate_generator
from tkinter import ttk
from s20111176.config_parser import load_config_yaml

class car_park():

    def __init__(self):
        # Global
        msgbox.showinfo("START", "This Program is made on Mac \nshould be some bugs in windows")
        self.config = load_config_yaml("s20111176/config.yaml")
        self.current_parking = 0
        self.os_name = platform.system()
        self.update_random_plate_id = None
        self.update_car_in_id = None 
        self.update_car_out_id = None
        self.new_plate_number = None
        self.used_plate_numbers = set()
        self.listbox_dict = dict()
        
        # Setup Tkinter
        self.root = Tk()
        self.root.title(self.config['app_info']['title'])
        self.root.resizable(False, False)

        # Title Label
        self.title_frame = Frame(self.root)
        self.title_frame.pack(side="top")
        self.title_label = Label(text=self.config['title_frame']['title_label'], pady=10, font=(self.config['title_frame']['title_font'], self.config['title_frame']['title_font_size']))
        self.title_label.pack(fill="x", expand=True)

        # Middle frame
        self.middle_frame = LabelFrame(self.root)
        self.middle_frame.pack(side="top")

        # Display left view
        self.left_view_frame = Frame(self.middle_frame)
        self.left_view_frame.pack(side="left", fill="both", expand=True)

        # Display right view
        self.right_view_frame = Frame(self.middle_frame)
        self.right_view_frame.pack(side="left")

        # Status view
        self.status_view_frame = Frame(self.root)
        self.status_view_frame.pack(side="top")
        self.status_view_frame_label = Label(self.status_view_frame, text=self.config['status_frame']['message'])
        self.status_view_frame_label.pack(side="bottom")

        # Display information
        self.display_frame = Frame(self.left_view_frame)
        self.display_frame.pack(side="top", fill="both")

        # Display sub frame for capacity
        self.capacity_sub_frame = LabelFrame(self.display_frame)
        self.capacity_sub_frame.pack(side="left", fill="both", expand=True)
        self.capacity_sub_frame_label_current_bays = Label(self.capacity_sub_frame, text=self.config['display_frame']["current_bays_icon"], font=(self.config['display_frame']['display_font'], self.config['display_frame']['display_font_size']))
        self.capacity_sub_frame_label_current_bays.pack(side="left")
        self.capacity_sub_frame_label_current = Label(self.capacity_sub_frame, text=f"{self.current_parking:0>3}", font=(self.config['display_frame']['display_font'], self.config['display_frame']['display_font_size']))
        self.capacity_sub_frame_label_current.pack(side="left")
        self.capacity_sub_frame_label_max_self_capacity = Label(self.capacity_sub_frame, text=f" / {self.config['display_frame']['display_max_bay']} ", font=(self.config['display_frame']['display_font'], self.config['display_frame']['display_font_size']))
        self.capacity_sub_frame_label_max_self_capacity.pack(side="left")

        # Display sub frame for weather
        self.weather_sub_frame = LabelFrame(self.display_frame)
        self.weather_sub_frame.pack(side="left", fill="both")

        self.weather_sub_frame_label_temp_weather = Label(self.weather_sub_frame, text="☀️ ", font=(self.config['weather']['font'],self.config['weather']['font_size']))
        self.weather_sub_frame_label_temp_weather.pack(side="left") 
        self.weather_sub_frame_label_temp_current = Label(self.weather_sub_frame, text="28", font=(self.config['weather']['font'],self.config['weather']['font_size']))
        self.weather_sub_frame_label_temp_current.pack(side="left")
        self.weather_sub_frame_label_temp_celsius = Label(self.weather_sub_frame, text="°C ", font=(self.config['weather']['font'],self.config['weather']['font_size']))
        self.weather_sub_frame_label_temp_celsius.pack(side="left") 
        self.update_random_weather() 

        # Progress Bar 
        self.p_var = DoubleVar()
        self.progressbar = ttk.Progressbar(self.left_view_frame, maximum=self.config['display_frame']['display_max_bay'], variable=self.p_var)
        self.progressbar.pack(side="top", fill='both')
        self.p_var.set(self.current_parking)
        self.progressbar.update()

        # ListBox
        self.list_frame = Frame(self.left_view_frame)
        self.list_frame.pack(side="top", fill="both")
        self.scrollbar = Scrollbar(self.list_frame)
        self.scrollbar.pack(side="right", fill="y")
        self.list_file = Listbox(self.list_frame, selectmode=SINGLE, height=self.config['list_box']['height'], width=50, yscrollcommand=self.scrollbar.set)
        self.list_file.pack(side="left", fill="both", expand=True)
        self.scrollbar.config(command=self.list_file.yview)

        # real time
        self.current_time = datetime.now().time()   
        self.formatted_time = self.current_time.strftime("%H:%M:%S")
        self.time_frame = LabelFrame(self.right_view_frame, text="CURRENT TIME")
        self.time_frame.pack(side='top', pady=10, fill = 'both')
        self.time_frame_label = Label(self.time_frame, text=self.formatted_time, font=(self.config['weather']['font'],self.config['weather']['font_size']))
        self.time_frame_label.pack(fill='both', anchor=CENTER)
        self.update_current_time() 


        # Setup option
        self.setup_frame = LabelFrame(self.right_view_frame, text=self.config['setup_option']['frame_text'])
        self.setup_frame.pack(side='top', pady=10, fill='both')
        self.setup_frame_button_MQTT_BROKER = Button(self.setup_frame, height=1, text=self.config['setup_option']['mqtt_broker_off'], command=self.mqtt_broker_on_off)
        self.setup_frame_button_MQTT_BROKER.pack(fill=BOTH, anchor=CENTER)
        self.setup_frame_button_MQTT_SUB = Button(self.setup_frame, height=1, text=self.config['setup_option']['mqtt_sub_off'], command=self.mqtt_sub_on_off)
        self.setup_frame_button_MQTT_SUB.pack(fill=BOTH, anchor=CENTER)
        self.setup_frame_button_customer_ui = Button(self.setup_frame, height=1, text=self.config['setup_option']['customer_ui_off'], command=self.customer_ui_on_off)
        self.setup_frame_button_customer_ui.pack(fill=BOTH, anchor=CENTER)





        # Publisher
        self.publisher_frame = LabelFrame(self.right_view_frame, text=self.config['publisher_frame']['frame_text'])
        self.publisher_frame.pack(side='top', pady=10, fill='both')
        self.publisher_frame_label_plate_number = Label(self.publisher_frame, text="PLATE NUMBER")
        self.publisher_frame_label_plate_number.pack()
        self.publisher_frame_entry = Entry(self.publisher_frame)
        self.publisher_frame_entry.pack()
        self.publisher_frame_button_car_in = Button(self.publisher_frame, state=self.config['publisher_frame']['button_state_default'], height=2, text=self.config['publisher_frame']['incoming_car'], cursor="right_side", command=self.incoming_car)
        self.publisher_frame_button_car_in.pack(fill=BOTH, anchor=CENTER)
        self.publisher_frame_button_car_out = Button(self.publisher_frame, state=self.config['publisher_frame']['button_state_default'], height=2, text=self.config['publisher_frame']['outgoing_car'], cursor="bottom_left_corner", command=self.outgoing_car)
        self.publisher_frame_button_car_out.pack(fill=BOTH, anchor=CENTER)

        # Auto Mode
        self.auto_frame = LabelFrame(self.right_view_frame, text=self.config['auto_mode']['frame_text'])
        self.auto_frame.pack(side='top', pady=10, fill='both')
        self.auto_frame_button_generate_car_plate_number = Button(self.auto_frame, state=self.config['auto_mode']['button_state_default'], text=self.config['auto_mode']['off_plate_number'], command=self.auto_plate_number)
        self.auto_frame_button_generate_car_plate_number.pack(fill=BOTH, anchor=CENTER)
        self.auto_frame_button_car_in = Button(self.auto_frame, state=self.config['auto_mode']['button_state_default'], text=self.config['auto_mode']['off_car_in'], command=self.auto_car_in)
        self.auto_frame_button_car_in.pack(fill=BOTH, anchor=CENTER)
        self.auto_frame_button_car_out = Button(self.auto_frame, state=self.config['auto_mode']['button_state_default'], text=self.config['auto_mode']['off_car_out'], command=self.auto_car_out)
        self.auto_frame_button_car_out.pack(fill=BOTH, anchor=CENTER)






        self.root.mainloop()


    def auto_plate_number(self):
        self.checkvalue = self.auto_frame_button_generate_car_plate_number.cget("text")
    
        if (self.checkvalue == self.config['auto_mode']['on_plate_number']):
            self.auto_frame_button_generate_car_plate_number.config(text=self.config['auto_mode']['off_plate_number'])
            self.update_stop_random_plate()
        else:
            self.auto_frame_button_generate_car_plate_number.config(text=self.config['auto_mode']['on_plate_number'])
            self.update_start_random_plate()

    def auto_car_in(self):
        self.checkvalue = self.auto_frame_button_car_in.cget("text")
    
        if (self.checkvalue == self.config['auto_mode']['on_car_in']):
            self.auto_frame_button_car_in.config(text=self.config['auto_mode']['off_car_in'])
            self.update_stop_car_in()
        else:
            self.auto_frame_button_car_in.config(text=self.config['auto_mode']['on_car_in'])
            self.update_start_car_in()

    def auto_car_out(self):
        self.checkvalue = self.auto_frame_button_car_out.cget("text")
    
        if (self.checkvalue == self.config['auto_mode']['on_car_out']):
            self.auto_frame_button_car_out.config(text=self.config['auto_mode']['off_car_out'])
            self.update_stop_car_out()
        else:
            self.auto_frame_button_car_out.config(text=self.config['auto_mode']['on_car_out'])
            self.update_start_car_out()



    def mqtt_broker_on_off(self):
        self.checkvalue = self.setup_frame_button_MQTT_BROKER.cget("text")
    
        if (self.checkvalue == self.config['setup_option']['mqtt_broker_on']):
            self.auto_frame_button_generate_car_plate_number.config(state=DISABLED)
            self.auto_frame_button_car_in.config(state=DISABLED)
            self.auto_frame_button_car_out.config(state=DISABLED)
            self.publisher_frame_button_car_in.config(state=DISABLED)
            self.publisher_frame_button_car_out.config(state=DISABLED)

            self.setup_frame_button_MQTT_BROKER.config(text=self.config['setup_option']['mqtt_broker_off'])
            if self.os_name == "Windows":
                subprocess.run(['cmd', '/c', 'exit'])
            elif self.os_name == "Darwin":
                subprocess.run(['osascript', '-e', 'tell application "Terminal" to close first window'])
        else:
            self.setup_frame_button_MQTT_BROKER.config(text=self.config['setup_option']['mqtt_broker_on'])
            self.auto_frame_button_generate_car_plate_number.config(state=ACTIVE)
            self.auto_frame_button_car_in.config(state=ACTIVE)
            self.auto_frame_button_car_out.config(state=ACTIVE)
            self.publisher_frame_button_car_in.config(state=ACTIVE)
            self.publisher_frame_button_car_out.config(state=ACTIVE)
            self.current_directory = subprocess.check_output('pwd', shell=True, text=True).strip()
            if self.os_name == "Windows":
                subprocess.run(['cmd', '/c', 'start /min "" "cd %programdata%\\Laragon\\bin\\mosquito\\mosquitto –v"'])
            elif self.os_name == "Darwin":
                subprocess.run(['osascript', '-e', 'tell application "Terminal" to do script "/opt/homebrew/opt/mosquitto/sbin/mosquitto -c /opt/homebrew/etc/mosquitto/mosquitto.conf"'])

    def mqtt_sub_on_off(self):
        self.checkvalue =  self.setup_frame_button_MQTT_SUB.cget("text")
        if (self.checkvalue == self.config['setup_option']['mqtt_sub_on']):
            self.setup_frame_button_MQTT_SUB.config(text=self.config['setup_option']['mqtt_sub_off'])
            if self.os_name == "Windows":
                subprocess.run(['cmd', '/c', 'taskkill /F /IM cmd.exe'])
            elif self.os_name == "Darwin":
                subprocess.run(['osascript', '-e', 'tell application "Terminal" to close first window'])
        else:
            self.setup_frame_button_MQTT_SUB.config(text=self.config['setup_option']['mqtt_sub_on'])
            self.current_directory = subprocess.check_output('pwd', shell=True, text=True).strip()
            if self.os_name == "Windows":
                subprocess.run(['cmd', '/c', f'python {self.current_directory}\\s20111176\\mqtt_sub.py'])
            elif self.os_name == "Darwin":
                subprocess.run(['osascript', '-e', f'tell application "Terminal" to do script "cd {self.current_directory}; python3 s20111176/mqtt/mqtt_sub.py;"'])

    def customer_ui_on_off(self):
        self.checkvalue =  self.setup_frame_button_customer_ui.cget("text")
        if (self.checkvalue == self.config['setup_option']['customer_ui_on']):
            self.setup_frame_button_customer_ui.config(text=self.config['setup_option']['customer_ui_off'])
            if self.os_name == "Windows":
                subprocess.run(['cmd', '/c', 'taskkill /F /IM cmd.exe'])
            elif self.os_name == "Darwin":
                subprocess.run(['osascript', '-e', 'tell application "Terminal" to close first window'])
        else:
            self.setup_frame_button_customer_ui.config(text=self.config['setup_option']['customer_ui_on'])
            self.current_directory = subprocess.check_output('pwd', shell=True, text=True).strip()
            if self.os_name == "Windows":
                subprocess.run(['cmd', '/c', f'python {self.current_directory}\\s20111176\\car_park_display.py'])
            elif self.os_name == "Darwin":
                subprocess.run(['osascript', '-e', f'tell application "Terminal" to do script "cd {self.current_directory}; python3 s20111176/car_park_display.py;"'])



    def incoming_car(self):
    # TODO: implement this method to publish the detection via MQTT
        # check mqtt_broker and sub on
        broker = self.setup_frame_button_MQTT_BROKER.cget('text')
        subscriber = self.setup_frame_button_MQTT_SUB.cget('text')
        server_check = broker + subscriber
        if "OFF" in server_check:
            msgbox.showinfo("Check Server", "Enable Broker and Subscriber")
            return

        if self.current_parking == self.config['display_frame']['display_max_bay']:
            msgbox.showinfo("FULL", "Car park is FULL\nWAIT UNTIL CAR GOES OUT")
            return

        self.current_time = datetime.now().time()   
        self.formatted_time = self.current_time.strftime("%H:%M:%S")
        self.temp = f"{self.weather_sub_frame_label_temp_weather.cget('text')} {self.weather_sub_frame_label_temp_current.cget('text')} {self.weather_sub_frame_label_temp_celsius.cget('text')}"
        self.get_entry_info = self.publisher_frame_entry.get()
        if len(self.get_entry_info) == 0:
            if self.update_car_in_id is None:
                msgbox.showinfo("Check Plate number", "Enter Plate number")
            return
        if len(self.get_entry_info) >= 8:
            self.get_entry_info = self.get_entry_info[:8]
        if len(self.get_entry_info) <= 2:
            self.get_entry_info = self.get_entry_info + "　　　"

        # Check if the plate number is already used
        if self.get_entry_info in self.used_plate_numbers:
            # msgbox.showinfo("Duplicate Plate Number", "Plate number already used")
            return

        self.used_plate_numbers.add(self.get_entry_info)  # Add the new plate number to the set

        self.listbox_dict.update({self.get_entry_info:{self.config['list_box']['weather']:self.temp, self.config['list_box']['car_in']:self.formatted_time, self.config['list_box']['car_out']:None}})
        # self.incoming_msg = f"  {self.get_entry_info:<8}\t| {self.formatted_time}\t|  {self.temp}  "
        self.incoming_msg = f"  {self.get_entry_info:<8}\t| {self.listbox_dict[self.get_entry_info]['car_in']}\t|  {self.listbox_dict[self.get_entry_info]['weather']}  "

        ## publish mqtt
        cd1 = CarDetector(self.formatted_time, self.current_parking, self.incoming_msg, "1")
        self.current_parking = cd1.incoming_car()
    
         # add to list
        self.list_file.insert(END, self.incoming_msg)
        self.update_progressbar()
        self.update_label_current_number()
        self.list_show_last_item()
        
    def outgoing_car(self):
        # TODO: implement this method to publish the detection via MQTT
        
        # publish mqtt
        if self.current_parking == 0:
            return

        # Random Selection
        if self.update_car_out_id is not None:
            self.list_file.selection_clear(0, END)
            self.list_file.select_set(random.randint(0, self.list_file.size() -1))


        self.out_car = self.list_file.curselection()
        if not self.out_car:
            return
        
        
        # remove selected item from the list
        selected_item = self.list_file.selection_get()
        cd2 = CarDetector(self.formatted_time, self.current_parking, self.incoming_msg, selected_item)
        self.current_parking = cd2.outgoing_car()
        selected_plate_number = selected_item.split("|")[0].strip()
        if selected_plate_number in self.used_plate_numbers:
            self.used_plate_numbers.remove(selected_plate_number)
        
        
        if self.out_car == -1:
            return
        self.list_file.delete(self.out_car)
        if self.current_parking == 0 or self.current_parking == -1:
            self.current_parking = 0
            self.capacity_sub_frame_label_current.config(text="000")
            return
        self.update_progressbar()
        self.update_label_current_number()

        
    # Scroll to the last item
    def list_show_last_item(self):
        self.list_file.yview_moveto(1.0)

    # update to app
    def update_progressbar(self):
        self.p_var.set(self.current_parking)
        self.progressbar.update()

    # update current parking number label
    def update_label_current_number(self):
        self.capacity_sub_frame_label_current.config(text=f"{self.current_parking:0>3}")

    # update random weather
    def update_random_weather(self):
        self.emoji = list(self.config['weather']['weather_list'])
        selected_emoji = self.emoji[random.randint(0, len(self.emoji)-1)]
        self.weather_sub_frame_label_temp_current.config(text=f'{random.randint(1, 45):0>2}')
        self.weather_sub_frame_label_temp_weather.config(text=f"{selected_emoji} ")
        self.root.after(1000, self.update_random_weather)

    # update time
    def update_current_time(self):
        self.current_time = datetime.now().time()
        self.formatted_time = self.current_time.strftime("%H:%M:%S")
        self.time_frame_label.config(text=self.formatted_time)
        self.root.after(1000, self.update_current_time)

    # auto number generator 
    def update_start_random_plate(self):
        self.new_plate_number = plate_generator().random_car_plate_number()
        self.publisher_frame_entry.delete(0, END)
        self.publisher_frame_entry.insert(0, self.new_plate_number)
        self.update_random_plate_id = self.root.after(200, self.update_start_random_plate)

    def update_stop_random_plate(self):
        if self.update_random_plate_id is not None:
            self.publisher_frame_entry.delete(0, END)
            self.root.after_cancel(self.update_random_plate_id)
            self.update_random_plate_id = None

    # auto car in 
    def update_start_car_in(self):
        self.publisher_frame_button_car_in.config(state=DISABLED)
        if self.current_parking < self.config['display_frame']['display_max_bay']:
            self.incoming_car()
        self.update_car_in_id = self.root.after(200, self.update_start_car_in)

    def update_stop_car_in(self):
        if self.update_car_in_id is not None:
            self.publisher_frame_button_car_in.config(state=ACTIVE)
            self.root.after_cancel(self.update_car_in_id)
            self.update_car_in_id = None
        
    # auto car out 
    def update_start_car_out(self):
        self.outgoing_car()
        self.publisher_frame_button_car_out.config(state=DISABLED)
        self.update_car_out_id = self.root.after(200, self.update_start_car_out)

    def update_stop_car_out(self):
        if self.update_car_out_id is not None:
            self.publisher_frame_button_car_out.config(state=ACTIVE)
            self.root.after_cancel(self.update_car_out_id)
            self.update_car_out_id = None

if __name__ == "__main__":
    car_park()