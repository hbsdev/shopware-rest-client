# -*- coding: utf-8 -*-
import easylog

LOG = easylog.get("SWAPI")

# siehe php siganturen !

def get(ctx, suffix=""):
  import swapi
  return swapi.get(ctx, "articles", suffix = suffix)


def get_by_number(ctx, number):
  # Artikelnummer = mainDetail.number
  return get(ctx, "/%s?useNumberAsId=true" % number)


def id_for(ctx, number):
  ok, r, info = get_by_number(ctx, number)
  if not ok:
    return False, r, info
  data = r.json()
  # data = {'success': True, 'data': {'tax': {'tax': '19.00', 'id': 1, 'name': '19%'}, 'categories': [], ...
  try:
    id = data["data"]["id"]
  except:
    return False, r, info
  return ok, r, id


def exists(ctx, number):
  # How Do we handle Timeouts and Network errors? 
  # Not just only here, but this is a good example.
  # --> use the "with" statement http://effbot.org/zone/python-with-statement.htm
  # and define a timeout probably globably
  # - should also handly repetition, delay, pause, "give up"
  # to handle network 
  ok, r, info = get_by_number(ctx, number)
  return ok


def dodelete(ctx, suffix=""):
  import swapi
  return swapi.dodelete(ctx, "articles", suffix = suffix)


def dodelete_by_number(ctx, number, forgive=False):
  # Artikelnummer = mainDetail.number
  ## Deleting articles by number isn't possible as of 2015-MAY
  # return dodelete(ctx,"/%s?useNumberAsId=true" % number)
  ok, r, info = id_for(ctx, number)
  if not ok:
    if forgive:
      return True, None, None
    return False, r, info
  id = info
  return dodelete(ctx, "/%s" % id)


def dodelete_by_id(ctx, id):
  # Artikelnummer = mainDetail.number
  return dodelete(ctx, "/%s" % id)
