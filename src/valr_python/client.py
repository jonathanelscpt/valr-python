import json
import time
from json.decoder import JSONDecodeError
from typing import Dict
from typing import List
from typing import Union

from requests.exceptions import HTTPError

from .base_client import MethodClientABC
from .base_client import sign_request
from .exceptions import APIError
from .exceptions import APIException
from .exceptions import RequiresAuthentication


class Client(MethodClientABC):
    """
        Python SDK for the VALR API.

            >>> from valr_python import Client
            >>> c = Client(api_key='api_key', api_secret='api_secret')
            >>> try:
            ...     res = c.get_market_summary()
            ...     print(res)
            ... except Exception as e:
            ...     print(e)
            ...
        """

    def _do(self, method: str, path: str, is_authenticated: bool = False,
            data: Dict = None) -> Union[List, Dict, None]:
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
            timestamp = int(time.time() * 1000)
            headers["X-VALR-API-KEY"] = self._api_key
            headers["X-VALR-SIGNATURE"] = sign_request(api_secret=self._api_secret, timestamp=timestamp,
                                                       method=method, path=path, body=params)
            headers["X-VALR-TIMESTAMP"] = str(timestamp)  # str or byte req for request headers
        if data:
            headers["Content-Type"] = "application/json"
        args = dict(timeout=self._timeout, params=params, headers=headers)
        res = self._session.request(method, url, **args)
        try:
            res.raise_for_status()
            e = res.json()
            if 'code' in e and 'message' in e:
                raise APIError(e['code'], e['message'])  # API errors within 200 OK responses
            return e
        except HTTPError as he:
            try:
                e = res.json()
                if 'code' in e and 'message' in e:
                    raise APIError(e['code'], e['message'])
                raise he  # bubble HTTP errors that the VALR API doesn't report on
            except JSONDecodeError:
                pass  # catch and pass json decode failures to outer try
        except JSONDecodeError as jde:
            raise APIException(res.status_code,
                               f'valr-python: unknown API error. HTTP ({res.status_code}): {jde.msg}')
