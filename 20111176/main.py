import sys
import os
from tkinter import *
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

# Setup Tkinter
root = Tk()
root.title("Smart car park")
root.resizable(False, False)


# Title Label
title_frame = Frame(root)
title_frame.pack(side="top")
title_label = Label(text="SMART CAR PARK", font=("Arial", 50))
title_label.pack(fill="x", expand=True)
title_label_newline = Label(text="   ", font=("Arial", 15))
title_label_newline.pack(fill="x", expand=True)

# Middle frame
middle_frame = LabelFrame(root)
middle_frame.pack(side="top")

# Display left view
left_view_frame = Frame(middle_frame)
left_view_frame.pack(side="left", fill="both", expand=True, )

# Display right view
right_view_frame = Frame(middle_frame)
right_view_frame.pack(side="left")

# Status view
status_view_frame = Frame(root)
status_view_frame.pack(side="top")
status_view_frame_label = Label(status_view_frame, text="status comment")
status_view_frame_label.pack(side="bottom")

# Display information
display_frame = Frame(left_view_frame)
display_frame.pack(side="top", fill="both")

# Display sub frame for capacity
capacity_sub_frame = LabelFrame(display_frame)
capacity_sub_frame.pack(side="left", fill="both", expand=True)
capacity_sub_frame_label_current = Label(capacity_sub_frame, text="39", font=("Arial", 50))
capacity_sub_frame_label_current.pack(side="left")
capacity_sub_frame_label_max_capacity = Label(capacity_sub_frame, text=" / 150", font=("Arial", 50))
capacity_sub_frame_label_max_capacity.pack(side="left")

# Display sub frame for weather
weather_sub_frame = LabelFrame(display_frame)
weather_sub_frame.pack(side="left", fill="both")
weather_sub_frame_label_image = Label(weather_sub_frame, image="")
weather_sub_frame_label_image.pack(side="left")
weather_sub_frame_label_temp_current = Label(weather_sub_frame, text="28", font=("Arial", 30))
weather_sub_frame_label_temp_current.pack(side="left")
weather_sub_frame_label_temp_celsius = Label(weather_sub_frame, text="°C", font=("Arial", 30))
weather_sub_frame_label_temp_celsius.pack(side="left") 



# ListBox
list_frame = Frame(left_view_frame)
list_frame.pack(side="top", fill="both")
scrollbar = Scrollbar(list_frame)
scrollbar.pack(side="right", fill="y")
list_file = Listbox(list_frame, selectmode="extended", height=15, width=50, yscrollcommand=scrollbar.set)
list_file.pack(side="left", fill="both", expand=True)
scrollbar.config(command=list_file.yview)


# Setup option
setup_frame = LabelFrame(right_view_frame, text="SETUP")
setup_frame.pack(fill="both")
setup_frame_button_MQTT_BROKER = Button(setup_frame, text="MQTT BROKER OFF")
setup_frame_button_MQTT_BROKER.pack(fill=BOTH, anchor=CENTER)
setup_frame_button_MQTT_SUB = Button(setup_frame, text="MQTT SUB OFF")
setup_frame_button_MQTT_SUB.pack(fill=BOTH, anchor=CENTER)

# Empty Line insert
emptyline = Frame(right_view_frame)
emptyline.pack()
emptyline_label = Label(emptyline, text="   ")
emptyline_label.pack()

# Publisher
publisher_frame = LabelFrame(right_view_frame, text="PUBLISHER")
publisher_frame.pack(fill="both")
publisher_frame_label_plate_number = Label(publisher_frame, text="PLATE NUMBER")
publisher_frame_label_plate_number.pack()
publisher_frame_entry = Entry(publisher_frame)
publisher_frame_entry.pack()
publisher_frame_button_car_in = Button(publisher_frame, text="CAR IN")
publisher_frame_button_car_in.pack(fill=BOTH, anchor=CENTER)
publisher_frame_button_car_out = Button(publisher_frame, text="CAR OUT")
publisher_frame_button_car_out.pack(fill=BOTH, anchor=CENTER)

# Empty Line2 insert
emptyline2 = Frame(right_view_frame)
emptyline2.pack()
emptyline2_label = Label(emptyline2, text="    ")
emptyline2_label.pack()

# Test Mode
testmode_frame = LabelFrame(right_view_frame, text="TEST MODE")
testmode_frame.pack(fill="both")
testmode_frame_button_on_off = Button(testmode_frame, text="OFF")
testmode_frame_button_on_off.pack(anchor=CENTER, fill=BOTH)





root.mainloop()