
def swap_legacy_data_address(address,original_field_name):

  address['_debug_info'] = 'This is a legacy dict, use %s instead in the future.' % original_field_name

  # lastName
  address['lastName'] = address.get('lastname')
  del address['lastname']

  # firstName
  address['firstName'] = address.get('firstname')
  del address['firstname']

  # zipcode
  address['zipCode'] = address.get('zipcode')
  del address['zipcode']

  # streetNumber
  address['streetNumber'] = ''

  attribute = address.get('attribute',None)
  if attribute is None:
    address['attribute'] = dict()
    attribute = dict()
  customerAddressId = attribute.get('customerAddressId')
  if original_field_name == 'defaultBillingAddress':
    address['attribute']['customerBillingId'] = customerAddressId
  elif original_field_name == 'defaultShippingAddress':
    address['attribute']['customerShippingId'] = customerAddressId
  else:
    raise Exception('3956253 original_field_name can only be defaultBillingAddress or defaultShippingAddress')

  return address


def add_legacy_data(data):

    import copy
    billing = copy.deepcopy(data['defaultBillingAddress'])
    billing = swap_legacy_data_address(billing,original_field_name='defaultBillingAddress')

    # customer number war vorher in billing number:
    billing['number'] = data['number']

    data['billing'] = billing

    import copy
    shipping = copy.deepcopy(data['defaultShippingAddress'])
    shipping = swap_legacy_data_address(shipping,original_field_name='defaultShippingAddress')
    data['shipping'] = shipping

    '''
    The customer api endpoint now uses the structure of the address model
    instead of the billing or shipping model
    '''

    return data
