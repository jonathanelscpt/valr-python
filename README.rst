========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - tests
      - | |travis|
    * - package
      - | |commits-since|
    * - quality
      - | |codacy|

.. |travis| image:: https://api.travis-ci.org/jonathanelscpt/valr-python.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/jonathanelscpt/valr-python

.. |commits-since| image:: https://img.shields.io/github/commits-since/jonathanelscpt/valr-python/v0.1.7.svg
    :alt: Commits since latest release
    :target: https://github.com/jonathanelscpt/valr-python/compare/v0.1.7...master

.. |codacy| image:: https://api.codacy.com/project/badge/Grade/cb879e2a6be142b88d4e0c2b3a294fb3
    :target: https://www.codacy.com/manual/jonathanelscpt/valr-python?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=jonathanelscpt/valr-python&amp;utm_campaign=Badge_Grade

.. end-badges

Python SDK for the VALR REST API

* Free software: MIT license

Installation
============

::

    pip install valr-python

You can also install the in-development version with::

    pip install https://github.com/jonathanelscpt/valr-python/archive/master.zip



Authentication
==============

Authenticating to the VALR API requires a valid API Key from the `VALR exchange <https://www.valr.com/>`_.


Documentation
=============


To use the project:

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
