import pytest
import requests_mock

from valr_python import Client
from valr_python.error import APIError
from valr_python.error import RequiresAuthentication


@pytest.fixture
def mock_client():
    c = Client()
    c.base_url = 'mock://test/'
    return c


def test_client_attrs(mock_client):
    mock_client.api_secret = 'api_secret'
    mock_client.api_key = 'api_key'
    mock_client.base_url = 'base_url'
    mock_client.timeout = 10

    assert mock_client.api_key == 'api_key'
    assert mock_client.api_secret == 'api_secret'
    assert mock_client.base_url == 'base_url'
    assert mock_client.timeout == 10


def test_client_do_authentication(mock_client):

    adapter = requests_mock.Adapter()
    mock_client._session.mount('mock', adapter)
    adapter.register_uri('GET', 'mock://test/', text='{}', status_code=200)

    with pytest.raises(RequiresAuthentication):
        mock_client._do('GET', 'mock://test/', is_authenticated=True)

    # no exceptions, because no error present
    mock_client._do('GET', '/')

    mock_client.api_secret = 'api_secret'
    mock_client.api_key = 'api_key'
    mock_client._do('GET', '/', is_authenticated=True)


def test_client_authentication_error(mock_client):

    with pytest.raises(RequiresAuthentication):
        mock_client.get_balances()


def test_client_do_basic(mock_client):
    adapter = requests_mock.Adapter()
    mock_client._session.mount('mock', adapter)

    adapter.register_uri('GET', 'mock://test/', text='ok')
    with pytest.raises(Exception):
        mock_client._do('GET', '/')

    adapter.register_uri('GET', 'mock://test/', text='{"key":"value"}')
    res = mock_client._do('GET', '/')
    assert res['key'] == 'value'

    adapter.register_uri('GET', 'mock://test/', text='{}', status_code=400)
    mock_client._do('GET', '/')  # no exception, because no error present

    adapter.register_uri('GET', 'mock://test/',
                         text='{"error_code":"code","error":"message"}',
                         status_code=400)
    with pytest.raises(APIError) as e:
        mock_client._do('GET', '/')
    assert e.value.code == 'code'
    assert e.value.message == 'message'
