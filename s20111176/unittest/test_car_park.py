import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import unittest
from car_park import car_park


class Test_CarPark(unittest.TestCase):
    def test_car_park_car_in_return_object_plate_number(self):
        test_plate_number = "TeSt-192"
        test_weather = "☀️"
        test_temp = "30"
        test_car_park = car_park(2)
        test_car_park.car_in(test_plate_number, test_weather, test_temp)
        print(f"test plate number is: {test_plate_number}")
        self.assertEqual(test_plate_number, test_car_park.all_cars[0].plate_number)

    def test_car_park_car_out_return_out_of_range(self):
        test_plate_number = "TeSt-552"
        test_weather = "☀️"
        test_temp = "30"
        test_car_park = car_park(2)
        test_car_park.car_in(test_plate_number, test_weather, test_temp)
        test_car_park.car_out(test_plate_number, test_weather, test_temp)

        print(f"test plate number is: {test_plate_number}")
        
        with self.assertRaises(IndexError):
            test_car_park.all_cars[0].plate_number

if __name__ == '__main__':
    unittest.main()