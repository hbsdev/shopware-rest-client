===============================
Shopware REST API client (Proof of concept)
===============================

.. image:: https://img.shields.io/travis/hbsdev/shopware-rest-client.svg
        :target: https://travis-ci.org/hbsdev/shopware-rest-client

Python 3 client library for Shopware 4 REST API

* Free software: Apache License, Version 2.0
* State: Experimental
* OS: Unix/Linux and OSX

Usage
-----

see tests/functional

.. code::

    ctx = ...
    import swapi.orders
    latest_orders = get_by_ordertime(ctx, "2016-12-29", "2016-12-30")

Swapi uses the requests library: http://docs.python-requests.org/en/master/ - the result of the requests http call is in ctx["json"] after a call.

Dependencies
------------

For some cases the DQL query plugin on the server needs to be installed: https://github.com/kwmiebach/shopware-api-query


Test Configuration
------------------

For integration tests a working Shopware 4 installation is required, which may not be in production.
It is necessary to create at least one supplier manually from the backend before running the tests.
For configuration create a file ./secret -
see ./secret-example

Development
-----------

Use a python 3.4 Virtual environment with pip.

Install dependencies: 

.. code::

  pip install -r requirements.txt

Run tests:

  source ./secret
  py.test

Some ways to invoke pytest
--------------------------

https://gist.github.com/kwmiebach/3fd49612ef7a52b5ce3a
