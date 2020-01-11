import pytest

from valr_python.decorators import check_xor_attrs
from valr_python.decorators import requires_authentication
from valr_python.exceptions import RequiresAuthentication


class DecoratorStub(object):
    def __init__(self, api_key=None, api_secret=None):
        self._api_key = api_key
        self._api_secret = api_secret

    @requires_authentication
    def private_action(self):
        return True

    @check_xor_attrs('attr1', 'attr2')
    def xor_function(self, attr1=None, attr2=None):  # noqa
        return True


def test_requires_authentication():

    stub = DecoratorStub()
    with pytest.raises(RequiresAuthentication):
        stub.private_action()

    stub._api_key = 'api_key'
    with pytest.raises(RequiresAuthentication):
        stub.private_action()

    stub._api_key = None
    stub._api_secret = 'api_secret'
    with pytest.raises(RequiresAuthentication):
        stub.private_action()

    stub._api_key = 'api_key'
    stub._api_secret = 'api_secret'
    assert stub.private_action() is True


def test_check_xor_attrs():
    stub = DecoratorStub()

    with pytest.raises(AttributeError):
        stub.xor_function()

    with pytest.raises(AttributeError):
        stub.xor_function(attr1=True, attr2=True)

    assert stub.xor_function(attr1=True) is True
    assert stub.xor_function(attr2=True) is True
