# Economic Fibrillation

Is the synchronization of business cycles across economies a signature of systemic fragility? Each economy's 2–9 year
cycle in real GDP per capita (Maddison Project Database 2023) is treated as a phase oscillator, and the Kuramoto order
parameter r(t) measures how aligned 31 economies are from 1970 to 2022. Paper 1 relates that alignment to the five
global recessions (1975, 1982, 1991, 2009 and 2020) and asks how much of a recession's extra variance in world output
comes from economies moving together rather than from bigger swings in each one.

This repository holds everything Paper 1 reports: the code, the pinned data manifests, the pre-registrations, every
results file, the figures and the manuscript.

**Paper.** Shinde, S. (2026). *Economic Fibrillation: Business-Cycle Synchronization and the Loss of Diversification in
Global Recessions.* SSRN: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7629818

**Version.** The tag `paper1-complete-v1.3` is the version the paper describes (https://github.com/fxcl1618033/economic-fibrillation/tree/paper1-complete-v1.3).

Author: Siddhant Shinde.

## Reproduce Paper 1

You need macOS or Linux, Python 3.13, `git` and `make` (and, only for the PDF, pandoc and a TeX distribution).

```bash
make reproduce
```

This builds the Python environment from `requirements.lock`, fetches the pinned data and checks their sha256
(`data/sources.yaml`), reruns every frozen as-run script, regenerates every result Paper 1 reports (the pre-registered
battery on S26, S30 and S31, the edge-matched nulls, the follow-up checks, the simulated worlds of G1 and G1b, the DTT
reproduction, the figures and the manuscript text), compares every regenerated file with the committed one and runs the
test suite. It takes several hours; the comparison is written to `build/REPRODUCE.md`.

For a quick check (minutes): `make all` fetches and verifies the data, reruns the as-run scripts and runs the tests,
which recompute the headline numbers (`tests/golden_paper1.json`) and check that the manuscript renders from the stored
results. `make help` lists every target; `make paper1-pdf` builds the PDF.

What "reproduces" means is in `src/ef/repro.py`: EXACT is every number within 1e-9. Outputs built from the Global Macro
Database may instead MATCH to floating-point rounding with no p-value changed, because its files are single precision
and logarithms round differently on different chips (on Apple silicon they MATCH; on Linux x86 they are EXACT).

## Pre-registrations and decisions

Every test was written down and committed before it was run.

| File | What it fixes |
|---|---|
| `docs/preregistration_S30.md` | The rerun of every Paper 1 test on the wider sample, with amendments 1–4 (Russia and the main sample S31; edge-matched nulls) |
| `docs/preregistration_G1.md` | The simulated worlds with known coupling, and the size and power of Paper 1's tests |
| `docs/preregistration_G1b_dtt.md` | The synchrony-driven escape layer (the DTT box), with its amendment 1 |
| `docs/decisions.md` | Every decision, with the reason and the alternative rejected |
| `docs/methods.md` | The Methods (generated from the manuscript templates) |
| `docs/results_registry.md` | Every number Paper 1 reports and where it comes from |

The commit history is filtered for this public release (see "Data" below). Commit hashes cited in documents written
before the release are translated by `HASH_MAP.md`. Commit dates and order are unchanged.

## Where to look

| You want | Open |
|---|---|
| The paper | `paper1/manuscript/paper1.pdf` (LaTeX source in `paper1/manuscript/latex/`) |
| Every figure, by category | `figures/compiled/EF_Figures_00_Index.pdf`, then books 01–07 |
| What is wrong or unfinished | `docs/open_issues.md` |
| Proof that it reproduces | `docs/reproduction_check.md` (Linux), `docs/reproduction_check_mac.md` (Mac), `docs/golden_check.md` |
| The library | `src/ef/` (filters, phases, order parameter, nulls, crisis tests, decomposition, network, tipping, data build) |
| Simulated worlds (G0, G1, G1b) | `gnn/` |

`CLAUDE.md` holds the standing rules used when working with Claude Code (see the AI disclosure in the manuscript).
Some documents refer to planning files that are not part of this release.

## Data

Every source is pinned to a repository commit or a dated download, with checksums, in `data/sources.yaml`;
`python3 tools/fetch_data.py` fetches and verifies them. The sources are the Maddison Project Database 2023, the Global
Macro Database (2026 release), Penn World Table 10.01, the IMF's trade by partner (IMTS), the BIS Locational Banking
Statistics, EIA and BP oil data, and World Bank GDP. Licences, attribution and what is or is not copied into this
repository are in `DATA_LICENSES.md`. The Global Macro Database's terms do not allow re-hosting, so its series
(`atlas/panel.csv`, `atlas/global.csv`) are not distributed: `make data` rebuilds them from the pinned release, and they
were removed from the public history together with a few other files.

## Licences

- Code (Python, Makefile, configuration and build scripts): MIT, `LICENSE`.
- Text, figures, tables and results: CC BY 4.0, `LICENSE-CC-BY-4.0.md`.
- Outputs built on the Global Macro Database (the atlas statistics, the category 07 figures and their book, the
  GMD-growth results and the channel anatomy): **CC BY-NC-SA 4.0**, following the database's terms; each affected
  folder has a `LICENSE.md` note.
- Third-party data keep their own terms (`DATA_LICENSES.md`), including the IMF and BIS attribution notes.

## Citation

Shinde, S. (2026). Economic Fibrillation: Business-Cycle Synchronization and the Loss of Diversification in Global
Recessions. SSRN, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7629818. Code and data: https://github.com/fxcl1618033/economic-fibrillation (tag
`paper1-complete-v1.3`).
