from datetime import datetime

class car():
    def __init__(self, plate_number):
        self.plate_number = plate_number
        self.car_in_time = datetime.now()
        self.car_out_time = None
        self.parking_duration = None
        self.car_parked = False

    def car_out(self):
        self.car_out_time = datetime.now()
        self.parking_duration = self.car_out_time - self.car_in_time