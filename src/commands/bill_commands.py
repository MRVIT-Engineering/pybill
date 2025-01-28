import click
import questionary
from questionary import Style
from providers.harvest_provider import HarvestProvider

custom_styles = Style([
    ('qmark', 'fg:#673ab7 bold'),       # The '?' symbol
    ('question', 'bold'),               # The question text
    ('answer', 'fg:#f44336 bold'),      # The answered value
    ('pointer', 'fg:#673ab7 bold'),     # The arrow pointer
    ('highlighted', 'fg:#673ab7 bold'), # The highlighted choice
    ('selected', 'fg:#cc5454'),         # The selected choice
    ('separator', 'fg:#673ab7'),        # The separator between choices
    ('instruction', 'fg:#808080'),   
])

@click.command()
def bill_init():
    click.echo("Initiating PyBill CLI...")
    billing_provider = questionary.select(
        "Select your billing / time tracking provider",
        choices=["Harvest", "Stripe"],
        style=custom_styles
    ).ask()

    provider = None 

    if billing_provider == "Harvest":
        provider = HarvestProvider()
        provider.setup_config()
    
    click.echo(f"Selected billing provider: {billing_provider}")

@click.command()
def bill_list():
    click.echo("Listing all bills...")

@click.command()
def bill_auth():
    click.echo("Press any key to authenticate...")

@click.command()
@click.option("--name", help="Name of the bill")
@click.option("--month", help="Month of the bill")
def bill_create(name: str, month: str):
    click.echo(f"Creating a new bill with name: {name} for month: {month}")
