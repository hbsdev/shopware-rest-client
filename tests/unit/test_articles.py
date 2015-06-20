# -*- coding: utf-8 -*-

def test_articles_create_main_detail():
  detail_data = (
    "12345-01", 199.90, 'Blue', 'S / Blue', "12 123 1012", "124323.3", "XR-3434C", 1, "SEO Title")

  import swapi.articles
  a = swapi.articles.article_main_detail(detail_data)
  assert a["number"] == "12345-01"
  assert a["additionaltext"] == "S / Blue"
  assert a["ean"] == "12 123 1012"
  assert a["attribute"]["attr1"] == "124323.3"
  assert a["attribute"]["attr2"] == "XR-3434C"
  assert a["attribute"]["dreiscSeoTitleReplace"] == 1
  assert a["attribute"]["dreiscSeoTitle"] == "SEO Title"

def test_articles_create_new_demodata():
  import swapi.articles
  import pytest
  a = swapi.articles.article(insert_demodata = True)
  # Demo data:
  assert a['name'] == 'Article None'
  assert a['supplier'] == 'Standard Supplier'
  # Standard data:
  assert a['mainDetail']['prices'][0]['customerGroupKey'] == 'EK'
  assert a['mainDetail']['prices'][0]['price'] is None
  assert a['mainDetail']['number'] is None
  assert a['taxId'] == 1
  assert a['categories'] == []
  assert a['tax'] is None
  assert a['description'] is None
  assert a['descriptionLong'] is None

  a = swapi.articles.article()
  # No demo data:
  assert a['name'] is None
  assert 'supplier' not in a
  # Standard data i still the same:
  assert a['mainDetail']['prices'][0]['customerGroupKey'] == 'EK'
  assert a['mainDetail']['prices'][0]['price'] is None
  assert a['mainDetail']['number'] is None
  assert a['taxId'] == 1
  assert a['categories'] == []
  assert a['tax'] is None
  assert a['description'] is None
  assert a['descriptionLong'] is None


def test_articles_create_update_categories():
  import swapi.articles
  import pytest
  a = swapi.articles.article(update=True)
  assert a == dict()

  # if we do not update, categories need to be set as array:
  a = swapi.articles.article(update=False)
  assert a["categories"] == []

  a = swapi.articles.article(categories = [1 ,2, 3], update=True)
  assert 1 in a["categories"]

  a = swapi.articles.article(categories = [1 ,2, 3], update=False)
  assert 1 in a["categories"]

  a = swapi.articles.article(categories = [], update=True)
  assert a["categories"] == []

  a = swapi.articles.article(categories = [], update=False)
  assert a["categories"] == []


def test_articles_create_update_main_detail():
  import swapi.articles
  a = swapi.articles.article(price = 1.23)
  assert a['mainDetail']['prices'][0]['price'] == 1.23
  assert a['mainDetail']['prices'][0]['customerGroupKey'] == 'EK'
  assert a['mainDetail']['number'] is None

  a = swapi.articles.article(number="A-01")
  #assert a['mainDetail']['prices'][0]['price'] == 1.23
  #assert a['mainDetail']['prices'][0]['customerGroupKey'] == 'EK'
  assert a['mainDetail']['number'] == "A-01"
  assert a['mainDetail']['prices'][0]['price'] is None
  assert a['mainDetail']['prices'][0]['customerGroupKey'] == 'EK'

  # when we update the prices field will not be overwritten:
  a = swapi.articles.article(number="A-01", update=True)
  assert a['mainDetail']['number'] == "A-01"
  assert 'prices' not in a['mainDetail']

  # neither price:
  a = swapi.articles.article(price=1.23, update=True)
  assert a['mainDetail']['prices'][0]['price'] == 1.23
  assert a['mainDetail']['prices'][0]['customerGroupKey'] == 'EK'
  assert 'number' not in a['mainDetail']
