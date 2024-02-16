from __future__ import annotations

import argparse
import hashlib
import os
import time
import uuid

from humanfriendly import format_timespan
from pyfiglet import Figlet


def short_uuid():
    my_uuid = uuid.uuid4()
    uuid_bytes = my_uuid.bytes
    hash_value = hashlib.md5(uuid_bytes).hexdigest()
    short_uuid = hash_value[:4]
    return short_uuid

def main():
    f = Figlet(font='slant')
    parser = argparse.ArgumentParser(description='Run the pipeline file')
    parser.add_argument(
        '--versions_path',
        type=str,
        required=True,
        help='Full Path for your versions folder',
    )
    parser.add_argument(
        '--file_name',
        type=str,
        required=True,
        help='Name of your file such as create_xyz_model',
    )
    args = parser.parse_args()
    env = os.environ['ENV']
    versions_path = args.versions_path
    file_name = args.file_name

    print(f.renderText('create a version file'))

    print(f'versions_path:\t{versions_path}')
    print(f'file name:\t{file_name}')
    print()
    full_file_name = os.path.join(versions_path,file_name)
    full_file_name = f'{full_file_name}_{short_uuid()}.py'

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

if __name__ == '__main__':
    start = time.time()
    main()
    print(f'Execution time: {format_timespan(time.time() - start)}')
