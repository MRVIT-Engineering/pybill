import click
import questionary
import requests

from providers.provider import Provider
from pathlib import Path

CONFIG_FILE = Path.home() / '.bill_config'

class HarvestProvider(Provider):
    __api_url = "https://api.harvestapp.com/v2"

    def __init__(self):
        super().__init__()
        pass
    
    # Reads the PAT from the config file
    def __get_pat(self):
        with open(CONFIG_FILE, 'r') as f:
            return f.read().split('=')[1]
        
    # Create HTTP request for Harvest API
    def __get_http_headers(self):
        return  {
          "Authorization": f"Bearer {self.__get_pat()}",
        }
  
    # Sets up the config file with the PAT
    def setup_config(self):
        pat = questionary.password("Enter your Harvest Personal Access Token: ").ask()

        with open(CONFIG_FILE, 'w') as f:
          f.write(f"PAT={pat}")

        response = requests.get(f"{self.__api_url}/users/me", headers=self.__get_http_headers())
        click.echo(response.json())
        click.echo(f"Harvest PAT saved to config file {self.__get_pat()} in {CONFIG_FILE}")


    # Fetches the bills from Harvest
    def get_bills(self):
        click.echo("Getting bills from Harvest...")
        pass

    # Creates a new bill in Harvest
    def create_bill(self):
        click.echo("Creating a new bill in Harvest...")
        pass

    # Fetches the time entries from Harvest
    def get_time_entries(self):
        click.echo("Getting time entries from Harvest...")
        pass
