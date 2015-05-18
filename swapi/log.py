# -*- coding: utf-8 -*-

# Todo: Console and file logging needs some functional tests

def create():
  # 1) If a SWAPI logger was configured already, use that one:
  import easylog
  log = easylog.get("SWAPI")
  if log is not None:
    return log

  # 2) Should we log to a file? Good for library development.
  # Look at environment:
  import os
  logfile = os.environ.get('SWAPI_LOGFILE', default = None)
  if logfile is not None:
    log = easylog.create("SWAPI", level = "DEBUG", path = logfile)
    return log

  #3) default is a standard WARNING level logger.
  # This should be the right thing for users of this library, see
  # see https://docs.python.org/3/howto/logging.html#configuring-logging-for-a-library >
  log = easylog.create("SWAPI", level = "WARNING")
  return log
