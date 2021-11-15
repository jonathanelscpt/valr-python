from decimal import Decimal

import pytest

from valr_python.exceptions import RequiresAuthentication
from valr_python.rest_base import BaseClientABC

BASE_URL = BaseClientABC._REST_API_URL


# Account APIs - API Keys

def test_get_current_api_key_info(rest_sync_mocker, sync_client, sync_client_with_auth, rest_sync_mock_resp, subaccount_id):
    rest_sync_mocker.get(f'{BASE_URL}/v1/account/api-keys/current', json=rest_sync_mock_resp)

    with pytest.raises(RequiresAuthentication):
        sync_client.get_current_api_key_info()

    sdk_resp = sync_client_with_auth.get_current_api_key_info()
    assert sdk_resp == rest_sync_mock_resp

    # subaccount_id must be supported
    try:
        sync_client_with_auth.get_current_api_key_info(subaccount_id=subaccount_id)
    except Exception:
        assert False, "Exception incorrectly raised when using subaccount_id"


# Account APIs - Sub-accounts

def test_get_subaccounts(rest_sync_mocker, sync_client, sync_client_with_auth, rest_sync_mock_resp, subaccount_id):
    rest_sync_mocker.get(f'{BASE_URL}/v1/account/subaccounts', json=rest_sync_mock_resp)

    with pytest.raises(RequiresAuthentication):
        sync_client.get_subaccounts()

    sdk_resp = sync_client_with_auth.get_subaccounts()
    assert sdk_resp == rest_sync_mock_resp

    # method must not support subaccount_id
    with pytest.raises(TypeError):
        sync_client_with_auth.get_subaccounts(subaccount_id=subaccount_id)


def test_get_nonzero_balances(rest_sync_mocker, sync_client, sync_client_with_auth, rest_sync_mock_resp, subaccount_id):
    rest_sync_mocker.get(f'{BASE_URL}/v1/account/balances/all', json=rest_sync_mock_resp)

    with pytest.raises(RequiresAuthentication):
        sync_client.get_nonzero_balances()

    sdk_resp = sync_client_with_auth.get_nonzero_balances()
    assert sdk_resp == rest_sync_mock_resp

    # method must not support subaccount_id
    with pytest.raises(TypeError):
        sync_client_with_auth.get_nonzero_balances(subaccount_id=subaccount_id)


def test_register_subaccount(rest_sync_mocker, sync_client, sync_client_with_auth, rest_sync_mock_resp, subaccount_id):
    label = 'label'
    rest_sync_mocker.post(f'{BASE_URL}/v1/account/subaccount', json=rest_sync_mock_resp)

    with pytest.raises(RequiresAuthentication):
        sync_client.register_subaccount(label=label)

    sdk_resp = sync_client_with_auth.register_subaccount(label=label)
    assert sdk_resp == rest_sync_mock_resp

    # method must not support subaccount_id
    with pytest.raises(TypeError):
        sync_client_with_auth.register_subaccount(label=label, subaccount_id=subaccount_id)


def test_post_internal_transfer_subaccounts(rest_sync_mocker, sync_client, sync_client_with_auth, rest_sync_mock_resp,
                                            zar, subaccount_id):
    from_id = subaccount_id
    to_id = '0'
    currency_code = zar
    amount = Decimal('200000.00')
    rest_sync_mocker.post(f'{BASE_URL}/v1/account/subaccounts/transfer', json=rest_sync_mock_resp)

    with pytest.raises(RequiresAuthentication):
        sync_client.post_internal_transfer_subaccounts(from_id=from_id, to_id=to_id,
                                                       currency_code=currency_code, amount=amount)

    sdk_resp = sync_client_with_auth.post_internal_transfer_subaccounts(from_id=from_id, to_id=to_id,
                                                                        currency_code=currency_code, amount=amount)
    assert sdk_resp == rest_sync_mock_resp

    # subaccount_id must be supported
    try:
        sync_client_with_auth.post_internal_transfer_subaccounts(from_id=from_id, to_id=to_id,
                                                                 currency_code=currency_code, amount=amount,
                                                                 subaccount_id=subaccount_id)
    except Exception:
        assert False, "Exception incorrectly raised when using subaccount_id"


# Account APIs - General

