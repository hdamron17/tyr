/* Copyright 2019 Hunter Damron */

%{
#include <stdio.h>
#include "Util/message.h"
extern int yylex(void);
void yyerror(char*);
int yyparse(void);
%}

%token CONSTANT;

%%

eval
    : eval line
    | /* empty */
    ;

newline
    : '\n'  { tyr_lineno++; }
    ;

line
    : expr newline  { printf("%d\n", $1); }
    | newline
    ;

expr
    : pmterm
    | pmterm '+' subexpr  { $$ = $1 + $3; }
    | pmterm '-' subexpr  { $$ = $1 - $3; }
    ;

pmterm
    : term
    | '+' term  { $$ = $2; }
    | '-' term  { $$ = -$2; }
    ;

subexpr
    : term
    | subexpr '+' term  { $$ = $1 + $3; }
    | subexpr '-' term  { $$ = $1 - $3; }
    ;

term
    : factor
    | term '*' factor  { $$ = $1 * $3; }
    | term '/' factor  { $$ = $1 / $3; }
    | term '%' factor  { $$ = $1 % $3; }
    ;

factor
    : CONSTANT  { $$ = $1; }
    | '(' expr ')'  { $$ = $2; }
    ;

%%

void yyerror(char *s)
{
    fprintf(stderr, "%s\n", s);
}
