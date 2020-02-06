__version__ = '0.1.7'
__author__ = 'Jonathan Els'
__all__ = ['WebSocketClient', 'RestClient']


import decimal
import logging

from valr_python.rest_client import RestClient
from valr_python.ws_client import WebSocketClient

logging.getLogger(__name__).addHandler(logging.NullHandler())

# set decimal precision for projects using sciencebot - also thread-safe
decimal.getcontext().prec = 8
decimal.DefaultContext.prec = 8
