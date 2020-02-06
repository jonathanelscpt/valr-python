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
from valr_python.utils import _get_valr_headers

__all__ = ['ValrWebSocketClient']


def _get_event_type(ws_type: WebSocketType) -> Type[Union[TradeEvent, AccountEvent]]:
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
        self._hooks = {_get_event_type(self._ws_type)[e.upper()]: f for e, f in hooks.items()}
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

    async def run(self):
        headers = _get_valr_headers(api_key=self._api_key, api_secret=self._api_secret, method='GET',
                                    path=self._ws_type.value, params='')
        async with websockets.connect(self._uri, ssl=True, extra_headers=headers) as ws:
            if self._ws_type == WebSocketType.TRADE:
                await ws.send(json.dumps(self._get_trade_subscription_req_data(), default=str))
            async for message in ws:
                data = json.loads(message)
                if data['type'] != 'AUTHENTICATED' and data['type'] != 'SUBSCRIBED':
                    func = self._hooks[_get_event_type(self._ws_type)[data['type']]]
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
