def is_set(conf):
  proto, server, basepath, user, key, use_query_plugin, sw4_compat = conf
  if sw4_compat == 0:
    return False
  if sw4_compat == 1:
    return True
  raise Exception('Please set sw4_compat in conf to 0 or 1')
