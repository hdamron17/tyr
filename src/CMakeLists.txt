### Copyright 2019 Hunter Damron

set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

set(${PROJECT_NAME}_INCLUDE_BASE ${CMAKE_SOURCE_DIR}/include/${PROJECT_NAME})
set(${PROJECT_NAME}_SOURCE_BASE ${CMAKE_CURRENT_SOURCE_DIR})
include_directories(${${PROJECT_NAME}_INCLUDE_BASE})

macro(subdir_include)
    file(RELATIVE_PATH SUBDIR ${${PROJECT_NAME}_SOURCE_BASE} ${CMAKE_CURRENT_SOURCE_DIR})
    include_directories(${${PROJECT_NAME}_INCLUDE_BASE}/${SUBDIR})
endmacro()

set(PROJECT_LIBS "")

add_subdirectory(CmdLine)
add_subdirectory(AST)
add_subdirectory(LexParse)
add_subdirectory(CodeGen)
add_subdirectory(Util)

set(PROJECT_LIB ${PROJECT_NAME})
string(REGEX REPLACE "([^ ;]+)" "$<TARGET_OBJECTS:\\1>" PROJECT_LIBS_OBJ "${PROJECT_LIBS}")
add_library(${PROJECT_LIB} STATIC ${PROJECT_LIBS_OBJ})

set(PROJECT_MAIN ${PROJECT_NAME}c)
add_executable(${PROJECT_MAIN} compiler.c)
target_link_libraries(${PROJECT_MAIN} ${PROJECT_LIB})
