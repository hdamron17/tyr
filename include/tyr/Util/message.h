/* Copyright 2019 Hunter Damron */

#ifndef TYR_MESSAGE_H
#define TYR_MESSAGE_H

#include <string.h>
#include <stdio.h>

/*
 * Verbosity Levels
 * 0 -- Absolute silence
 * 1 -- Internal errors and warnings
 * 2 -- Errors and warnings
 * 3 -- Messages (default)
 * 4 -- Debug messages
 * 5 -- Internal debug messages
 */

#ifndef VERBOSITY
#define VERBOSITY 3
#endif

char *tyr_file;
int tyr_lineno;

#define _tyr_print(stream, pre, post, file, lineno, ...) \
    { fprintf(stream, "%s [%s:%d] ", pre, \
    (strrchr(file, '/') ? strrchr(file, '/')+1 : file), lineno); \
    fprintf(stream, __VA_ARGS__); fprintf(stream, "\n%s", post); }

#define tyr_internal_print(stream, pre, post, ...) \
    _tyr_print(stream, pre, post, __FILE__, __LINE__, __VA_ARGS__);
#define tyr_print(stream, pre, post, ...) \
    _tyr_print(stream, pre, post, tyr_file, tyr_lineno, __VA_ARGS__);

#define C_RED "\033[0;31m"
#define C_YELLOW "\033[0;33m"
#define C_RESET "\033[0m"

#if VERBOSITY >= 1
#define tyr_internal_error(...) tyr_internal_print(stderr, C_RED "INTERNAL ERROR", C_RESET, __VA_ARGS__);
#define tyr_internal_warn(...) tyr_internal_print(stderr, C_YELLOW "INTERNAL WARNING", C_RESET, __VA_ARGS__);
#else
#define tyr_internal_error(...)
#define tyr_internal_warn(...)
#endif

#if VERBOSITY >= 2
#define tyr_error(...) tyr_print(stderr, C_RED "ERROR", C_RESET, __VA_ARGS__);
#define tyr_warn(...) tyr_print(stderr, C_YELLOW "WARNING", C_RESET, __VA_ARGS__);
#else
#define tyr_error(...)
#define tyr_warn(...)
#endif

#if VERBOSITY >= 3
#define tyr_info(...) tyr_print(stderr, "INFO", "", __VA_ARGS__);
#else
#define tyr_info(...)
#endif

#if VERBOSITY >= 4
#define tyr_debug(...) tyr_print(stderr, "DEBUG", "", __VA_ARGS__);
#else
#define tyr_debug(...)
#endif

#if VERBOSITY >= 5
#define tyr_verbose(...) tyr_internal_print(stderr, "DEBUG", "", __VA_ARGS__);
#else
#define tyr_verbose(...)
#endif

#endif /* TYR_MESSAGE_H */