def test_get_balances(rest_sync_mocker, sync_client, sync_client_with_auth, rest_sync_mock_resp, subaccount_id):
    rest_sync_mocker.get(f'{BASE_URL}/v1/account/balances', json=rest_sync_mock_resp)

    with pytest.raises(RequiresAuthentication):
        sync_client.get_balances()

    sdk_resp = sync_client_with_auth.get_balances()
    assert sdk_resp == rest_sync_mock_resp

    # subaccount_id must be supported
    try:
        sync_client_with_auth.get_balances(subaccount_id=subaccount_id)
    except Exception:
        assert False, "Exception incorrectly raised when using subaccount_id"


def test_get_transaction_history(rest_sync_mocker, sync_client, sync_client_with_auth, rest_sync_mock_resp,
                                 subaccount_id, zar):
    skip = 0
    limit = 100
    transaction_types_single = 'LIMIT_BUY'
    transaction_types_str_list = 'LIMIT_BUY,MARKET_BUY'
    transaction_types_list = ['LIMIT_BUY', 'MARKET_BUY']
    currency = zar
    start_time = '2020-02-29T22:00:00.000Z'
    end_time = '2021-04-30T21:59:59.999Z'
    before_id = '22861141-62a7-49e2-8d3f-acbaf14dd4ba'

    rest_sync_mocker.get(f'{BASE_URL}/v1/account/transactionhistory', json=rest_sync_mock_resp)

    with pytest.raises(RequiresAuthentication):
        sync_client.get_transaction_history(skip=skip, limit=limit)

    sdk_resp_basic = sync_client_with_auth.get_transaction_history()
    assert sdk_resp_basic == rest_sync_mock_resp

    sdk_resp_with_basic_params = sync_client_with_auth.get_transaction_history(skip=skip, limit=limit)
    assert sdk_resp_with_basic_params == rest_sync_mock_resp

    sdk_resp_filters_basic = sync_client_with_auth.get_transaction_history(transaction_types=transaction_types_single,
                                                                           currency=currency, start_time=start_time,
                                                                           end_time=end_time)
    assert sdk_resp_filters_basic == rest_sync_mock_resp

    sdk_resp_filters_str_list = sync_client_with_auth.get_transaction_history(transaction_types=transaction_types_str_list,  # noqa
                                                                              currency=currency, start_time=start_time,
                                                                              end_time=end_time)
    assert sdk_resp_filters_str_list == rest_sync_mock_resp

    sdk_resp_filters_list = sync_client_with_auth.get_transaction_history(transaction_types=transaction_types_list,
                                                                          currency=currency, start_time=start_time,
                                                                          end_time=end_time)
    assert sdk_resp_filters_list == rest_sync_mock_resp

    sdk_resp_paginated = sync_client_with_auth.get_transaction_history(limit=limit, before_id=before_id)
    assert sdk_resp_paginated == rest_sync_mock_resp

    # subaccount_id must be supported
    try:
        sync_client_with_auth.get_transaction_history(subaccount_id=subaccount_id)
    except Exception:
        assert False, "Exception incorrectly raised when using subaccount_id"


def test_get_trade_history(rest_sync_mocker, sync_client, sync_client_with_auth, rest_sync_mock_resp, btc_zar,
                           subaccount_id):
    limit = 5
    rest_sync_mocker.get(f'{BASE_URL}/v1/account/{btc_zar}/tradehistory', json=rest_sync_mock_resp)

    with pytest.raises(RequiresAuthentication):
        sync_client.get_trade_history(currency_pair=btc_zar, limit=limit)

    sdk_resp = sync_client_with_auth.get_trade_history(currency_pair=btc_zar, limit=limit)
    assert sdk_resp == rest_sync_mock_resp

    # subaccount_id must be supported
    try:
        sync_client_with_auth.get_trade_history(currency_pair=btc_zar, limit=limit, subaccount_id=subaccount_id)
    except Exception:
        assert False, "Exception incorrectly raised when using subaccount_id"


# Wallets - Crypto

def test_get_deposit_address(rest_sync_mocker, sync_client, sync_client_with_auth, rest_sync_mock_resp, btc,
                             subaccount_id):
    rest_sync_mocker.get(f'{BASE_URL}/v1/wallet/crypto/{btc}/deposit/address', json=rest_sync_mock_resp)

    with pytest.raises(RequiresAuthentication):
        sync_client.get_deposit_address(currency_code=btc)

    sdk_resp = sync_client_with_auth.get_deposit_address(currency_code=btc)
    assert sdk_resp == rest_sync_mock_resp

    # subaccount_id must be supported
    try:
        sync_client_with_auth.get_deposit_address(currency_code=btc, subaccount_id=subaccount_id)
    except Exception:
        assert False, "Exception incorrectly raised when using subaccount_id"


