import click

from providers.harvest_provider import HarvestProvider
from utils.fs import read_from_config

def with_provider(f):
    def wrapper(self, *args, **kwargs):
        configProvider = read_from_config('provider')
        if configProvider == 'harvest':
            self.provider = HarvestProvider()
        
        if not self.provider:
            click.echo("No provider configured. Please run 'bill init' first.")
            return
            
        return f(self, *args, **kwargs)
    return wrapper