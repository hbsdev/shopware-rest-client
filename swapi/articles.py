# -*- coding: utf-8 -*-
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

def get_data_by_number(ctx, number):
  r = get_by_number(ctx, number)
  LOG.debug("GET TEXT: %s" % r.text)  
  json = r.json()
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

def put_by_number(ctx, number, payload):
  # Todo: put by number directly instead
  id = id_for(ctx, number)
  return put(ctx, id, payload)

def id_for(ctx, number):
  r = get_by_number(ctx, number)
  data = r.json()
  # data = {'success': True, 'data': {'tax': {'tax': '19.00', 'id': 1, 'name': '19%'}, 'categories': [], ...
  id = data["data"]["id"]
  return id

def exists(ctx, number):
  import requests.exceptions
  try:
    r = get_by_number(ctx, number)
  except requests.exceptions.HTTPError as e:
    assert str(e) == "404 Client Error: Not Found"
    return False
  return True

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

def article(
  number, # "A0012-34"
  price, # 12.34
  name=None,
  supplierId=None, supplier=None, # e.g. supplier="Supplier Inc."
  taxId = None, tax=None, # e.g. tax=19.0
  categories=[], # [12, 22]
  customerGroupKey='EK',
  more_data=dict(),
  ):
  """Create a minimal article"""

  if name is None:
    name = "Article %s" % number

  r = dict(
    name = name,
    active = True,
    tax = tax,
    categories = categories,
    mainDetail = dict(
      number = number,
      prices = [
        dict(
          customerGroupKey = customerGroupKey,
          price = price,
          ),
      ]
      ),
    )
  if supplierId is None:
    if supplier is None:
      r["supplier"] = 'Standard Supplier'
    else:
      r["supplier"] = supplier
  else:
      r["supplierId"] = supplierId

  if taxId is None:
    if tax is None:
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

def article_variants(groupname, variant_data):
  """
  GROUP_NAME = "Colour"
  base="12345"

  # (number, price, option, additionaltext)
  VARIANT_DATA = (
    ("%s-11" % base, 199.90, 'Blau', 'S / Blau',),
    ("%s-12" % base, 299.90, 'Rot', 'M / Rot',),
    ("%s-13" % base, 399.90, 'Gelb', 'L / Gelb',),
    )
  """
  options = []
  variants = []
  isMain = True # only for the first
  for v in variant_data:
    d = dict(
      isMain = isMain,
      number = v[0],
      active = 1,
      inStock = 10,
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
      additionaltext = v[3],
      )
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
