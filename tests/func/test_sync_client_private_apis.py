import pytest

from valr_python.base_client import BaseClientABC
from valr_python.exceptions import RequiresAuthentication

BASE_URL = BaseClientABC.VALR_API_URL


# Account APIs

def test_get_balances(mocker, sync_client, sync_client_with_auth, mock_json_resp):
    mocker.get(f'{BASE_URL}/v1/account/balances', json=mock_json_resp)

    with pytest.raises(RequiresAuthentication):
        sync_client.get_balances()

    sdk_resp = sync_client_with_auth.get_balances()
    assert sdk_resp == mock_json_resp


def test_get_transaction_history(mocker, sync_client, sync_client_with_auth, mock_json_resp):
    skip = 5
    limit = 5
    mocker.get(f'{BASE_URL}/v1/account/transactionhistory?skip={skip}&limit={limit}', json=mock_json_resp)

    with pytest.raises(RequiresAuthentication):
        sync_client.get_transaction_history(skip=skip, limit=limit)

    sdk_resp = sync_client_with_auth.get_transaction_history(skip=skip, limit=limit)
    assert sdk_resp == mock_json_resp


def test_get_account_trade_history(mocker, sync_client, sync_client_with_auth, mock_json_resp, btc_zar):
    limit = 5
    mocker.get(f'{BASE_URL}/v1/account/{btc_zar}/tradehistory?limit={limit}', json=mock_json_resp)

    with pytest.raises(RequiresAuthentication):
        sync_client.get_account_trade_history(currency_pair=btc_zar, limit=limit)

    sdk_resp = sync_client_with_auth.get_account_trade_history(currency_pair=btc_zar, limit=limit)
    assert sdk_resp == mock_json_resp


# Crypto Wallet APIs

def test_get_deposit_address(mocker, sync_client, sync_client_with_auth, mock_json_resp, btc):
    mocker.get(f'{BASE_URL}/v1/wallet/crypto/{btc}/deposit/address', json=mock_json_resp)

    with pytest.raises(RequiresAuthentication):
        sync_client.get_deposit_address(currency_code=btc)

    sdk_resp = sync_client_with_auth.get_deposit_address(currency_code=btc)
    assert sdk_resp == mock_json_resp


def test_get_withdrawal_info(mocker, sync_client, sync_client_with_auth, mock_json_resp, btc):
    mocker.get(f'{BASE_URL}/v1/wallet/crypto/{btc}/withdraw', json=mock_json_resp)

    with pytest.raises(RequiresAuthentication):
        sync_client.get_withdrawal_info(currency_code=btc)

    sdk_resp = sync_client_with_auth.get_withdrawal_info(currency_code=btc)
    assert sdk_resp == mock_json_resp


def test_post_new_crypto_withdrawal(mocker, sync_client, sync_client_with_auth, mock_json_resp, btc):
    amount = 0.001
    address = 'crypto-address'
    payment_reference = 'payment-ref'
    mocker.post(f'{BASE_URL}/v1/wallet/crypto/{btc}/withdraw', json=mock_json_resp)

    with pytest.raises(RequiresAuthentication):
        sync_client.post_new_crypto_withdrawal(currency_code=btc, amount=amount, address=address,
                                               payment_reference=payment_reference)

    sdk_resp = sync_client_with_auth.post_new_crypto_withdrawal(currency_code=btc, amount=amount, address=address,
                                                                payment_reference=payment_reference)
    assert sdk_resp == mock_json_resp


def test_get_withdrawal_status(mocker, sync_client, sync_client_with_auth, mock_json_resp, btc):
    withdraw_id = 'withdraw_id'
    mocker.get(f'{BASE_URL}/v1/wallet/crypto/{btc}/withdraw/{withdraw_id}', json=mock_json_resp)

    with pytest.raises(RequiresAuthentication):
        sync_client.get_withdrawal_status(currency_code=btc)

    sdk_resp = sync_client_with_auth.get_withdrawal_status(currency_code=btc, withdraw_id=withdraw_id)
    assert sdk_resp == mock_json_resp


