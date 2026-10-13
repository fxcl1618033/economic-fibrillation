# Results registry — Paper 1

Every number Paper 1 reports or has reported, where it comes from and how much weight it can bear.

**Samples and conventions.** The main sample is **S31**: the original 26 economies plus Brazil, China, Iran, Saudi
Arabia and Russia (pre-registration amendment 3, Sid, 13 October 2026). **S30** (without Russia) is the reported
comparison and **S26**, the original 26, the first reference. All three columns are under the pre-registered conventions
(`docs/preregistration_S30.md`): convention P (band-pass and Hilbert transform on 1950–2022, statistics on 1970–2022,
T = 53), rolling windows that may start in 1962 and never earlier, Maddison 2023 real GDP per capita, 2–9 year band-pass
(Butterworth order 2, forward–backward), Kose–Terrones global recessions 1975, 1982, 1991, 2009 and 2020, unless a row
says otherwise.

**Updated 13 October 2026** with the S31 run (`results/S31*`, code 2a686a3; `results/COMPARISON.md` sections 13–25,
which list every result that changes sign or crosses p = 0.05 between S30 and S31; none does in the primary
comparison). Updated 11 October 2026 from the S26 and S30 run (code 07bbdd8) and Sid's decisions on it. Where an S26
value differs from the value first stored, the cell says "was" with the first-run value; old value, new value and
cause are in `docs/decisions.md` (rule 6). `tests/golden_paper1.json` keeps the first-run S26 values, which the code
still reproduces exactly: it is the regression baseline, not the paper's numbers.

**Columns.** *Source*: `results/<sample>/P/<test>.json` unless given (`S30/P/arc` means `results/S30/P/arc.json`).
*Status*: `headline` (a claim of the paper), `robustness`, `null` (reported as a null), `descriptive`, `limitation`
(reported, not claimed), `exploratory`, `dropped`, `superseded`, `flag` (see `docs/open_issues.md`).

**Nulls and floors.** Circular-shift permutation: 53 configurations, smallest possible p = 1/53 = 0.019, so p = 0.019
means "no shift did better" (split samples: 1/26 = 0.038 and 1/27 = 0.037). Surrogates: 5,000 spectrum-preserving
sets, floor 1/5001 = 0.0002; channel anatomy 2,000, floor 0.0005.

## 1. The crisis arc (Methods §6.3–6.4) — the primary test

A1–A5 on S31 under P are the pre-registered primary family (amendment 3; S30 before it). Values are corr(r(t), recession indicator at the lag) with
the one-sided p in brackets.

| ID | Quantity | S31 | S30 | S26 | Source | Status |
|---|---|---|---|---|---|---|
| A1 | Lead-2 | +0.235 (0.038) | +0.226 (0.038) | +0.230 (0.038) | `<sample>/P/arc` | reported, **not claimed as a lead**: fails past-only phases (A13) |
| A2 | Lead-1 | +0.231 (0.019) | +0.217 (0.019) | +0.216 (0.019) | same | **headline**: supported by survival under past-only phases (A13) and leave-one-economy-out (B16), not by corrected significance (A8, A9); past-only without China p 0.057 (B19); rests on 2009 and 2020 (B13–B15) |
| A3 | Crisis year | +0.159 (0.189) | +0.161 (0.189) | +0.149 (0.189) | same | null |
| A4 | After-1 (one-sided down) | +0.099 (0.717) | +0.111 (0.755) | +0.078 (0.679) | same | null |
| A5 | After-2 (one-sided down) | −0.258 (0.057) | −0.236 (0.057) | −0.277 (0.019) | same | **limitation** (Sid, 11 Oct 2026): fragile — not significant on S30 or S31, under W, N, E or C, at 3–10 years, with growth rates or without 2020; on S31 it reaches p < 0.05 when any of 20 of the 31 economies is left out or Russia enters in 1992 (on the line, not stronger) |
| A6 | Superposed epoch: mean r at t−1 / t+2 | 0.65 / 0.31 | 0.65 / 0.33 | 0.70 / 0.35 | same | descriptive |
| A7 | Mean r: recessions / downturns / normal years (95% bootstrap CI) | 0.60 [0.39, 0.83] / 0.30 [0.13, 0.55] / 0.48 [0.42, 0.55] | 0.61 [0.39, 0.84] / 0.30 [0.12, 0.55] / 0.49 [0.42, 0.56] | 0.65 [0.45, 0.86] / 0.37 [0.23, 0.62] / 0.54 [0.47, 0.61] | same | descriptive |
| A8 | Bonferroni over five lags: lead-1 / after-2 / lead-2 | 0.094 / 0.283 / 0.189 | 0.094 / 0.283 / 0.189 | 0.094 / 0.094 / 0.189 (Methods printed 0.095) | same | robustness; no raw p at the floor can pass (5/53 = 0.094) |
| A9 | Benjamini–Hochberg q: lead-1 / after-2 / lead-2 | 0.094 / 0.094 / 0.094 | 0.094 / 0.094 / 0.094 | 0.047 / 0.047 / 0.063 | same | robustness; **on S30 no lag survives**. A lag at the floor cannot pass BH on its own: it needs a second lag at the floor (as on S26) or four at ≤ 0.038 |
| A10 | Convention W (Hilbert on 1970–2022 only): lead-2 / lead-1 / after-2 | +0.216 (0.057) / +0.204 (0.019) / −0.165 (0.113) | +0.204 (0.075) / +0.184 (0.057) / −0.131 (0.170) | +0.210 (0.057) / +0.178 (0.094) / −0.144 (0.170) | `<sample>/P/conventions` (W) | robustness (issue 1) |
| A11 | Convention N (no run-in): same | +0.216 (0.038) / +0.192 (0.057) / −0.190 (0.094) | +0.204 (0.019) / +0.173 (0.094) / −0.158 (0.132) | +0.210 (0.038) / +0.178 (0.094) / −0.197 (0.094) | `<sample>/P/conventions` (N) | robustness (issue 1) |
| A12 | Convention E (9-year mirror): same | +0.233 (0.038) / +0.236 (0.019) / −0.160 (0.132) | +0.224 (0.038) / +0.226 (0.019) / −0.136 (0.170) | +0.228 (0.057) / +0.220 (0.019) / −0.170 (0.113) | `<sample>/P/conventions` (E) | robustness (issues 1, 2) |
| A13 | Convention C (past data only): same | −0.044 (0.585) / +0.379 (0.038) / −0.159 (0.170) | −0.021 (0.528) / +0.369 (0.038) / −0.161 (0.170) | +0.007 (0.453) / +0.374 (0.038) / −0.167 (0.151) | `<sample>/P/conventions` (C) | the rule-7 test: lead-1 holds, lead-2 and after-2 do not |
| A14 | Without 2020, conventions P / E: lead-1; after-2 | P +0.112 (0.283), E +0.113 (0.264); P −0.183 (0.151), E −0.187 (0.094) | P +0.099 (0.321), E +0.104 (0.283); P −0.166 (0.170), E −0.168 (0.113) | P +0.109 (0.264), E +0.112 (0.226); P −0.186 (0.151), E −0.193 (0.094) | `<sample>/{P,E}/robustness` | robustness (issue 2) |
| A15 | Russia's phases from 1992 only (amendment 3.6): lead-2 / lead-1 / after-2 | +0.229 (0.038) / +0.224 (0.019) / −0.254 (0.038) | — | — | `S31_rus_from_1992/P/arc` | robustness: the Soviet-era years do not drive the lead; after-2 crosses to p < 0.05 |

