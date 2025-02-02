import click #type: ignore
import questionary #type: ignore
import asyncio #type: ignore
from rich.console import Console #type: ignore
from rich.panel import Panel #type: ignore  
from pyfiglet import Figlet #type: ignore
from questionary import Style #type: ignore
from rich.table import Table

from providers.harvest_provider import HarvestProvider
from utils.fs import read_from_config, write_to_config
from decorators.provider import with_provider
  
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
    def _print_welcome_text(self):
        f = Figlet(font='slant')
        ascii_art = f.renderText('PyBill CLI')
        
        welcome_panel = Panel(
            f"[bold magenta]{ascii_art}[/bold magenta]\n"
            "[cyan]A modern CLI tool for managing software development billable hours / invoices.[/cyan]",
            border_style="green",
            padding=(1, 2)
        )
        
        self.console.print(welcome_panel)

    def _print_time_entries(self, time_entries):
      """
      Prints the time entries in a table
      """ 
      table = Table(title="Time Entries")
      
      # Add columns
      table.add_column("Date", style="cyan")
      table.add_column("Project", style="magenta")
      table.add_column("Task", style="green")
      table.add_column("Hours", justify="right", style="yellow")
      
      # Add rows
      for entry in time_entries:
          table.add_row(
              entry["spent_date"],
              entry["project"]["name"],
              entry["task"]["name"],
              str(entry["hours"])
          )
      
      # Print the table
      self.console.print(table)
    
    def _get_config_basic_info(self):
        """
        Get the basic information from the user and write it to the config file.
        """
        configured = read_from_config('CONFIGURED')
        if configured == '1':
            click.echo("Bill is already configured. Please run 'bill init' to reconfigure.")
            return
        
        self._print_welcome_text()
        national_trade_register_no = questionary.text('What is the national trade register number of your company? (CUI)').ask()
        vendor_name= questionary.text('What is the name of your company (vendor)?').ask()
        vendor_vat_code = questionary.text('What is the VAT code of your company?').ask()
        vendor_address = questionary.text('What is the address of your company?').ask()
        vendor_city = questionary.text('What is the city of your company?').ask()
        vendor_zip = questionary.text('What is the zip code of your company?').ask()
        vendor_country = questionary.text('What is the country of your company?').ask()
        vendor_email = questionary.text('What is the email of your company?').ask()
        vendor_phone = questionary.text('What is the phone number of your company?').ask()
        invoices_folder = questionary.path('Where should the invoices be saved?').ask()
        rate_per_hour = questionary.text('What is the rate per hour for your company?').ask()
        currency = questionary.text('What is the currency for your company?').ask()
        invoice_series_name = questionary.text('Input a name for the invoice series?').ask()
        invoice_series_number = questionary.text('Input the invoice series starting number?').ask()

        write_to_config('VENDOR_NAME', vendor_name)
        write_to_config('VENDOR_VAT_CODE', vendor_vat_code)
        write_to_config('VENDOR_ADDRESS', vendor_address)
        write_to_config('VENDOR_CITY', vendor_city)
        write_to_config('VENDOR_ZIP', vendor_zip)
        write_to_config('VENDOR_COUNTRY', vendor_country)
        write_to_config('VENDOR_RATE_PER_HOUR', int(rate_per_hour))
        write_to_config('VENDOR_CURRENCY', currency)
        write_to_config('VENDOR_EMAIL', vendor_email)
        write_to_config('VENDOR_PHONE', vendor_phone)
        write_to_config('INVOICES_FOLDER', invoices_folder)
        write_to_config('NATIONAL_TRADE_REGISTER_NO', national_trade_register_no)
        write_to_config('CONFIGURED', '1')
        write_to_config('INVOICE_SERIES_NAME', invoice_series_name)
        write_to_config('INVOICE_SERIES_NUMBER', int(invoice_series_number))


    # Instance methods without Click decorators
    def init_command(self):
        provider = read_from_config('PROVIDER')

        self._get_config_basic_info()

        if provider is None:
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
    async def list_time_entries_command(self, month: str):    
        time_entries = await self.provider.get_time_entries(month)
        self._print_time_entries(time_entries)


    @with_provider
    def create_command(self, month: str, name: str):
        asyncio.run(self.provider.create_bill(month, name))

# Create instance first
bill_commands = BillCommands()

# Define commands using standalone functions
@click.command('init')
def bill_init():
    return bill_commands.init_command()

@click.command('list-time')
@click.option('--month', type=str, required=True)
def bill_list_time_entries(month: str):
    return asyncio.run(bill_commands.list_time_entries_command(month))

@click.command('create')
@click.option('--month', type=str, required=True)
@click.option('--name', type=str)
def bill_create(month: str, name: str):
    return bill_commands.create_command(month, name)