# -*- coding: utf-8 -*-

from tests.fixtures.auth import proto_server_user_key

def test_shopware_api_connect(proto_server_user_key):
  proto, server, user, key = proto_server_user_key
  import requests.auth
  r = requests.get(
    url = '%s://%s/api/articles' % (proto,server),
    auth=requests.auth.HTTPDigestAuth(user, key),
  )
  assert(str(r) == "<Response [200]>")
