from __future__ import annotations

import os
from pathlib import Path

import envtoml

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))



def get_config(config_file_path: str):
    """
    Load Config from toml file
    Returns:
        config as dictionary

    """
    environment = os.environ['ENV']
    if environment not in ('DEV', 'QA', 'PROD'):
        raise RuntimeError('Environment ENV can be only DEV, QA, PROD')
    config = envtoml.load(open(config_file_path))
    return config


def get_project_root() -> Path:
    """
    Get the project root path (~/boomi_cicd)
    Returns:
        the project root path

    """
    return Path(__file__).parent.parent
