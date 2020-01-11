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


@pytest.mark.parametrize('api_key, api_secret',
                         [('api_key', None), (None, 'api_secret'), (None, None), ("", "")])
def test_requires_authentication_failures(api_key, api_secret):
    stub = DecoratorStub(api_secret=api_secret, api_key=api_key)
    with pytest.raises(RequiresAuthentication):
        stub.private_action()


@pytest.mark.parametrize('api_key, api_secret', [('api_key', ' api_secret')])
def test_requires_authentication_successful(api_key, api_secret):
    stub = DecoratorStub(api_secret=api_secret, api_key=api_key)
    assert stub.private_action() is True


@pytest.mark.parametrize('attr1, attr2', [(False, False), (True, True), (None, None)])
def test_check_xor_attrs_failures(attr1, attr2):
    stub = DecoratorStub()
    with pytest.raises(AttributeError):
        stub.xor_function(attr1=attr1, attr2=attr2)


@pytest.mark.parametrize('attr1, attr2', [(True, False), (False, True), (True, None), (None, True)])
def test_check_xor_attrs_successful(attr1, attr2):
    stub = DecoratorStub()
    assert stub.xor_function(attr1=attr1) is True
    assert stub.xor_function(attr2=attr2) is True
