# Copyright Hunter Damron 2018

# Tokens follow very simple rules:
#  * [...]      Means a choice of characters
#  * [x-y]      Inserts the range from x to y into the char group
#               Note: escape sequences are not currently accepted in char groups
#  * (...|...)  Chooses between two sub patterns
#  * x*         Chooses as many as possible of x
#  * x+         Chooses at least 1 and as many as possible of x
#  * x?         Chooses either 0 or 1 of x
#  * \x         Chooses the literal of whatever character follows
#  * ' '        The empty space chooses any whitespace
#  * `key       Replaced with the previously defined rule key
#  * $          Chooses literally anything (not greedy within a single command)

### Lexer Tokens (must start with a capital)

LETTER       = "[a-zA-Z_]"
DIGIT        = "[0-9]"
DIGITS       = "`DIGIT+"
NUMBER       = "(`DIGITS|`DIGITS.`DIGITS)"
SIDENTIFIER  = "`LETTER(`LETTER|`DIGIT)*"
IDENTIFIER   = "(`SIDENTIFIER|`SIDENTIFIER.`IDENTIFIER)"
COMMENT      = "(#$*\n|>#>$*<#<)"
STRING       = "\"$*\""
CHAR         = "'($|\\[n])'"
BINOP        = "(\\+|\\*|\\-|/|==|!=|<|>|<=|>=)"
UNIOP        = "(\\-)"
WBINOP       = "(or|and)"
WUNIOP       = "(not)"
BOOL         = "(true|false)"
LTERM        = "(`NUMBER|`CHAR|`STRING|`IDENTIFIER|`BOOL|`FUNCALL|`PTERM)"
PTERM        = "\\( *`TERM* *\\)"
FUNCALL      = "`IDENTIFIER *(\\( *(`TERM(, *`TERM)* *)?\\))+"
# Maybe eventually I'll be good enough for first class functions "(`IDENTIFIER|`PTERM)"
OPERATION    = "(`LTERM +`WBINOP +`TERM|`WUNIOP +`TERM|`LTERM *`BINOP *`TERM|`UNIOP *`TERM)"
TERM         = "(`LTERM|`PTERM|`OPERATION)"
DTYPE        = "(void|bool|int|float|char|string)"
DECLARATION  = "`DTYPE +`IDENTIFIER"
ASSIGNMENT   = "(`DECLARATION|`IDENTIFIER) *(= *`TERM *)?; *"
STATEMENT    = "(; *|`TERM; *|`ASSIGNMENT|`SCOPE)"
BODY         = "(`STATEMENT|`SCOPE) *"
IF           = "if *`PTERM *`BODY"
WHILE        = "while *`PTERM *`BODY"
FOR          = "for *\\(`IDENTIFIER +in +`TERM\\) *`BODY"
SCOPE        = "({ *`STATEMENT* *}|`IF|`WHILE)"
# TODO add in for loops eventually "|`FOR"
FUNDEF       = "`DECLARATION *\\( *(`DECLARATION(, *`DECLARATION)* *)?\\) *`BODY"
CONSTANT     = "const `DECLARATION *= *`TERM; *"
GLOBAL       = "(`FUNDEF|`CONSTANT)"

###
reserved_chars = "+*?-[]()|`\\$"
wildcards = "+*?"
