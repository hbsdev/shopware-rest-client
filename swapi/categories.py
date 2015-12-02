# -*- coding: utf-8 -*-

from pprint import pprint as pp

import easylog
LOG = easylog.get("SWAPI")

# siehe php signaturen !

def get_raw(ctx, suffix=""):
  import swapi
  return swapi.get(
    ctx,
    "categories",
    suffix=suffix,
    raise_for=True,
  )

def get(ctx, id = None):
  if id is None:
    return get_raw(ctx)
  return get_raw(ctx, "/%s" % id)

def get_all_data(ctx):
  r = get(ctx)
  json = r.json()
  data = r.json()
  if not data["success"]:
    return None
  return json["data"]

def exists(ctx, id):
  import requests.exceptions
  try:
    r = get(ctx, id)
  except requests.exceptions.HTTPError as e:
    if str(e) == "404 Client Error: Not Found":
      return False
    raise
  data = r.json()
  if not data["success"]:
    return False
  return True

def get_data(ctx, id):
  import requests.exceptions
  try:
    r = get(ctx, id)
  except requests.exceptions.HTTPError as e:
    if str(e) == "404 Client Error: Not Found":
      return None
    raise
  #LOG.debug("GET TEXT: %s" % r.text)  
  json = r.json()
  data = r.json()
  if not data["success"]:
    return None
  return json["data"]

def get_filtered(ctx, filter):
  import swapi.filter
  url_parameters = swapi.filter.condition(filter)

  import requests.exceptions
  try:
    r = get_raw(ctx, "/?%s" % url_parameters)
  except requests.exceptions.HTTPError as e:
    if str(e) == "404 Client Error: Not Found":
      return None
    if str(e) == "400 Client Error: Bad Request":
      return None
    raise Exception("Failed get_data_by_number(%s: %s" % (number,str(e)))
  #LOG.debug("GET TEXT: %s" % r.text)  
  json = r.json()
  data = r.json()
  if not data["success"]:
    return None
  return json["data"]

def post(ctx, payload, suffix=""):
  import swapi
  return swapi.post(
    ctx,
    "categories",
    payload,
    suffix=suffix,
    raise_for=True,
  )

def put(ctx, id, payload):
  """
  php: $client->put('categories/193', array(
         'name' => 'New order Name'
       ));
  """

  import swapi
  return swapi.put(
    ctx,
    "categories",
    payload,
    suffix = "/%s" % id,
    raise_for=True,
  )

def set_active(ctx, id, is_active):
  return put(
    ctx,
    id,
    payload = dict(
      active = is_active,
    )
  )

def is_active(ctx, id):
  a = get(ctx, id)
  d = a.json()
  try:
    data = d["data"] # can raise keyerror
  except KeyError:
    return None
  # other exceptions will raise here
  return data["active"]

def pprint(ctx, id):
  r = get(ctx, id)
  d = r.json()
  pp(d)
