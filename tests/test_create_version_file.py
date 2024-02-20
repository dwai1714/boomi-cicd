from __future__ import annotations

import os
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from cicd.create_version_file import cli
from cicd.create_version_file import short_uuid


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def getUUID():
    return short_uuid()


@patch('cicd.create_version_file.short_uuid')
def test_cli_success(mock_short_uuid, runner):
    # Mock the _short_uuid function to return a known value
    mock_short_uuid.return_value = 'abcd'

    versions_path = '/tmp'
    file_name = 'test_file'

    result = runner.invoke(cli, [versions_path, file_name])

    assert result.exit_code == 0
    assert 'Version file created successfully!' in result.output
    assert os.path.exists(os.path.join(versions_path, f'{file_name}_abcd.py'))  # Use the mocked short UUID value


def test_create_version_file_missing_argument(runner):
    result = runner.invoke(cli, [])
    assert result.exit_code != 0
    assert "Error: Missing argument 'VERSIONS_PATH'." in result.output
    versions_path = '/tmp'
    result = runner.invoke(cli, [versions_path])
    assert "Error: Missing argument 'FILE_NAME'." in result.output
