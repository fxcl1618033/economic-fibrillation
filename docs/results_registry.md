# Results registry — Paper 1

Every number Paper 1 reports or has reported, where it comes from and how much weight it can bear.

**Samples and conventions.** The main sample is **S30**: the original 26 economies plus Brazil, China, Iran and Saudi
Arabia (Sid, 11 October 2026). **S26** is the original 26, kept as the reference. Both columns are under the
pre-registered conventions (`docs/preregistration_S30.md`): convention P (band-pass and Hilbert transform on 1950–2022,
statistics on 1970–2022, T = 53), rolling windows that may start in 1962 and never earlier, Maddison 2023 real GDP per
capita, 2–9 year band-pass (Butterworth order 2, forward–backward), Kose–Terrones global recessions 1975, 1982, 1991,
2009 and 2020, unless a row says otherwise.

**Updated 11 October 2026** from the Phase 3 run (`results/`, code 07bbdd8; `results/COMPARISON.md`) and Sid's
decisions on it. Where an S26 value differs from the value first stored, the cell says "was" with the first-run value;
old value, new value and cause are in `docs/decisions.md` (rule 6). `tests/golden_paper1.json` keeps the first-run S26
values, which the code still reproduces exactly: it is the regression baseline, not the paper's numbers.

**Columns.** *Source*: `results/<sample>/P/<test>.json` unless given (`S30/P/arc` means `results/S30/P/arc.json`).
*Status*: `headline` (a claim of the paper), `robustness`, `null` (reported as a null), `descriptive`, `limitation`
(reported, not claimed), `exploratory`, `dropped`, `superseded`, `flag` (see `docs/open_issues.md`).

**Nulls and floors.** Circular-shift permutation: 53 configurations, smallest possible p = 1/53 = 0.019, so p = 0.019
means "no shift did better" (split samples: 1/26 = 0.038 and 1/27 = 0.037). Surrogates: 5,000 spectrum-preserving
sets, floor 1/5001 = 0.0002; channel anatomy 2,000, floor 0.0005.

## 1. The crisis arc (Methods §6.3–6.4) — the primary test

A1–A5 on S30 under P are the pre-registered primary family. Values are corr(r(t), recession indicator at the lag) with
the one-sided p in brackets.

