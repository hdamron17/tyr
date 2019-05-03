### Copyright 2019 Hunter Damron

subdir_include()

find_package(flex REQUIRED)
find_package(bison REQUIRED)

FLEX_TARGET(lexer lexer.l ${CMAKE_CURRENT_BINARY_DIR}/lexer.c)
BISON_TARGET(parser parser.y ${CMAKE_CURRENT_BINARY_DIR}/parser.c)
ADD_FLEX_BISON_DEPENDENCY(lexer parser)

set(LEXPARSE_LIB ${PROJECT_NAME}_lexparse)
list(APPEND PROJECT_LIBS ${LEXPARSE_LIB})
set(PROJECT_LIBS "${PROJECT_LIBS}" PARENT_SCOPE)
add_library(${LEXPARSE_LIB} OBJECT lexparse.c ${FLEX_lexer_OUTPUTS} ${BISON_parser_OUTPUTS})
