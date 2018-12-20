#! /usr/bin/env python3
# Copyright Hunter Damron 2018

"""
Usage:
  tyrc [options] <file> [-o <output>]

Options:
  -d, --debug           Be extremely verbose in debug mode
  -h, --help            Show this help screen
  --no-color            Disable color output
  -o <output>, --output=<output>  Specify LLVM IR output file [default: a.ll]
  -v, --verbose         Be verbose
  -V, --version         Print version
"""
from docopt import docopt

from tyr import util, compiler, VERSION

def main():
  args = docopt(__doc__, version='tyrc %s' % VERSION)
  ifile = args['<file>']
  ofile = args['--output']
  if args['--verbose']:
    util.setverbosity(4)
  if args['--debug']:
    util.setverbosity(5)
  if args['--no-color']:
    util.setcolor(False)
  compiler.compile_file(ifile, ofile)

if __name__ == "__main__":
  main()
