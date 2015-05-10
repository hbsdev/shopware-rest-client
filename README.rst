===============================
Shopware REST API client (Proof of concept)
===============================

.. image:: https://img.shields.io/travis/hbsdev/shopware-rest-client.svg
        :target: https://travis-ci.org/hbsdev/shopware-rest-client

Python 3 client library for Shopware 4 REST API

* Free software: Apache License, Version 2.0
* State: Proof of concept
* OS: Unix/Linux and OSX

Install latest release
----------------------

.. code::

  pip install --upgrade https://github.com/hbsdev/shopware-rest-client/raw/master/dist/shopware_rest_client-0.1.0.zip


Test Configuration
------------------

For integration tests a working Shopware 4 installation is required, which
may not be in production. The following environment variables need to be set:

* SW_API_SERVER (e.g. SW_API_SERVER=http://example.com)
* SW_API_USER
* SW_API_KEY

Run a single test
-----------------

Specify fileName.py::className, like so:

    py.test -q -s test_fixtures.py::TestSkip

Paste the file::test information from pytest's console output.


Calling pytest through python
-----------------------------

    python -m pytest ...

This is equivalent to invoking the command line script py.test ... directly.


Stopping pytest after the first failure
---------------------------------------

    py.test -x

Todo
----

* Add logging