def test_get_crypto_withdrawal_info(rest_sync_mocker, sync_client, sync_client_with_auth, rest_sync_mock_resp, btc,
                                    subaccount_id):
    rest_sync_mocker.get(f'{BASE_URL}/v1/wallet/crypto/{btc}/withdraw', json=rest_sync_mock_resp)

    with pytest.raises(RequiresAuthentication):
        sync_client.get_crypto_withdrawal_info(currency_code=btc)

    sdk_resp = sync_client_with_auth.get_crypto_withdrawal_info(currency_code=btc)
    assert sdk_resp == rest_sync_mock_resp

    # subaccount_id must be supported
    try:
        sync_client_with_auth.get_crypto_withdrawal_info(currency_code=btc, subaccount_id=subaccount_id)
    except Exception:
        assert False, "Exception incorrectly raised when using subaccount_id"


def test_post_crypto_withdrawal(rest_sync_mocker, sync_client, sync_client_with_auth, rest_sync_mock_resp, btc,
                                subaccount_id):
    amount = Decimal(0.001)
    address = 'crypto-address'
    payment_reference = 'payment-ref'
    rest_sync_mocker.post(f'{BASE_URL}/v1/wallet/crypto/{btc}/withdraw', json=rest_sync_mock_resp)

    with pytest.raises(RequiresAuthentication):
        sync_client.post_crypto_withdrawal(currency_code=btc, amount=amount, address=address,
                                           payment_reference=payment_reference)

    sdk_resp = sync_client_with_auth.post_crypto_withdrawal(currency_code=btc, amount=amount, address=address,
                                                            payment_reference=payment_reference)
    assert sdk_resp == rest_sync_mock_resp

    # subaccount_id must be supported
    try:
        sync_client_with_auth.post_crypto_withdrawal(currency_code=btc, amount=amount, address=address,
                                                     payment_reference=payment_reference, subaccount_id=subaccount_id)
    except Exception:
        assert False, "Exception incorrectly raised when using subaccount_id"


def test_get_crypto_withdrawal_status(rest_sync_mocker, sync_client, sync_client_with_auth, rest_sync_mock_resp, btc,
                                      subaccount_id):
    withdraw_id = 'withdraw_id'
    rest_sync_mocker.get(f'{BASE_URL}/v1/wallet/crypto/{btc}/withdraw/{withdraw_id}', json=rest_sync_mock_resp)

    with pytest.raises(RequiresAuthentication):
        sync_client.get_crypto_withdrawal_status(currency_code=btc)

    sdk_resp = sync_client_with_auth.get_crypto_withdrawal_status(currency_code=btc, withdraw_id=withdraw_id)
    assert sdk_resp == rest_sync_mock_resp

    # subaccount_id must be supported
    try:
        sync_client_with_auth.get_crypto_withdrawal_status(currency_code=btc, withdraw_id=withdraw_id,
                                                           subaccount_id=subaccount_id)
    except Exception:
        assert False, "Exception incorrectly raised when using subaccount_id"


def test_get_crypto_deposit_history(rest_sync_mocker, sync_client, sync_client_with_auth, rest_sync_mock_resp, btc,
                                    subaccount_id):
    skip = 5
    limit = 5
    rest_sync_mocker.get(f'{BASE_URL}/v1/wallet/crypto/{btc}/deposit/history', json=rest_sync_mock_resp)

    with pytest.raises(RequiresAuthentication):
        sync_client.get_deposit_history(currency_code=btc, skip=skip, limit=limit)

    sdk_resp = sync_client_with_auth.get_deposit_history(currency_code=btc, skip=skip, limit=limit)
    assert sdk_resp == rest_sync_mock_resp

    # subaccount_id must be supported
    try:
        sync_client_with_auth.get_deposit_history(currency_code=btc, skip=skip, limit=limit,
                                                  subaccount_id=subaccount_id)
    except Exception:
        assert False, "Exception incorrectly raised when using subaccount_id"


