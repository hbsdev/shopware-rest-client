===============================
Shopware REST API client 
===============================

Python 3 client library for Shopware 4/5 REST API

* OS: Unix/Linux and probably OSX

Licence
---------------------

This is proprietary software. Do not use, copy, or distribute without written permission of the owner. Sourcecode is only for review.

Install latest release
----------------------

.. code::

  pip install --upgrade https://github.com/hbsdev/shopware-rest-client/raw/master/dist/shopware_rest_client-0.1.0.zip


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
