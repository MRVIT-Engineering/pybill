import click #type: ignore
import questionary #type: ignore
import asyncio #type: ignore
from rich.console import Console #type: ignore
from rich.panel import Panel #type: ignore  
from pyfiglet import Figlet #type: ignore
from questionary import Style #type: ignore
from rich.table import Table #type: ignore

from providers.harvest_provider import HarvestProvider
from utils.fs import read_from_config, write_to_config, get_config_dict, replace_config, get_customer_by_id
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
        provider_name = read_from_config('provider')
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
        configured = read_from_config('configured')
        if configured == '1':
            click.echo("Bill is already configured.")
            return
        
        self._print_welcome_text()
        national_trade_register_no = questionary.text('What is the national trade register number of your company? (CUI)').ask()
        vendor_name= questionary.text('What is the name of your company (vendor)?').ask()
        vendor_vat_code = questionary.text('What is the VAT code of your company?').ask()
        account_number = questionary.text('What is the account number of your company?').ask()
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
        vendor_logo = questionary.text('Url with the logo of your company? (optional)').ask()

        write_to_config('vendor_name', vendor_name)
        write_to_config('vendor_vat_code', vendor_vat_code)
        write_to_config('vendor_address', vendor_address)
        write_to_config('vendor_city', vendor_city)
        write_to_config('vendor_zip', vendor_zip)
        write_to_config('vendor_country', vendor_country)
        write_to_config('vendor_rate_per_hour', int(rate_per_hour))
        write_to_config('vendor_currency', currency)
        write_to_config('vendor_email', vendor_email)
        write_to_config('vendor_phone', vendor_phone)
        write_to_config('invoices_folder', invoices_folder)
        write_to_config('national_trade_register_no', national_trade_register_no)
        write_to_config('configured', '1')
        write_to_config('invoice_series_name', invoice_series_name)
        write_to_config('invoice_series_number', int(invoice_series_number))
        write_to_config('vendor_logo', vendor_logo)
        write_to_config('account_number', account_number)
    
    # Instance methods without Click decorators
    def init_command(self):
        provider = read_from_config('provider')

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
    def create_command(self, month: str, customer: str, name: str):
        customer_dict = get_customer_by_id(customer)
        asyncio.run(self.provider.create_bill(month, customer_dict  , name))
        # Increment the invoice series number
        invoice_series_number = read_from_config('invoice_series_number')
        write_to_config('invoice_series_number', invoice_series_number + 1)

    @with_provider
    def create_customer_command(self, name: str, customer_id: str, address: str, country: str, email: str, phone: str, vat: str):
        config = get_config_dict()
        config['customers'] = {
            customer_id: {
                'name': name,
                'address': address,
                'country': country,
                'email': email,
                'phone': phone,
                'vat': vat
            }
        }
        replace_config(config)

        
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
@click.option('--customer', type=str, required=True)
@click.option('--name', type=str)
def bill_create(month: str, customer: str, name: str):
    return bill_commands.create_command(month, customer, name)


@click.command('create-customer')
@click.option('--name', type=str, required=True)
@click.option('--customer-id', type=str, required=True)
@click.option('--address', type=str, required=True)
@click.option('--country', type=str, required=True)
@click.option('--email', type=str, required=False)
@click.option('--phone', type=str, required=False)
@click.option('--vat', type=str, required=False)
def bill_create_customer(name: str, customer_id: str, address: str, country: str, email: str, phone: str, vat: str):
    return bill_commands.create_customer_command(name, customer_id, address, country, email, phone, vat)