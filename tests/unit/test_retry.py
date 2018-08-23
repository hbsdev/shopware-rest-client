# -*- coding: utf-8 -*-

'''
pytest tests/unit/test_retry.py
'''

class TestSwapiRetryDecorator():

  def test_catch_NameError(self):
    import swapi.retry as swr

    @swr.retry(retries=3,pause_sec=.0001)
    def difficult_function():
      print(undefined_var) # raises name error

    import pytest
    with pytest.raises(NameError) as excinfo:
      difficult_function()

  def test_catch_Exception(self):
    import swapi.retry as swr

    @swr.retry(retries=3,pause_sec=.0001)
    def difficult_function():
      print(undefined_var) # raises name error

    import pytest
    with pytest.raises(Exception) as excinfo:
      difficult_function()
