import click #type: ignore
import importlib.metadata
from commands.bill_commands import bill_init, bill_list_time_entries, bill_create, bill_create_customer
from commands.common_commands import bill_help

@click.group()
@click.version_option(version=importlib.metadata.version("mrvbill"), prog_name="MrvBill CLI")
def cli():
    """MrvBill CLI tool for managing bills"""
    pass

# Add all commands to the cli group
cli.add_command(bill_init)
cli.add_command(bill_list_time_entries)
cli.add_command(bill_create)
cli.add_command(bill_create_customer)
cli.add_command(bill_help)

if __name__ == '__main__':
    cli()