/* Copyright 2019 Hunter Damron */

#ifndef TYR_AST_H
#define TYR_AST_H

#include <stdbool.h>

typedef enum {VOID, BOOL, INT, REAL} DTYPE;

typedef enum {CONST, VAR, OP} AST_TYPE;

typedef struct ast_node AST_NODE;

typedef struct {
    DTYPE dtype;
    union {
        bool bool_val;
        int int_val;
        float real_val;
    };
} CONST_NODE;

typedef struct {
    // TODO
} VAR_NODE;

typedef struct {
    // TODO
} OP_NODE;

struct ast_node {
    char *name;
    bool resolved;
    AST_TYPE tag;
    union {
        CONST_NODE const_node;
        VAR_NODE var_node;
        OP_NODE op_node;
    };
};

#endif /* TYR_AST_H */
