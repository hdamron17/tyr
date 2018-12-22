# Copyright Hunter Damron 2018

from . import lexer, parser, generator
from .util import *

def compile(code):
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

  output_code = generator.generate_llvm(ast)
  if not output_code:
    perr("Unable to produce llvm code, giving up.")
    return
  pverbose("LLVM Output Code\n-----\n%s\n=====" % output_code)
  return output_code

def compile_file(ifile, ofile):
  with open(ifile, 'r') as ireader:
    code = ireader.read()
    output_code = compile(code)

    if output_code is not None:
      with open(ofile, 'w+') as owriter:
        owriter.write(output_code)

  # TODO remove the copying part
  pwarn("Unimplemented, copying instead")
  from shutil import copyfile
  copyfile(ifile, ofile)
