# -*- coding: utf-8 -*-

__author__ = 'Kurt Miebach'
__email__ = 'kwmiebach@gmail.com'
__version__ = '0.1.0'


from pprint import pprint as pp

# wegen schlechtem ssl cert:
SSL_STRICT_YN = False

import swapi.log
LOG = swapi.log.create()

def debuginfo(ctx, print=False):
  if print:
    print(ctx.get("json1",dict()))
    print(ctx.get("json",dict()))
  return dict(
    json1 = ctx.get("json1",dict()),
    json = ctx.get("json",dict()),
    )

class NetRetry():
  """
  Handle Timeouts and Network errors.
  using the "with" statement
  http://effbot.org/zone/python-with-statement.htm
  Also handle repetition, delay, pause, "give up"
  Define a timeout probably globably
  http://preshing.com/20110920/the-python-with-statement-by-example/
  Re-raise: http://stackoverflow.com/a/18399069/1431660
  """
  def __init__(self, ctx, try_number):
    self.ctx = ctx
    self.try_number = try_number
  def __enter__(self):
    #self.ctx.save()
    #return self.ctx
    pass
  def __exit__(self, etype, evalue, tb):
    # All exceptions that the python Requests library 
    # explicitly raises inherit from:
    # requests.exceptions.RequestException
    if evalue is None:
      return True
    import requests.exceptions
    if isinstance (evalue, requests.exceptions.RequestException):
      # in case we are unit testing:
      self.ctx["fake_error"] = swapi.http.next_error(self.ctx["fake_error"])
      LOG.error("RequestException exception: %s" % tb)
      # are we out of retries?
      if self.try_number >= self.ctx["retry"]["retries"]:
        # then re-raise it!
        return False
      # The exception does not matter,
      # because we are not out of retries yet:
      return True
    elif isinstance (evalue, OSError):
      # all IO Errors are catched here
      # in case we are unit testing:
      self.ctx["fake_error"] = swapi.http.next_error(self.ctx["fake_error"])
      LOG.error("OSError exception: %s" % tb)
      # are we out of retries?
      if self.try_number >= self.ctx["retry"]["retries"]:
        # then re-raise it:
        return False
      # The exception does not matter,
      # because we are not out of retries yet:
      return True
    elif isinstance (evalue, Exception):
      # All other exceptions
      LOG.error("Unexpected exception: %s" % tb)
      # we need to re-raise it!
      return False

def get(ctx, coll, suffix="", raise_for=False):
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
  last_i = ctx["retry"]["retries"] + 1
  assert last_i > 0
  for try_number in range(0, last_i):
    rest_call_ok = False
    with NetRetry(ctx, try_number):
      r = swapi.http.rest_call(
        ctx = ctx,
        method = "GET",
        url = url,
        auth = auth,
        fake_error = ctx["fake_error"],
        )
      # If we get here, then there was no exception:
      rest_call_ok = True
    # We are still in the loop.
    # but if the rest call worked,
    # we must exit the loop now:
    if rest_call_ok:
      break

  # we raise everything else here, also 404
  if raise_for:
    r.raise_for_status()

  return r


def post(ctx, coll, payload, suffix="", raise_for=True):
  conf = ctx["conf"]
  import swapi.http
  url = "%s%s" % (swapi.http.construct_url(conf, coll), suffix)
  import swapi
  swapi.LOG.debug("Auth user: %s", conf[3])
  auth = swapi.http.construct_auth(conf)
  import json
  data_json_string = json.dumps(payload)

  last_i = ctx["retry"]["retries"] + 1
  assert last_i > 0
  for try_number in range(0, last_i):
    rest_call_ok = False
    with NetRetry(ctx, try_number):
      swapi.LOG.debug("POST: %s data: %s" % (url, data_json_string))
      r = swapi.http.rest_call(
        ctx = ctx,
        method = "POST",
        url = url,
        auth = auth,
        data = data_json_string,
        fake_error = ctx["fake_error"],
        )
      # If we get here, then there was no exception:
      rest_call_ok = True
    # We are still in the loop.
    # but if the rest call worked, we must
    # exit the loop now:
    if rest_call_ok:
      break

  if raise_for:
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

def put(ctx, coll, payload, suffix="", raise_for=False):
  conf = ctx["conf"]
  import swapi.http
  url = "%s%s" % (swapi.http.construct_url(conf, coll), suffix)
  import swapi
  swapi.LOG.debug("Auth user: %s", conf[3])
  auth = swapi.http.construct_auth(conf)
  import json
  data_json_string = json.dumps(payload)

  last_i = ctx["retry"]["retries"] + 1
  assert last_i > 0
  for try_number in range(0, last_i):
    rest_call_ok = False
    with NetRetry(ctx, try_number):
      swapi.LOG.debug("PUT: %s data: %s" % (url, data_json_string))
      r = swapi.http.rest_call(
        ctx = ctx,
        method = "PUT",
        url = url,
        auth = auth,
        data = data_json_string,
        fake_error = ctx["fake_error"],
        )
      # If we get here, then there was no exception:
      rest_call_ok = True
    # We are still in the loop.
    # but if the rest call worked, we must
    # exit the loop now:
    if rest_call_ok:
      break

  if raise_for:
    pp(dict(url=url))
    r.raise_for_status() # raises exception for bad response codes

  return r

def id(r):
  id = r.json()["data"]["id"]
  return id

def dodelete(ctx, coll, suffix="", raise_for=False):
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
    verify = SSL_STRICT_YN,
  )
  if (str(r) == "<Response [200]>") or (str(r) == "<Response [201]>"):
    swapi.LOG.debug("Response of DELETE request: %s" % str(r))
    return r

  swapi.LOG.warning("Response of DELETE request: %s" % str(r))

  if raise_for:
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