def test_get_crypto_withdrawal_history(rest_sync_mocker, sync_client, sync_client_with_auth, rest_sync_mock_resp, btc,
                                       subaccount_id):
    skip = 5
    limit = 5
    rest_sync_mocker.get(f'{BASE_URL}/v1/wallet/crypto/{btc}/withdraw/history',
                         json=rest_sync_mock_resp)

    with pytest.raises(RequiresAuthentication):
        sync_client.get_crypto_withdrawal_history(currency_code=btc, skip=skip, limit=limit)

    sdk_resp = sync_client_with_auth.get_crypto_withdrawal_history(currency_code=btc, skip=skip, limit=limit)
    assert sdk_resp == rest_sync_mock_resp

    # subaccount_id must be supported
    try:
        sync_client_with_auth.get_crypto_withdrawal_history(currency_code=btc, skip=skip, limit=limit,
                                                            subaccount_id=subaccount_id)
    except Exception:
        assert False, "Exception incorrectly raised when using subaccount_id"


# Wallets - Fiat

def test_get_fiat_bank_accounts(rest_sync_mocker, sync_client, sync_client_with_auth, rest_sync_mock_resp, zar,
                                subaccount_id):
    rest_sync_mocker.get(f'{BASE_URL}/v1/wallet/fiat/{zar}/accounts', json=rest_sync_mock_resp)

    with pytest.raises(RequiresAuthentication):
        sync_client.get_fiat_bank_accounts(currency_code=zar)

    sdk_resp = sync_client_with_auth.get_fiat_bank_accounts(currency_code=zar)
    assert sdk_resp == rest_sync_mock_resp

    # subaccount_id must be supported
    try:
        sync_client_with_auth.get_fiat_bank_accounts(currency_code=zar, subaccount_id=subaccount_id)
    except Exception:
        assert False, "Exception incorrectly raised when using subaccount_id"


def test_post_fiat_withdrawal(rest_sync_mocker, sync_client, sync_client_with_auth, rest_sync_mock_resp, zar,
                              subaccount_id):
    linked_bank_account_id = 'linked_bank_account_id'
    amount = Decimal(100000.00)
    rest_sync_mocker.post(f'{BASE_URL}/v1/wallet/fiat/{zar}/withdraw', json=rest_sync_mock_resp)

    with pytest.raises(RequiresAuthentication):
        sync_client.post_fiat_withdrawal(currency_code=zar, amount=amount,
                                         linked_bank_account_id=linked_bank_account_id)

    sdk_resp = sync_client_with_auth.post_fiat_withdrawal(currency_code=zar, amount=amount,
                                                          linked_bank_account_id=linked_bank_account_id)
    assert sdk_resp == rest_sync_mock_resp

    # subaccount_id must be supported
    try:
        sync_client_with_auth.post_fiat_withdrawal(currency_code=zar, amount=amount,
                                                   linked_bank_account_id=linked_bank_account_id,
                                                   subaccount_id=subaccount_id)
    except Exception:
        assert False, "Exception incorrectly raised when using subaccount_id"


# Market Data APIs

def test_get_order_book(rest_sync_mocker, sync_client, sync_client_with_auth, rest_sync_mock_resp, btc_zar,
                        subaccount_id):
    rest_sync_mocker.get(f'{BASE_URL}/v1/marketdata/{btc_zar}/orderbook', json=rest_sync_mock_resp)

    with pytest.raises(RequiresAuthentication):
        sync_client.get_order_book(currency_pair=btc_zar)

    sdk_resp = sync_client_with_auth.get_order_book(currency_pair=btc_zar)
    assert sdk_resp == rest_sync_mock_resp

    # subaccount_id must be supported
    try:
        sync_client_with_auth.get_order_book(currency_pair=btc_zar, subaccount_id=subaccount_id)
    except Exception:
        assert False, "Exception incorrectly raised when using subaccount_id"


def test_get_order_book_full(rest_sync_mocker, sync_client, sync_client_with_auth, rest_sync_mock_resp, btc_zar,
                             subaccount_id):
    rest_sync_mocker.get(f'{BASE_URL}/v1/marketdata/{btc_zar}/orderbook/full', json=rest_sync_mock_resp)

    with pytest.raises(RequiresAuthentication):
        sync_client.get_order_book_full(currency_pair=btc_zar)

    sdk_resp = sync_client_with_auth.get_order_book_full(currency_pair=btc_zar)
    assert sdk_resp == rest_sync_mock_resp

    # subaccount_id must be supported
    try:
        sync_client_with_auth.get_order_book_full(currency_pair=btc_zar, subaccount_id=subaccount_id)
    except Exception:
        assert False, "Exception incorrectly raised when using subaccount_id"


