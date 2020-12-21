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

bool b_emit_LLVM_code(LLVMModuleRef mod, FILE *f);
bool b_emit_native_asm(LLVMModuleRef mod, FILE *f);
bool b_emit_native_obj(LLVMModuleRef mod, FILE *f);
bool b_emit_native_exe(LLVMModuleRef mod, FILE *f);

#endif /* TYR_LLVM_WRITER_H */
