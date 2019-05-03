/* Copyright 2019 Hunter Damron */

#include "llvm/printers.h"

void LLVMBuildPrintInt(LLVMBuilderRef builder, LLVMValueRef val, LLVMValueRef printf_fn) {
    LLVMValueRef str = LLVMBuildGlobalStringPtr(builder, "%d\n", "");
    LLVMBuildCall(builder, printf_fn, (LLVMValueRef[]){str, val}, 2, "");
}