def test_get_deposit_history(mocker, sync_client, sync_client_with_auth, mock_json_resp, btc):
    skip = 5
    limit = 5
    mocker.get(f'{BASE_URL}/v1/wallet/crypto/{btc}/deposit/history?skip={skip}&limit={limit}', json=mock_json_resp)

    with pytest.raises(RequiresAuthentication):
        sync_client.get_deposit_history(currency_code=btc, skip=skip, limit=limit)

    sdk_resp = sync_client_with_auth.get_deposit_history(currency_code=btc, skip=skip, limit=limit)
    assert sdk_resp == mock_json_resp


def test_get_withdrawal_history(mocker, sync_client, sync_client_with_auth, mock_json_resp, btc):
    skip = 5
    limit = 5
    mocker.get(f'{BASE_URL}/v1/wallet/crypto/{btc}/withdraw/history?skip={skip}&limit={limit}', json=mock_json_resp)

    with pytest.raises(RequiresAuthentication):
        sync_client.get_withdrawal_history(currency_code=btc, skip=skip, limit=limit)

    sdk_resp = sync_client_with_auth.get_withdrawal_history(currency_code=btc, skip=skip, limit=limit)
    assert sdk_resp == mock_json_resp


# Fiat Wallet APIs

def test_get_bank_accounts(mocker, sync_client, sync_client_with_auth, mock_json_resp, zar):
    mocker.get(f'{BASE_URL}/v1/wallet/fiat/{zar}/accounts', json=mock_json_resp)

    with pytest.raises(RequiresAuthentication):
        sync_client.get_bank_accounts(currency_code=zar)

    sdk_resp = sync_client_with_auth.get_bank_accounts(currency_code=zar)
    assert sdk_resp == mock_json_resp


def test_post_new_fiat_withdrawal(mocker, sync_client, sync_client_with_auth, mock_json_resp, zar):
    linked_bank_account_id = 'linked_bank_account_id'
    amount = 100000.00
    mocker.post(f'{BASE_URL}/v1/wallet/fiat/{zar}/withdraw', json=mock_json_resp)

    with pytest.raises(RequiresAuthentication):
        sync_client.post_new_fiat_withdrawal(currency_code=zar, amount=amount,
                                             linked_bank_account_id=linked_bank_account_id)

    sdk_resp = sync_client_with_auth.post_new_fiat_withdrawal(currency_code=zar, amount=amount,
                                                              linked_bank_account_id=linked_bank_account_id)
    assert sdk_resp == mock_json_resp


# Market Data APIs

def test_get_order_book(mocker, sync_client, sync_client_with_auth, mock_json_resp, btc_zar):
    mocker.get(f'{BASE_URL}/v1/marketdata/{btc_zar}/orderbook', json=mock_json_resp)

    with pytest.raises(RequiresAuthentication):
        sync_client.get_order_book(currency_pair=btc_zar)

    sdk_resp = sync_client_with_auth.get_order_book(currency_pair=btc_zar)
    assert sdk_resp == mock_json_resp


def test_get_order_book_full(mocker, sync_client, sync_client_with_auth, mock_json_resp, btc_zar):
    mocker.get(f'{BASE_URL}/v1/marketdata/{btc_zar}/orderbook/full', json=mock_json_resp)

    with pytest.raises(RequiresAuthentication):
        sync_client.get_order_book_full(currency_pair=btc_zar)

    sdk_resp = sync_client_with_auth.get_order_book_full(currency_pair=btc_zar)
    assert sdk_resp == mock_json_resp


def test_get_market_data_trade_history(mocker, sync_client, sync_client_with_auth, mock_json_resp, btc_zar):
    limit = 5
    mocker.get(f'{BASE_URL}/v1/marketdata/{btc_zar}/tradehistory?limit={limit}', json=mock_json_resp)

    with pytest.raises(RequiresAuthentication):
        sync_client.get_market_data_trade_history(currency_pair=btc_zar, limit=5)

    sdk_resp = sync_client_with_auth.get_market_data_trade_history(currency_pair=btc_zar, limit=5)
    assert sdk_resp == mock_json_resp


# Simple Buy/Sell APIs

