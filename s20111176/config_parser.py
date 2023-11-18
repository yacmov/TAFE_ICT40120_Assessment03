import yaml

def load_config_yaml(path):
    with open(path, 'r') as file:
        config: dict = yaml.safe_load(file)
    return dict(config)