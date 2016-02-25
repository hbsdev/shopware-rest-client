# -*- coding: utf-8 -*-

def test_articles_create_main_detail():

  art_number = "12345-01"
  vk_brutto = 19.90
  vtext1 = 'Blue'
  vtext2 = 'S / Blue'
  ean = "12 123 1012"
  pzn = "124323.3"
  herstnr = "XR-3434C"
  dreiscSeoTitleReplace = 1
  dreiscSeoTitle = "SEO Title"
  grundpreis_info_purchaseUnit = None
  grundpreis_info_referenceUnit = None # 10
  grundpreis_info_unitId = None
  pseudo_price_brutto = None


  detail_data = (
    art_number, # 0
    vk_brutto,
    vtext1,
    vtext2,
    ean,
    pzn, # 5
    herstnr,
    dreiscSeoTitleReplace,
    dreiscSeoTitle,
    grundpreis_info_purchaseUnit,
    grundpreis_info_referenceUnit, # 10
    grundpreis_info_unitId,
    pseudo_price_brutto,
  )

  import swapi.articles
  a = swapi.articles.article_main_detail(detail_data)
  assert a["number"] == "12345-01"
  assert a["additionalText"] == "S / Blue"
  assert a["ean"] == "12 123 1012"
  assert a["attribute"]["attr1"] == "124323.3"
  assert a["attribute"]["attr2"] == "XR-3434C"
  assert a["attribute"]["dreiscSeoTitleReplace"] == 1
  assert a["attribute"]["dreiscSeoTitle"] == "SEO Title"

def test_articles_create_new_demodata():
  import swapi.articles
  import pytest
  a = swapi.articles.article(
    number="12345-01",
    insert_demodata=True,
  )
  # Demo data:
  assert a['name'] == 'Article 12345-01'
  assert a['supplier'] == 'Standard Supplier'
  # Standard data:
  assert a['mainDetail']['prices'][0]['customerGroupKey'] == 'EK'
  assert a['mainDetail']['prices'][0]['price'] is None
  assert a['mainDetail']['number'] is "12345-01"
  assert a['taxId'] == 1
  assert a['categories'] == []
  assert a['tax'] is None
  assert a['description'] is None
  assert a['descriptionLong'] is None

  a = swapi.articles.article(
    number="12345-01",
  )
  # No demo data:
  assert a['name'] is None
  assert 'supplier' not in a
  # Standard data is still the same:
  assert a['mainDetail']['prices'][0]['customerGroupKey'] == 'EK'
  assert a['mainDetail']['prices'][0]['price'] is None
  assert a['mainDetail']['number'] == "12345-01"
  assert a['taxId'] == 1
  assert a['categories'] == []
  assert a['tax'] is None
  assert a['description'] is None
  assert a['descriptionLong'] is None


def test_articles_create_update_categories():
  import swapi.articles
  import pytest
  a = swapi.articles.article(
    update=True,
  )
  assert a == dict()

  # if we do not update, categories need to be set as array:
  a = swapi.articles.article(
    number="12345-01",
    update=False,
  )
  assert a["categories"] == []

  a = swapi.articles.article(
    categories = [1 ,2, 3],
    update=True,
  )
  assert 1 in a["categories"]

  a = swapi.articles.article(
    number="12345-01",
    categories = [1 ,2, 3], 
    update=False,
  )
  assert 1 in a["categories"]

  a = swapi.articles.article(
    categories = [],
    update=True,
  )
  assert a["categories"] == []

  a = swapi.articles.article(
    number="12345-01",
    categories = [],
    update=False,
  )
  assert a["categories"] == []


def test_articles_create_update_main_detail():
  import swapi.articles
  a = swapi.articles.article(
    number="12345-01",
    price = 1.23,
  )
  assert a['mainDetail']['prices'][0]['price'] == 1.23
  assert a['mainDetail']['prices'][0]['customerGroupKey'] == 'EK'
  assert a['mainDetail']['number'] == "12345-01"

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

def test_add_price():
  a = { 'mainDetail': { 'prices': [{'customerGroupKey': 'EK',
                                   'price': 1.23,
                                   'pseudoPrice': 2.23}], }}
  assert a['mainDetail']['prices'][0]['price'] == 1.23
  assert a['mainDetail']['prices'][0]['customerGroupKey'] == 'EK'
  import swapi.articles
  a = swapi.articles.add_price(a, "G2", 4.56)
  assert a['mainDetail']['prices'][1]['price'] == 4.56
  assert a['mainDetail']['prices'][1]['customerGroupKey'] == 'G2'
  
def test_variant_data_extract():
  v = [
    None, # 0
    1.00, # 1 price
    None, 
    None, 
    None, 
    None, 
    None, 
    None, 
    None, 
    None, 
    None, 
    None, 
    None, # 12
  ]
  isMain = False
  inStock = False
  groupname = "group1"
  import swapi.articles
  d = swapi.articles.variant_data_extract(v, isMain, inStock, groupname, ignore_active=False)
  assert len(d["prices"]) == 1
  more_prices_percentual = [dict(
    customerGroupKey = "K1",
    addPerCent = 11,
  ),]
  d = swapi.articles.variant_data_extract(v, isMain, inStock, groupname, ignore_active=False, more_prices_percentual=more_prices_percentual)
  assert len(d["prices"]) == 2
  assert d["prices"][0]["price"] == 1.00
  assert d["prices"][0]["customerGroupKey"] == "EK"
  assert d["prices"][1]["price"] == 1.11
  assert d["prices"][1]["customerGroupKey"] == "K1"
  """
  d = {
    '__options_prices': {'replace': True},
    'attribute': {
      'dreiscSeoTitle': None,
      'dreiscSeoTitleReplace': None,
      'attr1': None,
      'attr2': None},
    'additionalText': None,
    'referenceUnit': None,
    'prices': [
      {
        'price': None,
        'pseudoPrice': None,
        'customerGroupKey': 'EK'
      }
    ],
    'purchaseUnit': None,
    'isMain': False,
    'configuratorOptions': 
      [{'option': None,
      'group': 'group1'}],
    'ean': None,
    'unitId': None,
    'inStock': False,
    'number': None,
    'active': 1}  
  """
  print(d)
