========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1


    * - package
      - | |version| |commits-since|
        | |supported-versions| |supported-implementations| |wheel|
        | |license|
    * - quality
      - | |codacy| |codecov|
    * - tests
      - | |travis|

.. |travis| image:: https://api.travis-ci.org/jonathanelscpt/valr-python.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/jonathanelscpt/valr-python

.. |version| image:: https://img.shields.io/pypi/v/valr-python.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/valr-python

.. |wheel| image:: https://img.shields.io/pypi/wheel/valr-python.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/valr-python

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/valr-python.svg
    :alt: Supported versions
    :target: https://pypi.org/project/valr-python

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/valr-python.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/valr-python

.. |commits-since| image:: https://img.shields.io/github/commits-since/jonathanelscpt/valr-python/v0.1.7.svg
    :alt: Commits since latest release
    :target: https://github.com/jonathanelscpt/valr-python/compare/v0.1.7...master

.. |license| image:: https://img.shields.io/pypi/l/valr-python.svg
    :alt: PyPI License
    :target: https://pypi.org/project/valr-python

.. |codacy| image:: https://api.codacy.com/project/badge/Grade/cb879e2a6be142b88d4e0c2b3a294fb3
    :target: https://www.codacy.com/manual/jonathanelscpt/valr-python?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=jonathanelscpt/valr-python&amp;utm_campaign=Badge_Grade
    :alt: Codacy Code Quality Status

.. |codecov| image:: https://codecov.io/gh/jonathanelscpt/valr-python/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/jonathanelscpt/valr-python
    :alt: Coverage Status


.. end-badges


A Python SDK for the VALR cryptocurrency exchange APIs.


Installation
============

::

    pip install valr-python

You can also install the in-development version with::

    pip install https://github.com/jonathanelscpt/valr-python/archive/master.zip



Authentication
==============

Authenticating to the VALR API requires a valid API Key from the `VALR exchange <https://www.valr.com/>`_.


Synchronous REST API Client
===========================


To use the **synchronous** REST API client:

.. code-block:: python

    >>> from valr_python import Client
    >>> from valr_python.exceptions import IncompleteOrderWarning
    >>>
    >>> c = Client(api_key='api_key', api_secret='api_secret')
    >>> c.rate_limiting_support = True # honour HTTP 429 "Retry-After" header values
    >>> limit_order = {
    ...     "side": "SELL",
    ...     "quantity": 0.1,
    ...     "price": 10000,
    ...     "pair": "BTCZAR",
    ...     "post_only": True,
    ... }
    >>> try:
    ...    res = c.post_limit_order(**limit_order)
    ...    order_id = res['id']
    ...    print(order_id)
    ... except IncompleteOrderWarning as w:  # HTTP 202 Accepted handling for incomplete orders
    ...    order_id = w.data['id']
    ...    print(order_id)
    ... except Exception as e:
    ...    print(e)
    "558f5e0a-ffd1-46dd-8fae-763d93fa2f25"
    >>>


Asynchronous REST API Client
============================

The **synchronous** REST API client is still in development.  Coming soon!


WebSocket API Client
====================

To use the WebSocket API client:


.. code-block:: python

    >>> import asyncio
    >>> from typing import Dict
    >>> from valr_python import WebSocketClient
    >>> from valr_python.enum import TradeEvent
    >>> from valr_python.enum import WebSocketType
    >>>
    >>> def print_hook(data: Dict):
    ...    print(data)
    >>>
    >>> c = WebSocketClient(api_key='api_key', api_secret='api_secret', currency_pairs=['BTCZAR'],
                            ws_type=WebSocketType.TRADE.name,
                            trade_subscriptions=[TradeEvent.AGGREGATED_ORDERBOOK_UPDATE.name,
                                                 TradeEvent.MARKET_SUMMARY_UPDATE.name],
                            hooks={TradeEvent.AGGREGATED_ORDERBOOK_UPDATE.name : print_hook,
                                   TradeEvent.MARKET_SUMMARY_UPDATE.name : print_hook})
    >>> loop = asyncio.get_event_loop()
    >>> loop.run_until_complete(c.run())


This library leverages :code:`websockets` and :code:`asyncio` and is thus a coroutine-based API client.  Both of
VALR's **Account WebSocket connection** and **Trade WebSocket connection** API endpoints are supported.  The SDK fully
supports VALR subscription methods for both endpoints.  Please see the
`VALR API documentation <https://docs.valr.com/>`_ for more information.

For each subscription, a hook must be provided
to process the WS responses.  Failing to do so raises a :code:`HookNotFoundError` exception.  For ease of use,
several :code:`Enum` classes have been implemented (as showcased above) for client instantiation and hook consumption
of API responses. However, client input is accepted in :code:`str` format.

Although not completely minimalistic,
do note that the SDK is implemented as a thin client and implementing parsing of API response streams is left to
the user.


Development
===========

To execute all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox


Donate
======

If this library has helped you, or if you would like to support future development, donations are most welcome:

==============  ==========================================
Cryptocurrency  Address
==============  ==========================================
 **BTC**        38c7QWggrB2HLUJZFmhAC2zh4t8C57c1ec
 **ETH**        0x01eD3b58a07c6d005281Db76e6c1AE2bfF2226AD
==============  ==========================================
