import threading
import time
import tkinter as tk
from typing import Iterable
import paho.mqtt.subscribe as subscribe
from config_parser import load_config_yaml

class WindowedDisplay:
    """Displays values for a given set of fields as a simple GUI window. Use .show() to display the window; use .update() to update the values displayed.
    """

    DISPLAY_INIT = '– – –'
    SEP = ':'  # field name separator

    def __init__(self, title: str, display_fields: Iterable[str]):
        """Creates a Windowed (tkinter) display to replace sense_hat display. To show the display (blocking) call .show() on the returned object.

        Parameters
        ----------
        title : str
            The title of the window (usually the name of your carpark from the config)
        display_fields : Iterable
            An iterable (usually a list) of field names for the UI. Updates to values must be presented in a dictionary with these values as keys.
        """
        self.window = tk.Tk()
        self.window.title(f'{title}: Parking')
        self.window.geometry('600x250')
        self.window.resizable(False, False)
        self.display_fields = display_fields

        self.gui_elements = {}
        for i, field in enumerate(self.display_fields):

            # create the elements
            self.gui_elements[f'lbl_field_{i}'] = tk.Label(
                self.window, text=field+self.SEP, font=('Arial', 50))
            self.gui_elements[f'lbl_value_{i}'] = tk.Label(
                self.window, text=self.DISPLAY_INIT, font=('Arial', 50))

            # position the elements
            self.gui_elements[f'lbl_field_{i}'].grid(
                row=i, column=0, sticky=tk.E, padx=5, pady=5)
            self.gui_elements[f'lbl_value_{i}'].grid(
                row=i, column=2, sticky=tk.W, padx=10)

    def show(self):
        """Display the GUI. Blocking call."""
        self.window.mainloop()

    def update(self, updated_values: dict):
        """Update the values displayed in the GUI. Expects a dictionary with keys matching the field names passed to the constructor."""
        for field in self.gui_elements:
            if field.startswith('lbl_field'):
                field_value = field.replace('field', 'value')
                self.gui_elements[field_value].configure(
                    text=updated_values[self.gui_elements[field].cget('text').rstrip(self.SEP)])
        self.window.update()


class CarParkDisplay():
    """Provides a simple display of the car park status. This is a skeleton only. 
    The class is designed to be customizable without requiring and understanding of tkinter or threading."""
    # determines what fields appear in the UI
    fields = ['Available bays', 'Temperature', 'At']

    def __init__(self):
        self.weather = ""
        self.available_bay = ""
        self.config = load_config_yaml("s20111176/mqtt_config.yaml")
        self.window = WindowedDisplay(
            'Moondalup', CarParkDisplay.fields)
        updater = threading.Thread(target=self.check_updates)
        updater.daemon = True
        updater.start()
        self.window.show()\
    
    def check_updates(self):
        # TODO: This is where you should manage the MQTT subscription
        
        while True:
            self.mqtt()
            self.available_bay = self.available_bay + " "
            # NOTE: Dictionary keys *must* be the same as the class fields
            field_values = dict(zip(CarParkDisplay.fields, [
                f'{(self.available_bay)}',
                f'{self.weather}',
                time.strftime("%H:%M:%S")]))
            # Pretending to wait on updates from MQTT
            # time.sleep(1)
            # When you get an update, refresh the display.
            self.window.update(field_values)


    def mqtt(self):        
        msg = subscribe.simple(self.config['mqtt']['publish'], hostname=self.config['mqtt']['host'], port=self.config['mqtt']['port'])
        detection = msg.payload.decode()
        split = detection.split('|')
        


        if "in " in detection:
            print("Incoming car detected!")
            self.weather = split[7][1:]
            self.available_bay = split[1].strip()
            # TODO: Handle incoming car detection, update display accordingly
        elif "out" in detection:
            print("Outgoing car detected!")
            self.weather = split[7][1:]
            self.available_bay = split[1].strip()


if __name__ == '__main__':
    # TODO: Run each of these classes in a separate terminal. You should see the CarParkDisplay update when you click the buttons in the CarDetector.
    # These classes are not designed to be used in the same module - they are both blocking. If you uncomment one, comment-out the other.

    CarParkDisplay()
