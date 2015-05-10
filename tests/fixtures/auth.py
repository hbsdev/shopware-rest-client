# -*- coding: utf-8 -*-

import pytest

@pytest.fixture
def proto_server_user_key():
  import os
  proto = os.environ.get('SWAPI_PROTO')
  server = os.environ.get('SWAPI_SERVER')
  user = os.environ.get('SWAPI_USER')
  key = os.environ.get('SWAPI_KEY')

  return proto, server, user, key
