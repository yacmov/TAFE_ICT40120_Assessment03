import random
from config_parser import load_config_yaml

class weather():
    def __init__(self, path):
        self.config = load_config_yaml(path)
        
        
        
    def generate(self):    
        self.emoji = list(self.config['weather']['weather_list'])
        selected_emoji = f" {(self.emoji[random.randint(0, len(self.emoji) -1)])}"
        selected_temp = f"{random.randint(1,45):0>2}"
        return selected_emoji, selected_temp
