#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_shopware_rest_client
----------------------------------

Tests for the shopware_rest_client module.

http://pytest.org/latest/getting-started.html
http://pytest.org/latest/goodpractises.html
http://pytest.org/latest/example/index.html

Pytest’s powerful fixture mechanism which leverages the concept of dependency injection:
http://pytest.org/latest/fixture.html#fixture
"""

import unittest

from shopware_rest_client import shopware_rest_client


class TestBuildSystem():

  def test_build_system(self):
    import shopware_rest_client.test_helpers
    assert shopware_rest_client.test_helpers.ok() == "OK"

if __name__ == '__main__':
  unittest.main()
