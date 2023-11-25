import paho.mqtt.client as paho
from config_parser import load_config_yaml

mqtt_config = load_config_yaml('s20111176/mqtt_config.yaml')

class mqtt_broker():
    
    def mqtt_broker(msg):
        BROKER, PORT = mqtt_config['mqtt']['host'], mqtt_config['mqtt']['port']
        client = paho.Client()
        client.connect(BROKER, PORT)
        client.publish(mqtt_config['mqtt']['publish'], msg)
        return msg

if __name__ == '__main__':
    print(mqtt_config['mqtt']['port'])
    
