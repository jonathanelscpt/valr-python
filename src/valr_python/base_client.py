import hashlib
import hmac
import json
import time
from json.decoder import JSONDecodeError

import requests

from .error import APIError
from .error import RequiresAuthentication

DEFAULT_BASE_URL = 'https://api.valr.com'
DEFAULT_TIMEOUT = 10


def _sign_request(api_secret, timestamp, method, path, body=""):
    """Signs the request payload using the api key secret

    :param api_secret: the api key secret
    :type api_secret: str
    :param timestamp: the unix timestamp of this request e.g. int(time.time()*1000)
    :type timestamp: int
    :param method: Http method - GET, POST, PUT or DELETE
    :type method: str
    :param path: path excluding host name, e.g. '/api/v1/withdraw'
    :type path: str
    :param body: http request body as a string, optional
    :type body: str
    :rtype: str
    """
    payload = f"{timestamp}{method.upper()}{path}{body}"
    message = bytearray(payload, 'utf-8')
    signature = hmac.new(bytearray(api_secret, 'utf-8'), message, digestmod=hashlib.sha512).hexdigest()
    return signature


def _check_timeout(timeout):
    """Check if request is non-zero and set to 10 if zero.

    :param timeout: HTTP _timeout
    :type timeout: int
    :rtype: int
    """
    if timeout == 0:
        return DEFAULT_TIMEOUT
    return timeout


class BaseClient:
    def __init__(self, base_url=None, api_key='', api_secret='', timeout=DEFAULT_TIMEOUT):
        """
        :type base_url: str
        :type timeout: int
        :type api_key: str
        :type api_secret: str
        """
        self._api_key = api_key
        self._api_secret = api_secret
        self._base_url = base_url.rstrip('/') if base_url else DEFAULT_BASE_URL
        self._timeout = _check_timeout(timeout)
        self._session = requests.Session()

    @property
    def api_key(self):
        return self._api_key

    @api_key.setter
    def api_key(self, value):
        self._api_key = value

    @property
    def api_secret(self):
        return self._api_secret

    @api_secret.setter
    def api_secret(self, value):
        self._api_secret = value

    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, value):
        self._timeout = _check_timeout(value)

    @property
    def base_url(self):
        return self._base_url

    @base_url.setter
    def base_url(self, value):
        self._base_url = value.rstrip('/') if value else DEFAULT_BASE_URL

    def _do(self, method, path, is_authenticated=False, data=None):
        """Performs an API request and returns the response.

        TODO: Handle 429s

        :type method: str
        :type path: str
        :type data: object
        :type is_authenticated: bool
        :type method: custom_headers: object
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
            if 'error' in e and 'error_code' in e:
                raise APIError(e['error_code'], e['error'])
            return e
        except JSONDecodeError:
            raise Exception(f'valr-python: unknown API error ({res.status_code})')
