# Copyright Hunter Damron 2018

from .AST import *

MAIN_FN = "main"

def resolve_fn(ast_fn, symbol_table={}):
  pass

def resolve_scope(statements, symbol_table={}, local_start=1):
  pass

def resolve_global(ast_constant, symbol_table={}):
  pass

def generate_llvm(ast):
  symbol_table = {}
  function_table = {}
  llvm_code = ""
  for node in ast:
    if node.fn:
      llvm_code += str(resolve_fn(node))
    else:
      llvm_code += str(resolve_fn(node))
  return "\n".join(str(stmt) for stmt in ast)  # TODO replace with the real deal
