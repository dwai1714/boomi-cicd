from __future__ import annotations

import json
import os
import sys
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from cicd.common_functions import add_applied_file
from cicd.common_functions import load_module
from cicd.common_functions import process_file
from cicd.common_functions import remove_applied_file
from cicd.common_functions import rollback_file


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


@patch('cicd.common_functions.load_module')
@patch('cicd.common_functions.add_applied_file')
def test_process_file_successful(add_applied_file_mock, load_module_mock):
    module_mock = MagicMock()
    load_module_mock.return_value = module_mock
    process_file('version_path', 'file_name', 'ind', 'changelog_path')
    load_module_mock.assert_called_once_with('version_path', 'file_name', 'versions')
    module_mock.forward.assert_called_once()
    add_applied_file_mock.assert_called_once_with('ind', 'file_name', 'changelog_path')


@patch('cicd.common_functions.load_module')
@patch('cicd.common_functions.add_applied_file')
def test_process_file_exception(add_applied_file_mock, load_module_mock):
    module_mock = MagicMock()
    load_module_mock.return_value = module_mock
    module_mock.forward.side_effect = Exception('Mock exception')
    process_file('version_path', 'file_name', 'ind', 'changelog_path')
    load_module_mock.assert_called_once_with('version_path', 'file_name', 'versions')
    module_mock.forward.assert_called_once()
    add_applied_file_mock.assert_not_called()


@patch('cicd.common_functions.load_module')
@patch('cicd.common_functions.remove_applied_file')
def test_rollback_file_successful(remove_applied_file_mock, load_module_mock):
    module_mock = MagicMock()
    load_module_mock.return_value = module_mock
    rollback_file('versions_path', 'file_name', 'ind', 'changelog_path')
    load_module_mock.assert_called_once_with('versions_path', 'file_name', 'versions')
    module_mock.backward.assert_called_once()
    remove_applied_file_mock.assert_called_once_with('ind', 'changelog_path')


@patch('cicd.common_functions.load_module')
@patch('cicd.common_functions.remove_applied_file')
def test_rollback_file_exception(remove_applied_file_mock, load_module_mock):
    module_mock = MagicMock()
    load_module_mock.return_value = module_mock
    module_mock.backward.side_effect = Exception('Mock exception')
    with pytest.raises(RuntimeError):
        rollback_file('versions_path', 'file_name', 'ind', 'changelog_path')
    load_module_mock.assert_called_once_with('versions_path', 'file_name', 'versions')
    module_mock.backward.assert_called_once()
    remove_applied_file_mock.assert_not_called()
