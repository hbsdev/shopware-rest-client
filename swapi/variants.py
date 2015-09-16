# -*- coding: utf-8 -*-

"""
Variante aktualisieren: In dem folgenden Beispiel
wird gezeigt, wie eine bestehende Variante
aktualisiert wird. Wie schon in dem Beispiel
zum Erstellen einer Variante, erwartet die API
den articleId Parameter innerhlalb des Daten Arrays!

  // PUT /api/variants/2
  array(
      'articleId' => 279,
      'inStock' => 40,
      ..
  );
"""


def dodelete_by_number(ctx, number, forgive=False):
  # http://community.shopware.com/_detail_1694.html#DELETE_.28einzeln.29
  if forgive:
    raise_for = False
  else:
    raise_for = True
  import swapi
  return swapi.dodelete(
    ctx,
    "variants", 
    suffix = "/%s?useNumberAsId=true" % number,
    raise_for=raise_for,
  )

"""
http://community.shopware.com/Shopware-4-API-Beispiele-und-Erweiterungen_detail_1070.html#L.F6schen_von_Varianten
Löschen von Varianten

Das Löschen von Varianten ist ab Shopware 4.0.5 möglich. Dazu wurde eine eigene
Variants-Ressource angelegt. Der Funktionsumfang der Ressource beschränkt sich zur
Zeit auf das Auslesen einzelner Varianten via GET und das Löschen von Varianten via DELETE.
Im Folgenden Beispiel wird die Variante mit der articleDetailId 23 gelöscht.
 
$client->call('variants/23', ApiClient::METHODE_DELETE);
Die Variants-Ressource unterstützt dabei ebenfalls den Zugriff via number. Dazu muss der Parameter "useNumberAsId" gesetzt werden.

$params = array(
    'useNumberAsId' => true
);
 
$client->delete('variants/SW1234', $params);  
"""

# def set_main(ctx, number_master, number_detail):
#   # hat keinen erfolg, es kann der vorherige nicht aufgehoben werden
#   v = dict(
#     variants = [
#       dict(
#         number = number_detail,
#         isMain = False,
#       ),
#     ]
#   )
#   import swapi.articles
#   swapi.articles.put_by_number(ctx, number_master, v)


# def put_kind_by_number(ctx, art8, kind=1):
#   """kind kann 1 sein = default artikel oder
#      2 bei den anderen. ausserdem hat der vaterartikel
#      kind = 1 aber dort ist active = 0"""
#   art5 = art8[:5]
#   payload = dict(kind=kind)
#   import swapi.articles
#   id = swapi.articles.get_id(ctx, art5)
#   import swapi
#   return swapi.put(ctx, 'variants', payload, 
#     '/%s?useNumberAsId=true' % art8)

#def set_first_kind1(ctx, art8_list):
#  """set the first to kind=1 and all others to kind=2"""
#  """
#  Funktiert nicht, gleicher Effekt wie hier:
#  http://forum.shopware.com/programmierung-f56/varianten-vorauswahl-setzen-t25603.html#p120518
#  import swapi.variants
#  swapi.variants.set_first_kind1(ctx, a["display"])
#  """
#  for k2 in art8_list[1:]:
#    put_kind_by_number(ctx, k2, kind=2)
#  put_kind_by_number(ctx, art8_list[0], kind=1)


def count_details(ctx, id):
  """Count how many details exist. Raises Not found error if id not found"""
  import swapi.articles
  import requests.exceptions
  r = swapi.articles.get(ctx, id)
  d = r.json()
  try:
    details = d["data"]["details"]
  except KeyError:
    return 0
  return len(details)

def is_variants_article(ctx, id):
  """If details is empty or does not exist, this is a normal article.
    If details holds at least one variant then this is a variant article."""
  cd = count_details(ctx, id)
  return cd > 0


