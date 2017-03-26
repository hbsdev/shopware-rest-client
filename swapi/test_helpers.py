# -*- coding: utf-8 -*-

def ok():
  return "OK"


def articles_testdata(number):
  return dict(
    name = 'Demoartikel %s' % number,
    active = True,
    supplierId = 1,
    taxId = 1,
    mainDetail = dict(
      number = "%s" % number
    ),
  )

def customers_testdata(number):
  return dict(
    email = 'schmitz-%s@example.com' % number,
    firstname = 'Klaus',
    lastname = 'Schmitz-%s' % number,
    salutation = 'mr',
    billing = dict(
      number = "%s" % number,
      firstname = 'Klaus',
      lastname = 'Schmitz-%s' % number,
      salutation = 'mr',
      street = 'Neue Strasse',
      streetNumber = '1',
      city = 'Neustadt',
      zipcode = '12345',
      country = 2,
    ),
  )
