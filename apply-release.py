#! /usr/bin/env python3
# Copyright Hunter Damron 2018

from subprocess import check_output, CalledProcessError
from sys import stdout
from tyr.version import *

if __name__ == "__main__":
  git_versions = check_output("git tag".split()).decode(stdout.encoding)
  if VERSION not in git_versions and not VERSION.startswith("0.0.0"):
    version_type = "major " if ismajor() else "minor " if isminor() else ""
    cmd = ("git tag -a v%s -m" % VERSION).split() + ["\"%s\"" % VERSION_MSG] if ismajor() or isminor() else ("git tag %s" % VERSION).split()
    check_output(cmd).decode(stdout.encoding)
    print("Updated git version to %srelease %s" % (version_type, VERSION))
  else:
    print("Version %s already tracked by git" % VERSION)
