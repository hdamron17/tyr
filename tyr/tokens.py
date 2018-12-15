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
STRING       = "(\"$*\"|'(`LETTER|`DIGIT| )*')"
BINOP        = "(\\+|\\*|\\-|/|==|!=|<|>|<=|>=)"
UNIOP        = "(\\-)"
WBINOP       = "(or|and)"
WUNIOP       = "(not)"
STERM        = "(`NUMBER|`STRING|`IDENTIFIER)"
PTERM        = "\\( *`TERM* *\\)"
FUNCALL      = "(`IDENTIFIER|`PTERM) *\\( *(`TERM(, *`TERM)* *)?\\)+"
OPERATION    = "(`STERM +`WBINOP +`TERM|`WUNIOP +`TERM|`STERM *`BINOP *`TERM|`UNIOP *`TERM|`FUNCALL)"
TERM         = "(`STERM|`PTERM|`OPERATION)"
DTYPE        = "(bool|int|float|char|string)"
ASSIGNMENT   = "(`DTYPE +)?`IDENTIFIER *(= *`TERM)?; *"
BODY         = "(;|`STATEMENT|{ *`STATEMENT* *})"
IF           = "if *`PTERM *`BODY *"
WHILE        = "while *`PTERM *`BODY *"
# FOR          = "for *\\(`IDENTIFIER +in +`TERM\\) *`BODY *"
STATEMENT    = "(`TERM; *|`ASSIGNMENT|`IF|`WHILE)"
# TODO add in for loops eventually "|`FOR"

###
reserved_chars = "+*?-[]()|`\\$"
wildcards = "+*?"
