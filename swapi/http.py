import requests.auth
import swapi
import swapi.error


def construct_auth(conf):
  proto, server, basepath, user, key = conf
  import requests.auth
  auth = requests.auth.HTTPDigestAuth(user, key)
  return auth


def construct_url(conf, coll):
  """
  >>> conf = ("http","example.com", "/subshop/", "api", "key123key")
  >>> construct_url(conf,"articles")
  'http://example.com/subshop/api/articles'

  >>> conf = ("https","example.com", "/", "api", "key123key")
  >>> construct_url(conf,"orders")
  'https://example.com/api/orders'

  """
  proto, server, basepath, user, key = conf
  url = '%s://%s%sapi/%s' % (proto, server, basepath, coll)
  import swapi
  swapi.LOG.debug("Url constructed: %s", url)
  return url


def rest_call(method, url, auth, data=None, fake_error={}):
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
  import requests
  if method == "GET":
    r = requests.get(
      url = url,
      auth = auth,
    )
  elif method == "POST":
    r = requests.delete(
      url = url,
      auth = auth,
    )
  elif method == "PUT":
    r = requests.delete(
      url = url,
      auth = auth,
    )
  elif method == "DELETE":
    r = requests.delete(
      url = url,
      auth = auth,
    )
  else:
    raise Exception("Wrong method: %s" % method)
  return r

def next_error(fake_error):
  # helper function for unittests
  if fake_error.get("fail_times", None) is None:
    # fail_times is not set, do nothing:
    return fake_error
  # count down:
  fake_error["fail_times"] = fake_error["fail_times"] - 1
  return fake_error
