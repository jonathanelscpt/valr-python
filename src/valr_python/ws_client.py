import asyncio
import json
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Type
from typing import Union

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

__all__ = ['WebSocketClient']


def _get_event_type(ws_type: WebSocketType) -> Type[Union[TradeEvent, AccountEvent]]:
    return TradeEvent if ws_type == WebSocketType.TRADE else AccountEvent


class WebSocketClient:

    _WEBSOCKET_API_URI = 'wss://api.valr.com'
    _ACCOUNT_CONNECTION = f'{_WEBSOCKET_API_URI}{WebSocketType.ACCOUNT.value}'
    _TRADE_CONNECTION = f'{_WEBSOCKET_API_URI}{WebSocketType.TRADE.value}'

    def __init__(self, api_key: str, api_secret: str, hooks: Dict[str, Callable],
                 currency_pairs: Optional[List[str]] = None, ws_type: str = 'trade',
                 trade_subscriptions: Optional[List[str]] = None):
        self._api_key = api_key
        self._api_secret = api_secret
        self._ws_type = WebSocketType[ws_type.upper()]
        self._hooks = {_get_event_type(self._ws_type)[e.upper()]: f for e, f in hooks.items()}
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

    @asyncio.coroutine
    async def run(self):
        headers = _get_valr_headers(api_key=self._api_key, api_secret=self._api_secret, method='GET',
                                    path=self._ws_type.value, params='')
        async with websockets.connect(self._uri, ssl=True, extra_headers=headers) as ws:
            if self._ws_type == WebSocketType.TRADE:
                await ws.send(self.get_subscribe_data(self._currency_pairs, self._trade_subscriptions))
            async for message in ws:
                data = json.loads(message)
                try:
                    # ignore auth and subscription response messages
                    if data['type'] not in (MessageFeedType.SUBSCRIBED.name, MessageFeedType.AUTHENTICATED.name):
                        func = self._hooks[_get_event_type(self._ws_type)[data['type']]]
                        # apply hooks to mapped stream events
                        if asyncio.iscoroutinefunction(func):
                            await func(data)
                        else:
                            func(data)
                except KeyError:
                    events = [e.name for e in _get_event_type(self._ws_type)]
                    if data['type'] in events:
                        raise HookNotFoundError(f'no hook supplied for {data["type"]} event')
                    raise WebSocketAPIException(f'WebSocket API failed to handle {data["type"]} event: {data}')

    @staticmethod
    def get_subscribe_data(currency_pairs, events) -> JSONType:
        subscriptions = [{"event": e.name, "pairs": [p.name for p in currency_pairs]} for e in events]
        data = {
            "type": MessageFeedType.SUBSCRIBE.name,
            "subscriptions": subscriptions
        }
        return json.dumps(data, default=str)
