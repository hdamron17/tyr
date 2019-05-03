/* Copyright 2019 Hunter Damron */

#include "cmdline.h"

typedef struct {
    char *ifname;
    char *ofname;
} TYR_OPTS;
TYR_OPTS DEFAULT_OPTS = {NULL, NULL};

void rmTYR_OPTS(TYR_OPTS *opt) {
    if (opt->ifname)
        free(opt->ifname);
    if (opt->ofname)
        free(opt->ofname);
}