## 2. Robustness of the arc (Methods §7.1–7.5)

S31 under P (`S31/P/robustness`; the main sample):

| ID | Check | Lead-2 | Lead-1 | Crisis | After-2 | Status |
|---|---|---|---|---|---|---|
| B1 | Band 2–8 years | +0.23 (0.057) | +0.19 (0.094) | +0.12 (0.226) | −0.27 (0.019) | robustness |
| B2 | Band 3–10 years | +0.26 (0.038) | +0.25 (0.019) | +0.16 (0.132) | +0.00 (0.509) | robustness |
| B3 | HP filter, λ = 100 | +0.27 (0.038) | +0.29 (0.019) | +0.14 (0.113) | −0.18 (0.094) | robustness |
| B4 | Growth rates instead of band-pass | +0.25 (0.057) | +0.34 (0.038) | +0.15 (0.132) | +0.04 (0.679) | robustness |
| B8 | 1970–1995 only (1975, 1982, 1991) | +0.34 (0.077) | +0.24 (0.154) | +0.06 (0.423) | −0.21 (0.192) | robustness |
| B9 | 1996–2022 only (2009, 2020) | +0.32 (0.111) | +0.38 (0.037) | +0.35 (0.074) | −0.36 (0.074) | robustness |
| B10 | Without 1975 | +0.22 (0.057) | +0.22 (0.019) | +0.19 (0.113) | −0.16 (0.151) | robustness |
| B11 | Without 1982 | +0.26 (0.038) | +0.26 (0.019) | +0.19 (0.075) | −0.22 (0.038) | robustness |
| B12 | Without 1991 | +0.28 (0.038) | +0.31 (0.019) | +0.23 (0.057) | −0.30 (0.038) | robustness |
| B13 | Without 2009 | +0.14 (0.208) | +0.13 (0.226) | +0.06 (0.358) | −0.28 (0.057) | robustness |
| B14 | Without 2020 | +0.14 (0.208) | +0.11 (0.283) | +0.03 (0.434) | −0.18 (0.151) | robustness |
| B15 | Without 2009 and 2020 | +0.02 (0.377) | −0.02 (0.491) | −0.09 (0.717) | −0.20 (0.094) | robustness |
| B16 | Each of the 31 left out in turn (range) | +0.22 to +0.26 (0.019–0.075) | +0.22 to +0.25 (0.019–0.038) | +0.13 to +0.17 (0.170–0.208) | −0.27 to −0.24 (0.019–0.075) | robustness; after-2 reaches p < 0.05 with 20 of the 31 left out |
| B17 | Each added economy left out: CHN / BRA / SAU / IRN / RUS (p) | 0.057 / 0.038 / 0.019 / 0.038 / 0.038 | 0.019 / 0.019 / 0.038 / 0.019 / 0.019 | — | 0.038 / 0.019 / 0.038 / 0.019 / 0.057 | robustness (mandatory); without RUS = S30 |
| B18 | Norway, Switzerland, South Africa with GMD growth 1991–2011 | +0.24 (0.057) | +0.24 (0.019) | +0.16 (0.170) | −0.28 (0.038) | robustness (`S31_gmd_growth/P/arc`) |
| B19 | Lead-1 with past-only phases, each added economy left out: CHN / BRA / SAU / IRN / RUS | — | +0.357 (0.057) / +0.391 (0.038) / +0.403 (0.038) / +0.373 (0.038) / +0.369 (0.038) | — | — | robustness (`S31_minus_*/P/conventions`, C) |

