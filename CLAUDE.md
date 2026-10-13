# CLAUDE.md — Economic Fibrillation

Standing instructions for Claude Code in this repository. Read this first, then `docs/open_issues.md`.

## The project

Economic Fibrillation asks whether synchronization of business cycles across economies is a signature of systemic
fragility. Each economy's 2–9 year cycle in log real GDP per capita (Maddison 2023) is treated as a phase oscillator;
the Kuramoto order parameter r(t) measures how aligned they are; global recessions are the Kose–Terrones dates (1975,
1982, 1991, 2009, 2020). Paper 1 (26 economies, 1970–2022) is analysed and its Methods are written. This round:
rebuild everything reproducibly, rerun every Paper 1 test on a wider sample, and build a graph neural network (GNN)
to understand how the coupling between economies works.

## Rules that do not bend

1. **Report everything.** Every test that is run gets reported, nulls included, with the same prominence as the
   results that support the thesis. Never drop a check because it came out badly.
2. **Never tune on the crisis years.** The five recession dates, the 2–9 year band, the 1970–2022 window and the
   test directions are fixed. Any change is a robustness check reported beside the baseline, never a replacement.
3. **Pre-register.** Before running anything on a new sample or with a new model, write the hypotheses, test
   directions, convention and sample into a dated file in `docs/` and commit it. Then run.
4. **Quote floors.** Circular-shift permutation p-values have a floor of 1/53 = 0.019 (p = 0.019 means "no shift did
   better"); 5,000 surrogates give a floor of 0.0002. Say so wherever such a p appears.
5. **State the effective sample.** The pre-crisis lead rests on 2009 and 2020 (n ≈ 2). Never describe it as a
   fifty-year regularity, and never call r(t) a crisis forecast.
6. **No silent changes to Paper 1 numbers.** If a rerun changes a number in `docs/methods.md` or
   `docs/results_registry.md`, record old value, new value and the cause in `docs/decisions.md` and tell Sid.
7. **Two-sided filters cannot support predictive claims.** The band-pass (forward–backward) and the Hilbert transform
   both use future data. Anything framed as a lead, a forecast or a GNN prediction must be re-tested with phases
   built from past data only.

## Reproducibility

- Data come only from the pinned commits in `data/sources.yaml`. `python3 tools/fetch_data.py` fetches and verifies
  checksums; build nothing on unverified files. A new source is added to `sources.yaml` with commit or download date,
  URL and sha256 before any code reads it.
- `python3 tools/rerun_asrun.py` must keep reporting EXACT for every row. It is the regression baseline.
- The as-run scripts in `paper1/scripts/` and `atlas/*.py` are frozen records. Do not edit them; new code goes in
  `src/ef/` and is tested against `tests/golden_paper1.json`.
- Every random draw is seeded and the seed is saved with the result. Every number in a document must trace to a
  results file produced by code in this repository.
- Record decisions, with the reason and the alternative rejected, in `docs/decisions.md`.

## Conventions

- **Phases.** Convention P is the paper's: band-pass and Hilbert transform on the full 1950–2022 series, statistics on
  1970–2022. Several as-run scripts used other conventions (W, N, or a 1962 start; see open issue 1). In the rerun,
  compute every test under P and report W, N and an edge-robust variant as sensitivity.
- **Samples.** S26 = the original 26 (frozen reference). S30 = S26 + China, Brazil, Saudi Arabia and Iran (the
  reported comparison). **S31 = S30 + Russia, the main sample** (pre-registration amendment 3, 13 October 2026). The
  UAE is excluded (its Maddison series misses 1991–1992). Never pool the added economies into the 26's averages in
  the atlas.
- **Data repairs** live in `atlas/data.py` and are listed per economy in `atlas/meta.json` ("fixes"). Do not add,
  remove or change a repair without recording it.
- **Figures.** Every figure has an ID and a category (`docs/FIGURES.md`). Regenerated figures keep their ID and
  folder; update `tools/figure_catalog.py` and rebuild the books with `tools/build_figure_docs.py`. Never overwrite a
  superseded figure. Palette: blue #2a78d6, orange #eb6834, aqua #1baf7a, yellow #eda100, red #e34948, greys
  #898781 and #c3c2b7. Figures use Inter; documents use TeX Gyre Pagella, Inter and Latin Modern Math (xelatex).

