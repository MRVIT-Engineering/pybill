import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from pyfiglet import Figlet

class CommonCommands:
    def __init__(self):
        self.console = Console()

    def _print_welcome_text(self):
        f = Figlet(font='slant')
        ascii_art = f.renderText('MrvBill CLI')
        
        welcome_panel = Panel(
            f"[bold magenta]{ascii_art}[/bold magenta]\n"
            "[cyan]A modern CLI tool for managing software development billable hours / invoices.[/cyan]",
            border_style="green",
            padding=(1, 2)
        )
        
        self.console.print(welcome_panel)

    def help_command(self):
        self._print_welcome_text()
        
        # Create a table for commands
        table = Table(title="Available Commands")
        table.add_column("Command", style="cyan")
        table.add_column("Description", style="magenta")
        
        # Add commands to the table
        table.add_row(
            "bill init",
            "Initialize the bill configuration and set up your billing provider"
        )
        table.add_row(
            "bill list-time --month <month>",
            "List time entries for a specific month"
        )
        table.add_row(
            "bill create --month <month> --customer <customer_id> [--name <name>]",
            "Create a new bill for a specific month and customer"
        )
        table.add_row(
            "bill create-customer",
            "Create a new customer with required information"
        )
        
        self.console.print(table)
        
        # Add usage examples
        examples_panel = Panel(
            "[bold]Usage Examples:[/bold]\n\n"
            "[cyan]1. Initialize the bill configuration:[/cyan]\n"
            "   bill init\n\n"
            "[cyan]2. List time entries for January:[/cyan]\n"
            "   bill list-time --month January\n\n"
            "[cyan]3. Create a bill for January:[/cyan]\n"
            "   bill create --month January --customer CUST001 --name \"January Invoice\"\n\n"
            "[cyan]4. Create a new customer:[/cyan]\n"
            "   bill create-customer --name \"Acme Corp\" --customer-id CUST001 --address \"123 Main St\" --country \"USA\"",
            title="Examples",
            border_style="blue"
        )
        
        self.console.print(examples_panel)

# Create instance
common_commands = CommonCommands()

# Define the help command
@click.command('help')
def bill_help():
    """Show help information about available commands"""
    return common_commands.help_command()
