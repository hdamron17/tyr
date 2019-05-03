/* Sample code using C API */

#include <stdlib.h>
#include <stdio.h>

#include <llvm-c/Core.h>
#include <llvm-c/Analysis.h>

#include "llvm/printers.h"
#include "llvm/writer.h"

int main() {
    LLVMModuleRef mod = LLVMModuleCreateWithName("");

    LLVMValueRef sum = LLVMAddFunction(mod, "", LLVMFunctionType(LLVMInt32Type(), (LLVMTypeRef[]){LLVMInt32Type(), LLVMInt32Type()}, 2, 0));
    LLVMValueRef printf_fn = LLVMAddFunction(mod, "printf", LLVMFunctionType(LLVMVoidType(), (LLVMTypeRef[]){LLVMPointerType(LLVMInt8Type(), 0)}, 1, 1));

    LLVMBasicBlockRef entry = LLVMAppendBasicBlock(sum, "entry");
    LLVMBuilderRef builder = LLVMCreateBuilder();
    LLVMPositionBuilderAtEnd(builder, entry);

    LLVMValueRef tmp = LLVMBuildAdd(builder, LLVMGetParam(sum, 0), LLVMGetParam(sum, 1), "tmp");
    LLVMBuildPrintInt(builder, tmp, printf_fn);
    LLVMBuildRet(builder, tmp);
    LLVMDisposeBuilder(builder);

    LLVMValueRef main = LLVMAddFunction(mod, "main", LLVMFunctionType(LLVMInt32Type(), NULL, 0, 0));
    LLVMBasicBlockRef mainentry = LLVMAppendBasicBlock(main, "entry");
    builder = LLVMCreateBuilder();
    LLVMPositionBuilderAtEnd(builder, mainentry);
    LLVMBuildCall(builder, sum, (LLVMValueRef[]){LLVMConstInt(LLVMInt32Type(), 8, 0), LLVMConstInt(LLVMInt32Type(), 18, 0)}, 2, "");
    LLVMBuildRet(builder, LLVMConstInt(LLVMInt32Type(), 0, 0));

    char *error = NULL;
    LLVMVerifyModule(mod, LLVMAbortProcessAction, &error);
    LLVMDisposeMessage(error);

    emitLLVMCode(mod, "sample.bc");
    emitNativeCode(mod, "sample.o");
}
