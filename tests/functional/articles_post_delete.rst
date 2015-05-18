Generate our article json object:

>>> import swapi.context

>>> number = "A0001"
>>> import swapi.test_helpers
>>> ART = swapi.test_helpers.articles_testdata(number)

Create API context:

>>> from tests.fixtures.auth import read_conf
>>> conf = read_conf()
>>> ctx = swapi.context.create(conf)

Make sure article does not yet exist:

>>> import swapi.articles
>>> forgive = True
>>> ok, r, info = swapi.articles.dodelete_by_number(ctx, number, forgive)
>>> ok
True

>>> swapi.articles.exists(ctx, number)
False

Try to delete an article that's not there:
>>> forgive = False
>>> ok, r, info = swapi.articles.dodelete_by_number(ctx, number, forgive)
>>> ok
False

Create article:

>>> ok, r, info = swapi.post(ctx, "articles", ART)
>>> ok
True

>>> str(r)
'<Response [201]>'

Make sure it exists:

>>> swapi.articles.exists(ctx, number)
True

Delete it:

>>> ok, r, info = swapi.articles.dodelete_by_number(ctx, number)
>>> ok
True

>>> swapi.articles.exists(ctx, number)
False
