### Copyright 2019 Hunter Damron

subdir_include()

set(CODEGEN_LIBS "")
FILE(GLOB subs RELATIVE ${CMAKE_CURRENT_SOURCE_DIR} ${CMAKE_CURRENT_SOURCE_DIR}/*)

set(CODEGEN_LIB "")
foreach(sub ${subs})
    if(IS_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/${sub})
        set(CODEGEN_NAME ${PROJECT_NAME}_${sub}codegen)
        list(APPEND CODEGEN_LIBS ${CODEGEN_NAME})
        add_subdirectory(${sub})
        if(${sub} STREQUAL ${BACKEND})
            set(CODEGEN_LIB ${CODEGEN_NAME})
        endif()
    endif()
endforeach()

if (CODEGEN_LIB STREQUAL "")
    message(SEND_ERROR "Unavailable backend configuration ${BACKEND}")
else()
    list(APPEND PROJECT_LIBS ${CODEGEN_LIB})
    set(PROJECT_LIBS "${PROJECT_LIBS}" PARENT_SCOPE)
endif()

set(CODEGEN_LIBS "${CODEGEN_LIBS}" PARENT_SCOPE)