| ID | Quantity | S30 | S26 | Source | Status |
|---|---|---|---|---|---|
| A1 | Lead-2 | +0.226 (0.038) | +0.230 (0.038) | `<sample>/P/arc` | reported, **not claimed as a lead**: fails past-only phases (A13) |
| A2 | Lead-1 | +0.217 (0.019) | +0.216 (0.019) | same | **headline**: survives past-only phases (A13); rests on 2009 and 2020 (B13–B15) |
| A3 | Crisis year | +0.161 (0.189) | +0.149 (0.189) | same | null |
| A4 | After-1 (one-sided down) | +0.111 (0.755) | +0.078 (0.679) | same | null |
| A5 | After-2 (one-sided down) | −0.236 (0.057) | −0.277 (0.019) | same | **limitation** (Sid, 11 Oct 2026): fragile — not significant on S30, under W, N, E or C, at 3–10 years, with growth rates or without 2020 |
| A6 | Superposed epoch: mean r at t−1 / t+2 | 0.65 / 0.33 | 0.70 / 0.35 | same | descriptive |
| A7 | Mean r: recessions / downturns / normal years (95% bootstrap CI) | 0.61 [0.39, 0.84] / 0.30 [0.12, 0.55] / 0.49 [0.42, 0.56] | 0.65 [0.45, 0.86] / 0.37 [0.23, 0.62] / 0.54 [0.47, 0.61] | same | descriptive |
| A8 | Bonferroni over five lags: lead-1 / after-2 / lead-2 | 0.094 / 0.283 / 0.189 | 0.094 / 0.094 / 0.189 (Methods printed 0.095) | same | robustness; no raw p at the floor can pass (5/53 = 0.094) |
| A9 | Benjamini–Hochberg q: lead-1 / after-2 / lead-2 | 0.094 / 0.094 / 0.094 | 0.047 / 0.047 / 0.063 | same | robustness; **on S30 no lag survives** |
| A10 | Convention W (Hilbert on 1970–2022 only): lead-2 / lead-1 / after-2 | +0.204 (0.075) / +0.184 (0.057) / −0.131 (0.170) | +0.210 (0.057) / +0.178 (0.094) / −0.144 (0.170) | `<sample>/P/conventions` (W) | robustness (issue 1) |
| A11 | Convention N (no run-in): same | +0.204 (0.019) / +0.173 (0.094) / −0.158 (0.132) | +0.210 (0.038) / +0.178 (0.094) / −0.197 (0.094) | `<sample>/P/conventions` (N) | robustness (issue 1) |
| A12 | Convention E (9-year mirror): same | +0.224 (0.038) / +0.226 (0.019) / −0.136 (0.170) | +0.228 (0.057) / +0.220 (0.019) / −0.170 (0.113) | `<sample>/P/conventions` (E) | robustness (issues 1, 2) |
| A13 | Convention C (past data only): same | −0.021 (0.528) / +0.369 (0.038) / −0.161 (0.170) | +0.007 (0.453) / +0.374 (0.038) / −0.167 (0.151) | `<sample>/P/conventions` (C) | the rule-7 test: lead-1 holds, lead-2 and after-2 do not |
| A14 | Without 2020, conventions P / E: lead-1; after-2 | P +0.099 (0.321), E +0.104 (0.283); P −0.166 (0.170), E −0.168 (0.113) | P +0.109 (0.264), E +0.112 (0.226); P −0.186 (0.151), E −0.193 (0.094) | `<sample>/{P,E}/robustness` | robustness (issue 2) |

## 2. Robustness of the arc (Methods §7.1–7.5)

S30 under P (`S30/P/robustness`):

| ID | Check | Lead-2 | Lead-1 | Crisis | After-2 | Status |
|---|---|---|---|---|---|---|
| B1 | Band 2–8 years | +0.22 (0.038) | +0.18 (0.113) | +0.12 (0.226) | −0.26 (0.038) | robustness |
| B2 | Band 3–10 years | +0.26 (0.038) | +0.24 (0.019) | +0.16 (0.113) | +0.02 (0.566) | robustness |
| B3 | HP filter, λ = 100 | +0.28 (0.038) | +0.27 (0.019) | +0.14 (0.113) | −0.19 (0.075) | robustness |
| B4 | Growth rates instead of band-pass | +0.24 (0.075) | +0.33 (0.038) | +0.14 (0.132) | +0.04 (0.679) | robustness |
| B5 | Without the United States | +0.22 (0.057) | +0.21 (0.019) | +0.16 (0.208) | −0.22 (0.075) | robustness |
| B6 | Without Germany | +0.23 (0.038) | +0.23 (0.019) | +0.17 (0.151) | −0.25 (0.057) | robustness |
| B7 | Without Japan | +0.22 (0.038) | +0.22 (0.019) | +0.16 (0.208) | −0.24 (0.057) | robustness |
| B8 | 1970–1995 only (1975, 1982, 1991) | +0.31 (0.077) | +0.21 (0.154) | +0.06 (0.385) | −0.18 (0.192) | robustness |
| B9 | 1996–2022 only (2009, 2020) | +0.32 (0.111) | +0.37 (0.037) | +0.35 (0.074) | −0.34 (0.074) | robustness |
| B10 | Without 1975 | +0.21 (0.057) | +0.20 (0.057) | +0.18 (0.132) | −0.15 (0.151) | robustness |
| B11 | Without 1982 | +0.25 (0.038) | +0.25 (0.019) | +0.20 (0.057) | −0.19 (0.038) | robustness |
| B12 | Without 1991 | +0.28 (0.038) | +0.29 (0.019) | +0.24 (0.057) | −0.28 (0.038) | robustness |
| B13 | Without 2009 | +0.14 (0.208) | +0.12 (0.226) | +0.07 (0.358) | −0.26 (0.075) | robustness |
| B14 | Without 2020 | +0.12 (0.264) | +0.10 (0.321) | +0.03 (0.453) | −0.17 (0.170) | robustness |
| B15 | Without 2009 and 2020 | +0.01 (0.377) | −0.03 (0.528) | −0.09 (0.679) | −0.19 (0.113) | robustness |
| B16 | Each of the 30 left out in turn (range) | +0.21 to +0.25 (0.019–0.094) | +0.21 to +0.23 (0.019–0.038) | +0.13 to +0.18 (0.132–0.226) | −0.25 to −0.22 (0.019–0.075) | robustness |
| B17 | Each added economy left out: CHN / BRA / SAU / IRN | 0.057 / 0.038 / 0.019 / 0.038 | 0.019 / 0.019 / 0.038 / 0.019 | — | 0.075 / 0.019 / 0.057 / 0.057 | robustness (p only; mandatory) |
| B18 | Norway, Switzerland, South Africa with GMD growth 1991–2011 (issue 13) | +0.23 (0.038) | +0.22 (0.019) | +0.16 (0.151) | −0.26 (0.075) | robustness (`S30_gmd_growth/P/arc`; S26 below: `S26_gmd_growth/P/arc`) |

