# -*- coding: utf-8 -*-

def describe_articles():
  from tests.fixtures.auth import read_conf

  def articles_get(read_conf):
    import swapi
    ctx = swapi.context.create(read_conf)
    ok, r, info = swapi.get(ctx, "articles")
    assert ok
    assert str(r) == "<Response [200]>"
    j = r.json()
    assert j["success"]
    assert str(type(j["data"])) == "<class 'list'>"
    assert j["total"] >= 0
