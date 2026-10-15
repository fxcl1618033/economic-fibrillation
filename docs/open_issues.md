# Issues — Paper 1 (closed 15 October 2026)

**Every issue is closed.** Each is FIXED (with the commit), moved to LIMITATIONS (it is in the manuscript's
Limitations, `paper1/manuscript/06_limitations.md`) or moved to FUTURE WORK (`paper1/manuscript/07_future_work.md`).
Paper 1 is locked after G1b (`docs/decisions.md`): no new tests; anything new is Paper 2. The text recorded before
closing is kept under each item. Commit 62109da is the manuscript, the generated Methods and the redrawn figures.

| # | Issue | Status |
|---|---|---|
| 1 | The crisis arc depends on where the Hilbert transform is applied | FIXED + LIMITATIONS |
| 2 | The end of the sample is edge-affected in every convention | LIMITATIONS |
| 3 | "+0.51 vs +0.608" for the amplitude link | FIXED |
| 4 | Diversification weights: Methods and script differ | FIXED |
| 5 | "Correlation events, not volatility events" is wrong | FIXED + FUTURE WORK |
| 6 | The diversification surrogate p = 0.0002 on figures is not a test of the claim | FIXED |
| 7 | Network figure annotations | FIXED |
| 8 | Phase-lag p stored as the upper tail | FIXED |
| 9 | `robustness.py` saves only the baseline | FIXED |
| 10 | The restoring-time indicator was lost | FIXED |
| 11 | Lay companion book is internally inconsistent | FUTURE WORK |
| 12 | Imports and budget-spending channels predate the data repairs | FIXED |
| 13 | Maddison growth for Norway, Switzerland and South Africa | FIXED |
| 14 | The two-year rate lead needs past-only phases | FIXED + LIMITATIONS |
| 15 | Citations to fix | FIXED |
| 16 | Banking-crisis history not re-verified | FUTURE WORK |
| 17 | Sample definition | FIXED |
| 18 | The Methods diagnostics figure does not exist in our files | FIXED |
| 19 | Two different "real GDP" r(t) series | FIXED |
| 20 | Bonferroni value in Methods 7.4 is rounded twice | FIXED |
| 21 | MST decade means in Methods 6.5 and 7.7 | FIXED |
| 22 | The restoring-time indicator needs a definition that adds information | FIXED |
| 23 | The detrended pre-crisis MST trend does not reproduce | FIXED |
| 24 | Russia is not in the sample, and no reason is recorded | FIXED |
| 25 | What the G1 simulations say about four Paper 1 tests | FIXED + LIMITATIONS |

Figure file names such as `mst_network.pdf` are the original files in `figures/_sources/analysis/`; their IDs (F5.1 and
so on) and category copies are listed in `docs/FIGURES.md`.

---

## 1. The crisis arc depends on where the Hilbert transform is applied — **FIXED + LIMITATIONS**

**Resolution (15 October 2026).** FIXED: every test computed under P with W, N, E and C reported (Phase 3, 0617bf6; S31, b741410); the convention table is Methods §7.2 / manuscript Table 2 and Appendix Table A12 (62109da). The post-crisis fall and lead-1's failure under N go to LIMITATIONS ("The fall after recessions", "Phase conventions").

*As recorded before closing:*


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


## 2. The end of the sample is edge-affected in every convention — **LIMITATIONS**

**Resolution (15 October 2026).** LIMITATIONS ("The end of the sample"). Reported without 2020 (registry A14); edge-matched nulls run (amendment 4, 864317a / 83a86b4). Extending the data to 2023–2025 is FUTURE WORK.

*As recorded before closing:*


2020 sits two years from the last observation (2022), and the after-2 test for 2020 uses r(2022), the very last
point. Both the forward–backward filter and the Hilbert transform are least reliable there, and leave-one-crisis-out
shows the lead rests on 2009 and 2020. **What to do:** report the arc with 2020 excluded beside the full result
(row B14 of the registry already does this for the lead), add the edge-robust variant from issue 1, and say plainly
in Limitations that the most recent event is the least well measured. When data for 2023–2025 are available, extend
the series and re-test: that is the cleanest fix.


## 3. "+0.51 vs +0.608" for the amplitude link — **FIXED**

