
def swap_legacy_data_address(address):
  address['zipCode'] = address.get('zipcode')
  del address['zipcode']
  return address


def add_legacy_data(data):

    import copy
    billing = copy.deepcopy(data['defaultBillingAddress'])
    billing = swap_legacy_data_address(billing)
    data['billing'] = billing

    import copy
    shipping = copy.deepcopy(data['defaultShippingAddress'])
    shipping = swap_legacy_data_address(shipping)
    data['shipping'] = shipping

    '''
    The customer api endpoint now uses the structure of the address model
    instead of the billing or shipping model
    '''

    return data
