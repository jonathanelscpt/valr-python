import pytest

from valr_python.base_client import BaseClientABC
from valr_python.exceptions import RequiresAuthentication


BASE_URL = BaseClientABC.DEFAULT_BASE_URL


# Public APIs

def test_sync_get_order_book_public(mocker, sync_client, mock_json_resp, btc_zar):
    mocker.get(f'{BASE_URL}/v1/public/{btc_zar}/orderbook', json=mock_json_resp)
    sdk_resp = sync_client.get_order_book_public(btc_zar)
    assert sdk_resp == mock_json_resp


def test_sync_get_currencies(mocker, sync_client, mock_json_resp):
    mocker.get(f'{BASE_URL}/v1/public/currencies', json=mock_json_resp)
    sdk_resp = sync_client.get_currencies()
    assert sdk_resp == mock_json_resp


def test_sync_get_currency_pairs(mocker, sync_client, mock_json_resp):
    mocker.get(f'{BASE_URL}/v1/public/pairs', json=mock_json_resp)
    sdk_resp = sync_client.get_currency_pairs()
    assert sdk_resp == mock_json_resp


def test_sync_get_order_types(mocker, sync_client, mock_json_resp, btc_zar):
    mocker.get(f'{BASE_URL}/v1/public/ordertypes', json=mock_json_resp)
    sdk_resp_no_currency_pair = sync_client.get_order_types()
    assert sdk_resp_no_currency_pair == mock_json_resp

    mocker.get(f'{BASE_URL}/v1/public/{btc_zar}/ordertypes', json=mock_json_resp)
    sdk_resp = sync_client.get_order_types(currency_pair=btc_zar)
    assert sdk_resp == mock_json_resp


def test_sync_get_market_summary(mocker, sync_client, mock_json_resp, btc_zar):
    mocker.get(f'{BASE_URL}/v1/public/marketsummary', json=mock_json_resp)
    sdk_resp_no_currency_pair = sync_client.get_market_summary()
    assert sdk_resp_no_currency_pair == mock_json_resp

    mocker.get(f'{BASE_URL}/v1/public/{btc_zar}/marketsummary', json=mock_json_resp)
    sdk_resp_no_currency_pair = sync_client.get_market_summary()
    assert sdk_resp_no_currency_pair == mock_json_resp


def test_sync_get_server_time(mocker, sync_client, mock_json_resp):
    mocker.get(f'{BASE_URL}/v1/public/time', json=mock_json_resp)
    sdk_resp = sync_client.get_server_time()
    assert sdk_resp == mock_json_resp


# Account APIs

def test_sync_get_balances(mocker, sync_client, sync_client_with_auth, mock_json_resp):
    mocker.get(f'{BASE_URL}/v1/account/balances', json=mock_json_resp)

    with pytest.raises(RequiresAuthentication):
        sync_client.get_balances()

    sdk_resp = sync_client_with_auth.get_balances()
    assert sdk_resp == mock_json_resp


def test_sync_get_transaction_history(mocker, sync_client, sync_client_with_auth, mock_json_resp):
    skip = 5
    limit = 5
    mocker.get(f'{BASE_URL}/v1/account/transactionhistory?skip={skip}&limit={limit}', json=mock_json_resp)

    with pytest.raises(RequiresAuthentication):
        sync_client.get_transaction_history(skip=skip, limit=limit)

    sdk_resp = sync_client_with_auth.get_transaction_history(skip=skip, limit=limit)
    assert sdk_resp == mock_json_resp


def test_sync_get_account_trade_history(mocker, sync_client, sync_client_with_auth, mock_json_resp, btc_zar):
    limit = 5
    mocker.get(f'{BASE_URL}/v1/account/{btc_zar}/tradehistory?limit={limit}', json=mock_json_resp)

    with pytest.raises(RequiresAuthentication):
        sync_client.get_account_trade_history(currency_pair=btc_zar, limit=limit)

    sdk_resp = sync_client_with_auth.get_account_trade_history(currency_pair=btc_zar, limit=limit)
    assert sdk_resp == mock_json_resp


# Crypto Wallet APIs

def test_sync_get_deposit_address():
    pass


def test_sync_get_withdrawal_info():
    pass


def test_sync_post_new_crypto_withdrawal():
    pass


def test_sync_get_withdrawal_status():
    pass


def test_sync_get_deposit_history():
    pass


def test_sync_get_withdrawal_history():
    pass


# Fiat Wallet APIs

def test_sync_get_bank_accounts():
    pass


def test_sync_post_new_fiat_withdrawal():
    pass


# Market Data APIs

def test_sync_get_order_book():
    pass


def test_sync_get_order_book_full():
    pass


def test_sync_get_market_data_trade_history():
    pass


# Simple Buy/Sell APIs

def test_sync_post_simple_quote():
    pass


def test_sync_post_simple_order():
    pass


def test_sync_get_simple_order_status():
    pass


# Exchange Buy/Sell APIs

def test_sync_post_limit_order():
    pass


def test_sync_post_market_order():
    pass


def test_sync_get_order_status():
    pass


def test_sync_get_all_open_orders():
    pass


def test_sync_get_order_history():
    pass


def test_sync_get_order_history_summary():
    pass


def test_sync_get_order_history_detail():
    pass


def test_sync_delete_order():
    pass