B5–B7 (without the United States, Germany, Japan) are inside B16; on S31 lead-1 is p 0.019 in each.

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
| B19 | Lead-1 with past-only phases, each added economy left out: CHN / BRA / SAU / IRN | — | +0.345 (0.057) / +0.380 (0.038) / +0.394 (0.019) / +0.363 (0.038) | — | — | robustness (`S30_minus_*/P/conventions`, C); Appendix Table A1 |

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

Reading (all samples): the lead is carried by 2009 and 2020 (effective n ≈ 2, both modern); the post-crisis fall is
not robust to the band, to growth rates or to the phase convention, and on S31 sits on the 0.05 line; no single economy drives the lead.

## 3. Synchronization and swing size (Methods §6.2)

| ID | Quantity | S31 | S30 | S26 | Source | Status |
|---|---|---|---|---|---|---|
| C1 | corr(r, Ā), detrended (σ = 8 yr) | +0.646 (0.019; surrogate 0.0002) | +0.641 (0.019; surrogate 0.0002) | +0.608 (0.019; surrogate 0.0002, was 0.0006 with W surrogates) | `<sample>/P/amplitude` | headline |
| C2 | same, raw | +0.472 (0.019) | +0.458 (0.019) | +0.530 (0.019) | same | robustness |
| C3 | same, detrended, convention W (the "+0.51" of early drafts) | +0.566 (0.019; surrogate 0.0004) | +0.549 (0.019; surrogate 0.0008) | +0.509 (0.019; surrogate 0.0006) | `<sample>/W/amplitude` | robustness (issue 3, resolved) |
| C4 | same, convention N | +0.547 (0.019; surrogate 0.0008) | +0.535 (0.019; surrogate 0.0008) | +0.531 (0.019; surrogate 0.0006) | `<sample>/N/amplitude` | robustness |
| C5 | Two-stage timing: r peaks at t−1, amplitude at t0 | — | — | — | amplitude_results.json (epoch, S26 first run) | descriptive |
| C6 | same, convention E | +0.583 (0.019; surrogate 0.0002) | +0.577 (0.019; surrogate 0.0004) | +0.536 (0.019; surrogate 0.0006) | `<sample>/E/amplitude` | robustness |
| C7 | same, convention C (past data only) | +0.726 (0.019) | +0.723 (0.019) | +0.682 (0.019) | `<sample>/P/conventions` (C) | robustness |
| C8 | Without Iran / Saudi Arabia / both (detrended) | +0.650 / +0.625 / +0.625 (0.019 each; surrogate 0.0002) | +0.644 / +0.621 / +0.620 (0.019 each; surrogate 0.0002) | — | `S30_minus_*/P/amplitude` | robustness (mandatory) |
| C9 | Russia's phases from 1992 only (detrended; raw) | +0.655 (0.019); +0.478 (0.019) | — | — | `S31_rus_from_1992/P/amplitude` | robustness (circular shift only) |

## 4. What moves in a crisis (Methods §6.1, §7.6)

