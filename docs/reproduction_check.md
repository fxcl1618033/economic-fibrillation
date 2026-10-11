# Reproduction check — 11 October 2026

**Result: every stored Paper 1 result and every atlas data file reproduces exactly from the pinned sources.**

How it was run, from a clean copy of this repository:

```bash
python3 tools/fetch_data.py      # clones the six pinned commits in data/sources.yaml, verifies sha256 (about 7 s)
python3 tools/rerun_asrun.py     # runs every as-run script unchanged, compares with paper1/results (about 90 s)
```

Environment: Python 3.13.16, numpy 2.5.3, scipy 1.18.1, pandas 3.0.5, matplotlib 3.11.2, pyreadr 0.5.7,
networkx 3.6.1, openpyxl 3.1.5.

| Script or file | Result | Note |
|---|---|---|
| kose_terrones_test | EXACT | crisis arc, the paper's primary test |
| amplitude_test | EXACT | uses convention W (see open issue 1) |
| robustness | EXACT | only the baseline is saved; the full printout is in `paper1/results/printed/robustness_output.txt` |
| real_gdp_analysis | EXACT | superseded hand-picked windows |
| structure_tests | EXACT | fibrillation identity, Fiedler blocs |
| crossterm_split | ran | prints only; output in `paper1/results/printed/` |
| panel26 | EXACT | channel anatomy |
| usjp | ran | prints only; output in `paper1/results/printed/` |
| phase_lags | EXACT | |
| csd_surrogate | EXACT | |
| kuramoto_bifurcation | EXACT | |
| diversification | EXACT | end-of-window GDP weights (see open issue 4) |
| diversification_equal | EXACT | |
| mst_network | EXACT | |
| crisis_analysis | EXACT | superseded current-dollar data |
| hilbert_oscillators | EXACT | superseded current-dollar data |
| surrogate_test | EXACT | superseded current-dollar data |
| atlas/panel.csv | EXACT | byte-for-byte |
| atlas/global.csv | EXACT | byte-for-byte |
| atlas/meta.json | EXACT | byte-for-byte |
| atlas/stats.json | EXACT | byte-for-byte |
| atlas/sync.json | EXACT | byte-for-byte |

Not run: `crisis_dating_test.py` (needs `jst.xlsx`, never pinned), `build_coupling_matrix.py` (needs the BIS file,
never downloaded), `prepare_data.py` (fetched from the network in July; its outputs are kept in `paper1/data/`).

Also checked the same day:

- `tools/check_runin_conventions.py` recomputes r(t) three ways. Convention P reproduces the stored
  `kose_terrones_results.json` series to 3 × 10⁻¹⁶ and convention W reproduces `amplitude_results.json` exactly. This
  settles where the "+0.51" amplitude coefficient came from (open issue 3) and shows the crisis arc depends on the
  convention (open issue 1).
- The Methods §6.1 GDP-weighted figures (82.4%, cross shares 0.723 and 0.669) are reproduced by weighting each window
  by its within-window mean real GDP, as the Methods text says. The as-run script weights by the window's last year
  and gives 82.6%, 0.724 and 0.668 (open issue 4).
- The Maddison file has not changed since 12 October 2025 (commit 8316aec); the package version moved from 1.1.0 to
  1.1.1 on 10 October 2026 with documentation changes only. Methods §8 should cite the commit and checksum, not only
  the version.
