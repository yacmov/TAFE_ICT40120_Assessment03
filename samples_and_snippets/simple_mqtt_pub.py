import paho.mqtt.client as paho
import time



def mqtt_broker(msg):
    BROKER, PORT = "localhost", 1883
    client = paho.Client()
    client.connect(BROKER, PORT)
    client.publish("lot/sensor", msg)

