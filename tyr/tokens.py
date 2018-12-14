# Copyright Hunter Damron 2018

# Tokens follow very simple rules:
#  * [...]      Means a choice of characters
#  * [x-y]      Inserts the range from x to y into the char group
#  * (...|...)  Chooses between two sub patterns
#  * x*         Chooses as many as possible of x
#  * x+         Chooses at least 1 and as many as possible of x
#  * \x         Chooses the literal of whatever character follows
#  * ' '        The empty space chooses any whitespace
#  * `key       Replaced with the previously defined rule key
##  * $          Chooses literally everything possible on a line
##  * !          Chooses literally everything possible across lines

LETTER      = "[a-zA-Z_]"
DIGIT       = "[0-9]"
DIGITS      = "`DIGIT+"
IDENTIFIER  = "`LETTER(`LETTER|`DIGIT)*"
# COMMENT     = "(#$|>#>!<#<)"  # Comments are weird so we'll wait a bit to figure out how to play nicely with strings and things
STRING      = "(\"(`LETTER|`DIGIT| )*\"|'(`LETTER|`DIGIT| )*')"
BINOP       = "(\\+|\\*|\\-|/)"
UNIOP       = "(\\-)"
WBINOP      = "(or|and)"
WUNIOP      = "(not)"
STERM       = "(`DIGITS|`STRING|`IDENTIFIER)"
TERM        = "(`STERM|\\( *`TERM* *\\)|`STERM +`WBINOP +`TERM|`WUNIOP +`TERM" \
            + "|`STERM *`BINOP *`TERM|`UNIOP *`TERM)"
STATEMENT   = "`TERM. *"
