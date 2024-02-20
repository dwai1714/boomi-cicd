from __future__ import annotations

from unittest.mock import patch

from cicd.resources.repository import Repository


def test_create_repo(post_api_success):
    repository = Repository('test_repo', 'test_config.toml')

    response, response.content = repository.create_repo()

    assert response.status_code == 200


def test_create_repo_failure(post_api_failure):
    repository = Repository('test_repo', 'test_config.toml')

    try:
        response, response.content = repository.create_repo()
    except RuntimeError as e:
        assert str(e) == 'Response is not 200. Exiting'


def test_get_repo_id(get_repo_api_success):
    repository = Repository('test_repo', 'test_config.toml')

    response = repository.get_repo_id()

    assert int(response) == 1


def test_delete_repo(get_repo_api_success, delete_api_success):
    repository = Repository('test_repo', 'test_config.toml')

    response, response.content = repository.delete_repo()

    assert response.status_code == 200


def test_delete_repo_failre(get_repo_api_success, delete_api_failure):
    repository = Repository('test_repo', 'test_config.toml')

    try:
        response, response.content = repository.delete_repo()
    except RuntimeError as e:
        assert str(e) == 'Response is not 200. Exiting'


@patch('cicd.resources.repository.requests.get')
@patch('cicd.resources.repository.xmltodict.parse')
def test_get_repo_id_with_dict(parse_mock, get_mock):
    response_content = '''
    <mdm:Repositories>
        <mdm:Repository id="1" name="Repo1"/>
    </mdm:Repositories>
    '''
    parse_mock.return_value = {'mdm:Repositories': {'mdm:Repository': {'@id': '1', '@name': 'Repo1'}}}
    get_mock.return_value.content = response_content
    repository = Repository('test_repo', 'test_config.toml')
    repository.repository_name = 'Repo1'
    repo_id = repository.get_repo_id()
    assert repo_id == '1'
