# Copyright Hunter Damron 2018

TYRROOT=..
TYRC=$(TYRROOT)/tyrc
TYRFLAGS=-d
SRC=src
BUILD=build
BIN=bin

DEPS:=$(TYRC) $(wildcard $(TYRROOT)/tyr/*.py)

SOURCES:=$(wildcard $(SRC)/*.tyr)
NAMES:=$(patsubst $(SRC)/%.tyr, %, $(SOURCES))

LLVM_SOURCES:=$(wildcard $(SRC)/*.ll)
LLVM_NAMES:=$(patsubst $(SRC)/%.ll, %, $(LLVM_SOURCES))

.PHONY: test
test: $(NAMES) $(LLVM_NAMES)
#	./test.sh  # TODO use test script once compiler works

.PHONY: $(NAMES) $(LLVM_NAMES)
$(NAMES): %: $(BUILD)/%.ll  # TODO build binaries once compiler works
$(LLVM_NAMES): %: $(BIN)/%

$(BUILD)/%.ll: $(SRC)/%.ll | $(BUILD)
	cp $< $@
	
$(BUILD)/%.ll: $(SRC)/%.tyr $(DEPS) | $(BUILD)
	$(TYRC) $(TYRFLAGS) $< -o $@

$(BUILD)/%.s: $(BUILD)/%.ll | $(BUILD)
	llc $<

$(BIN)/%: $(BUILD)/%.s | $(BIN)
	gcc $< -o $@

$(BIN) $(BUILD):
	mkdir -p $@

clean:
	rm -rf $(BUILD) $(BIN)
