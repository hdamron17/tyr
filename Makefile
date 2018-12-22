# Copyright Hunter Damron 2018

VERSION:=$(firstword $(shell cat VERSIONS.txt))
DIST_FILE:=dist/tyr-$(VERSION).tar.gz

DEPS:=setup.py $(wildcard tyr/*.py test/src/*.tyr)

PY=python3
PIP=pip3

all:  # Do nothing by default

.PHONY: test
test:
	$(PY) setup.py test
	$(MAKE) -C test/

dist: $(DIST_FILE)

$(DIST_FILE): $(DEPS)
	$(PY) setup.py sdist

install:
	$(PY) setup.py install --force

uninstall:
	$(PIP) uninstall tyr

clean:
	find . -name '*.py[co]' -delete
	find . -name '__pycache__' -delete
	$(MAKE) -C test/ clean

distclean: clean
	rm -rf dist/ build/ tyr.egg-info/
