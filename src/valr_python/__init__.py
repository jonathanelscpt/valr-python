__version__ = '0.2.1'
__author__ = 'Jonathan Els'

import decimal
import logging

from valr_python.rest_client import *  # noqa
from valr_python.ws_client import *  # noqa

__all__ = (rest_client.__all__, ws_client.__all__)


logging.getLogger(__name__).addHandler(logging.NullHandler())

decimal.getcontext().prec = 8
decimal.DefaultContext.prec = 8
