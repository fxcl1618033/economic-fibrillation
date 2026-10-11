# Economic Fibrillation — starter targets. Phase 0 of HANDOFF.md extends these.
.PHONY: data verify asrun golden figures atlas-figs atlas-pdf

data:            ## fetch the pinned sources and verify checksums
	python3 tools/fetch_data.py

verify:          ## verify checksums only
	python3 tools/fetch_data.py --verify

asrun: data      ## rerun every frozen script and compare with the stored results
	python3 tools/rerun_asrun.py

golden:          ## rewrite tests/golden_paper1.json from paper1/results
	python3 tools/make_golden.py

figures:         ## rebuild the category folders, figure books and docs/FIGURES.md
	python3 tools/build_figure_docs.py

atlas-figs:      ## redraw the 35 atlas figures (atlas/fig/*.png) from atlas/panel.csv and friends (~1 min)
	cd atlas && mkdir -p fig && python3 figs.py all

atlas-pdf: atlas-figs  ## rebuild the 39-page atlas PDF (xelatex with TeX Gyre Pagella, Inter, Latin Modern Math)
	mkdir -p build/atlas && cp atlas/*.py atlas/*.csv atlas/*.json build/atlas/ && cp -r atlas/fig build/atlas/
	cd build/atlas && python3 build_tex.py && xelatex -interaction=nonstopmode atlas.tex >/dev/null && xelatex -interaction=nonstopmode atlas.tex >/dev/null
	cp build/atlas/atlas.pdf "atlas/The 26 Economies 1970-2022 - Atlas.pdf"
