import paho.mqtt.client as paho


class mqtt_broker():
    def mqtt_broker(msg):
        BROKER, PORT = "localhost", 1883
        client = paho.Client()
        client.connect(BROKER, PORT)
        client.publish("lot/sensor", msg)