S26 under P (`S26/P/robustness`; identical to the first run, which used P):

| ID | Check | Lead-2 | Lead-1 | Crisis | After-2 |
|---|---|---|---|---|---|
| B1 | Band 2–8 years | +0.22 (0.038) | +0.19 (0.057) | +0.12 (0.245) | −0.31 (0.019) |
| B2 | Band 3–10 years | +0.26 (0.019) | +0.23 (0.038) | +0.16 (0.094) | −0.02 (0.453) |
| B3 | HP filter, λ = 100 | +0.27 (0.038) | +0.27 (0.019) | +0.19 (0.057) | −0.25 (0.038) |
| B4 | Growth rates instead of band-pass | +0.23 (0.094) | +0.34 (0.038) | +0.21 (0.075) | −0.01 (0.509) |
| B5 | Without the United States | +0.22 (0.057) | +0.20 (0.038) | +0.14 (0.208) | −0.27 (0.019) |
| B6 | Without Germany | +0.23 (0.038) | +0.23 (0.019) | +0.16 (0.170) | −0.29 (0.019) |
| B7 | Without Japan | +0.23 (0.038) | +0.22 (0.019) | +0.14 (0.226) | −0.29 (0.019) |
| B8 | 1970–1995 only (1975, 1982, 1991) | +0.31 (0.077) | +0.24 (0.115) | +0.06 (0.385) | −0.17 (0.192) |
| B9 | 1996–2022 only (2009, 2020) | +0.32 (0.111) | +0.34 (0.037) | +0.32 (0.074) | −0.45 (0.037) |
| B10 | Without 1975 | +0.23 (0.038) | +0.21 (0.019) | +0.17 (0.189) | −0.19 (0.113) |
| B11 | Without 1982 | +0.25 (0.038) | +0.24 (0.019) | +0.19 (0.057) | −0.23 (0.038) |
| B12 | Without 1991 | +0.27 (0.038) | +0.27 (0.019) | +0.21 (0.075) | −0.34 (0.019) |
| B13 | Without 2009 | +0.13 (0.226) | +0.12 (0.208) | +0.06 (0.321) | −0.28 (0.057) |
| B14 | Without 2020 | +0.14 (0.208) | +0.11 (0.264) | +0.03 (0.434) | −0.19 (0.151) |
| B15 | Without 2009 and 2020 | +0.02 (0.377) | −0.01 (0.491) | −0.08 (0.717) | −0.18 (0.094) |
| B16 | Each of the 26 left out in turn (range) | +0.21 to +0.26 (0.019–0.113) | +0.20 to +0.23 (0.019–0.057) | +0.12 to +0.17 (0.132–0.264) | −0.30 to −0.26 (0.019–0.038) |
| B18 | Norway, Switzerland, South Africa with GMD growth 1991–2011 | +0.23 (0.057) | +0.22 (0.038) | +0.15 (0.170) | −0.30 (0.019) |

