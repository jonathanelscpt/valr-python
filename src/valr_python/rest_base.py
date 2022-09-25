import warnings
from abc import ABCMeta
from abc import abstractmethod
from decimal import Decimal
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import requests

from valr_python.decorators import check_xor_attrs
from valr_python.decorators import requires_authentication
from valr_python.enum import CurrencyPair
from valr_python.enum import Side
from valr_python.enum import TransactionType
from valr_python.exceptions import APIError

__all__ = ()

DEFAULT_TIMEOUT = 10


class BaseClientABC(metaclass=ABCMeta):
    _REST_API_URL = 'https://api.valr.com'

    def __init__(self, api_key: str = "", api_secret: str = "", timeout: int = 10, base_url: str = "",
                 rate_limiting_support: bool = False) -> None:
        self._api_key = api_key
        self._api_secret = api_secret
        self._base_url = base_url.rstrip('/') if base_url else self._REST_API_URL
        self._timeout = self.check_timeout(timeout)
        self._rate_limiting_support = rate_limiting_support
        self._session = requests.Session()

    @property
    def api_key(self) -> str:
        return self._api_key

    @api_key.setter
    def api_key(self, value: str) -> None:
        self._api_key = value

    @property
    def api_secret(self) -> str:
        return self._api_secret

    @api_secret.setter
    def api_secret(self, value: str) -> None:
        self._api_secret = value

    @property
    def timeout(self) -> int:
        return self._timeout

    @timeout.setter
    def timeout(self, value: int) -> None:
        self._timeout = self.check_timeout(value)

    @property
    def base_url(self) -> str:
        return self._base_url

    @base_url.setter
    def base_url(self, value: str) -> None:
        self._base_url = value.rstrip('/') if value else self._REST_API_URL

    @property
    def rate_limiting_support(self) -> bool:
        return self._rate_limiting_support

    @rate_limiting_support.setter
    def rate_limiting_support(self, value: bool) -> None:
        self._rate_limiting_support = value

    @staticmethod
    def check_timeout(timeout: int) -> int:
        """Check if request is non-zero and set to 10 if zero. """
        if timeout == 0:
            return DEFAULT_TIMEOUT
        return timeout

    @staticmethod
    def _raise_for_api_error(e):
        """Raise api responses containing error codes"""
        if 'code' in e and 'message' in e:
            raise APIError(e['code'], e['message'])

    @abstractmethod
    def _do(self, method: str, path: str, data: Optional[Dict] = None, params: Optional[Dict] = None,
            is_authenticated: bool = False, subaccount_id: str = '') -> Optional[Union[List, Dict]]:
        """Executes API request and returns the response."""
        raise NotImplementedError


