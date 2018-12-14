# Copyright Hunter Damron 2018

from . import lexer
from .util import *

def compile(ifile, ofile):
  success = False
  bincode = ""
  with open(ifile, 'r') as ireader:
    code = ireader.read()
    ast = lexer.tokenize(code)
    pverbose("=====\n%s\n=====" % "\n".join(str(s.partial_consolidate(basecases=["DIGITS", "STRING", "IDENTIFIER"])) for s in ast))
    success = True

  if success:
    with open(ofile, 'w+') as owriter:
      owriter.write(bincode)

  print("Unimplemented, copying instead")
  from shutil import copyfile
  copyfile(ifile, ofile)
