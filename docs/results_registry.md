# Results registry — Paper 1

Every number Paper 1 reports or has reported, where it comes from and how much weight it can bear. 26 economies,
Maddison 2023 real GDP per capita, 2–9 year band-pass (Butterworth order 2, forward–backward), statistics on
1970–2022 (T = 53), Kose–Terrones global recessions 1975, 1982, 1991, 2009 and 2020, unless a row says otherwise.
Machine-readable headline values with tolerances: `tests/golden_paper1.json`.

**Columns.** *Source* is the results file (in `paper1/results/`) or Methods section the number comes from.
*Status*: `headline` (a claim of the paper), `robustness`, `null` (reported as a null), `descriptive`,
`superseded`, `flag` (see `docs/open_issues.md`).

**Nulls and floors.** Circular-shift permutation: 53 configurations, smallest possible p = 1/53 = 0.019, so
p = 0.019 means "no shift did better". Surrogates: 5,000 spectrum-preserving sets, floor 1/5001 = 0.0002.

## 1. The crisis arc (Methods §6.3–6.4) — the primary test

| ID | Quantity | Value | p | Source | Status |
|---|---|---|---|---|---|
| A1 | corr(r(t), recession at t+2) — lead-2 | +0.230 | 0.038 | kose_terrones_results.json | headline |
| A2 | lead-1 | +0.216 | 0.019 | same | headline |
| A3 | crisis year | +0.149 | 0.189 | same | headline (n.s.) |
| A4 | after-1 (one-sided down) | +0.078 | 0.679 | same | headline (n.s.) |
| A5 | after-2 (one-sided down) | −0.277 | 0.019 | same | headline |
| A6 | Superposed epoch: mean r at t−1 / t+2 | 0.70 / 0.35 | — | same | descriptive |
| A7 | Mean r: recessions / downturns / normal years (95% bootstrap CI) | 0.65 [0.45, 0.86] / 0.37 [0.23, 0.62] / 0.54 [0.47, 0.61] | — | same | descriptive |
| A8 | Bonferroni over five lags: lead-1 and after-2 / lead-2 | p_adj 0.095 / 0.189 | — | Methods §7.4 | robustness |
| A9 | Benjamini–Hochberg: lead-1 and after-2 / lead-2 | q 0.047 / 0.063 | — | Methods §7.4 | robustness |
| A10 | Same arc under convention W (Hilbert on 1970–2022 only): lead-2 / lead-1 / after-2 | +0.210 / +0.178 / −0.144 | 0.057 / 0.094 / 0.170 | runin_convention_check.json | **flag** (issue 1) |
| A11 | Same arc under convention N (no run-in): lead-2 / lead-1 / after-2 | +0.210 / +0.178 / −0.197 | 0.038 / 0.094 / 0.094 | runin_convention_check.json | **flag** (issue 1) |

## 2. Robustness of the arc (Methods §7.1–7.5; all convention P)

Full printout: `paper1/results/printed/robustness_output.txt` (only the baseline is saved as JSON).

| ID | Check | Lead-2 | Lead-1 | Crisis | After-2 | Status |
|---|---|---|---|---|---|---|
| B1 | Band 2–8 years | +0.22 (0.038) | +0.19 (0.057) | +0.12 (0.245) | −0.31 (0.019) | robustness |
| B2 | Band 3–10 years | +0.26 (0.019) | +0.23 (0.038) | +0.16 (0.094) | −0.02 (0.453) | robustness |
| B3 | HP filter, λ = 100 | +0.27 (0.038) | +0.27 (0.019) | +0.19 (0.057) | −0.25 (0.038) | robustness |
| B4 | Growth rates instead of band-pass | +0.23 (0.094) | +0.34 (0.038) | +0.21 (0.075) | −0.01 (0.509) | robustness |
| B5 | Without the United States | +0.22 (0.057) | +0.20 (0.038) | +0.14 (0.208) | −0.27 (0.019) | robustness |
| B6 | Without Germany | +0.23 (0.038) | +0.23 (0.019) | +0.16 (0.170) | −0.29 (0.019) | robustness |
| B7 | Without Japan | +0.23 (0.038) | +0.22 (0.019) | +0.14 (0.226) | −0.29 (0.019) | robustness |
| B8 | 1970–1995 only (1975, 1982, 1991) | +0.31 (0.077) | +0.24 (0.115) | +0.06 (0.385) | −0.17 (0.192) | robustness |
| B9 | 1996–2022 only (2009, 2020) | +0.32 (0.111) | +0.34 (0.037) | +0.32 (0.074) | −0.45 (0.037) | robustness |
| B10 | Without 1975 | +0.23 (0.038) | +0.21 (0.019) | +0.17 (0.189) | −0.19 (0.113) | robustness |
| B11 | Without 1982 | +0.25 (0.038) | +0.24 (0.019) | +0.19 (0.057) | −0.23 (0.038) | robustness |
| B12 | Without 1991 | +0.27 (0.038) | +0.27 (0.019) | +0.21 (0.075) | −0.34 (0.019) | robustness |
| B13 | Without 2009 | +0.13 (0.226) | +0.12 (0.208) | +0.06 (0.321) | −0.28 (0.057) | robustness |
| B14 | Without 2020 | +0.14 (0.208) | +0.11 (0.264) | +0.03 (0.434) | −0.19 (0.151) | robustness |
| B15 | Without 2009 and 2020 | +0.02 (0.377) | −0.01 (0.491) | −0.08 (0.717) | −0.18 (0.094) | robustness |

