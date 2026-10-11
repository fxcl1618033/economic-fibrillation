# Open issues — Paper 1 (as of 11 October 2026)

Ordered by how much they could change what the paper says. Each has the evidence, what to do and who decides.
"Sid decides" means: prepare the numbers, explain the trade-off in plain words, and wait. Figure file names such as
`mst_network.pdf` are the original files in `figures/_sources/analysis/`; their IDs (F5.1 and so on) and category
copies are listed in `docs/FIGURES.md`.

---

## 1. The crisis arc depends on where the Hilbert transform is applied — CRITICAL

**Evidence** (`tools/check_runin_conventions.py`, `paper1/results/runin_convention_check.json`). Same data, filter and
permutation test; correlation of r(t) with the recession indicator, one-sided p in brackets:

| Convention | Lead-2 | Lead-1 | Crisis | After-1 | After-2 | r–Ā detrended |
|---|---|---|---|---|---|---|
| **P** · filter and Hilbert on 1950–2022, keep 1970–2022 (paper; `kose_terrones_test.py`) | +0.230 (0.038) | +0.216 (0.019) | +0.149 (0.189) | +0.078 (0.679) | −0.277 (0.019) | +0.608 |
| **W** · filter from 1950, Hilbert on 1970–2022 only (`amplitude_test.py`, companion figures) | +0.210 (0.057) | +0.178 (0.094) | +0.112 (0.208) | +0.088 (0.698) | −0.144 (0.170) | +0.509 |
| **N** · filter and Hilbert on 1970–2022 only | +0.210 (0.038) | +0.178 (0.094) | +0.124 (0.189) | +0.089 (0.679) | −0.197 (0.094) | +0.531 |

The lead-1 and after-2 results are significant under P only. Methods §1 and §7.2 already argue for P (run-in protects
1970 from edge transients) and disclose that the run-in moves the amplitude coefficient, but they do not say that it
moves the arc. The amplitude link survives every convention; the arc does not.

**Which scripts use which convention.** P: `kose_terrones_test.py`, `robustness.py`, `real_gdp_analysis.py`,
`structure_tests.py`, `panel26.py`. W: `amplitude_test.py`, `phase_lags.py` (so the 0.403-year phase-lead spread is a
W number) and the r(t) used for `corr_rbar_r` in `diversification*.py`. Hilbert on 1962–2022 (eight years of run-in):
`csd_surrogate.py`, `kuramoto_bifurcation.py`. No Hilbert transform at all: the variance decomposition and
`mst_network.py` (band-passed cycles only, so issue 1 does not touch them). The rerun must compute every test under
one stated convention and report the others as sensitivity.

**Why it happens.** The Hilbert transform is computed with an FFT over the whole series it is given, so its edge
errors depend on where that series starts and ends, and they leak a few years inward. P gives the 1970s twenty years
of run-in; W and N do not.

**What to do.** (a) Keep P as the stated convention but report W and N beside it in Results and add one sentence to
Methods §7.2. (b) Add an edge-robust variant (for example mirror-padding the cycle before the Hilbert transform, or a
causal phase estimate) and report it too. (c) Fix the convention before running anything on the 30 economies, and
write that decision down first (`docs/decisions.md`). **Sid decides** the wording; the numbers are not in doubt.

## 2. The end of the sample is edge-affected in every convention — HIGH

2020 sits two years from the last observation (2022), and the after-2 test for 2020 uses r(2022), the very last
point. Both the forward–backward filter and the Hilbert transform are least reliable there, and leave-one-crisis-out
shows the lead rests on 2009 and 2020. **What to do:** report the arc with 2020 excluded beside the full result
(row B14 of the registry already does this for the lead), add the edge-robust variant from issue 1, and say plainly
in Limitations that the most recent event is the least well measured. When data for 2023–2025 are available, extend
the series and re-test: that is the cleanest fix.

## 3. "+0.51 vs +0.608" for the amplitude link — RESOLVED, needs a text update

`amplitude_test.py` applies the Hilbert transform to 1970–2022 only (convention W), which gives +0.509. The paper's
convention P gives +0.608; N gives +0.531. Methods §8 says "we were unable to recover the exact amplitude convention
behind the earlier figures": it can now say which convention it was. Every "+0.51" in drafts, the companion book
(figure A8) and `amplitude.pdf` (F4.1) is the W value.

## 4. Diversification weights: Methods and script differ — LOW

Methods §6.1 says GDP weights are the within-window mean of real GDP and reports 82.4% (cross shares 0.723 and 0.669);
that reproduces exactly. `diversification.py` weights each window by its last year and gives 82.6% (0.724 and 0.668).
**What to do:** make the code match the Methods text; quote 82.4%.

