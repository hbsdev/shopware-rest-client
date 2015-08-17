# -*- coding: utf-8 -*-

from tests.fixtures.auth import read_conf

def test_check_and_change_active(read_conf):

  # Create API context:
  import swapi.context
  ctx = swapi.context.create(read_conf)

  number = "A0001"

  # Delete and forgive if not existed:
  import swapi.articles
  r = swapi.articles.dodelete_by_number(ctx, number, forgive = True)

  # Create article:
  import swapi.test_helpers
  ART = swapi.test_helpers.articles_testdata(
    number=number,
  )
  r = swapi.post(ctx, "articles", ART)
  assert str(r) == '<Response [201]>'

  # Make sure it exists:
  assert swapi.articles.exists(ctx, number) == True

  # Make sure it is active:

  assert swapi.articles.is_active_by_number(ctx, number)

  # DEACTIVATE IT:
  r = swapi.articles.set_active_by_number(ctx, number, False)

  # Make sure it is INACTIVE NOW:

  assert False == swapi.articles.is_active_by_number(ctx, number)

  # CTIVATE IT AGAIN:
  r = swapi.articles.set_active_by_number(ctx, number, True)

  # Make sure it is ACTIVE AGAIN:

  assert swapi.articles.is_active_by_number(ctx, number)

  # Delete it:

  r = swapi.articles.dodelete_by_number(ctx, number, forgive = False)
  assert swapi.articles.exists(ctx, number) == False