**Resolution (15 October 2026).** FIXED: the convention is known (W); Methods §8 now says so (62109da).

*As recorded before closing:*


`amplitude_test.py` applies the Hilbert transform to 1970–2022 only (convention W), which gives +0.509. The paper's
convention P gives +0.608; N gives +0.531. Methods §8 says "we were unable to recover the exact amplitude convention
behind the earlier figures": it can now say which convention it was. Every "+0.51" in drafts, the companion book
(figure A8) and `amplitude.pdf` (F4.1) is the W value.


## 4. Diversification weights: Methods and script differ — **FIXED**

**Resolution (15 October 2026).** FIXED: the rerun uses the Methods' within-window mean GDP weights (6ecf40c); 82.4% is reproduced by S26 with windows inside 1970–2022 (registry D14), and the paper quotes the S31 value 84.3% (62109da); F4.4 redrawn without the 82.6% label (62109da).

*As recorded before closing:*


Methods §6.1 says GDP weights are the within-window mean of real GDP and reports 82.4% (cross shares 0.723 and 0.669);
that reproduces exactly. `diversification.py` weights each window by its last year and gives 82.6% (0.724 and 0.668).
**What to do:** make the code match the Methods text; quote 82.4%.


## 5. "Correlation events, not volatility events" is wrong — **FIXED + FUTURE WORK**

**Resolution (15 October 2026).** FIXED: Methods and Results say "co-movement and larger swings contribute about equally" and "amplification transmitted by alignment" (62109da); F4.4 and F4.5 redrawn without the slogan (62109da). The companion-book versions (F4.6, F4.7) are FUTURE WORK with issue 11.

*As recorded before closing:*


The cross term supplies 82–97% of the excess crisis variance, but inside the cross term's rise, bigger swings
contribute 46–50%, higher correlation 35–41% and their interaction 13–14% (`printed/crossterm_split_output.txt`). The
fibrillation identity says the same from another angle: 61% of the crisis excess in world swing comes from swing size,
39% from alignment. Defensible phrase: **amplification transmitted by alignment**. Places still carrying the old claim:
the titles of `diversification.pdf` and `diversification_compare.pdf` (F4.4, F4.5), the two companion versions (F4.6,
F4.7), the companion sentence "the danger is not that anyone panics harder in a crisis. It is that everyone stops
cancelling one another out", and any abstract draft that says crises are "correlation events, not volatility events".
Methods §6.1 itself does not use the slogan but should add the split so readers do not take "cross term" to mean
"correlation".


## 6. The diversification surrogate p = 0.0002 on figures is not a test of the claim — **FIXED**

**Resolution (15 October 2026).** FIXED: F4.4 and F4.5 redrawn with no p-value (62109da); §7.6 says the share has no proper null.

*As recorded before closing:*


It compares the crisis cross share with phase-randomized (uncorrelated) economies, so it only shows the economies are
correlated at all. Methods §6.1 and §7.6 already say the share statistic has no proper null. Remove the p from the
figures when they are redrawn.


## 7. Network figure annotations — **FIXED**

**Resolution (15 October 2026).** FIXED: F5.1 redrawn on S31 with decade means (1.6×) and no "p = 0.47" (62109da).

*As recorded before closing:*


`mst_network.pdf` (F5.1) prints "~3× tighter" (single-year endpoints; decade means give 1.9×) and "p = 0.47" for
pre-crisis contraction (not reproducible; stored τ = −0.171, p = 0.167 raw; τ = −0.086, p = 0.316 detrended). Redraw.


## 8. Phase-lag p stored as the upper tail — **FIXED**

**Resolution (15 October 2026).** FIXED: the lower tail is stored (`p_spread_lower`, 6ecf40c); the Methods diagnostics figure F5.4 shows it (62109da).

*As recorded before closing:*


`phase_lags.py` stores p_spread = 1.0 (upper tail). The intended lower-tail p is 0.0002 (observed 0.403 years, every
one of 5,000 surrogates larger). Fix the script; the Methods already reports the right value.


## 9. `robustness.py` saves only the baseline — **FIXED**

**Resolution (15 October 2026).** FIXED: every robustness check is saved (`results/*/P/robustness.json`, 6ecf40c and 0617bf6); Appendix Tables A2–A3 (62109da).

