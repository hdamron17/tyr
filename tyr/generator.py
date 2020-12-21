# Copyright Hunter Damron 2018

from .AST import *
from .util import *
from . import llvm_code

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

rev_dtype_map = {v: k for k, v in dtype_map.items()}

# TODO handle different dtypes
op_map = {
  "+": "add",
  "-": "sub",
  "*": "mul",
  "/": "sdiv",
  "==": "icmp eq",
  "!=": "icmp ne",
}

def name_mangle(fn):
  pdebug("Mangling %s" % fn.name)
  if fn.name == MAIN_FN:
    return "@" + fn.name
  else:
    return "@_" + fn.name + "_" + ("".join(p.dtype[0] for p in fn.inputs) if len(fn.inputs) else "v")

# TODO do two passes to allow calling function declared later
def resolve_fn(ast_fn, symbol_table, fn_table, llvm_consts):
  llvm_dtype = dtype_map.get(ast_fn.dtype)
  llvm_name = name_mangle(ast_fn)
  fn_table[llvm_name] = llvm_dtype  # TODO make sure there is no name clash
  local_symbol_table = {("%" + p.name): (p, False) for p in ast_fn.inputs}
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
    pdebug("variables:", symbol_table)
    if isinstance(node, Scope):
      pdebug(node.statements)
      local_start, node_llvm_statements = resolve_scope(node, symbol_table, fn_table, llvm_consts, local_start)
      llvm_statements += ["; begin scope"] + node_llvm_statements + ["; end scope"]
    elif isinstance(node, Statement):
      pdebug("TODO %s" % node)
      expr_name, expr_dtype, local_start, node_llvm_statements = resolve_expr(node.value, symbol_table, fn_table, llvm_consts, local_start)
      node_llvm_statements.append("; TODO Assign to variable %s -> %s" % (expr_name, node.lval))
      llvm_statements += node_llvm_statements  # TODO change this maybe?
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
    llvm_param_dtypes = []
    llvm_param_names = []
    llvm_param_decls = []
    llvm_statements = []
    for i, param in enumerate(ast_node.inputs):
      if isinstance(param, UnresolvedIdentifier):
        pdebug("Resolving parameter %s" % ast_node)
        pname = param.name
        param = ast_node.inputs[i] = symbol_table.get("%" + param.name)[0]
        if not param:
          perr("Unresolved identifier %s" % pname)
          exit(1)
      param_name, param_dtype, local_start, param_llvm_statements = resolve_expr(param, symbol_table, fn_table, llvm_consts, local_start)
      llvm_param_dtypes.append(param_dtype)  # TODO check for valid types
      llvm_param_names.append(param_name)
      llvm_param_decls.append("%s %s" % (param_dtype, param_name))
      llvm_statements += param_llvm_statements
      ast_node.inputs[i].dtype = param_dtype

    if ast_node.name in op_map.keys():
      llvm_name = op_map[ast_node.name]
      fn_dtype = ast_node.inputs[0].dtype  # TODO Assert that all operands have same dtype
      # TODO use different mapping for different types
      if ast_node.name in "-+" and len(llvm_param_names) == 1:
        llvm_param_names = ["0"] + llvm_param_names  # For unary +,- add or subtract 0
      llvm_call = "%s %s %s" % (llvm_name, fn_dtype, ", ".join(llvm_param_names))
      # TODO other symbol operators
    else:
      if isinstance(ast_node.name, UnresolvedIdentifier):
        ast_node.name = ast_node.name.name  # Resolve identifier
      llvm_name = name_mangle(ast_node)
      fn_dtype = fn_table.get(llvm_name)
      if not fn_dtype:
        perr("Unresolved function name %s [%s]" % (ast_node.name, llvm_name))
        return "", "void", local_start, []  # TODO handle this better
      # TODO handle all builtin operators
      pdebug("Operator %s" % ast_node.name)
      pdebug(", ".join(str(x) for x in ast_node.inputs))
      llvm_call = "call %s (%s) %s (%s)" % (fn_dtype, ", ".join(llvm_param_dtypes), llvm_name, ", ".join(llvm_param_decls))

    llvm_call_ret =  ""
    if fn_dtype != "void":
      llvm_ret = ("%%%d" % local_start)  # TODO check this
      local_start += 1
      llvm_call_ret += llvm_ret + " = "
    else:
      llvm_ret = ""

    return llvm_ret, fn_dtype, local_start, llvm_statements + [llvm_call_ret + llvm_call]

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

  elif isinstance(ast_node, UnresolvedIdentifier):
    pdebug("Resolving identifier %s" % ast_node)
    resolved, needs_deref = symbol_table.get("%" + ast_node.name)
    if not resolved:
      perr("Unresolved identifier %s" % ast_node.name)
      return "", "void", local_start, []
    return resolve_expr(resolved, symbol_table, fn_table, llvm_consts, local_start)

  elif isinstance(ast_node, Identifier):
    llvm_dtype = dtype_map.get(ast_node.dtype)
    llvm_prederef_name = "%" + ast_node.name
    if "%" + ast_node.name not in symbol_table:
      perr("Unresolved identifier %s" % ast_node)
    llvm_statements = []
    if symbol_table.get(llvm_prederef_name)[1]:
      # Needs deref
      llvm_name = "%%%d" % local_start
      local_start += 1
      llvm_statement = "%s = load %s, %s* %s" % (llvm_name, llvm_dtype, llvm_dtype, llvm_prederef_name)
      return llvm_name, llvm_dtype, local_start, [llvm_statement]
    else:
      return llvm_prederef_name, llvm_dtype, local_start, []

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
  symbol_table = {}  # Maps string llvm_name -> AST node, bool needs dereference
  fn_table = {}

  header = llvm_code.stdio()
  add_header_declarations(header, symbol_table, fn_table)

  llvm_consts = {}
  llvm_body = ""
  for node in ast:
    pdebug("Globals:", symbol_table)
    pdebug("Functions:", fn_table)
    if node.fn:
      llvm_name, llvm_fn_code = resolve_fn(node, symbol_table, fn_table, llvm_consts)
      llvm_body += llvm_fn_code
    else:
      if node.name in symbol_table:
        perr("Redefinition of %s" % node.name)
      llvm_body += resolve_global(node, symbol_table, llvm_consts)
      symbol_table["@_" + node.name] = (node, True)
  constants = "\n".join(v[0] + v[1] for k, v in llvm_consts.items())
  return header + "\n" + constants + "\n" + llvm_body
