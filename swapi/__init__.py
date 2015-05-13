# -*- coding: utf-8 -*-

__author__ = 'Kurt Miebach'
__email__ = 'kwmiebach@gmail.com'
__version__ = '0.1.0'


def _get_swapi_log():
  import easylog

  # 1) If a SWAPI logger was configured already, use that one:
  log = easylog.get("SWAPI")
  if log is not None:
    return log

  #2) Should we log to a file? Look at environment:
  import os
  logfile = os.environ.get('SWAPI_LOGFILE',default=None)
  if logfile is not None:
    log = easylog.create("SWAPI",level="DEBUG",path=logfile)
    return log

  #3) default is a null logger whcih does nothing to not confuse development of the main application
  # see https://docs.python.org/3/howto/logging.html#configuring-logging-for-a-library >
  log = easylog.create("SWAPI",level="WARNING")
  return log

LOG=_get_swapi_log()

def construct_auth(conf):
  proto, server, basepath, user, key = conf
  import requests.auth
  auth=requests.auth.HTTPDigestAuth(user, key)
  return auth

def construct_url(conf,coll):
  """
  >>> conf = ("http","example.com", "/subshop/", "api", "key123key")
  >>> construct_url(conf,"articles")
  'http://example.com/subshop/api/articles'

  >>> conf = ("https","example.com", "/", "api", "key123key")
  >>> construct_url(conf,"orders")
  'https://example.com/api/orders'

  """
  proto, server, basepath, user, key = conf
  url = '%s://%s%sapi/%s' % (proto,server,basepath, coll)
  import swapi
  swapi.LOG.debug("Url constructed: %s", url)
  return url

def get(conf,coll,suffix = ""):
  url = "%s%s" % (construct_url(conf,coll), suffix)
  global LOG # use LOG from the module namespace
  import swapi
  swapi.LOG.debug("Auth user: %s", conf[3])
  auth = construct_auth(conf)
  import requests
  r = requests.get(
    url = url,
    auth = auth,
  )
  if str(r) != "<Response [200]>":
    swapi.LOG.warning("Response of GET request: %s" % str(r))
  else:
    swapi.LOG.debug("Response of GET request: %s" % str(r))
  return r

def post(conf,coll,payload,suffix = ""):
  url = "%s%s" % (construct_url(conf,coll), suffix)
  import swapi
  swapi.LOG.debug("Auth user: %s", conf[3])
  auth = construct_auth(conf)
  import json
  data_json_string = json.dumps(payload)
  import requests
  r = requests.post(
    url = url,
    auth = auth,
    data = data_json_string,
  )
  rdict = r.json()
  # {"success":true,"data":{"id":2,"location":"http:\/\/sw-travis.vhost99.com\/api\/articles\/2"}}
  # ODER:
  # {'message': 'Errormesage: An exception occurred while executing \
  # 'INSERT INTO s_articles_details (articleID, unitID, ordernumber, suppliernumber, kind, additionaltext,
  #  active, instock, stockmin, weight, width, length, height, ean, position, minpurchase, purchasesteps,
  # maxpurchase, purchaseunit, referenceunit, packunit, shippingfree, releasedate, shippingtime) VALUES
  # (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)\
  # ' with params [4, null, "SW456221", null, 1, null, false, null, null, null, null, null, null,
  # null, 0, null, null, null, null, null, null, 0, null, null]:\n\n
  # SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry \'SW456221\' for key
  # \'ordernumber\'', 'success': False}
  if (str(r) != "<Response [200]>") and (str(r) != "<Response [201]>"):
    swapi.LOG.warning("Payload: %s" % payload)
    swapi.LOG.warning("Response of POST request: %s" % str(r))
  else:
    swapi.LOG.debug("Response of POST request: %s" % str(r))
  if rdict.get("success", False):
    data = rdict.get("data",{})
    id = data.get("id", None)
    info = id
    swapi.LOG.debug("ID from POST response: %s" % info)
    return True, r , info
  else:
    message = rdict.get("message",None)
    info = message
    swapi.LOG.warning("Message from POST response: %s" % info)
    return False, r , info

