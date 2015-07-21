# -*- coding: utf-8 -*-

from pprint import pprint as pp

import easylog
LOG = easylog.get("SWAPI")

# siehe php signaturen !

def get_raw(ctx, suffix=""):
  import swapi
  return swapi.get(ctx, "articles", suffix = suffix)

def get(ctx, id = None):
  if id is None:
    return get_raw(ctx)
  return get_raw(ctx, "/%s" % id)

def get_by_number(ctx, number):
  # Artikelnumber = mainDetail.number
  # raises requests.exceptions.HTTPError if not found:
  return get_raw(ctx, "/%s?useNumberAsId=true" % number)

def id_for_startswith(ctx, number_prefix):
  """returns articleId of first found article who's ordernumber starts with number_prefix"""
  # TODO: use proper url encoding function
  q = "".join([
    "SELECT+a+FROM+%5CShopware%5CModels%5CArticle%5CDetail+a+",
    "WHERE+a.number+LIKE+%27",
    number_prefix,
    "%25", # %
    "%27", # '
  ])
  import swapi.d_query
  r = swapi.d_query.get(ctx, q)
  data = r.json()
  if not data["success"]:
    return None
  if len(data["data"]) == 0:
    return None
  articleId = data["data"][0]["articleId"]
  return articleId


def id_for(ctx, number):
  r = get_by_number(ctx, number)
  data = r.json()
  # data = {'success': True, 'data': {'tax': {'tax': '19.00', 'id': 1, 'name': '19%'}, 'categories': [], ...
  if not data["success"]:
    return None
  articleId = data["data"]["id"]
  return articleId

def get_id(ctx, number):
  import requests.exceptions
  try:
    r = get_by_number(ctx, number)
  except requests.exceptions.HTTPError as e:
    assert str(e) == "404 Client Error: Not Found"
    return None
  data = r.json()
  if not data["success"]:
    return None
  articleId = data["data"]["id"]
  return articleId

def exists(ctx, number):
  import requests.exceptions
  try:
    r = get_by_number(ctx, number)
  except requests.exceptions.HTTPError as e:
    assert str(e) == "404 Client Error: Not Found"
    return False
  data = r.json()
  if not data["success"]:
    return False
  return True

def get_data(ctx, id):
  import requests.exceptions
  try:
    r = get(ctx, id)
  except requests.exceptions.HTTPError as e:
    assert str(e) == "404 Client Error: Not Found"
    return None
  #LOG.debug("GET TEXT: %s" % r.text)  
  json = r.json()
  data = r.json()
  if not data["success"]:
    return None
  return json["data"]

def get_data_by_number(ctx, number):
  import requests.exceptions
  try:
    r = get_by_number(ctx, number)
  except requests.exceptions.HTTPError as e:
    if str(e) != "404 Client Error: Not Found":
      r.raise_for_status()
    return None
  #LOG.debug("GET TEXT: %s" % r.text)  
  json = r.json()
  data = r.json()
  if not data["success"]:
    return None
  return json["data"]

def post(ctx, payload, suffix=""):
  import swapi
  return swapi.post(ctx, "articles", payload, suffix = suffix)

def put(ctx, id, payload):
  """
  php: $client->put('articles/193', array(
         'name' => 'New Article Name'
       ));
  """

  import swapi
  return swapi.put(ctx, "articles", payload, suffix = "/%s" % id)

def ensure_by_number(ctx, payload):
  number = payload["mainDetail"]["number"]
  import requests.exceptions
  try:
    r = get_by_number(ctx, number)
    found = True
    #print("FOUND!")
  except requests.exceptions.HTTPError as e:
    assert str(e) == "404 Client Error: Not Found"
    # Does not yet exist:
    found = False
    #print("NOT FOUND %s" % number)

  if not found:

    return post(ctx, payload)

  # Already exists, overwrite:
  data = r.json()
  id = data["data"]["id"]
  #print (payload)
  return put(ctx, id, payload)

def put_by_number(ctx, number, payload):
  # Todo: put by number directly instead
  id = id_for(ctx, number)
  return put(ctx, id, payload)

def dodelete(ctx, id):
  # Artikelnummer = mainDetail.number
  # php: $client->delete('articles/193');
  import swapi
  return swapi.dodelete(ctx, "articles", suffix = "/%s" % id)

def dodelete_by_number(ctx, number, forgive=False):
  # Artikelnummer = mainDetail.number
  ## Deleting articles by number using the API isn't possible as of 2015-MAY
  # return dodelete(ctx,"/%s?useNumberAsId=true" % number)
  if not forgive:
    id = id_for(ctx, number)
    return dodelete(ctx, id)
  # Do forgive if not exists:
  try:  
    id = id_for(ctx, number)
  except:
    return None
  return dodelete(ctx, id)