Reading: the lead is carried by 2009 and 2020 (effective n ≈ 2, both modern), the post-crisis collapse is not robust
to the band or to growth rates, and no single large economy drives the result.

## 3. Synchronization and swing size (Methods §6.2)

| ID | Quantity | Value | p | Source | Status |
|---|---|---|---|---|---|
| C1 | corr(r, Ā), detrended (σ = 8 yr), convention P | +0.608 | 0.019 (circular shift) | runin_convention_check.json; Methods §6.2 | headline |
| C2 | same, raw, convention P | +0.530 | 0.019 | same | robustness |
| C3 | same, detrended, convention W (the "+0.51" of early drafts) | +0.509 | 0.019; surrogate 0.0006 | amplitude_results.json | **flag** (issue 3, resolved) |
| C4 | same, detrended, convention N | +0.531 | 0.019 | runin_convention_check.json; Methods §7.2 | robustness |
| C5 | Two-stage timing: r peaks at t−1, amplitude at t0 | — | — | amplitude_results.json (epoch) | descriptive |

## 4. What moves in a crisis (Methods §6.1, §7.6)

| ID | Quantity | Value | p | Source | Status |
|---|---|---|---|---|---|
| D1 | Cross term's share of excess crisis variance, GDP-weighted (within-window mean weights, as Methods states) | 82.4% | no valid test (§7.6) | Methods §6.1 | headline (descriptive magnitude) |
| D2 | same with end-of-window weights (as-run script) | 82.6% | — | diversification_results.json | **flag** (issue 4) |
| D3 | same, equal-weighted | 96.9% | — | diversification_equal_results.json | headline (descriptive) |
| D4 | Cross share of world variance, crisis vs normal windows: GDP-weighted / equal | 0.723 vs 0.669 / 0.880 vs 0.818 | — | Methods §6.1 | descriptive |
| D5 | Surrogate p printed on figures for the crisis cross share | 0.0002 | tests only "are economies correlated at all" | diversification_results.json | **flag** (issue 6) |
| D6 | Nominal surrogate p of the excess-share ratio (ill-posed null): equal / GDP | 0.48 / 0.35 | — | Methods §7.6 | disclosure |
| D7 | Inside the cross term's rise, GDP-weighted: from higher correlation / from bigger swings / interaction | 35% / 50% / 14% | — | printed/crossterm_split_output.txt | headline (correction) |
| D8 | same, equal-weighted | 41% / 46% / 13% | — | same | headline (correction) |
| D9 | Mean pairwise correlation, normal → crisis windows; mean cycle s.d. ratio | 0.376 → 0.490; × 1.14 | — | same | descriptive |
| D10 | Fibrillation identity |Z| = Ā × R_A, max error | 4 × 10⁻¹⁹ | — | structure_results.json | descriptive |
| D11 | Share of the crisis excess in log world swing² from alignment / from swing size | 39.3% / 60.7% | alignment 0.103; swing 0.0002 (surrogates) | structure_results.json | headline |
| D12 | corr(R_A, r) | +0.942 | — | printed/structure_tests_output.txt | descriptive |

## 5. Network geometry and phase structure (Methods §6.5–6.6, §7.7)

