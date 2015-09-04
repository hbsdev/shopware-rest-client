# -*- coding: utf-8 -*-

#from pprint import pprint as pp

import easylog
LOG = easylog.get("SWAPI")

def dodelete_by_number_doctrine(ctx, number):
  # Second paramter 'number' is 'ordernumber'
  # Sometimes the shopware API leaves entries in s_articles_details 
  # thatshould not be there and they are not removed, when the article is removed
  # This method does remove them.
  dql_query = "DELETE+FROM+%5CShopware%5CModels%5CArticle%5CDetail+d+WHERE+d.number+=+%27" + "%s" % number + "%27"
  import swapi.d_query
  return swapi.d_query.get(ctx, dql_query)
