/* Copyright 2019 Hunter Damron */

%{
#include <stdio.h>
#include <stdlib.h>
#include "parser.h"
%}
%option noyywrap
ws [ \t]*
digit [0-9]
digits {digit}*
letter [a-zA-Z_]
identifier {letter}({letter}|{digit})*
%%
{ws}     {}
{digits}    { yylval = atoi(yytext); return CONST; }
.|\n      { return *yytext; }
%%
