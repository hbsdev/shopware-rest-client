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

def apply_hex_blacklist(hex2):
  # sw https://github.com/shopware/shopware/blob/5.2/engine/Shopware/Bundle/MediaBundle/Strategy/Md5Strategy.php#L35
  # ad wird zu g0 um nicht werbefilter, die auf 'ad' reagieren, zu verwirren:  
  if hex2 == 'ad':
    return 'g0'
  return hex2

def md5path8(s):
  '''
  param s: Bild Pfad a la media/image/name.jpg':
  result: 3-gliedriger Pfad, der ans ende des 2-gliedrigen 
  media/xxx/ Pfades angefuegt wird.

  https://forum.shopware.com/discussion/comment/134466/#Comment_134466
  Es sind die ersten 6 Zeichen des MD5-Hashes vom Namen inkl. Pfad ab "media"
  z.B. media/image/bienen_teaser.jpg:
  md5('media/image/bienen_teaser.jpg') = 'a8c36fe5227a5cb5d59a72f5e1d41f71'

  also Verzeichnis: media/image/a8/c3/6f
  '''
  import hashlib; md5 = hashlib.md5(s.encode()).hexdigest()
  return '%s/%s/%s' % (
    apply_hex_blacklist(md5[:2]),
    apply_hex_blacklist(md5[2:4]),
    apply_hex_blacklist(md5[4:6]),
  )

def uri_is_tn(s):
  # wip
  # 'media/image/my-image_100x100.png
  lastpart = s.split('/')[-1]
  tn_parts = s.split('_')
  if len(tn_parts) < 2:
    return False
  if len(tn_parts[1].split('x')) < 2:
    return False
  return True

def deep_uri(s):
  '''
  fuegt 3 Verzeichnisebenen ein, die idR dem linken Teil des md5 code
  von s entsprechen. analog zu SW getUrl
  SW Original: https://developers.shopware.com/developers-guide/shopware-5-media-service/#url-generation    
  echo $mediaService->getUrl('media/image/my-fancy-image.png');
  // result: https://www.myshop.com/media/image/0a/20/03/my-fancy-image.png
  '''
  parts = s.split('/')
  if parts[2] == 'thumbnail':
    del parts[2]
  return '/'.join(
    parts[:-1] +
    [md5path8(s),] +
    parts[-1:]
  )

def flat_uri(s):
  # die umkehrung von deep_uri
  parts = s.split('/')
  assert(len(parts[2])) == 2
  assert(len(parts[3])) == 2
  assert(len(parts[4])) == 2
  return '/'.join(
    parts[:2] +
    parts[5:]
  )

def flat_uri_as_thumbnail(s):
  parts = s.split('/')
  assert len(parts) == 3
  return '/'.join(
    parts[:2] +
    ['thumbnail'] +
    parts[2:]
  )


def verify_deep_uri(s,print_debug=False):
  '''
  assert verify_deep_uri('media/image/06/cf/b1/mp_logo_pp-h100px.png')
  assert verify_deep_uri('media/image/03/97/85/mp_logo.png')
  print('Expected error:')
  assert False == verify_deep_uri('media/image/BO/GU/S!/BOGUS.png')
  '''
  import c.swapi.media
  import imp; imp.reload(c.swapi.media)
  flat1 = flat_uri(s)
  deep2 = deep_uri(flat1)
  if deep2 == s:
    return True
  # it  cold still be a thumbnail:
  flat3 = flat_uri_as_thumbnail(flat1)
  deep3 = deep_uri(flat3)
  if deep3 == s:
    return True
  # verification failed:
  if print_debug:
    print('Deep uri error:')
    print('A. calculated flat uri: %s' % flat1)
    print('B. deep uri input: %s' % s)
    print('C. deep uri from A: %s' % deep2)
    print('D. flat tn uri from A: %s' % flat3)
    print('E. deep uri from D: %s' % deep3)

  return False