import random
import string



class plate_generator():
    def __init__(self):
        self.all_alphabets = list(string.ascii_uppercase)
        self.generated_plate_number = []

    def random_car_plate_number(self):
        self.generated_plate_number.clear()
        self.generated_plate_number.append('1')
        for i in range(3):
            self.generated_plate_number.append(self.all_alphabets[random.randint(0, len(self.all_alphabets) -1)])
        self.generated_plate_number.append('-')
        for y in range(3):
            self.generated_plate_number.append(f"{random.randint(1,9)}")
        car_plate_number = ''.join(str(item) for item in self.generated_plate_number)
        return car_plate_number
        
if __name__ == "__main__":
    plate_generator().random_car_plate_number()