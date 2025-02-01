import click #type: ignore
import questionary #type: ignore
import asyncio #type: ignore
from rich.console import Console #type: ignore
from rich.panel import Panel #type: ignore  
from pyfiglet import Figlet #type: ignore

from config.fs import read_from_config
from questionary import Style #type: ignore
from providers.harvest_provider import HarvestProvider
from utils.date import get_first_day_of_month, get_last_day_of_month
def with_provider(f):
    def wrapper(self, *args, **kwargs):
        configProvider = read_from_config('PROVIDER')
        if configProvider == 'harvest':
            self.provider = HarvestProvider()
        
        if not self.provider:
            click.echo("No provider configured. Please run 'bill init' first.")
            return
            
        return f(self, *args, **kwargs)
    return wrapper
  
class BillCommands:
    def __init__(self):
        self.console = Console()
        self.provider = self._get_provider()
        self.custom_styles = Style([
            ('qmark', 'fg:#673ab7 bold'),
            ('question', 'bold'),
            ('answer', 'fg:#f44336 bold'),
            ('pointer', 'fg:#673ab7 bold'),
            ('highlighted', 'fg:#673ab7 bold'),
            ('selected', 'fg:#cc5454'),
            ('separator', 'fg:#673ab7'),
            ('instruction', 'fg:#808080'),
        ])

    # Used in __init__ to get the provider's initial value if there is one.
    def _get_provider(self):
        provider_name = read_from_config('PROVIDER')
        if provider_name == 'harvest':
            return HarvestProvider()
        return None
    
    # Prints prettified welcome text to the console. 
    def __print_welcome_text(self):
        f = Figlet(font='slant')
        ascii_art = f.renderText('PyBill CLI')
        
        welcome_panel = Panel(
            f"[bold magenta]{ascii_art}[/bold magenta]\n"
            "[cyan]A modern CLI tool for managing software development billable hours / invoices.[/cyan]",
            border_style="green",
            padding=(1, 2)
        )
        
        self.console.print(welcome_panel)

    # Instance methods without Click decorators
    def init_command(self):
        provider = read_from_config('PROVIDER')

        if provider is None:
            self.__print_welcome_text()
            billing_provider = questionary.select(
                "Select your billing / time tracking provider",
                choices=["Harvest", "Stripe"],
                style=self.custom_styles
            ).ask()

            if billing_provider == "Harvest":
                provider = HarvestProvider()
                provider.setup_config()
                self.provider = provider
        else:
            click.echo(f"{provider} is already set up as the billing provider")

    @with_provider
    def list_time_entries_command(self, month: str):
        first_day = get_first_day_of_month(month)
        last_day = get_last_day_of_month(month)
        
        asyncio.run(self.provider.get_time_entries(first_day, last_day))

    def auth_command(self):
        if not self.provider:
            click.echo("No provider configured. Please run 'bill init' first.")
            return
        click.echo("Press any key to authenticate...")

    def create_command(self, name: str, month: str):
        if not self.provider:
            click.echo("No provider configured. Please run 'bill init' first.")
            return
        self.provider.create_bill()

# Create instance first
bill_commands = BillCommands()

# Define commands using standalone functions
@click.command('init')
def bill_init():
    return bill_commands.init_command()

@click.command('list-time')
@click.argument('month', type=str, required=True)
def bill_list_time_entries(month: str):
    return bill_commands.list_time_entries_command(month)