def count_variants(ctx, id):
  """Count how many variants are defined.
    Result ist len of details + 1 because of mainDetails"""
  import swapi.articles
  r = swapi.articles.get(ctx, id)
  d = r.json()
  try:
    details = d["data"]["details"]
  except KeyError:
    return 0
  return len(details) + 1


def numbers(ctx, id, active=True):
  """Return numbers of variants as a sorted list,
    return only active numbers if active == True"""
  import swapi.articles
  r = swapi.articles.get(ctx, id)
  d = r.json()
  # setzt sich zusammen aus array "details" und "mainDetail"
  try:
    details = d["data"]["details"]
  except KeyError:
    details = []
  try:
    details.append(d["data"]["mainDetail"])
  except Keyerror:
    pass
  res = []
  for detail in details:
    if (detail["active"] == 1) or (not active):
      res.append(detail["number"])
  return sorted(res)


"""

Struktur der Varianten im Artikel:

- a) Eine dictionary im Feld "mainDetail"
       hier ist kind = 1

- b) Eine liste von dictionaries im Feld "details":

     'details': [ .., ]
       hier ist kind = 2

- Jedes dictionary hat folgenden Keys:

  
 {
   'active': 1,
   'additionalText': '0,30 x 12mm gelb "Insulin" 100 '
                     'Stück',
   'articleId': 12,
   'attribute': {
     'articleDetailId': 13,
     'articleId': 12,
     'attr1': None,
     ....
     'attr9': None,
     'dreiscCanonicalLink': None,
     'dreiscRobotsTag': None,
     'dreiscSeoBreadcrumb': None,
     'dreiscSeoTitle': None,
     'dreiscSeoTitleReplace': None,
     'dreiscSeoUrl': None,
     'id': 4
   },
   'configuratorOptions': [{
      'groupId': 1,
      'id': 3,
      'name': '0,30 x 12mm '
              'gelb "Insulin" '
              '100 Stück',
      'position': 1
   }],
   'ean': None,
   'height': None,
   'id': 13,
   'images': [],
   'inStock': 10,
   'kind': 2,
   'len': None,
   'maxPurchase': None,
   'minPurchase': None,
   'number': '10025-02',
   'packUnit': None,
   'position': 0,
   'prices': [{
     'articleDetailsId': 13,
     'articleId': 12,
     'basePrice': 0,
     'customerGroup': {'discount': 0,
                       'id': 1,
                       'key': 'EK',
                       'minimumOrder': 10,
                       'minimumOrderSurcharge': 5,
                       'mode': False,
                       'name': 'Test '
                               'Kundengruppe',
                       'tax': True,
                       'taxInput': True},
     'customerGroupKey': 'EK',
     'from': 1,
     'id': 33,
     'percent': 0,
     'price': 3.3949579831933,
     'pseudoPrice': 0,
     'to': 'beliebig'
   }],
   'purchaseSteps': None,
   'purchaseUnit': None,
   'referenceUnit': None,
   'releaseDate': None,
   'shippingFree': False,
   'shippingTime': None,
   'stockMin': None,
   'supplierNumber': None,
   'unitId': None,
   'weight': None,
   'width': None
 },

ENDE


Löschen von Varianten

Das Löschen von Varianten ist ab Shopware 4.0.5 möglich.
Dazu wurde eine eigene Variants-Ressource angelegt.
Der Funktionsumfang der Ressource beschränkt sich
zur Zeit auf das Auslesen einzelner Varianten via
GET und das Löschen von Varianten via DELETE.

Im Folgenden Beispiel wird die Variante mit der 
articleDetailId 23 gelöscht.
 
$client->call('variants/23', ApiClient::METHODE_DELETE);
 
Die Variants-Ressource unterstützt dabei ebenfalls den
Zugriff via number. Dazu muss der Parameter 
"useNumberAsId" gesetzt werden.

$params = array(
    'useNumberAsId' => true
);
 
$client->delete('variants/SW1234', $params);
 
"""
