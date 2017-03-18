import click

from .config import load_configs
from .server import start


@click.command()
@click.option('--config', '-c', multiple=True, required=True)
def runserver(config):
    load_configs(*config)
    start()


runserver()
