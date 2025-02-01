import click #type: ignore
from commands.bill_commands import bill_init, bill_list_time_entries

@click.group()
def cli():
    """PyBill CLI tool for managing bills"""
    pass

# Add all commands to the cli group
cli.add_command(bill_init)
cli.add_command(bill_list_time_entries)

if __name__ == '__main__':
    cli()