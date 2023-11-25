import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import yaml

def load_config_yaml(path):
    with open(path, 'r') as file:
        config: dict = yaml.safe_load(file)
    return dict(config)

if __name__ == '__main__':
    test = load_config_yaml("s20111176/mqtt_config.yaml")
    print(test['mqtt']['host']) 