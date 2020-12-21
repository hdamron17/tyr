/* Copyright 2019 Hunter Damron */

#ifndef TYR_CODEGEN_H
#define TYR_CODEGEN_H

#include <stdio.h>
#include <stdbool.h>

void b_setup();
bool b_write(FILE *stream, char *fname);
inline bool b_write_stdout() { return b_write(stdout, ""); }

#endif /* TYR_CODEGEN_H */