| ID | Quantity | S31 | S30 | S26 | Source | Status |
|---|---|---|---|---|---|---|
| D1 | Cross term's share of excess crisis variance, GDP-weighted (within-window mean weights, as the Methods state) | 84.3% | 83.3% | 80.2% (was 82.4%: four recessions, windows from 1970) | `<sample>/P/diversification` | headline (descriptive magnitude); the Results term is **loss of diversification** (Sid) |
| D2 | same with end-of-window weights (as-run script) | — | — | 82.6% (first run) | diversification_results.json | **flag** (issue 4); kept as the as-run record |
| D3 | same, equal-weighted | 97.0% | 96.8% | 96.5% (was 96.9%) | same | headline (descriptive) |
| D4 | Cross share of world variance, crisis vs normal windows: GDP-weighted / equal | 0.706 vs 0.620 / 0.783 vs 0.691 | 0.707 vs 0.619 / 0.771 vs 0.671 | 0.704 vs 0.646 / 0.876 vs 0.817 (was 0.723 vs 0.669 / 0.880 vs 0.818) | same | descriptive |
| D5 | Surrogate p printed on figures for the crisis cross share | 0.0002 | 0.0002 | 0.0002 | same | **flag** (issue 6): tests only "are economies correlated at all" |
| D6 | Disclosure: nominal p of the share ratio, GDP / equal; Δcross; Δown | 0.32 / 0.48; 0.0002 both; 0.038 GDP, 0.0002 equal | 0.32 / 0.47; 0.0002 both; 0.035 GDP, 0.0002 equal | 0.34 / 0.48; all 0.0002 (Methods: 0.35 / 0.48) | same (`d6`) | disclosure |
| D7 | Inside the cross term's rise, GDP-weighted: correlation / swing size / interaction | 46% / 40% / 14% | 44% / 41% / 15% | 33% / 53% / 14% (was 35 / 50 / 14%) | `<sample>/P/cross_split` | headline (correction). Results: "co-movement and larger swings contribute about equally"; "amplification transmitted by alignment" only as Discussion interpretation (Sid) |
| D8 | same, equal-weighted | 50% / 37% / 13% | 49% / 38% / 13% | 39% / 49% / 12% (was 41 / 46 / 13%) | same | headline (correction) |
| D9 | Mean pairwise correlation, normal → crisis windows; mean cycle s.d. ratio | 0.291 → 0.385; × 1.10 | 0.294 → 0.392; × 1.11 | 0.351 → 0.441; × 1.13 (was 0.376 → 0.490; × 1.14) | same | descriptive |
| D10 | Fibrillation identity \|Z\| = Ā × R_A, max error | below 10⁻¹⁸ (machine rounding) | below 10⁻¹⁸ (machine rounding) | below 10⁻¹⁸ (machine rounding) | `<sample>/P/structure` | descriptive |
| D11 | Share of the crisis excess in log world swing² from alignment / from swing size (surrogate p) | 28.5% / 71.5% (0.239 / 0.0002) | 18.9% / 81.1% (0.356 / 0.0002) | 39.3% / 60.7% (0.103 / 0.0002) | same | **descriptive, sample-sensitive** (Sid): reported as S26 39.3%, S30 18.9%, S30 without Iran 33.0%, S31 28.5% (D13); Results builds nothing on it |
| D12 | corr(R_A, r) | +0.891 | +0.886 | +0.942 | same | descriptive |
| D13 | Without Iran / Saudi Arabia / both: D1; D3; D7; D11 alignment share | 84.0 / 83.8 / 83.5%; 96.7 / 97.3 / 97.0%; 44/42/14, 45/41/14, 43/43/14%; 38.3 / 28.6 / 41.4% | 83.0 / 82.9 / 82.5%; 96.5 / 97.1 / 96.8%; 42/43/15, 43/42/15, 41/44/15%; 33.0 / 17.4 / 37.4% | — | `S30_minus_*/P/` | robustness (mandatory) |
| D14 | Windows kept inside 1970–2022 (four recessions): D1 / D3 | 86.8% / 96.9% | 85.9% / 96.7% | 82.4% / 96.9% (the first-run values) | `<sample>_strict/P/diversification` | robustness |

## 5. Network geometry and phase structure (Methods §6.5–6.6, §7.7)

| ID | Quantity | S31 | S30 | S26 | Source | Status |
|---|---|---|---|---|---|---|
| E1 | MST mean edge length, decade means 1979–89 vs 2013–22 (same with windows from 1962 or from 1970) | 0.687 vs 0.424 (1.6×) | 0.680 vs 0.421 (1.6×) | 0.677 vs 0.379 (1.8×) | `<sample>/P/mst` | headline (descriptive); replaces 0.706 vs 0.379 (1.9×) |
| E2 | Single-year endpoints 1971 vs 2022 (the old "~3×") | — | — | 0.781 vs 0.249 | mst_results.json | dropped (Sid, 11 Oct 2026); Methods' 0.771 matched no result |
| E3 | Windows kept inside 1970–2022: L from 1979; decade means unchanged | 0.687 vs 0.424 | 0.680 vs 0.421 | 0.677 vs 0.379 | `<sample>_strict/P/mst` | robustness; replaces 0.652, which was L(1979) alone |
| E4 | Pre-crisis MST contraction, Kendall τ, raw; detrended (σ = 8) | −0.157 (0.206); +0.014 (0.561) | −0.143 (0.219); +0.057 (0.659) | −0.171 (0.168, was 0.167); −0.057 (0.356) | `<sample>/P/mst` | null; the first-run detrended −0.086 (0.316) does not reproduce (issue 23) |
| E4s | same, windows inside 1970–2022 (1991, 2009, 2020) | +0.095 (0.654); +0.333 (0.910) | +0.119 (0.692); +0.381 (0.936) | +0.000 (0.504); +0.167 (0.740) | `<sample>_strict/P/mst` | null |
| E5 | The old "p = 0.47" for E4 | — | — | not reproducible | — | do not cite |
| E6 | Largest-eigenvalue fragility trend | τ +0.129 (0.271) | τ +0.086 (0.338) | τ +0.100 (0.311, was 0.306) | `<sample>/P/mst` | null |
| E7 | Phase-lead spread (s.d. of the leads), lower tail | 0.546 yr (0.0002; surrogate mean 0.992, min 0.554) | 0.535 yr (0.0004; surrogate mean 0.988, min 0.523) | 0.445 yr (0.0002; surrogate mean 0.949, min 0.456); was 0.403 under W | `<sample>/P/phase_lags` | headline |
| E8 | Upper-tail p stored by the first run | 1.0 | 1.0 | 1.0 | same (`p_spread_upper_as_run`) | resolved (issue 8): the lower tail is now stored |
| E9 | Mean cycle period | 5.93 yr | 5.95 yr | 5.98 yr (was 5.85, W) | same | descriptive |
| E10 | Fiedler split of the correlation network: λ2; blocs | 0.838; A = USA, GBR, DEU, FRA, ITA, CAN, ESP, AUS, MEX, NLD, SWE, CHE, BEL, ZAF, AUT, FIN, GRC, PRT, BRA; B = JPN, KOR, IND, TUR, NOR, DNK, IDN, THA, CHN, SAU, IRN, RUS | 0.834; A = USA, GBR, JPN, KOR, IND, TUR, NOR, DNK, IDN, THA, CHN, IRN; B = the other 18 | 0.868; A = GBR, FRA, JPN, KOR, IND, ZAF, IDN, THA; B = the other 18 | `<sample>/P/structure` | descriptive |
| E11 | Arc within blocs / between blocs: lead-1 | +0.25 (0.019) / +0.07 (0.358) | +0.21 (0.019) / +0.13 (0.151) | +0.18 (0.057) / +0.18 (0.038) | same | exploratory |

