# -*- coding: utf-8 -*-

import doctest2 as doctest  # pip install doctest2


def test_swapi_docstrings():
  import swapi
  (num_failures, num_attempts) = doctest.testmod(
    swapi,
    raise_on_error = False
    )
  assert num_failures == 0

def test_swapi_http_docstrings():
  import swapi.http
  (num_failures, num_attempts) = doctest.testmod(
    swapi.http,
    raise_on_error = False
    )
  assert num_failures == 0

def test_swapi_context_docstrings():
  import swapi.context
  (num_failures, num_attempts) = doctest.testmod(
    swapi.context,
    raise_on_error = False
    )
  assert num_failures == 0
