#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_shopware_rest_client
----------------------------------

Tests for the shopware_rest_client module.

http://pytest.org/latest/getting-started.html
https://pytest.org/latest/goodpractises.html

Pytest’s powerful fixture mechanism which leverages the concept of dependency injection:
https://pytest.org/latest/fixture.html#fixture
"""

import unittest

from shopware_rest_client import shopware_rest_client


class TestShopwareRestClient():

  def test_build_system(self):
    import shopware_rest_client.t_helpers
    assert(shopware_rest_client.t_helpers.ok() == "OK")

if __name__ == '__main__':
  unittest.main()