class MethodClientABC(BaseClientABC, metaclass=ABCMeta):

    @abstractmethod
    def _do(self, method: str, path: str, data: Optional[Dict] = None, params: Optional[Dict] = None,
            is_authenticated: bool = False, subaccount_id: str = '') -> Optional[Union[List, Dict]]:
        """Executes API request and returns the response."""
        raise NotImplementedError

    # Public APIs

    def get_order_book_public(self, currency_pair: Union[str, CurrencyPair]) -> Dict[str, List]:
        """Makes a call to GET https://api.valr.com/v1/public/:currencyPair/orderbook

        Returns a list of the top 20 bids and asks in the order book.
        Ask orders are sorted by price ascending.
        Bid orders are sorted by price descending. Orders of the same price are aggregated.

        Please note: This is not an authenticated call.
        More constrained rate-limiting rules will apply than when you use :currencyPair/orderbook route.
        """
        return self._do('GET', f'/v1/public/{currency_pair}/orderbook')

    def get_order_book_full_public(self, currency_pair: Union[str, CurrencyPair]) -> Dict[str, List]:
        """MReturns a list of all the bids and asks in the order book. Ask orders are sorted by price ascending.
        Bid orders are sorted by price descending. Orders of the same price are NOT aggregated.
        The LastChange field indicates the timestamp of the last update to the order book.

        Please note: This is not an authenticated call. More constrained rate-limiting rules will apply than when
        you use the /marketdata/:currencyPair/orderbook/full route.
        """
        return self._do('GET', f'/v1/public/{currency_pair}/orderbook/full')

    def get_currencies(self) -> List[Dict]:
        """Makes a call to GET https://api.valr.com/v1/public/currencies

        Get a list of currencies supported by VALR.
        """
        return self._do('GET', '/v1/public/currencies')

    def get_currency_pairs(self) -> List[Dict]:
        """Makes a call to GET https://api.valr.com/v1/public/pairs

        Get a list of all the currency pairs supported by VALR.
        """
        return self._do('GET', '/v1/public/pairs')

    def get_order_types(self, currency_pair: Union[str, CurrencyPair] = "") -> Union[List[Dict], List[str]]:
        """Makes a call to GET https://api.valr.com/v1/public/ordertypes

        Get all the order types supported for all currency pairs.

        An array of currency pairs is returned along with an array of order types for each currency pair.
        You can only place an order that is supported by that currency pair.


        OR


        Makes a call to GET https://api.valr.com/v1/public/:currencyPair/ordertypes

        Get the order types supported for a given currency pair.

        An array of order types is returned. You can only place an order that is listed in this
        array for this currency pair.
        """
        if currency_pair:
            return self._do('GET', f'/v1/public/{currency_pair}/ordertypes')
        else:
            return self._do('GET', '/v1/public/ordertypes')

    def get_market_summary(self, currency_pair: Union[str, CurrencyPair] = "") -> Union[List[Dict], Dict]:
        """Makes a call to GET https://api.valr.com/v1/public/marketsummary

        Get the market summary for all supported currency pairs.


        OR


        Makes a call to GET https://api.valr.com/v1/public/:currencyPair/marketsummary

        Get the market summary for a given currency pair.
        """
        if currency_pair:
            return self._do('GET', f'/v1/public/{currency_pair}/marketsummary')
        else:
            return self._do('GET', '/v1/public/marketsummary')

    def get_trade_history_public(self, currency_pair: Union[str, CurrencyPair], limit: Optional[int] = 100,
                                 skip: Optional[int] = None, start_time: Optional[int] = None,
                                 end_time: Optional[int] = None, before_id: Optional[int] = None) -> List[Dict]:
        """Makes a call to GET https://api.valr.com/v1/marketdata/:currencyPair/tradehistory?limit=10

        Get the last 100 recent trades for a given currency pair.
        You can limit the number of trades returned by specifying the limit parameter.
        """
        opts = {'skip': skip, 'limit': limit, 'startTime': start_time, 'endTime': end_time, 'beforeId': before_id}
        params = {k: v for k, v in opts.items() if v}
        return self._do('GET', f'/v1/public/{currency_pair}/trades', params=params)

    def get_server_time(self) -> Dict:
        """Makes a call to GET https://api.valr.com/v1/public/time

        Get the server time. Please note: The server time is returned in seconds.
        """
        return self._do('GET', '/v1/public/time')

    def get_valr_status(self) -> Dict:
        """Get the current status of VALR.

        May be "online" when all functionality is available, or "read-only" when only GET and OPTIONS requests are accepted.
        All other requests in read-only mode will respond with a 503 error code.
        """
        return self._do('GET', '/v1/public/status')

    # Account APIs - API Keys

    @requires_authentication
    def get_current_api_key_info(self, subaccount_id: str = "") -> List[Dict]:
        """Returns the current API Key's information and permissions.
        This information includes the label, date created, and permissions.
        Permission levels are View Access, Trade , or Withdraw.

        If an API key has Whitelisted IP address ranges or Whitelisted Withdrawal addresses,
        the IP addresses and Currency withdrawal addresses will also be returned.
        """
        return self._do('GET', '/v1/account/api-keys/current', is_authenticated=True, subaccount_id=subaccount_id)

    # Account APIs - Sub-accounts

    @requires_authentication
    def get_subaccounts(self) -> List[Dict]:
        """Returns the list of all subaccounts that belong to a primary account, with each subaccount's label and id.

        Can only be called by a primary account API key.
        """
        return self._do('GET', '/v1/account/subaccounts', is_authenticated=True)

    @requires_authentication
    def get_nonzero_balances(self) -> List[Dict]:
        """Returns the entire portfolio's balances that are greater than 0, grouped by account
        for primary account and subaccounts.

        Can only be called by a primary account API key.
        """
        return self._do('GET', '/v1/account/balances/all', is_authenticated=True)

    @requires_authentication
    def register_subaccount(self, label: str) -> Dict:
        """Creates a new subaccount.

        Can only be called by a primary account API key with Trade permissions.
        """
        data = {"label": label}
        return self._do('POST', '/v1/account/subaccount', data=data, is_authenticated=True)

    @requires_authentication
    def post_internal_transfer_subaccounts(self, from_id: str, to_id: str, currency_code: str, amount: str,
                                           subaccount_id: str = "") -> Dict:
        """Transfer funds between 2 accounts.

        The primary API key can transfer from and to any subaccount.
        The subaccount API key can only transfer from itself.
        """
        data = {"fromId": from_id, "toId": to_id, "currencyCode": currency_code, "amount": amount}
        return self._do('POST', '/v1/account/subaccounts/transfer', data=data, is_authenticated=True,
                        subaccount_id=subaccount_id)

    # Account APIs - General

    @requires_authentication
    def get_balances(self, subaccount_id: str = '') -> List[Dict]:
        """Makes a call to GET https://api.valr.com/v1/account/balances

        Returns the list of all wallets with their respective balances.
        """
        return self._do('GET', '/v1/account/balances', is_authenticated=True, subaccount_id=subaccount_id)

    # todo - fix attr names to be pythonic
    @requires_authentication
    def get_transaction_history(self, skip: Optional[int] = None, limit: Optional[int] = 100,
                                transaction_types: Optional[Union[List[Union[str, TransactionType]], str, TransactionType]] = None,
                                before_id: Optional[str] = None, currency: Optional[str] = None,
                                start_time: Optional[str] = None, end_time: Optional[str] = None,
                                subaccount_id: str = '') -> List[Dict]:
        """Makes a call to GET https://api.valr.com/v1/account/transactionhistory?skip=0&limit=100

        Transaction history for your account. Note: This API supports pagination.
        """
        if transaction_types and isinstance(transaction_types, list):
            transaction_types = ','.join(transaction_types)
        opts = {
            'skip': skip,
            'limit': limit,
            'transactionTypes': transaction_types,
            'currency': currency,
            'startTime': start_time,
            'endTime': end_time,
            'beforeId': before_id
        }
        params = {k: v for k, v in opts.items() if v}
        return self._do('GET', '/v1/account/transactionhistory', params=params, is_authenticated=True,
                        subaccount_id=subaccount_id)

    # check with valr if full param support is included as per public calls
    @requires_authentication
    def get_trade_history(self, currency_pair: Union[str, CurrencyPair],
                          limit: Optional[int] = 100, subaccount_id: str = '') -> List[Dict]:
        """Makes a call to GET https://api.valr.com/v1/account/:currencyPair/tradehistory?limit=10

        Get the last 100 recent trades for a given currency pair for your account.
        You can limit the number of trades returned by specifying the `limit` parameter.
        """
        opts = {'limit': limit}
        params = {k: v for k, v in opts.items() if v}
        return self._do('GET', f'/v1/account/{currency_pair}/tradehistory', params=params, is_authenticated=True,
                        subaccount_id=subaccount_id)

    # Crypto Wallet APIs

    @requires_authentication
    def get_deposit_address(self, currency_code: str, subaccount_id: str = '') -> Dict:
        """Makes a call to GET https://api.valr.com/v1/wallet/crypto/:currencyCode/deposit/address

        Returns the default deposit address associated with currency specified in the path variable `:currencyCode`.
        """
        return self._do('GET', f'/v1/wallet/crypto/{currency_code}/deposit/address',
                        is_authenticated=True, subaccount_id=subaccount_id)

    @requires_authentication
    def get_whitelisted_address_book(self, currency_code: Optional[str] = None, subaccount_id: str = '') -> Dict:
        """Makes a call to GET https://api.valr.com/v1/wallet/crypto/:currencyCode/withdraw

        Get all the information about withdrawing a given currency from your VALR account.
        That will include withdrawal costs, minimum withdrawal amount etc.
        """
        if currency_code:
            return self._do('GET', f'/v1/wallet/crypto/address-book/{currency_code}',
                            is_authenticated=True, subaccount_id=subaccount_id)
        else:
            return self._do('GET', '/v1/wallet/crypto/address-book',
                            is_authenticated=True, subaccount_id=subaccount_id)

    @requires_authentication
    def get_crypto_withdrawal_info(self, currency_code: str, subaccount_id: str = '') -> Dict:
        """Makes a call to GET https://api.valr.com/v1/wallet/crypto/:currencyCode/withdraw

        Get all the information about withdrawing a given currency from your VALR account.
        That will include withdrawal costs, minimum withdrawal amount etc.
        """
        return self._do('GET', f'/v1/wallet/crypto/{currency_code}/withdraw',
                        is_authenticated=True, subaccount_id=subaccount_id)

    @requires_authentication
    def post_crypto_withdrawal(self, currency_code: str, amount: Union[Decimal, str],
                               address: str, payment_reference: str = "", subaccount_id: str = '') -> Dict:
        """Makes a call to POST https://api.valr.com/v1/wallet/crypto/:currencyCode/withdraw

        Withdraw cryptocurrency funds to an address.

        The request body for XRP, XMR, XEM, XLM will accept an optional field called "paymentReference".
        Max length for paymentReference is 256.
        """
        data = {"amount": amount, "address": address}
        if payment_reference:
            data["paymentReference"] = payment_reference
        return self._do('POST', f'/v1/wallet/crypto/{currency_code}/withdraw', data=data,
                        is_authenticated=True, subaccount_id=subaccount_id)

    @requires_authentication
    def get_crypto_withdrawal_status(self, currency_code: str, withdraw_id: str, subaccount_id: str = '') -> Dict:
        """Makes a call to GET https://api.valr.com/v1/wallet/crypto/:currencyCode/withdraw/:withdrawId

        Check the status of a withdrawal.
        """
        return self._do('GET', f'/v1/wallet/crypto/{currency_code}/withdraw/{withdraw_id}',
                        is_authenticated=True, subaccount_id=subaccount_id)

    @requires_authentication
    def get_deposit_history(self, currency_code: str, skip: Optional[int] = None, limit: Optional[int] = 100,
                            subaccount_id: str = '') -> List[Dict]:
        """Makes a call to GET https://api.valr.com/v1/wallet/crypto/:currencyCode/deposit/history?skip=0&limit=10

        Get the Deposit History records for a given currency.
        """
        opts = {'skip': skip, 'limit': limit}
        params = {k: v for k, v in opts.items() if v}
        return self._do('GET', f'/v1/wallet/crypto/{currency_code}/deposit/history', params=params,
                        is_authenticated=True, subaccount_id=subaccount_id)

    @requires_authentication
    def get_crypto_withdrawal_history(self, currency_code: str, skip: Optional[int] = None, limit: Optional[int] = 100,
                                      subaccount_id: str = '') -> List[Dict]:
        """Makes a call to GET https://api.valr.com/v1/wallet/crypto/:currencyCode/withdraw/history?skip=0&limit=10

        Get Withdrawal History records for a given currency.
        """
        opts = {'skip': skip, 'limit': limit}
        params = {k: v for k, v in opts.items() if v}
        return self._do('GET', f'/v1/wallet/crypto/{currency_code}/withdraw/history', params=params,
                        is_authenticated=True, subaccount_id=subaccount_id)

    # Fiat Wallet APIs

    @requires_authentication
    def get_fiat_bank_accounts(self, currency_code: str, subaccount_id: str = '') -> List[Dict]:
        """Makes a call to GET https://api.valr.com/v1/wallet/fiat/:currencyCode/accounts

        Get a list of bank accounts that are linked to your VALR account.
        Bank accounts can be linked by signing in to your account on www.VALR.com.
        """
        return self._do('GET', f'/v1/wallet/fiat/{currency_code}/accounts',
                        is_authenticated=True, subaccount_id=subaccount_id)

    @requires_authentication
    def post_fiat_withdrawal(self, currency_code: str, linked_bank_account_id: str,
                             amount: Union[Decimal, str], fast: bool = False, subaccount_id: str = '') -> Dict:
        """Makes a call to POST https://api.valr.com/v1/wallet/fiat/:currencyCode/withdraw

        Withdraw your ZAR funds into one of your linked bank accounts.
        """
        data = {"linkedBankAccountId": linked_bank_account_id, "amount": amount, "fast": fast}
        return self._do('POST', f'/v1/wallet/fiat/{currency_code}/withdraw', data=data,
                        is_authenticated=True, subaccount_id=subaccount_id)

    # Market Data APIs

    @requires_authentication
    def get_order_book(self, currency_pair: Union[str, CurrencyPair], subaccount_id: str = '') -> Dict[str, List]:
        """Makes a call to GET https://api.valr.com/v1/marketdata/:currencyPair/orderbook

        Returns a list of the top 20 bids and asks in the order book.
        Ask orders are sorted by price ascending.
        Bid orders are sorted by price descending. Orders of the same price are aggregated.
        """
        return self._do('GET', f'/v1/marketdata/{currency_pair}/orderbook', is_authenticated=True,
                        subaccount_id=subaccount_id)

    @requires_authentication
    def get_order_book_full(self, currency_pair: Union[str, CurrencyPair],
                            subaccount_id: str = '') -> Dict[str, List]:
        """Makes a call to GET https://api.valr.com/v1/marketdata/:currencyPair/orderbook/full

        Returns a list of all the bids and asks in the order book.
        Ask orders are sorted by price ascending.
        Bid orders are sorted by price descending. Orders of the same price are NOT aggregated..
        """
        return self._do('GET', f'/v1/marketdata/{currency_pair}/orderbook/full', is_authenticated=True,
                        subaccount_id=subaccount_id)

    @requires_authentication
    def get_trade_history_marketdata(self, currency_pair: Union[str, CurrencyPair], limit: Optional[int] = 100,
                                     skip: Optional[int] = None, start_time: Optional[int] = None,
                                     end_time: Optional[int] = None, before_id: Optional[int] = None,
                                     subaccount_id: str = '') -> List[Dict]:
        """Makes a call to GET https://api.valr.com/v1/marketdata/:currencyPair/tradehistory?limit=10

        Get the last 100 recent trades for a given currency pair.
        You can limit the number of trades returned by specifying the limit parameter.
        """
        opts = {'skip': skip, 'limit': limit, 'startTime': start_time, 'endTime': end_time, 'beforeId': before_id}
        params = {k: v for k, v in opts.items() if v}
        return self._do('GET', f'/v1/marketdata/{currency_pair}/tradehistory', params=params, is_authenticated=True,
                        subaccount_id=subaccount_id)

    # Simple Buy/Sell APIs

    @requires_authentication
    def post_simple_quote(self, currency_pair: Union[str, CurrencyPair], pay_in_currency: str,
                          pay_amount: Union[Decimal, str], side: Union[str, Side], subaccount_id: str = '') -> Dict:
        """Makes a call to POST https://api.valr.com/v1/simple/:currencyPair/quote

        Get a quote to buy or sell instantly using Simple Buy.

        A sample request body is as follows:

        {
            "payInCurrency": "BTC",
            "payAmount": "0.001",
            "side": "SELL"
        }
        Example usage of payInCurrency and side for the BTCZAR currency pair:

         - If you want to sell BTC for ZAR, payInCurrency will be BTC and the side would be SELL
         - If you want to buy BTC with ZAR, payInCurrency will be ZAR and the side would be BUY

        Example usage of payInCurrency and side for the ETHBTC currency pair:

         - If you want to sell ETH for BTC, payInCurrency will be ETH and the side would be SELL
         - If you want to buy ETH with BTC, payInCurrency will be BTC and the side would be BUY
        """
        data = {"payInCurrency": pay_in_currency, "payAmount": pay_amount, "side": side}
        return self._do('POST', f'/v1/simple/{currency_pair}/quote', data=data, is_authenticated=True,
                        subaccount_id=subaccount_id)

    @requires_authentication
    def post_simple_order(self, currency_pair: Union[str, CurrencyPair], pay_in_currency: str,
                          pay_amount: Union[Decimal, str], side: Union[str, Side], subaccount_id: str = '') -> Dict:
        """Makes a call to POST https://api.valr.com/v1/simple/:currencyPair/order

        Submit an order to buy or sell instantly using Simple Buy/Sell.

        A sample request body is as follows:

        {
            "payInCurrency": "BTC",
            "payAmount": "0.001",
            "side": "SELL"
        }
        Example usage of payInCurrency and side for the BTCZAR currency pair:

         - If you want to sell BTC for ZAR, payInCurrency will be BTC and the side would be SELL
         - If you want to buy BTC with ZAR, payInCurrency will be ZAR and the side would be BUY

        Example usage of payInCurrency and side for the ETHBTC currency pair:

         - If you want to sell ETH for BTC, payInCurrency will be ETH and the side would be SELL
         - If you want to buy ETH with BTC, payInCurrency will be BTC and the side would be BUY
        """
        data = {"payInCurrency": pay_in_currency, "payAmount": pay_amount, "side": side}
        return self._do('POST', f'/v1/simple/{currency_pair}/order', data=data, is_authenticated=True,
                        subaccount_id=subaccount_id)

    @requires_authentication
    def get_simple_order_status(self, currency_pair: Union[str, CurrencyPair], order_id: str,
                                subaccount_id: str = '') -> Dict:
        """Makes a call to GET https://api.valr.com/v1/simple/:currencyPair/order/:orderId

        Get the status of a Simple Buy/Sell order.
        """
        return self._do('GET', f'/v1/simple/{currency_pair}/order/{order_id}', is_authenticated=True,
                        subaccount_id=subaccount_id)

    # Exchange Buy/Sell APIs

    @requires_authentication
    def post_limit_order(self, side: Union[str, Side], quantity: Union[Decimal, str], price: Union[Decimal, str],
                         pair: str, post_only: bool = False, customer_order_id: str = "",
                         time_in_force: Optional[str] = None, subaccount_id: str = '') -> Dict:
        """Makes a call to POST https://api.valr.com/v1/orders/limit

        Create a new limit order.

        The JSON body used to create a limit order looks like this:

        {
            "side": "SELL",
            "quantity": "0.100000",
            "price": "10000",
            "pair": "BTCZAR",
            "postOnly": true,
            "customerOrderId": "1234"
        }


        side (required)	- BUY or SELL
        quantity (required)	- ase amount in BTC
        price (required) - Price per coin in ZAR
        pair (required) - BTCZAR
        postOnly (optional)	- true or false
        customerOrderId (optional) - Numeric value. See below for explanation.

        The customerOrderId is an optional field which can be specified by clients to track
        this order using their own internal order management systems.

        - When you retrieve your open orders or history of orders, this field will also be returned along with the
        VALR's orderId for each order for which this field was specified during creation.
        - When you cancel an order, you can either specify orderId or customerOrderId, not both.
        - customerOrderId is alphanumeric with no special chars, limit of 50 characters.
        - The customerOrderId has to be unique accross all open orders for a given account.
        If you do reuse an id value that is currently an active open order, your order will not be placed
        (you can check the status of an order using the order status API call).

        Fee currency

        - If you are a Maker and you are Buying BTC with ZAR, your reward will be paid in ZAR
        - If you are a Maker and you are Selling BTC for ZAR, your reward will be paid in BTC
        - If you are a Taker and you are Buying BTC with ZAR, your fee will be charged in BTC
        - If you are a Taker and you are Selling BTC for ZAR, your fee will be charged in ZAR

        In short, fees will be in the currency that the taker is receiving and the maker is paying in the trade.

        BTC/ZAR	    MAKER	TAKER	FEE/REWARD CURRENCY
        TRADE SIDE	BUY	    SELL	ZAR
        TRADE SIDE	SELL	BUY	    BTC

        PLEASE NOTE: When you receive a response with an id, it does not always mean that the order has been placed.
        When the response is 202 Accepted, you can use the Order Status REST API or use WebSocket API
        to receive the status of this order. The reasons why an order could fail are as follows:

        - Insufficient balance in your account.
        - If you're using a non-unique customerOrderId.
        - If you set postOnly flag to true, but your order would have matched immediately.
        - Self trading: If your order matches against your own order (on the other side).
        - Insufficient liquidity: If you're placing an order and there isn't liquidity to fulfill the order.
        """
        data = {
            "side": side,
            "quantity": quantity,
            "price": price,
            "pair": pair
        }
        if post_only:
            data["postOnly"] = post_only
        if customer_order_id:
            data["customerOrderId"] = customer_order_id
        if time_in_force:
            data["timeInForce"] = time_in_force
        return self._do('POST', '/v1/orders/limit', data=data, is_authenticated=True, subaccount_id=subaccount_id)

    @requires_authentication
    @check_xor_attrs("base_amount", "quote_amount")
    def post_market_order(self, side: Union[str, Side], pair: Union[str, CurrencyPair],
                          base_amount: Optional[Union[Decimal, str]] = None,
                          quote_amount: Optional[Union[Decimal, str]] = None, customer_order_id: str = "",
                          subaccount_id: str = '') -> Dict:
        """Makes a call to POST https://api.valr.com/v1/orders/market

        Create a new market order.

        When the response is 202 Accepted, you can either use the Order Status REST API
        or use WebSocket API to receive updates about this order.

        Example request body:

        {
            "side": "SELL",
            "baseAmount": "0.100000",
            "pair": "BTCZAR",
            "customerOrderId": "1234"
        }

        side (required)	- BUY or SELL
        baseAmount / quoteAmount (required)	- Quote amount for BUY (in ZAR). Base amount for SELL (in BTC)
        pair (required)	- BTCZAR
        customerOrderId (optional) - Numeric value. See below for explanation.

        The customerOrderId is an optional field which can be specified by clients to track this order
        using their own internal order management systems.

        - When you retrieve your open orders or history of orders, this field will also be returned along
        with the VALR's orderId for each order for which this field was specified during creation.
        - When you cancel an order, you can either specify orderId or customerOrderId, not both.
        - customerOrderId is alphanumeric with no special chars, limit of 50 characters.
        - The customerOrderId has to be unique accross all open orders for a given account.
        If you do reuse an id value that is currently an active open order, your order will not be placed
        (you can check the status of an order using the order status API call).

        Fee currency

        When you place a market order, you will be charged the "Taker fee" on the trade.

        - As a Taker, if you are Buying BTC with ZAR, your fee will be charged in BTC
        - As a Taker, if you are Selling BTC for ZAR, your fee will be charged in ZAR

        PLEASE NOTE: When you receive a response with an id, it does not always mean that the order has been placed.
        When the response is 202 Accepted, you can use the Order Status REST API or use WebSocket API to receive
        the status of this order. The reasons why an order could fail are as follows:

        - Insufficient balance in your account.
        - If you're using a non-unique customerOrderId.
        - If you set postOnly flag to true, but your order would have matched immediately.
        - Self trading: If your order matches against your own order (on the other side).
        - Insufficient liquidity: If you're placing an order and there isn't liquidity to fulfill the order.
        """
        data = {
            "side": side,
            "pair": pair
        }
        if base_amount:
            data["baseAmount"] = base_amount
        else:
            data["quoteAmount"] = quote_amount
        if customer_order_id:
            data["customerOrderId"] = customer_order_id
        return self._do('POST', '/v1/orders/market', data=data, is_authenticated=True, subaccount_id=subaccount_id)

    @requires_authentication
    def post_stop_limit_order(self, side: Union[str, Side], quantity: Union[Decimal, str],
                              limit_price: Union[Decimal, str], pair: str, stop_price: Union[Decimal, str],
                              stop_limit_type: str, time_in_force: str = "GTC", customer_order_id: str = "",
                              subaccount_id: str = '') -> Dict:
        """Create a new Stop Loss Limit or Take Profit Limit order.

            When the response is 202 Accepted, you can either use the Order Status REST API or use WebSocket API
            to receive updates about this order.

            Example request body:

            View More
            {
                "side": "BUY",
                "quantity": "0.00015",
                "price": "645055",
                "pair": "BTCZAR",
                "customerOrderId": "56789",
                "timeInForce": "GTC",
                "stopPrice": "644021",
                "type": "STOP_LOSS_LIMIT"
            }
            Parameter	Description
            side (required)	BUY or SELL
            quantity (required)	Amount in Base Currency must be provided.
            price (required)	The Limit Price at which the BUY or SELL order will be placed .
            pair (required)	Can be BTCZAR, ETHZAR or XRPZAR.
            timeInForce (required)	Can be GTC, FOK or IOC. See below for explanation
            stopPrice (required)	The target price for the trade to trigger. Cannot be equal to last traded price.
            type (required)	Can be TAKE_PROFIT_LIMIT or STOP_LOSS_LIMIT.
            customerOrderId (optional)	Alphanumeric value. See below for explanation.
            timeInForce is the duration that an order will remain active, this can be Good Till Cancelled (GTC),
            Fill or Kill (FOK) or Immediate or Cancel (IOC).

            The customerOrderId is an optional field which can be specified by clients to track this order \
            using their own internal order management systems.

            When you retrieve your open orders or history of orders, this field will also be returned along
            with the VALR's orderId for each order for which this field was specified during creation.
            When you cancel an order, you can either specify orderId or customerOrderId, not both.
            customerOrderId is alphanumeric with no special chars, limit of 50 characters.
            The customerOrderId has to be unique across all open orders for a given account. If you do reuse an
            id value that is currently an active open order, your order will not be placed
            (you can check the status of an order using the order status API call).

            PLEASE NOTE: When you receive a response with an id, it does not always mean that the order has been placed.
            When the response is 202 Accepted, you can use the WebSocket API (or Order Status REST API) to
            receive the status of this order. The reasons why an order could fail are as follows:

            Insufficient balance in your account.
            If it would be triggered immediately.
            If you're using a non-unique customerOrderId.
            Self trading: If your order matches against your own order (on the other side).
            Insufficient liquidity: If you're placing an order and there isn't liquidity to fulfil the order.
        """
        data = {
            "side": side,
            "quantity": quantity,
            "price": limit_price,
            "pair": pair,
            "timeInForce": time_in_force,
            "stopPrice": stop_price,
            "type": stop_limit_type
        }
        if customer_order_id:
            data["customerOrderId"] = customer_order_id
        return self._do('POST', '/v1/orders/stop/limit', data=data, is_authenticated=True, subaccount_id=subaccount_id)

    @requires_authentication
    def post_batch_orders(self, batch_requests: List[Dict],
                          subaccount_id: str = '') -> Dict:
        """Create a batch of multiple orders, or cancel orders, in a single request

        Note: This API is still in Alpha phase and we would love to improve the user experience with your feedback.
        We urge you to share any suggestions by logging a quick Feature Request on our Support Portal

        When the response is 200 - OK, this means that the Batch Order has been submitted.
        However, this does not mean that all the orders in the Batch have been executed.

        In the response body will be the outcomes of each of the orders in the batch. Values are true with an orderId
        for accepted orders, or false with a failure message for failed orders.

        Example request body:

        View More
        {
            "requests": [
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
                },
                {
                    "type": "PLACE_LIMIT",
                    "data": {
                        "pair": "ETHZAR",
                        "side": "SELL",
                        "quantity": "0.2",
                        "price": "32000",
                        "postOnly":"false",
                        "timeInForce": "GTC"
                    }
                },
                {
                    "type": "PLACE_STOP_LIMIT",
                    "data": {
                        "pair": "BTCZAR",
                        "side": "BUY",
                        "quantity": "0.0002",
                        "price": "100000",
                        "timeInForce": "GTC",
                        "stopPrice": "110000",
                        "type": "TAKE_PROFIT_LIMIT"
                    }
                },
                {
                    "type": "PLACE_STOP_LIMIT",
                    "data": {
                        "pair": "BTCZAR",
                        "side": "SELL",
                        "quantity": "0.0003",
                        "price": "1150000",
                        "timeInForce": "GTC",
                        "stopPrice": "110000",
                        "type": "STOP_LOSS_LIMIT"
                    }
                },
                {
                    "type": "PLACE_STOP_LIMIT",
                    "data": {
                        "pair": "BTCZAR",
                        "side": "BUY",
                        "quantity": "0.0000002",
                        "price": "100000",
                        "timeInForce": "GTC",
                        "stopPrice": "110000",
                        "type": "STOP_LOSS_LIMIT"
                    }
                    },
                {
                    "type": "CANCEL_ORDER",
                    "data": {
                        "orderId":"e5886f2d-191b-4330-a221-c7b41b0bc553",
                        "pair": "ETHZAR"
                    }
                }
            ]
        }
        Parameter	Description
        type (required)	For each order in the batch, order type being placed.
        Can be PLACE_MARKET, PLACE_LIMIT, PLACE_STOP LIMIT or CANCEL_ORDER
        data (required)	This contains the actual values of each of the order type.
        Must be valid values according to the order type being placed.
        The customerOrderId is an optional field which can be specified by clients to
        track an order using their own internal order management systems.
        This is valid for order types PLACE_MARKET, PLACE_LIMIT and PLACE_STOP LIMIT within the batch.

        customerOrderId has to be unique across all open orders for a given account.
        If you do reuse an id value that is currently an active open order, your order will not be placed
        (you can check the status of an order using the order status API call).

        When you retrieve All Open Orders or Order History the customerOrderId field will also be returned
        along with the VALR's orderId for the orders in which this field was specified in the request.

        customerOrderId is alphanumeric with no special chars, limit of 50 characters.

        For CANCEL_ORDER you can either specify orderId or customerOrderId, not both.

        PLEASE NOTE:

        A maximum of 20 orders may be submitted in a single Batch Orders request.
        Responses for the orders will be returned in the same sequence that they are submitted in the request.
        When you receive a response with accepted: true and an orderId,
        it means that the order has been accepted and will be placed if possible, and filled if matched.
        When the response is 200-OK, you can use the WebSocket API (or Order Status REST API)
        to receive the up to date status each of the orders in the batch by orderId.
        The reasons why an order could fail are as follows:

        Insufficient balance in your account.
        If it would be triggered immediately for any applicable PLACE_STOP_LIMIT orders in the batch .
        If you're using a non-unique customerOrderId.
        Self trading: If your order matches against your own order (on the other side).
        Insufficient liquidity: If you're placing an order and there isn't enough liquidity on the order
        book to fulfil the order.
        Minimum order size is not met. In this case, the response will be accepted:false, with the failure reason.
        """
        warnings.warn('POST Batch Orders still in alpha status at time of valr-python lib develop')
        data = {"requests": batch_requests}
        return self._do('POST', '/v1/batch/orders', data=data, is_authenticated=True, subaccount_id=subaccount_id)

    @requires_authentication
    @check_xor_attrs("order_id", "customer_order_id")
    def get_order_status(self, currency_pair: Union[str, CurrencyPair], order_id: str = "",
                         customer_order_id: str = "", subaccount_id: str = '') -> Dict:
        """Makes a call to GET https://api.valr.com/v1/orders/:currencyPair/orderid/:orderId

        This API returns the status of an order that was placed on the Exchange queried using the id provided by VALR.
        VALR provides an id for every order that is placed on the Exchange.
        Use this id to populate the path variable orderId in this API to query the status of the order.

        Note: If a customerOrderId was also specified while placing the order,
        that customerOrderId will be returned as part of the response.


        OR


        Makes a call to GET https://api.valr.com/v1/orders/:currencyPair/customerorderid/:customerOrderId

        This API returns the status of an order that was placed on the Exchange queried using customerOrderId.
        The customer can specify a customerOrderId while placing an order on the Exchange.
        Use this API to query the order status using that customerOrderId.
        """
        if customer_order_id:
            return self._do('GET', f'/v1/orders/{currency_pair}/customerorderid/{customer_order_id}',
                            is_authenticated=True, subaccount_id=subaccount_id)
        else:
            return self._do('GET', f'/v1/orders/{currency_pair}/orderid/{order_id}', is_authenticated=True,
                            subaccount_id=subaccount_id)

    @requires_authentication
    def get_all_open_orders(self, subaccount_id: str = '') -> List[Dict]:
        """Makes a call to GET https://api.valr.com/v1/orders/open

        Get all open orders for your account.

        A customerOrderId field will be returned in the response for all those orders
        that were created with a customerOrderId field.
        """
        return self._do('GET', '/v1/orders/open', is_authenticated=True, subaccount_id=subaccount_id)

    @requires_authentication
    def get_order_history(self, skip: Optional[int] = None, limit: Optional[int] = 100,
                          subaccount_id: str = '') -> List[Dict]:
        """Makes a call to GET https://api.valr.com/v1/orders/history?skip=0&limit=2

        Get historical orders placed by you.
        """
        opts = {'skip': skip, 'limit': limit}
        params = {k: v for k, v in opts.items() if v}
        return self._do('GET', '/v1/orders/history', params=params, is_authenticated=True,
                        subaccount_id=subaccount_id)

    @requires_authentication
    @check_xor_attrs("order_id", "customer_order_id")
    def get_order_history_summary(self, order_id: str = '', customer_order_id: str = '',
                                  subaccount_id: str = '') -> Dict:
        """Makes a call to GET https://api.valr.com/v1/orders/history/summary/orderid/:orderId

        An order is considered completed when the "Order Status" call returns one of the following statuses:

        "Filled", "Cancelled" or "Failed".

        When this happens, you can get a more detailed summary about this order using this call.
        Orders that are not completed are invalid for this request.


        OR


        Makes a call to GET https://api.valr.com/v1/orders/history/summary/customerorderid/:customerOrderId

        An order is considered completed when the "Order Status" call returns one of the following statuses:

        "Filled", "Cancelled" or "Failed".

        When this happens, you can get a more detailed summary about this order using this call.
        Orders that are not completed are invalid for this request.
        """
        if customer_order_id:
            return self._do('GET', f'/v1/orders/history/summary/customerorderid/{customer_order_id}',
                            is_authenticated=True, subaccount_id=subaccount_id)
        else:
            return self._do('GET', f'/v1/orders/history/summary/orderid/{order_id}', is_authenticated=True,
                            subaccount_id=subaccount_id)

    @requires_authentication
    @check_xor_attrs("order_id", "customer_order_id")
    def get_order_history_detail(self, order_id: str = '', customer_order_id: str = '',
                                 subaccount_id: str = '') -> Dict:
        """Makes a call to GET https://api.valr.com/v1/orders/history/detail/orderid/:orderId

        Get a detailed history of an order's statuses. This call returns an array of "Order Status" objects.
        The latest and most up-to-date status of this order is the zeroth element in the array.


        OR


        Makes a call to GET https://api.valr.com/v1/orders/history/detail/customerorderid/:customerOrderId

        Get a detailed history of an order's statuses. This call returns an array of "Order Status" objects.
        The latest and most up-to-date status of this order is the zeroth element in the array.
        """
        if customer_order_id:
            return self._do('GET', f'/v1/orders/history/detail/customerorderid/{customer_order_id}',
                            is_authenticated=True, subaccount_id=subaccount_id)
        else:
            return self._do('GET', f'/v1/orders/history/detail/orderid/{order_id}', is_authenticated=True,
                            subaccount_id=subaccount_id)

    @requires_authentication
    @check_xor_attrs("order_id", "customer_order_id")
    def delete_order(self, currency_pair: Union[str, CurrencyPair], order_id: str = '', customer_order_id: str = '',
                     subaccount_id: str = '') -> None:
        """Makes a call to DELETE https://api.valr.com/v1/orders/order

        Cancel an open order.

        A 202 Accepted response means the request to cancel the order was accepted.
        You can either use the Order Status REST API or use WebSocket API to receive status update about this request.

        The DELETE request requires a JSON request body in the following format:

        {
          "orderId": "UUID",
          "pair": "BTCZAR"
        }
        Alternatively, the body can be of the following format if you specified a customerOrderId
        when creating your order:

        {
          "customerOrderId": "^[0-9a-zA-Z-]{0,50}$",
          "pair": "BTCZAR"
        }
        NOTE: When you receive this response with an id, it does not always mean that the order has been placed.
        When the response is 202 Accepted, you can either use the Order Status REST API
        or use WebSocket API to receive status update about this order.
        """
        data = {"pair": currency_pair}
        if order_id:
            data["orderId"] = order_id
        else:
            data["customerOrderId"] = customer_order_id
        return self._do('DELETE', '/v1/orders/order', data=data, is_authenticated=True, subaccount_id=subaccount_id)
