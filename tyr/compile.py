# Copyright Hunter Damron 2018

from . import lexer, parser
from .util import *

def compile(ifile, ofile):
  success = False
  bincode = ""
  with open(ifile, 'r') as ireader:
    code = ireader.read()
    syntax_tree = lexer.tokenize(code)
    if not syntax_tree:
      perr("Unable to create token tree, giving up.")
      return
    pverbose("TOKEN TREE\n-----\n%s\n=====" % "\n".join(str(s.consolidate()) for s in syntax_tree))

    ast = parser.parse(syntax_tree)
    if not ast:
      perr("Unable to process the created syntax tree, giving up.")
      return
    pverbose("AST\n-----\n%s\n=====" % "\n".join(str(s) for s in ast))

    success = True

  if success:
    with open(ofile, 'w+') as owriter:
      owriter.write(bincode)

  print("Unimplemented, copying instead")
  from shutil import copyfile
  copyfile(ifile, ofile)
