# Economic Fibrillation — one-command rebuild (HANDOFF.md Phases 0–1).
#   make all      environment, pinned data, as-run reproduction check and tests (needs no LaTeX)
#   make help     list the targets
# Every target runs the project's own Python (.venv, Python 3.13, versions from requirements.lock).

PY     := $(CURDIR)/.venv/bin/python
STAMP  := .venv/.installed
export PYTHONPATH := $(CURDIR)/src
export MPLBACKEND := Agg

.PHONY: all help env data fetch verify asrun test golden figures atlas-figs atlas-pdf clean

all: data asrun test           ## environment, data, as-run check and tests

help:                          ## list the targets
	@grep -E '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | sed 's/:.*## /\t/' | expand -t 16

env: $(STAMP)                  ## build .venv from requirements.lock (uv if present, else python3.13 -m venv)
$(STAMP): requirements.lock
	@if command -v uv >/dev/null 2>&1; then \
		uv venv -q --clear --python 3.13 .venv && uv pip install -q --python $(PY) -r requirements.lock; \
	else \
		python3.13 -m venv --clear .venv && $(PY) -m pip install -q -r requirements.lock; \
	fi
	@touch $@

fetch: $(STAMP)                ## fetch the pinned sources and verify their checksums
	$(PY) tools/fetch_data.py

verify: $(STAMP)               ## verify checksums of the pinned sources only
	$(PY) tools/fetch_data.py --verify

data: fetch                    ## fetch -> verify -> build -> validate (build and validate arrive in Phase 1)

asrun: fetch                   ## rerun every frozen script; EXACT or MATCH everywhere, then the reported-precision check
	$(PY) tools/rerun_asrun.py
	$(PY) tools/check_reported_precision.py > /dev/null && echo "reported-precision check: build/asrun/PRECISION.md"

test: $(STAMP)                 ## run the test suite
	$(PY) -m pytest -q

golden: $(STAMP)               ## rewrite tests/golden_paper1.json from paper1/results
	$(PY) tools/make_golden.py

figures: $(STAMP)              ## rebuild the category folders, figure books and docs/FIGURES.md (needs xelatex and pdftoppm)
	@command -v xelatex >/dev/null && command -v pdftoppm >/dev/null || { echo "make figures needs xelatex (TeX Live or MacTeX) and pdftoppm (poppler)"; exit 1; }
	$(PY) tools/build_figure_docs.py

atlas-figs: $(STAMP)           ## redraw the 35 atlas figures (atlas/fig/*.png) from atlas/panel.csv and friends (~1 min)
	cd atlas && mkdir -p fig && $(PY) figs.py all

atlas-pdf: atlas-figs          ## rebuild the 39-page atlas PDF (xelatex with TeX Gyre Pagella, Inter, Latin Modern Math)
	@command -v xelatex >/dev/null || { echo "make atlas-pdf needs xelatex (TeX Live or MacTeX)"; exit 1; }
	mkdir -p build/atlas && cp atlas/*.py atlas/*.csv atlas/*.json build/atlas/ && cp -r atlas/fig build/atlas/
	cd build/atlas && $(PY) build_tex.py && xelatex -interaction=nonstopmode atlas.tex >/dev/null && xelatex -interaction=nonstopmode atlas.tex >/dev/null
	cp build/atlas/atlas.pdf "atlas/The 26 Economies 1970-2022 - Atlas.pdf"

clean:                         ## remove build/ (keeps data/raw and .venv)
	rm -rf build
