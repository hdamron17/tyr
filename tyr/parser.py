# Copyright Hunter Damron 2018

from .util import *
from .lexer import tokens

from enum import Enum

class Identifier:
  def __init__(self, dtype, name, value=None, constant=False, fn=False, inputs=[]):
    self.dtype = dtype
    self.name = name
    self.value = value
    self.constant = constant
    self.fn = fn
    self.inputs = inputs

  def __str__(self):
    return "%s%s %s%s%s" % (
        "const " if self.constant and not self.fn else "",
        self.dtype,
        self.name,
        "(%s)" % ", ".join(str(x) for x in self.inputs) if self.fn else "",
        " = %s" % str(self.value) if self.constant else ""
    )
  __repr__ = __str__

class Scope:
  def __init__(self, statements, condition_type=None, condition=None):
    self.statements = statements  # Must be a list
    self.condition_type = condition_type  # One of IF, WHILE, FOR  # TODO determine the exact details of this
    self.condition = condition  # Type TERM  # TODO use ast types

  def __str__(self):
    return "%s{\n%s\n}" % (
        "%s (%s) " % (self.condition_type, self.condition) if self.condition_type else "",
        "\n".join(str(x) for x in self.statements)
    )
  __repr__ = __str__

class Constant:
  def __init__(self, dtype, value):
    self.dtype = dtype
    self.value = value

  def __str__(self):
    return "%s{%s}" % (self.dtype, self.value)
  __repr__ = __str__

class UnresolvedIdentifier:
  def __init__(self, name):
    self.name = name

  def __str__(self):
    return "Var{%s}" % self.name
  __repr__ = __str__

class Operation:
  def __init__(self, name, inputs):
    self.name = name
    self.inputs = inputs

  def __str__(self):
    return "%s(%s)" % (self.name, ",".join(str(x) for x in self.inputs))
  __repr__ = __str__

class Statement:
  def __init__(self, value, lval=None, declares=[]):
    self.value = value
    self.lval = None
    self.declares = declares

default_parser = lambda n: n.consolidate()
single_id = lambda x: x[0]  # Not an actual id but like a passthrough for length one signatures

def parse_fn_def(n):
  declaration, inputs, body = split_token(n, ("DECLARATION", "DECLARATION*", "BODY"))
  return Identifier(declaration.dtype, declaration.name, value=body, constant=True, fn=True, inputs=inputs)

def parse_const_def(n):
  declaration, value = split_token(n, ("DECLARATION", "TERM"))
  return Identifier(declaration.dtype, declaration.name, value=value, constant=True)

def parse_declaration(n):
  dtype, name = split_token(n, ("DTYPE", "IDENTIFIER"))
  return Identifier(dtype, name.name)  # name.name because we want to resolve

def parse_body(n):
  return pattern_match(n, {
    ("STATEMENT",): lambda statement: Scope(statement),
    ("SCOPE",): single_id
  })

def parse_scope(n):
  conditional_lambda = single_id
  return pattern_match(n, {
    ("STATEMENT*",): lambda block: Scope(block[0]),
    ("IF",): conditional_lambda,
    ("WHILE",): conditional_lambda
  })

def parse_conditional(n, ctype):
  # ctype is "IF", "WHILE", or "FOR"
  condition, body = split_token(n, ("PTERM", "BODY"))
  return Scope(body.statements, condition_type=ctype, condition=condition)

def parse_statement(n):
  if not len(token_subgroups(n)):
    return "EMPTY"  # TODO make an empty statement possible and deal with it
  return passthrough(n)

def parse_funcall(n):
  return pattern_match(n, {
    ("IDENTIFIER", "TERM*"): lambda block: Operation(block[0], block[1]),
  })

def parse_operation(n):
  binop_fn = lambda block: Operation(block[1], [block[0], block[2]])
  uniop_fn = lambda block: Operation(block[0], [block[1]])
  return pattern_match(n, {
    ("LTERM","WBINOP","TERM"): binop_fn,
    ("WUNIOP","TERM"): uniop_fn,
    ("LTERM","BINOP","TERM"): binop_fn,
    ("UNIOP","TERM"): uniop_fn
  })

def parse_number(n):
  return pattern_match(n, {
    ("DIGITS","DIGITS"): lambda block: Constant("float", float(".".join(block))),
    ("DIGITS",): lambda block: Constant("int", int(block[0]))
  })

