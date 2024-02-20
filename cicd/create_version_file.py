from __future__ import annotations

import hashlib
import os
import time
import uuid

import click
from humanfriendly import format_timespan
from pyfiglet import Figlet


def short_uuid():
    my_uuid = uuid.uuid4()
    uuid_bytes = my_uuid.bytes
    hash_value = hashlib.md5(uuid_bytes).hexdigest()
    short_uuid = hash_value[:4]
    return short_uuid


@click.command()
@click.argument('versions_path')
@click.argument('file_name')
def cli(versions_path, file_name):
    """
        versions_path: Full Path to your versions folder

        file_name: The file name (without spaces and without extension)
    """
    f = Figlet(font='slant')
    click.echo(f.renderText('create a version file Such as create_xyz_model. Dont give spaces or extension '))
    click.echo(f'versions_path {versions_path}')
    click.echo(f'file name {file_name}')

    uuid_value = short_uuid()
    full_file_name = os.path.join(versions_path, file_name)
    full_file_name = f'{full_file_name}_{uuid_value}.py'

    content = """
from __future__ import annotations
import os
from pathlib import Path

# Example of how to import from boomi-cicd package
from cicd.resources.model import Model
from cicd.resources.repository import Repository
VERSION_DIR = os.path.dirname(os.path.abspath(__file__)) # This is full path where your version file is
PROJECT_ROOT_PATH = os.getcwd() # This is the root path of your project
def forward():
    # Write your forward function
    pass


def backward():
    # Write your backward function
    pass
"""
    with open(full_file_name, 'w') as f:
        f.write(content)

    click.echo('Version file created successfully!')


if __name__ == '__main__':
    start = time.time()
    cli()
    click.echo(f'Execution time: {format_timespan(time.time() - start)}')
