import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import paho.mqtt.client as paho
from paho.mqtt.client import MQTTMessage


BROKER, PORT = "localhost", 1883

def on_message(client, userdata, msg):
    print(f'{msg.payload.decode()}')


client = paho.Client()
client.on_message = on_message
client.connect(BROKER, PORT)
client.subscribe("lot/sensor")
client.loop_forever()
