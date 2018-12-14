# Copyright Hunter Damron 2018

from . import tokens
from .util import *

from collections import OrderedDict
from string import whitespace

tokens = OrderedDict((k,v) for k,v in vars(tokens).items() if not k.startswith("_"))
preview_length = 15

class Token:
  def __init__(self, token_type, length, value):
    self.token_type = token_type
    self.length = length
    self.value = value

  def consolidate(self):
    if self.token_type == "_CHAR":
      return self.value  # should be raw character
    else:
      # Consolidate subtokens and smash them together
      return "".join(token.consolidate() for token in self.value)

  def partial_consolidate(self, basecases=[], fmtstr="({1}: {0})"):
    substrs = []
    for sub in self.value:
      if sub.token_type in (basecases + ["_CHAR"]):
        substrs.append(sub.consolidate())
      elif sub.token_type in ["_GRP", "*"]:
        substrs.append("{0}".format(sub.partial_consolidate(basecases=basecases)))
      else:
        substrs.append(fmtstr.format(sub.partial_consolidate(basecases=basecases), sub.token_type))
    return "".join(substrs)

  def __str__(self):
    return "(%s: {%s})" % (self.token_type, self.consolidate())
  def __repr__(self):
    return "(%s: {%s})" % (self.token_type, self.partial_consolidate())

def malformed(name, loc, msg=""):
  perr("Malformed token pattern %s at char %d%s" % (name, loc, " (%s)" % msg if msg else ""))

def findgroup(pattern, grouper="()", innergroups=[], start=0, escape="\\"):
  # Find first instance of grouper, will usually be the first element
  groupstarters = [g[0] for g in innergroups]
  while start < len(pattern) and pattern[start] != grouper[0]:
    start += 1
  if start == len(pattern):
    return None
  brackstack = 1
  end = start + 1
  while brackstack > 0:
    if end >= len(pattern):
      return malformed("_GRP%s" % grouper, start, "Unmatched bracket")
    if pattern[end] in groupstarters:
      grpstart, grpend = findgroup(pattern, grouper=innergroups[groupstarters.index(pattern[end])], start=end, escape=escape)
      end = grpend
    elif pattern[end] == escape:
      if end+1 >= len(pattern):
        return malformed("_GRP%s" % grouper, end, "Unfinished escape")
      end += 1  # Skip two chars if it's escaped
    elif pattern[end] == grouper[1]:
      # Do end grouper first in case they are the same
      brackstack -= 1
    elif pattern[end] == grouper[0]:
      brackstack += 1
    end += 1
  return start, end-1

def findbars(pattern, bar="|", innergroups=["()", "[]"], start=0, escape="\\"):
  groupstarters = [g[0] for g in innergroups]
  bars = []
  i = 0
  while i < len(pattern):
    if pattern[i] in groupstarters:
      grpstart, grpend = findgroup(pattern, grouper=innergroups[groupstarters.index(pattern[i])], start=i, escape=escape)
      i = grpend
    if pattern[i] == escape:
      if i+1 >= len(pattern):
        return malformed("_GRP%s" % grouper, i, "Unfinished escape")
      i += 1  # Skip two chars if it's escaped
    elif pattern[i] == "|":
      bars.append(i)
    i += 1
  return bars

def match_chargroup(code, tokpat, tokname="_CHAR", code_start=0):
  codechar = code[code_start]
  toklen = len(tokpat)
  pverbose("Attempting to match char range with contents '%s'" % tokpat)
  dashes = [j for j in range(toklen) if tokpat[j] == '-']
  backslashes = [j for j in range(toklen) if tokpat[j] == '\\']
  if len(backslashes) != 0:
    pwarn("Escaped characters in char range not yet implemented")  # TODO implement this
  prevdash = toklen-1
  haschar = False
  for dash in dashes:
    if dash == 0 or dash == toklen-1 or tokpat[dash+1] == '-':
      pverbose("Dash at index %d in token length %d" % (dash, toklen))
      return malformed(tokname, dash, "Unmatched dash in range")
    if ord(tokpat[dash-1]) <= ord(codechar) <= ord(tokpat[dash+1]):
      # code char is between range
      haschar = True
    if codechar in tokpat[prevdash+2:toklen-1]:
      # code char is in the raw letters before this dash
      haschar = True
    prevdash = dash
  if codechar in tokpat[prevdash+2:]:
    haschar = True

  if haschar:
    return Token(tokname, 1, codechar)
  else:
    return False

def match_pgroup(code, tokpat, tokname="_GRP", code_start=0):
  bars = [-1] + findbars(tokpat)
  prevbar = len(tokpat)
  for bar in reversed(bars):
    # reversed to do more complex matches first
    pmatch = match(code, (tokname, tokpat[bar+1:prevbar]), code_start=code_start)
    if pmatch:
      return pmatch
    prevbar = bar
  return None  # If none of the innards match, it doesn't match