## 5. "Correlation events, not volatility events" is wrong — MEDIUM (wording)

The cross term supplies 82–97% of the excess crisis variance, but inside the cross term's rise, bigger swings
contribute 46–50%, higher correlation 35–41% and their interaction 13–14% (`printed/crossterm_split_output.txt`). The
fibrillation identity says the same from another angle: 61% of the crisis excess in world swing comes from swing size,
39% from alignment. Defensible phrase: **amplification transmitted by alignment**. Places still carrying the old claim:
the titles of `diversification.pdf` and `diversification_compare.pdf` (F4.4, F4.5), the two companion versions (F4.6,
F4.7), the companion sentence "the danger is not that anyone panics harder in a crisis. It is that everyone stops
cancelling one another out", and any abstract draft that says crises are "correlation events, not volatility events".
Methods §6.1 itself does not use the slogan but should add the split so readers do not take "cross term" to mean
"correlation".

## 6. The diversification surrogate p = 0.0002 on figures is not a test of the claim — MEDIUM

It compares the crisis cross share with phase-randomized (uncorrelated) economies, so it only shows the economies are
correlated at all. Methods §6.1 and §7.6 already say the share statistic has no proper null. Remove the p from the
figures when they are redrawn.

## 7. Network figure annotations — LOW

`mst_network.pdf` (F5.1) prints "~3× tighter" (single-year endpoints; decade means give 1.9×) and "p = 0.47" for
pre-crisis contraction (not reproducible; stored τ = −0.171, p = 0.167 raw; τ = −0.086, p = 0.316 detrended). Redraw.

## 8. Phase-lag p stored as the upper tail — LOW

`phase_lags.py` stores p_spread = 1.0 (upper tail). The intended lower-tail p is 0.0002 (observed 0.403 years, every
one of 5,000 surrogates larger). Fix the script; the Methods already reports the right value.

## 9. `robustness.py` saves only the baseline — LOW

Band, detrending, leave-one-economy-out, split-sample and leave-one-crisis-out results exist only as printed text
(`paper1/results/printed/robustness_output.txt`). Save them as JSON in the rerun.

## 10. The restoring-time indicator was lost — LOW

`csd_fast.py` (the third critical-slowing-down indicator) and its figure were lost with the September workspace;
Methods §6.7 reports it as null. Rebuild it in the rerun so all three indicators come from code in the repository.

## 11. Lay companion book is internally inconsistent — MEDIUM (it is in people's hands)