def test_get_trade_history_marketdata(rest_sync_mocker, sync_client, sync_client_with_auth, rest_sync_mock_resp,
                                      btc_zar, subaccount_id):
    limit = 10
    skip = 0
    start_time = '2020-11-30T08:51:21.604113Z'
    end_time = '2020-11-30T08:55:29.339000Z'
    before_id = '35f07b86-d788-43e2-96f0-9e5a7b9b56d0'
    rest_sync_mocker.get(f'{BASE_URL}/v1/marketdata/{btc_zar}/tradehistory', json=rest_sync_mock_resp)

    with pytest.raises(RequiresAuthentication):
        sync_client.get_trade_history_marketdata(currency_pair=btc_zar, limit=limit)

    sdk_resp_basic = sync_client_with_auth.get_trade_history_marketdata(currency_pair=btc_zar)
    assert sdk_resp_basic == rest_sync_mock_resp

    sdk_resp_basic_params = sync_client_with_auth.get_trade_history_marketdata(currency_pair=btc_zar, limit=limit,
                                                                               skip=skip)
    assert sdk_resp_basic_params == rest_sync_mock_resp

    sdk_resp_filters = sync_client_with_auth.get_trade_history_marketdata(currency_pair=btc_zar, limit=limit,
                                                                          skip=skip, start_time=start_time,
                                                                          end_time=end_time)
    assert sdk_resp_filters == rest_sync_mock_resp

    sdk_resp_paginated = sync_client_with_auth.get_trade_history_marketdata(currency_pair=btc_zar, limit=limit,
                                                                            before_id=before_id)
    assert sdk_resp_paginated == rest_sync_mock_resp

    # subaccount_id must be supported
    try:
        sync_client_with_auth.get_trade_history_marketdata(currency_pair=btc_zar, subaccount_id=subaccount_id)
    except Exception:
        assert False, "Exception incorrectly raised when using subaccount_id"


# Simple Buy/Sell APIs

def test_post_simple_quote(rest_sync_mocker, sync_client, sync_client_with_auth, rest_sync_mock_resp, btc_zar, btc,
                           subaccount_id):
    pay_in_currency = btc
    pay_amount = 0.01
    side = "SELL"
    rest_sync_mocker.post(f'{BASE_URL}/v1/simple/{btc_zar}/quote', json=rest_sync_mock_resp)

    with pytest.raises(RequiresAuthentication):
        sync_client.post_simple_quote(currency_pair=btc_zar, pay_in_currency=pay_in_currency,
                                      pay_amount=pay_amount, side=side)

    sdk_resp = sync_client_with_auth.post_simple_quote(currency_pair=btc_zar, pay_in_currency=pay_in_currency,
                                                       pay_amount=pay_amount, side=side)
    assert sdk_resp == rest_sync_mock_resp

    # subaccount_id must be supported
    try:
        sync_client_with_auth.post_simple_quote(currency_pair=btc_zar, pay_in_currency=pay_in_currency,
                                                pay_amount=pay_amount, side=side, subaccount_id=subaccount_id)
    except Exception:
        assert False, "Exception incorrectly raised when using subaccount_id"


def test_post_simple_order(rest_sync_mocker, sync_client, sync_client_with_auth, rest_sync_mock_resp, btc_zar, btc,
                           subaccount_id):
    pay_in_currency = btc
    pay_amount = 0.01
    side = "SELL"
    rest_sync_mocker.post(f'{BASE_URL}/v1/simple/{btc_zar}/order', json=rest_sync_mock_resp)

    with pytest.raises(RequiresAuthentication):
        sync_client.post_simple_order(currency_pair=btc_zar, pay_in_currency=pay_in_currency,
                                      pay_amount=pay_amount, side=side)

    sdk_resp = sync_client_with_auth.post_simple_order(currency_pair=btc_zar, pay_in_currency=pay_in_currency,
                                                       pay_amount=pay_amount, side=side)
    assert sdk_resp == rest_sync_mock_resp

    # subaccount_id must be supported
    try:
        sync_client_with_auth.post_simple_order(currency_pair=btc_zar, pay_in_currency=pay_in_currency,
                                                pay_amount=pay_amount, side=side, subaccount_id=subaccount_id)
    except Exception:
        assert False, "Exception incorrectly raised when using subaccount_id"


