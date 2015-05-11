# -*- coding: utf-8 -*-

from tests.fixtures.auth import read_conf

def test_shopware_api_connect(read_conf):
  import swapi
  r = swapi.get(read_conf,"articles")
  assert(str(r) == "<Response [200]>")