## 6. Tipping tests (Methods §6.7)

Pre-crisis windows used (15-year windows from 1962): 1982 (six of eight years defined), 1991, 2009, 2020; 1975 has
none. Coupling test: after all five recessions.

| ID | Quantity | S31 | S30 | S26 | Source | Status |
|---|---|---|---|---|---|---|
| F1 | Pre-crisis trend of the lag-1 autocorrelation of r(t) | τ −0.152 (0.789) | τ −0.098 (0.676) | τ +0.027 (0.456); was −0.152 (0.757) under W | `<sample>/P/csd` | null |
| F2 | Pre-crisis trend of the variance of r(t) | τ +0.438 (0.031) | τ +0.420 (0.037) | τ +0.438 (0.033); was +0.295 (0.107) under W | same | **reported as it is** (Sid, 11 Oct 2026): rising variance without rising autocorrelation, so not the slowing-down signature; presented as consistent with loss of diversification (shocks stop cancelling), an interpretation; rests on 2009 and 2020 (F2b) |
| F2b | F2 by recession (not pre-registered): without 2009 and 2020; 2009 and 2020 alone; without 2009; without 2020 | +0.018 (0.514); +0.857 (0.003); +0.274 (0.206); +0.321 (0.125) | −0.018 (0.528); +0.857 (0.005); +0.274 (0.200); +0.274 (0.176) | +0.125 (0.408); +0.750 (0.019); +0.369 (0.123); +0.298 (0.154) | `followup/<sample>/P/csd_by_event`; `results/FOLLOWUP.md` | exploratory (Sid asked for it after Phase 3) |
| F2c | F2 under W / N / E | +0.259 (0.135) / +0.393 (0.073) / +0.402 (0.045) | +0.295 (0.113) / +0.393 (0.075) / +0.384 (0.054) | +0.295 (0.107) / +0.369 (0.091) / +0.420 (0.041) | `<sample>/{W,N,E}/csd` | robustness; under E significant on S26 and S31, not S30 |
| F2s | F1 / F2 with windows inside 1970–2022 (2009 and 2020 only) | −0.107 (0.644) / +0.857 (0.003) | −0.036 (0.550) / +0.857 (0.005) | −0.071 (0.595) / +0.750 (0.019) | `<sample>_strict/P/csd` | robustness |
| F3 | Restoring time (third indicator) | — | — | — | — | dropped (Sid, 11 Oct 2026): as 1/(−ln φ) it is a monotone function of the lag-1 autocorrelation, so not independent (issue 22) |
| F4 | Post-crisis change in recovery rate λ (coupling as bifurcation parameter) | +0.002 (0.502) | +0.024 (0.507) | +0.078 (0.534); was +0.098 (0.542) under W | `<sample>/P/bifurcation` | null |
| F4s | same, windows inside 1970–2022 (1982–2020) | +0.065 (0.520) | +0.102 (0.530) | +0.182 (0.578) | `<sample>_strict/P/bifurcation` | null |
| F5 | Implied K/K_c around onsets, mean t−1 / t0 | 4.0 / 3.5 | 4.0 / 4.6 | 5.6 / 6.7; was 6.4 / 7.1 under W | `<sample>/P/bifurcation` | descriptive (a transform of r) |

## 7. Channels inside the economies (Global Macro Database on the repaired atlas panel, not Maddison)

An economy enters a channel only with continuous data 1965–2022 (amendment 1.5); counts in brackets.

