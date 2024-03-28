from __future__ import annotations

import importlib.util
import json
import os
import sys

from cicd.utils.log import get_logger

logger = get_logger(__name__)


def add_applied_file(ind, file_name, changelog_path):
    """

    Args:
        ind : index of the tuple
        file_name : file name of the tuple
        updates changelog.json with new tuple
        changelog_path : Full path of the directory where changelog.json is present (/tmp/log/)

    Returns:
        None

    """
    environment = os.environ['ENV']

    with open(f'{changelog_path}/changelog.json', 'r') as json_s:
        changelog_dict = json.load(json_s)
        env_dict = changelog_dict[environment]
        env_dict[str(ind)] = file_name
        logger.info(changelog_dict)
    with open(f'{changelog_path}/changelog.json', 'w') as json_s:
        json.dump(changelog_dict, json_s)


def remove_applied_file(ind, changelog_path):
    """

    Args:
        removes element by key from changelog.json
        changelog_path : Full path of the directory where changelog.json is present (/tmp/log/)

    Returns:
        None

    """
    environment = os.environ['ENV']

    with open(f'{changelog_path}/changelog.json', 'r') as json_s:
        changelog_dict = json.load(json_s)
        del changelog_dict[environment][str(ind)]
        logger.info(changelog_dict)
    with open(f'{changelog_path}/changelog.json', 'w') as json_s:
        json.dump(changelog_dict, json_s)


def load_module(file_path, file_name, module_name):
    full_file_name = os.path.join(file_path, file_name)
    spec = importlib.util.spec_from_file_location(module_name, full_file_name)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def apply_forward(version_path, file_name):
    """
        Apply a version file to the database.

        Args:
            version_path (str): The path to the directory containing the version files.
            file_name (str): The name of the version file to apply.

        Raises:
            Exception: If the version file fails to apply.

        """
    module_name = 'versions'
    module = load_module(version_path, file_name, module_name)
    try:
        module.forward()
    except Exception as e:
        logger.error(f'Failed to add file {file_name}, Doing rollback')
        logger.info(e)
        module.backward()
        return


def process_file(version_path, file_name, ind, changelog_path):
    """

    Args:
        file_name (): The version file that we are processing
        ind (): The index that is needed for the configlog.json
        changelog_path : Full path of the directory where changelog.json is present (/tmp/log/)


    Returns:
        None

    """
    apply_forward(version_path, file_name)
    add_applied_file(ind, file_name, changelog_path)


def apply_rollback(version_path, file_name):
    """
        Apply a version file to the database.

        Args:
            version_path (str): The path to the directory containing the version files.
            file_name (str): The name of the version file to apply.

        Raises:
            Exception: If the version file fails to apply.

        """
    module_name = 'versions'
    module = load_module(version_path, file_name, module_name)
    try:
        module.backward()
    except Exception as e:
        logger.info(e)
        raise RuntimeError(
            'IMPORTANT: Fatal Error:Failed to roll back. Please check the errors and do manual intervention',
        )


def rollback_file(versions_path, file_name, ind, changelog_path):
    """

    Args:
        file_name (): The version file that we are processing
        ind (): The index that is needed for the configlog.json
        changelog_path : Full path of the directory where changelog.json is present (/tmp/log/)


    Returns:
        None

    """
    apply_rollback(versions_path, file_name)
    remove_applied_file(ind, changelog_path)
