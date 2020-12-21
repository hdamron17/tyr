/* Copyright 2019 Hunter Damron */

#ifndef TYR_LEXPARSE_H
#define TYR_LEXPARSE_H

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "AST/ast.h"
#include "Util/message.h"

AST_NODE* build_AST_str(char* str);
AST_NODE* build_AST_stdin();
AST_NODE* build_AST(FILE* stream);

#endif /* TYR_LEXPARSE_H */
