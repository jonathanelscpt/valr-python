import pytest
from requests.exceptions import HTTPError

from valr_python.exceptions import APIError
from valr_python.exceptions import APIException
from valr_python.exceptions import IncompleteOrderWarning
from valr_python.exceptions import RequiresAuthentication
from valr_python.exceptions import TooManyRequestsWarning


def test_client_attrs(sync_client):
    sync_client.api_secret = 'api_secret'
    sync_client.api_key = 'api_key'
    sync_client.base_url = 'base_url'
    sync_client.timeout = 10
    sync_client.rate_limiting_support = True

    assert sync_client.api_key == 'api_key'
    assert sync_client.api_secret == 'api_secret'
    assert sync_client.base_url == 'base_url'
    assert sync_client.timeout == 10
    assert sync_client.rate_limiting_support is True


def test_client_do_basic(mock_sync_client, mocker):
    mocker.get('mock://test/', json={"key": "value"}, status_code=200)

    # valid k/v responses
    res = mock_sync_client._do('GET', '/')
    assert res['key'] == 'value'


def test_client_do_authentication_success(mock_sync_client, mocker, mock_resp):
    mocker.get('mock://test/', json=mock_resp)
    mock_sync_client.api_secret = 'api_secret'
    mock_sync_client.api_key = 'api_key'
    resp = mock_sync_client._do('GET', '/', is_authenticated=True)
    assert resp == mock_resp


def test_client_do_authentication_no_key_secret_pair(mock_sync_client, mocker, mock_resp):
    mocker.get('mock://test/', json=mock_resp)
    with pytest.raises(RequiresAuthentication):
        # fail as no api key/secret
        mock_sync_client._do('GET', '/', is_authenticated=True)


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


def test_client_do_warn_on_202_response(mock_sync_client, mocker):
    _202_resp = {"id": "order-id"}
    mocker.get('mock://test/', json=_202_resp, status_code=202)
    with pytest.warns(IncompleteOrderWarning) as w:
        resp = mock_sync_client._do('GET', '/')
        assert resp == _202_resp
        # check that warning bundles expected response data
        assert w[0].message.data == _202_resp


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
    _429_resp = {'status_code': 429, "headers": {"Retry-After": "1"}}
    _200_resp = {'json': {"key": "value"}, "status_code": 200}
    resp_list = [_429_resp, _200_resp]

    # fail without 429 handling flag set
    mocker.get('mock://test/', resp_list)
    with pytest.raises(HTTPError):
        mock_sync_client._do('GET', '/')

    # handle 429s when enabled and validate warning issued
    with pytest.warns(TooManyRequestsWarning):
        mock_sync_client.rate_limiting_support = True
        mocker.get('mock://test/', resp_list)
        res = mock_sync_client._do('GET', '/')
        assert res['key'] == 'value'


@pytest.mark.parametrize('headers', [{}, {"Retry-After": "bogus"}])
def test_client_do_http_429_api_exception_handling(mock_sync_client, mocker, headers):
    mock_sync_client.rate_limiting_support = True

    # raise api exception if header not in response
    mocker.get('mock://test/', headers={}, status_code=429)
    with pytest.raises(APIException):
        mock_sync_client._do('GET', '/')

    # raise api exception if "Retry-After" parsing fails
    mocker.get('mock://test/', headers={"Retry-After": "bogus"}, status_code=429)
    with pytest.raises(APIException):
        mock_sync_client._do('GET', '/')
