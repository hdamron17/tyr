# Copyright Hunter Damron 2018

import sys

VERBOSE = 3
# Verbosity levels are as follows:
# 0. Silent
# 1. Allow errors
# 2. Allow warnings
# 3. Allow info messages
# 4. Allow debug messages
# 5. Allow extra verbose debug messages

def setverbosity(b=3):
  global VERBOSE
  VERBOSE = b

def pinfo(s, level=3, err=False):
  if VERBOSE >= level:
    if err:
      print(s, file=sys.stderr)
    else:
      print(s)

def perr(s):
  pinfo(s, level=1)

def pwarn(s):
  pinfo(s, level=2)

def pdebug(s):
  pinfo(s, level=4)

def pverbose(s):
  pinfo(s, level=5)
