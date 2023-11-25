import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import unittest
import car_park_display


class Test_CarPark_Display(unittest.TestCase):
    def test_car_park_display_fields_type_is_list(self):
        test_text = []
        test_display = car_park_display.CarParkDisplay.fields
        
        print(f"test_text's Type: {type(test_text)}")
        print(f"test_display's Type: {type(test_display)}")

        self.assertEqual(type(test_display), type(test_text))

if __name__ == '__main__':
    unittest.main()