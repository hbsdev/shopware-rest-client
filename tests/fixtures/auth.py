# -*- coding: utf-8 -*-

import pytest

@pytest.fixture
def read_conf():
  import os
  proto = os.environ.get('SWAPI_PROTO')
  server = os.environ.get('SWAPI_SERVER')
  basepath = os.environ.get('SWAPI_BASEPATH')
  user = os.environ.get('SWAPI_USER')
  key = os.environ.get('SWAPI_KEY')

  return proto, server, basepath, user, key