def test_post_simple_quote(mocker, sync_client, sync_client_with_auth, mock_json_resp, btc_zar, btc):
    pay_in_currency = btc
    pay_amount = 0.01
    side = "SELL"
    mocker.post(f'{BASE_URL}/v1/simple/{btc_zar}/quote', json=mock_json_resp)

    with pytest.raises(RequiresAuthentication):
        sync_client.post_simple_quote(currency_pair=btc_zar, pay_in_currency=pay_in_currency,
                                      pay_amount=pay_amount, side=side)

    sdk_resp = sync_client_with_auth.post_simple_quote(currency_pair=btc_zar, pay_in_currency=pay_in_currency,
                                                       pay_amount=pay_amount, side=side)
    assert sdk_resp == mock_json_resp


def test_post_simple_order(mocker, sync_client, sync_client_with_auth, mock_json_resp, btc_zar, btc):
    pay_in_currency = btc
    pay_amount = 0.01
    side = "SELL"
    mocker.post(f'{BASE_URL}/v1/simple/{btc_zar}/order', json=mock_json_resp)

    with pytest.raises(RequiresAuthentication):
        sync_client.post_simple_order(currency_pair=btc_zar, pay_in_currency=pay_in_currency,
                                      pay_amount=pay_amount, side=side)

    sdk_resp = sync_client_with_auth.post_simple_order(currency_pair=btc_zar, pay_in_currency=pay_in_currency,
                                                       pay_amount=pay_amount, side=side)
    assert sdk_resp == mock_json_resp


def test_get_simple_order_status(mocker, sync_client, sync_client_with_auth, mock_json_resp, btc_zar):
    order_id = 'order_id'
    mocker.get(f'{BASE_URL}/v1/simple/{btc_zar}/order/{order_id}', json=mock_json_resp)

    with pytest.raises(RequiresAuthentication):
        sync_client.get_simple_order_status(currency_pair=btc_zar, order_id=order_id)

    sdk_resp = sync_client_with_auth.get_simple_order_status(currency_pair=btc_zar, order_id=order_id)
    assert sdk_resp == mock_json_resp


# Exchange Buy/Sell APIs

def test_post_limit_order(mocker, sync_client, sync_client_with_auth, mock_json_resp, btc_zar):
    side = "SELL"
    quantity = 0.100000
    price = 123000
    post_only = True
    customer_order_id = 'customer_order_id'
    mocker.post(f'{BASE_URL}/v1/orders/limit', json=mock_json_resp)

    with pytest.raises(RequiresAuthentication):
        sync_client.post_limit_order(side=side, quantity=quantity, price=price, pair=btc_zar, post_only=post_only,
                                     customer_order_id=customer_order_id)

    sdk_resp = sync_client_with_auth.post_limit_order(side=side, quantity=quantity, price=price, pair=btc_zar,
                                                      post_only=post_only, customer_order_id=customer_order_id)
    assert sdk_resp == mock_json_resp


def test_post_market_order(mocker, sync_client, sync_client_with_auth, mock_json_resp, btc_zar):
    side = "SELL"
    base_amount = 0.100000
    quote_amount = 123000
    customer_order_id = 'customer_order_id'
    mocker.post(f'{BASE_URL}/v1/orders/market', json=mock_json_resp)

    with pytest.raises(RequiresAuthentication):
        sync_client.post_market_order(side=side, pair=btc_zar, base_amount=base_amount,
                                      customer_order_id=customer_order_id)

    with pytest.raises(AttributeError):
        sync_client_with_auth.post_market_order(side=side, pair=btc_zar, base_amount=base_amount,
                                                quote_amount=quote_amount, customer_order_id=customer_order_id)

    sdk_resp = sync_client_with_auth.post_market_order(side=side, pair=btc_zar, base_amount=base_amount,
                                                       customer_order_id=customer_order_id)
    assert sdk_resp == mock_json_resp


def test_get_order_status(mocker, sync_client, sync_client_with_auth, mock_json_resp, btc_zar):
    customer_order_id = "customer_order_id"
    order_id = "order_id"

    mocker.get(f'{BASE_URL}/v1/orders/{btc_zar}/orderid/{order_id}', json=mock_json_resp)

    with pytest.raises(RequiresAuthentication):
        sync_client.get_order_status(currency_pair=btc_zar, order_id=order_id)

    with pytest.raises(AttributeError):
        sync_client_with_auth.get_order_status(currency_pair=btc_zar, order_id=order_id,
                                               customer_order_id=customer_order_id)

    sdk_resp_order_id = sync_client_with_auth.get_order_status(currency_pair=btc_zar, order_id=order_id)
    assert sdk_resp_order_id == mock_json_resp

    mocker.get(f'{BASE_URL}/v1/orders/{btc_zar}/customerorderid/{customer_order_id}', json=mock_json_resp)
    sdk_resp_customer_order_id = sync_client_with_auth.get_order_status(currency_pair=btc_zar,
                                                                        customer_order_id=customer_order_id)
    assert sdk_resp_customer_order_id == mock_json_resp


