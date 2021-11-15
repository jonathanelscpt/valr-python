from datetime import datetime
from datetime import timedelta
from time import sleep

LIVE_API_TIMEOUT = 4


def teardown_function(function):
    """Add timeout between live public api calls to avoid HTTP 429 rate-limiting"""
    sleep(LIVE_API_TIMEOUT)


def test_live_get_order_book_public(sync_client, btc_zar):
    resp = sync_client.get_order_book_public(currency_pair=btc_zar)
    assert isinstance(resp, dict)
    assert 'Asks' in resp and 'Bids' in resp
    assert isinstance(resp['Asks'], list) and isinstance(resp['Bids'], list)


def test_get_order_book_full_public(sync_client, btc_zar):
    resp = sync_client.get_order_book_full_public(currency_pair=btc_zar)
    assert isinstance(resp, dict)
    assert 'Asks' in resp and 'Bids' in resp
    assert isinstance(resp['Asks'], list) and isinstance(resp['Bids'], list)


def test_live_get_currencies(sync_client):
    resp = sync_client.get_currencies()
    assert isinstance(resp, list)
    assert isinstance(resp[0], dict)


def test_live_get_currency_pairs(sync_client):
    resp = sync_client.get_currency_pairs()
    assert isinstance(resp, list)
    assert isinstance(resp[0], dict)


def test_live_get_order_types_no_currency_pair(sync_client):
    resp = sync_client.get_order_types()
    assert isinstance(resp, list)
    assert isinstance(resp[0], dict)


def test_live_get_order_types_with_currency_pair(sync_client, btc_zar):
    resp = sync_client.get_order_types(currency_pair=btc_zar)
    assert isinstance(resp, list)
    assert isinstance(resp[0], str)


def test_live_get_market_summary_no_currency_pair(sync_client):
    resp = sync_client.get_market_summary()
    assert isinstance(resp, list)
    assert isinstance(resp[0], dict)


def test_live_get_market_summary_with_currency_pair(sync_client, btc_zar):
    resp = sync_client.get_market_summary(currency_pair=btc_zar)
    assert isinstance(resp, dict)


def test_live_get_trade_history_public(sync_client, btc_zar):
    skip = 0
    limit = 5
    resp = sync_client.get_trade_history_public(currency_pair=btc_zar, skip=skip, limit=limit)
    assert isinstance(resp, list)


def test_live_get_trade_history_public_filtered(sync_client, btc_zar):
    skip = 0
    limit = 5
    start_time = (datetime.now() - timedelta(seconds=15000)).strftime('%Y-%m-%dT%H:%M:%SZ')
    end_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    resp = sync_client.get_trade_history_public(currency_pair=btc_zar, skip=skip, limit=limit, start_time=start_time,
                                                end_time=end_time)
    assert isinstance(resp, list)


def test_live_get_trade_history_public_paginated(sync_client, btc_zar):
    limit = 5
    before_id = sync_client.get_trade_history_public(currency_pair=btc_zar, limit=limit)[0]['id']
    resp = sync_client.get_trade_history_public(currency_pair=btc_zar, limit=limit, before_id=before_id)
    assert isinstance(resp, list)


def test_live_get_server_time(sync_client):
    resp = sync_client.get_server_time()
    assert isinstance(resp, dict)


def test_live_get_valr_status(sync_client):
    resp = sync_client.get_valr_status()
    assert isinstance(resp, dict)
