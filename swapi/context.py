# -*- coding: utf-8 -*-

def create(conf, retry=None, fake_error=None):
  """
  Examples:
    - Do not fail unless the third try goes also wrong: retries = 3
    - wait delay_ms between each try
    - Succeed on the 3rd try: fails=2

  retry = dict(retries=2, delay_ms=1)
  fake_error = dict(fails=3)
  ctx = swapi.context(conf)
  """
  res = dict(
    conf = conf,
    retry = dict(
      retries = 3,
      delay_ms = 2000,
    ),
    fake_error = dict(),  # fake_error = dict(fails=2)
  )
  if retry is not None:
    res["retry"].update(retry)
  if fake_error is not None:
    res["fake_error"].update(fake_error)
  return res