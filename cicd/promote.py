from __future__ import annotations

import json
import os
import shutil

from cicd.common_functions import process_file
from cicd.common_functions import rollback_file
from cicd.utils.log import get_logger

logger = get_logger(__name__)


def get_sorted_dict(items):
    """

    Args:
        items (): Unsorted set of dict

    Returns:
        dictionary, sorted list

    """
    lst = []
    for item in items:
        lst.append(item[0])
    new_list = [int(current_integer) for current_integer in lst]
    sorted_list = sorted(new_list)
    item_dict = dict(items)
    return item_dict, sorted_list


def _find_difference(changelog_path):
    """
    Reads from changelog.json, does a diff of the dev and the env specific dictionary
    Returns:
        set containing the differences
    """
    environment = os.environ['ENV']
    with open(f'{changelog_path}/changelog.json') as json_s:
        changelog_dict = json.load(json_s)
        dev_dict = set((changelog_dict['DEV']).items())
        env_dict = set((changelog_dict[environment]).items())
        return dev_dict - env_dict


def apply_changes(versions_path, changelog_path):
    """
    apply the changes from DEV to higher environments
    Returns:

    """
    source_file = f'{changelog_path}/changelog.json'
    destination_dir = '/tmp/'
    shutil.copy(source_file, destination_dir)

    items = _find_difference(changelog_path)
    item_dict, sorted_list = get_sorted_dict(items)

    for ind in sorted_list:
        file_name = item_dict[str(ind)]
        process_file(versions_path, file_name, ind, changelog_path)


def rollback_changes(versions_path, changelog_path):
    """
    rollback the changes from  higher environments if tests fail
    Returns:

    """
    items = _find_difference('/tmp')
    item_dict, sorted_list = get_sorted_dict(items)
    if len(sorted_list) != 0:
        reversed_list = sorted_list[::-1]

        for ind in reversed_list:
            file_name = item_dict[str(ind)]
            rollback_file(versions_path, file_name, ind, changelog_path)
    else:
        logger.info('Nothing to Rollback')