def mainDetail_number(data):
  try:
    variant = data["mainDetail"]["number"]
  except KeyError:
    variant = None
  except TypeError:
    # 'NoneType' object is not subscriptable
    variant = None
  return variant

def get_mainDetail_number(ctx, id):
  a = get(ctx, id)
  d = a.json()
  try:
    data = d["data"] # can raise keyerror
    variant = mainDetail_number(data) # can also raise keyerror
  except KeyError:
    variant = None
  return variant

def pprint(ctx, id):
  """"""
  r = get(ctx, id)
  d = r.json()
  import pprint
  pprint.pprint(d)

def article(
  number = None, # mainDetail, ex: "A0012-34" 
  active = None, # mainDetail
  price = None, # 12.34 (incl. tax?!)
  pseudoPrice = None,
  name = None,
  metaTitle = None,
  keywords = None,
  description = None,
  descriptionLong = None,
  inStock = None,
  purchaseUnit = None, # mainDetail, unit price / Grundpreis
  referenceUnit = None, # mainDetail, unit price / Grundpreis
  unitId= None, # mainDetail, unit price / Grundpreis
  supplierId = None, supplier = None, # e.g. supplier = "Supplier Inc."
  taxId  =  None, tax = None, # e.g. tax = 19.0
  categories = None, # [12, 22]
  customerGroupKey = 'EK',
  more_data = dict(),
  update = False, # Update existing article, True only updates existing
  insert_demodata = False, 
  ):
  """Create a minimal article. if update = True, only
  the supplied values will be overwritten. Otherwise all "None"
  values will be overwritten with Null Values"""

  
  new_article = not update
  if new_article:
    if categories is None:
      categories = []

  if new_article:
    if name is None:
      if insert_demodata:
        name = "Article %s" % number


  def should_write(is_new, val):
    """checks if attribute needs to be written or not.
      For new object always write. For existing objects 
      only overwrite, if a value is given. None means 'no value'"""
    if is_new:
      # new object, write data no matter what:
      return True
    # existing object:
    if val is None:
      # do not overwrite existing data if no new value given:
      return False
    # overwrite existing data with new value given:
    return True

  def update_if(d, is_new, key, val):
    if should_write(is_new, val):
      d[key] = val

  r = dict()

  update_if(r, new_article, "active", active)
  update_if(r, new_article, "name", name)
  update_if(r, new_article, "metaTitle", metaTitle)
  update_if(r, new_article, "keywords", keywords)
  update_if(r, new_article, "description", description)
  update_if(r, new_article, "descriptionLong", descriptionLong)
  update_if(r, new_article, "tax", tax)
  update_if(r, new_article, "categories", categories)
  update_if(r, new_article, "name", name)

  mainDetail = dict()

  # mainDetail = dict(
  #   number = number,
  #   prices = [
  #     dict(
  #       customerGroupKey = customerGroupKey,
  #       price = price,
  #       ),
  #   ]
  #   ),
  # )

  # mainDetail needs a number
  update_if(mainDetail, new_article, "number", number)
  update_if(mainDetail, new_article, "inStock", inStock)
  update_if(mainDetail, new_article, "purchaseUnit", purchaseUnit)
  update_if(mainDetail, new_article, "referenceUnit", referenceUnit)
  update_if(mainDetail, new_article, "unitId", unitId)

  if number is None:
    if mainDetail != dict():
      msg = "Cannot add mainDetails (%s) when 'number' is not set. Article data: %s" % (
        mainDetail, r)
      import swapi.error
      raise swapi.error.SwapiDataStructurError(msg)

  if should_write(new_article, price):

    # http://team.mercadia.info/issue/MP-2432
    # __options_prices' => array('replace' => true),
    #    'prices' => array( ..
    mainDetail["__options_prices"] = dict(replace=True)
    mainDetail["prices"] = [
      dict(
         customerGroupKey = customerGroupKey,
         price = price,
         pseudoPrice = pseudoPrice,
      ),
    ]
  
  if mainDetail: # Empty dictionaries evaluate to False!
    r["mainDetail"] = mainDetail

  if supplierId is None:
    if supplier is None:
      if new_article:
        if insert_demodata:
          r["supplier"] = 'Standard Supplier'
    else:
      r["supplier"] = supplier
  else:
    r["supplierId"] = supplierId

  if taxId is None:
    if tax is None:
      if new_article:
        r["taxId"] = 1
    else:
      r["tax"] = tax
  else:
      r["taxId"] = taxId
  r.update(more_data)
  return r

