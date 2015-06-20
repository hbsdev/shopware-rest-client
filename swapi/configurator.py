# -*- coding: utf-8 -*-

def count_variants(ctx, id):
  """Count how many variants are defined"""
  import swapi.articles
  r = swapi.articles.get(ctx, id)
  d = r.json()
  import pprint
  pprint.pprint(d)
  try:
    c_options = d["data"]["mainDetail"]["configuratorOptions"]
  except KeyError:
    return 0
  return len(c_options)

def downgrade_standard(ctx, id):
  pdata = dict(
    configuratorSet = None,
    variants = None,
  )