Its arc figure (A7, F2.9) was drawn with convention W and shows no bar below p = 0.05, while its text says the rise
and collapse are significant. Figures A5, A6 and A8 are also convention W, and figure A4 (F1.4, "far more
synchronized than chance") draws an r(t) that matches no stored series. **What to do:** redraw A4–A8 with
convention P (and say in one plain sentence that the most recent crisis carries the result), fix the diversification
sentence in issue 5, then re-export the PDF and Word file. **Sid decides** whether to send a corrected copy.

## 12. Imports and budget-spending channels predate the data repairs — MEDIUM

`panel26.py` (the channel anatomy, F7.2) reads the raw Global Macro Database. The atlas later repaired budget
splices, debt splices, net exports and money breaks (`atlas/meta.json`, "fixes"). Rerun the channel anatomy on the
repaired panel, especially imports and budget spending, and report any change.

## 13. Maddison growth for Norway, Switzerland and South Africa — MEDIUM

For 1991–2011, the atlas comparison found Maddison's per-capita growth for these three running 2–3 percentage
points above national-accounts growth.
Robustness run: swap in GMD (national accounts) real GDP per capita for these three and rerun the arc, the amplitude
link and the decomposition.

## 14. The two-year rate lead needs past-only phases — HIGH for the channel claim and for any GNN

The band-pass and Hilbert transform both use future data, so a lead found with them can partly come from the future.
Re-test G1 (short rates lead recessions by two years, p = 0.019) with phases built only from data available at each
date (a one-sided filter, or re-estimating phases on an expanding window). Report both.

## 15. Citations to fix

- Ikeda, Aoyama and Yoshikawa on international synchronization is RIETI Discussion Paper 13-E-089; arXiv 1110.6679
  is Ikeda et al. (2011) on Japanese industrial sectors.
- Kose–Terrones global recessions: cite the dating source (Kose, Sugawara and Terrones 2020, World Bank Policy
  Research Working Paper 9172, and the 2015 IMF book *Collapse and Revival* by Kose and Terrones). Check the exact
  references before the paper goes out.
- Methods §8: cite the Maddison commit and file checksum from `data/sources.yaml`, not only the package version
  (1.1.0 then, 1.1.1 now; the data file is unchanged).

## 16. Banking-crisis history not re-verified — LOW

`crisis_dating_test.py` needs `jst.xlsx`, which was never pinned. GMD carries `data/clean/aggregators/JST/JST.dta`
(pinned) as a likely replacement. History only; no paper claim depends on it.

## 17. Sample definition — DECIDED 11 October 2026

**Decision (Sid):** S30 is the main sample for Paper 1 and the GNN; no S31 run, because the UAE's 1991–92 gap breaks the
filter. The inclusion rule below is now enforced in code (`src/ef/data/maddison.py`) and reported per economy in
`docs/data_validation.md` (`make data`). **Mandatory in Phase 3 (Sid, 11 October 2026):** leave each of the four added
economies out in turn for every test, and report the amplitude link and the variance decomposition with and without
Iran and Saudi Arabia (their cycles are 2.9× and 2.2× the median size of the 26).


Working assumption: main sample S30 = the 26 + China, Brazil, Saudi Arabia and Iran; S26 is the frozen reference;
S31 (adding the UAE) is a sensitivity run only. Inclusion rule to state before any rerun: an economy enters if its
Maddison series is continuous over 1950–2022 with no interpolation or splices, and its national-accounts data pass the
atlas checks. First check (11 October, Maddison at the pinned commit): China, Brazil, Saudi Arabia and Iran are complete
for 1950–2022; the UAE is missing 1991 and 1992, so it fails the balanced-panel rule, which is a concrete reason to keep
it out of the main sample. Year-on-year moves above 15% are real events, not splices (China 1961, the Great Leap
famine; Saudi Arabia 1973, 1983 and 1991, oil; Iran 1978–80, the revolution), but they will dominate those economies'
cycles, so report the S30 results with each added economy left out in turn. The atlas found spliced GDP estimates in the Global Macro Database
for Saudi Arabia before 1970 and the UAE before 1975; Maddison's early Gulf figures are estimates too. Sid has not yet
answered the comment in the literature-review doc. **Sid decides.**

## 18. The Methods diagnostics figure does not exist in our files — LOW

`docs/methods.md` ends with a caption for a three-panel diagnostics figure (MST decade means, phase-lag null,
corrected p-values). It was described in Claude Science and never saved here. Draw it in the rerun.

## 19. Two different "real GDP" r(t) series — NOTE

The paper's r(t) uses Maddison GDP per capita. The atlas `sync.json` uses Global Macro Database real GDP (total). They
differ year by year (1970: 0.28 against 0.34). Keep them apart in the text; quote the Maddison series for Paper 1
claims and the GMD series only for the channel comparison.

## 20. Bonferroni value in Methods 7.4 is rounded twice — LOW (wording)

Found in Phase 2. Bonferroni over the five lags for lead-1 and after-2 is 5 × 1/53 = 0.0943, so "0.094"; Methods 7.4 and
registry A8 print 0.095 (5 × the rounded 0.019). Benjamini–Hochberg (0.047, 0.063) is right. **What to do:** propose the
corrected text in the Phase 3 text-changes file; Sid decides.

## 21. MST decade means in Methods 6.5 and 7.7 — MEDIUM (definition)

Found in Phase 2 (`src/ef/network.py`; the stored `mst_results.json` reproduces exactly). The Methods' 0.706 (1970s)
reproduces only if the 10-year windows may reach back into the 1950–69 run-in, so that 1970 counts (mean of 1970–79,
windows from 1961); but the same paragraph says L is defined only from 1971, where the 1971–79 mean is 0.696. The 7.7
value 0.652 (1979–89, windows inside 1970–2022) is not reproduced by any variant tried (0.669–0.679), and the single-year
endpoint 0.771 in 6.5 disagrees with the stored 0.781 (registry E2). 2013–2022 (0.379) and the 1.9× contrast are
unaffected in substance. **What to do:** fix one stated window convention in Phase 3, recompute all three numbers from
code, and propose the text; Sid decides.

## 22. The restoring-time indicator needs a definition that adds information — MEDIUM (issue 10 continued)

Phase 2 reconstructs it as 1/(−ln φ), the inverse of the recovery rate used in the bifurcation test. That is a
monotone function of the lag-1 autocorrelation φ, so its rank-based pre-crisis trend is the same as the autocorrelation's
(τ −0.152; surrogate p 0.769 against 0.757, the gap coming only from clipping). As defined it is not a third
indicator. **What to do:** before Phase 3, choose a definition that measures something else (for example the decay
time of r after its own deviations, fitted on levels, or the e-folding time of the windowed autocorrelation function
beyond lag 1), pre-register it, and report it beside the other two; Sid decides.
