===============================
Shopware REST API client (Proof of concept)
===============================

.. image:: https://img.shields.io/travis/hbsdev/shopware-rest-client.svg
        :target: https://travis-ci.org/hbsdev/shopware-rest-client

Python 3 client library for Shopware 4 REST API

* Free software: Apache License, Version 2.0
* State: Proof of concept

Install latest release
----------------------

.. code::

  pip install --upgrade https://github.com/hbsdev/shopware-rest-client/raw/master/dist/shopware_rest_client-0.1.0.zip

Dependencies
------------

For some cases the DQL query plugin on the server needs to be installed: https://github.com/kwmiebach/shopware-api-query


Test Configuration
------------------

For integration tests a working Shopware 4 testserver is required. The
following environment variables need to be set:

* SW_API_SERVER (e.g. example.com)
* SW_API_USER
* SW_API_KEY


