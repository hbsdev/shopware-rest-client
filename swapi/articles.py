# -*- coding: utf-8 -*-
import easylog

LOG = easylog.get("SWAPI")

# siehe php signaturen !

def get(ctx, suffix=""):
  import swapi
  return swapi.get(ctx, "articles", suffix = suffix)

def get_by_id(ctx, id):
  return get(ctx, "/%s" % id)

def get_by_number(ctx, number):
  # Artikelnumber = mainDetail.number
  # raises requests.exceptions.HTTPError if not found:
  return get(ctx, "/%s?useNumberAsId=true" % number)

def post(ctx, payload, suffix=""):
  import swapi
  return swapi.post(ctx, "articles", payload, suffix = suffix)

def id_for(ctx, number):
  r = get_by_number(ctx, number)
  data = r.json()
  # data = {'success': True, 'data': {'tax': {'tax': '19.00', 'id': 1, 'name': '19%'}, 'categories': [], ...
  id = data["data"]["id"]
  return id

def exists(ctx, number):
  import requests.exceptions
  try:
    r = get_by_number(ctx, number)
  except requests.exceptions.HTTPError as e:
    assert str(e) == "404 Client Error: Not Found"
    return False
  return True

def dodelete_by_id(ctx, id):
  # Artikelnummer = mainDetail.number
  import swapi
  return swapi.dodelete(ctx, "articles", suffix = "/%s" % id)

def dodelete_by_number(ctx, number, forgive=False):
  # Artikelnummer = mainDetail.number
  ## Deleting articles by number using the API isn't possible as of 2015-MAY
  # return dodelete(ctx,"/%s?useNumberAsId=true" % number)
  if not forgive:
    id = id_for(ctx, number)
    return dodelete_by_id(ctx, id)
  # Do forgive if not exists:
  try:  
    id = id_for(ctx, number)
  except:
    return None
  return dodelete_by_id(ctx, id)
