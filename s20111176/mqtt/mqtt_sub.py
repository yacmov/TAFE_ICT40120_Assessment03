import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
# sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
# customer_display = car_park_display("___", "___")
import paho.mqtt.client as paho
from paho.mqtt.client import MQTTMessage
import yaml

with open('s20111176/mqtt/mqtt_config.yaml', 'r') as file:
    config: dict = yaml.safe_load(file)
mqtt_config = dict(config)


BROKER, PORT = mqtt_config['mqtt']['host'], mqtt_config['mqtt']['port']

def on_message(client, userdata, msg):
    # update_car_park_display("test", "TEst")
    print(f'{msg.payload.decode()}')

# def update_car_park_display(available_bay, weather):
#     customer_display.available_bay = available_bay
#     customer_display.weather = weather

print(mqtt_config['mqtt']['host'])

client = paho.Client()
client.on_message = on_message
client.connect(BROKER, PORT)
client.subscribe(mqtt_config['mqtt']['subscribe'])
client.loop_forever()
