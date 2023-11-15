import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from s20111176.mqtt import mqtt_pub

# -----------------------------------------#
# TODO: STUDENT IMPLEMENTATION STARTS HERE #
# -----------------------------------------#
class CarDetector:
    """Provides a couple of simple buttons that can be used to represent a sensor detecting a car. This is a skeleton only."""

    def __init__(self, formatted_time, current_parking, incoming_msg):
        self.formatted_time = formatted_time
        self.current_parking = current_parking
        self.incoming_msg = incoming_msg
        pass

    def incoming_car(self):
        # TODO: implement this method to publish the detection via MQTT
        mqtt_pub.mqtt_broker(f"car in  {self.formatted_time} [{self.current_parking:0>3}/150] : [{self.incoming_msg}]")
        self.current_parking += 1
        print(self.current_parking)
        return self.current_parking

    def outgoing_car(self):
        # TODO: implement this method to publish the detection via MQTT
        print("Car goes out")


if __name__ == '__main__':
    # TODO: Run each of these classes in a separate terminal. You should see the CarParkDisplay update when you click the buttons in the CarDetector.
    # These classes are not designed to be used in the same module - they are both blocking. If you uncomment one, comment-out the other.

    CarDetector()
