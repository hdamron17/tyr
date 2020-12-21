/* Copyright 2019 Hunter Damron */

#include "LexParse/lexparse.h"

extern int yyparse(void);

AST_NODE* build_AST_str(char *str) {
    FILE *stream = fmemopen(str, strlen(str), "r");
    AST_NODE *ret = build_AST(stream);
    fclose(stream);
    return ret;
}

AST_NODE* build_AST_stdin() {
    return build_AST(stdin);
}

AST_NODE* build_AST(FILE *stream) {
    tyr_file = "";   // TODO move this
    tyr_lineno = 1;  // ^^^^
    extern FILE *yyin;
    yyin = stream;
    yyparse();
    return NULL;  // TODO actually do this
}
