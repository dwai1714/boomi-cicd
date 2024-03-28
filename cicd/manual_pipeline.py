from __future__ import annotations

import os
import time
from typing import Optional

import click
from humanfriendly import format_timespan
from pyfiglet import Figlet

from cicd import common_functions

f = Figlet(font='slant')


@click.command()
@click.argument('file_name', type=str, required=True)
@click.argument('versions_path', type=str, required=True)
@click.option('--rollback', is_flag=True, help='Set this flag to perform rollback')
def cli(versions_path: str, file_name: str, rollback: Optional[str]):
    env = os.environ.get('ENV', 'DEV')

    click.echo(f.renderText('Manually apply changes. This does not update changelog.json'))
    click.echo(f'file_name: {file_name}')
    click.echo(f'versions_path: {versions_path}')
    click.echo(f'rollback: {rollback}')
    click.echo()

    if env != 'DEV':
        raise ValueError('This command requires environment to be DEV only')
    if rollback:
        common_functions.apply_rollback(versions_path, file_name)
    else:
        common_functions.apply_forward(versions_path, file_name)
    click.confirm('With great power comes great responsibility. This is a risky operation', abort=True)


if __name__ == '__main__':
    start = time.time()
    cli()
    click.echo(f'Execution time: {format_timespan(time.time() - start)}')
