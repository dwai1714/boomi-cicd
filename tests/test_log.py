from __future__ import annotations

import logging
import os
from pathlib import Path
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from cicd.utils.log import configure_logging
from cicd.utils.log import get_logger


@pytest.mark.parametrize(
    'log_level, expected_format', [

        ('DEBUG', '%(asctime)s %(levelname)s %(name)s[%(lineno)s] %(funcName)s: %(message)s'),
        ('INFO', '%(asctime)s %(levelname)s %(name)s: %(message)s'),

    ],
)
def test_configure_logging(log_level, expected_format):
    # Set LOG_LEVEL environment variable using monkeypatch
    os.environ['LOG_LEVEL'] = log_level

    # Call configure_logging function
    logging_lvel, log_format = configure_logging()
    print('Here now ', log_level, log_format)
    # assert True
    # Assert that the returned format matches the expected format
    assert log_format == expected_format


# Mock settings for testing
SETTINGS = {
    'default': {
        'LOG_FILE_LOCATION': '/tmp/',
        'LOG_FILE_NAME': 'test.log',
    },
}


# Test get_logger function
@pytest.mark.parametrize(
    'log_level, handler', [

        ('DEBUG', ''),
        ('DEBUG', 'logging.StreamHandler()'),
        ('INFO', ''),
        ('INFO', 'logging.StreamHandler()'),

    ],
)
def test_get_logger(log_level, handler):
    os.environ['LOG_LEVEL'] = log_level

    # Mock logging functions and objects
    mock_logger = MagicMock(spec=logging.Logger)
    if handler == '':
        mock_logger.handlers = []
    else:
        mock_logger.handlers = [logging.StreamHandler()]

    mock_getLogger = MagicMock(return_value=mock_logger)
    mock_path = MagicMock(spec=Path)
    mock_path.return_value.mkdir.return_value = None
    mock_path.return_value.__truediv__.return_value = '/tmp/test.log'
    mock_stream_handler = MagicMock(spec=logging.StreamHandler)
    mock_formatter = MagicMock(spec=logging.Formatter)

    logger = get_logger(name='test_name')

    # Assertions

    # Patch necessary functions and objects
    with patch.dict('cicd.utils.log.settings', SETTINGS), \
            patch('cicd.utils.log.logging.getLogger', mock_getLogger), \
            patch('cicd.utils.log.Path', mock_path), \
            patch('cicd.utils.log.logging.StreamHandler', MagicMock(return_value=mock_stream_handler)), \
            patch('cicd.utils.log.logging.Formatter', MagicMock(return_value=mock_formatter)):

        # Call get_logger function
        logger = get_logger(name='test_name')

        # Assertions
        assert logger is mock_logger
        if handler == '':
            mock_logger.setLevel.assert_called_once_with(log_level)
            mock_logger.addHandler.assert_called_once_with(mock_stream_handler)
