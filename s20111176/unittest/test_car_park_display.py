import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import unittest
from config_parser import load_config_yaml

class TestConfigParsing(unittest.TestCase):
    # TODO: class test create 
    def test_parse_config_has_correct_location_and_spaces(self):
        config = load_config_yaml('s20111176/config.yaml')
        self.assertEqual(config['location'], "Moondalup City Square Parking")
        self.assertEqual(config['total_spaces'], 192)

if __name__ == '__main__':
    unittest.main()