| ID | Quantity | S31 | S30 | S26 | Source | Status |
|---|---|---|---|---|---|---|
| G1 | Short-rate synchronization, lead-2 | +0.273 (0.019) [19; Russia has no rates before 1997] | +0.273 (0.019) [19] | +0.266 (0.019) [18] | `<sample>/P/channels` (`sync`) | **description only** (Sid, 11 Oct 2026): fails past-only phases (G1C), so not a lead claim |
| G1C | same, past data only | +0.165 (0.151) | +0.165 (0.151) | +0.151 (0.170) | `<sample>/C/channels` | the rule-7 test (issue 14): fails |
| G2 | Investment synchronization, lead-2; past data only | +0.270 (0.038) [28]; −0.110 (0.717) | +0.270 (0.038) [28]; −0.110 (0.717) | +0.293 (0.038) [26]; −0.085 (0.642) | same | description only: fails past-only phases |
| G3 | Real GDP (GMD, not per capita) synchronization, lead-1 / after-2; past-only lead-1 | +0.254 (0.019) / −0.320 (0.019) [30, with Russia]; +0.319 (0.038) | +0.245 (0.019) / −0.291 (0.019) [29]; +0.311 (0.057) | +0.237 (0.019) / −0.332 (0.019) [26]; +0.278 (0.057) | same | robustness of A2/A5 on other data; past-only lead-1 holds on S31 (p 0.038), just misses on S30 and S26 (0.057) |
| G3o | Channel order, two-sided phases: short rates peak at lead-2, investment at lead-2 and lead-1 (+0.270, +0.262), real GDP at lead-1 | — | — | — | same | descriptive only (Sid) |
| G4 | Channel synchronization above surrogate chance, all nine channels | mean r 0.33–0.61 vs null 0.16–0.30 | mean r 0.33–0.61 vs null 0.17–0.30 | mean r 0.34–0.64 vs null 0.17–0.30 (was null 0.17–0.25) | `<sample>/P/channels` (`anatomy`) | descriptive; p 0.0005 each (the floor with 2,000 surrogates) |
| G5 | Mean pairwise cycle correlation before/after 1990: GDP, exports, imports, budget balance | 0.20→0.50, 0.27→0.57, 0.36→0.55, 0.19→0.59 | 0.20→0.51, 0.27→0.57, 0.36→0.55, 0.19→0.59 | 0.23→0.58, 0.30→0.60, 0.39→0.61, 0.19→0.59 (was GDP 0.22→0.58, balance 0.09→0.56) | same | descriptive |
| G5b | Budget channels (spending, balance) on the repaired panel | the same 9 (Russia's budget series start in 1998) | 9 economies: USA, JPN, CAN, KOR, IND, ZAF, NOR, GRC, THA | same 9 (was 26 on the raw data) | same | **note**: most repaired spending series start after 1965 and fail the coverage rule |
| G6 | US–Japan cycle correlation 1961–89 → 1990–2019: exports, imports, investment, GDP | — | — | 0.36→0.73, 0.47→0.64, 0.08→0.43, 0.32→0.44 | printed/usjp_output.txt | descriptive (not rerun: two economies) |
| G7 | Economies contracting in 1975, 1982, 1991, 2009, 2020 | 14, 9, 9, 25, 28 of 31 | 13, 9, 8, 24, 27 of 30 | 11, 8, 8, 22, 25 of 26 | same (`contracting`) | descriptive |
| G8 | Average coupling to the rest of the sample, 1970–89 vs 1990–2022 | 0.43 vs 0.70 | 0.43 vs 0.70 | 0.46 vs 0.75 | same (`coupling`) | descriptive |

## 8. Superseded explorations (history only)

| ID | Quantity | Value | p | Source |
|---|---|---|---|---|
| H1 | Current-dollar GDP, hand-picked windows: mean R global / regional / normal; contrast | 0.75 / 0.45 / 0.67; +0.103 | 0.038 (20,000 placements) | crisis_results.json |
| H2 | Real GDP, hand-picked windows: same | 0.70 / 0.30 / 0.52; +0.202 | 0.020 | crisis_results_real.json |
| H3 | JST banking crises (17 economies, 1970–2016): same year / lead-1 / lead-2 | +0.23 / +0.21 / +0.13 | 0.106 / 0.149 / 0.298 | crisis_dating_results.json (not re-verified) |
| H4 | First-pass surrogate test on current-dollar GDP: 2009 / 2020 | R 0.74 / 0.81 | 0.0002 / 0.0002 | surrogate_results.csv |

## 9. Edge-matched nulls (pre-registration amendment 4, 14 October 2026)

Each listed test's statistic with its current p and, after the arrow, its p against edge-matched surrogates (surrogates
with ends, passed through the same band-pass and Hilbert transform; 5,000, floor 0.0002; multivariate for the arcs,
independent otherwise). **Bold**: the two fall on opposite sides of 0.05. The current p-values above are unchanged.
Validation on the G1 worlds and the reading of each crossing: `results/EDGE_MATCHED.md`.

