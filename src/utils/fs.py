from pathlib import Path
import json

# Gets the config file
def get_config_file() -> Path:
    """Gets the config file path"""
    config_dir = Path.home() / '.pybill'
    config_dir.mkdir(exist_ok=True)  # Create directory if it doesn't exist
    return config_dir / 'config.json'

# Writes the value to the config file
def write_to_config(key: str, value: str) -> None:
    """
    Writes a key-value pair to the config file.
    Creates the file and directory if they don't exist.
    """
    config_file = get_config_file()
    config_file.parent.mkdir(parents=True, exist_ok=True)  # Ensure directory exists
    
    # Read existing config
    if config_file.exists():
        with open(config_file, 'r') as f:
            try:
                config = json.load(f)
            except json.JSONDecodeError:
                config = {}
    else:
        config = {}

    # Update or add new value
    config[key] = value

    # Write back all values
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)

# Reads the value from the config file
def read_from_config(key: str) -> str | None:
    """
    Reads a value from the config file.
    Returns None if the key doesn't exist.
    """
    config_file = get_config_file()
    
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
            return config.get(key)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def get_config_dict() -> dict:
    """
    Reads the entire config file as a dictionary.
    Returns an empty dictionary if the file doesn't exist.
    """
    config_file = get_config_file()
    return json.load(open(config_file, 'r')) if config_file.exists() else {}

def replace_config(config: dict) -> None:
    """
    Replaces the entire config file with the provided dictionary.
    """
    config_file = get_config_file()
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)

def get_customer_by_id(id: str) -> dict:
    """
    Reads the customers from the config file as a dictionary.
    """
    config = get_config_dict()
    return config.get('customers', {}).get(id, {})