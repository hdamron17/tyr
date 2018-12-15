# Copyright Hunter Damron 2018

import sys
from functools import partial

_VERBOSE = 3
# Verbosity levels are as follows:
# 0. Silent
# 1. Allow errors
# 2. Allow warnings
# 3. Allow info messages
# 4. Allow verbose messages
# 5. Allow extra verbose debug messages

def setverbosity(b=3):
  global _VERBOSE
  _VERBOSE = b

def override_verb(fn, b=3):
  def override_fn(*args, **kwargs):
    global _VERBOSE
    oldverbosity = _VERBOSE
    if _VERBOSE != b:
      pwarn("Overriding verbosity in function %s" % fn.__name__)
    setverbosity(b)
    ret = fn(*args, **kwargs)
    setverbosity(oldverbosity)
    return ret
  return override_fn

def override_verb2(b):
  return partial(override_verb, b=b)

_COLOR = True

def setcolor(b=True):
  global _COLOR
  _COLOR = b

class colors:
  RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(31, 38)

def pinfo(*s, level=3, err=False, color=0, prefix="", **kw):
  if _VERBOSE >= level:
    s = prefix + " ".join(str(x) for x in s)
    if color and _COLOR:
      s = ('\033[%sm' % color) + s + '\033[0m'

    if err:
      print(s, file=sys.stderr, **kw)
    else:
      print(s, **kw)

def perr(*s, color=colors.RED, **kw):
  pinfo(*s, level=1, err=True, color=color, prefix="ERROR: ", **kw)

def pwarn(*s, color=colors.YELLOW, **kw):
  pinfo(*s, level=2, err=True, color=color, prefix="WARN: ", **kw)

def pverbose(*s, **kw):
  pinfo(*s, level=4, **kw)

def pdebug(*s, **kw):
  pinfo(*s, level=5, **kw)