def match(code, token, code_start=0):
  tokname, tokpat = token  # elements from tokens dictionary
  pverbose("ENTERING MATCH")
  pverbose("Attempting to match token %s: '%s' from code segment '%s%s'"
      % (tokname, tokpat, code[code_start:code_start+min(preview_length, len(code))]
      .replace("\n", " "), "..." if len(code) > preview_length else ""))
  if not tokpat :
    return malformed(tokname, 0, "Cannot match empty pattern")
  c = code_start  # code pointer
  i = 0  # tokpat pointer
  subgroups = []
  matchfun = lambda code, c: None  # function which gets token out of code
  matchtoklen = 1  # amount of the token pattern used by the function (1 is default)
  while i < len(tokpat):
    tchar = tokpat[i]

    # Reset match variables to default
    matchfun = lambda code, c: None
    matchtoklen = 1

    if tchar == '\\':
      if i+1 >= len(tokpat):
        return malformed(tokname, i, "Unfinished escape")
      pverbose("Escaped char %c" % tokpat[i+1])
      refchar = tokpat[i+1]
      matchfun = lambda code, c: Token("_CHAR", 1, code[c]) if code[c] == refchar else None
      matchtoklen = 2
    elif tchar == '[':
      start, endbracket = findgroup(tokpat, grouper="[]", start=i)
      subpattern = tokpat[i+1:endbracket]
      matchfun = lambda code, c: match_chargroup(code, subpattern, code_start=c)
      matchtoklen = endbracket - start + 1
    elif tchar == '(':
      start, endbracket = findgroup(tokpat, grouper="()", start=i)
      print("DBG: ", start, i+1,  endbracket, tokpat[i+1:endbracket])
      subpattern = tokpat[i+1:endbracket]  # Because apparently lambdas don't bind constants
      matchfun = lambda code, c: match_pgroup(code, subpattern, code_start=c)
      matchtoklen = endbracket - start + 1
    elif tchar == "`":
      recursive_token = next((token for token in reversed(tokens.items()) if tokpat[i+1:].startswith(token[0])), None)
      if recursive_token is None:
        return malformed(tokname, i, "Unknown token name")
      matchfun = lambda code, c: match(code, recursive_token, code_start=c)
      matchtoklen = len(recursive_token[0]) + 1
    elif tchar == ' ':
      matchfun = lambda code, c: Token("_CHAR", 1, " ") if code[c] in whitespace else None
    else:
      matchfun = lambda code, c: Token("_CHAR", 1, code[c]) if code[c] == tchar else None

    wildcard = ""
    if i + matchtoklen < len(tokpat):
      postchar = tokpat[i + matchtoklen]
      if postchar in "*+":
        wildcard = postchar
        matchtoklen += 1  # Match the wildcard also
        pverbose("Applying wildcard %s" % wildcard)

    pverbose("Applying token rule of length %d" % matchtoklen)
    # Apply the produced function and add that token to subgroups
    if wildcard:
      i += matchtoklen
      wildcard_matches = []
      matchlen = 0
      done = False
      while not done and c < len(code):
        ctok = matchfun(code, c)
        if ctok:
          pverbose("Found %s subtoken %s at token index %d" % (wildcard, ctok, i-matchtoklen))
          print(ctok.length)
          c += ctok.length
          matchlen += ctok.length
          wildcard_matches.append(ctok)
        else:
          pverbose("Match * exiting")
          done = True
      subgroups.append(Token("*", matchlen, wildcard_matches))
      if wildcard == "+" and not len(wildcard_matches):
        pverbose("Wildcard + not satisfied")
        return None
    else:
      ctok = matchfun(code, c)
      i += matchtoklen  # Move down token by exhausted amount
      if ctok:
        pverbose("Found subtoken %s at token index %d" % (ctok, i-matchtoklen))
        c += ctok.length  # Move down token by matched amount
        subgroups.append(ctok)
      else:
        pverbose("Token not found")
        return None
    pverbose("Subtoken search ending with i=%d and char %s" % (i, tokpat[i] if i < len(tokpat) else "\\0"))
  # If the for loop exits, we have exhausted the pattern so it's a match
  tok = Token(tokname, c-code_start, subgroups)
  pverbose("Matched token %s" % tok)
  pverbose("EXITING MATCH")
  return tok

def matchstatement(code, key="STATEMENT"):
  # matches = {}  # TODO add in ability to keep track of intermediates found
  # TODO in the end this will just match to statements
  val = match(code, (key, tokens[key]))
  if val is not None:
    return val

def tokenize(code):
  linenum = 1
  statements = []
  while len(code):
    statement = matchstatement(code)
    if statement is None:
      print("Error in token in line %d" % linenum)
      break # return None
    statements.append(statement)
    code = code[statement.length:]
    linenum += code[:statement.length].count('\n')
  return statements
