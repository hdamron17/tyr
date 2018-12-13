# Copyright Hunter Damron 2018

from . import tokens
from .util import *

from collections import OrderedDict
from string import whitespace

tokens = OrderedDict((k,v) for k,v in vars(tokens).items() if not k.startswith("_"))

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

  def __str__(self):
    return "(%s: {%s})" % (self.token_type, self.consolidate())
  def __repr__(self):
    return self.__str__()

def malformed(name, loc, msg=""):
  perr("Malformed token pattern %s at char %d%s" % (name, loc, " (%s)" % msg if msg else ""))

def findgroup(pattern, grouper="()", start=0, escape="\\"):
  # Find first instance of grouper, will usually be the first element
  while start < len(pattern) and pattern[start] != grouper[0]:
    start += 1
  if start == len(pattern):
    return None
  brackstack = 1
  end = start + 1
  while brackstack > 0:
    if end >= len(pattern):
      return malformed("_GRP%s" % grouper, start, "Unmatched bracket")
    if pattern[end] == escape:
      pverbose("Escaping %s" % pattern[end+1])  # throw nice error if user escapes the end char
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
    pwarn("Escaped characters in char range not yet implemented")
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
  bars = findbars(tokpat) + [len(tokpat)]
  prevbar = 0
  for bar in bars:
    pverbose("ENTERING MATCH")
    pmatch = match(code, (tokname, tokpat[prevbar:bar]), code_start=code_start)
    pverbose("EXITING MATCH")
    if pmatch:
      return pmatch
    prevbar = bar + 1
  return None  # If none of the innards match, it doesn't match

def match(code, token, code_start=0):
  tokname, tokpat = token  # elements from tokens dictionary
  pverbose("Attempting to match token '%s' from code segment '%s%s'" % (tokpat, code[code_start:code_start+min(10, len(code))].replace("\n", " "), "..." if len(code) > 10 else ""))
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

    if tchar == '[':
      start, endbracket = findgroup(tokpat, grouper="[]", start=i)
      matchfun = lambda code, c: match_chargroup(code, tokpat[i+1:endbracket], code_start=c)
      matchtoklen = endbracket - start + 2
    elif tchar == '(':
      start, endbracket = findgroup(tokpat, grouper="()", start=i)
      matchfun = lambda code, c: match_pgroup(code, tokpat[i+1:endbracket], code_start=c)
      matchtoklen = endbracket - start + 1
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
          c += ctok.length
          matchlen += ctok.length
          wildcard_matches.append(ctok)
        else:
          done = True
      subgroups.append(Token("*", matchlen, wildcard_matches))
      if wildcard == "+" and not len(wildcard_matches):
        return None
    else:
      ctok = matchfun(code, c)
      i += matchtoklen  # Move down token by exhausted amount
      if ctok:
        pverbose("Found subtoken %s at token index %d" % (ctok, i-matchtoklen))
        c += ctok.length  # Move down token by matched amount
        subgroups.append(ctok)
      else:
        return None
    pverbose("Subtoken search ending with i=%d and char %s" % (i, tokpat[i] if i < len(tokpat) else "\\0"))
  # If the for loop exits, we have exhausted the pattern so it's a match
  tok = Token(tokname, c, subgroups)
  pverbose("Matched token %s" % tok)
  return tok

def matchlargest(code):
  # matches = {}  # TODO add in ability to keep track of intermediates found
  # TODO in the end this will just match to statements
  for token in reversed(tokens.items()):
    val = match(code, token)
    if val is not None:
      return val

def tokenize(code):
  linenum = 1
  while len(code):
    val = matchlargest(code)
    print(val)
    if val is None:
      print("Error in token in line %d" % linenum)
      return None
    code = code[val.length:]
    linenum += code[:val.length].count('\n')
