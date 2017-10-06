# -*- coding: utf-8 -*-

from tests.fixtures.auth import read_conf
from pprint import pprint as pp
#  https://developers.shopware.com/developers-guide/rest-api/api-resource-customer/

# py.test tests/functional/test_customers.py

def test_check_and_change_active(read_conf):

  import pytest
  pytest.skip("SW 5 vergibt beim Anlegen von Kunden eine abweichende Kundennummer.")
  
  # Create API context:
  import swapi.context
  ctx = swapi.context.create(read_conf)

  # Create customer:
  import random
  number = "%s" % random.randrange(1000000,10000000)
  # number is now a client number with 7 digits as string 

  import swapi.test_helpers
  CUST = swapi.test_helpers.customers_testdata(number)

  # Insert customer into shop db:
  import swapi.customers
  r = swapi.customers.post(ctx, CUST)
  id = swapi.customers.id(r)
  assert str(r) == '<Response [201]>'
  #pp(ctx["json"])
  #pp(r.json())

  # Make sure customer exists:
  assert swapi.customers.exists(ctx, number) == True

  # Make sure is active:
  assert swapi.customers.is_active_by_number(ctx, number)

  # DEACTIVATE:
  r = swapi.customers.set_active_by_number(ctx, number, False)

  # Make sure is INACTIVE NOW:
  assert False == swapi.customers.is_active_by_number(ctx, number)
  # ... should also work with id:
  assert False == swapi.customers.is_active(ctx, id)

  # ACTIVATE CUSTOMER AGAIN:
  r = swapi.customers.set_active_by_number(ctx, number, True)

  # Make sure it is ACTIVE AGAIN:

  assert swapi.customers.is_active_by_number(ctx, number)

  # Delete it:

  r = swapi.customers.dodelete_by_number(ctx, number, forgive = False)

  # Make sure no longer exists: 
  assert swapi.customers.exists(ctx, number) == False
