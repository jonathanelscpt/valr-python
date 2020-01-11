import json


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
    signature = sync_client._sign_request(timestamp=timestamp, method=method, path=path, body=body)
    assert signature == '862ab6527f1ec72bb2243e5f01ae66515d0e74ef1e36aa68c031c045df1b3b62bd43858642a8425368895354e360715add8e3aec47432ea69f60bf6cbd546ea5'  # noqa


def test_request_signature_empty_body(sync_client):
    sync_client.api_secret = 'superdupersecret'
    timestamp = 1577572690093
    method = 'GET'
    path = '/v1/account/balances'
    body = ''
    signature = sync_client._sign_request(timestamp=timestamp, method=method, path=path, body=body)
    assert signature == '647d276537b952fe37f349422a4a60a76ecc2e3fad509a523b03dccd1a940525f8ff06314ad1adc5625000223c514637cd9682ee89ffc285b7493e7c64e746aa'  # noqa
