import click

from pyimagediet.helpers import get_config

CONFIGURE_HELP = '''\
Inspect and print configuration customisation for your environment.'''


@click.command()
@click.option('--check', is_flag=True, help=CONFIGURE_HELP)
def diet(check):
    """Simple program that either print config customisations for your
    environment or compresses file FILE."""
    if check:
        click.echo(get_config())
