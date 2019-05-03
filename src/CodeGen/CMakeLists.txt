### Copyright 2019 Hunter Damron

subdir_include()

set(CODEGEN_LIB "")
FILE(GLOB subs RELATIVE ${CMAKE_CURRENT_SOURCE_DIR} ${CMAKE_CURRENT_SOURCE_DIR}/*)
foreach(sub ${subs})
    if(IS_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/${sub})
        set(CODEGEN_NAME ${PROJECT_NAME}_${sub}codegen)
        list(APPEND CODEGEN_LIB ${CODEGEN_NAME})
        add_subdirectory(${sub})
    endif()
endforeach()
list(APPEND PROJECT_LIBS ${CODEGEN_LIB})
set(PROJECT_LIBS "${PROJECT_LIBS}" PARENT_SCOPE)
