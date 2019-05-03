### Copyright 2019 Hunter Damron

subdir_include()

set(CMDLINE_LIB ${PROJECT_NAME}_cmdline)
list(APPEND PROJECT_LIBS ${CMDLINE_LIB})
set(PROJECT_LIBS "${PROJECT_LIBS}" PARENT_SCOPE)
add_library(${CMDLINE_LIB} OBJECT cmdline.c)
