# Copyright Hunter Damron 2018

from . import lexer

def compile(ifile, ofile):
  success = False
  bincode = ""
  with open(ifile, 'r') as ireader:
    code = ireader.read()
    ast = lexer.tokenize(code)
    success = True

  if success:
    with open(ofile, 'w+') as owriter:
      owriter.write(bincode)

  print("Unimplemented, copying instead")
  from shutil import copyfile
  copyfile(ifile, ofile)
