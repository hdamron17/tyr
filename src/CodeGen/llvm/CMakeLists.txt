### Copyright 2019 Hunter Damron

find_package(LLVM REQUIRED CONFIG)

execute_process(COMMAND ${LLVM_TOOLS_BINARY_DIR}/llvm-config --targets-built OUTPUT_VARIABLE LLVM_TARGETS OUTPUT_STRIP_TRAILING_WHITESPACE)
string (REPLACE " " ";" LLVM_TARGETS "${LLVM_TARGETS}")
list(TRANSFORM LLVM_TARGETS APPEND codegen)

add_definitions(${LLVM_DEFINITIONS})
llvm_map_components_to_libnames(LLVM_LIBRARIES core analysis bitwriter target native ${LLVM_TARGETS})
include_directories(PUBLIC ${LLVM_INCLUDE_DIRS})

add_executable(sample_gen sample.c printers.c writer.c)
target_link_libraries(sample_gen PUBLIC ${LLVM_LIBRARIES})
set_target_properties(sample_gen PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/test)

add_library(${CODEGEN_NAME} OBJECT codegen.c printers.c writer.c)
target_link_libraries(${CODEGEN_NAME} PUBLIC ${LLVM_LIBRARIES})
