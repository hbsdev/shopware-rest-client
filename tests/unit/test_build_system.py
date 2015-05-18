# -*- coding: utf-8 -*-

def describe_build_system():
  def check_helpers():
    import swapi.test_helpers
    assert swapi.test_helpers.ok() == "OK"