| ID | Test | S31 | S30 | S26 | Source | Status |
|---|---|---|---|---|---|---|
| X1 | Arc, lead-1, convention P (A2) | +0.231 (0.019 → 0.033) | +0.217 (0.019 → 0.043) | +0.216 (0.019 → 0.042) | `edge_matched/<sample>.json` (`arc.P.lead1`) | second null |
| X2 | Arc, crisis year, convention P (A3) | +0.159 (0.189 → 0.116) | +0.161 (0.189 → 0.108) | +0.149 (0.189 → 0.123) | `edge_matched/<sample>.json` (`arc.P.crisis`) | second null |
| X3 | Arc, after-1, convention P (A4) | +0.099 (0.717 → 0.760) | +0.111 (0.755 → 0.786) | +0.078 (0.679 → 0.707) | `edge_matched/<sample>.json` (`arc.P.after1`) | second null |
| X4 | Arc, after-2, convention P (A5) | -0.258 (0.057 → **0.039**) | -0.236 (0.057 → 0.054) | -0.277 (0.019 → 0.026) | `edge_matched/<sample>.json` (`arc.P.after2`) | second null |
| X5 | Arc, lead-1, convention W (A10) | +0.204 (0.019 → **0.056**) | +0.184 (0.057 → 0.079) | +0.178 (0.094 → 0.085) | `edge_matched/<sample>.json` (`arc.W.lead1`) | second null |
| X6 | Arc, crisis year, convention W (A10) | +0.134 (0.189 → 0.161) | +0.130 (0.226 → 0.167) | +0.112 (0.208 → 0.198) | `edge_matched/<sample>.json` (`arc.W.crisis`) | second null |
| X7 | Arc, after-1, convention W (A10) | +0.109 (0.774 → 0.784) | +0.121 (0.774 → 0.806) | +0.088 (0.698 → 0.734) | `edge_matched/<sample>.json` (`arc.W.after1`) | second null |
| X8 | Arc, after-2, convention W (A10) | -0.165 (0.113 → 0.142) | -0.131 (0.170 → 0.204) | -0.144 (0.170 → 0.177) | `edge_matched/<sample>.json` (`arc.W.after2`) | second null |
| X9 | Arc, lead-1, convention N (A11) | +0.192 (0.057 → 0.071) | +0.173 (0.094 → 0.093) | +0.178 (0.094 → 0.083) | `edge_matched/<sample>.json` (`arc.N.lead1`) | second null |
| X10 | Arc, crisis year, convention N (A11) | +0.135 (0.208 → 0.156) | +0.133 (0.189 → 0.158) | +0.124 (0.189 → 0.168) | `edge_matched/<sample>.json` (`arc.N.crisis`) | second null |
| X11 | Arc, after-1, convention N (A11) | +0.105 (0.755 → 0.775) | +0.116 (0.774 → 0.800) | +0.089 (0.679 → 0.737) | `edge_matched/<sample>.json` (`arc.N.after1`) | second null |
| X12 | Arc, after-2, convention N (A11) | -0.190 (0.094 → 0.101) | -0.158 (0.132 → 0.151) | -0.197 (0.094 → 0.088) | `edge_matched/<sample>.json` (`arc.N.after2`) | second null |
| X13 | Arc, lead-1, convention E (A12) | +0.236 (0.019 → 0.029) | +0.226 (0.019 → 0.037) | +0.220 (0.019 → 0.038) | `edge_matched/<sample>.json` (`arc.E.lead1`) | second null |
| X14 | Arc, crisis year, convention E (A12) | +0.159 (0.189 → 0.110) | +0.164 (0.170 → 0.103) | +0.152 (0.170 → 0.118) | `edge_matched/<sample>.json` (`arc.E.crisis`) | second null |
| X15 | Arc, after-1, convention E (A12) | +0.101 (0.755 → 0.780) | +0.107 (0.755 → 0.794) | +0.075 (0.717 → 0.719) | `edge_matched/<sample>.json` (`arc.E.after1`) | second null |
| X16 | Arc, after-2, convention E (A12) | -0.160 (0.132 → 0.090) | -0.136 (0.170 → 0.120) | -0.170 (0.113 → 0.080) | `edge_matched/<sample>.json` (`arc.E.after2`) | second null |
| X17 | Arc within the Fiedler blocs, lead-1 (E11) | +0.250 (0.019 → 0.023) | +0.212 (0.019 → **0.050**) | +0.182 (0.057 → 0.082) | `edge_matched/<sample>.json` (`E11.within.lead1`) | second null |
| X18 | Arc between the Fiedler blocs, lead-1 (E11) | +0.066 (0.358 → 0.354) | +0.135 (0.151 → 0.152) | +0.180 (0.038 → 0.025) | `edge_matched/<sample>.json` (`E11.between.lead1`) | second null |
| X19 | Real-GDP channel arc, lead-1 (G3) | +0.254 (0.019 → 0.020) | +0.245 (0.019 → 0.023) | +0.237 (0.019 → 0.025) | `edge_matched/<sample>.json` (`G3.lead1`) | second null |
| X20 | Real-GDP channel arc, crisis year (G3) | +0.208 (0.094 → **0.046**) | +0.202 (0.094 → **0.050**) | +0.192 (0.094 → 0.061) | `edge_matched/<sample>.json` (`G3.same`) | second null |
| X21 | Real-GDP channel arc, after-2 (G3) | -0.320 (0.019 → 0.018) | -0.291 (0.019 → 0.029) | -0.332 (0.019 → 0.015) | `edge_matched/<sample>.json` (`G3.after2`) | second null |
| X22 | Cross share at recessions, GDP weights (D5) | +0.706 (0.0002 → 0.0002) | +0.707 (0.0002 → 0.0002) | +0.704 (0.0002 → 0.0002) | `edge_matched/<sample>.json` (`D5.gdp_mean`) | second null |
| X23 | Cross share at recessions, equal weights (D5) | +0.783 (0.0002 → 0.0002) | +0.771 (0.0002 → 0.0002) | +0.876 (0.0002 → 0.0002) | `edge_matched/<sample>.json` (`D5.equal`) | second null |
| X24 | Share of the excess from the cross term, GDP weights (D6) | +0.843 (0.316 → 0.319) | +0.833 (0.319 → 0.313) | +0.802 (0.344 → 0.349) | `edge_matched/<sample>.json` (`D6.ratio.gdp_mean`) | second null |
| X25 | Share of the excess from the cross term, equal weights (D6) | +0.970 (0.478 → 0.476) | +0.968 (0.466 → 0.459) | +0.965 (0.476 → 0.466) | `edge_matched/<sample>.json` (`D6.ratio.equal`) | second null |
| X26 | Δcross at recessions, GDP weights (D6) | +4.17e-05 (0.0002 → 0.0002) | +4.48e-05 (0.0002 → 0.0002) | +5.72e-05 (0.0002 → 0.0002) | `edge_matched/<sample>.json` (`D6.cross.gdp_mean`) | second null |
| X27 | Δcross at recessions, equal weights (D6) | +4.72e-05 (0.0002 → 0.0002) | +4.97e-05 (0.0002 → 0.0002) | +5.22e-05 (0.0002 → 0.0002) | `edge_matched/<sample>.json` (`D6.cross.equal`) | second null |
| X28 | Δown at recessions, GDP weights (D6) | +7.78e-06 (0.038 → **0.053**) | +8.96e-06 (0.035 → 0.047) | +1.41e-05 (0.0002 → 0.0002) | `edge_matched/<sample>.json` (`D6.own.gdp_mean`) | second null |
| X29 | Δown at recessions, equal weights (D6) | +1.46e-06 (0.0002 → 0.0004) | +1.65e-06 (0.0002 → 0.0004) | +1.88e-06 (0.0002 → 0.0002) | `edge_matched/<sample>.json` (`D6.own.equal`) | second null |
| X30 | Identity: alignment at recessions (D11) | +0.406 (0.239 → 0.228) | +0.241 (0.356 → 0.355) | +0.654 (0.103 → 0.105) | `edge_matched/<sample>.json` (`D11.align`) | second null |
| X31 | Identity: swing size at recessions (D11) | +1.021 (0.0002 → 0.0002) | +1.033 (0.0002 → 0.0002) | +1.010 (0.0002 → 0.0002) | `edge_matched/<sample>.json` (`D11.swing`) | second null |
| X32 | MST contraction before recessions (E4) | -0.157 (0.206 → 0.185) | -0.143 (0.219 → 0.216) | -0.171 (0.168 → 0.166) | `edge_matched/<sample>.json` (`E4.raw`) | second null |
| X33 | MST contraction, detrended (E4) | +0.014 (0.561 → 0.524) | +0.057 (0.659 → 0.624) | -0.057 (0.356 → 0.338) | `edge_matched/<sample>.json` (`E4.detrended`) | second null |
| X34 | MST fragility before recessions (E6) | +0.129 (0.271 → 0.252) | +0.086 (0.338 → 0.336) | +0.100 (0.311 → 0.299) | `edge_matched/<sample>.json` (`E6`) | second null |
| X35 | Slowing down: autocorrelation of r (F1) | -0.152 (0.789 → 0.770) | -0.098 (0.676 → 0.678) | +0.027 (0.456 → 0.456) | `edge_matched/<sample>.json` (`F1`) | second null |
| X36 | Slowing down: variance of r (F2) | +0.438 (0.031 → 0.029) | +0.420 (0.037 → 0.037) | +0.438 (0.033 → 0.036) | `edge_matched/<sample>.json` (`F2`) | second null |
| X37 | Slower recovery after recessions (F4) | +2.26e-03 (0.502 → 0.478) | +0.024 (0.507 → 0.488) | +0.078 (0.534 → 0.517) | `edge_matched/<sample>.json` (`F4`) | second null |
| X38 | r with swing size, detrended (outside the rule) (C1) | +0.646 (0.0002 → 0.0002) | +0.641 (0.0002 → 0.0002) | +0.608 (0.0002 → 0.0006) | `edge_matched/<sample>.json` (`C1`) | second null |
