import paho.mqtt.client as paho
from config_parser import load_config_yaml

mqtt_config = load_config_yaml('s20111176/mqtt_config.yaml')

BROKER, PORT = mqtt_config['mqtt']['host'], mqtt_config['mqtt']['port']

def on_message(client, userdata, msg):
    print(f'{msg.payload.decode()}')

print(mqtt_config['mqtt']['host'])

client = paho.Client()
client.on_message = on_message
client.connect(BROKER, PORT)
client.subscribe(mqtt_config['mqtt']['subscribe'])
client.loop_forever()