Reading (both samples): the lead is carried by 2009 and 2020 (effective n ≈ 2, both modern); the post-crisis fall is
not robust to the band, to growth rates or, on S30, to anything; no single economy drives the lead.

## 3. Synchronization and swing size (Methods §6.2)

| ID | Quantity | S30 | S26 | Source | Status |
|---|---|---|---|---|---|
| C1 | corr(r, Ā), detrended (σ = 8 yr) | +0.641 (0.019; surrogate 0.0002) | +0.608 (0.019; surrogate 0.0002, was 0.0006 with W surrogates) | `<sample>/P/amplitude` | headline |
| C2 | same, raw | +0.458 (0.019) | +0.530 (0.019) | same | robustness |
| C3 | same, detrended, convention W (the "+0.51" of early drafts) | +0.549 (0.019; surrogate 0.0008) | +0.509 (0.019; surrogate 0.0006) | `<sample>/W/amplitude` | robustness (issue 3, resolved) |
| C4 | same, convention N | +0.535 (0.019; surrogate 0.0008) | +0.531 (0.019; surrogate 0.0006) | `<sample>/N/amplitude` | robustness |
| C5 | Two-stage timing: r peaks at t−1, amplitude at t0 | — | — | amplitude_results.json (epoch, S26 first run) | descriptive |
| C6 | same, convention E | +0.577 (0.019; surrogate 0.0004) | +0.536 (0.019; surrogate 0.0006) | `<sample>/E/amplitude` | robustness |
| C7 | same, convention C (past data only) | +0.723 (0.019) | +0.682 (0.019) | `<sample>/P/conventions` (C) | robustness |
| C8 | Without Iran / Saudi Arabia / both (detrended) | +0.644 / +0.621 / +0.620 (0.019 each; surrogate 0.0002) | — | `S30_minus_*/P/amplitude` | robustness (mandatory) |

## 4. What moves in a crisis (Methods §6.1, §7.6)

