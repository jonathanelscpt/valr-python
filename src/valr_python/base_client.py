import hashlib
import hmac
import json
import time
from json.decoder import JSONDecodeError
from typing import Dict
from typing import List
from typing import Union

import requests

from .exceptions import APIError
from .exceptions import APIException
from .exceptions import RequiresAuthentication

DEFAULT_TIMEOUT = 10


def _sign_request(api_secret: str, timestamp: int, method: str, path: str, body: str = "") -> str:
    """Signs the request payload using the api key secret

    :param api_secret: the api key secret
    :param timestamp: the unix timestamp of this request e.g. int(time.time()*1000)
    :param method: Http method - GET, POST, PUT or DELETE
    :param path: path excluding host name, e.g. '/api/v1/withdraw'
    :param body: http request body as a string, optional
    :return signature hash
    """
    body = body if body else ""
    payload = f"{timestamp}{method.upper()}{path}{body}"
    message = bytearray(payload, 'utf-8')
    signature = hmac.new(bytearray(api_secret, 'utf-8'), message, digestmod=hashlib.sha512).hexdigest()
    return signature


def _check_timeout(timeout: int) -> int:
    """Check if request is non-zero and set to 10 if zero.

    :param timeout: HTTP _timeout
    """
    if timeout == 0:
        return DEFAULT_TIMEOUT
    return timeout


class BaseClient:
    DEFAULT_BASE_URL = 'https://api.valr.com'

    def __init__(self, api_key: str = None, api_secret: str = None, timeout: int = DEFAULT_TIMEOUT,
                 base_url: str = None) -> None:
        """
        :param base_url: base api url
        :param api_key: api key
        :param api_secret: api secret
        :param timeout: http timeout
        """
        self._api_key = api_key
        self._api_secret = api_secret
        self._base_url = base_url.rstrip('/') if base_url else self.DEFAULT_BASE_URL
        self._timeout = _check_timeout(timeout)
        self._session = requests.Session()

    @property
    def api_key(self) -> str:
        return self._api_key

    @api_key.setter
    def api_key(self, value: str) -> None:
        self._api_key = value

    @property
    def api_secret(self) -> str:
        return self._api_secret

    @api_secret.setter
    def api_secret(self, value: str) -> None:
        self._api_secret = value

    @property
    def timeout(self) -> int:
        return self._timeout

    @timeout.setter
    def timeout(self, value: int) -> None:
        self._timeout = _check_timeout(value)

    @property
    def base_url(self) -> str:
        return self._base_url

    @base_url.setter
    def base_url(self, value: str) -> None:
        self._base_url = value.rstrip('/') if value else self.DEFAULT_BASE_URL

    def _do(self, method: str, path: str, is_authenticated: bool = False, data: Dict = None) -> Union[List, Dict, None]:
        """Performs an API request and returns the response.

        TODO: Handle 429s retry with exponential back-off

        :param method: HTTP method (e.g. GET, POST, DELETE, etc.
        :param path: REST API endpoint path
        :param is_authenticated: True if api call requires authentication and signature hashing
        :param data: request data
        :return: HTTP REST API response from VALR
        """
        params = json.loads(json.dumps(data))
        headers = {}
        url = self._base_url + '/' + path.lstrip('/')
        if is_authenticated:
            if not (self._api_key and self._api_secret):
                raise RequiresAuthentication("Cannot generate private request without API key/secret.")
            timestamp = int(time.time()*1000)
            headers["X-VALR-API-KEY"] = self._api_key
            headers["X-VALR-SIGNATURE"] = _sign_request(api_secret=self._api_secret, timestamp=timestamp,
                                                        method=method, path=path, body=params)
            headers["X-VALR-TIMESTAMP"] = str(timestamp)  # str or byte req for request headers
        if data:
            headers["Content-Type"] = "application/json"
        args = dict(timeout=self._timeout, params=params, headers=headers)
        res = self._session.request(method, url, **args)
        try:
            e = res.json()
            if 'code' in e and 'message' in e:
                raise APIError(e['code'], e['message'])
            return e
        except JSONDecodeError as jde:
            raise APIException(res.status_code, f'valr-python: unknown API error. HTTP ({res.status_code}): {jde.msg}')
