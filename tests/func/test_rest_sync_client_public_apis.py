from valr_python.rest_base import BaseClientABC

BASE_URL = BaseClientABC.VALR_API_URL


# Public APIs

def test_get_order_book_public(rest_sync_mocker, sync_client, rest_sync_mock_resp, btc_zar):
    rest_sync_mocker.get(f'{BASE_URL}/v1/public/{btc_zar}/orderbook', json=rest_sync_mock_resp)
    sdk_resp = sync_client.get_order_book_public(btc_zar)
    assert sdk_resp == rest_sync_mock_resp


def test_get_currencies(rest_sync_mocker, sync_client, rest_sync_mock_resp):
    rest_sync_mocker.get(f'{BASE_URL}/v1/public/currencies', json=rest_sync_mock_resp)
    sdk_resp = sync_client.get_currencies()
    assert sdk_resp == rest_sync_mock_resp


def test_get_currency_pairs(rest_sync_mocker, sync_client, rest_sync_mock_resp):
    rest_sync_mocker.get(f'{BASE_URL}/v1/public/pairs', json=rest_sync_mock_resp)
    sdk_resp = sync_client.get_currency_pairs()
    assert sdk_resp == rest_sync_mock_resp


def test_get_order_types(rest_sync_mocker, sync_client, rest_sync_mock_resp, btc_zar):
    rest_sync_mocker.get(f'{BASE_URL}/v1/public/ordertypes', json=rest_sync_mock_resp)
    sdk_resp_no_currency_pair = sync_client.get_order_types()
    assert sdk_resp_no_currency_pair == rest_sync_mock_resp

    rest_sync_mocker.get(f'{BASE_URL}/v1/public/{btc_zar}/ordertypes', json=rest_sync_mock_resp)
    sdk_resp = sync_client.get_order_types(currency_pair=btc_zar)
    assert sdk_resp == rest_sync_mock_resp


def test_get_market_summary(rest_sync_mocker, sync_client, rest_sync_mock_resp, btc_zar):
    rest_sync_mocker.get(f'{BASE_URL}/v1/public/marketsummary', json=rest_sync_mock_resp)
    sdk_resp_no_currency_pair = sync_client.get_market_summary()
    assert sdk_resp_no_currency_pair == rest_sync_mock_resp

    rest_sync_mocker.get(f'{BASE_URL}/v1/public/{btc_zar}/marketsummary', json=rest_sync_mock_resp)
    sdk_resp_no_currency_pair = sync_client.get_market_summary()
    assert sdk_resp_no_currency_pair == rest_sync_mock_resp


def test_get_server_time(rest_sync_mocker, sync_client, rest_sync_mock_resp):
    rest_sync_mocker.get(f'{BASE_URL}/v1/public/time', json=rest_sync_mock_resp)
    sdk_resp = sync_client.get_server_time()
    assert sdk_resp == rest_sync_mock_resp
