# -*- coding: utf-8 -*-

class TestBuildSystem():

  def test_build_system(self):
    import swapi.test_helpers
    assert swapi.test_helpers.ok() == "OK"
