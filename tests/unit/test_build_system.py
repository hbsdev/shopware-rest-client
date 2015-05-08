# -*- coding: utf-8 -*-

class TestBuildSystem():

  def test_build_system(self):
    import shopware_rest_client.test_helpers
    assert shopware_rest_client.test_helpers.ok() == "OK"
