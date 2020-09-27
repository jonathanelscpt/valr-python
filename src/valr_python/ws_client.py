import asyncio
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Type
from typing import Union

try:
    import simplejson as json
except ImportError:
    import json

import websockets

from valr_python.enum import AccountEvent
from valr_python.enum import CurrencyPair
from valr_python.enum import MessageFeedType
from valr_python.enum import TradeEvent
from valr_python.enum import WebSocketType
from valr_python.exceptions import HookNotFoundError
from valr_python.exceptions import WebSocketAPIException
from valr_python.utils import JSONType
from valr_python.utils import _get_valr_headers

__all__ = ('WebSocketClient',)


def get_event_type(ws_type: WebSocketType) -> Type[Union[TradeEvent, AccountEvent]]:
    return TradeEvent if ws_type == WebSocketType.TRADE else AccountEvent


class WebSocketClient:
    """The WebSocket API is an advanced technology that makes it possible to open a two-way interactive
    communication session between a client and a server. With this API, you can send messages to a server and
    receive event-driven responses without having to poll the server for a reply.


    Example Usage
    ~~~~~~~~~~~~~

    >>> import asyncio
    >>> from typing import Dict
    >>> from pprint import pprint
    >>> from valr_python import WebSocketClient
    >>> from valr_python.enum import TradeEvent
    >>> from valr_python.enum import WebSocketType
    >>>
    >>> def pretty_hook(data: Dict):
    ...    pprint(data)
    >>>
    >>> c = WebSocketClient(api_key='api_key', api_secret='api_secret', currency_pairs=['BTCZAR'],
    ...                     ws_type=WebSocketType.TRADE.name,
    ...                     trade_subscriptions=[TradeEvent.MARKET_SUMMARY_UPDATE.name],
    ...                     hooks={TradeEvent.MARKET_SUMMARY_UPDATE.name : pretty_hook})
    >>> loop = asyncio.get_event_loop()
    >>> loop.run_until_complete(c.run())
    {'currencyPairSymbol': 'BTCZAR',
     'data': {'askPrice': '151601',
              'baseVolume': '314.7631144',
              'bidPrice': '151600',
              'changeFromPrevious': '2.14',
              'created': '2020-02-06T22:47:03.129Z',
              'currencyPairSymbol': 'BTCZAR',
              'highPrice': '152440',
              'lastTradedPrice': '151600',
              'lowPrice': '146765',
              'previousClosePrice': '148410',
              'quoteVolume': '47167382.04552981'},
     'type': 'MARKET_SUMMARY_UPDATE'}

    Connection
    ~~~~~~~~~~

    Our WebSocket API is accessible on the following address: wss://api.valr.com.

    Account WebSocket connection: In order to receive streaming updates about your VALR account, you would
    open up a WebSocket connection to wss://api.valr.com/ws/account

    Trade WebSocket connection: In order to receive streaming updates about Trade data, you would open up a
    WebSocket connection to wss://api.valr.com/ws/trade


    Authentication
    ~~~~~~~~~~~~~~

    Our WebSocket API needs authentication. To authenticate, pass in the following headers to the first
    call that establishes the WebSocket connection.

    X-VALR-API-KEY: Your API Key
    X-VALR-SIGNATURE: Generated signature. The signature is generated using the following parameters:
        Api Secret
        Timestamp of request
        HTTP verb 'GET'
        Path (either /ws/account or /ws/trade)
        Request Body should be empty
    X-VALR-TIMESTAMP: Timestamp of the request

    The headers that are passed to establish the connection are the same 3 headers you pass to
    any authenticated call to the REST API.


    Subscribing to events
    ~~~~~~~~~~~~~~~~~~~~~

    Once you open a connection to Account, you are automatically subscribed to all messages for all events on
    the Account WebSocket connection. You will start receiving message feeds pertaining to your VALR account.
    For example, you will receive messages when your balance is updated or when a new trade is executed on your account.

    On the other hand, when you open a connection to Trade, in order to receive message feeds about trading data, you
    must subscribe to events you are interested in on the Trade WebSocket connection.  For example, if you want to
    receive messages when markets fluctuate, you must send a message on the connection with the following payload:

    {
       "type":"SUBSCRIBE",
       "subscriptions":[
          {
             "event":"MARKET_SUMMARY_UPDATE",
             "pairs":[
                "BTCZAR"
             ]
          }
       ]
    }

    Here, the event you are subscribing to is called MARKET_SUMMARY_UPDATE and the currency pair you are subscribing to
     is an array. We currently only support BTCZAR and ETHZAR. XRPZAR will be added in due course.


    Unsubscribing from events
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    When you are no longer interested in receiving messages for certain events on the Trade WebSocket connection,
    you can send a synthetic "unsubscribe" message. For example, if you want to unsubscribe from MARKET_SUMMARY_UPDATE
    event, you would send a message as follows:

    {
       "type":"SUBSCRIBE",
       "subscriptions":[
          {
             "event":"MARKET_SUMMARY_UPDATE",
             "pairs":[

             ]
          }
       ]
    }


    Staying connected with Ping-Pong messages
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    To ensure that you stay connected to either the Account or Trade WebSocket you can send a "PING" message on the
    WebSocket you wish to monitor. VALR will respond with a PONG event. The message must be as follows:

    {
      "type": "PING"
    }

    Events (On Trade WebSocket)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Here is a list of events you can subscribe to on the Trade WebSocket connection:

    Event	                        Description

    AGGREGATED_ORDERBOOK_UPDATE	    When subscribed to this event for a given currency pair, the client receives the
                                    top 20 bids and asks from the order book for that currency pair.
    MARKET_SUMMARY_UPDATE	        When subscribed to this event for a given currency pair, the client receives a
                                    message feed with the latest market summary for that currency pair.
    NEW_TRADE_BUCKET	            When subscribed to this event for a given currency pair, the client receives the
                                    Open, High, Low, Close data valid for the last 60 seconds.
    NEW_TRADE	                    When subscribed to this event for a given currency pair, the client receives
                                    message feeds with the latest trades that are executed for that currency pair.


    AGGREGATED_ORDERBOOK_UPDATE

    In order to subscribe to AGGREGATED_ORDERBOOK_UPDATE for BTCZAR and ETHZAR, you must send the following message
    on the Trade WebSocket connection once it is opened:

    {
       "type":"SUBSCRIBE",
       "subscriptions":[
          {
             "event":"AGGREGATED_ORDERBOOK_UPDATE",
             "pairs":[
                "BTCZAR",
                "ETHZAR"
             ]
          }
       ]
    }

    To unsubscribe, send the following message:

    {
       "type":"SUBSCRIBE",
       "subscriptions":[
          {
             "event":"AGGREGATED_ORDERBOOK_UPDATE",
             "pairs":[

             ]
          }
       ]
    }


    MARKET_SUMMARY_UPDATE

    In order to subscribe to MARKET_SUMMARY_UPDATE for just BTCZAR, you must send the following message on the
    Trade WebSocket connection once it is opened:

    {
       "type":"SUBSCRIBE",
       "subscriptions":[
          {
             "event":"MARKET_SUMMARY_UPDATE",
             "pairs":[
                "BTCZAR"
             ]
          }
       ]
    }

    To unsubscribe, send the following message:

    {
       "type":"SUBSCRIBE",
       "subscriptions":[
          {
             "event":"MARKET_SUMMARY_UPDATE",
             "pairs":[

             ]
          }
       ]
    }


    NEW_TRADE_BUCKET

    In order to subscribe to NEW_TRADE_BUCKET for BTCZAR as well as ETHZAR, you must send the following message on the
    Trade WebSocket connection once it is opened:

    {
       "type":"SUBSCRIBE",
       "subscriptions":[
          {
             "event":"NEW_TRADE_BUCKET",
             "pairs":[
                "BTCZAR",
                "ETHZAR"
             ]
          }
       ]
    }

    To unsubscribe, send the following message:

    {
       "type":"SUBSCRIBE",
       "subscriptions":[
          {
             "event":"NEW_TRADE_BUCKET",
             "pairs":[

             ]
          }
       ]
    }


    NEW_TRADE

    In order to subscribe to NEW_TRADE just for BTCZAR, you must send the following message on the Trade WebSocket
    connection once it is opened:

    {
       "type":"SUBSCRIBE",
       "subscriptions":[
          {
             "event":"NEW_TRADE",
             "pairs":[
                "BTCZAR"
             ]
          }
       ]
    }

    To unsubscribe, send the following message:

    {
       "type":"SUBSCRIBE",
       "subscriptions":[
          {
             "event":"NEW_TRADE",
             "pairs":[

             ]
          }
       ]
    }


    Message Feeds (On Trade WebSocket)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    As and when events occur, the message feeds come through to the Trade WebSocket connection for the events the client
    has subscribed to. You will find an example message feed for each event specified above.


    AGGREGATED_ORDERBOOK_UPDATE

    Sample message feed:

    {
       "type":"AGGREGATED_ORDERBOOK_UPDATE",
       "currencyPairSymbol":"BTCZAR",
       "data":{
          "Asks":[
             {
                "side":"sell",
                "quantity":"0.005",
                "price":"9500",
                "currencyPair":"BTCZAR",
                "orderCount":1
             },
             {
                "side":"sell",
                "quantity":"0.01",
                "price":"9750",
                "currencyPair":"BTCZAR",
                "orderCount":1
             },
             {
                "side":"sell",
                "quantity":"0.643689",
                "price":"10000",
                "currencyPair":"BTCZAR",
                "orderCount":3
             },
             {
                "side":"sell",
                "quantity":"0.2",
                "price":"11606",
                "currencyPair":"BTCZAR",
                "orderCount":2
             },
             {
                "side":"sell",
                "quantity":"0.67713484",
                "price":"14000",
                "currencyPair":"BTCZAR",
                "orderCount":1
             },
             {
                "side":"sell",
                "quantity":"1",
                "price":"15000",
                "currencyPair":"BTCZAR",
                "orderCount":1
             },
             {
                "side":"sell",
                "quantity":"1",
                "price":"16000",
                "currencyPair":"BTCZAR",
                "orderCount":1
             },
             {
                "side":"sell",
                "quantity":"1",
                "price":"17000",
                "currencyPair":"BTCZAR",
                "orderCount":1
             },
             {
                "side":"sell",
                "quantity":"1",
                "price":"18000",
                "currencyPair":"BTCZAR",
                "orderCount":1
             },
             {
                "side":"sell",
                "quantity":"1",
                "price":"19000",
                "currencyPair":"BTCZAR",
                "orderCount":1
             }
          ],
          "Bids":[
             {
                "side":"buy",
                "quantity":"0.038",
                "price":"9000",
                "currencyPair":"BTCZAR",
                "orderCount":1
             },
             {
                "side":"buy",
                "quantity":"0.1",
                "price":"8802",
                "currencyPair":"BTCZAR",
                "orderCount":1
             },
             {
                "side":"buy",
                "quantity":"0.2",
                "price":"8801",
                "currencyPair":"BTCZAR",
                "orderCount":1
             },
             {
                "side":"buy",
                "quantity":"0.1",
                "price":"8800",
                "currencyPair":"BTCZAR",
                "orderCount":1
             },
             {
                "side":"buy",
                "quantity":"0.1",
                "price":"8700",
                "currencyPair":"BTCZAR",
                "orderCount":1
             },
             {
                "side":"buy",
                "quantity":"0.1",
                "price":"8600",
                "currencyPair":"BTCZAR",
                "orderCount":1
             },
             {
                "side":"buy",
                "quantity":"0.1",
                "price":"8500",
                "currencyPair":"BTCZAR",
                "orderCount":1
             },
             {
                "side":"buy",
                "quantity":"0.1",
                "price":"8400",
                "currencyPair":"BTCZAR",
                "orderCount":1
             },
             {
                "side":"buy",
                "quantity":"0.3",
                "price":"8200",
                "currencyPair":"BTCZAR",
                "orderCount":1
             },
             {
                "side":"buy",
                "quantity":"0.1",
                "price":"8100",
                "currencyPair":"BTCZAR",
                "orderCount":1
             },
             {
                "side":"buy",
                "quantity":"0.1",
                "price":"8000",
                "currencyPair":"BTCZAR",
                "orderCount":1
             },
             {
                "side":"buy",
                "quantity":"1.08027437",
                "price":"1",
                "currencyPair":"BTCZAR",
                "orderCount":3
             }
          ]
       }
    }


    MARKET_SUMMARY_UPDATE

    Sample message feed:

    {
       "type":"MARKET_SUMMARY_UPDATE",
       "currencyPairSymbol":"BTCZAR",
       "data":{
          "currencyPairSymbol":"BTCZAR",
          "askPrice":"9500",
          "bidPrice":"9000",
          "lastTradedPrice":"9500",
          "previousClosePrice":"9000",
          "baseVolume":"0.0551",
          "highPrice":"10000",
          "lowPrice":"9000",
          "created":"2016-04-25T19:41:16.237Z",
          "changeFromPrevious":"5.55"
       }
    }


    NEW_TRADE_BUCKET

    Sample message feed:

    {
       "type":"NEW_TRADE_BUCKET",
       "currencyPairSymbol":"BTCZAR",
       "data":{
          "currencyPairSymbol":"BTCZAR",
          "bucketPeriodInSeconds":60,
          "startTime":"2019-04-25T19:41:00Z",
          "open":"9500",
          "high":"9500",
          "low":"9500",
          "close":"9500",
          "volume":"0"
       }
    }


    NEW_TRADE

    Sample message feed:

    {
       "type":"NEW_TRADE",
       "currencyPairSymbol":"BTCZAR",
       "data":{
          "price":"9500",
          "quantity":"0.001",
          "currencyPair":"BTCZAR",
          "tradedAt":"2019-04-25T19:51:55.393Z",
          "takerSide":"buy"
       }
    }


    Message Feeds (On Account WebSocket)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    As and when events occur, the message feeds come through to the Account WebSocket connection. As mentioned
    previously, the client is automatically subscribed to all events on the Account WebSocket connection as soon as
    the connection is established. That means, the client need not subscribe to events on the Account WebSocket
    connection. That also means that the client cannot unsubscribe from these events.

    Here is a list of events that occur on the Account WebSocket and the corresponding sample message feed:


    NEW_ACCOUNT_HISTORY_RECORD : NEW SUCCESSFUL TRANSACTION

    Sample message feed:

    {
       "type":"NEW_ACCOUNT_HISTORY_RECORD",
       "data":{
          "transactionType":{
             "type":"SIMPLE_BUY",
             "description":"Simple Buy"
          },
          "debitCurrency":{
             "symbol":"R",
             "decimalPlaces":2,
             "isActive":true,
             "shortName":"ZAR",
             "longName":"Rand",
             "supportedWithdrawDecimalPlaces":2
          },
          "debitValue":"10",
          "creditCurrency":{
             "symbol":"BTC",
             "decimalPlaces":8,
             "isActive":true,
             "shortName":"BTC",
             "longName":"Bitcoin",
             "supportedWithdrawDecimalPlaces":8
          },
          "creditValue":"0.00104473",
          "feeCurrency":{
             "symbol":"BTC",
             "decimalPlaces":8,
             "isActive":true,
             "shortName":"BTC",
             "longName":"Bitcoin",
             "supportedWithdrawDecimalPlaces":8
          },
          "feeValue":"0.00000789",
          "eventAt":"2019-04-25T20:36:53.426Z",
          "additionalInfo":{
             "costPerCoin":9500,
             "costPerCoinSymbol":"R",
             "currencyPairSymbol":"BTCZAR"
          }
       }
    }


    BALANCE_UPDATE : BALANCE HAS BEEN UPDATED

    Sample message feed:

    {
       "type":"BALANCE_UPDATE",
       "data":{
          "currency":{
             "symbol":"BTC",
             "decimalPlaces":8,
             "isActive":true,
             "shortName":"BTC",
             "longName":"Bitcoin",
             "supportedWithdrawDecimalPlaces":8
          },
          "available":"0.88738681",
          "reserved":"0.97803484",
          "total":"1.86542165"
       }
    }

    NEW_ACCOUNT_TRADE : NEW TRADE EXECUTED ON YOUR ACCOUNT

    Sample message feed:

    {
       "type":"NEW_ACCOUNT_TRADE",
       "currencyPairSymbol":"BTCZAR",
       "data":{
          "price":"9500",
          "quantity":"0.00105263",
          "currencyPair":"BTCZAR",
          "tradedAt":"2019-04-25T20:36:53.426Z",
          "side":"buy"
       }
    }


    INSTANT_ORDER_COMPLETED: NEW SIMPLE BUY/SELL EXECUTED

    Sample message feed:

    {
       "type":"INSTANT_ORDER_COMPLETED",
       "data":{
          "orderId":"247dc157-bb5b-49af-b476-2f613b780697",
          "success":true,
          "paidAmount":"10",
          "paidCurrency":"R",
          "receivedAmount":"0.00104473",
          "receivedCurrency":"BTC",
          "feeAmount":"0.00000789",
          "feeCurrency":"BTC",
          "orderExecutedAt":"2019-04-25T20:36:53.445"
       }
    }


    OPEN_ORDERS_UPDATE : NEW ORDER ADDED TO OPEN ORDERS

    Sample message feed (all open orders are returned) :

    {
       "type":"OPEN_ORDERS_UPDATE",
       "data":[
          {
             "orderId":"38511e49-a755-4f8f-a2b1-232bae6967dc",
             "side":"sell",
             "remainingQuantity":"0.1",
             "originalPrice":"10000",
             "currencyPair":{
                "id":1,
                "symbol":"BTCZAR",
                "baseCurrency":{
                   "id":2,
                   "symbol":"BTC",
                   "decimalPlaces":8,
                   "isActive":true,
                   "shortName":"BTC",
                   "longName":"Bitcoin",
                   "currencyDecimalPlaces":8,
                   "supportedWithdrawDecimalPlaces":8
                },
                "quoteCurrency":{
                   "id":1,
                   "symbol":"R",
                   "decimalPlaces":2,
                   "isActive":true,
                   "shortName":"ZAR",
                   "longName":"Rand",
                   "currencyDecimalPlaces":2,
                   "supportedWithdrawDecimalPlaces":2
                },
                "shortName":"BTC/ZAR",
                "exchange":"VALR",
                "active":true,
                "minBaseAmount":0.0001,
                "maxBaseAmount":2,
                "minQuoteAmount":10,
                "maxQuoteAmount":100000
             },
             "createdAt":"2019-04-17T19:51:35.776Z",
             "originalQuantity":"0.1",
             "filledPercentage":"0.00",
             "customerOrderId":""
          },
          {
             "orderId":"d1d9f20a-778c-4f4a-98a1-d336da960158",
             "side":"sell",
             "remainingQuantity":"0.1",
             "originalPrice":"10000",
             "currencyPair":{
                "id":1,
                "symbol":"BTCZAR",
                "baseCurrency":{
                   "id":2,
                   "symbol":"BTC",
                   "decimalPlaces":8,
                   "isActive":true,
                   "shortName":"BTC",
                   "longName":"Bitcoin",
                   "currencyDecimalPlaces":8,
                   "supportedWithdrawDecimalPlaces":8
                },
                "quoteCurrency":{
                   "id":1,
                   "symbol":"R",
                   "decimalPlaces":2,
                   "isActive":true,
                   "shortName":"ZAR",
                   "longName":"Rand",
                   "currencyDecimalPlaces":2,
                   "supportedWithdrawDecimalPlaces":2
                },
                "shortName":"BTC/ZAR",
                "exchange":"VALR",
                "active":true,
                "minBaseAmount":0.0001,
                "maxBaseAmount":2,
                "minQuoteAmount":10,
                "maxQuoteAmount":100000
             },
             "createdAt":"2019-04-20T13:48:44.922Z",
             "originalQuantity":"0.1",
             "filledPercentage":"0.00",
             "customerOrderId":"4"
          }
       ]
    }


    ORDER_PROCESSED : ORDER PROCESSED

    Sample message feed:

    {
       "type":"ORDER_PROCESSED",
       "data":{
          "orderId":"247dc157-bb5b-49af-b476-2f613b780697",
          "success":true,
          "failureReason":""
       }
    }


    ORDER_STATUS_UPDATE : ORDER STATUS HAS BEEN UPDATED

    Sample message feed:

    {
       "type":"ORDER_STATUS_UPDATE",
       "data":{
          "orderId":"247dc157-bb5b-49af-b476-2f613b780697",
          "orderStatusType":"Filled",
          "currencyPair":{
             "id":1,
             "symbol":"BTCZAR",
             "baseCurrency":{
                "id":2,
                "symbol":"BTC",
                "decimalPlaces":8,
                "isActive":true,
                "shortName":"BTC",
                "longName":"Bitcoin",
                "currencyDecimalPlaces":8,
                "supportedWithdrawDecimalPlaces":8
             },
             "quoteCurrency":{
                "id":1,
                "symbol":"R",
                "decimalPlaces":2,
                "isActive":true,
                "shortName":"ZAR",
                "longName":"Rand",
                "currencyDecimalPlaces":2,
                "supportedWithdrawDecimalPlaces":2
             },
             "shortName":"BTC/ZAR",
             "exchange":"VALR",
             "active":true,
             "minBaseAmount":0.0001,
             "maxBaseAmount":2,
             "minQuoteAmount":10,
             "maxQuoteAmount":100000
          },
          "originalPrice":"80000",
          "remainingQuantity":"0.01",
          "originalQuantity":"0.01",
          "orderSide":"buy",
          "orderType":"limit",
          "failedReason":"",
          "orderUpdatedAt":"2019-05-10T14:47:24.826Z",
          "orderCreatedAt":"2019-05-10T14:42:37.333Z",
          "customerOrderId":"4"
       }
    }

    orderStatusType can be one of the following values: "Placed", "Failed", "Cancelled", "Filled", "Partially Filled",
    "Instant Order Balance Reserve Failed", "Instant Order Balance Reserved","Instant Order Completed".


    FAILED_CANCEL_ORDER : UNABLE TO CANCEL ORDER

    Sample message feed:

    {
       "type":"FAILED_CANCEL_ORDER",
       "data":{
          "orderId":"247dc157-bb5b-49af-b476-2f613b780697",
          "message":"An error occurred while cancelling your order."
       }
    }

    NEW_PENDING_RECEIVE : NEW PENDING CRYPTO DEPOSIT

    Sample message feed:

    {
       "type":"NEW_PENDING_RECEIVE",
       "data":{
          "currency":{
             "id":3,
             "symbol":"ETH",
             "decimalPlaces":8,
             "isActive":true,
             "shortName":"ETH",
             "longName":"Ethereum",
             "currencyDecimalPlaces":18,
             "supportedWithdrawDecimalPlaces":8
          },
          "receiveAddress":"0xA7Fae2Fd50886b962d46FF4280f595A3982aeAa5",
          "transactionHash":"0x804bbfa946b57fc5ffcb0c37ec02e7503435d19c35bf8eb0b0c6deb289f7009a",
          "amount":0.01,
          "createdAt":"2019-04-25T21:16:28Z",
          "confirmations":1,
          "confirmed":false
       }
    }

    This message feed is sent through every time there is an update to the number of confirmations to this
    pending deposit.


    SEND_STATUS_UPDATE : CRYPTO WITHDRAWAL STATUS UPDATE

    Sample message feed:

    {
       "type":"SEND_STATUS_UPDATE",
       "data":{
          "uniqueId":"beb8a612-1a1a-4d68-9bd3-96d5ea341119",
          "status":"SEND_BROADCASTED",
          "confirmations":0
       }
    }
    """

    _WEBSOCKET_API_URI = 'wss://api.valr.com'
    _ACCOUNT_CONNECTION = f'{_WEBSOCKET_API_URI}{WebSocketType.ACCOUNT.value}'
    _TRADE_CONNECTION = f'{_WEBSOCKET_API_URI}{WebSocketType.TRADE.value}'

    def __init__(self, api_key: str, api_secret: str, hooks: Dict[str, Callable],
                 currency_pairs: Optional[List[str]] = None, ws_type: str = 'trade',
                 trade_subscriptions: Optional[List[str]] = None):
        self._api_key = api_key
        self._api_secret = api_secret
        self._ws_type = WebSocketType[ws_type.upper()]
        self._hooks = {get_event_type(self._ws_type)[e.upper()]: f for e, f in hooks.items()}
        if currency_pairs:
            self._currency_pairs = [CurrencyPair[p.upper()] for p in currency_pairs]
        else:
            self._currency_pairs = [p for p in CurrencyPair]
        if self._ws_type == WebSocketType.ACCOUNT:
            self._uri = self._ACCOUNT_CONNECTION
        else:
            self._uri = self._TRADE_CONNECTION
        if self._ws_type == WebSocketType.TRADE:
            if trade_subscriptions:
                self._trade_subscriptions = [TradeEvent[e] for e in trade_subscriptions]
            else:
                self._trade_subscriptions = [e for e in TradeEvent]
        elif trade_subscriptions:
            raise ValueError(f'trade subscriptions requires ws_type of {WebSocketType.TRADE.name} ')
        else:
            self._trade_subscriptions = None

    async def run(self):
        """Open an async websocket connection, consume responses and executed mapped hooks.  Async hooks are also
        supported.  The method relies on the underlying 'websockets' libraries ping-pong support.  No API-level
        ping-pong messages are sent to keep the connection alive (not necessary).  Support for custom-handling of
        websockets.exceptions.ConnectionClosed must be handled in the application.
        """
        headers = _get_valr_headers(api_key=self._api_key, api_secret=self._api_secret, method='GET',
                                    path=self._ws_type.value, data='')
        async with websockets.connect(self._uri, ssl=True, extra_headers=headers) as ws:
            if self._ws_type == WebSocketType.TRADE:
                await ws.send(self.get_subscribe_data(self._currency_pairs, self._trade_subscriptions))
            async for message in ws:
                data = json.loads(message)
                try:
                    # ignore auth and subscription response messages
                    if data['type'] not in (MessageFeedType.SUBSCRIBED.name, MessageFeedType.AUTHENTICATED.name):
                        func = self._hooks[get_event_type(self._ws_type)[data['type']]]
                        # apply hooks to mapped stream events
                        if asyncio.iscoroutinefunction(func):
                            await func(data)
                        else:
                            func(data)
                except KeyError:
                    events = [e.name for e in get_event_type(self._ws_type)]
                    if data['type'] in events:
                        raise HookNotFoundError(f'no hook supplied for {data["type"]} event')
                    raise WebSocketAPIException(f'WebSocket API failed to handle {data["type"]} event: {data}')

    @staticmethod
    def get_subscribe_data(currency_pairs, events) -> JSONType:
        """Get subscription data for ws client request"""
        subscriptions = [{"event": e.name, "pairs": [p.name for p in currency_pairs]} for e in events]
        data = {
            "type": MessageFeedType.SUBSCRIBE.name,
            "subscriptions": subscriptions
        }
        return json.dumps(data, default=str)
