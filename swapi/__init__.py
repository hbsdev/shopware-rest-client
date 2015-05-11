# -*- coding: utf-8 -*-

__author__ = 'Kurt Miebach'
__email__ = 'kwmiebach@gmail.com'
__version__ = '0.1.0'


def construct_auth(conf):
  proto, server, basepath, user, key = conf
  import requests.auth
  auth=requests.auth.HTTPDigestAuth(user, key)
  return auth

def construct_url(conf,coll):
  """
  >>> conf = ("http","example.com", "/subshop/", "api", "key123key")
  >>> construct_url(conf,"articles")
  'http://example.com/subshop/api/articles'

  >>> conf = ("https","example.com", "/", "api", "key123key")
  >>> construct_url(conf,"orders")
  'https://example.com/api/orders'

  """
  proto, server, basepath, user, key = conf
  url = '%s://%s%sapi/%s' % (proto,server,basepath, coll)
  return url

def get(conf,coll,suffix = ""):
  url = "%s%s" % (construct_url(conf,coll), suffix)
  auth = construct_auth(conf)
  import requests
  r = requests.get(
    url = url,
    auth = auth,
  )
  return r
