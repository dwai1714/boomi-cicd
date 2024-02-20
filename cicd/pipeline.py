from __future__ import annotations

import argparse
import os
import time

from humanfriendly import format_timespan
from pyfiglet import Figlet

from cicd import merge_to_master
from cicd import promote

f = Figlet(font='slant')


def main():
    parser = argparse.ArgumentParser(description='Run the pipeline file')
    parser.add_argument(
        '--versions_path',
        type=str,
        required=True,
        help='Full Path for your versions folder',
    )
    parser.add_argument(
        '--changelog_path',
        type=str,
        required=True,
        help='Full Path for your changelog.json file',
    )
    parser.add_argument(
        '--rollback',
        type=str,
        required=False,
        help='If you want to rollback then Y',
    )

    args = parser.parse_args()
    env = os.environ['ENV']
    versions_path = args.versions_path
    changelog_path = args.changelog_path
    rollback = args.rollback
    print(f.renderText('run pipeline'))

    print(f'versions_path:\t{versions_path}')
    print(f'changelog_path:\t{changelog_path}')
    print(f'rollback:\t{rollback}')
    print()

    if rollback == 'Y':
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
    main()
    print(f'Execution time: {format_timespan(time.time() - start)}')

"""pip install https://raw.githubusercontent.com/dwai1714/boomi_cicd/main/dist/boomi_cicd-0.1.0-py3-none-any.whl"""
