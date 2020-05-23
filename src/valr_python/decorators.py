from functools import wraps
from typing import List

from valr_python.exceptions import RequiresAuthentication

__all__ = ()


def requires_authentication(func):
    """Decorator to determine private API calls with require authentication"""

    @wraps(func)
    def inner(self, *args, **kwargs):
        if not (self._api_key and self._api_secret):
            raise RequiresAuthentication("cannot generate private request without API key/secret.")
        return func(self, *args, **kwargs)

    return inner


def check_xor_attrs(*xor_args: List[str]):
    """Decorator to check that only one of two attributes was provided in function kwargs"""

    def xor_decorator(func):

        @wraps(func)
        def inner(self, *args, **kwargs):
            if len(xor_args) != 2:
                raise AttributeError("only comparisons of two args supported")
            has_args = [i in kwargs for i in xor_args]
            if not any(has_args) or all(has_args):
                raise AttributeError(f"either {xor_args[0]} or {xor_args[1]} must be provided, but not both.")
            return func(self, *args, **kwargs)

        return inner

    return xor_decorator
