import os.path

VERSIONS_FILE = "../VERSIONS.txt"

versions = list(filter(None, open(os.path.join(os.path.dirname(__file__), VERSIONS_FILE), 'r').read().split("\n")))
_version = versions[0].split(" ", 1)
if len(_version) > 1:
  VERSION, VERSION_MSG = _version
else:
  VERSION = _version[0]
  VERSION_MSG = ""

prev = versions[1].split()[0] if len(versions) > 1 else "0.0.0"

def version_tuple(version):
  vlist = version.split(".")
  if len(vlist) < 3:
    vlist += [0] * (3 - len(vlist))
  return tuple(vlist)

def version_diff(v1, v2):
  return [x != y for x,y in zip(version_tuple(v1), version_tuple(v2))]

def ismajor():
  return version_diff(VERSION, prev)[0]

def isminor():
  return version_diff(VERSION, prev)[1]
