import json

from valr_python.utils import _sign_request


def test_request_signature_basic(sync_client):
    sync_client.api_secret = 'superdupersecret'
    timestamp = 1577572690093
    method = 'DELETE'
    path = '/v1/orders/order'
    data = {
        "orderId": "UUID",
        "pair": "BTCZAR"
    }
    body = json.loads(json.dumps(data))
    signature = _sign_request(api_secret=sync_client.api_secret, timestamp=timestamp,
                              method=method, path=path, body=body)
    assert signature == '862ab6527f1ec72bb2243e5f01ae66515d0e74ef1e36aa68c031c045df1b3b62bd43858642a8425368895354e360715add8e3aec47432ea69f60bf6cbd546ea5'  # noqa


def test_request_signature_empty_body(sync_client):
    sync_client.api_secret = 'superdupersecret'
    timestamp = 1577572690093
    method = 'GET'
    path = '/v1/account/balances'
    body = ''
    signature = _sign_request(api_secret=sync_client.api_secret, timestamp=timestamp,
                              method=method, path=path, body=body)
    assert signature == '647d276537b952fe37f349422a4a60a76ecc2e3fad509a523b03dccd1a940525f8ff06314ad1adc5625000223c514637cd9682ee89ffc285b7493e7c64e746aa'  # noqa


def test_request_signature_subaccount(sync_client, subaccount_id):
    sync_client.api_secret = 'superdupersecret'
    timestamp = 1577572690093
    method = 'GET'
    path = '/v1/account/balances'
    body = ''
    signature = _sign_request(api_secret=sync_client.api_secret, timestamp=timestamp,
                              method=method, path=path, body=body, subaccount_id=subaccount_id)
    assert signature == '3dc9ed14dbb13f9c529bd75241686523ca1e77fcbe0184ca35fe8d5329692e5e26a3b3d7ff339dce6e829d3b1c93ef9e187cf696c07ef12517198950ea68af0f'  # noqa


def test_request_signature_empty_subaccount(sync_client):
    sync_client.api_secret = 'superdupersecret'
    timestamp = 1577572690093
    method = 'GET'
    path = '/v1/account/balances'
    body = ''
    subaccount = ''
    signature = _sign_request(api_secret=sync_client.api_secret, timestamp=timestamp,
                              method=method, path=path, body=body, subaccount_id=subaccount)
    assert signature == '647d276537b952fe37f349422a4a60a76ecc2e3fad509a523b03dccd1a940525f8ff06314ad1adc5625000223c514637cd9682ee89ffc285b7493e7c64e746aa'  # noqa
