# -*- coding: utf-8 -*-

def describe_list():
  import pytest

  @pytest.fixture
  def list():
    return []

  def describe_append():
    def adds_to_end_of_list(list):
      list.append('foo')
      list.append('bar')
      assert list == ['foo', 'bar']

  def describe_remove():
    @pytest.fixture
    def list():
      return ['foo', 'bar']

    def removes_item_from_list(list):
      list.remove('foo')
      assert list == ['bar']
