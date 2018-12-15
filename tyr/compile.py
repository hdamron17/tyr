# Copyright Hunter Damron 2018

from . import lexer
from .util import *

def compile(ifile, ofile):
  success = False
  bincode = ""
  with open(ifile, 'r') as ireader:
    code = ireader.read()
    token_tree = lexer.tokenize(code)
    if not token_tree:
      perr("Unable to create token tree, giving up.")
      return
    pverbose("TOKEN TREE\n=====\n%s\n=====" % "\n".join(str(s.consolidate()) for s in token_tree))
    success = True

  if success:
    with open(ofile, 'w+') as owriter:
      owriter.write(bincode)

  print("Unimplemented, copying instead")
  from shutil import copyfile
  copyfile(ifile, ofile)
