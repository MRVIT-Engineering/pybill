import click #type: ignore
import questionary #type: ignore
from rich.console import Console #type: ignore
from rich.panel import Panel #type: ignore  
from pyfiglet import Figlet #type: ignore

from config.fs import read_from_config
from questionary import Style #type: ignore
from providers.harvest_provider import HarvestProvider

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

    def _get_provider(self):
        provider_name = read_from_config('PROVIDER')
        if provider_name == 'harvest':
            return HarvestProvider()
        return None

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

    def list_command(self):
        if not self.provider:
            click.echo("No provider configured. Please run 'bill init' first.")
            return
        self.provider.get_bills()

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

@click.command()
def bill_list():
    return bill_commands.list_command()

@click.command()
def bill_auth():
    return bill_commands.auth_command()

@click.command()
@click.option("--name", help="Name of the bill")
@click.option("--month", help="Month of the bill")
def bill_create(name: str, month: str):
    return bill_commands.create_command(name, month)

