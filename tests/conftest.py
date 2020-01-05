import pytest

from valr_python import Client


@pytest.fixture
def test_client():
    """Provides a response object as a fixture"""
    return Client()


@pytest.fixture
def mock_client():
    c = Client()
    c.base_url = 'mock://test/'
    return c
