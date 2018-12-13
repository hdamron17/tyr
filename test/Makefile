TYRROOT=..
TYRC=$(TYRROOT)/tyrc
TYRFLAGS=-d
SRC=src
BUILD=build
BIN=bin

DEPS=$(TYRC) $(wildcard $(TYRROOT)/tyr/*.py)

SOURCES=$(wildcard $(SRC)/*.tyr)
NAMES=$(patsubst $(SRC)/%.tyr, %, $(SOURCES))

.PHONY: test
test: $(NAMES)
#	./test.sh  # TODO use test script once compiler works

.PHONY: $(NAMES)
$(NAMES): %: $(BUILD)/%.ll  # TODO build binaries once compiler works

$(BUILD)/%.ll: $(SRC)/%.tyr $(DEPS) | $(BUILD)
	@mkdir -p $(dir $@)
	$(TYRC) $(TYRFLAGS) $< -o $@

$(BUILD)/%.s: $(BUILD)/%.ll | $(BUILD)
	@mkdir -p $(dir $@)
	llc $<

$(BIN)/%: $(BUILD)/%.s | $(BIN)
	@mkdir -p $(dir $@)
	gcc $< -o $@

$(BIN) $(BUILD):
	mkdir -p $@

clean:
	rm -rf $(BUILD) $(BIN)

