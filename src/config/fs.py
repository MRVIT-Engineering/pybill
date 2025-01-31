from pathlib import Path

# Gets the config file
def get_config_file():
    # return Path.home() / '.bill_config'
    return 'bill_config'

# Writes the value to the config file
def write_to_config(key, value):
    # Read existing config
    config = {}
    try:
        with open(get_config_file(), 'r') as f:
            for line in f:
                if '=' in line:
                    k, v = line.strip().split('=')
                    config[k] = v
    except FileNotFoundError:
        pass

    # Update or add new value
    config[key] = value

    # Write back all values
    with open(get_config_file(), 'w') as f:
        for k, v in config.items():
            f.write(f"{k}={v}\n")

# Reads the value from the config file
def read_from_config(key):
    with open(get_config_file(), 'r') as f:
        for line in f:
            if line.startswith(key):
                # Strip whitespace and newlines from the value
                return line.split('=')[1].strip()
        return None
