# Copyright Hunter Damron 2018

# Tokens follow very simple rules:
#  * [...]      Means a choice of characters
#  * [x-y]      Inserts the range from x to y into the char group
#  * (...|...)  Chooses between two sub patterns
#  * x*         Chooses as many as possible of x
#  * x+         Chooses at least 1 and as many as possible of x
#  * $          Chooses literally everything possible on a line
#  * !          Chooses literally everything possible across lines
#  * \x         Chooses the literal of whatever character follows
#  * ' '        The empty space chooses any whitespace
#  * `key       Replaced with the previously defined rule key

LETTER      = "[a-zA-Z_]"
DIGIT       = "[0-9]"
DIGITS      = "`DIGIT+"
IDENTIFIER  = "`LETTER(`LETTER|`DIGIT)*"
COMMENT     = "(#$|>#>!<#<)"
STRING      = "(\"`LETTER*\"|'`LETTER*')"
BINOP       = "(\\-|/)"
            # TODO add back '\\+|\\*|' once escapes work
UNIOP       = "(\\-)"
WBINOP      = "(or|and)"
WUNIOP      = "(not)"
TERM        = "(`DIGITS|`STRING|`IDENTIFIER|`TERM *`BINOP *`TERM|`UNIOP *`TERM" \
            + "|`TERM +`WBINOP +`TERM|`WUNIOP +`TERM)"
            # TODO add back '\\( *`TERM* *\\)|' once escapes work
TERM        = "(`DIGITS|`WBINOP +`TERM `TERM)"
STATEMENT   = "`TERM. *"