def test_get_simple_order_status(rest_sync_mocker, sync_client, sync_client_with_auth, rest_sync_mock_resp, btc_zar,
                                 subaccount_id):
    order_id = 'order_id'
    rest_sync_mocker.get(f'{BASE_URL}/v1/simple/{btc_zar}/order/{order_id}', json=rest_sync_mock_resp)

    with pytest.raises(RequiresAuthentication):
        sync_client.get_simple_order_status(currency_pair=btc_zar, order_id=order_id)

    sdk_resp = sync_client_with_auth.get_simple_order_status(currency_pair=btc_zar, order_id=order_id)
    assert sdk_resp == rest_sync_mock_resp

    # subaccount_id must be supported
    try:
        sync_client_with_auth.get_simple_order_status(currency_pair=btc_zar, order_id=order_id, subaccount_id=subaccount_id)
    except Exception:
        assert False, "Exception incorrectly raised when using subaccount_id"


# Exchange Buy/Sell APIs

def test_post_limit_order(rest_sync_mocker, sync_client, sync_client_with_auth, rest_sync_mock_resp, btc_zar,
                          subaccount_id):
    side = "SELL"
    quantity = Decimal(0.100000)
    price = Decimal(123000)
    post_only = True
    customer_order_id = 'customer_order_id'
    rest_sync_mocker.post(f'{BASE_URL}/v1/orders/limit', json=rest_sync_mock_resp)

    with pytest.raises(RequiresAuthentication):
        sync_client.post_limit_order(side=side, quantity=quantity, price=price, pair=btc_zar, post_only=post_only,
                                     customer_order_id=customer_order_id)

    sdk_resp = sync_client_with_auth.post_limit_order(side=side, quantity=quantity, price=price, pair=btc_zar,
                                                      post_only=post_only, customer_order_id=customer_order_id)
    assert sdk_resp == rest_sync_mock_resp

    # subaccount_id must be supported
    try:
        sync_client_with_auth.post_limit_order(side=side, quantity=quantity, price=price, pair=btc_zar,
                                               post_only=post_only, customer_order_id=customer_order_id,
                                               subaccount_id=subaccount_id)
    except Exception:
        assert False, "Exception incorrectly raised when using subaccount_id"


def test_post_market_order(rest_sync_mocker, sync_client, sync_client_with_auth, rest_sync_mock_resp, btc_zar,
                           subaccount_id):
    side = "SELL"
    base_amount = Decimal(0.100000)
    quote_amount = Decimal(123000)
    customer_order_id = 'customer_order_id'
    rest_sync_mocker.post(f'{BASE_URL}/v1/orders/market', json=rest_sync_mock_resp)

    with pytest.raises(RequiresAuthentication):
        sync_client.post_market_order(side=side, pair=btc_zar, base_amount=base_amount,
                                      customer_order_id=customer_order_id)

    with pytest.raises(AttributeError):
        sync_client_with_auth.post_market_order(side=side, pair=btc_zar, base_amount=base_amount,
                                                quote_amount=quote_amount, customer_order_id=customer_order_id)

    sdk_resp = sync_client_with_auth.post_market_order(side=side, pair=btc_zar, base_amount=base_amount,
                                                       customer_order_id=customer_order_id)
    assert sdk_resp == rest_sync_mock_resp

    # subaccount_id must be supported
    try:
        sync_client_with_auth.post_market_order(side=side, pair=btc_zar, base_amount=base_amount,
                                                customer_order_id=customer_order_id, subaccount_id=subaccount_id)
    except Exception:
        assert False, "Exception incorrectly raised when using subaccount_id"


def test_post_stop_limit_order(rest_sync_mocker, sync_client, sync_client_with_auth, rest_sync_mock_resp, btc_zar,
                               subaccount_id):
    side = "SELL"
    quantity = Decimal(0.100000)
    limit_price = Decimal(123000)
    stop_price = Decimal(120000)
    customer_order_id = 'customer_order_id'
    time_in_force = 'GTC'
    stop_limit_type = 'STOP_LOSS_LIMIT'
    rest_sync_mocker.post(f'{BASE_URL}/v1/orders/stop/limit', json=rest_sync_mock_resp)

    with pytest.raises(RequiresAuthentication):
        sync_client.post_stop_limit_order(side=side, pair=btc_zar, quantity=quantity,
                                          limit_price=limit_price, stop_price=stop_price,
                                          time_in_force=time_in_force, stop_limit_type=stop_limit_type,
                                          customer_order_id=customer_order_id)

    sdk_resp = sync_client_with_auth.post_stop_limit_order(side=side, pair=btc_zar, quantity=quantity,
                                                           limit_price=limit_price, stop_price=stop_price,
                                                           time_in_force=time_in_force, stop_limit_type=stop_limit_type,
                                                           customer_order_id=customer_order_id)
    assert sdk_resp == rest_sync_mock_resp

    # subaccount_id must be supported
    try:
        sync_client_with_auth.post_stop_limit_order(side=side, pair=btc_zar, quantity=quantity,
                                                    limit_price=limit_price, stop_price=stop_price,
                                                    time_in_force=time_in_force, stop_limit_type=stop_limit_type,
                                                    customer_order_id=customer_order_id)
    except Exception:
        assert False, "Exception incorrectly raised when using subaccount_id"


