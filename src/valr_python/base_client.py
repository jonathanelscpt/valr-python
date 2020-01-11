import hashlib
import hmac
import time
from abc import ABCMeta
from abc import abstractmethod
from typing import Dict
from typing import List
from typing import Union

import requests

from .decorators import check_xor_attrs
from .decorators import requires_authentication
from .exceptions import RequiresAuthentication

DEFAULT_TIMEOUT = 10


def check_timeout(timeout: int) -> int:
    """Check if request is non-zero and set to 10 if zero.

    :param timeout: HTTP _timeout
    """
    if timeout == 0:
        return DEFAULT_TIMEOUT
    return timeout


class BaseClientABC(metaclass=ABCMeta):
    VALR_API_URL = 'https://api.valr.com'

    def __init__(self, api_key: str = "", api_secret: str = "", timeout: int = DEFAULT_TIMEOUT,
                 base_url: str = "", handle_429_errors: bool = False) -> None:
        """
        :param base_url: base api url
        :param api_key: api key
        :param api_secret: api secret
        :param timeout: http timeout
        :param handle_429_errors: true if 429 error Retry-After header should be honoured
        """
        self._api_key = api_key
        self._api_secret = api_secret
        self._base_url = base_url.rstrip('/') if base_url else self.VALR_API_URL
        self._timeout = check_timeout(timeout)
        self._handle_429_errors = handle_429_errors
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
        self._timeout = check_timeout(value)

    @property
    def base_url(self) -> str:
        return self._base_url

    @base_url.setter
    def base_url(self, value: str) -> None:
        self._base_url = value.rstrip('/') if value else self.VALR_API_URL

    @property
    def handle_429_errors(self) -> bool:
        return self._handle_429_errors

    @handle_429_errors.setter
    def handle_429_errors(self, value: bool) -> None:
        self._handle_429_errors = value

    @abstractmethod
    def _do(self, method: str, path: str, is_authenticated: bool = False,
            data: Dict = None) -> Union[List, Dict, None]:
        raise NotImplementedError

    def _sign_request(self, timestamp: int, method: str, path: str, body: str = "") -> str:
        """Signs the request payload using the api key secret

        :param timestamp: the unix timestamp of this request e.g. int(time.time()*1000)
        :param method: Http method - GET, POST, PUT or DELETE
        :param path: path excluding host name, e.g. '/api/v1/withdraw'
        :param body: http request body as a string, optional
        :return signature hash
        """
        body = body if body else ""
        payload = f"{timestamp}{method.upper()}{path}{body}"
        message = bytearray(payload, 'utf-8')
        signature = hmac.new(bytearray(self._api_secret, 'utf-8'), message, digestmod=hashlib.sha512).hexdigest()
        return signature

    def _get_valr_headers(self, method, path, params):
        valr_headers = {}
        if not (self._api_key and self._api_secret):
            raise RequiresAuthentication("Cannot generate private request without API key/secret.")
        timestamp = int(time.time() * 1000)
        valr_headers["X-VALR-API-KEY"] = self._api_key
        valr_headers["X-VALR-SIGNATURE"] = self._sign_request(timestamp=timestamp, method=method, path=path,
                                                              body=params)
        valr_headers["X-VALR-TIMESTAMP"] = str(timestamp)  # str or byte req for request headers
        return valr_headers


