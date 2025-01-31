import click
from commands.bill_commands import bill_init, bill_list, bill_auth, bill_create

@click.group()
def cli():
    """PyBill CLI tool for managing bills"""
    pass

# Add all commands to the cli group
cli.add_command(bill_init)
cli.add_command(bill_list)
cli.add_command(bill_auth)
cli.add_command(bill_create)

if __name__ == '__main__':
    cli()