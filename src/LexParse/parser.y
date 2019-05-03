/* Copyright 2019 Hunter Damron */

%{
#include <stdio.h>
extern int yylex(void);
void yyerror(char*);
int yyparse(void);
%}

%token CONST;

%%

eval
    : eval line
    | /* empty */
    ;

line
    : expr '\n'            { printf("%d\n", $1); }
    ;

expr
    : pmterm
    | pmterm '+' subexpr  { $$ = $1 + $3; }
    | pmterm '-' subexpr  { $$ = $1 - $3; }
    ;

pmterm
    : term
    | '+' term            { $$ = $2; }
    | '-' term            { $$ = -$2; }
    ;

subexpr
    : term
    | subexpr '+' term    { $$ = $1 + $3; }
    | subexpr '-' term    { $$ = $1 - $3; }
    ;

term
    : factor
    | term '*' factor     { $$ = $1 * $3; }
    | term '/' factor     { $$ = $1 / $3; }
    | term '%' factor     { $$ = $1 % $3; }
    ;

factor
    : CONST               { $$ = $1; }
    | '(' expr ')'        { $$ = $2; }
    ;

%%

void yyerror(char *s)
{
    fprintf(stderr, "%s\n", s);
}
