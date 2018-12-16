# Copyright Hunter Damron 2018

from .tokens import reserved_chars, wildcards
from . import tokens
from .util import *

from collections import OrderedDict
from string import whitespace

tokens = OrderedDict((k,v) for k,v in vars(tokens).items() if k[0].isupper())
preview_length = 15

class Token:
  def __init__(self, token_type, length, value, signature):
    self.token_type = token_type
    self.length = length
    self.value = value
    self.signature = signature

  def consolidate(self):
    if self.token_type == "_CHAR":
      return self.value  # should be raw character
    if self.token_type == "COMMENT":
      return " "
    else:
      # Consolidate subtokens and smash them together
      return "".join(token.consolidate() for token in self.value)

  def partial_consolidate(self, basecases=[], fmtstr="({1}: {0})"):
    substrs = []
    for sub in self.value:
      if isinstance(sub, str):
        substrs.append(sub)
      elif sub.token_type in (basecases + ["_CHAR"]):
        substrs.append(sub.consolidate())
      elif sub.token_type in ["_GRP", "*"]:
        substrs.append("{0}".format(sub.partial_consolidate(basecases=basecases)))
      else:
        substrs.append(fmtstr.format(sub.partial_consolidate(basecases=basecases), sub.token_type))
    return "".join(substrs)

  def __str__(self):
    return "(%s: {%s})" % (self.token_type, self.consolidate())
  # def __repr__(self):
  #   return "(%s{%s}: {%s})" % (self.token_type, self.signature, self.partial_consolidate())
  __repr__ = __str__

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
  pdebug("Attempting to match char range with contents '%s'" % tokpat)
  dashes = [j for j in range(toklen) if tokpat[j] == '-']
  backslashes = [j for j in range(toklen) if tokpat[j] == '\\']
  if len(backslashes) != 0:
    pwarn("Escaped characters in char range not yet implemented")  # TODO implement this
  prevdash = toklen-1
  haschar = False
  for dash in dashes:
    if dash == 0 or dash == toklen-1 or tokpat[dash+1] == '-':
      pdebug("Dash at index %d in token length %d" % (dash, toklen))
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
    return Token(tokname, 1, codechar, "[" + tokpat + "]")
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

def match_whitespace(code, code_start=0):
  if code[code_start] in whitespace:
    return Token("_CHAR", 1, " ", code[code_start])
  else:
    comment_key = "COMMENT"
    comment = match(code, (comment_key, tokens[comment_key]), code_start=code_start)
    return comment if comment else None

def match(code, token, code_start=0):
  if len(code) - code_start <= 0:
    return None
  tokname, tokpat = token  # elements from tokens dictionary
  pdebug("ENTERING MATCH")
  pdebug("Attempting to match token %s: '%s' from code segment '%s%s'"
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
      if i+1 >= len(tokpat) or tokpat[i+1] not in reserved_chars:
        return malformed(tokname, i, "Unfinished escape")
      pdebug("Escaped char %c" % tokpat[i+1])
      refchar = tokpat[i+1]
      matchfun = lambda code, c: Token("_CHAR", 1, code[c], tokpat[i:i+2]) if code[c] == refchar else None
      matchtoklen = 2
    elif tchar == '[':
      start, endbracket = findgroup(tokpat, grouper="[]", start=i)
      subpattern = tokpat[i+1:endbracket]
      matchfun = lambda code, c: match_chargroup(code, subpattern, code_start=c)
      matchtoklen = endbracket - start + 1
    elif tchar == '(':
      start, endbracket = findgroup(tokpat, grouper="()", start=i)
      subpattern = tokpat[i+1:endbracket]  # Because apparently lambdas don't bind constants
      matchfun = lambda code, c: match_pgroup(code, subpattern, code_start=c)
      matchtoklen = endbracket - start + 1
    elif tchar == "`":
      recursive_token = next((token for token in reversed(tokens.items()) if tokpat[i+1:].startswith(token[0])), None)
      if recursive_token is None:
        return malformed(tokname, i, "Unknown token name")
      matchfun = lambda code, c: match(code, recursive_token, code_start=c)
      matchtoklen = len(recursive_token[0]) + 1
    elif tchar == '$':
      ungreedy_i = i + (2 if i+1 < len(tokpat) and tokpat[i+1] in wildcards else 1)
      matchfun = lambda code, c: Token("_CHAR", 1, code[c], tchar) if not match(code, ("",tokpat[ungreedy_i:]), code_start=c) else None
    elif tchar == ' ':
      matchfun = lambda code, c: match_whitespace(code, c)
    else:
      matchfun = lambda code, c: Token("_CHAR", 1, code[c], tchar) if code[c] == tchar else None

    wildcard = ""
    if i + matchtoklen < len(tokpat):
      postchar = tokpat[i + matchtoklen]
      if postchar in wildcards:
        wildcard = postchar
        matchtoklen += 1  # Match the wildcard also
        pdebug("Applying wildcard %s" % wildcard)

    pdebug("Applying token rule of length %d" % matchtoklen)
    # Apply the produced function and add that token to subgroups
    if wildcard:
      i += matchtoklen
      wildcard_matches = []
      matchlen = 0
      done = False
      matches = 0
      while not done and c < len(code):  #  and not (wildcard == "?" and matches > 1)
        ctok = matchfun(code, c)
        if ctok:
          pdebug("Found %s subtoken %s at token index %d" % (wildcard, ctok, i-matchtoklen))
          c += ctok.length
          matchlen += ctok.length
          wildcard_matches.append(ctok)
          matches += 1
        else:
          pdebug("Match * exiting")
          done = True
      subgroups.append(Token("*", matchlen, wildcard_matches, tokpat[i-matchtoklen:i]))
      if wildcard == "+" and not len(wildcard_matches):
        pdebug("Wildcard + not satisfied")
        return None
    else:
      ctok = matchfun(code, c)
      i += matchtoklen  # Move down token by exhausted amount
      if ctok:
        pdebug("Found subtoken %s at token index %d" % (ctok, i-matchtoklen))
        c += ctok.length  # Move down token by matched amount
        subgroups.append(ctok)
      else:
        return None
    pdebug("Subtoken search ending with i=%d and char %s" % (i, tokpat[i] if i < len(tokpat) else "\\0"))
  # If the for loop exits, we have exhausted the pattern so it's a match
  tok = Token(tokname, c-code_start, subgroups, tokpat)
  pdebug("Matched token %s" % tok)
  pdebug("EXITING MATCH")
  return tok

def matchbase(code, key="GLOBAL", **kwargs):
  # matches = {}  # TODO add in ability to keep track of intermediates found
  # TODO in the end this will just match to statements
  return match(code, (key, tokens[key]), **kwargs)

# Accepts a string containing the code body
@override_verb
def tokenize(code):
  linenum = 1
  statements = []
  strip_left = match_whitespace(code)
  while strip_left:
    linenum += code[:strip_left.length].count('\n')
    code = code[strip_left.length:]
    strip_left = match_whitespace(code)
  while len(code):
    statement = matchbase(code)
    if statement is None:
      perr("Error in token in line %d" % linenum)
      return None
    else:
      statements.append(statement)
    linenum += code[:statement.length].count('\n')
    code = code[statement.length:]
  return statements
