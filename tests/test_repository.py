from cicd.resources.repository import Repository


def test_create_repo(post_repo_api_sucess):
    repository = Repository('test_repo', 'test_config.toml')

    response, response.content = repository.create_repo()

    assert response.status_code == 200


def test_create_repo_failure(post_repo_api_failure):
    repository = Repository('test_repo', 'test_config.toml')

    try:
        response, response.content = repository.create_repo()
        assert response.status_code == 500
    except RuntimeError as e:
        assert str(e) == "Response is not 200. Exiting"


def test_get_repo_id(get_repo_api_sucess):
    repository = Repository('test_repo', 'test_config.toml')

    response = repository.get_repo_id()

    assert int(response) == 1


def test_delete_repo(get_repo_api_sucess, delete_repo_api_success):
    repository = Repository('test_repo', 'test_config.toml')

    response, response.content = repository.delete_repo()

    assert response.status_code == 200


def test_delete_repo_failre(get_repo_api_sucess, delete_repo_api_failure):
    repository = Repository('test_repo', 'test_config.toml')

    try:
        response, response.content = repository.delete_repo()
        assert response.status_code == 500
    except RuntimeError as e:
        assert str(e) == "Response is not 200. Exiting"