| ID | Quantity | S30 | S26 | Source | Status |
|---|---|---|---|---|---|
| D1 | Cross term's share of excess crisis variance, GDP-weighted (within-window mean weights, as the Methods state) | 83.3% | 80.2% (was 82.4%: four recessions, windows from 1970) | `<sample>/P/diversification` | headline (descriptive magnitude) |
| D2 | same with end-of-window weights (as-run script) | — | 82.6% (first run) | diversification_results.json | **flag** (issue 4); kept as the as-run record |
| D3 | same, equal-weighted | 96.8% | 96.5% (was 96.9%) | same | headline (descriptive) |
| D4 | Cross share of world variance, crisis vs normal windows: GDP-weighted / equal | 0.707 vs 0.619 / 0.771 vs 0.671 | 0.704 vs 0.646 / 0.876 vs 0.817 (was 0.723 vs 0.669 / 0.880 vs 0.818) | same | descriptive |
| D5 | Surrogate p printed on figures for the crisis cross share | 0.0002 | 0.0002 | same | **flag** (issue 6): tests only "are economies correlated at all" |
| D6 | Disclosure: nominal p of the share ratio, GDP / equal; Δcross; Δown | 0.32 / 0.47; 0.0002 both; 0.035 GDP, 0.0002 equal | 0.34 / 0.48; all 0.0002 (Methods: 0.35 / 0.48) | same (`d6`) | disclosure |
| D7 | Inside the cross term's rise, GDP-weighted: correlation / swing size / interaction | 44% / 41% / 15% | 33% / 53% / 14% (was 35 / 50 / 14%) | `<sample>/P/cross_split` | headline (correction): both parts of similar size; which is larger depends on the sample |
| D8 | same, equal-weighted | 49% / 38% / 13% | 39% / 49% / 12% (was 41 / 46 / 13%) | same | headline (correction) |
| D9 | Mean pairwise correlation, normal → crisis windows; mean cycle s.d. ratio | 0.294 → 0.392; × 1.11 | 0.351 → 0.441; × 1.13 (was 0.376 → 0.490; × 1.14) | same | descriptive |
| D10 | Fibrillation identity \|Z\| = Ā × R_A, max error | below 10⁻¹⁸ (machine rounding) | below 10⁻¹⁸ (machine rounding) | `<sample>/P/structure` | descriptive |
| D11 | Share of the crisis excess in log world swing² from alignment / from swing size (surrogate p) | 18.9% / 81.1% (0.356 / 0.0002) | 39.3% / 60.7% (0.103 / 0.0002) | same | headline for the swing part; **the alignment share depends on Iran** (D13); its use in Results is for Sid to decide |
| D12 | corr(R_A, r) | +0.886 | +0.942 | same | descriptive |
| D13 | Without Iran / Saudi Arabia / both: D1; D3; D7; D11 alignment share | 83.0 / 82.9 / 82.5%; 96.5 / 97.1 / 96.8%; 42/43/15, 43/42/15, 41/44/15%; 33.0 / 17.4 / 37.4% | — | `S30_minus_*/P/` | robustness (mandatory) |
| D14 | Windows kept inside 1970–2022 (four recessions): D1 / D3 | 85.9% / 96.7% | 82.4% / 96.9% (the first-run values) | `<sample>_strict/P/diversification` | robustness |

## 5. Network geometry and phase structure (Methods §6.5–6.6, §7.7)

| ID | Quantity | S30 | S26 | Source | Status |
|---|---|---|---|---|---|
| E1 | MST mean edge length, decade means 1979–89 vs 2013–22 (same with windows from 1962 or from 1970) | 0.680 vs 0.421 (1.6×) | 0.677 vs 0.379 (1.8×) | `<sample>/P/mst` | headline (descriptive); replaces 0.706 vs 0.379 (1.9×) |
| E2 | Single-year endpoints 1971 vs 2022 (the old "~3×") | — | 0.781 vs 0.249 | mst_results.json | dropped (Sid, 11 Oct 2026); Methods' 0.771 matched no result |
| E3 | Windows kept inside 1970–2022: L from 1979; decade means unchanged | 0.680 vs 0.421 | 0.677 vs 0.379 | `<sample>_strict/P/mst` | robustness; replaces 0.652, which was L(1979) alone |
| E4 | Pre-crisis MST contraction, Kendall τ, raw; detrended (σ = 8) | −0.143 (0.219); +0.057 (0.659) | −0.171 (0.168, was 0.167); −0.057 (0.356) | `<sample>/P/mst` | null; the first-run detrended −0.086 (0.316) does not reproduce (issue 23) |
| E4s | same, windows inside 1970–2022 (1991, 2009, 2020) | +0.119 (0.692); +0.381 (0.936) | +0.000 (0.504); +0.167 (0.740) | `<sample>_strict/P/mst` | null |
| E5 | The old "p = 0.47" for E4 | — | not reproducible | — | do not cite |
| E6 | Largest-eigenvalue fragility trend | τ +0.086 (0.338) | τ +0.100 (0.311, was 0.306) | `<sample>/P/mst` | null |
| E7 | Phase-lead spread (s.d. of the leads), lower tail | 0.535 yr (0.0004; surrogate mean 0.988, min 0.523) | 0.445 yr (0.0002; surrogate mean 0.949, min 0.456); was 0.403 under W | `<sample>/P/phase_lags` | headline |
| E8 | Upper-tail p stored by the first run | 1.0 | 1.0 | same (`p_spread_upper_as_run`) | resolved (issue 8): the lower tail is now stored |
| E9 | Mean cycle period | 5.95 yr | 5.98 yr (was 5.85, W) | same | descriptive |
| E10 | Fiedler split of the correlation network: λ2; blocs | 0.834; A = USA, GBR, JPN, KOR, IND, TUR, NOR, DNK, IDN, THA, CHN, IRN; B = the other 18 | 0.868; A = GBR, FRA, JPN, KOR, IND, ZAF, IDN, THA; B = the other 18 | `<sample>/P/structure` | descriptive |
| E11 | Arc within blocs / between blocs: lead-1 | +0.21 (0.019) / +0.13 (0.151) | +0.18 (0.057) / +0.18 (0.038) | same | exploratory |

