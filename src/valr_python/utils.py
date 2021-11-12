import decimal
import hashlib
import hmac
import time
from typing import Any
from typing import Dict
from typing import List
from typing import Union

try:
    import simplejson as json
except ImportError:
    import json

from valr_python.enum import WebSocketType
from valr_python.exceptions import RequiresAuthentication

__all__ = ()

JSONType = Union[str, int, float, bool, None, Dict[str, Any], List[Any]]


def _get_valr_headers(api_key: str, api_secret: str, method: str, path: Union[str, WebSocketType],
                      data: str, subaccount_id: str = '') -> Dict:
    """Create signed VALR headers from method, api path and request params

    :param method: HTTP method (e.g. GET, POST, DELETE, etc.
    :param path: REST API endpoint path
    :param data: params dict for request body
    :return: header dict
    """
    valr_headers = {}
    if not (api_key and api_secret):
        raise RequiresAuthentication("Cannot generate private request without API key/secret.")
    timestamp = int(time.time() * 1000)
    valr_headers["X-VALR-API-KEY"] = api_key
    valr_headers["X-VALR-SIGNATURE"] = _sign_request(api_secret=api_secret, timestamp=timestamp,
                                                     method=method, path=path,
                                                     body=data, subaccount_id=subaccount_id)
    valr_headers["X-VALR-TIMESTAMP"] = str(timestamp)  # str or byte req for request headers
    if subaccount_id:
        valr_headers["X-VALR-SUB-ACCOUNT-ID"] = subaccount_id

    return valr_headers


def _sign_request(api_secret: str, timestamp: int, method: str, path: str,
                  body: Union[Dict, str] = "", subaccount_id: str = "") -> str:
    """Signs the request payload using the api key secret

    :param timestamp: the unix timestamp of this request e.g. int(time.time()*1000)
    :param method: Http method - GET, POST, PUT or DELETE
    :param path: path excluding FQDN
    :param body: http request body as a JSON string, optional
    :return signature hash
    """
    body = body if body else ""
    payload = f"{timestamp}{method.upper()}{path}{body}{subaccount_id}"
    message = bytearray(payload, 'utf-8')
    signature = hmac.new(bytearray(api_secret, 'utf-8'), message, digestmod=hashlib.sha512).hexdigest()
    return signature


class DecimalEncoder(json.JSONEncoder):
    """Serialize Decimal obj as str"""
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)
