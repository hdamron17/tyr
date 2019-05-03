/* Copyright 2019 Hunter Damron */

#include "llvm/writer.h"

bool emitLLVMCode(LLVMModuleRef mod, char *fname) {
    LLVMWriteBitcodeToFile(mod, fname);
    return true;
}

bool emitNativeCode(LLVMModuleRef mod, char *fname) {
    // LLVMInitializeAllTargets();
    LLVMInitializeNativeTarget();
    LLVMTargetRef target;
    char *triple = LLVMGetDefaultTargetTriple();
    char *error = NULL;
    if (LLVMGetTargetFromTriple(triple, &target, &error)) {
        fprintf(stderr, "%s\n", error);
        return false;
    }
    LLVMTargetMachineRef targetmachine = LLVMCreateTargetMachine(target, triple, "", "", LLVMCodeGenLevelNone, LLVMRelocDefault, LLVMCodeModelDefault);
    if (LLVMTargetMachineEmitToFile(targetmachine, mod, fname, LLVMObjectFile, &error)) {
        fprintf(stderr, "%s\n", error);
        return false;
    }
    LLVMDisposeMessage(error);
    LLVMDisposeMessage(triple);
    LLVMDisposeTargetMachine(targetmachine);
    return true;
}
