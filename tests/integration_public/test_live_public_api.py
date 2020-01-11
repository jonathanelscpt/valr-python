from time import sleep

LIVE_API_TIMEOUT = 4


def setup_function(function):
    """ setup any state tied to the execution of the given function.
    Invoked for every test function in the module.
    """
    pass


def teardown_function(function):
    """Add timeout between live public api calls to avoid HTTP 429 rate-limiting"""
    sleep(LIVE_API_TIMEOUT)


def test_live_get_order_book_public(sync_client, btc_zar):
    resp = sync_client.get_order_book_public(currency_pair=btc_zar)
    assert type(resp) is dict
    assert 'Asks' in resp and 'Bids' in resp
    assert type(resp['Asks']) is list and type(resp['Bids'])


def test_live_get_currencies(sync_client):
    resp = sync_client.get_currencies()
    assert type(resp) is list
    assert type(resp[0]) is dict


def test_live_get_currency_pairs(sync_client):
    resp = sync_client.get_currency_pairs()
    assert type(resp) is list
    assert type(resp[0]) is dict


def test_live_get_order_types_no_currency_pair(sync_client):
    resp = sync_client.get_order_types()
    assert type(resp) is list
    assert type(resp[0]) is dict


def test_live_get_order_types_with_currency_pair(sync_client, btc_zar):
    resp = sync_client.get_order_types(currency_pair=btc_zar)
    assert type(resp) is list
    assert type(resp[0]) is str


def test_live_get_market_summary_no_currency_pair(sync_client):
    resp = sync_client.get_market_summary()
    assert type(resp) is list
    assert type(resp[0]) is dict


def test_live_get_market_summary_with_currency_pair(sync_client, btc_zar):
    resp = sync_client.get_market_summary(currency_pair=btc_zar)
    assert type(resp) is dict


def test_live_get_server_time(sync_client):
    resp = sync_client.get_server_time()
    assert type(resp) is dict