## 6. Tipping tests (Methods §6.7)

Pre-crisis windows used (15-year windows from 1962): 1982 (six of eight years defined), 1991, 2009, 2020; 1975 has
none. Coupling test: after all five recessions.

| ID | Quantity | S30 | S26 | Source | Status |
|---|---|---|---|---|---|
| F1 | Pre-crisis trend of the lag-1 autocorrelation of r(t) | τ −0.098 (0.676) | τ +0.027 (0.456); was −0.152 (0.757) under W | `<sample>/P/csd` | null |
| F2 | Pre-crisis trend of the variance of r(t) | τ +0.420 (0.037) | τ +0.438 (0.033); was +0.295 (0.107) under W | same | **reported as it is** (Sid, 11 Oct 2026): rising variance without rising autocorrelation, so not the slowing-down signature; rests on 2009 and 2020 (F2b) |
| F2b | F2 by recession (not pre-registered): without 2009 and 2020; 2009 and 2020 alone; without 2009; without 2020 | −0.018 (0.528); +0.857 (0.005); +0.274 (0.200); +0.274 (0.176) | +0.125 (0.408); +0.750 (0.019); +0.369 (0.123); +0.298 (0.154) | `followup/<sample>/P/csd_by_event`; `results/FOLLOWUP.md` | exploratory (Sid asked for it after Phase 3) |
| F2c | F2 under W / N / E | +0.295 (0.113) / +0.393 (0.075) / +0.384 (0.054) | +0.295 (0.107) / +0.369 (0.091) / +0.420 (0.041) | `<sample>/{W,N,E}/csd` | robustness |
| F2s | F1 / F2 with windows inside 1970–2022 (2009 and 2020 only) | −0.036 (0.550) / +0.857 (0.005) | −0.071 (0.595) / +0.750 (0.019) | `<sample>_strict/P/csd` | robustness |
| F3 | Restoring time (third indicator) | — | — | — | dropped (Sid, 11 Oct 2026): as 1/(−ln φ) it is a monotone function of the lag-1 autocorrelation, so not independent (issue 22) |
| F4 | Post-crisis change in recovery rate λ (coupling as bifurcation parameter) | +0.024 (0.507) | +0.078 (0.534); was +0.098 (0.542) under W | `<sample>/P/bifurcation` | null |
| F4s | same, windows inside 1970–2022 (1982–2020) | +0.102 (0.530) | +0.182 (0.578) | `<sample>_strict/P/bifurcation` | null |
| F5 | Implied K/K_c around onsets, mean t−1 / t0 | 4.0 / 4.6 | 5.6 / 6.7; was 6.4 / 7.1 under W | `<sample>/P/bifurcation` | descriptive (a transform of r) |

## 7. Channels inside the economies (Global Macro Database on the repaired atlas panel, not Maddison)

An economy enters a channel only with continuous data 1965–2022 (amendment 1.5); counts in brackets.

