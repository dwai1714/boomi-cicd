from __future__ import annotations

import io
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from cicd.resources.source import Source  # Import the class containing the method to be tested


@pytest.fixture
def mock_create_source_xml_data():
    # Mock the payload data
    return b'<xml>sample data</xml>'


@pytest.fixture
def mock_requests_post():
    with patch('cicd.resources.source.requests.post') as mock_post:
        yield mock_post


def test_create_source_raises_runtime_error_when_source_id_already_present(
        mock_requests_post,
        mock_create_source_xml_data,
):
    source = Source('existing_source_id', 'test_config.toml')  # Create an instance of your class
    source.source_id = 'existing_source_id'
    source._list_sources = MagicMock(return_value=['existing_source_id'])

    with pytest.raises(RuntimeError):
        source.create_source()


def test_create_source_raises_runtime_error_when_file_name_is_none(mock_requests_post, mock_create_source_xml_data):
    source = Source('existing_source_id', 'test_config.toml')
    source.file_name = None
    source._list_sources = MagicMock(return_value=[])

    with pytest.raises(RuntimeError):
        source.create_source()


def test_create_source_successful(mock_requests_post, mock_create_source_xml_data):
    source = Source('existing_source_id', 'test_config.toml')  # Create an instance of your class
    source.source_id = 'new_source_id'
    source.file_name = 'test.xml'
    source.endpoint_url = 'http://example.com'
    source.account_id = 'account_id'
    source.headers = {'Content-Type': 'application/xml'}

    source._list_sources = MagicMock(return_value=[])
    with patch('builtins.open', return_value=io.BytesIO(mock_create_source_xml_data)):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_requests_post.return_value = mock_response
        source.create_source()
        assert mock_requests_post.called
        mock_requests_post.assert_called_with(
            url='http://example.com/account_id/sources/create',
            headers={'Content-Type': 'application/xml'},
            data=mock_create_source_xml_data,
        )
