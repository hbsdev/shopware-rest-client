# -*- coding: utf-8 -*-

import doctest2 as doctest #pip install doctest2

def test_auth_docstrings():
  import swapi
  (num_failures, num_attempts) = doctest.testmod(swapi, raise_on_error=False)
  assert num_failures == 0