class MethodClientABC(BaseClientABC, metaclass=ABCMeta):

    @abstractmethod
    def _do(self, method: str, path: str, is_authenticated: bool = False,
            data: Dict = None) -> Union[List, Dict, None]:
        raise NotImplementedError

    # Public APIs

    def get_order_book_public(self, currency_pair: str) -> Dict[str, List]:
        """Makes a call to GET https://api.valr.com/v1/public/:currencyPair/orderbook

        Returns a list of the top 20 bids and asks in the order book.
        Ask orders are sorted by price ascending.
        Bid orders are sorted by price descending. Orders of the same price are aggregated.

        Please note: This is not an authenticated call.
        More constrained rate-limiting rules will apply than when you use :currencyPair/orderbook route.

        :param currency_pair: Currency pair for which you want to query the order book.
        Supported currency pairs: BTCZAR, ETHZAR
        :return public order book for currency pair
        """
        return self._do('GET', f'/v1/public/{currency_pair}/orderbook')

    def get_currencies(self) -> List[Dict]:
        """Makes a call to GET https://api.valr.com/v1/public/currencies

        Get a list of currencies supported by VALR.

        :return: list of currencies
        """
        return self._do('GET', '/v1/public/currencies')

    def get_currency_pairs(self) -> List[Dict]:
        """Makes a call to GET https://api.valr.com/v1/public/pairs

        Get a list of all the currency pairs supported by VALR.

        :return: list of currency pairs
        """
        return self._do('GET', '/v1/public/pairs')

    def get_order_types(self, currency_pair: str = "") -> Union[List[Dict], List[str]]:
        """Makes a call to GET https://api.valr.com/v1/public/ordertypes

        Get all the order types supported for all currency pairs.

        An array of currency pairs is returned along with an array of order types for each currency pair.
        You can only place an order that is supported by that currency pair.


        OR


        Makes a call to GET https://api.valr.com/v1/public/:currencyPair/ordertypes

        Get the order types supported for a given currency pair.

        An array of order types is returned. You can only place an order that is listed in this
        array for this currency pair.


        :param currency_pair: Specify the currency pair for which you want to query the order types.
        Examples: BTCZAR, ETHZAR, ADABTC, ADAETH etc.
        :return: list of order types
        """
        if currency_pair:
            return self._do('GET', f'/v1/public/{currency_pair}/ordertypes')
        else:
            return self._do('GET', '/v1/public/ordertypes')

    def get_market_summary(self, currency_pair: str = "") -> Union[List[Dict], Dict]:
        """Makes a call to GET https://api.valr.com/v1/public/marketsummary

        Get the market summary for all supported currency pairs.


        OR


        Makes a call to GET https://api.valr.com/v1/public/:currencyPair/marketsummary

        Get the market summary for a given currency pair.

        :param currency_pair: Specify the currency pair for which you want to query the order types.
        Examples: BTCZAR, ETHZAR, ADABTC, ADAETH etc.
        :return: summary of market orders
        """
        if currency_pair:
            return self._do('GET', f'/v1/public/{currency_pair}/marketsummary')
        else:
            return self._do('GET', '/v1/public/marketsummary')

    def get_server_time(self) -> Dict:
        """Makes a call to GET https://api.valr.com/v1/public/time

        Get the server time. Please note: The server time is returned in seconds.

        :return: server time
        """
        return self._do('GET', '/v1/public/time')

    # Account APIs

    @requires_authentication
    def get_balances(self) -> List[Dict]:
        """Makes a call to GET https://api.valr.com/v1/account/balances

        Returns the list of all wallets with their respective balances.

        :return: list of wallets with balances
        """
        return self._do('GET', '/v1/account/balances', is_authenticated=True)

    @requires_authentication
    def get_transaction_history(self, skip: int = 0, limit: int = 100) -> List[Dict]:
        """Makes a call to GET https://api.valr.com/v1/account/transactionhistory?skip=0&limit=100

        Transaction history for your account. Note: This API supports pagination.

        :param limit: Limit the number of items returned
        :param skip: Skip number of items from the list

        :return: list of historical transactions
        """
        return self._do('GET', f'/v1/account/transactionhistory?skip={skip}&limit={limit}', is_authenticated=True)

    @requires_authentication
    def get_account_trade_history(self, currency_pair: str, limit: int = 10) -> List[Dict]:
        """Makes a call to GET https://api.valr.com/v1/account/:currencyPair/tradehistory?limit=10

        Get the last 100 recent trades for a given currency pair for your account.
        You can limit the number of trades returned by specifying the `limit` parameter.

        :param currency_pair: Specify the currency pair for which you want to query the trade history.
        Examples: BTCZAR, ETHZAR
        :param limit: Limit the number of items returned
        :return: list of historical trades
        """
        return self._do('GET', f'/v1/account/{currency_pair}/tradehistory?limit={limit}', is_authenticated=True)

    # Crypto Wallet APIs

    @requires_authentication
    def get_deposit_address(self, currency_code: str) -> Dict:
        """Makes a call to GET https://api.valr.com/v1/wallet/crypto/:currencyCode/deposit/address

        Returns the default deposit address associated with currency specified in the path variable `:currencyCode`.

        :param currency_code: Currently, the allowed values here are BTC and ETH.
        :return: currency wallet address
        """
        return self._do('GET', f'/v1/wallet/crypto/{currency_code}/deposit/address', is_authenticated=True)

    @requires_authentication
    def get_withdrawal_info(self, currency_code: str) -> Dict:
        """Makes a call to GET https://api.valr.com/v1/wallet/crypto/:currencyCode/withdraw

        Get all the information about withdrawing a given currency from your VALR account.
        That will include withdrawal costs, minimum withdrawal amount etc.

        :param currency_code: This is the currency code of the currency you want withdrawal information about.
        Examples: BTC, ETH, XRP, ADA, etc.
        :return: currency withdrawal information
        """
        return self._do('GET', f'/v1/wallet/crypto/{currency_code}/withdraw', is_authenticated=True)

    @requires_authentication
    def post_new_crypto_withdrawal(self, currency_code: str, amount: float, address: str,
                                   payment_reference: str = "") -> Dict:
        """Makes a call to POST https://api.valr.com/v1/wallet/crypto/:currencyCode/withdraw

        Withdraw cryptocurrency funds to an address.

        The request body for XRP, XMR, XEM, XLM will accept an optional field called "paymentReference".
        Max length for paymentReference is 256.

        :param currency_code: This is the currency code of the currency you want withdrawal information about.
        Examples: BTC, ETH, XRP, ADA, etc.
        :param amount: Amount of currency
        :param address: This is the currency code of the currency you want withdrawal information about.
        Examples: BTC, ETH, XRP, ADA, etc.
        :param payment_reference: optional field called "paymentReference". Max length for paymentReference is 256.
        :return: withdrawal id
        """
        data = {"amount": amount, "address": address}
        if payment_reference:
            data["paymentReference"] = payment_reference
        return self._do('POST', f'/v1/wallet/crypto/{currency_code}/withdraw', data=data, is_authenticated=True)

    @requires_authentication
    def get_withdrawal_status(self, currency_code: str, withdraw_id: str) -> Dict:
        """Makes a call to GET https://api.valr.com/v1/wallet/crypto/:currencyCode/withdraw/:withdrawId

        Check the status of a withdrawal.

        :param currency_code: This is the currency code for the currency you have withdrawn.
        Examples: BTC, ETH, XRP, ADA, etc.
        :param withdraw_id: The unique id that represents your withdrawal request.
        This is provided as a response to the API call to withdraw.
        :return: withdrawal status information
        """
        return self._do('GET', f'/v1/wallet/crypto/{currency_code}/withdraw/{withdraw_id}', is_authenticated=True)

    @requires_authentication
    def get_deposit_history(self, currency_code: str, skip: int = 0, limit: int = 10) -> List[Dict]:
        """Makes a call to GET https://api.valr.com/v1/wallet/crypto/:currencyCode/deposit/history?skip=0&limit=10

        Get the Deposit History records for a given currency.

        :param currency_code: This is the currency code for the currency you have withdrawn.
        Examples: BTC, ETH, XRP, ADA, etc.
        :param skip: Skip number of items from the list.
        :param limit: Limit the number of items returned.
        :return: list of historical deposits
        """
        return self._do('GET', f'/v1/wallet/crypto/{currency_code}/deposit/history?skip={skip}&limit={limit}',
                        is_authenticated=True)

    @requires_authentication
    def get_withdrawal_history(self, currency_code: str, skip: int = 0, limit: int = 10) -> List[Dict]:
        """Makes a call to GET https://api.valr.com/v1/wallet/crypto/:currencyCode/withdraw/history?skip=0&limit=10

        Get Withdrawal History records for a given currency.

        :param currency_code: This is the currency code for the currency you have withdrawn.
        Examples: BTC, ETH, XRP, ADA, etc.
        :param skip: Skip number of items from the list.
        :param limit: Limit the number of items returned.
        :return: list of historical withdrawals
        """
        return self._do('GET', f'/v1/wallet/crypto/{currency_code}/withdraw/history?skip={skip}&limit={limit}',
                        is_authenticated=True)

    # Fiat Wallet APIs

    @requires_authentication
    def get_bank_accounts(self, currency_code: str) -> List[Dict]:
        """Makes a call to GET https://api.valr.com/v1/wallet/fiat/:currencyCode/accounts

        Get a list of bank accounts that are linked to your VALR account.
        Bank accounts can be linked by signing in to your account on www.VALR.com.

        :param currency_code: The currency code for the fiat currency. Supported: ZAR.
        :return: list of bank accounts
        """
        return self._do('GET', f'/v1/wallet/fiat/{currency_code}/accounts', is_authenticated=True)

    @requires_authentication
    def post_new_fiat_withdrawal(self, currency_code: str, linked_bank_account_id: str, amount: float) -> Dict:
        """Makes a call to POST https://api.valr.com/v1/wallet/fiat/:currencyCode/withdraw

        Withdraw your ZAR funds into one of your linked bank accounts.

        :param currency_code: The currency code for the fiat currency. Supported: ZAR.
        :param linked_bank_account_id: bank account for withdrawal
        :param amount: withdrawal amount
        :return: withdrawal transaction id
        """
        data = {"linkedBankAccountId": linked_bank_account_id, "amount": amount}
        return self._do('POST', f'/v1/wallet/fiat/{currency_code}/withdraw', data=data, is_authenticated=True)

    # Market Data APIs

    @requires_authentication
    def get_order_book(self, currency_pair: str) -> Dict[str, List]:
        """Makes a call to GET https://api.valr.com/v1/marketdata/:currencyPair/orderbook

        Returns a list of the top 20 bids and asks in the order book.
        Ask orders are sorted by price ascending.
        Bid orders are sorted by price descending. Orders of the same price are aggregated.

        :param currency_pair: Currency pair for which you want to query the order book.
        Supported currency pairs: BTCZAR.
        :return: order book list of asks and list of bids
        """
        return self._do('GET', f'/v1/marketdata/{currency_pair}/orderbook', is_authenticated=True)

    @requires_authentication
    def get_order_book_full(self, currency_pair: str) -> Dict[str, List]:
        """Makes a call to GET https://api.valr.com/v1/marketdata/:currencyPair/orderbook/full

        Returns a list of all the bids and asks in the order book.
        Ask orders are sorted by price ascending.
        Bid orders are sorted by price descending. Orders of the same price are NOT aggregated..

        :param currency_pair: Currency pair for which you want to query the order book.
        Supported currency pairs: BTCZAR.
        :return: full order book list of asks and list of bids
        """
        return self._do('GET', f'/v1/marketdata/{currency_pair}/orderbook/full', is_authenticated=True)

    @requires_authentication
    def get_market_data_trade_history(self, currency_pair: str, limit: int = 10) -> List[Dict]:
        """Makes a call to GET https://api.valr.com/v1/marketdata/:currencyPair/tradehistory?limit=10

        Get the last 100 recent trades for a given currency pair.
        You can limit the number of trades returned by specifying the limit parameter.

        :param currency_pair: Currency pair for which you want to query the order book.
        Supported currency pairs: BTCZAR.
        :param limit: Limit the number of items returned.
        :return: list of historical trades
        """
        return self._do('GET', f'/v1/marketdata/{currency_pair}/tradehistory?limit={limit}', is_authenticated=True)

    # Simple Buy/Sell APIs

    @requires_authentication
    def post_simple_quote(self, currency_pair: str, pay_in_currency: str, pay_amount: float, side: str) -> Dict:
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

        :param currency_pair: Currency pair to get a simple quote for.
        Any currency pair that supports the "simple" order type, can be specified.
        :param pay_in_currency: crypto currency
        :param pay_amount: crypto currency pay amount
        :param side: side is SELL or BUY
        :return: simple quote data
        """
        data = {"payInCurrency": pay_in_currency, "payAmount": pay_amount, "side": side}
        return self._do('POST', f'/v1/simple/{currency_pair}/quote', data=data, is_authenticated=True)

    @requires_authentication
    def post_simple_order(self, currency_pair: str, pay_in_currency: str, pay_amount: float, side: str) -> Dict:
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

        :param currency_pair: Currency pair to get a simple quote for.
        Any currency pair that supports the "simple" order type, can be specified.
        :param pay_in_currency: crypto currency
        :param pay_amount: crypto currency pay amount
        :param side: side is SELL or BUY
        :return: simple order data
        """
        data = {"payInCurrency": pay_in_currency, "payAmount": pay_amount, "side": side}
        return self._do('POST', f'/v1/simple/{currency_pair}/order', data=data, is_authenticated=True)

    @requires_authentication
    def get_simple_order_status(self, currency_pair: str, order_id: str) -> Dict:
        """Makes a call to GET https://api.valr.com/v1/simple/:currencyPair/order/:orderId

        Get the status of a Simple Buy/Sell order.

        :param currency_pair: Currency pair you want a simple buy/sell quote for.
        Supported currency pairs: BTCZAR.
        :param order_id: Order Id of the order for which you are querying the status.
        :return: simple order data
        """
        return self._do('GET', f'/v1/simple/{currency_pair}/order/{order_id}', is_authenticated=True)

    # Exchange Buy/Sell APIs

    @requires_authentication
    def post_limit_order(self, side: str, quantity: float, price: float, pair: str, post_only: bool = False,
                         customer_order_id: str = "") -> Dict:
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

        :param side: BUY or SELL
        :param quantity: Base amount in BTC
        :param price: Price per coin in ZAR
        :param pair: BTCZAR etc.
        :param post_only: true or false
        :param customer_order_id: Numeric value.
        :return: order id
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
        return self._do('POST', f'/v1/orders/limit', data=data, is_authenticated=True)
    # TODO - check 202 Accepted

    @requires_authentication
    @check_xor_attrs("base_amount", "quote_amount")
    def post_market_order(self, side: str, pair: float, base_amount: float = None, quote_amount: float = None,
                          customer_order_id: str = "") -> Dict:
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

        :param side: BUY or SELL
        :param base_amount: Base amount for SELL (in BTC)
        :param quote_amount: Quote amount for BUY (in ZAR).
        :param pair: BTCZAR etc.
        :param customer_order_id: Numeric value.
        :return: order id
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
        return self._do('POST', f'/v1/orders/market', data=data, is_authenticated=True)
    # TODO - check 202 Accepted

    @requires_authentication
    @check_xor_attrs("order_id", "customer_order_id")
    def get_order_status(self, currency_pair: str, order_id: str = "", customer_order_id: str = "") -> Dict:
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


        :param currency_pair: Currency pair
        :param order_id: Order Id provided by VALR
        :param customer_order_id: Order Id provided by customer when creating the order
        :return: order status data
        """
        if customer_order_id:
            return self._do('GET', f'/v1/orders/{currency_pair}/customerorderid/{customer_order_id}',
                            is_authenticated=True)
        else:
            return self._do('GET', f'/v1/orders/{currency_pair}/orderid/{order_id}', is_authenticated=True)

    @requires_authentication
    def get_all_open_orders(self) -> List[Dict]:
        """Makes a call to GET https://api.valr.com/v1/orders/open

        Get all open orders for your account.

        A customerOrderId field will be returned in the response for all those orders
        that were created with a customerOrderId field.

        :return: list of open orders
        """
        return self._do('GET', f'/v1/orders/open', is_authenticated=True)

    @requires_authentication
    def get_order_history(self, skip: int = 0, limit: int = 2) -> List[Dict]:
        """Makes a call to GET https://api.valr.com/v1/orders/history?skip=0&limit=2

        Get historical orders placed by you.

        :param skip: Skip number of items from the list.
        :param limit: Limit the number of items returned.
        :return: list of historical orders
        """
        return self._do('GET', f'/v1/orders/history?skip={skip}&limit={limit}', is_authenticated=True)

    @requires_authentication
    @check_xor_attrs("order_id", "customer_order_id")
    def get_order_history_summary(self, order_id: str = "", customer_order_id: str = "") -> Dict:
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


        :param order_id: Order Id provided by VALR
        :param customer_order_id: Order Id provided by the customer
        :return: order summary
        """
        if customer_order_id:
            return self._do('GET', f'/v1/orders/history/summary/customerorderid/{customer_order_id}',
                            is_authenticated=True)
        else:
            return self._do('GET', f'/v1/orders/history/summary/orderid/{order_id}', is_authenticated=True)

    @requires_authentication
    @check_xor_attrs("order_id", "customer_order_id")
    def get_order_history_detail(self, order_id: str = "", customer_order_id: str = "") -> Dict:
        """Makes a call to GET https://api.valr.com/v1/orders/history/detail/orderid/:orderId

        Get a detailed history of an order's statuses. This call returns an array of "Order Status" objects.
        The latest and most up-to-date status of this order is the zeroth element in the array.


        OR


        Makes a call to GET https://api.valr.com/v1/orders/history/detail/customerorderid/:customerOrderId

        Get a detailed history of an order's statuses. This call returns an array of "Order Status" objects.
        The latest and most up-to-date status of this order is the zeroth element in the array.


        :param order_id: Order Id provided by VALR
        :param customer_order_id: Order Id provided by the customer
        :return: detailed order history
        """
        if customer_order_id:
            return self._do('GET', f'/v1/orders/history/detail/customerorderid/{customer_order_id}',
                            is_authenticated=True)
        else:
            return self._do('GET', f'/v1/orders/history/detail/orderid/{order_id}', is_authenticated=True)

    @requires_authentication
    @check_xor_attrs("order_id", "customer_order_id")
    def delete_order(self, pair, order_id: str = "", customer_order_id: str = "") -> None:
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

        :param pair: Currency pair
        :param order_id: Order Id provided by VALR
        :param customer_order_id: Order Id provided by the customer
        :return: None
        """
        data = {"pair": pair}
        if order_id:
            data["orderId"] = order_id
        else:
            data["customerOrderId"] = customer_order_id
        return self._do('DELETE', f'/v1/orders/order', data=data, is_authenticated=True)
    # TODO - check 202 Accepted
