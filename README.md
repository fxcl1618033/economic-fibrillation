# Economic Fibrillation

Is the synchronization of business cycles across economies a signature of systemic fragility? This repository holds
everything produced for **Paper 1** up to 11 October 2026 (scripts, results, figures, the Methods, the country atlas,
the companion book and the GNN literature review) and the plan for the next round: a reproducible rebuild, a rerun of
every test on a wider sample, and a graph neural network for the coupling between economies.

Author: Siddhant Shinde.

## Start

```bash
make all     # Python 3.13 environment from requirements.lock, pinned data, as-run reproduction check, tests
make help    # every target
```

`make asrun` reruns every frozen script: Paper 1's results must come out EXACT; outputs built from the Global Macro
Database may instead MATCH to floating-point rounding (its data are single precision, and logs round differently on
different chips). The rules are in `src/ef/repro.py`, the Mac check in `docs/reproduction_check_mac.md`.

Working with Claude Code: it reads `CLAUDE.md` automatically; point it at `HANDOFF.md` (the start prompt is in §0).

**This copy came as two zips** (upload limit): unzip `economic-fibrillation.zip` and then
`economic-fibrillation-atlas-figures.zip` into the same parent folder, then run `make figures` to recreate
`figures/08_country_atlas/`. The atlas PDF is not in either zip: use `EF_Figures_08_Country_Atlas.pdf` or run
`make atlas-pdf`. Sid's reference PDFs are listed in `references/README.md`.

## The library (`src/ef/`)

| Module | What it does |
|---|---|
| `ef.filters` | 2–9 year band-pass, HP filter, growth rates |
| `ef.phases` | phase and swing size under conventions P (paper), W, N, E (edge-robust) and C (past data only) |
| `ef.order` | r(t), mean phase, mean swing, world phasor, amplitude-weighted alignment, the fibrillation identity |
| `ef.nulls` | circular-shift test and spectrum-preserving surrogate economies (as-run draw order) |
| `ef.crisis` | the arc, superposed epoch, bootstrap, pre-crisis trends, Bonferroni and Benjamini–Hochberg |
| `ef.decomposition` | own and cross terms (end-of-window, window-mean and equal weights) and the cross-term split |
| `ef.network`, `ef.phaselags`, `ef.tipping` | MST and eigenvalue, Fiedler blocs; phase leads; early-warning indicators and implied coupling |
| `ef.paper1` | every Paper 1 test from a run config (`configs/runs/*.yaml`); `make paper1` checks the golden numbers |
| `ef.data` | the data build (`make data`): Maddison panels, atlas, channel anatomy, validation |

## Where to look

| You want | Open |
|---|---|
| Every figure, by category | `figures/compiled/EF_Figures_00_Index.pdf`, then books 01–08 |
| Every number and where it comes from | `docs/results_registry.md` |
| What is wrong or unfinished | `docs/open_issues.md` |
| How the analysis works | `docs/methods.md` (and `docs/Economic_Fibrillation_Methods.pdf`) |
| The 31 economies in detail | `atlas/The 26 Economies 1970-2022 - Atlas.pdf` |
| What has been tried with GNNs elsewhere | `docs/literature_review_gnn.md` |
| The plan for Claude Code | `HANDOFF.md` |
| Proof that it all reproduces | `docs/reproduction_check.md` (Linux), `docs/reproduction_check_mac.md` (Sid's Mac), `docs/golden_check.md` (the library) |
| Decisions and why | `docs/decisions.md` |

## Figure books

| Book | Category | Figures |
|---|---|---|
| 00 | Index of every figure, with status | — |
| 01 | Method: from GDP to oscillators | 10 |
| 02 | The crisis arc: synchronization around global recessions | 9 |
| 03 | How the crisis definition was chosen (history) | 16 |
| 04 | What moves in a crisis: swing size, alignment and diversification | 7 |
| 05 | Network geometry and phase structure | 3 |
| 06 | Tipping tests: the honest nulls | 2 |
| 07 | Inside the economies: channels and global forces | 6 |
| 08 | Country atlas: 31 economy dashboards | 31 |

Every figure carries a status: current, needs relabelling, convention W (phases computed on 1970–2022 only),
superseded history, descriptive or unverified (one companion figure whose series matches no stored file).

## Data

Maddison Project Database 2023, the Global Macro Database (2026 release) with its IMF source files, Penn World Table
10.01, BP and EIA oil prices, and World Bank current-dollar GDP for the superseded first pass. All are pinned to a
commit with file checksums in `data/sources.yaml`.
