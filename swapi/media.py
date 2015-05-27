# -*- coding: utf-8 -*-

# TODO: verify english names
ALBUM_ID_ARTICLES = -1
ALBUM_ID_BANNER = -2 
ALBUM_ID_EINKAUFSWELTEN = -3 
ALBUM_ID_CAMPAIGNS = -4 # AKTIONEN
ALBUM_ID_NEWSLETTER = -5 
ALBUM_ID_FILES = -6 # DATEIEN
ALBUM_ID_VIDEO = -7 
ALBUM_ID_MUSIC = -8 
ALBUM_ID_OTHER = -9 # SONSTIGES
ALBUM_ID_UNSORTED = -10 # UNSORTIERT
ALBUM_ID_BLOG = -11
ALBUM_ID_SUPPLIER = -12 # HERSTELLER


"""
http://community.shopware.com/REST-API-Medien-Endpunkt_detail_1689.html

id integer (Primärschlüssel) 

albumID integer (Fremdschlüssel)  Album
name  string  
path  string  
description string  

type  string  
extension string  
userId  integer (Fremdschlüssel)  User
created date/time 
fileSize  integer

"""


def get_raw(ctx, suffix=""):
  import swapi
  return swapi.get(ctx, "media", suffix = suffix)

def get(ctx, id = None):
  if id is None:
    return get_raw(ctx)
  return get_raw(ctx, "/%s" % id)

def exists(ctx, id):
  import requests.exceptions
  try:
    r = get(ctx, id)
  except requests.exceptions.HTTPError as e:
    assert str(e) == "404 Client Error: Not Found"
    return False
  return True

def post(ctx, payload, suffix="", raise_for=False):
  import swapi
  return swapi.post(ctx, "media", payload, suffix = suffix, raise_for = raise_for)

def put(ctx, id, payload):
  """PUT oficially not supported with media"""
  import swapi
  return swapi.put(ctx, "media", payload, suffix = "/%s" % id)

def dodelete(ctx, id):
  import swapi
  return swapi.dodelete(ctx, "media", suffix = "/%s" % id)

def pprint(ctx, id):
  """"""
  r = get(ctx, id)
  d = r.json()
  import pprint
  pprint.pprint(d)

def media(
  id = None,
  albumID = None, # int album ID (is it "album" or "albumID" ?)
  name = None, # name for image
  path = None, # original 'path/name.jpg' will be deleted after import
  description = None,
  userId = None, # int
  ):
  res = dict()
  if id is not None:
    res["id"] = id
  if album is not None:
    res["albumID"] = albumID
  if userId is not None:
    res["userId"] = userId
  if name is not None:
    res["name"] = name
  if path is not None:
    res["path"] = path
  if description is not None:
    res["description"] = description
  return res
