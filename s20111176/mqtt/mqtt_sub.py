import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import paho.mqtt.client as paho
from paho.mqtt.client import MQTTMessage
import yaml

with open('s20111176/mqtt/mqtt_config.yaml', 'r') as file:
    config: dict = yaml.safe_load(file)
mqtt_config =  dict(config)


BROKER, PORT = mqtt_config['mqtt']['host'], mqtt_config['mqtt']['port']

def on_message(client, userdata, msg):
    print(f'{msg.payload.decode()}')


client = paho.Client()
client.on_message = on_message
client.connect(BROKER, PORT)
client.subscribe(['mqtt']['subscribe'])
client.loop_forever()
