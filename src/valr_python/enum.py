from enum import Enum
from enum import auto

__all__ = (
    'WebSocketType',
    'MessageFeedType',
    'TradeEvent',
    'AccountEvent',
    'OrderStatusType',
    'TransactionType',
    'CurrencyPair',
)


class NameStrEnum(Enum):

    def __str__(self):
        return str(self.name)


class Side(NameStrEnum):
    SELL = auto()
    BUY = auto()


class WebSocketType(Enum):
    ACCOUNT = '/ws/account'
    TRADE = '/ws/trade'


class MessageFeedType(NameStrEnum):
    SUBSCRIBE = auto()
    SUBSCRIBED = auto()
    AUTHENTICATED = auto()
    UNSUPPORTED = auto()
    PING = auto()
    PONG = auto()


class TradeEvent(NameStrEnum):
    AGGREGATED_ORDERBOOK_UPDATE = auto()
    MARKET_SUMMARY_UPDATE = auto()
    NEW_TRADE_BUCKET = auto()
    NEW_TRADE = auto()


class AccountEvent(NameStrEnum):
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


class OrderStatusType(NameStrEnum):
    PLACED = auto()
    FAILED = auto()
    CANCELLED = auto()
    FILLED = auto()
    PARTIALLY_FILLED = auto()
    INSTANT_ORDER_BALANCE_RESERVE_FAILED = auto()
    INSTANT_ORDER_BALANCE_RESERVED = auto()
    INSTANT_ORDER_COMPLETED = auto()


class TransactionType(NameStrEnum):
    LIMIT_BUY = auto()
    LIMIT_SELL = auto()
    MARKET_BUY = auto()
    MARKET_SELL = auto()
    SIMPLE_BUY = auto()
    SIMPLE_SELL = auto()
    MAKER_REWARD = auto()
    BLOCKCHAIN_RECEIVE = auto()
    BLOCKCHAIN_SEND = auto()
    FIAT_DEPOSIT = auto()
    FIAT_WITHDRAWAL = auto()
    REFERRAL_REBATE = auto()
    REFERRAL_REWARD = auto()
    PROMOTIONAL_REBATE = auto()
    INTERNAL_TRANSFER = auto()
    FIAT_WITHDRAWAL_REVERSAL = auto()


class CurrencyPair(NameStrEnum):
    BTCZAR = auto()
    ETHZAR = auto()
    XRPZAR = auto()
