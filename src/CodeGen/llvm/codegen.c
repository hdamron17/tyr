/* Copyright 2019 Hunter Damron */

#include "codegen.h"
#include "llvm/printers.h"
#include "llvm/writer.h"
#include <string.h>

LLVMModuleRef mod;

void b_setup() {
    mod = LLVMModuleCreateWithName("");
}

bool endswith(char *str, char *end) {
    size_t len = strlen(str);
    size_t endlen = strlen(end);
    if (len < endlen)
        return false;
    return strcmp(str + len - endlen, end) == 0;
}

bool b_write(FILE *stream, char *fname) {
    if (endswith(fname, ".bc") || !strlen(fname)) {
        return b_emit_LLVM_code(mod, stream);
    } else if (endswith(fname, ".s")) {
        return b_emit_native_asm(mod, stream);
    } else if (endswith(fname, ".o")) {
        return b_emit_native_obj(mod, stream);
    } else {
        return b_emit_native_exe(mod, stream);
    }
}
