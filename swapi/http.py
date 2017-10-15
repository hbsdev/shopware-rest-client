import requests.auth
import swapi
import swapi.error


def construct_auth(conf):
  proto, server, basepath, user, key, use_query_plugin, sw4_compat = conf
  import requests.auth
  auth = requests.auth.HTTPDigestAuth(user, key)
  return auth


def construct_url(conf, coll):
  """
  >>> conf = ("http","example.com", "/subshop/", "api", "key123key", 0, 0)
  >>> construct_url(conf,"articles")
  'http://example.com/subshop/api/articles'

  >>> conf = ("https","example.com", "/", "api", "key123key", 0, 0)
  >>> construct_url(conf,"orders")
  'https://example.com/api/orders'

  """
  proto, server, basepath, user, key, use_query_plugin, sw4_compat = conf
  url = '%s://%s%sapi/%s' % (proto, server, basepath, coll)
  import swapi
  swapi.LOG.debug("Url constructed: %s" % url)
  return url


def rest_call(ctx, method, url, auth, data=None, fake_error={}):
  """
  Make HTTP request, do not raise exceptions for http error codes yet.
  Raises fake errors for unittests.
  """
  # 1) Handle fails for unit tests first:
  fails_left = fake_error.get("fail_times", 0)
  if fails_left > 0:
    msg = "%s %s fails, %s fake errors left." % (
      method, url, fails_left - 1)
    swapi.LOG.debug(msg)
    # In most cases we fake IO related errors:
    fake_error_type = fake_error.get("type", "io")
    if fake_error_type == "io":
      msg = "%s - creating a fake error for the swapi library." % msg
      raise swapi.error.SwapiFakeIOError(msg)
    elif fake_error_type == "requests":
      msg = "%s - creating a fake io error for the requests library." % msg
      import requests.exceptions
      # see http://docs.python-requests.org/en/latest/user/quickstart/#errors-and-exceptions
      # and http://docs.python-requests.org/en/latest/api/#exceptions
      raise requests.exceptions.RequestException(msg)
    elif fake_error_type == "requests_timeout":
      msg = "%s - creating a fake io TIMEOUT error for the requests library." % msg
      import requests.exceptions
      raise requests.exceptions.Timeout(msg)
    else:
      msg = "%s - creating a non-io related arithmetic error." % msg
      raise ArithmeticError(msg)

  # 2) Regular code starts here:

  ctx["json1"] = dict(
    url=url,
    auth=auth,
    data=data,
  )

  import requests
  if method == "GET":
    r = requests.get(
      url = url,
      auth = auth,
    )
  elif method == "POST":
    r = requests.post(
      url = url,
      auth = auth,
      data = data,
    )
  elif method == "PUT":
    r = requests.put(
      url = url,
      auth = auth,
      data = data,
    )
  elif method == "DELETE":
    r = requests.delete(
      url = url,
      auth = auth,
    )
  else:
    raise Exception("Wrong method: %s" % method)
  swapi.LOG.debug("%s response: %s" % (method, str(r)))
  try:
    rdict = r.json()
  except:
    rdict = dict()
  ctx["json"] = rdict # in case of exception query this dict!
  if r.status_code == 503:
    # because shopware 4.x delivered a raw 503 error like this:
    """

    Fatal error: Allowed memory size of 134217728 bytes exhausted (tried to allocate 123 bytes) in /var/www/vendor/doctrine/orm/lib/Doctrine/ORM/UnitOfWork.php on 
    line 2700
    503 Service Unavailable  
    """
    chunk_size = 512
    chunks = []
    # Also works without stream = True:
    for chunk in r.iter_content(chunk_size):
      chunks.append(str(chunk))
    ctx['json']['raw_error'] = 'HTTP Error 503: %s' % " ".join(chunks)
    print(ctx['json']['raw_error'])
    #Or write it to a file:
    #with open('/tmp/raw_error', 'wb') as fd:
    #    for chunk in r.iter_content(chunk_size):
    #      fd.write(chunk)    

  def debug_json(key,d):
    val = d.get(key, None)    
    if val is not None:
      swapi.LOG.debug("JSON field '%s' from %s answer was %s" % (
        key, method, val ))
  debug_json("success", rdict)
  debug_json("message", rdict)
  debug_json("data", rdict)
  debug_json("errors", rdict)

  return r

def next_error(fake_error):
  """
  >>> next_error(dict())
  {}

  >>> next_error(dict(fail_times=2))
  {'fail_times': 1}
  
  >>> next_error(dict(fail_times=1))
  {'fail_times': 0}
  
  # Does this make sense? Does it ever happen?

  >>> next_error(dict(fail_times=0))
  {'fail_times': -1}
  """
  # helper function for unittests
  if fake_error.get("fail_times", None) is None:
    # fail_times is not set, do nothing:
    return fake_error
  # count down:
  fake_error["fail_times"] = fake_error["fail_times"] - 1
  return fake_error
