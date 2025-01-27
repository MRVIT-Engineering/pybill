import click

@click.command()
def bill_init():
    click.echo("Initiating PyBill CLI...")

@click.command()
def bill_list():
    click.echo("Listing all bills...")

@click.command()
def bill_auth():
    click.echo("Press any key to authenticate...")

@click.command()
@click.option("--name", help="Name of the bill")
@click.option("--month", help="Month of the bill")
def bill_create(name: str, month: str):
    click.echo(f"Creating a new bill with name: {name} for month: {month}")
