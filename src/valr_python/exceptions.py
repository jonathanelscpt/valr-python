class APIError(Exception):
    """API error responses"""
    def __init__(self, code, message):
        self.code = code
        self.message = message


class APIException(Exception):
    """Unhandled API exceptions"""
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message


class RequiresAuthentication(Exception):
    """Request requires API authentication"""
    def __init__(self, message):
        self.message = message


class TooManyRequestsWarning(Warning):
    """HTTP 429 received and handled"""


class IncompleteOrderWarning(Warning):
    """HTTP 202 Accepted response received for incomplete order processing"""
    def __init__(self, message, data):
        self.message = message
        self.data = data
