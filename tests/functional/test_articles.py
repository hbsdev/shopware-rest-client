# -*- coding: utf-8 -*-

from tests.fixtures.auth import read_conf

def test_articles(read_conf):
  import swapi
  r = swapi.get(read_conf,"articles")
  assert str(r) == "<Response [200]>"
  j = r.json()
  assert j["success"]
  assert str(type(j["data"])) == "<class 'list'>"
  assert j["total"] >= 0
