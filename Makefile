# Economic Fibrillation — one-command rebuild (HANDOFF.md Phases 0–1).
#   make all      environment, pinned data, as-run reproduction check and tests (needs no LaTeX)
#   make help     list the targets
# Every target runs the project's own Python (.venv, Python 3.13, versions from requirements.lock).

PY     := $(CURDIR)/.venv/bin/python
STAMP  := .venv/.installed
export PYTHONPATH := $(CURDIR)/src
export MPLBACKEND := Agg

.PHONY: all help env data fetch verify build-data validate asrun test paper1 phase3 phase3-s31 followup gnn-g0 gnn-g1 golden figures atlas-figs atlas-pdf clean

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

data: fetch build-data validate  ## fetch -> verify -> build -> validate, from nothing

build-data: fetch              ## build panel26, the atlas files and the Maddison panels into build/data; check them
	$(PY) -m ef.data.build --quiet

validate: build-data           ## validation report per economy: build/data/VALIDATION.md and docs/data_validation.md
	$(PY) -m ef.data.validate

asrun: fetch                   ## rerun every frozen script; EXACT or MATCH everywhere, then the reported-precision check
	$(PY) tools/rerun_asrun.py
	$(PY) tools/check_reported_precision.py > /dev/null && echo "reported-precision check: build/asrun/PRECISION.md"

test: $(STAMP)                 ## run the test suite (includes the golden numbers, about 25 s)
	$(PY) -m pytest -q

paper1: build-data             ## every Paper 1 test, as run, on S26; compare with the golden numbers (build/paper1/GOLDEN.md)
	$(PY) -m ef.paper1 --golden

phase3: build-data             ## the pre-registered rerun on S26 and S30 with every variant -> results/, results/COMPARISON.md
	$(PY) -m ef.phase3

phase3-s31: build-data         ## the pre-registered battery on S31 = S30 + Russia (amendment 3) -> results/S31*, COMPARISON.md
	$(PY) -m ef.phase3 --config configs/runs/phase3_s31.yaml

gnn-g0: build-data             ## GNN stage G0: yearly graphs on S31 -> build/gnn/g0, gnn/G0_data_card.md, gnn/G0_missing_data.md
	$(PY) -m ef.gnn.report

gnn-g1: gnn-g0                 ## GNN stage G1: calibrate the simulator, run every Paper 1 test on 8,000 simulated worlds (~80 min) -> gnn/G1/, gnn/G1_report.md
	$(PY) -m ef.gnn.g1 calibrate
	$(PY) -m ef.gnn.g1 run
	$(PY) -m ef.gnn.g1 checks
	$(PY) -m ef.gnn.g1 report

followup: build-data           ## follow-up checks Sid asked for after Phase 3 (not pre-registered) -> results/FOLLOWUP.md
	$(PY) -m ef.followup

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
