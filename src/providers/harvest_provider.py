import click # type: ignore
import questionary # type: ignore
import aiohttp # type: ignore
from rich.table import Table # type: ignore
from rich.console import Console # type: ignore

from utils.fs import write_to_config, read_from_config
from providers.provider import Provider
from utils.pdf import generate_invoice_pdf
from utils.date import get_first_day_of_month, get_last_day_of_month

class HarvestProvider(Provider):
    __api_url = "https://api.harvestapp.com/v2"

    def __init__(self):
      super().__init__()
      self.console = Console()

        
    # Create HTTP request for Harvest API
    def __get_http_headers(self):
      pat = read_from_config('PAT')
      account_id = read_from_config('ACCOUNT_ID')
      
      if not pat or not account_id:
          raise ValueError("Missing PAT or Account ID in config")
        
      return {
        "Authorization": f"Bearer {pat}",
        "Harvest-Account-ID": account_id
      }
    
    def _map_time_entry(self, time_entry: dict) -> dict:
      """
      Maps the time entry to a dictionary with only the fields we need
      """
      return {
        "id": time_entry["id"],
        "spent_date": time_entry["spent_date"],
        "project": time_entry["project"],
        "task": time_entry["task"],
        "hours": time_entry["hours"],
        "hours_without_timer": time_entry["hours_without_timer"],
        "rounded_hours": time_entry["rounded_hours"],
        "created_at": time_entry["created_at"],
        "updated_at": time_entry["updated_at"],
      }
    
    # Sets up the config file with the PAT
    def setup_config(self):
      config_pat = read_from_config('PAT')
      config_account_id = read_from_config('ACCOUNT_ID')
      write_to_config("provider", "harvest")


      # Get credentials synchronously before async operations
      if config_pat is None or config_account_id is None:
        # These are sync operations and should be done before async code
        pat = questionary.password("Enter your Harvest Personal Access Token: ").ask()
        account_id = questionary.text("Enter your Harvest account ID: ").ask()

        
        write_to_config("PAT", pat)
        write_to_config("ACCOUNT_ID", account_id)
      else:
        click.echo("Harvest PAT & Account ID already configured")

    # Fetches the bills from Harvest
    def get_bills(self):
      click.echo("Getting bills from Harvest...")
      pass

    # Creates a new bill in Harvest
    async def create_bill(self, month: str, customer: str, name: str):
      time_entries = await self.get_time_entries(month)
      generate_invoice_pdf(time_entries, month, name, customer)


    # Fetches the time entries from Harvest
    async def get_time_entries(self, month: str):
      first_day = get_first_day_of_month(month)
      last_day = get_last_day_of_month(month)
      async with aiohttp.ClientSession() as session:
        async with session.get(f"{self.__api_url}/time_entries?from={first_day}&to={last_day}", headers=self.__get_http_headers()) as response:
          data = await response.json()
          time_entries = list(map(self._map_time_entry, data["time_entries"]))
          return time_entries