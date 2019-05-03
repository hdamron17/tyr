/* Copyright 2019 Hunter Damron */

#ifndef TYR_LLVM_WRITER_H
#define TYR_LLVM_WRITER_H

#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include <llvm-c/Core.h>
#include <llvm-c/BitWriter.h>
#include <llvm-c/Target.h>
#include <llvm-c/TargetMachine.h>

bool emitLLVMCode(LLVMModuleRef mod, char *fname);
bool emitNativeCode(LLVMModuleRef mod, char *fname);

#endif /* TYR_LLVM_WRITER_H */