def passthrough(n):
  subs = token_subgroups(n)
  if not subs:
    return malformed("Cannot passthrough item because there are no matches", -1)
  else:
    return process_node(subs[0])

parse_functions = {
  "GLOBAL": lambda n: multi_match(n, [("FUNDEF",), ("CONSTANT",)], single_id),
  "FUNDEF": parse_fn_def,
  "CONSTANT": parse_const_def,
  "DECLARATION": parse_declaration,
  "BODY": parse_body,
  "SCOPE": parse_scope,
  "IF": partial(parse_conditional, ctype="IF"),
  "WHILE": partial(parse_conditional, ctype="WHILE"),
  "STATEMENT": parse_statement,
  "PTERM": passthrough,
  "TERM": passthrough,
  "LTERM": passthrough,
  "FUNCALL": parse_funcall,
  "OPERATION": parse_operation,
  "IDENTIFIER": lambda n: UnresolvedIdentifier(n.consolidate()),  # TODO possibly deal with SIDENTIFIER
  "NUMBER": parse_number,
  "*": lambda n: [process_node(sub) for sub in n.value]
}

allow_default = ["DIGITS", "LETTER", "DTYPE", "BINOP", "UNIOP", "WBINOP", "WUNIOP"]

def pattern_match(n, signature_map, default_fn=None, required=True, comm_fn=None):
  # Signature map must be a dictionary of signature lists to parse functions
  for k, v in signature_map.items():
    parsed = split_token(n, k, required=False)
    if parsed and all(parsed):
      if comm_fn:
        parsed = comm_fn(parsed)
      return v(parsed)
  pdebug("Pattern match reached default function with signatures [%s]" % ", ".join(str(x) for x in signature_map.items()))
  if default_fn:
    return default_fn(n)
  if required:
    return malformed("Unable to apply pattern match with keys {%s}" % ", ".join(str(x) for x in signature_map.keys()), -1)

def multi_match(n, signature_list, fn, **kw):
  return pattern_match(n, {tuple(pat): fn for pat in signature_list}, **kw)

def token_subgroups(n):
  subgroups = []
  for sub in n.value:
    if sub.token_type in ("_GRP", "*"):
      subgroups += token_subgroups(sub)
    elif sub.token_type in tokens.keys():
      subgroups.append(sub)
    # Anything else, including _CHAR is ignored
  return subgroups

# @override_verb
def split_token(n, signature, required=True):
  splits = []
  vnum = 0
  subgroups = token_subgroups(n)
  for i, token_type in enumerate(signature):
    pdebug("Searching for token %s" % token_type)
    wildcard = token_type.endswith("*")
    if wildcard:
      token_type = token_type.rstrip("*")
    donext = False
    curr_subgroup = []
    while not donext:
      if vnum >= len(subgroups):
        if wildcard:
          break
        elif not required:
          return None  # Return nothing but not in an aggressive way
        else:
          return malformed("Unable to unpack token into %d subgroups" % len(signature), -1)
      pdebug("Looking at index %d of type %s for type %s" % (vnum, subgroups[vnum].token_type, token_type))
      if wildcard and i+1 < len(signature) and subgroups[vnum].token_type == signature[i+1].rstrip("*"):
        pdebug("Breaking out of wildcard")
        donext = True
        continue
      if subgroups[vnum].token_type == token_type:
        if wildcard:
          pdebug("Adding type %s * : %s" % (token_type, subgroups[vnum]))
          curr_subgroup.append(process_node(subgroups[vnum]))
        else:
          pdebug("Adding type %s : %s" % (token_type, subgroups[vnum]))
          curr_subgroup = process_node(subgroups[vnum])
          donext = True
      vnum += 1
    splits.append(curr_subgroup)
    pdebug("After adding %s, splits is now %s" % (token_type, [str(x) for x in splits]))
  return splits

def process_node(node):
  fn = parse_functions.get(node.token_type, default_parser)
  if fn is default_parser:
    if node.token_type not in tokens:
      pwarn("Unknown token type %s" % node.token_type)
    elif node.token_type not in allow_default:
      pwarn("Applying default parser to %s with type %s" % (node.consolidate(), node.token_type))  # TODO remove this
  return fn(node)

# Accepts a syntax tree of class lexer.Token
@override_verb
def parse(syntax_tree):
  ast = []
  for i, node in enumerate(syntax_tree):
    node_ast = process_node(node)
    if node_ast is None:
      perr("Failed to process node %d" % i)
      return None
    ast.append(node_ast)
  return ast
