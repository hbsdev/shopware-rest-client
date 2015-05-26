# -*- coding: utf-8 -*-

from tests.fixtures.auth import read_conf

def test_not_exists(read_conf):

  number = "A0001"

  # Create API context:
  import swapi.context
  ctx = swapi.context.create(read_conf)

  # Delete and forgive if not existed:
  import swapi.articles
  r = swapi.articles.dodelete_by_number(ctx, number, forgive = True)

  # Article should not exist now:
  assert swapi.articles.exists(ctx, number) == False

def test_delete_not_existing(read_conf):

  number = "A0001"

  # Create API context:
  import swapi.context
  ctx = swapi.context.create(read_conf)

  # Delete and forgive if not existed:
  import swapi.articles
  r = swapi.articles.dodelete_by_number(ctx, number, forgive = True)

  # Try to delete an article that's not there
  # and DO NOT forgive, should raise 404:
 
  import pytest
  import requests.exceptions
  with pytest.raises(requests.exceptions.HTTPError) as einfo:
    import swapi.articles
    r = swapi.articles.dodelete_by_number(ctx, number, forgive = False)
  assert '404 Client Error: Not Found' in str(einfo.value)


def test_create_and_delete(read_conf):

  # Create article:
  number = "A0001"
  import swapi.test_helpers
  ART = swapi.test_helpers.articles_testdata(number)

  # Create API context:
  import swapi.context
  ctx = swapi.context.create(read_conf)

  r = swapi.post(ctx, "articles", ART)
  assert str(r) == '<Response [201]>'

  # Make sure it exists:

  assert swapi.articles.exists(ctx, number)

  # Delete it:

  r = swapi.articles.dodelete_by_number(ctx, number, forgive = False)
  assert swapi.articles.exists(ctx, number) == False
