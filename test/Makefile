TYRC=../tyrc
SRC=src
BUILD=build
BIN=bin

SOURCES=$(wildcard $(SRC)/*.tyr)
BINARIES=$(patsubst $(SRC)/%.tyr, $(BIN)/%, $(SOURCES))

test: $(BINARIES)
	./test.sh

$(BUILD)/%.ll: $(SRC)/%.tyr | $(BUILD)
	@mkdir -p $(dir $@)
	$(TYRC) $< -o $@

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

