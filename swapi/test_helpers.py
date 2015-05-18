# -*- coding: utf-8 -*-

def ok():
  return "OK"


def articles_testdata(number):
  a = dict(
    name = 'Demoartikel %s' % number,
    supplierId = 1,
    taxId = 1,
    mainDetail = dict(
      number = "%s" % number
    ),
  )
  return a
