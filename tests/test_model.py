import io
import tempfile

import pytest
from unittest.mock import Mock, patch, MagicMock
from cicd.resources.model import Model

@pytest.fixture
def mock_requests_post():
    with patch('cicd.resources.model.requests.post') as mock_post:
        yield mock_post

@pytest.fixture
def mock_open():
    with patch('builtins.open') as mocked_open:
        yield mocked_open
@pytest.fixture
def mock_create_source_xml_data():
    mock_create_source_xml_data = """<mdm:CreateModelRequest xmlns:mdm="http://mdm.api.platform.boomi.com/" 
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            <mdm:name>newModel</mdm:name>
            <mdm:fields>
                <mdm:field name="field1" repeatable="false" required="true" type="STRING"
                           uniqueId="FIELD1" minLength="1" maxLength="100"/>
            </mdm:fields>
            </mdm:CreateModelRequest>"""

    return  mock_create_source_xml_data

def test_create_model_success(mock_requests_post, mock_create_source_xml_data):
    model = Model('newModel', 'test_config.toml')
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
        temp_file.write(mock_create_source_xml_data)
    model.file_name = temp_file
    model.endpoint_url = 'http://example.com'
    model.account_id = 'account_id'
    model.headers = {'Content-Type': 'application/xml'}

    with patch('builtins.open', return_value=io.BytesIO(mock_create_source_xml_data.encode())):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_requests_post.return_value = mock_response
        model.create_model()
        assert mock_requests_post.called
        mock_requests_post.assert_called_with(
            url='http://example.com/account_id/models',
            headers={'Content-Type': 'application/xml'},
            data=mock_create_source_xml_data,
        )