"""
dict(
    name = 'Article Name',
    active = True,
    mainDetail = dict(
      configuratorOptions = [
          
      ],
      active = 1,
      additionalText = 'Additional Text',
      kind = 1,
      number = number,
      inStock = 6,
      prices = [
        dict(
          price = 4.20,
          customerGroupKey = 'EK',
        ),
      ],
      shippingFree = False,
      referenceUnit = None,
      purchaseUnit = None,
      shippingTime = '',
      purchaseSteps = None,
      packUnit = '',
  },
  configuratorSetId = 8,
  )
"""

#def article_no_variants():
#  # Put this to an existing variants article and he should become
#  # a standard article again: (not tested)
#  return dict(
#    configuratorSet = None,
#    variants = None,
#    )


def article_main_detail(detail_data, inStock=50000, as_active=True):
  """
  # (number, price, option, additionalText, ...)
  DETAIL_DATA = (
    "12345-11", 199.90, 'blue', 'S / blue', ean, pzn, supplier_order_number, tax)
  """
  if len(detail_data) < 9:
    import swapi.error
    raise swapi.error.SwapiParameterError("Need at least article number and price (%s)" % detail_data)
  
  # Fill missing values with empty String
  while len(detail_data) < 9:
    detail_data.append("")

  if as_active:
    active = 1
  else:
    active = 0

  # Grundpreise / unit price:
  purchaseUnit = detail_data[9]
  referenceUnit = detail_data[10]
  unitId = detail_data[11]
  if (purchaseUnit is None) or (referenceUnit is None) or (unitId is None):
    # alle oder keins:
    purchaseUnit = None
    referenceUnit = None
    unitId = None

  return dict(
    number = detail_data[0],
    active = active,
    inStock = inStock,
    __options_prices = dict(replace=True),
    prices = [
      dict(
        customerGroupKey = 'EK',
        price = detail_data[1],
      ),
    ],
    configuratorOptions = [
    ],
    additionalText = detail_data[3],
    ean = detail_data[4],
    attribute = dict(
      attr1 = detail_data[5], #PZN
      attr2 = detail_data[6], #Herstellernummer
      dreiscSeoTitleReplace = detail_data[7],
      dreiscSeoTitle = detail_data[8],
    ),
    purchaseUnit = purchaseUnit,
    referenceUnit = referenceUnit,
    unitId = unitId,
  )

def article_variants(groupname, variant_data_list, inStock=50000, ignore_active = False):
  """
  Wenn der Hauptartikel deaktiviert wird, schreiben wir bei den Varianten KEIN
  active Feld! ignore_active = True

  GROUP_NAME = "Colour"
  base="12345"

  # (number, price, option, additionalText)
  VARIANT_DATA_LIST = (
    ("%s-11" % base, 199.90, 'Blau', 'S / Blau', ean, pzn, herstnr),
    ("%s-12" % base, 299.90, 'Rot', 'M / Rot', ean, pzn, herstnr),
    ("%s-13" % base, 399.90, 'Gelb', 'L / Gelb', ean, pzn, herstnr),
    )
  """
  options = []
  variants = []
  isMain = True # only for the first
  for v in variant_data_list:

    # Grundpreis / unit price:
    purchaseUnit = v[9]
    referenceUnit = v[10]
    unitId = v[11]
    if (purchaseUnit is None) or (referenceUnit is None) or (unitId is None):
      # alle oder keins:
      purchaseUnit = None
      referenceUnit = None
      unitId = None
  
    d = dict(
      isMain = isMain,
      number = v[0],
      inStock = inStock,
      __options_prices = dict(replace=True),
      prices = [
        dict(
          customerGroupKey = 'EK',
          price = v[1],
        ),
      ],
      configuratorOptions = [
        dict(
          group = groupname,
          option = v[2],
        ),
      ],
      additionalText = v[3],
      ean = v[4],
      attribute = dict(
        attr1 = v[5], #PZN
        attr2 = v[6], #Herstellernummer
        dreiscSeoTitleReplace = v[7],
        dreiscSeoTitle = v[8],
      ),
      purchaseUnit = purchaseUnit,
      referenceUnit = referenceUnit,
      unitId = unitId,
    )
    if not ignore_active:
      d["active"] = 1

    options.append(dict(name = v[2]))
    variants.append(d)
    # was only True for the first:
    isMain = False

  configuratorSet = dict(
    groups = [
      dict(
        name = groupname,
        options = options,
      ),
      ],
    )

  return dict(
    configuratorSet = configuratorSet,
    variants = variants,
    taxId = 1,
    )
