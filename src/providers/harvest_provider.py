import json
import click # type: ignore
import questionary # type: ignore
import aiohttp # type: ignore
from config.fs import write_to_config, read_from_config
from providers.provider import Provider
from pathlib import Path
from rich.table import Table
from rich.console import Console

CONFIG_FILE = Path.home() / '.bill_config'

class HarvestProvider(Provider):
    __api_url = "https://api.harvestapp.com/v2"

    def __init__(self):
      super().__init__()
      self.console = Console()

        
    # Create HTTP request for Harvest API
    def __get_http_headers(self):
      print(read_from_config('PAT'))
      print(read_from_config('ACCOUNT_ID'))

      return  {
        "Authorization": f"Bearer {read_from_config('PAT')}",
        "Harvest-Account-ID": f"{read_from_config('ACCOUNT_ID')}"
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
    
    """
    Gets the bill config.
    Used to check if the config is valid or not."""
    def get_bill_config(self):
      config_pat = read_from_config('PAT')
      config_account_id = read_from_config('ACCOUNT_ID')

      return {
        config_pat,
        config_account_id 
      }
    
    # Sets up the config file with the PAT
    def setup_config(self):
      config_pat = read_from_config('PAT')
      config_account_id = read_from_config('ACCOUNT_ID')
      write_to_config("PROVIDER", "harvest")


      # Get credentials synchronously before async operations
      if config_pat is None or config_account_id is None:
        # These are sync operations and should be done before async code
        pat = questionary.password("Enter your Harvest Personal Access Token: ").ask()
        account_id = questionary.text("Enter your Harvest account ID: ").ask()

        
        write_to_config("PAT", pat)
        write_to_config("ACCOUNT_ID", account_id)
        click.echo(f"Harvest PAT saved to config file {read_from_config('PAT')} in {CONFIG_FILE}")
      else:
        click.echo("Harvest PAT & Account ID already configured")

      # asyncio.run(self.__get_user_data())
      pass

    # Fetches the bills from Harvest
    def get_bills(self):
      click.echo("Getting bills from Harvest...")
      pass

    # Creates a new bill in Harvest
    def create_bill(self):
      click.echo("Creating a new bill in Harvest...")
      pass

    # Fetches the time entries from Harvest
    async def get_time_entries(self, first_day: str, last_day: str):
      async with aiohttp.ClientSession() as session:
        async with session.get(f"{self.__api_url}/time_entries?from={first_day}&to={last_day}", headers=self.__get_http_headers()) as response:
          
          data = await response.json()
          time_entries = list(map(self._map_time_entry, data["time_entries"]))
          self._print_time_entries(time_entries)
      pass