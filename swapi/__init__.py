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

  if str(r) != "<Response [200]>":
    # we raise everything else here, also 404
    try:
      rdict = r.json()
    except:
      rdict = dict()
    message = rdict.get("message", None)
    swapi.LOG.debug("Response of GET request: %s, message: %s" % (str(r), message ))
    r.raise_for_status()

  swapi.LOG.debug("Response of GET request: %s" % str(r))
  #rdict = r.json()
  #data = rdict.get("data", {})
  return r


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
  if (str(r) != "<Response [200]>") and ( 
      str(r) != "<Response [201]>"):
    swapi.LOG.warning("Payload: %s" % payload)
    swapi.LOG.warning("Response of POST request: %s" % str(r))
  
  try:
    rdict = r.json()
  except Exception:
    rdict = {}

  swapi.LOG.debug("Response of POST request: %s" % str(r))

  r.raise_for_status() # raises exception for bad response codes

  #if rdict.get("success", False):
  #  ok = True
  #  data = rdict.get("data", {})
  #  id = data.get("id", None)
  #  info = id
  #  swapi.LOG.debug("ID from POST response: %s" % info)
  #else:
  #  ok = False
  #  message = rdict.get("message", None)
  #  info = message
  #  swapi.LOG.warning("Message from POST response: %s" % info)

  return r

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
  if (str(r) == "<Response [200]>") or (str(r) == "<Response [201]>"):
    swapi.LOG.debug("Response of DELETE request: %s" % str(r))
    return r

  swapi.LOG.warning("Response of DELETE request: %s" % str(r))
  r.raise_for_status() # raises exception for bad response codes

  #rdict = r.json()
  #if rdict.get("success", False):
  #  data = rdict.get("data", {})
  #  id = data.get("id", None)
  #  info = id
  #  swapi.LOG.debug("ID from DELETE response: %s" % info)
  #  return True, r, info
  #else:
  #  message = rdict.get("message", None)
  #  info = message
  #  swapi.LOG.warning("Message from DELETE response: %s" % info)
  #  return False, r, info
