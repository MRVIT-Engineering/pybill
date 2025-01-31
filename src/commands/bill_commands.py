import click # type: ignore
import questionary # type: ignore
from rich.console import Console 
from rich.panel import Panel
from pyfiglet import Figlet

from config.fs import read_from_config
from questionary import Style # type: ignore
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

def __print_welcome_text():
    # Option 1: Using pyfiglet for ASCII art
    f = Figlet(font='slant')
    ascii_art = f.renderText('PyBill CLI')
    
    # Option 2: Using rich for styled panel
    console = Console()
    welcome_panel = Panel(
        f"[bold magenta]{ascii_art}[/bold magenta]\n"
        "[cyan]A modern CLI tool for managing software development billable hours / incoices.[/cyan]",
        border_style="green",
        padding=(1, 2)
    )
    
    console.print(welcome_panel)

@click.command('init')
def bill_init():

    provider = read_from_config('PROVIDER')
    print (f"Provider is {provider}")

    if provider is None:
        __print_welcome_text()
        billing_provider = questionary.select(
            "Select your billing / time tracking provider",
            choices=["Harvest", "Stripe"],
            style=custom_styles
        ).ask()

        if billing_provider == "Harvest":
            provider = HarvestProvider()
            provider.setup_config()
    else:
        click.echo(f"{provider} is already set up as the billing provider")  
    

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
