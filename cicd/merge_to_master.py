from __future__ import annotations

import json
import os

from cicd.common_functions import process_file
from cicd.common_functions import rollback_file
from cicd.utils.log import get_logger

logger = get_logger(__name__)
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def find_files_to_apply(versions_path, changelog_path):
    """

    Args:
        versions_path (): Full Path of where the versions file resides
        changelog_path (): Full Path of where the changelog.json file resides


    Go through versions directory and match with changelog for DEV
    Apply the file that is new. If someone has created two files it will throw error
    Returns:
        highest index in json
        file that has to be applied

    """
    env_dict, files_applied, last_index = get_last_index(changelog_path)

    from os.path import isfile, join
    only_py_files = [
        f for f in os.listdir(versions_path) if (
                isfile(join(versions_path, f)) and f.endswith('.py')
        )
    ]
    logger.info(only_py_files)
    changed_files = set(only_py_files) - set(files_applied)
    if len(changed_files) > 1:
        raise RuntimeError('Number of files is more than 1. Aborting')
    return last_index, changed_files


def get_last_index(changelog_path):
    with open(f'{changelog_path}/changelog.json', 'r') as json_s:
        changelog_dict = json.load(json_s)
        env_dict = changelog_dict['DEV']
        files_applied = list(env_dict.values())
        indexes = list(env_dict.keys())
        last_index = 0
        new_list = [int(current_integer) for current_integer in indexes]
        sorted_list = sorted(new_list)
        if len(indexes) != 0:
            last_index = sorted_list[-1]
    return env_dict, files_applied, last_index


def apply_changes(versions_path, changelog_path):
    """
    Apply the changes that is there in the last checked in file in versions folder
    Returns:

    """
    last_index, changed_file_list = find_files_to_apply(versions_path, changelog_path)
    if len(changed_file_list) == 0:
        return
    file_name = list(changed_file_list)[0]
    process_file(versions_path, file_name, last_index + 1, changelog_path)


def rollback_changes(versions_path, changelog_path):
    env_dict, files_applied, last_index = get_last_index(changelog_path)
    if len(env_dict) != 0:
        file_name = env_dict[str(last_index)]
        rollback_file(versions_path, file_name, last_index, changelog_path)
    else:
        logger.info('Nothing to rollback')
