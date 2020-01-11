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
        mock_sync_client._do('GET', '/', is_authenticated=True)

    # no exceptions, because no error present
    mock_sync_client._do('GET', '/')

    mock_sync_client.api_secret = 'api_secret'
    mock_sync_client.api_key = 'api_key'
    resp = mock_sync_client._do('GET', '/', is_authenticated=True)
    assert resp == mock_json_resp


def test_client_do_basic(mock_sync_client, mocker):
    mocker.get('mock://test/', json={"key": "value"}, status_code=200)

    # valid k/v responses
    res = mock_sync_client._do('GET', '/')
    assert res['key'] == 'value'


def test_client_do_api_error_handling(mock_sync_client, mocker):
    mocker.get('mock://test/', json={"code": "-12345", "message": "api error message"}, status_code=400)
    with pytest.raises(APIError) as e:
        mock_sync_client._do('GET', '/')
    assert e.value.code == '-12345'
    assert e.value.message == 'api error message'


def test_client_do_200_ok_error_handling(mock_sync_client, mocker):
    mocker.get('mock://test/', json={"code": "-12345", "message": "api error message"}, status_code=200)
    with pytest.raises(APIError) as e:
        mock_sync_client._do('GET', '/')
    assert e.value.code == '-12345'
    assert e.value.message == 'api error message'


def test_client_do_invalid_response_handling(mock_sync_client, mocker):
    mocker.get('mock://test/', text='invalid json response')
    with pytest.raises(APIException):
        mock_sync_client._do('GET', '/')


def test_client_do_http_error_handling(mock_sync_client, mocker):
    # HTTP errors without VALR api handling
    mocker.get('mock://test/', json={'error': 'Internal Server Error'}, status_code=500)
    with pytest.raises(HTTPError):
        mock_sync_client._do('GET', '/')


def test_client_do_http_429_handling(mock_sync_client, mocker):
    _429_response = {'status_code': 429, "headers": {"Retry-After": "1"}}
    _200_ok_resp = {'json': {"key": "value"}, "status_code": 200}
    resp_list = [_429_response, _200_ok_resp]

    # fail without 429 handling flag set
    mocker.get('mock://test/', resp_list)
    with pytest.raises(HTTPError):
        mock_sync_client._do('GET', '/')

    # handle 429s when enabled
    mock_sync_client.handle_429_errors = True
    mocker.get('mock://test/', resp_list)
    res = mock_sync_client._do('GET', '/')
    assert res['key'] == 'value'


@pytest.mark.parametrize('headers', [{}, {"Retry-After": "bogus"}])
def test_client_do_http_429_api_exception_handling(mock_sync_client, mocker, headers):
    mock_sync_client.handle_429_errors = True

    # raise api exception if header not in response
    mocker.get('mock://test/', headers={}, status_code=429)
    with pytest.raises(APIException):
        mock_sync_client._do('GET', '/')

    # raise api exception if "Retry-After" parsing fails
    mocker.get('mock://test/', headers={"Retry-After": "bogus"}, status_code=429)
    with pytest.raises(APIException):
        mock_sync_client._do('GET', '/')
