from tests.fixtures.auth import read_conf

def test_1_no_retry_swapi(read_conf):

  # Create API context, no retries, fail 1 time: This should fail!

  import swapi.context
  ctx = swapi.context.create(
    read_conf,
    dict(retries=0),
    dict(fail_times=1),
    )

  import pytest
  import swapi.error
  with pytest.raises(swapi.error.SwapiFakeIOError) as einfo:
    import swapi.articles
    swapi.articles.get(ctx)
  assert "0 fake errors left" in str(einfo.value)
  assert "error for the swapi library" in str(einfo.value)

def test_2_no_retry_requests(read_conf):
  # Same for Requests:

  import swapi.context
  ctx = swapi.context.create(
    read_conf, 
    dict(retries=0),
    dict(fail_times=1, type="requests"),
    )

  import pytest
  import requests.exceptions
  with pytest.raises(requests.exceptions.RequestException) as einfo:
    import swapi.articles
    swapi.articles.get(ctx)
  assert "0 fake errors left" in str(einfo.value)
  assert "io error for the requests library" in str(einfo.value)

def test_3_no_retry_timeout_error(read_conf):
  # Also the specific requests exceptions should work. Timeout:

  import swapi.context
  ctx = swapi.context.create(
    read_conf,
    dict(retries=0),
    dict(fail_times=1, type="requests_timeout"),
    )

  import pytest
  import requests.exceptions
  with pytest.raises(requests.exceptions.Timeout) as einfo:
    import swapi.articles
    swapi.articles.get(ctx)
  assert "0 fake errors left" in str(einfo.value)
  assert "io TIMEOUT error for the requests library" in str(einfo.value)

  
def test_4_retry_timeout_pass(read_conf):
  # Requests Timeout, 2 retries, fail 2 times
  # This should pass.

  import swapi.context
  ctx = swapi.context.create(
    read_conf,
    dict(retries=2),
    dict(fail_times=2, type="requests_timeout"),
    )

  import pytest
  import requests.exceptions

  import swapi.articles
  r = swapi.articles.get(ctx)
  assert str(r) == '<Response [200]>'


def test_5_retry_pass(read_conf):
  # Create API context, 2 retries, fail 2 times
  # This should pass.

  import swapi.context
  ctx = swapi.context.create(
    read_conf,
    dict(retries=2),
    dict(fail_times=2),
    )

  import pytest
  import requests.exceptions

  import swapi.articles
  r = swapi.articles.get(ctx)
  assert str(r) == '<Response [200]>'


def test_6_retry_fail(read_conf):
  # Create API context, 2 retries, fail 3 times
  # This should fail!

  import swapi.context
  ctx = swapi.context.create(
    read_conf,
    dict(retries=2),
    dict(fail_times=3),
    )

  import pytest
  import swapi.error
  with pytest.raises(swapi.error.SwapiFakeIOError) as einfo:
    import swapi.articles
    swapi.articles.get(ctx)
  assert "0 fake errors left" in str(einfo.value)
  assert "error for the swapi library" in str(einfo.value)

def test_7_requests_retry_fail(read_conf):
  # Create API context, 2 retries, fail 3 times
  # This should fail!

  import swapi.context
  ctx = swapi.context.create(
    read_conf,
    dict(retries=2),
    dict(fail_times=3, type="requests"),
    )

  import pytest
  import requests.exceptions
  with pytest.raises(requests.exceptions.RequestException) as einfo:
    import swapi.articles
    swapi.articles.get(ctx)
  assert "0 fake errors left" in str(einfo.value)
  assert "fake io error for the requests library" in str(einfo.value)

def test_8_requests_non_io_error_always_fail(read_conf):
  # Create API context, 2 retries,
  # fail 1 time with Non-IO error.
  # This should still fail, because
  # swapi is supposed to only heal IO errors!

  import swapi.context
  ctx = swapi.context.create(
    read_conf,
    dict(retries=2),
    dict(fail_times=1, type="numeric"),
    )

  import pytest
  with pytest.raises(ArithmeticError) as einfo:
    import swapi.articles
    swapi.articles.get(ctx)
  assert "0 fake errors left" in str(einfo.value)
  assert "a non-io related arithmetic error" in str(einfo.value)
