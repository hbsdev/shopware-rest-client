# -*- coding: utf-8 -*-
import easylog

easylog.create("SWAPI", "DEBUG")

LOG = easylog.get("SWAPI")

# siehe php signaturen !

def get_raw(ctx, suffix=""):
  import swapi
  LOG.debug("Query: /api/query%s" % suffix)
  return swapi.get(ctx, "query", suffix = suffix)

def get(ctx, q):
  return get_raw(ctx, "/?q=%s" % q)