*As recorded before closing:*


Band, detrending, leave-one-economy-out, split-sample and leave-one-crisis-out results exist only as printed text
(`paper1/results/printed/robustness_output.txt`). Save them as JSON in the rerun.


## 10. The restoring-time indicator was lost — **FIXED**

**Resolution (15 October 2026).** FIXED (dropped, issue 22): Sid's decision of 11 October 2026 (4872c0b); Methods §6.7 says why (62109da).

*As recorded before closing:*


`csd_fast.py` (the third critical-slowing-down indicator) and its figure were lost with the September workspace;
Methods §6.7 reports it as null. Rebuild it in the rerun so all three indicators come from code in the repository.


## 11. Lay companion book is internally inconsistent — **FUTURE WORK**

**Resolution (15 October 2026).** FUTURE WORK: the companion book is outside the paper. Redrawing A4–A8 under convention P and fixing the diversification sentence waits for Sid's decision on whether to send a corrected copy.

*As recorded before closing:*


Its arc figure (A7, F2.9) was drawn with convention W and shows no bar below p = 0.05, while its text says the rise
and collapse are significant. Figures A5, A6 and A8 are also convention W, and figure A4 (F1.4, "far more
synchronized than chance") draws an r(t) that matches no stored series. **What to do:** redraw A4–A8 with
convention P (and say in one plain sentence that the most recent crisis carries the result), fix the diversification
sentence in issue 5, then re-export the PDF and Word file. **Sid decides** whether to send a corrected copy.


## 12. Imports and budget-spending channels predate the data repairs — **FIXED**

**Resolution (15 October 2026).** FIXED: anatomy rerun on the repaired panel (0617bf6; S31 b741410); Appendix Table A10.

*As recorded before closing:*


`panel26.py` (the channel anatomy, F7.2) reads the raw Global Macro Database. The atlas later repaired budget
splices, debt splices, net exports and money breaks (`atlas/meta.json`, "fixes"). Rerun the channel anatomy on the
repaired panel, especially imports and budget spending, and report any change.


## 13. Maddison growth for Norway, Switzerland and South Africa — **FIXED**

**Resolution (15 October 2026).** FIXED: GMD growth swap run, no conclusion changes (0617bf6; S31 b741410); Methods §7.8, Appendix Table A2.

*As recorded before closing:*


For 1991–2011, the atlas comparison found Maddison's per-capita growth for these three running 2–3 percentage
points above national-accounts growth.
Robustness run: swap in GMD (national accounts) real GDP per capita for these three and rerun the arc, the amplitude
link and the decomposition.


## 14. The two-year rate lead needs past-only phases — **FIXED + LIMITATIONS**

**Resolution (15 October 2026).** FIXED: re-tested with past-only phases; it fails and is dropped as a lead claim (f60ed64). The dropped rate lead is in LIMITATIONS.

*As recorded before closing:*


The band-pass and Hilbert transform both use future data, so a lead found with them can partly come from the future.
Re-test G1 (short rates lead recessions by two years, p = 0.019) with phases built only from data available at each
date (a one-sided filter, or re-estimating phases on an expanding window). Report both.


## 15. Citations to fix — **FIXED**

**Resolution (15 October 2026).** FIXED: the manuscript cites Ikeda, Aoyama and Yoshikawa (2013) as RIETI DP 13-E-089, Kose, Sugawara and Terrones (2020) and Kose and Terrones (2015), and Methods §8 cites the Maddison commit and checksum (62109da). Every reference was checked; the unverified details are marked in the reference list.

*As recorded before closing:*


- Ikeda, Aoyama and Yoshikawa on international synchronization is RIETI Discussion Paper 13-E-089; arXiv 1110.6679
  is Ikeda et al. (2011) on Japanese industrial sectors.
- Kose–Terrones global recessions: cite the dating source (Kose, Sugawara and Terrones 2020, World Bank Policy
  Research Working Paper 9172, and the 2015 IMF book *Collapse and Revival* by Kose and Terrones). Check the exact
  references before the paper goes out.
- Methods §8: cite the Maddison commit and file checksum from `data/sources.yaml`, not only the package version
  (1.1.0 then, 1.1.1 now; the data file is unchanged). Drafted as edit B4.


## 16. Banking-crisis history not re-verified — **FUTURE WORK**

**Resolution (15 October 2026).** FUTURE WORK ("Banking-crisis dating"): no claim depends on it.

*As recorded before closing:*


`crisis_dating_test.py` needs `jst.xlsx`, which was never pinned. GMD carries `data/clean/aggregators/JST/JST.dta`
(pinned) as a likely replacement. History only; no paper claim depends on it.


## 17. Sample definition — **FIXED**

**Resolution (15 October 2026).** FIXED: S31 is the main sample (f8f32e2); every leave-out run (0617bf6, b741410); Appendix Table A1.

*As recorded before closing:*


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


## 18. The Methods diagnostics figure does not exist in our files — **FIXED**

**Resolution (15 October 2026).** FIXED: drawn as F5.4 from the S31 results (62109da).

*As recorded before closing:*


`docs/methods.md` ends with a caption for a three-panel diagnostics figure (MST decade means, phase-lag null,
corrected p-values). It was described in Claude Science and never saved here. Draw it in the rerun.


## 19. Two different "real GDP" r(t) series — **FIXED**

**Resolution (15 October 2026).** FIXED in the text: the paper's claims use Maddison GDP per capita; the Global Macro Database appears only in the channel table (Appendix Table A10) and in the count of contracting economies, both labelled (62109da).

*As recorded before closing:*


The paper's r(t) uses Maddison GDP per capita. The atlas `sync.json` uses Global Macro Database real GDP (total). They
differ year by year (1970: 0.28 against 0.34). Keep them apart in the text; quote the Maddison series for Paper 1
claims and the GMD series only for the channel comparison.


## 20. Bonferroni value in Methods 7.4 is rounded twice — **FIXED**

**Resolution (15 October 2026).** FIXED: Methods §7.4 says 0.094 (decided 4872c0b; applied 62109da).

*As recorded before closing:*


Found in Phase 2. Bonferroni over the five lags for lead-1 and after-2 is 5 × 1/53 = 0.0943, so "0.094"; Methods 7.4 and
registry A8 print 0.095 (5 × the rounded 0.019). Benjamini–Hochberg (0.047, 0.063) is right. **What to do:** propose the
corrected text in the Phase 3 text-changes file; Sid decides.


## 21. MST decade means in Methods 6.5 and 7.7 — **FIXED**

**Resolution (15 October 2026).** FIXED: decade means 1979–89 vs 2013–22 on S31 (0.687 vs 0.424, 1.6×) in Methods §6.5 and §7.7 (decided 4872c0b; applied 62109da).

*As recorded before closing:*


Found in Phase 2 (`src/ef/network.py`; the stored `mst_results.json` reproduces exactly). The Methods' 0.706 (1970s)
reproduces only if the 10-year windows may reach back into the 1950–69 run-in, so that 1970 counts (mean of 1970–79,
windows from 1961); but the same paragraph says L is defined only from 1971, where the 1971–79 mean is 0.696. The 7.7
value 0.652 (1979–89, windows inside 1970–2022) is not reproduced by any variant tried (0.669–0.679), and the single-year
endpoint 0.771 in 6.5 disagrees with the stored 0.781 (registry E2). 2013–2022 (0.379) and the 1.9× contrast are
unaffected in substance. **What to do:** fix one stated window convention in Phase 3, recompute all three numbers from
code, and propose the text; Sid decides.


## 22. The restoring-time indicator needs a definition that adds information — **FIXED**

**Resolution (15 October 2026).** FIXED: dropped (decided 4872c0b); Methods §6.7 says why (62109da).

*As recorded before closing:*


Phase 2 reconstructs it as 1/(−ln φ), the inverse of the recovery rate used in the bifurcation test. That is a
monotone function of the lag-1 autocorrelation φ, so its rank-based pre-crisis trend is the same as the autocorrelation's
(τ −0.152; surrogate p 0.769 against 0.757, the gap coming only from clipping). As defined it is not a third
indicator. **What to do:** before Phase 3, choose a definition that measures something else (for example the decay
time of r after its own deviations, fitted on levels, or the e-folding time of the windowed autocorrelation function
beyond lag 1), pre-register it, and report it beside the other two; Sid decides.


## 23. The detrended pre-crisis MST trend does not reproduce — **FIXED**

**Resolution (15 October 2026).** FIXED: the pre-registered σ = 8 value is in Methods §6.5 (62109da); the irreproducible first-run value stays in the registry and is not quoted.

*As recorded before closing:*


Methods 6.5 and registry E4 give τ = −0.086, p = 0.316 for Gaussian-detrended L. Detrending with σ = 5, 8 or 10 years
on the as-run windows (from 1962, seed 303) gives τ between −0.043 and −0.057 and p between 0.36 and 0.42; the
original script is not in the repository. The conclusion (null) is the same. **What to do:** the pre-registration fixes
σ = 8 and the new windows; Phase 3 reports that value and edit B5 rewrites the sentence.


## 24. Russia is not in the sample, and no reason is recorded — **FIXED**

**Resolution (15 October 2026).** FIXED: Russia added, S31 main (f8f32e2, c842019); results b741410.

*As recorded before closing:*


By mean real GDP over 1970–2022, the largest economies missing from the 26 are China (8.06 trillion 2011 PPP dollars),
Russia (2.18), Brazil (1.74), Iran (0.71), Saudi Arabia (0.65) and Poland (0.54); in 2022 Russia (3.73) is still larger
than Brazil (3.19) (`docs/data_validation.md`, `ef.data.maddison.largest_outside`). Russia's Maddison series is complete
for 1950–2022, so the inclusion rule does not exclude it: the rule filtered the candidates chosen on 10 October (China,
Brazil, Saudi Arabia, the UAE, Iran) and was never applied to every Maddison economy. The §1 sentence "China and Brazil
are the largest economies missing from the 26" is therefore not true as written. **What to do:** Sid gives the reason
for leaving Russia out (it goes into §1), rewords the sentence ("with Russia, the five largest"), or adds Russia as a
sensitivity run after a pre-registration amendment. Nothing is run until he decides.


## 25. What the G1 simulations say about four Paper 1 tests — **FIXED + LIMITATIONS**

**Resolution (15 October 2026).** FIXED: (a) edge-matched nulls pre-registered and run (864317a, fc63e87, 83a86b4); the κ = 0 table is Methods §5.3 (62109da). (b) and (c) are LIMITATIONS ("How global recessions are dated", "What the cross-term test shows"); (d) after-2 is in LIMITATIONS ("The fall after recessions").

*As recorded before closing:*


From `gnn/G1_report.md` (8,000 simulated worlds, pre-registered in `docs/preregistration_G1.md`). **(a) The identity's
swing-size test** rejects in 14–19% of uncoupled worlds on the real calendar, where it should reject in 5%. The cause
is an edge effect (found by a check that was not pre-registered, `python -m ef.gnn.g1 checks`): under convention P
the swing size is inflated in 2019–2020 and collapses in 2022, and the circular surrogates have no ends. The lean
(+0.06 in the statistic) is small next to the real S31 value (1.02), so the result very likely stands, but its
p = 0.0002 should be recomputed with an edge-matched null or under convention E before it is quoted. **(b) Two-sided
lead-1 and crisis-year arcs** reject about twice as often as they should when recessions are dated from the same
economies' output, even with no coupling; the past-only lead-1 does not, and no simulated world produces it above
chance. **(c) The cross-term test** rejects in nearly every coupled world on any calendar: it shows co-movement, not
co-movement at recessions. **(d) After-2** over-rejects on the real calendar in the Kuramoto worlds (6.2%, 11.6% with
trade links). **What to do:** Sid decides which of these go into Methods and Limitations, and whether to rerun the
swing-size test with an edge-matched null (a pre-registration amendment). Nothing in `docs/methods.md` is changed.

**Outcome (14 October 2026).** Sid decided: (a) an edge-matched null for the swing-size test and every test leaning
on 2019–2022, pre-registered as amendment 4 and run (`results/EDGE_MATCHED.md`): the null rejects at about 5% on the
G1 worlds (the swing-size test 1.5% and 4.8%, from 13.8% and 18.9%), and the real swing-size p stays at the floor on
S31, S30 and S26; (b) and (c) go into Limitations as L8 and L9 in `docs/methods_proposed_edits.md`; the κ = 0 table
goes into the proposed Methods as §5.3. `docs/methods.md` is unchanged.
