import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import unittest
from config_parser import load_config_yaml


class Test_Config_Parsing(unittest.TestCase):
    
    def test_parse_config_has_correct_location_and_spaces(self):
        config = load_config_yaml('s20111176/app_config.yaml')
        self.assertEqual(config['app_info']['title'], "SMART CAR PARK")
        self.assertEqual(config['display_frame']['display_max_bay'], 150)

    def test_display_frame_emoji(self):
        config = load_config_yaml('s20111176/app_config.yaml')
        self.assertEqual(config['display_frame']['current_bays_icon'], " 🅿️ : ")

    def test_weather_list(self):
        config = load_config_yaml('s20111176/app_config.yaml')
        weather_list = ["☀️", "🌤️", "⛅", "🌥️", "🌦️", "🌧️", "⛈️", "🌩️", "🌨️", "⛄", "🌪️", "🌊"]
        self.assertEqual(config['weather']['weather_list'], weather_list)

    

if __name__ == '__main__':
    unittest.main()