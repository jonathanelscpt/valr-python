from valr_python.base_client import BaseClientABC

BASE_URL = BaseClientABC.VALR_API_URL


# Public APIs

def test_get_order_book_public(mocker, sync_client, mock_resp, btc_zar):
    mocker.get(f'{BASE_URL}/v1/public/{btc_zar}/orderbook', json=mock_resp)
    sdk_resp = sync_client.get_order_book_public(btc_zar)
    assert sdk_resp == mock_resp


def test_get_currencies(mocker, sync_client, mock_resp):
    mocker.get(f'{BASE_URL}/v1/public/currencies', json=mock_resp)
    sdk_resp = sync_client.get_currencies()
    assert sdk_resp == mock_resp


def test_get_currency_pairs(mocker, sync_client, mock_resp):
    mocker.get(f'{BASE_URL}/v1/public/pairs', json=mock_resp)
    sdk_resp = sync_client.get_currency_pairs()
    assert sdk_resp == mock_resp


def test_get_order_types(mocker, sync_client, mock_resp, btc_zar):
    mocker.get(f'{BASE_URL}/v1/public/ordertypes', json=mock_resp)
    sdk_resp_no_currency_pair = sync_client.get_order_types()
    assert sdk_resp_no_currency_pair == mock_resp

    mocker.get(f'{BASE_URL}/v1/public/{btc_zar}/ordertypes', json=mock_resp)
    sdk_resp = sync_client.get_order_types(currency_pair=btc_zar)
    assert sdk_resp == mock_resp


def test_get_market_summary(mocker, sync_client, mock_resp, btc_zar):
    mocker.get(f'{BASE_URL}/v1/public/marketsummary', json=mock_resp)
    sdk_resp_no_currency_pair = sync_client.get_market_summary()
    assert sdk_resp_no_currency_pair == mock_resp

    mocker.get(f'{BASE_URL}/v1/public/{btc_zar}/marketsummary', json=mock_resp)
    sdk_resp_no_currency_pair = sync_client.get_market_summary()
    assert sdk_resp_no_currency_pair == mock_resp


def test_get_server_time(mocker, sync_client, mock_resp):
    mocker.get(f'{BASE_URL}/v1/public/time', json=mock_resp)
    sdk_resp = sync_client.get_server_time()
    assert sdk_resp == mock_resp
