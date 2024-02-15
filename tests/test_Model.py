from __future__ import annotations

from unittest import mock
from unittest.mock import Mock, patch

import pytest

from cicd.resources.model import Model


@pytest.fixture
def mock_config(monkeypatch):
    mock_config_data = {
        'dev': {
            'account_id': 'dev_account_id',
            'cloud_id': 'dev_cloud_id',
            'base64_credentials': 'dev_base64_credentials',
            'endpoint_url': 'dev_endpoint_url',
        },
        'test': {
            'account_id': 'test_account_id',
            'cloud_id': 'test_cloud_id',
            'base64_credentials': 'test_base64_credentials',
            'endpoint_url': 'test_endpoint_url',
        },
    }
    monkeypatch.setattr('cicd.utils.utility.get_config', lambda _: mock_config_data)


@pytest.fixture
def model_instance(mock_config):
    return Model(
        model_name='TestModel',
        config_file_path='test_config.yaml',
        file_name='test.xml',
        repository_name='TestRepo',
        source_id='TestSource',
    )


def test_init(model_instance):
    assert model_instance.model_name == 'TestModel'
    assert model_instance.config_file_path == 'test_config.yaml'
    assert model_instance.file_name == 'test.xml'
    assert model_instance.repository_name == 'TestRepo'
    assert model_instance.source_id == 'TestSource'
    assert model_instance.account_id == 'dev_account_id'
    assert model_instance.cloud_id == 'dev_cloud_id'
    assert model_instance.base64_credentials == 'dev_base64_credentials'
    assert model_instance.endpoint_url == 'dev_endpoint_url'


@patch('cicd.resources.model.requests.post')
def test_create_model(mock_post, model_instance):
    mock_response = Mock(status_code=200, content=b'Mock response content')
    mock_post.return_value = mock_response

    response, content = model_instance.create_model()

    assert response.status_code == 200
    assert content == b'Mock response content'
    mock_post.assert_called_once_with(
        url='dev_endpoint_url/dev_account_id/models',
        headers={
            'Authorization': 'Basic dev_base64_credentials',
            'Content-Type': 'application/xml',
        },
        data=mock.ANY,
    )