def test_post_batch_orders(rest_sync_mocker, sync_client, sync_client_with_auth, rest_sync_mock_resp, btc_zar,
                           subaccount_id):
    batch_requests = [
        {
            "type": "PLACE_MARKET",
            "data": {
                "side": "SELL",
                "quoteAmount": "100",
                "pair": "BTCZAR",
                "customerOrderId": "1234"
            }
        },
        {
            "type": "PLACE_LIMIT",
            "data": {
                "pair": "BTCZAR",
                "side": "BUY",
                "quantity": "0.0002",
                "price": "100000",
                "timeInForce": "GTC"
            }
        }
    ]
    rest_sync_mocker.post(f'{BASE_URL}/v1/batch/orders', json=rest_sync_mock_resp)

    with pytest.raises(RequiresAuthentication):
        sync_client.post_batch_orders(batch_requests=batch_requests)

    sdk_resp = sync_client_with_auth.post_batch_orders(batch_requests=batch_requests)
    assert sdk_resp == rest_sync_mock_resp

    # subaccount_id must be supported
    try:
        sync_client_with_auth.post_batch_orders(batch_requests=batch_requests, subaccount_id=subaccount_id)
    except Exception:
        assert False, "Exception incorrectly raised when using subaccount_id"


def test_get_order_status(rest_sync_mocker, sync_client, sync_client_with_auth, rest_sync_mock_resp, btc_zar,
                          subaccount_id):
    customer_order_id = "customer_order_id"
    order_id = "order_id"

    rest_sync_mocker.get(f'{BASE_URL}/v1/orders/{btc_zar}/orderid/{order_id}', json=rest_sync_mock_resp)

    with pytest.raises(RequiresAuthentication):
        sync_client.get_order_status(currency_pair=btc_zar, order_id=order_id)

    with pytest.raises(AttributeError):
        sync_client_with_auth.get_order_status(currency_pair=btc_zar, order_id=order_id,
                                               customer_order_id=customer_order_id)

    sdk_resp_order_id = sync_client_with_auth.get_order_status(currency_pair=btc_zar, order_id=order_id)
    assert sdk_resp_order_id == rest_sync_mock_resp

    rest_sync_mocker.get(f'{BASE_URL}/v1/orders/{btc_zar}/customerorderid/{customer_order_id}',
                         json=rest_sync_mock_resp)
    sdk_resp_customer_order_id = sync_client_with_auth.get_order_status(currency_pair=btc_zar,
                                                                        customer_order_id=customer_order_id)
    assert sdk_resp_customer_order_id == rest_sync_mock_resp

    # subaccount_id must be supported
    try:
        sync_client_with_auth.get_order_status(currency_pair=btc_zar, order_id=order_id, subaccount_id=subaccount_id)
    except Exception:
        assert False, "Exception incorrectly raised when using subaccount_id"


def test_get_all_open_orders(rest_sync_mocker, sync_client, sync_client_with_auth, rest_sync_mock_resp,
                             subaccount_id):
    rest_sync_mocker.get(f'{BASE_URL}/v1/orders/open', json=rest_sync_mock_resp)

    with pytest.raises(RequiresAuthentication):
        sync_client.get_all_open_orders()

    sdk_resp = sync_client_with_auth.get_all_open_orders()
    assert sdk_resp == rest_sync_mock_resp

    # subaccount_id must be supported
    try:
        sync_client_with_auth.get_all_open_orders(subaccount_id=subaccount_id)
    except Exception:
        assert False, "Exception incorrectly raised when using subaccount_id"


