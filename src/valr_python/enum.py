from enum import Enum
from enum import auto

__all__ = (
    'WebSocketType',
    'MessageFeedType',
    'TradeEvent',
    'AccountEvent',
    'OrderStatusType',
    'CurrencyPair'
)


class WebSocketType(Enum):
    ACCOUNT = '/ws/account'
    TRADE = '/ws/trade'


class MessageFeedType(Enum):
    SUBSCRIBE = auto()
    SUBSCRIBED = auto()
    AUTHENTICATED = auto()
    UNSUPPORTED = auto()
    PING = auto()
    PONG = auto()


class TradeEvent(Enum):
    AGGREGATED_ORDERBOOK_UPDATE = auto()
    MARKET_SUMMARY_UPDATE = auto()
    NEW_TRADE_BUCKET = auto()
    NEW_TRADE = auto()


class AccountEvent(Enum):
    NEW_ACCOUNT_HISTORY_RECORD = auto()
    BALANCE_UPDATE = auto()
    NEW_ACCOUNT_TRADE = auto()
    INSTANT_ORDER_COMPLETED = auto()
    OPEN_ORDERS_UPDATE = auto()
    ORDER_PROCESSED = auto()
    ORDER_STATUS_UPDATE = auto()
    FAILED_CANCEL_ORDER = auto()
    NEW_PENDING_RECEIVE = auto()
    SEND_STATUS_UPDATE = auto()


class OrderStatusType(Enum):
    PLACED = "Placed"
    FAILED = "Failed"
    CANCELLED = "Cancelled"
    FILLED = "Filled"
    PARTIALLY_FILLED = "Partially Filled"
    INSTANT_ORDER_BALANCE_RESERVE_FAILED = "Instant Order Balance Reserve Failed"
    INSTANT_ORDER_BALANCE_RESERVED = "Instant Order Balance Reserved"
    INSTANT_ORDER_COMPLETED = "Instant Order Completed"


class CurrencyPair(Enum):
    BTCZAR = auto()
    ETHZAR = auto()
