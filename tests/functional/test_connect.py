# -*- coding: utf-8 -*-

def server_user_key():
  import os
  server = os.environ.get('SW_API_SERVER')
  user = os.environ.get('SW_API_USER')
  key = os.environ.get('SW_API_KEY')
  return server, user, key


class TestConnect():

  def test_shopware_api_connect(self):
    server, user, key = server_user_key()
    import requests.auth
    response = requests.get(
      # this actually works:
      url = 'http://%s/api/articles' % server,
      auth=requests.auth.HTTPDigestAuth(user, key),
    )
    assert str(response) == "<Response [200]>"
