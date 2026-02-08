import pytest
from unittest.mock import patch, mock_open, MagicMock

@pytest.fixture
def mock_file_content():
    """Fixture to mock file reading with custom content."""
    def _mock(content, encoding='utf-8'):
        m = mock_open(read_data=content)
        return m
    return _mock

@pytest.fixture
def mock_chardet():
    """Mock chardet.detect to return a specific encoding."""
    with patch('chardet.detect') as mock_detect:
        yield mock_detect

@pytest.fixture
def mock_translator():
    """Mock deep_translator.GoogleTranslator used in translators.py."""
    with patch('srt_translator.translators.GoogleTranslator') as mock_trans:
        yield mock_trans

@pytest.fixture
def mock_tqdm():
    """Mock tqdm to avoid progress bar in tests."""
    with patch('tqdm.tqdm') as mock_prog:
        mock_prog.return_value = lambda x, **kwargs: x  # Just iterate without progress
        yield mock_prog
