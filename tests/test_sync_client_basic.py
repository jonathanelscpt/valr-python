import pytest
from requests.exceptions import HTTPError

from valr_python.exceptions import APIError
from valr_python.exceptions import APIException
from valr_python.exceptions import RequiresAuthentication


def test_client_attrs(sync_client):
    sync_client.api_secret = 'api_secret'
    sync_client.api_key = 'api_key'
    sync_client.base_url = 'base_url'
    sync_client.timeout = 10

    assert sync_client.api_key == 'api_key'
    assert sync_client.api_secret == 'api_secret'
    assert sync_client.base_url == 'base_url'
    assert sync_client.timeout == 10


def test_client_do_authentication(mock_sync_client, mocker, mock_json_resp):

    mocker.get('mock://test/', json=mock_json_resp)

    with pytest.raises(RequiresAuthentication):
        # fail as no api key/secret
        mock_sync_client._do('GET', 'mock://test/', is_authenticated=True)

    # no exceptions, because no error present
    mock_sync_client._do('GET', '/')

    mock_sync_client.api_secret = 'api_secret'
    mock_sync_client.api_key = 'api_key'
    mock_sync_client._do('GET', '/', is_authenticated=True)


def test_client_do_basic(mock_sync_client, mocker):
    mocker.get('mock://test/', json={"key": "value"}, status_code=200)

    # valid k/v responses
    res = mock_sync_client._do('GET', '/')
    assert res['key'] == 'value'


def test_client_do_errors(mock_sync_client, mocker):
    # api error handling for HTTP errors
    mocker.get('mock://test/', json={"code": "-12345", "message": "api error message"}, status_code=400)
    with pytest.raises(APIError) as e:
        mock_sync_client._do('GET', '/')
    assert e.value.code == '-12345'
    assert e.value.message == 'api error message'

    # api error handling for 200 OK cases
    mocker.get('mock://test/', json={"code": "-12345", "message": "api error message"}, status_code=200)
    with pytest.raises(APIError) as e:
        mock_sync_client._do('GET', '/')
    assert e.value.code == '-12345'
    assert e.value.message == 'api error message'

    # invalid responses exception handling
    mocker.get('mock://test/', text='invalid json response')
    with pytest.raises(APIException):
        mock_sync_client._do('GET', '/')

    # HTTP errors without VALR api handling
    mocker.get('mock://test/', json={'error': 'Internal Server Error'}, status_code=500)
    with pytest.raises(HTTPError):
        mock_sync_client._do('GET', '/')
