import click
import questionary

from providers.provider import Provider
from pathlib import Path

CONFIG_FILE = Path.home() / '.bill_config'

class HarvestProvider(Provider):
    def __init__(self):
        super().__init__()
        pass
    
    def get_pat(self):
        with open(CONFIG_FILE, 'r') as f:
            return f.read().split('=')[1]
    
    def setup_config(self):
        pat = questionary.password("Enter your Harvest Personal Access Token: ").ask()

        with open(CONFIG_FILE, 'w') as f:
          f.write(f"PAT={pat}")

        click.echo(f"Harvest PAT saved to config file {self.get_pat()} in {CONFIG_FILE}")


    def get_bills(self):
        click.echo("Getting bills from Harvest...")
        pass

    def create_bill(self):
        click.echo("Creating a new bill in Harvest...")
        pass

    def get_time_entries(self):
        click.echo("Getting time entries from Harvest...")
        pass
