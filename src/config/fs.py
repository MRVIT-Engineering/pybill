from pathlib import Path

# Gets the config file
def get_config_file():
    return Path.home() / '.bill_config'

# Writes the value to the config file
def write_to_config(key, value):
    with open(get_config_file(), 'w') as f:
        f.write(f"{key}={value}")

# Reads the value from the config file
def read_from_config(key):
    with open(get_config_file(), 'r') as f:
        for line in f:
            if line.startswith(key):
                return line.split('=')[1]
        return None
