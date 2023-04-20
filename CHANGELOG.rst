
Changelog
=========


0.3.0 (2023-04-20)
------------------

* Added new API features:
* Add fiat bank accounts APIs
* Add VALR Pay APIs
* Added formatting of balances as a convenience function


0.2.7 (2021-12-06)
------------------

* Enum support for SOLZAR


0.2.6 (2021-11-15)
------------------

* added subaccount support
* added all rest api endpoint changes for 2021
* api renaming to align with VALR api docs
* unit tests extended to support endpoint changes and subaccount feature


0.2.5 (2021-11-02)
------------------

* bank fast withdrawal support

0.2.4 (2020-09-27)
------------------

* build stability bugfixes

0.2.3 (2020-09-27)
------------------

* replaced :code:`json` with :code:`simplejson` for speed improvements

0.2.2 (2020-05-25)
------------------

* renamed several sdk methods for API standardization
* added enums for REST API
* added support for simple enum str printing
* added type support for enums
* added XRPZAR support in currency enum

0.2.1 (2020-05-25)
------------------

* :code:`Decimal` support and JSON serialization handling
* added :code:`typing` support for all API calls
* async support for VALR's beta websocket API
* additional api documentation
* build automation extensions

0.1.7 (2020-01-11)
------------------

* Standardised api attribute naming in Client
* Updated doctest and readme for more detailed SDK description

0.1.6 (2020-01-11)
------------------

* Added custom warning :code:`IncompleteOrderWarning` on receiving :code:`202 Accepted` response to support
  custom handling of incomplete orders
* Added custom warning :code:`TooManyRequestsWarning` during 429 handling
* Added class flag for enabling or disabling 429 handler

0.1.5 (2020-01-11)
------------------

* Expanded test suites to unit, functional and live integration testing
* Internal class refactoring
* Added optional HTTP 429 handling by honouring the "Retry-After" header value sent in VALR responses

0.1.4 (2020-01-04)
------------------

* Streamlined ordering api calls with decorators
* Added typing support
* Re-worked class design internals to support later async expansion
* Fixed bugs with str 'None' insertion with f-strings
* Expanded unit tests to cover all api endpoints for synchronous client

0.1.3 (2020-01-02)
------------------

* Fixed defect with empty body signed signatures
* Updated class importing
* Added additional docstrings and unit tests

0.1.2 (2019-12-31)
------------------

* Updated readme and documentation

0.1.1 (2019-12-31)
------------------

* corrected build error issue in setup.py

0.1.0 (2019-12-29)
------------------

* Initial PyPi release

0.0.0 (2019-12-27)
------------------

* Alpha-only. Not released on PyPI.
