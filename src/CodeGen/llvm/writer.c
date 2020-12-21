/* Copyright 2019 Hunter Damron */

#include "llvm/writer.h"
#include "Util/message.h"

bool b_copy_memory_buffer(LLVMMemoryBufferRef membuf, FILE *f) {
    int len = LLVMGetBufferSize(membuf);
    int written = fwrite(LLVMGetBufferStart(membuf), 1, len, f);
    if (written < len) {
        tyr_internal_error("Could not write whole file (only %d of %d)", written, len);
        return false;
    }
    return true;
}

bool b_emit_LLVM_code(LLVMModuleRef mod, FILE *f) {
    LLVMMemoryBufferRef membuf = LLVMWriteBitcodeToMemoryBuffer(mod);
    bool success = b_copy_memory_buffer(membuf, f);
    LLVMDisposeMemoryBuffer(membuf);
    return success;
}

bool b_emit_native_code(LLVMModuleRef mod, FILE *f, LLVMCodeGenFileType type) {
    LLVMInitializeNativeTarget();
    LLVMInitializeNativeAsmPrinter();
    char *triple = LLVMGetDefaultTargetTriple();
    char *error = NULL;

    LLVMTargetRef target;
    if (LLVMGetTargetFromTriple(triple, &target, &error)) {
        tyr_internal_error("Unable to find native target\n  %s", error);
        return false;
    }

    if (!LLVMTargetHasAsmBackend(target)) {
        tyr_internal_warn("Missing target assembly backend");
    }

    LLVMTargetMachineRef targetmachine = LLVMCreateTargetMachine(target, triple,
        "", "", LLVMCodeGenLevelNone, LLVMRelocDefault, LLVMCodeModelDefault);

    LLVMMemoryBufferRef membuf;
    if (LLVMTargetMachineEmitToMemoryBuffer(targetmachine, mod, type, &error, &membuf)) {
        tyr_internal_error("Unable to emit native code\n  %s", error);
        return false;
    }

    b_copy_memory_buffer(membuf, f);

    LLVMDisposeMessage(error);
    LLVMDisposeMessage(triple);
    LLVMDisposeTargetMachine(targetmachine);
    LLVMDisposeMemoryBuffer(membuf);
    return true;
}

bool b_emit_native_asm(LLVMModuleRef mod, FILE *f) {
    return b_emit_native_code(mod, f, LLVMAssemblyFile);
}

bool b_emit_native_obj(LLVMModuleRef mod, FILE *f) {
    return b_emit_native_code(mod, f, LLVMObjectFile);
}

bool b_emit_native_exe(LLVMModuleRef mod, FILE *f) {
    tyr_internal_error("Native exe not implemented");
    return false;
}
