# -*- coding: utf-8 -*-

from tests.fixtures.auth import proto_server_user_key

def test_articles(proto_server_user_key):
  proto, server, user, key = proto_server_user_key
  import requests.auth
  # use "list all articles" page for http connection test:
  r = requests.get(
    url = '%s://%s/api/articles' % (proto,server),
    auth=requests.auth.HTTPDigestAuth(user, key),
  )
  assert str(r) == "<Response [200]>"
  j = r.json()
  assert j["success"]
  assert str(type(j["data"])) == "<class 'list'>"
  assert j["total"] >= 0
