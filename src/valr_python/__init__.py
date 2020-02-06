__version__ = '0.1.7'
__all__ = ['ValrWebSocketClient', 'RestClient']
__author__ = 'Jonathan Els'

import decimal
import logging

from valr_python.rest_client import RestClient
from valr_python.ws_client import ValrWebSocketClient

logging.getLogger(__name__).addHandler(logging.NullHandler())

# set decimal precision for projects using sciencebot - also thread-safe
decimal.getcontext().prec = 8
decimal.DefaultContext.prec = 8
