# Copyright Hunter Damron 2018

from .AST import *
from .util import *

MAIN_FN = "main"

dtype_map = {
  "void": "void",
  "bool": "i1",
  "char": "i8",
  "int": "i32",
  "float": "double",
  "str": "i8*"
  # TODO deal with strings differently
}

def name_mangle(fn):
  if fn.name == MAIN_FN:
    return "@" + fn.name
  else:
    return "@_" + fn.name + "_" + ("".join(p.name[0] for p in fn.inputs) if len(fn.inputs) else "v")

def resolve_fn(ast_fn, symbol_table={}, fn_table=[]):
  llvm_dtype = dtype_map.get(ast_fn.dtype)
  llvm_name = name_mangle(ast_fn)
  llvm_params = ", ".join(dtype_map.get(p.dtype) + " %" + p.name for p in ast_fn.inputs)
  llvm_decl = "define %s %s (%s) #%d" % (llvm_dtype, llvm_name, llvm_params, len(ast_fn.inputs))
  llvm_statements = [("ret %s" % llvm_dtype) + " 0" if llvm_dtype != "void" else ""]  # TODO deal with non integer types and proper returns
  llvm_fn = "%s {\n%s\n}\n" % (llvm_decl, "\n".join(llvm_statements))
  return llvm_name, llvm_fn

def resolve_scope(statements, symbol_table={}, local_start=1):
  pass

def resolve_global(ast_constant, symbol_table={}):
  pass

def generate_llvm(ast):
  symbol_table = {}
  fn_table = []
  llvm_code = ""
  for node in ast:
    if node.fn:
      llvm_name, llvm_fn_code = resolve_fn(node, symbol_table=symbol_table, fn_table=fn_table)
      llvm_code += llvm_fn_code
      fn_table.append(llvm_name)
    else:
      llvm_code += resolve_fn(node)  # TODO change this for constants
  return llvm_code
