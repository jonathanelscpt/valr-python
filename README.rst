========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - tests
      - | |travis|
        |
    * - package
      - | |commits-since|

.. |travis| image:: https://api.travis-ci.org/jonathanelscpt/valr-python.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/jonathanelscpt/valr-python

.. |commits-since| image:: https://img.shields.io/github/commits-since/jonathanelscpt/valr-python/v0.1.1.svg
    :alt: Commits since latest release
    :target: https://github.com/jonathanelscpt/valr-python/compare/v0.1.1...master



.. end-badges

Python SDK for the VALR REST API

* Free software: MIT license

Installation
============

::

    pip install valr-python

You can also install the in-development version with::

    pip install https://github.com/jonathanelscpt/valr-python/archive/master.zip


Documentation
=============


To use the project:

.. code-block:: python

    from valr_python import Client

    c = Client(api_key='api_key', api_secret='api_secret')
    try:
        res = c.get_market_summary()
        print(res)
    except Exception as e:
        print(e)


Development
===========

To run the all tests run::

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
