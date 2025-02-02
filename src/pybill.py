import click #type: ignore
from commands.bill_commands import bill_init, bill_list_time_entries, bill_create, bill_create_customer

@click.group()
def cli():
    """PyBill CLI tool for managing bills"""
    pass

# Add all commands to the cli group
cli.add_command(bill_init)
cli.add_command(bill_list_time_entries)
cli.add_command(bill_create)
cli.add_command(bill_create_customer)

if __name__ == '__main__':
    cli()