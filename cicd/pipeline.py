from __future__ import annotations

import os
import time
from typing import Optional

import click
from humanfriendly import format_timespan
from pyfiglet import Figlet

from cicd import merge_to_master
from cicd import promote

f = Figlet(font='slant')


@click.command()
@click.argument('versions_path', type=str, required=True)
@click.argument('changelog_path', type=str, required=True)
@click.option('--rollback', is_flag=True, help='Set this flag to perform rollback')
def cli(versions_path: str, changelog_path: str, rollback: Optional[str]):
    env = os.environ.get('ENV', 'DEV')

    click.echo(f.renderText('run pipeline'))
    click.echo(f'versions_path: {versions_path}')
    click.echo(f'changelog_path: {changelog_path}')
    click.echo(f'rollback: {rollback}')
    click.echo()

    if rollback:
        if env == 'DEV':
            merge_to_master.rollback_changes(versions_path, changelog_path)
        else:
            promote.rollback_changes(versions_path, changelog_path)
    else:
        if env == 'DEV':
            merge_to_master.apply_changes(versions_path, changelog_path)
        else:
            promote.apply_changes(versions_path, changelog_path)


if __name__ == '__main__':
    start = time.time()
    cli()
    click.echo(f'Execution time: {format_timespan(time.time() - start)}')
