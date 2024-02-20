from __future__ import annotations

import json

import pytest
from click.testing import CliRunner

from cicd.pipeline import cli


@pytest.fixture
def runner():
    return CliRunner()


def test_cli_without_rollback_flag(runner, tmp_path, monkeypatch):
    versions_path = tmp_path / 'versions'
    changelog_path = tmp_path / 'changelog'
    versions_path.mkdir()
    changelog_path.mkdir()
    mock_json_data = {'DEV': {'1': 'xyz_f363.py'}, 'QA': {}, 'PROD': {}}

    with open(f'{changelog_path}/changelog.json', 'w') as f:
        json.dump(mock_json_data, f)
    monkeypatch.setenv('ENV', 'DEV')

    result = runner.invoke(cli, [str(versions_path), str(changelog_path)])
    assert result.exit_code == 0
    assert f'versions_path: {versions_path}' in result.output
    assert f'changelog_path: {changelog_path}' in result.output
    assert 'rollback: False' in result.output


def test_cli_with_rollback_flag(runner, monkeypatch, tmp_path):
    versions_path = tmp_path / 'versions'
    changelog_path = tmp_path / 'changelog'
    versions_path.mkdir()
    changelog_path.mkdir()
    mock_json_data = {'DEV': {'1': 'xyz_f363.py'}, 'QA': {}, 'PROD': {}}

    content = """
def forward():
    # Write your forward function
    pass


def backward():
    # Write your backward function
    pass
    """
    with open(f'{versions_path}/xyz_f363.py', 'w') as f:
        f.write(content)

    with open(f'{changelog_path}/changelog.json', 'w') as f:
        json.dump(mock_json_data, f)
    monkeypatch.setenv('ENV', 'DEV')
    result = runner.invoke(cli, [str(versions_path), str(changelog_path), '--rollback'])
    assert result.exit_code == 0
    assert f'versions_path: {versions_path}' in result.output
    assert f'changelog_path: {changelog_path}' in result.output
    assert 'rollback: True' in result.output
