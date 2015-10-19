# -*- coding: utf-8 -*-

class TestFilter():
  def test_filter_condition_single(self):
    import swapi.filter
    ot1 = swapi.filter.condition(('orderTime', '>=', '2016-12-31'))
    assert(ot1 == 'filter[0][property]=orderTime&filter[0][expression]=%3E%3D&filter[0][value]=2016-12-31')

    ot2 = swapi.filter.condition(('orderTime', '<=', '2015-12-31'))
    assert(ot2 == 'filter[0][property]=orderTime&filter[0][expression]=%3C%3D&filter[0][value]=2015-12-31')

    # list doesn't matter:
    ot3 = swapi.filter.condition(['orderTime', '<=', '2015-12-31'])
    assert(ot2 == ot3)

  def test_filter_condition_many(self):
    import swapi.filter
    ot1 = swapi.filter.condition((
      ('orderTime', '>=', '2015-12-01'),
      ('orderTime', '<=', '2015-12-31'),
    ))
    assert(
      ot1 ==
      'filter[0][property]=orderTime&filter[0][expression]=%3E%3D&filter[0][value]=2015-12-01' +
      '&' +
      'filter[1][property]=orderTime&filter[1][expression]=%3C%3D&filter[1][value]=2015-12-31'
    )
    # lists don't matter:
    ot2 = swapi.filter.condition([
      ['orderTime', '>=', '2015-12-01'],
      ['orderTime', '<=', '2015-12-31'],
    ])
    assert(ot1 == ot2)
