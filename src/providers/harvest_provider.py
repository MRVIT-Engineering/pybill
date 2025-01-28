import click
from providers.provider import Provider
from pathlib import Path

CONFIG_FILE = Path.home() / '.bill_config'

class HarvestProvider(Provider):
    def __init__(self):
        super().__init__()
        pass
    
    def setup_config(self):
        click.echo("Setting up Harvest configuration...")
        api_key = click.input("Enter your Harvest API key: ")
        account_id = click.input("Enter your Harvest account ID: ")


        with open(CONFIG_FILE, 'w') as f:
            f.write(f"api_key: {api_key}\n")
            f.write(f"account_id: {account_id}\n")
        
        click.echo(f"Harvest configuration setup complete. Config file saved to {CONFIG_FILE}")

    def get_bills(self):
        click.echo("Getting bills from Harvest...")
        pass

    def create_bill(self):
        click.echo("Creating a new bill in Harvest...")
        pass

    def get_time_entries(self):
        click.echo("Getting time entries from Harvest...")
        pass
