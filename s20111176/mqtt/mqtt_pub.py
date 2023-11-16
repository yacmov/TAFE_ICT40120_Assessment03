import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import paho.mqtt.client as paho
import yaml


class mqtt_broker():
    
    def mqtt_broker(msg):
        BROKER, PORT = "localhost", 1883
        client = paho.Client()
        client.connect(BROKER, PORT)
        client.publish("lot/sensor", msg)
        
    def load_config_yaml(self):
        with open('s20111176/mqtt/mqtt_config.yaml', 'r') as file:
            config: dict = yaml.safe_load(file)
        return config

