import pytest
import requests_mock

from valr_python.base_client import _sign_request  # noqa
from valr_python.client import Client
from valr_python.error import APIError
from valr_python.error import RequiresAuthentication


@pytest.fixture
def client():
    c = Client()
    c.base_url = 'mock://test/'
    return c


def test_client(client):
    client.api_secret = 'api_secret'
    client.api_key = 'api_key'
    client.base_url = 'base_url'
    client.timeout = 10

    assert client.api_key == 'api_key'
    assert client.api_secret == 'api_secret'
    assert client.base_url == 'base_url'
    assert client.timeout == 10


def test_client_authentication(client):

    adapter = requests_mock.Adapter()
    client._session.mount('mock', adapter)
    adapter.register_uri('GET', 'mock://test/', text='{}', status_code=200)

    with pytest.raises(RequiresAuthentication):
        client._do('GET', 'mock://test/', is_authenticated=True)

    # no exceptions, because no error present
    client._do('GET', '/')

    client.api_secret = 'api_secret'
    client.api_key = 'api_key'
    client._do('GET', '/', is_authenticated=True)


def test_client_do_basic(client):
    adapter = requests_mock.Adapter()
    client._session.mount('mock', adapter)

    adapter.register_uri('GET', 'mock://test/', text='ok')
    with pytest.raises(Exception):
        res = client._do('GET', '/')

    adapter.register_uri('GET', 'mock://test/', text='{"key":"value"}')
    res = client._do('GET', '/')
    assert res['key'] == 'value'

    adapter.register_uri('GET', 'mock://test/', text='{}', status_code=400)
    res = client._do('GET', '/')  # no exception, because no error present

    adapter.register_uri('GET', 'mock://test/',
                         text='{"error_code":"code","error":"message"}',
                         status_code=400)
    with pytest.raises(APIError) as e:
        res = client._do('GET', '/')
    assert e.value.code == 'code'
    assert e.value.message == 'message'


def test_request_signature_basic():
    api_secret = 'b9fb68df5485639d03c3171cf6e49b89e52fd78d5c313819b9c592b59c689f33'
    timestamp = 1577572690093
    method = 'GET'
    path = '/v1/account/balances'
    body = ''
    signature = _sign_request(api_secret=api_secret, timestamp=timestamp, method=method, path=path, body=body)
    assert signature == 'caf54b16a73d87a3dd7ac89edbfda5191db7847843a6c0839a2a482716c3be6e5af2b3fc5f442957a62747f4651c3b07931f9fad3866529c45e356e50e9c2cba'  # noqa
