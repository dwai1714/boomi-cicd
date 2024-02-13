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


def load_module(file_path, file_name, module_name):
    full_file_name = os.path.join(file_path, file_name)
    spec = importlib.util.spec_from_file_location(module_name, full_file_name)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def process_file(version_path, file_name, ind, changelog_path):
    """

    Args:
        file_name (): The version file that we are processing
        ind (): The index that is needed for the configlog.json
        changelog_path : Full path of the directory where changelog.json is present (/tmp/log/)


    Returns:
        None

    """
    module_name = 'versions'
    module = load_module(version_path, file_name, module_name)
    try:
        module.forward()
    except Exception as e:
        logger.info(e)
        module.backward()
        return
    add_applied_file(ind, file_name, changelog_path)
