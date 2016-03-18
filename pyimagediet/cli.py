import click

import pyimagediet.process as process
from pyimagediet.helpers import get_config

CONFIGURE_HELP = '''\
Inspect and print configuration customisation for your environment.'''


def get_configuration(ctx, param, value):
    if value:
        click.echo(get_config())
        ctx.exit()


@click.command()
@click.option('--check', is_flag=True, callback=get_configuration,
              help=CONFIGURE_HELP)
@click.option('--config', 'configuration', required=True, envvar='DIET_CONFIG',
              type=click.Path(exists=True))
@click.argument('file', type=click.Path(exists=True))
def diet(file, configuration, check):
    """Simple program that either print config customisations for your
    environment or compresses file FILE."""
    config = process.read_yaml_configuration(configuration)
    process.diet(file, config)
