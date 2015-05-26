# -*- coding: utf-8 -*-

from tests.fixtures.auth import read_conf

def test_shopware_api_connect(read_conf):
  import swapi.context
  ctx = swapi.context.create(read_conf)
  r = swapi.get(ctx, "articles")
  assert (str(r) == "<Response [200]>")
