# -*- coding: utf-8 -*-

import pytest


@pytest.fixture
def read_conf():
  import os
  proto = os.environ.get('SWAPI_PROTO')
  if proto not in ["http", "https"]:
    raise Exception("Set environment SWAPI_PROTO to 'http' or  'https'.")
  server = os.environ.get('SWAPI_SERVER')
  basepath = os.environ.get('SWAPI_BASEPATH')
  user = os.environ.get('SWAPI_USER')
  key = os.environ.get('SWAPI_KEY')
  if os.environ.get('SWAPI_QUERY_PLUGIN') == "1":
    use_query_plugin = True
  elif os.environ.get('SWAPI_QUERY_PLUGIN') == "0":
    use_query_plugin = False
  else:
    raise Exception("Set environment SWAPI_QUERY_PLUGIN to 0 or 1.")

  return proto, server, basepath, user, key, use_query_plugin

