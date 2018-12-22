# Copyright Hunter Damron 2018

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
    self.lval = lval
    self.declares = declares  # TODO figure out what declares does

  def __str__(self):
    return "%s%s%s;" % (
        str(self.lval) if self.lval else "",
        " = " if self.lval and self.value else "",
        str(self.value) if self.value else ""
    )
  __repr__ = __str__
