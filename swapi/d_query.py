# -*- coding: utf-8 -*-
import easylog

easylog.create("SWAPI", "DEBUG")

LOG = easylog.get("SWAPI")

# siehe php signaturen !

def get_raw(ctx, suffix="", raise_for=False):
  import swapi
  LOG.debug("Query: /api/query%s" % suffix)
  return swapi.get(ctx, "query", suffix = suffix, raise_for=raise_for)

def get(ctx, q, raise_for=False):
  return get_raw(ctx, "/?q=%s" % q, raise_for=raise_for)
