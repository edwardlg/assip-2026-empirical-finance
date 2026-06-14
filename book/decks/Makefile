# Makefile — render Quarto deck sources (.qmd) to PowerPoint (.pptx)
#
# Usage:
#   make            # render every .qmd in this directory to .pptx
#   make all        # same as above
#   make week-01.pptx
#   make list       # list discoverable decks
#   make clean      # remove generated .pptx and _files/ caches
#
# Conventions:
#   - Files beginning with "_" (e.g. _template.qmd) are treated as partials
#     and are NOT rendered. To render the template for a smoke test:
#       make template
#   - Output .pptx files are written next to their .qmd source.
#   - Speaker notes inside ::: notes ::: fences become PPTX speaker notes
#     and are later piped to TTS for narration.

QUARTO   ?= quarto
DECK_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

# Discover all deck sources, then drop anything that starts with "_".
ALL_QMD     := $(wildcard *.qmd)
DECK_QMD    := $(filter-out _%.qmd,$(ALL_QMD))
DECK_PPTX   := $(DECK_QMD:.qmd=.pptx)

.PHONY: all list clean template help

all: $(DECK_PPTX)
	@echo "Rendered $(words $(DECK_PPTX)) deck(s) to .pptx in $(DECK_DIR)"

help:
	@echo "Targets:"
	@echo "  all        render every non-underscore .qmd to .pptx (default)"
	@echo "  list       list discoverable deck sources"
	@echo "  template   render _template.qmd to _template.pptx (smoke test)"
	@echo "  clean      remove generated .pptx and Quarto _files/ caches"
	@echo "  <name>.pptx  render one specific deck"

list:
	@echo "Deck sources in $(DECK_DIR):"
	@for f in $(DECK_QMD); do echo "  $$f"; done
	@echo "Partials (skipped):"
	@for f in $(filter _%.qmd,$(ALL_QMD)); do echo "  $$f"; done

# Pattern rule: any deck.pptx is built from its sibling deck.qmd.
%.pptx: %.qmd
	$(QUARTO) render $< --to pptx

# Explicit target for rendering the template as a smoke test.
template: _template.pptx

_template.pptx: _template.qmd
	$(QUARTO) render $< --to pptx

clean:
	@rm -f $(DECK_PPTX) _template.pptx
	@rm -rf *_files .quarto
	@echo "Cleaned generated decks and caches in $(DECK_DIR)"
