To run pytest on this file only:

  python -m pytest tests/functional/retry.rst

>>> import swapi
>>> import swapi.articles
>>> import swapi.context

Prepare config:

>>> from tests.fixtures.auth import read_conf
>>> conf = read_conf()


Create API context, no retries, fail 1 time: This should fail!

>>> retry = dict(retries=0)
>>> fake_error = dict(fail_times=1)
>>> ctx = swapi.context.create(conf, retry, fake_error)

>>> swapi.articles.get(ctx) # doctest: +IGNORE_EXCEPTION_DETAIL
Traceback (most recent call last):
...
swapi.SwapiFakeIOError


Same for Requests:

>>> fake_error = dict(fail_times=1, type="requests")
>>> ctx = swapi.context.create(conf, retry, fake_error)

>>> swapi.articles.get(ctx) # doctest: +IGNORE_EXCEPTION_DETAIL
Traceback (most recent call last):
...
requests.exceptions.RequestException


Also the specific requests exceptions should work. Timeout:

>>> fake_error = dict(fail_times=1, type="requests_timeout")
>>> ctx = swapi.context.create(conf, retry, fake_error)

>>> swapi.articles.get(ctx) # doctest: +IGNORE_EXCEPTION_DETAIL
Traceback (most recent call last):
...
requests.exceptions.Timeout


Requests Timeout, 2 retries, fail 2 times : This should pass!

>>> retry = dict(retries=2)
>>> fake_error = dict(fail_times=2, type="requests_timeout")
>>> ctx = swapi.context.create(conf, retry, fake_error)

>>> ok, r, info = swapi.articles.get(ctx) # doctest: +IGNORE_EXCEPTION_DETAIL
>>> ok
True


Create API context, 2 retries, fail 2 time : This should pass!

>>> retry = dict(retries=2)
>>> fake_error = dict(fail_times=2)
>>> ctx = swapi.context.create(conf, retry, fake_error)

>>> ok, r, info = swapi.articles.get(ctx) # doctest: +IGNORE_EXCEPTION_DETAIL
>>> ok
True
>>> str(r)
'<Response [200]>'

Create API context, 2 retries, fail 3 time : This should fail!

>>> retry = dict(retries=2)
>>> fake_error = dict(fail_times=3)
>>> ctx = swapi.context.create(conf, retry, fake_error)

>>> ok, r, info = swapi.articles.get(ctx) # doctest: +IGNORE_EXCEPTION_DETAIL
Traceback (most recent call last):
...
swapi.SwapiFakeIOError

Same for requests error type:

>>> fake_error = dict(fail_times=3, type="requests")
>>> ctx = swapi.context.create(conf, retry, fake_error)

>>> ok, r, info = swapi.articles.get(ctx) # doctest: +IGNORE_EXCEPTION_DETAIL
Traceback (most recent call last):
...
requests.exceptions.RequestException

Create API context, 2 retries, fail 1 time with Non-IO error.
This should still fail, because swapi can only heal IO errors:

>>> retry = dict(retries=2)
>>> fake_error = dict(fail_times=1, type="numeric")
>>> ctx = swapi.context.create(conf, retry, fake_error)

>>> ok, r, info = swapi.articles.get(ctx) # doctest: +IGNORE_EXCEPTION_DETAIL
Traceback (most recent call last):
...
ArithmeticError
