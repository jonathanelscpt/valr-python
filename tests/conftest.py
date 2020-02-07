import pytest
import requests_mock

from valr_python import RestClient
from valr_python import WebSocketClient
from valr_python.enum import TradeEvent

@pytest.fixture
def sync_client():
    return RestClient()


@pytest.fixture
def sync_client_with_auth():
    return RestClient(api_key='api_key', api_secret='api_secret')


@pytest.fixture
def mock_sync_client(sync_client):
    sync_client.base_url = 'mock://test/'
    return sync_client


@pytest.fixture
def rest_sync_mocker():
    with requests_mock.Mocker() as m:
        yield m


@pytest.fixture
def rest_sync_mock_resp():
    return {}


@pytest.fixture
def btc_zar():
    return 'BTCZAR'


@pytest.fixture
def btc():
    return 'BTC'


@pytest.fixture
def zar():
    return 'ZAR'
