# -*- coding: utf-8 -*-
if __name__ == "__main__":


  from tests.fixtures.auth import read_conf
  conf = read_conf()

  import tests.functional.test_orders
  tests.functional.test_orders.test_sw4_compat(conf)
  import sys
  sys.exit()

  import pytest

  # pass in a string:

  pytest.main("tests/functional/test_orders.py")
