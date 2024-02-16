from unittest.mock import Mock

import pytest
import requests


@pytest.fixture
def get_api_success(mocker):
    mocked_response = Mock(spec=requests.Response)
    mocked_response.status_code = 200

    mocker.patch.object(requests, 'get', return_value=mocked_response)

    return mocker


@pytest.fixture
def get_api_failure(mocker):
    mocked_response = Mock(spec=requests.Response)
    mocked_response.status_code = 500

    mocker.patch.object(requests, 'get', return_value=mocked_response)

    return mocker


@pytest.fixture
def post_api_success(mocker):
    mocked_response = Mock(spec=requests.Response)
    mocked_response.status_code = 200

    mocker.patch.object(requests, 'post', return_value=mocked_response)

    return mocker


@pytest.fixture
def post_api_failure(mocker):
    mocked_response = Mock(spec=requests.Response)
    mocked_response.status_code = 500

    mocker.patch.object(requests, 'post', return_value=mocked_response)

    return mocker


@pytest.fixture
def get_repo_api_success(mocker):
    mocked_response = Mock(spec=requests.Response)

    xml_response_content = """
    <mdm:Repositories xmlns:mdm="http://example.com/mdm">
      <mdm:Repository id="1" name="test_repo"/>
      <mdm:Repository id="2" name="repository2"/>
      <mdm:Repository id="3" name="repository3"/>
    </mdm:Repositories>
    """

    mocked_response.content = xml_response_content
    mocked_response.status_code = 200

    mocker.patch.object(requests, 'get', return_value=mocked_response)

    return mocker


@pytest.fixture
def delete_api_success(mocker):
    mocked_response = Mock(spec=requests.Response)
    mocked_response.status_code = 200

    mocker.patch.object(requests, 'delete', return_value=mocked_response)

    return mocker


@pytest.fixture
def delete_api_failure(mocker):
    mocked_response = Mock(spec=requests.Response)
    mocked_response.status_code = 500

    mocker.patch.object(requests, 'delete', return_value=mocked_response)

    return mocker
