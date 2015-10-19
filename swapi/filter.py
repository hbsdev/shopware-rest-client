# -*- coding: utf-8 -*-

#from pprint import pprint as pp

def _condition(property, expression, value, ind=0):
  if expression == '<=':
    encoded_ex = '%3C%3D'
  elif expression == '>=':
    encoded_ex = '%3E%3D'
  else:
    encoded_ex = expression
  url_part =  'filter[%s][property]=%s&filter[%s][expression]=%s&filter[%s][value]=%s' % (
    ind, property,
    ind, encoded_ex,
    ind, value)
  return url_part

def condition(conditions):
  if (type(conditions[0]).__name__ != 'list') and (type(conditions[0]).__name__ != 'tuple'):
    # not a list of conditions, there is only 1 condition:
    one_condition = conditions
    return _condition(one_condition[0], one_condition[1], one_condition[2])

  # a list or tuple of conditions was given
  parts = []
  ind = 0
  for cond_tuple in conditions:
    parts.append(_condition(cond_tuple[0], cond_tuple[1], cond_tuple[2], ind))
    ind += 1
  return '&'.join(parts)
