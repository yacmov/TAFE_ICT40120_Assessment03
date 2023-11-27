import random
import platform
import time
from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
from config_parser import load_config_yaml
from weather_generator import weather
from datetime import datetime
from plate_generator import plate_generator
import subprocess
from car_park import car_park



class car_park_management():

    def __init__(self, config_yaml):
        ## Setup config

        msgbox.showinfo("Info", "This program made by Mac, \n if test on windows need to run\n*Broker, \n*car_park_display.py")
        self.update_random_plate_id = None
        self.update_car_in_id = None 
        self.update_car_out_id = None
        self.weather_icon = None
        self.weather_temp = None
        self.config_yaml = config_yaml
        self.config_setup()
        self.cp = car_park(self.max_car_bay)
        self.load_ui()
        self.cp.load_log_when_start()
        self.update_list_view()
        self.update(self.cp)
        self.root.mainloop()


        ## GUI SENSOR 
    def incoming_car(self, weather, temp):
        new_car = self.cp.car_in(self.publisher_frame_entry.get(), weather, temp)
        if new_car == None: return
        self.update_list_view()
        self.update(self.cp)

    def inincoming_car(self):
        self.incoming_car(self.weather_icon, self.weather_temp)
        
        
    def outgoing_car(self, weather, temp):
        selected_car = self.cp.car_out(self.publisher_frame_entry.get(), weather, temp)
        if selected_car == None: return
        self.update_list_view()
        self.update(self.cp)

    def outoutgoing_car(self):
        self.outgoing_car(self.weather_icon, self.weather_temp)
        
    def outgoing_car_random(self, weather, temp):
        if self.list_file.size() <= 0: return
        self.publisher_frame_entry.delete(0, END)
        self.list_file.select_set(random.randint(0, self.list_file.size() -1))
        selected_index = self.list_file.curselection()
        if not selected_index:
            return
        selected_item = self.list_file.get(selected_index)
        plate_number_start = selected_item.find("Plate Number:") + len("Plate Number:")
        plate_number_end = selected_item.find("\t", plate_number_start)
        plate_number = selected_item[plate_number_start:plate_number_end].strip()
        self.publisher_frame_entry.insert(END, plate_number)
        selected_car = self.cp.car_out(self.publisher_frame_entry.get(), weather, temp)
        if selected_car == None: return
        self.update_list_view()
        self.update(self.cp)

    def update(self, car_park):
        current_parking = car_park.get_current_parking()
        self.update_label_current_number(current_parking)
        self.update_progressbar(current_parking)
        self.list_show_last_item()

    def update_progressbar(self, current_parking):
        self.p_var.set(current_parking)
        self.progressbar.update()

    def update_label_current_number(self, current_parking):
        self.capacity_sub_frame_label_current.config(text=f"{current_parking:0>3}")

    def update_list_view(self):
        if self.list_file.size() > 0:
            self.list_file.delete(0, END)

        for car in enumerate(self.cp.all_cars):
            msg = f" Car in time: {str(self.cp.all_cars[car[0]].car_in_time)[11:-7]}\t |  Plate Number: {self.cp.all_cars[car[0]].plate_number: <11}\t |  Parked : {self.cp.all_cars[car[0]].car_parked}"
            self.list_file.insert(END, msg)
            
        # msg = f" Car in time: {str(car.car_in_time)[11:-7]}\t |  Plate Number: {car.plate_number}\t |  Parked : {car.car_parked}"
        # self.list_file.insert(END, msg)


    def update_listbox_select(self, event):
        self.publisher_frame_entry.delete(0, END)
        selected_index = self.list_file.curselection()
        if not selected_index:
            return
        selected_item = self.list_file.get(selected_index)

        plate_number_start = selected_item.find("Plate Number:") + len("Plate Number:")
        plate_number_end = selected_item.find("\t", plate_number_start)
        plate_number = selected_item[plate_number_start:plate_number_end].strip()

        self.publisher_frame_entry.insert(END, plate_number)


    # update random weather
    def update_random_weather(self):
        self.weather_icon, self.weather_temp = weather(self.config_yaml).generate()
        self.weather_sub_frame_label_temp_current.config(text=self.weather_temp)
        self.weather_sub_frame_label_temp_weather.config(text=self.weather_icon)
        self.root.after(1000, self.update_random_weather)


    # update parking labels
    def update_parking_labels(self):
        self.capacity_sub_frame_label_current.config(text=f"{self.cp.get_current_parking():0>3}")
        self.capacity_sub_frame_label_que.config(text=f"[{self.cp.get_waiting_number_of_cars():0>2}]")
        self.root.after(500, self.update_parking_labels)


    # update time
    def update_current_time(self):
        self.current_time = datetime.now().time()
        self.formatted_time = self.current_time.strftime(self.time_format)
        self.time_frame_label.config(text=self.formatted_time)
        self.root.after(1000, self.update_current_time)
        
    # update Scroll to the last item
    def list_show_last_item(self):
        self.list_file.yview_moveto(1.0)


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
                msgbox.showinfo("Info", "This program made by Mac, \n if test on windows need to run\n*Broker, \n*car_park_display.py")
                # subprocess.run(['cmd', '/c', 'start /min "" "cd %programdata%\\Laragon\\bin\\mosquito\\mosquitto –v"'])
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
                msgbox.showinfo("Info", "This program made by Mac, \n if test on windows need to run\n*Broker, \n*car_park_display.py")
                # subprocess.run(['cmd', '/c', f'python {self.current_directory}\\s20111176\\mqtt_sub.py'])
            elif self.os_name == "Darwin":
                subprocess.run(['osascript', '-e', f'tell application "Terminal" to do script "cd {self.current_directory}; python3 s20111176/mqtt_sub.py;"'])

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
                msgbox.showinfo("Info", "This program made by Mac, \n if test on windows need to run\n*Broker, \n*car_park_display.py")
                subprocess.run(['cmd', '/c', f'python {self.current_directory}\\s20111176\\car_park_display.py'])
            elif self.os_name == "Darwin":
                subprocess.run(['osascript', '-e', f'tell application "Terminal" to do script "cd {self.current_directory}; python3 s20111176/car_park_display.py;"'])




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



    # auto number generator 
    def update_start_random_plate(self):
        self.new_plate_number = plate_generator().random_car_plate_number()
        self.publisher_frame_entry.delete(0, END)
        self.publisher_frame_entry.insert(0, self.new_plate_number)
        self.update_random_plate_id = self.root.after(50, self.update_start_random_plate)

    def update_stop_random_plate(self):
        if self.update_random_plate_id is not None:
            self.publisher_frame_entry.delete(0, END)
            self.root.after_cancel(self.update_random_plate_id)
            self.update_random_plate_id = None

    # auto car in 
    def update_start_car_in(self):
        self.publisher_frame_button_car_in.config(state=DISABLED)
        self.incoming_car(self.weather_icon, self.weather_temp)
        self.update_car_in_id = self.root.after(1000, self.update_start_car_in)

    def update_stop_car_in(self):
        # if self.update_car_in_id != None:
        self.publisher_frame_button_car_in.config(state=ACTIVE)
        self.root.after_cancel(self.update_car_in_id)
        self.update_car_in_id = None
        
    # auto car out 
    def update_start_car_out(self):
        self.outgoing_car_random(self.weather_icon, self.weather_temp)
        self.publisher_frame_button_car_out.config(state=DISABLED)
        self.update_car_out_id = self.root.after(1000, self.update_start_car_out)
        

    def update_stop_car_out(self):
        # if self.update_car_out_id != None:
        self.publisher_frame_button_car_out.config(state=ACTIVE)
        self.root.after_cancel(self.update_car_out_id)
        self.update_car_out_id = None


    ## GUI LOAD
    def load_ui(self):
        ## Setup Tkinter
        self.root = Tk()
        self.root.title(self.config['app_info']['title'])
        self.root.resizable(False, False)

        ## Title Label
        self.title_frame = Frame(self.root)
        self.title_frame.pack(side='top')
        self.title_label = Label(text=self.title_text, pady=10, font=self.title_font)
        self.title_label.pack(fill='x', expand=True)

        ## middle frame
        self.middle_frame = LabelFrame(self.root)
        self.middle_frame.pack(side='top')

        ## Display left View
        self.left_view_frame = Frame(self.middle_frame)
        self.left_view_frame.pack(side='left', fill='both', expand=True)

        ## Display right View
        self.right_view_frame = Frame(self.middle_frame)
        self.right_view_frame.pack(side='left')

        ## Display information
        self.display_frame = Frame(self.left_view_frame)
        self.display_frame.pack(side='top', fill='both')

        ### Display Sub frame for capacity
        self.capacity_sub_frame = LabelFrame(self.display_frame)
        self.capacity_sub_frame.pack(side='left', fill='both', expand=True)
        self.capacity_sub_frame_label_parking_icon = Label(self.capacity_sub_frame, text=self.parking_icon, font=self.display_font)
        self.capacity_sub_frame_label_parking_icon.pack(side='left')
        self.capacity_sub_frame_label_current = Label(self.capacity_sub_frame, text=f"{self.cp.get_current_parking():0>3}", font=self.display_font)
        self.capacity_sub_frame_label_current.pack(side='left')
        self.capacity_sub_frame_label_max_parking_lot = Label(self.capacity_sub_frame, text=f" / {self.max_car_bay:0>3} ", font=self.display_font)
        self.capacity_sub_frame_label_max_parking_lot.pack(side='left')
        self.capacity_sub_frame_label_que = Label(self.capacity_sub_frame, text=f"[{self.cp.get_waiting_number_of_cars():0>2}]", font=self.display_font)
        self.capacity_sub_frame_label_que.pack(side='left')
        self.update_parking_labels()

        
        ### Display Sub frame for weather
        self.weather_sub_frame = LabelFrame(self.display_frame)
        self.weather_sub_frame.pack(side='left', fill='both')
        self.weather_sub_frame_label_temp_weather = Label(self.weather_sub_frame, text="☀️ ", font=self.weather_font)
        self.weather_sub_frame_label_temp_weather.pack(side="left") 
        self.weather_sub_frame_label_temp_current = Label(self.weather_sub_frame, text="28", font=self.weather_font)
        self.weather_sub_frame_label_temp_current.pack(side="left")
        self.weather_sub_frame_label_temp_celsius = Label(self.weather_sub_frame, text="°C ", font=self.weather_font)
        self.weather_sub_frame_label_temp_celsius.pack(side="left") 
        self.update_random_weather() 


        ## Progress Bar
        self.p_var = DoubleVar()
        self.progressbar = ttk.Progressbar(self.left_view_frame, maximum=self.max_car_bay, variable=self.p_var)
        self.progressbar.pack(side='top', fill='both')
        self.p_var.set(self.cp.get_current_parking)
        self.progressbar.update()


        ## ListBox
        self.list_frame = Frame(self.left_view_frame)
        self.list_frame.pack(side="top", fill='both')
        self.scrollbar = Scrollbar(self.list_frame)
        self.scrollbar.pack(side='right', fill='y')
        self.list_file = Listbox(self.list_frame, selectmode=SINGLE, height=self.listbox_height, width = 50, yscrollcommand=self.scrollbar.set)
        self.list_file.pack(side='left', fill='both', expand=True)
        self.list_file.bind("<<ListboxSelect>>", self.update_listbox_select)
        self.scrollbar.config(command=self.list_file.yview)

        ## real time
        self.current_time = datetime.now().time()   
        self.formatted_time = self.current_time.strftime(self.time_format)
        self.time_frame = LabelFrame(self.right_view_frame, text="CURRENT TIME")
        self.time_frame.pack(side='top', pady=10, fill = 'both')
        self.time_frame_label = Label(self.time_frame, text=self.formatted_time, font=self.weather_font)
        self.time_frame_label.pack(fill='both', anchor=CENTER)
        self.update_current_time()
        

        ## Setup option
        self.setup_frame = LabelFrame(self.right_view_frame, text=self.config['setup_option']['frame_text'])
        self.setup_frame.pack(side='top', pady=10, fill='both')
        self.setup_frame_button_MQTT_BROKER = Button(self.setup_frame, height=1, text=self.config['setup_option']['mqtt_broker_off'], command=self.mqtt_broker_on_off)
        self.setup_frame_button_MQTT_BROKER.pack(fill=BOTH, anchor=CENTER)
        self.setup_frame_button_MQTT_SUB = Button(self.setup_frame, height=1, text=self.config['setup_option']['mqtt_sub_off'], command=self.mqtt_sub_on_off)
        self.setup_frame_button_MQTT_SUB.pack(fill=BOTH, anchor=CENTER)
        self.setup_frame_button_customer_ui = Button(self.setup_frame, height=1, text=self.config['setup_option']['customer_ui_off'], command=self.customer_ui_on_off)
        self.setup_frame_button_customer_ui.pack(fill=BOTH, anchor=CENTER)



        ## Publisher
        self.publisher_frame = LabelFrame(self.right_view_frame, text=self.config['publisher_frame']['frame_text'])
        self.publisher_frame.pack(side='top', pady=10, fill='both')
        self.publisher_frame_label_plate_number = Label(self.publisher_frame, text="PLATE NUMBER")
        self.publisher_frame_label_plate_number.pack()
        self.publisher_frame_entry = Entry(self.publisher_frame)
        self.publisher_frame_entry.pack()
        self.publisher_frame_button_car_in = Button(self.publisher_frame, state=self.config['publisher_frame']['button_state_default'], height=2, text=self.config['publisher_frame']['incoming_car'], cursor="right_side", command=self.inincoming_car)
        self.publisher_frame_button_car_in.pack(fill=BOTH, anchor=CENTER)
        self.publisher_frame_button_car_out = Button(self.publisher_frame, state=self.config['publisher_frame']['button_state_default'], height=2, text=self.config['publisher_frame']['outgoing_car'], cursor="bottom_left_corner", command=self.outoutgoing_car)
        self.publisher_frame_button_car_out.pack(fill=BOTH, anchor=CENTER)

        ## Auto Mode
        self.auto_frame = LabelFrame(self.right_view_frame, text=self.config['auto_mode']['frame_text'])
        self.auto_frame.pack(side='top', pady=10, fill='both')
        self.auto_frame_button_generate_car_plate_number = Button(self.auto_frame, state=self.config['auto_mode']['button_state_default'], text=self.config['auto_mode']['off_plate_number'], command=self.auto_plate_number)
        self.auto_frame_button_generate_car_plate_number.pack(fill=BOTH, anchor=CENTER)
        self.auto_frame_button_car_in = Button(self.auto_frame, state=self.config['auto_mode']['button_state_default'], text=self.config['auto_mode']['off_car_in'], command=self.auto_car_in)
        self.auto_frame_button_car_in.pack(fill=BOTH, anchor=CENTER)
        self.auto_frame_button_car_out = Button(self.auto_frame, state=self.config['auto_mode']['button_state_default'], text=self.config['auto_mode']['off_car_out'], command=self.auto_car_out)
        self.auto_frame_button_car_out.pack(fill=BOTH, anchor=CENTER)



        ## Test Mode
        self.test_frame = LabelFrame(self.right_view_frame, text="Cheat Mode")
        self.test_frame.pack(side='top', pady=10, fill='both')
        self.test_frame_button_car_in = Button(self.test_frame, text="Add 50 car objects", command=self.add_car_objects_test)
        self.test_frame_button_car_in.pack(fill=BOTH, anchor=CENTER)
        self.test_frame_button_car_out = Button(self.test_frame, text="Remove all car objects", command=self.remove_car_objects_test)
        self.test_frame_button_car_out.pack(fill=BOTH, anchor=CENTER)

    def add_car_objects_test(self):
        for i in range(50):
            new_car = self.cp.car_in(plate_generator().random_car_plate_number(), self.weather_icon, self.weather_temp)
            if new_car == None: return
            self.update_list_view()
            self.update(self.cp)


    def remove_car_objects_test(self):
        if len(self.cp.all_cars) == 0: return
        for i in range(len(self.cp.all_cars)):
            selected_car = self.cp.car_out(self.cp.all_cars[0].plate_number, self.weather_icon, self.weather_temp)
            if selected_car == None: return
            self.update_list_view()
            self.update(self.cp)

        

    def config_setup(self):
        self.config = load_config_yaml(self.config_yaml)
        self.os_name = platform.system()

        self.time_format = "%H:%M:%S"
        self.title_text = self.config['title_frame']['title_label']
        self.title_font = self.config['title_frame']['title_font'],self.config['title_frame']['title_font_size']

        self.display_font = self.config['display_frame']['display_font'],self.config['display_frame']['display_font_size']
        self.parking_icon = self.config['display_frame']['current_bays_icon']
        self.max_car_bay = self.config['display_frame']['display_max_bay']

        self.weather_font = self.config['weather']['font'],self.config['weather']['font_size']

        self.listbox_height = self.config['list_box']['height']


if __name__ == "__main__":
    car_park_management("s20111176/app_config.yaml")