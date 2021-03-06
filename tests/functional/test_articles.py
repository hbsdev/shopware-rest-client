# -*- coding: utf-8 -*-

from tests.fixtures.auth import read_conf

def test_articles_get(read_conf):
  import swapi.context
  ctx = swapi.context.create(read_conf)
  r = swapi.get(ctx, "articles")
  assert str(r) == "<Response [200]>"
  j = r.json()
  assert j["success"]
  assert str(type(j["data"])) == "<class 'list'>"
  assert j["total"] >= 0