def test_get_order_history(rest_sync_mocker, sync_client, sync_client_with_auth, rest_sync_mock_resp,
                           subaccount_id):
    skip = 0
    limit = 2
    rest_sync_mocker.get('/v1/orders/history', json=rest_sync_mock_resp)

    with pytest.raises(RequiresAuthentication):
        sync_client.get_order_history()

    sdk_resp = sync_client_with_auth.get_order_history(skip=skip, limit=limit)
    assert sdk_resp == rest_sync_mock_resp

    # subaccount_id must be supported
    try:
        sync_client_with_auth.get_order_history(subaccount_id=subaccount_id)
    except Exception:
        assert False, "Exception incorrectly raised when using subaccount_id"


def test_get_order_history_summary(rest_sync_mocker, sync_client, sync_client_with_auth, rest_sync_mock_resp,
                                   subaccount_id):
    customer_order_id = "customer_order_id"
    order_id = "order_id"

    rest_sync_mocker.get(f'{BASE_URL}/v1/orders/history/summary/orderid/{order_id}', json=rest_sync_mock_resp)

    with pytest.raises(RequiresAuthentication):
        sync_client.get_order_history_summary(order_id=order_id)

    with pytest.raises(AttributeError):
        sync_client_with_auth.get_order_history_summary(order_id=order_id, customer_order_id=customer_order_id)

    sdk_resp_order_id = sync_client_with_auth.get_order_history_summary(order_id=order_id)
    assert sdk_resp_order_id == rest_sync_mock_resp

    rest_sync_mocker.get(f'{BASE_URL}/v1/orders/history/summary/customerorderid/{customer_order_id}',
                         json=rest_sync_mock_resp)
    sdk_resp_customer_order_id = sync_client_with_auth.get_order_history_summary(customer_order_id=customer_order_id)
    assert sdk_resp_customer_order_id == rest_sync_mock_resp

    # subaccount_id must be supported
    try:
        sync_client_with_auth.get_order_history_summary(order_id=order_id, subaccount_id=subaccount_id)
    except Exception:
        assert False, "Exception incorrectly raised when using subaccount_id"


def test_get_order_history_detail(rest_sync_mocker, sync_client, sync_client_with_auth, rest_sync_mock_resp,
                                  subaccount_id):
    customer_order_id = "customer_order_id"
    order_id = "order_id"

    rest_sync_mocker.get(f'{BASE_URL}/v1/orders/history/detail/orderid/{order_id}', json=rest_sync_mock_resp)

    with pytest.raises(RequiresAuthentication):
        sync_client.get_order_history_detail(order_id=order_id)

    with pytest.raises(AttributeError):
        sync_client_with_auth.get_order_history_detail(order_id=order_id, customer_order_id=customer_order_id)

    sdk_resp_order_id = sync_client_with_auth.get_order_history_detail(order_id=order_id)
    assert sdk_resp_order_id == rest_sync_mock_resp

    rest_sync_mocker.get(f'{BASE_URL}/v1/orders/history/detail/customerorderid/{customer_order_id}',
                         json=rest_sync_mock_resp)
    sdk_resp_customer_order_id = sync_client_with_auth.get_order_history_detail(customer_order_id=customer_order_id)
    assert sdk_resp_customer_order_id == rest_sync_mock_resp

    # subaccount_id must be supported
    try:
        sync_client_with_auth.get_order_history_detail(order_id=order_id, subaccount_id=subaccount_id)
    except Exception:
        assert False, "Exception incorrectly raised when using subaccount_id"


def test_delete_order(rest_sync_mocker, sync_client, sync_client_with_auth, rest_sync_mock_resp, btc_zar,
                      subaccount_id):
    customer_order_id = "customer_order_id"
    order_id = "order_id"

    rest_sync_mocker.delete(f'{BASE_URL}/v1/orders/order', json=rest_sync_mock_resp)

    with pytest.raises(RequiresAuthentication):
        sync_client.delete_order(pair=btc_zar, order_id=order_id)

    with pytest.raises(AttributeError):
        sync_client_with_auth.delete_order(pair=btc_zar, order_id=order_id, customer_order_id=customer_order_id)

    sdk_resp_order_id = sync_client_with_auth.delete_order(currency_pair=btc_zar, order_id=order_id)
    assert sdk_resp_order_id == rest_sync_mock_resp

    sdk_resp_customer_order_id = sync_client_with_auth.delete_order(currency_pair=btc_zar, customer_order_id=customer_order_id)
    assert sdk_resp_customer_order_id == rest_sync_mock_resp

    # subaccount_id must be supported
    try:
        sync_client_with_auth.delete_order(currency_pair=btc_zar, order_id=order_id, subaccount_id=subaccount_id)
    except Exception:
        assert False, "Exception incorrectly raised when using subaccount_id"
