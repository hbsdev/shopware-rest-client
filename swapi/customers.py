# -*- coding: utf-8 -*-

from pprint import pprint as pp

import easylog
LOG = easylog.get("SWAPI")

# siehe php signaturen !

def get_raw(ctx, suffix=""):
  import swapi
  return swapi.get(
    ctx,
    "customers",
    suffix=suffix,
    raise_for=True,
  )

def get(ctx, id = None):
  if id is None:
    return get_raw(ctx)
  return get_raw(ctx, "/%s" % id)

def get_by_number(ctx, number):
  # useNumberAsId=true - This tells the API to query the customer's
  # data by its number, instead of its id identifier.
  # the number is a string and stored in billing.number
  # raises requests.exceptions.HTTPError if not found:
  return get_raw(ctx, "/%s?useNumberAsId=true" % number)

def id(r):
  import swapi
  return swapi.id(r)

def id_for_prefix(ctx, number_prefix):
  """returns id of first found who's ordernumber starts with number_prefix"""
  # TODO: use proper url encoding function
  q = "".join([
    "SELECT+a+FROM+%5CShopware%5CModels%5COrder%5CDetail+a+",
    "WHERE+a.number+LIKE+%27",
    "%s" % number_prefix,
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
  orderId = data["data"][0]["orderId"]
  return orderId

# old name, deprecate!
def id_for_startswith(ctx, number_prefix):
  return id_for_prefix(ctx, number_prefix)

def get_by_prefix(ctx, number_prefix):
  orderId = id_for_prefix(ctx, number_prefix)
  if orderId is None:
    return None
  # Artikelnumber = mainDetail.number
  # raises requests.exceptions.HTTPError if not found:
  return get(ctx, orderId)

def id_for(ctx, number):
  r = get_by_number(ctx, number)
  data = r.json()
  # data = {'success': True, 'data': {'tax': {'tax': '19.00', 'id': 1, 'name': '19%'}, 'categories': [], ...
  if not data["success"]:
    return None
  orderId = data["data"]["id"]
  return orderId

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
  orderId = data["data"]["id"]
  return orderId

def exists(ctx, number):
  import requests.exceptions
  try:
    r = get_by_number(ctx, number)
  except requests.exceptions.HTTPError as e:
    s = "404 Client Error: Not Found"
    if str(e)[:len(s)] == s:
      return False
    # re reaise all other exceptions:
    raise
    #assert str(e) == "404 Client Error: Not Found"
    #return False
  data = r.json()
  if not data["success"]:
    return False
  return True

def exists_by_prefix(ctx, number_prefix):
  if id_for_prefix(ctx, number_prefix) is None:
    return False
  return True

def get_data(ctx, id):
  import requests.exceptions
  try:
    r = get(ctx, id)
  except requests.exceptions.HTTPError as e:
    s = "404 Client Error: Not Found"
    if str(e)[:len(s)] == s:
      return None
    # re raise if string does not match:
    raise

  #LOG.debug("GET TEXT: %s" % r.text)
  data = r.json()
  if not data["success"]:
    return None
  data2 = data["data"]

  # sw 4 compat:
  import swapi.sw4_compat as compat4
  if compat4.is_set(ctx['conf']):
    import swapi.sw4_compat.customers as compat4customers
    data2 = compat4customers.add_legacy_data(data2)

  return data2


def get_data_by_number(ctx, number):
  import requests.exceptions
  try:
    r = get_by_number(ctx, number)
  except requests.exceptions.HTTPError as e:
    s = "404 Client Error: Not Found"
    if str(e)[:len(s)] == s:
      return None
    s = "400 Client Error: Bad Request"
    ls = len(s)
    if str(e)[:len(s)] == s:
      return None
    raise Exception("Failed get_data_by_number(%s: %s" % (number,str(e)))
  #LOG.debug("GET TEXT: %s" % r.text)
  data = r.json()
  if not data["success"]:
    return None
  data2 = data["data"]

  # sw 4 compat:
  import swapi.sw4_compat as compat4
  if compat4.is_set(ctx['conf']):
    import swapi.sw4_compat.customers as compat4customers
    data2 = compat4customers.add_legacy_data(data2)
  return data2


def get_filtered(ctx, filter):
  import swapi.filter
  url_parameters = swapi.filter.condition(filter)

  import requests.exceptions
  try:
    # r = get_by_number(ctx, number)
    r = get_raw(ctx, "/?%s" % url_parameters)
  except requests.exceptions.HTTPError as e:
    if str(e) == "404 Client Error: Not Found":
      return None
    if str(e) == "400 Client Error: Bad Request":
      return None
    raise Exception("Failed get_data_by_number(%s: %s" % (number,str(e)))
  #LOG.debug("GET TEXT: %s" % r.text)
  data = r.json()
  if not data["success"]:
    return None
  return data["data"]

def get_by_ordertime(ctx, isodatefrom, isodateto=None):
  filter = ('orderTime', '>=', isodatefrom)
  if isodateto is not None:
    filter_to = ('orderTime', '<=', isodateto)
    filter = (filter, filter_to)
  # raises requests.exceptions.HTTPError if not found:
  return get_filtered(ctx, filter)

def post(ctx, payload, suffix=""):
  import swapi
  return swapi.post(
    ctx,
    "customers",
    payload,
    suffix=suffix,
    raise_for=True,
  )

def put(ctx, id, payload):
  """
  php: $client->put('customers/193', array(
         'name' => 'New order Name'
       ));
  """

  import swapi
  return swapi.put(
    ctx,
    "customers",
    payload,
    suffix = "/%s" % id,
    raise_for=True,
  )

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

def dodelete(ctx, id, forgive=False):
  # Artikelnummer = mainDetail.number
  # php: $client->delete('customers/193');
  if forgive:
    raise_for = False
  else:
    raise_for = True
  import swapi
  return swapi.dodelete(
    ctx,
    "customers",
    suffix = "/%s" % id,
    raise_for=raise_for,
  )

def dodelete_by_number(ctx, number, forgive=False):
  # Artikelnummer = mainDetail.number
  ## Deleting customers by number using the API isn't possible as of 2015-MAY
  # return dodelete(ctx,"/%s?useNumberAsId=true" % number)
  if not forgive:
    id = id_for(ctx, number)
    return dodelete(ctx, id, forgive=forgive)
  # Do forgive if not exists:
  try:
    id = id_for(ctx, number)
  except:
    return None
  return dodelete(ctx, id, forgive=forgive)

def set_active(ctx, id, is_active):
  # Artikelnummer = mainDetail.number
  # php: $client->delete('customers/193');
  return put(
    ctx,
    id,
    payload = dict(
      active = is_active,
    )
  )

def set_active_by_number(ctx, number, is_active):
  # Artikelnummer = mainDetail.number
  ## Deleting customers by number using the API isn't possible as of 2015-MAY
  # return dodelete(ctx,"/%s?useNumberAsId=true" % number)
  id = id_for(ctx, number)
  return set_active(ctx, id, is_active)

def is_active(ctx, id):
  a = get(ctx, id)
  d = a.json()
  try:
    data = d["data"] # can raise keyerror
  except KeyError:
    return None
  # other exceptions will raise here
  return data["active"]

def is_active_by_number(ctx, number):
  id = id_for(ctx, number)
  return is_active(ctx, id)

def mainDetail_number(data):
  try:
    return data["mainDetail"]["number"]
  except KeyError:
    return None
  except TypeError:
    # 'NoneType' object is not subscriptable
    return None
  # other exceptions will raise here

def get_mainDetail_number(ctx, id):
  a = get(ctx, id)
  d = a.json()
  try:
    data = d["data"] # can raise keyerror
  except KeyError:
    return None
  # other exceptions will raise here
  variant = mainDetail_number(data) # can also raise keyerror
  return variant

def first_detail_number(data):
  try:
    return data["details"][0]["number"]
  except KeyError:
    return None
  # other exceptions will raise here

def get_first_detail_number(ctx,id):
  a = get(ctx, id)
  d = a.json()
  try:
    data = d["data"] # can raise keyerror
  except KeyError:
    return None
  # other exceptions will raise here
  number = first_detail_number(data)
  return number

def pprint(ctx, id):
  """"""
  r = get(ctx, id)
  d = r.json()
  import pprint
  pprint.pprint(d)


def order_main_detail(detail_data, inStock=50000, as_active=True, with_configuratorOptions=True):
  """
  # (number, price, option, additionalText, ...)
  DETAIL_DATA = (
    "12345-11", 199.90, 'blue', 'S / blue', ean, pzn, supplier_order_number, tax)
  """
  if len(detail_data) < 9:
    import swapi.error
    raise swapi.error.SwapiParameterError("Need at least order number and price (%s)" % detail_data)

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

  res = dict(
    number = detail_data[0],
    active = active,
    inStock = inStock,
    __options_prices = dict(replace=True),
    prices = [
      dict(
        customerGroupKey = 'EK',
        price = detail_data[1],
        pseudoPrice = detail_data[12],
      ),
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
  if with_configuratorOptions:
    res["configuratorOptions"] = []
  return res


def _is_active(c):
  d = c.json()
  try:
    data = d["data"] # can raise keyerror
  except KeyError:
    return None
  # other exceptions will raise here
  return data["active"]

def is_active(ctx, id):
  c = get(ctx, id)
  return _is_active(c)

def is_active_by_number(ctx, number):
  c = get_by_number(ctx, id)
  return _is_active(c)

def set_active(ctx, id, is_active):
  return put(
    ctx,
    id,
    payload = dict(
      active = is_active,
    )
  )

def set_active_by_number(ctx, number, is_active):
  id = id_for(ctx, number)
  return set_active(ctx, id, is_active)

def is_active(ctx, id):
  a = get(ctx, id)
  d = a.json()
  try:
    data = d["data"] # can raise keyerror
  except KeyError:
    return None
  # other exceptions will raise here
  return data["active"]

def is_active_by_number(ctx, number):
  id = id_for(ctx, number)
  return is_active(ctx, id)

