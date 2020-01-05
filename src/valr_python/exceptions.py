class APIError(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message


class APIException(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message


class RequiresAuthentication(Exception):
    def __init__(self, message):
        self.message = message
