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

.. |commits-since| image:: https://img.shields.io/github/commits-since/jonathanelscpt/valr-python/v0.1.5.svg
    :alt: Commits since latest release
    :target: https://github.com/jonathanelscpt/valr-python/compare/v0.1.5...master

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
    >>> c = Client(api_key='api_key', api_secret='api_secret')
    >>> try:
    ...     res = c.get_deposit_address(currency_code="ETH")
    ...     print(res)
    ... except Exception as e:
    ...     print(e)
    ...
    {"currency": "ETH", "address": "0xA7Fae2Fd50886b962d46FF4280f595A3982aeAa5"}


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
