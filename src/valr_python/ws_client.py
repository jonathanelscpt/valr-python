import asyncio
import hashlib
import hmac
import json
import time
import websockets

from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Type
from typing import Union

from valr_websocket.enum import CurrencyPair
from valr_websocket.enum import MessageFeedType
from valr_websocket.enum import TradeEvent
from valr_websocket.enum import AccountEvent
from valr_websocket.enum import WebSocketType
from valr_websocket.exceptions import RequiresAuthentication


def get_event_type(ws_type: WebSocketType) -> Type[Union[TradeEvent, AccountEvent]]:
    return TradeEvent if ws_type == WebSocketType.TRADE else AccountEvent


class ValrWebSocketClient:

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
        self._currency_pairs = [CurrencyPair[p.upper()] for p in currency_pairs] if currency_pairs \
            else [p for p in CurrencyPair]
        self._uri = self._ACCOUNT_CONNECTION if self._ws_type == WebSocketType.ACCOUNT else self._TRADE_CONNECTION
        if self._ws_type == WebSocketType.TRADE:
            self._trade_subscriptions = [TradeEvent[e] for e in trade_subscriptions] if trade_subscriptions \
                else [e for e in TradeEvent]
        elif trade_subscriptions:
            raise ValueError(f'trade subscriptions requires ws_type of {WebSocketType.TRADE.name} ')
        else:
            self._trade_subscriptions = None

    async def handler(self):
        headers = self._get_valr_headers(method='GET', path=self._ws_type.value, params='')
        async with websockets.connect(self._uri, ssl=True, extra_headers=headers) as ws:
            if self._ws_type == WebSocketType.TRADE:
                await ws.send(json.dumps(self._get_trade_subscription_req_data(), default=str))
            async for message in ws:
                data = json.loads(message)
                if data['type'] != 'AUTHENTICATED' and data['type'] != 'SUBSCRIBED':
                    func = self._hooks[get_event_type(self._ws_type)[data['type']]]
                    if asyncio.iscoroutinefunction(func):
                        await func(data)
                    else:
                        func(data)

    def _get_trade_subscription_req_data(self):
        subscriptions = [{"event": s.name, "pairs": [p.name for p in self._currency_pairs]}
                         for s in self._trade_subscriptions]
        return {
            "type": MessageFeedType.SUBSCRIBE.name,
            "subscriptions": subscriptions
        }

    def _get_valr_headers(self, method: str, path: Union[str, WebSocketType], params: Union[str, Dict]) -> Dict:
        """Create signed VALR headers from method, api path and request params

        :param method: HTTP method (e.g. GET, POST, DELETE, etc.
        :param path: REST API endpoint path
        :param params: params dict for request body
        :return: header dict
        """
        valr_headers = {}
        if not (self._api_key and self._api_secret):
            raise RequiresAuthentication("Cannot generate private request without API key/secret.")
        timestamp = int(time.time() * 1000)
        valr_headers["X-VALR-API-KEY"] = self._api_key
        valr_headers["X-VALR-SIGNATURE"] = self._sign_request(timestamp=timestamp, method=method, path=path,
                                                              body=params)
        valr_headers["X-VALR-TIMESTAMP"] = str(timestamp)  # str or byte req for request headers
        return valr_headers

    def _sign_request(self, timestamp: int, method: str, path: str, body: str = "") -> str:
        """Signs the request payload using the api key secret

        :param timestamp: the unix timestamp of this request e.g. int(time.time()*1000)
        :param method: Http method - GET, POST, PUT or DELETE
        :param path: path excluding FQDN
        :param body: http request body as a string, optional
        :return signature hash
        """
        body = body if body else ""
        payload = f"{timestamp}{method.upper()}{path}{body}"
        message = bytearray(payload, 'utf-8')
        signature = hmac.new(bytearray(self._api_secret, 'utf-8'), message, digestmod=hashlib.sha512).hexdigest()
        return signature
