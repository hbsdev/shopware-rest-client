# -*- coding: utf-8 -*-

from tests.fixtures.auth import read_conf

def test_create_query_delete(read_conf):

  use_query_plugin = read_conf[5]
  if not use_query_plugin:
    import pytest
    pytest.skip("Query Plugin not installed on server")

  # Create article:
  import random
  a6 = "A%s" % random.randrange(10000,100000) # 10000 - 99999
  a9 = "%s-10" % a6
  number = a9
  import swapi.test_helpers
  ART = swapi.test_helpers.articles_testdata(number)

  # Create API context:
  import swapi.context
  ctx = swapi.context.create(read_conf)

  r = swapi.post(ctx, "articles", ART)
  assert str(r) == '<Response [201]>'

  # Get its id:
  
  import swapi.articles
  id = swapi.articles.id_for(ctx, number)
  assert id is not None

  # Now find it using the query resource:

  assert id == swapi.articles.id_for_startswith(ctx, a6)

  r = swapi.articles.dodelete_by_number(ctx, number, forgive = False)
  assert swapi.articles.exists(ctx, number) == False

def test_ensure(read_conf):

  use_query_plugin = read_conf[5]
  if not use_query_plugin:
    import pytest
    pytest.skip("Query Plugin not installed on server")

  # Create article:
  number = "A0001"
  import swapi.test_helpers
  ART = swapi.test_helpers.articles_testdata(number)

  # Create API context:
  import swapi.context
  ctx = swapi.context.create(read_conf)

  # Delete and forgive if not existed:
  import swapi.articles
  r = swapi.articles.dodelete_by_number(ctx, number, forgive = True)

  # Create using ensure
  print("\nCREATE:")
  r = swapi.articles.ensure_by_number(ctx, ART)
  data_post = r.json()
  assert data_post["success"]

  # Update using ensure
  print("OVERWRITE 1:")
  r = swapi.articles.ensure_by_number(ctx, ART)
  data_put1 = r.json()
  assert data_put1["success"]

  # both results must have same id:
  assert data_put1["data"]["id"] == data_post["data"]["id"]

  # Update AGAIN using ensure
  print("OVERWRITE 2:")
  r = swapi.articles.ensure_by_number(ctx, ART)
  data_put2 = r.json()
  assert data_put2["success"]

  # results must have same id agin:
  assert data_put2["data"]["id"] == data_post["data"]["id"]

  # Finally delete it:
  print("DELETE:")
  import swapi.articles
  r = swapi.articles.dodelete(ctx, data_put2["data"]["id"])
