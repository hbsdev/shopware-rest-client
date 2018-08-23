# -*- coding: utf-8 -*-

def retry(retries=3,pause_sec=0):

  left = {'retries': retries}

  def decorator(f):
    def inner(*args, **kwargs):
      print('') # Start with a fresh line
      while left['retries']:
        if left['retries'] == 1:
          # do not catch
          # exception on the last try:
          print ("Last Retry ...")
          return f(*args, **kwargs)
        # not the last try, do not throw:
        try:
          return f(*args, **kwargs)
        except Exception as e:
          left['retries'] -= 1
          print ("Exception caught (retries Left %s):" % left['retries'])
          print (e)
          if pause_sec > 0:
            import time
            time.sleep(pause_sec)
    return inner
  return decorator
