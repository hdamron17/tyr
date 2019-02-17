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
    pdebug(type(fn.name))
    return "@_" + fn.name + "_" + ("".join(p.dtype[0] for p in fn.inputs) if len(fn.inputs) else "v")

# TODO do two passes to allow calling function declared later
def resolve_fn(ast_fn, symbol_table, fn_table, llvm_consts):
  llvm_dtype = dtype_map.get(ast_fn.dtype)
  llvm_name = name_mangle(ast_fn)
  fn_table[llvm_name] = llvm_dtype  # TODO make sure there is no name clash
  local_symbol_table = {("%" + p.name): p for p in ast_fn.inputs}
  local_symbol_table.update(symbol_table)
  llvm_params = ", ".join(dtype_map.get(p.dtype) + " %" + p.name for p in ast_fn.inputs)
  llvm_decl = "define %s %s (%s) #%d" % (llvm_dtype, llvm_name, llvm_params, len(ast_fn.inputs))
  local_end, llvm_statements = resolve_scope(ast_fn.value, local_symbol_table, fn_table, llvm_consts)
  llvm_statements += [("ret %s" % llvm_dtype) + " 0" if llvm_dtype != "void" else ""]  # TODO deal with non integer types and proper returns
  llvm_fn = "%s {\n%s\n}\n" % (llvm_decl, "\n".join(llvm_statements))
  return llvm_name, llvm_fn

def resolve_scope(ast_node, symbol_table, fn_table, llvm_consts, local_start=1):
  llvm_statements = []
  # TODO handle conditionals and loops
  for node in ast_node.statements:
    pdebug("local_start:", local_start)
    pdebug("constants:", llvm_consts)
    if isinstance(node, Scope):
      pdebug(node.statements)
      local_start, node_llvm_statements = resolve_scope(node, symbol_table, fn_table, llvm_consts, local_start)
      llvm_statements += ["; begin scope"] + node_llvm_statements + ["; end scope"]
    elif isinstance(node, Statement):
      pdebug("TODO")
      print(node)
    else:
      expr_name, expr_dtype, local_start, node_llvm_statements = resolve_expr(node, symbol_table, fn_table, llvm_consts, local_start)
      llvm_statements += node_llvm_statements
  return local_start, llvm_statements

def resolve_expr(ast_node, symbol_table, fn_table, llvm_consts, local_start):
  '''
  Returns expr_name, expr_dtype, local_end, node_llvm_statements
  '''
  if isinstance(ast_node, Operation):
    pdebug("Operation")
    if ast_node.name == "+":
      perr("+ operator not implemente")  # TODO
    # TODO handle all builtin operators
    else:
      pdebug("Operator %s" % ast_node.name)
      pdebug(", ".join(str(x) for x in ast_node.inputs))
      ast_node.name = ast_node.name.name  # Resolve identifier
      llvm_name = name_mangle(ast_node)
      fn_dtype = fn_table.get(llvm_name, None)
      if not fn_dtype:
        perr("Unresolved function name %s [%s]" % (ast_node.name, llvm_name))
        return "", "void", local_start, []  # TODO handle this better
      llvm_call =  ""
      if fn_dtype != "void":
        llvm_ret = ("%%%d" % local_start)  # TODO check this
        local_start += 1
        llvm_call += llvm_ret + " = "
      else:
        llvm_ret = ""
      llvm_param_dtypes = []
      llvm_param_decls = []
      llvm_statements = []
      for param in ast_node.inputs:
        param_name, param_dtype, local_start, param_llvm_statements = resolve_expr(param, symbol_table, fn_table, llvm_consts, local_start)
        llvm_param_dtypes.append(param_dtype)  # TODO check for valid types
        llvm_param_decls.append("%s %s" % (param_dtype, param_name))
        llvm_statements += param_llvm_statements
      llvm_call += "call %s (%s) %s (%s)" % (fn_dtype, ", ".join(llvm_param_dtypes), llvm_name, ", ".join(llvm_param_decls))
      llvm_statements.append(llvm_call)
      # TODO expand parameters into llvm_statements

      return llvm_ret, fn_dtype, local_start, llvm_statements
      # TODO actually check name
  elif isinstance(ast_node, Constant):
    pdebug("Constant")
    key = (ast_node.dtype, ast_node.value)
    print(key, llvm_consts)
    if key in llvm_consts:
      llvm_const_name = llvm_consts[key][0]
      llvm_dtype = dtype_map.get(key[0])
    else:
      llvm_const_name = "@.const.%d" % len(llvm_consts.keys())
      pdebug("New constant %s" % llvm_const_name)
      llvm_dtype = dtype_map.get(ast_node.dtype)
      llvm_consts[key] = (llvm_const_name, " = private constant %s %s" % (llvm_dtype, ast_node.value))
    llvm_name = "%%%d" % local_start
    llvm_statement = "%s = load %s, %s* %s" % (llvm_name, llvm_dtype, llvm_dtype, llvm_const_name)
    local_start += 1
    return llvm_name, llvm_dtype, local_start, [llvm_statement]
  else:
    perr("Unrecognized expression (%s) %s" % (type(ast_node), ast_node))
  return "", "void", local_start, []  # TODO check that this is not used

def resolve_global(ast_const, symbol_table, llvm_consts={}):
  # TODO allow const expressions to be evaluated
  llvm_dtype = dtype_map.get(ast_const.dtype)
  if ast_const.dtype != ast_const.value.dtype:
    pwarn("Type mismatch in symbol %s: expected %s, got %s" % (ast_const.name, ast_const.dtype, ast_const.value.dtype))
  llvm_statement = "@_%s = private constant %s %s\n" % (ast_const.name, llvm_dtype, ast_const.value.value)
  return llvm_statement

def add_header_declarations(header, symbol_table, fn_table):
  # TODO automate this
  fn_table["@_print_i"] = "void"

def generate_llvm(ast):
  symbol_table = {}
  fn_table = {}

  header = open(pathjoin(PY_ROOT, "llvm_code/stdio.ll")).read()
  add_header_declarations(header, symbol_table, fn_table)

  llvm_consts = {}
  llvm_code = ""
  for node in ast:
    pdebug("Globals:", symbol_table)
    pdebug("Functions:", fn_table)
    if node.fn:
      llvm_name, llvm_fn_code = resolve_fn(node, symbol_table, fn_table, llvm_consts)
      llvm_code += llvm_fn_code
    else:
      if node.name in symbol_table:
        perr("Redefinition of %s" % node.name)
      llvm_code += resolve_global(node, symbol_table, llvm_consts)
      symbol_table["@_" + node.name] = node
  constants = "\n".join(v[0] + v[1] for k, v in llvm_consts.items())
  return header + "\n" + constants + "\n" + llvm_code
