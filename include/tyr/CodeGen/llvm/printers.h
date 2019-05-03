/* Copyright 2019 Hunter Damron */

#ifndef TYR_LLVM_PRINTERS_H
#define TYR_LLVM_PRINTERS_H

#include <llvm-c/Core.h>

void LLVMBuildPrintInt(LLVMBuilderRef builder, LLVMValueRef val, LLVMValueRef printf_fn);

#endif /* TYR_LLVM_PRINTERS_H */