def test_get_all_open_orders(mocker, sync_client, sync_client_with_auth, mock_json_resp):
    mocker.get(f'{BASE_URL}/v1/orders/open', json=mock_json_resp)

    with pytest.raises(RequiresAuthentication):
        sync_client.get_all_open_orders()

    sdk_resp = sync_client_with_auth.get_all_open_orders()
    assert sdk_resp == mock_json_resp


def test_get_order_history(mocker, sync_client, sync_client_with_auth, mock_json_resp):
    skip = 5
    limit = 5
    mocker.get(f'/v1/orders/history?skip={skip}&limit={limit}', json=mock_json_resp)

    with pytest.raises(RequiresAuthentication):
        sync_client.get_order_history(skip=skip, limit=limit)

    sdk_resp = sync_client_with_auth.get_order_history(skip=skip, limit=limit)
    assert sdk_resp == mock_json_resp


def test_get_order_history_summary(mocker, sync_client, sync_client_with_auth, mock_json_resp):
    customer_order_id = "customer_order_id"
    order_id = "order_id"

    mocker.get(f'{BASE_URL}/v1/orders/history/summary/orderid/{order_id}', json=mock_json_resp)

    with pytest.raises(RequiresAuthentication):
        sync_client.get_order_history_summary(order_id=order_id)

    with pytest.raises(AttributeError):
        sync_client_with_auth.get_order_history_summary(order_id=order_id, customer_order_id=customer_order_id)

    sdk_resp_order_id = sync_client_with_auth.get_order_history_summary(order_id=order_id)
    assert sdk_resp_order_id == mock_json_resp

    mocker.get(f'{BASE_URL}/v1/orders/history/summary/customerorderid/{customer_order_id}', json=mock_json_resp)
    sdk_resp_customer_order_id = sync_client_with_auth.get_order_history_summary(customer_order_id=customer_order_id)
    assert sdk_resp_customer_order_id == mock_json_resp


def test_get_order_history_detail(mocker, sync_client, sync_client_with_auth, mock_json_resp):
    customer_order_id = "customer_order_id"
    order_id = "order_id"

    mocker.get(f'{BASE_URL}/v1/orders/history/detail/orderid/{order_id}', json=mock_json_resp)

    with pytest.raises(RequiresAuthentication):
        sync_client.get_order_history_detail(order_id=order_id)

    with pytest.raises(AttributeError):
        sync_client_with_auth.get_order_history_detail(order_id=order_id, customer_order_id=customer_order_id)

    sdk_resp_order_id = sync_client_with_auth.get_order_history_detail(order_id=order_id)
    assert sdk_resp_order_id == mock_json_resp

    mocker.get(f'{BASE_URL}/v1/orders/history/detail/customerorderid/{customer_order_id}', json=mock_json_resp)
    sdk_resp_customer_order_id = sync_client_with_auth.get_order_history_detail(customer_order_id=customer_order_id)
    assert sdk_resp_customer_order_id == mock_json_resp


def test_delete_order(mocker, sync_client, sync_client_with_auth, mock_json_resp, btc_zar):
    customer_order_id = "customer_order_id"
    order_id = "order_id"

    mocker.delete(f'{BASE_URL}/v1/orders/order', json=mock_json_resp)

    with pytest.raises(RequiresAuthentication):
        sync_client.delete_order(pair=btc_zar, order_id=order_id)

    with pytest.raises(AttributeError):
        sync_client_with_auth.delete_order(pair=btc_zar, order_id=order_id, customer_order_id=customer_order_id)

    sdk_resp_order_id = sync_client_with_auth.delete_order(pair=btc_zar, order_id=order_id)
    assert sdk_resp_order_id == mock_json_resp

    sdk_resp_customer_order_id = sync_client_with_auth.delete_order(pair=btc_zar, customer_order_id=customer_order_id)
    assert sdk_resp_customer_order_id == mock_json_resp
