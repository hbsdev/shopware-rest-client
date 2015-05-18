# -*- coding: utf-8 -*-

__author__ = 'Kurt Miebach'
__email__ = 'kwmiebach@gmail.com'
__version__ = '0.1.0'

import swapi.log
LOG = swapi.log.create()

def get(ctx, coll, suffix=""):
  # next_action, exception, message, result = handle_context(ctx)
  #if next_action == "return"
  #  return result
  #if next_action == "exception"
  #  raise
  import swapi.http

  conf = ctx["conf"]
  url = "%s%s" % (swapi.http.construct_url(conf, coll), suffix)
  global LOG  # use LOG from the module namespace
  swapi.LOG.debug("Auth user: %s", conf[3])
  auth = swapi.http.construct_auth(conf)
  import requests
  import swapi.http
  last_i = ctx["retry"]["retries"] + 1
  assert last_i > 0
  for i in range(0, last_i):
    import requests.exceptions
    try:
      r = swapi.http.rest_call(
        method = "GET",
        url = url,
        auth = auth,
        fake_error = ctx["fake_error"],
      )

      # All exceptions that the python Requests library 
      # explicitly raises inherit from:
      # requests.exceptions.RequestException
    except requests.exceptions.RequestException as e:
      # in case we are unit testing:
      ctx["fake_error"] = swapi.http.next_error(ctx["fake_error"])
      import traceback
      tb = traceback.format_exc()
      LOG.error("RequestException exception: %s" % tb)
      # are we out of retries?
      if i >= ctx["retry"]["retries"]:
        # then re-raise it!
        raise
    except OSError as e:  # all IO Errors are catched here
      # in case we are unit testing:
      ctx["fake_error"] = swapi.http.next_error(ctx["fake_error"])
      import traceback
      tb = traceback.format_exc()
      LOG.error("OSError exception: %s" % tb)
      # are we out of retries?
      if i >= ctx["retry"]["retries"]:
        # then re-raise it!
        raise
    except Exception:
      import traceback
      tb = traceback.format_exc()
      LOG.error("Unexpected exception: %s" % tb)
      # we need to re-raise it!
      raise
    else:  # no exception
      break  # if it worked, exit the loop now

  rdict = r.json()
  if str(r) == "<Response [200]>":
    swapi.LOG.debug("Response of GET request: %s" % str(r))
    data = rdict.get("data", {})
    info = data
    return True, r, info
  else:
    swapi.LOG.warning("Response of GET request: %s" % str(r))
    message = rdict.get("message", None)
    info = message
    return False, r, info


def post(ctx, coll, payload, suffix=""):
  conf = ctx["conf"]
  import swapi.http
  url = "%s%s" % (swapi.http.construct_url(conf, coll), suffix)
  import swapi
  swapi.LOG.debug("Auth user: %s", conf[3])
  auth = swapi.http.construct_auth(conf)
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
  # active, instock, stockmin, weight, width, length, height, ean, position, minpurchase, purchasesteps,
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
    data = rdict.get("data", {})
    id = data.get("id", None)
    info = id
    swapi.LOG.debug("ID from POST response: %s" % info)
    return True, r, info
  else:
    message = rdict.get("message", None)
    info = message
    swapi.LOG.warning("Message from POST response: %s" % info)
    return False, r, info


def dodelete(ctx, coll, suffix=""):
  conf = ctx["conf"]
  import swapi.http
  url = "%s%s" % (swapi.http.construct_url(conf, coll), suffix)
  import swapi
  swapi.LOG.debug("Auth user: %s", conf[3])
  auth = swapi.http.construct_auth(conf)
  import requests
  r = requests.delete(
    url = url,
    auth = auth,
  )
  rdict = r.json()
  if (str(r) != "<Response [200]>") and (str(r) != "<Response [201]>"):
    swapi.LOG.warning("Response of DELETE request: %s" % str(r))
  else:
    swapi.LOG.debug("Response of DELETE request: %s" % str(r))
  if rdict.get("success", False):
    data = rdict.get("data", {})
    id = data.get("id", None)
    info = id
    swapi.LOG.debug("ID from DELETE response: %s" % info)
    return True, r, info
  else:
    message = rdict.get("message", None)
    info = message
    swapi.LOG.warning("Message from DELETE response: %s" % info)
    return False, r, info