| ID | Quantity | Value | p | Source | Status |
|---|---|---|---|---|---|
| E1 | MST mean edge length, decade means: 1970s vs 2013–22 | 0.706 vs 0.379 (1.9×) | — | Methods §6.5 | headline (descriptive) |
| E2 | Single-year endpoints 1971 vs 2022 (the old "~3×") | 0.781 vs 0.249 | — | mst_results.json | superseded wording |
| E3 | Windows kept inside 1970–2022: 1979–89 vs 2013–22 | 0.652 vs 0.379 | — | Methods §7.7 | robustness |
| E4 | Pre-crisis MST contraction, Kendall τ (raw / detrended) | −0.171 / −0.086 | 0.167 / 0.316 | mst_results.json; Methods §6.5 | null |
| E5 | The old "p = 0.47" for E4 | — | not reproducible | — | do not cite |
| E6 | Largest-eigenvalue fragility trend | τ +0.10 | 0.306 | mst_results.json | null |
| E7 | Phase-lead spread (s.d. of 26 leads) | 0.403 yr | 0.0002 lower tail (surrogate mean 0.942, min 0.446) | phase_lag_results.json; Methods §6.6 | headline, but computed with convention W: recompute under P (issue 1) |
| E8 | Stored p_spread | 1.0 | upper tail | phase_lag_results.json | **flag** (issue 8) |
| E9 | Mean cycle period | 5.85 yr | — | phase_lag_results.json | descriptive |
| E10 | Fiedler split of the correlation network: λ2; blocs | 0.868; A = GBR, FRA, JPN, KOR, IND, ZAF, IDN, THA; B = the other 18 | — | structure_results.json | descriptive |
| E11 | Arc within blocs / between blocs: lead-1 | +0.18 (0.057) / +0.18 (0.038) | — | printed/structure_tests_output.txt | exploratory |

## 6. Tipping tests (Methods §6.7) — all null

| ID | Quantity | Value | p | Source | Status |
|---|---|---|---|---|---|
| F1 | Pre-crisis trend of AR(1) of r(t) | τ −0.152 | 0.757 | csd_surrogate_results.json | null |
| F2 | Pre-crisis trend of variance of r(t) | τ +0.295 | 0.107 | same | null |
| F3 | Restoring time (third indicator) | null | — | csd_fast.py (lost) | null, to rebuild (issue 10) |
| F4 | Post-crisis change in recovery rate λ (coupling as bifurcation parameter) | +0.098 | 0.542 | kuramoto_bifurcation_results.json | null |
| F5 | Implied K/K_c around onsets, mean t−1 / t0 | 6.4 / 7.1 | — | printed/kuramoto_bifurcation_output.txt | descriptive (a transform of r) |

## 7. Channels inside the economies (atlas and panel26; Global Macro Database, not Maddison)

| ID | Quantity | Value | p | Source | Status |
|---|---|---|---|---|---|
| G1 | Short-rate synchronization leads recessions by two years (18 economies) | +0.266 | 0.019 | atlas/sync.json | headline (new, needs past-only phases: issue 14) |
| G2 | Investment synchronization, lead-2 | +0.293 | 0.038 | atlas/sync.json | exploratory |
| G3 | Real GDP (GMD, not per capita) synchronization, lead-1 / after-2 | +0.237 / −0.332 | 0.019 / 0.019 | atlas/sync.json | robustness of A2/A5 on other data |
| G4 | Channel synchronization above surrogate chance, all nine channels | mean r 0.34–0.64 vs null 0.17–0.25 | 0.0005 each (the floor with 2,000 surrogates) | panel26_results.json | descriptive |
| G5 | Mean pairwise cycle correlation before/after 1990: GDP, exports, imports, budget balance | 0.22→0.58, 0.30→0.60, 0.39→0.61, 0.09→0.56 | — | panel26_results.json | descriptive |
| G6 | US–Japan cycle correlation 1961–89 → 1990–2019: exports, imports, investment, GDP | 0.36→0.73, 0.47→0.64, 0.08→0.43, 0.32→0.44 | — | printed/usjp_output.txt | descriptive |
| G7 | Economies contracting: 2020 / 2009 / 1975, 1982, 1991 | 25 / 22 / 8–11 of 26 | — | atlas/global.csv | descriptive |
| G8 | Average coupling to the other 25, 1970–89 vs 1990–2022 | 0.46 vs 0.75 | — | atlas/stats.json | descriptive |

## 8. Superseded explorations (history only)

| ID | Quantity | Value | p | Source |
|---|---|---|---|---|
| H1 | Current-dollar GDP, hand-picked windows: mean R global / regional / normal; contrast | 0.75 / 0.45 / 0.67; +0.103 | 0.038 (20,000 placements) | crisis_results.json |
| H2 | Real GDP, hand-picked windows: same | 0.70 / 0.30 / 0.52; +0.202 | 0.020 | crisis_results_real.json |
| H3 | JST banking crises (17 economies, 1970–2016): same year / lead-1 / lead-2 | +0.23 / +0.21 / +0.13 | 0.106 / 0.149 / 0.298 | crisis_dating_results.json (not re-verified) |
| H4 | First-pass surrogate test on current-dollar GDP: 2009 / 2020 | R 0.74 / 0.81 | 0.0002 / 0.0002 | surrogate_results.csv |
