from __future__ import annotations

import json
import os
import sys
from unittest.mock import patch

from cicd.common_functions import add_applied_file
from cicd.common_functions import load_module
from cicd.common_functions import remove_applied_file


def test_add_applied_file(tmp_path):
    changelog_path = tmp_path / 'log'
    changelog_path.mkdir()

    changelog_content = {
        'test': {'0': 'file1.txt', '1': 'file2.txt'},
    }
    with open(changelog_path / 'changelog.json', 'w') as f:
        json.dump(changelog_content, f)

    # Mocking os.environ['ENV']
    with patch.dict('os.environ', {'ENV': 'test'}):
        add_applied_file(2, 'file3.txt', changelog_path)

    # Reading the modified changelog file to assert the changes
    with open(changelog_path / 'changelog.json', 'r') as f:
        modified_changelog = json.load(f)
        assert modified_changelog == {
            'test': {'0': 'file1.txt', '1': 'file2.txt', '2': 'file3.txt'},
        }


def test_remove_applied_file(tmp_path):
    changelog_path = tmp_path / 'log'
    changelog_path.mkdir()

    # Create a sample changelog JSON file
    changelog_content = {
        'test': {'0': 'file1.txt', '1': 'file2.txt', '2': 'file3.txt'},
    }
    with open(changelog_path / 'changelog.json', 'w') as f:
        json.dump(changelog_content, f)

    # Mocking os.environ['ENV']
    with patch.dict('os.environ', {'ENV': 'test'}):
        remove_applied_file(1, changelog_path)

    # Reading the modified changelog file to assert the changes
    with open(changelog_path / 'changelog.json', 'r') as f:
        modified_changelog = json.load(f)
        assert modified_changelog == {
            'test': {'0': 'file1.txt', '2': 'file3.txt'},
        }


def test_load_module(tmp_path, monkeypatch):
    file_content = """
def hello():
    return 'Hello, World!'
"""
    module_path = tmp_path / 'test_module.py'
    with open(module_path, 'w') as f:
        f.write(file_content)

    monkeypatch.setattr(os.path, 'join', lambda *args: str(module_path))

    module_name = 'test_module'
    loaded_module = load_module(str(tmp_path), 'test_module.py', module_name)
    assert loaded_module.hello() == 'Hello, World!'
    del sys.modules[module_name]
