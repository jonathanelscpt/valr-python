import json
import warnings
from json.decoder import JSONDecodeError
from time import sleep
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from requests.exceptions import HTTPError

from .base_client import MethodClientABC
from .exceptions import APIException
from .exceptions import IncompleteOrderWarning
from .exceptions import TooManyRequestsWarning


class Client(MethodClientABC):
    """
        Python SDK for the VALR API.

            >>> from valr_python import Client
            >>> c = Client(api_key='api_key', api_secret='api_secret')
            >>> try:
            ...     res = c.get_deposit_address(currency_code="ETH")
            ...     print(res)
            ... except Exception as e:
            ...     print(e)
            ...
            {"currency": "ETH", "address": "0xA7Fae2Fd50886b962d46FF4280f595A3982aeAa5"}
        """

    def _do(self, method: str, path: str, data: Dict = None,
            is_authenticated: bool = False) -> Optional[Union[List, Dict]]:
        """Executes API request and returns the response.

        Includes HTTP 429 handling by honouring VALR's 429 Retry-After header cool-down.

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
            headers.update(self._get_valr_headers(method=method, path=path, params=params))
        if data:
            headers["Content-Type"] = "application/json"
        args = dict(timeout=self._timeout, params=params, headers=headers)
        res = self._session.request(method, url, **args)

        try:
            res.raise_for_status()
            e = res.json()
            self._raise_for_api_error(e)
            # provide warning with bundled response dict for incomplete transactions
            if res.status_code == 202:
                warnings.warn(IncompleteOrderWarning(data=e, message="Order processing incomplete"))
            return e
        except HTTPError as he:
            if res.status_code == 429:
                if self._handle_rate_limiting:
                    try:
                        retry_after = float(res.headers['Retry-After'])
                        warnings.warn(f"HTTP 429 response received. Applying Retry-After {retry_after}sec back-off",
                                      TooManyRequestsWarning)
                        sleep(retry_after)
                        return self._do(method=method, path=path, is_authenticated=is_authenticated, data=data)
                    except (KeyError, ValueError):
                        raise APIException(res.status_code,
                                           f'valr-python: HTTP 429 processing failed. '
                                           f'HTTP ({res.status_code}): {res.headers}')
                else:
                    # avoid JSONDecodeError - VALR 429 response has html body
                    raise he
            e = res.json()
            self._raise_for_api_error(e)
            # bubble HTTP errors that VALR API doesn't report on
            raise he
        except JSONDecodeError as jde:
            raise APIException(res.status_code,
                               f'valr-python: unknown API error. HTTP ({res.status_code}): {jde.msg}')
