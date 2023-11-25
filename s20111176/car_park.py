from car import car
from datetime import datetime
from mqtt_pub import mqtt_broker
import os

class car_park():
    def __init__(self, max_bays):
        self.all_cars = []
        self.max_bays = max_bays


    def car_in(self, plate_number, weather, temp):
        if plate_number == "": return
        if self.get_specific_car(plate_number) != None: return
        new_car = car(plate_number)
        self.all_cars.append(new_car)
        if len(self.all_cars) <= self.max_bays: new_car.car_parked = True
        self.recode_log(plate_number)
        mqtt_broker.mqtt_broker(f"in  | {self.get_available_bays():0>3} | {self.get_car_detail(plate_number)} {weather}  {temp}")
        print("car in")
        return new_car


    def car_out(self, plate_number, weather, temp):
        if plate_number == "": return
        selected_car = self.get_specific_car(plate_number)
        if selected_car == None: return
        selected_car.car_out()
        self.recode_log(plate_number)
        mqtt_bay = self.max_bays + 1 - self.get_current_parking()
        if len(self.all_cars)  > self.max_bays: mqtt_bay = 0
        mqtt_broker.mqtt_broker(f"out | {mqtt_bay:0>3} | {self.get_car_detail(plate_number)} {weather}  {temp}")
        self.all_cars.remove(selected_car)
        self.car_park_waiting_list_into_park()
        print("car out")
        return selected_car


    def car_parked(self, plate_number):
        selected_car = self.get_specific_car(plate_number)
        if selected_car == None: return
        selected_car.car_parked = True

    def car_park_waiting_list_into_park(self):
        for car in enumerate(self.all_cars):
            if self.max_bays == self.get_current_parking(): continue
            if self.all_cars[car[0]].car_out_time != None: continue
            if self.all_cars[car[0]].car_parked == False:
                self.all_cars[car[0]].car_parked = True
                continue

    def is_car_parked(self, plate_number):
        try:
            return self.get_specific_car(plate_number).car_parked
        except:
            pass


    def convert_formatted_time(self, time):
        return time.strftime("%H:%M:%S")
    
    def get_specific_car(self, plate_number):
        selected_car = None
        for car in enumerate(self.all_cars):
            if self.all_cars[car[0]].plate_number == plate_number:
                selected_car = car[1]
                break
        return selected_car
        
    def get_available_bays(self):
        carpark_available_bays = self.max_bays - self.get_current_parking()
        if carpark_available_bays <= 0: return 0
        return carpark_available_bays
    
    def get_waiting_number_of_cars(self):
        que = len(self.all_cars) - self.max_bays
        if que <= 0: return 0
        return que

    def get_current_parking(self):
        current_bay = 0
        for bay in enumerate(self.all_cars):
            if self.all_cars[bay[0]].car_parked == True:
                current_bay += 1
        if current_bay >= self.max_bays:
            return self.max_bays
        return current_bay
    
    def get_car_detail(self, plate_number):
        selected_car = self.get_specific_car(plate_number)
        if selected_car == None: return
        car_in_time = str(selected_car.car_in_time)[11:-7]
        car_out_time = str(selected_car.car_out_time)[11:-7]
        if car_out_time == "": car_out_time = "00:00:00"
        duration = str(selected_car.parking_duration)[:-7]
        if duration == "": duration = "0:00:00"
        car_parked = selected_car.car_parked
        if car_parked == True: car_parked = "True "
        return f"Plate number: {plate_number}\t| Car in: {car_in_time}\t| Car out: {car_out_time}\t| Duration: {duration}\t| Parked?: {car_parked}\t| "
    

    def load_log_when_start(self):
        date = datetime.today()
        date = str(date)[:-16]
        file_path = f's20111176/log/{date}.txt'
        if not os.path.exists(file_path):
            with open(file_path, 'w') as file:
                file.write()
        with open(file_path, 'r') as file:
            log_load = file.readlines()
        
        for line in log_load:
            plate_number_start = line.find("Plate Number:") + len("Plate Number:")+ 1
            plate_number_end = line.find("\t", plate_number_start)
            plate_number = line[plate_number_start:plate_number_end].strip()
            car_in_time_start = line.find("Car in:") + len("Car in:")+ 1
            car_in_time_end = line.find("\t", car_in_time_start)
            car_in_time = line[car_in_time_start:car_in_time_end].strip()
            car_out_time_start = line.find("Car out:") + len("Car out:")+ 1
            car_out_time_end = line.find("\t", car_out_time_start)
            car_out_time = line[car_out_time_start:car_out_time_end].strip()
            car_parked_start = line.find("Parked?:") + len("Parked?:")+ 1
            car_parked_end = line.find("\t", car_parked_start)
            car_parked = line[car_parked_start:car_parked_end].strip()     
            car_park_duration_start = line.find("Duration:") + len("Duration:")+ 1
            car_park_duration_end = line.find("\t", car_park_duration_start)
            car_park_duration = line[car_park_duration_start:car_park_duration_end].strip()
            print(car_parked)
            new_car = car(plate_number)
            current_date = datetime.today().date()
            time_obj = datetime.strptime(f"{car_in_time}.111", "%H:%M:%S.%f").time()
            new_car.car_in_time = datetime.combine(current_date, time_obj)
            if car_out_time != "00:00:00":
                selected_car = self.get_specific_car(plate_number)
                if selected_car != None:
                    self.all_cars.remove(selected_car)
                    continue
            self.all_cars.append(new_car)
            new_car.car_parked = car_parked.lower() == "true"
            
            
        

    def recode_log(self, plate_number):
        date = datetime.today()
        date = str(date)[:-16]
        msg = str(self.get_car_detail(plate_number))
        with open(f's20111176/log/{date}.txt', 'a') as file:
            file.write(f"{msg}\n")

    

if __name__ == "__main__":
    cp1 = car_park(3)
    cp1.load_log_when_start()
    print(len(cp1.all_cars))
    print(cp1.all_cars[0].car_in_time)
    print(cp1.all_cars[len(cp1.all_cars) -1].car_parked)
    print(cp1.all_cars[len(cp1.all_cars) -1].plate_number)
    print(cp1.all_cars[104].parking_duration)



