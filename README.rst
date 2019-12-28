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

.. |commits-since| image:: https://img.shields.io/github/commits-since/jonathanelscpt/valr-python/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/jonathanelscpt/valr-python/compare/v0.1.0...master



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

    import valr_python
    valr_python.longest()


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
