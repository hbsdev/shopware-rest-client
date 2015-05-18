# -*- coding: utf-8 -*-

def describe_ape_connection():
  from tests.fixtures.auth import read_conf

  def shopware_api_connect(read_conf):
    import swapi
    ctx = swapi.context.create(read_conf)
    ok, r, info = swapi.get(ctx, "articles")
    assert (str(r) == "<Response [200]>")
