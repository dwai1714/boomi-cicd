from __future__ import annotations

import io
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from cicd.resources.source import Source  # Import the class containing the method to be tested


@pytest.fixture
def mock_create_source_xml_data():
    return b'<xml>sample data</xml>'


@pytest.fixture
def mock_requests_post():
    with patch('cicd.resources.source.requests.post') as mock_post:
        yield mock_post


@pytest.fixture
def mock_update_source_xml_data():
    return b'<xml>updated sample data</xml>'


@pytest.fixture
def mock_requests_put():
    with patch('cicd.resources.source.requests.put') as mock_put:
        yield mock_put


@pytest.fixture
def mock_requests_delete():
    with patch('cicd.resources.source.requests.delete') as mock_delete:
        yield mock_delete


@pytest.fixture
def mock_requests_get():
    with patch('cicd.resources.source.requests.get') as mock_get:
        yield mock_get


@pytest.fixture
def mock_logger_error():
    with patch('cicd.resources.source.logger.error') as mock_logger:
        yield mock_logger


def test_create_source_raises_runtime_error_when_source_id_already_present(
        mock_requests_post,
        mock_create_source_xml_data,
):
    source = Source('existing_source_id', 'test_config.toml')
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
    source = Source('existing_source_id', 'test_config.toml')
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


def test_create_source_unsuccessful(mock_requests_post, mock_create_source_xml_data, mock_logger_error):
    source = Source('existing_source_id', 'test_config.toml')
    source.source_id = 'existing_source_id'
    source.endpoint_url = 'http://example.com'
    source.account_id = 'account_id'
    source.headers = {'Content-Type': 'application/json'}
    source._list_sources = MagicMock(return_value=['existing_source_id'])
    with patch('builtins.open', return_value=io.BytesIO(mock_create_source_xml_data)):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_requests_post.return_value = mock_response
        with pytest.raises(RuntimeError):
            source.create_source()
            mock_requests_post.assert_called_with(
                url='http://example.com/account_id/sources/create',
                headers={'Content-Type': 'application/xml'},
                data=mock_create_source_xml_data,
            )
            assert mock_logger_error.called_with('Failed to create source. Server Error')


def test_update_source_raises_runtime_error_when_source_id_not_present(mock_requests_put, mock_update_source_xml_data):
    source = Source('existing_source_id', 'test_config.toml')
    source.source_id = 'non_existing_source_id'
    source._list_sources = MagicMock(return_value=['existing_source_id'])
    with pytest.raises(RuntimeError):
        source.update_source()


def test_update_source_successful(mock_requests_put, mock_update_source_xml_data):
    source = Source('existing_source_id', 'test_config.toml')
    source.source_id = 'existing_source_id'
    source.file_name = 'test.xml'
    source.endpoint_url = 'http://example.com'
    source.account_id = 'account_id'
    source.headers = {'Content-Type': 'application/xml'}

    source._list_sources = MagicMock(return_value=['existing_source_id'])
    with patch('builtins.open', MagicMock(return_value=io.BytesIO(mock_update_source_xml_data))):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_requests_put.return_value = mock_response
        source.update_source()
        assert mock_requests_put.called
        mock_requests_put.assert_called_with(
            url='http://example.com/account_id/sources/existing_source_id',
            headers={'Content-Type': 'application/xml'},
            data=mock_update_source_xml_data,
        )


def test_delete_source_raises_runtime_error_when_source_id_not_present(mock_requests_delete):
    source = Source('existing_source_id', 'test_config.toml')
    source.source_id = 'non_existing_source_id'
    source._list_sources = MagicMock(return_value=['existing_source_id'])

    # Act & Assert
    with pytest.raises(RuntimeError):
        source.delete_source()


def test_delete_source_successful(mock_requests_delete):
    source = Source('existing_source_id', 'test_config.toml')
    source.source_id = 'existing_source_id'
    source.endpoint_url = 'http://example.com'
    source.account_id = 'account_id'
    source.headers = {'Content-Type': 'application/json'}
    source._list_sources = MagicMock(return_value=['existing_source_id'])
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_requests_delete.return_value = mock_response
    source.delete_source()
    assert mock_requests_delete.called
    mock_requests_delete.assert_called_with(
        url='http://example.com/account_id/sources/existing_source_id',
        headers={'Content-Type': 'application/json'},
    )


def test_delete_source_unsuccessful(mock_requests_delete):
    source = Source('existing_source_id', 'test_config.toml')
    source.source_id = 'existing_source_id'
    source.endpoint_url = 'http://example.com'
    source.account_id = 'account_id'
    source.headers = {'Content-Type': 'application/xml'}
    source._list_sources = MagicMock(return_value=['existing_source_id'])
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_requests_delete.return_value = mock_response

    with pytest.raises(RuntimeError):
        source.delete_source()

    assert mock_requests_delete.called
    mock_requests_delete.assert_called_with(
        url='http://example.com/account_id/sources/existing_source_id',
        headers={'Content-Type': 'application/xml'},
    )


def test_list_sources_successful(mock_requests_get):
    source = Source('existing_source_id', 'test_config.toml')
    source.endpoint_url = 'http://example.com'
    source.account_id = 'account_id'
    source.headers = {'Content-Type': 'application/xml'}
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = '''<mdm:AccountSources xmlns:mdm="http://example.com/mdm">
                              <mdm:AccountSource>
                                <mdm:sourceId>source1</mdm:sourceId>
                              </mdm:AccountSource>
                              <mdm:AccountSource>
                                <mdm:sourceId>source2</mdm:sourceId>
                              </mdm:AccountSource>
                            </mdm:AccountSources>'''
    mock_requests_get.return_value = mock_response
    source_ids = source._list_sources()
    assert source_ids == ['source1', 'source2']
    assert mock_requests_get.called
    mock_requests_get.assert_called_with(
        url='http://example.com/account_id/sources',
        headers={'Content-Type': 'application/xml'},
    )


def test_list_sources_unsuccessful(mock_requests_get):
    source = Source('existing_source_id', 'test_config.toml')
    source.endpoint_url = 'http://example.com'
    source.account_id = 'account_id'
    source.headers = {'Content-Type': 'application/xml'}
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_requests_get.return_value = mock_response
    with pytest.raises(RuntimeError):
        source._list_sources()
    assert mock_requests_get.called
    mock_requests_get.assert_called_with(
        url='http://example.com/account_id/sources',
        headers={'Content-Type': 'application/xml'},
    )