| ID | Quantity | S30 | S26 | Source | Status |
|---|---|---|---|---|---|
| G1 | Short-rate synchronization, lead-2 | +0.273 (0.019) [19] | +0.266 (0.019) [18] | `<sample>/P/channels` (`sync`) | **description only** (Sid, 11 Oct 2026): fails past-only phases (G1C), so not a lead claim |
| G1C | same, past data only | +0.165 (0.151) | +0.151 (0.170) | `<sample>/C/channels` | the rule-7 test (issue 14): fails |
| G2 | Investment synchronization, lead-2; past data only | +0.270 (0.038) [28]; −0.110 (0.717) | +0.293 (0.038) [26]; −0.085 (0.642) | same | description only: fails past-only phases |
| G3 | Real GDP (GMD, not per capita) synchronization, lead-1 / after-2; past-only lead-1 | +0.245 (0.019) / −0.291 (0.019) [29]; +0.311 (0.057) | +0.237 (0.019) / −0.332 (0.019) [26]; +0.278 (0.057) | same | robustness of A2/A5 on other data; past-only lead-1 just misses 0.05 |
| G3o | Channel order, two-sided phases: short rates peak at lead-2, investment at lead-2 and lead-1 (+0.270, +0.262), real GDP at lead-1 | — | — | same | descriptive only (Sid) |
| G4 | Channel synchronization above surrogate chance, all nine channels | mean r 0.33–0.61 vs null 0.17–0.30 | mean r 0.34–0.64 vs null 0.17–0.30 (was null 0.17–0.25) | `<sample>/P/channels` (`anatomy`) | descriptive; p 0.0005 each (the floor with 2,000 surrogates) |
| G5 | Mean pairwise cycle correlation before/after 1990: GDP, exports, imports, budget balance | 0.20→0.51, 0.27→0.57, 0.36→0.55, 0.19→0.59 | 0.23→0.58, 0.30→0.60, 0.39→0.61, 0.19→0.59 (was GDP 0.22→0.58, balance 0.09→0.56) | same | descriptive |
| G5b | Budget channels (spending, balance) on the repaired panel | 9 economies: USA, JPN, CAN, KOR, IND, ZAF, NOR, GRC, THA | same 9 (was 26 on the raw data) | same | **note**: most repaired spending series start after 1965 and fail the coverage rule |
| G6 | US–Japan cycle correlation 1961–89 → 1990–2019: exports, imports, investment, GDP | — | 0.36→0.73, 0.47→0.64, 0.08→0.43, 0.32→0.44 | printed/usjp_output.txt | descriptive (not rerun: two economies) |
| G7 | Economies contracting in 1975, 1982, 1991, 2009, 2020 | 13, 9, 8, 24, 27 of 30 | 11, 8, 8, 22, 25 of 26 | same (`contracting`) | descriptive |
| G8 | Average coupling to the rest of the sample, 1970–89 vs 1990–2022 | 0.43 vs 0.70 | 0.46 vs 0.75 | same (`coupling`) | descriptive |

## 8. Superseded explorations (history only)

| ID | Quantity | Value | p | Source |
|---|---|---|---|---|
| H1 | Current-dollar GDP, hand-picked windows: mean R global / regional / normal; contrast | 0.75 / 0.45 / 0.67; +0.103 | 0.038 (20,000 placements) | crisis_results.json |
| H2 | Real GDP, hand-picked windows: same | 0.70 / 0.30 / 0.52; +0.202 | 0.020 | crisis_results_real.json |
| H3 | JST banking crises (17 economies, 1970–2016): same year / lead-1 / lead-2 | +0.23 / +0.21 / +0.13 | 0.106 / 0.149 / 0.298 | crisis_dating_results.json (not re-verified) |
| H4 | First-pass surrogate test on current-dollar GDP: 2009 / 2020 | R 0.74 / 0.81 | 0.0002 / 0.0002 | surrogate_results.csv |
