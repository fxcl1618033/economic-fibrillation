# Pre-registration — Paper 1 rerun on the 30 economies (S30)

Written 11 October 2026, before any test is run on S30 (`CLAUDE.md` rule 3). **Status: draft for Sid's sign-off.**
Nothing runs on S30 until Sid signs below and this file is committed with the sign-off date. Any later change is
added as a dated amendment at the end; results obtained before an amendment are kept and reported beside the new ones.

The S26 results that S30 is compared with are the stored Paper 1 results (`docs/results_registry.md`), reproduced
exactly by the library (`docs/golden_check.md`). Where this document changes a convention (section 3), S26 is rerun
under the new convention too, so each comparison is like with like.

## 1. Hypotheses

Stated as Paper 1 states them, with the direction fixed in advance.

1. **Synchronization rises before global recessions** (arc lead-1 and lead-2 positive).
2. **Synchronization collapses after them** (arc after-2 negative).
3. **When the world synchronizes it also swings harder** (r and mean swing size positively correlated, detrended).
4. **Most of the excess world variance in recessions arrives through co-movement** (the cross term), and inside the
   cross term both larger swings and higher correlation contribute ("amplification transmitted by alignment").
5. **The network of cycles has tightened** over the sample (MST mean edge length lower in 2013–22 than in 1979–89).
6. **The economies move nearly together**: the spread of phase leads is smaller than in uncoupled surrogate worlds.
7. **No critical slowing down precedes recessions** (S26 nulls; their continuation is expected, not claimed as a test).
8. **Synchronized short-rate rises lead recessions by two years** (inside the economies, on the repaired atlas panel).

## 2. What is fixed and never tuned

| Item | Setting |
|---|---|
| Sample | **S30**: USA, GBR, DEU, FRA, ITA, JPN, CAN, ESP, AUS, KOR, IND, MEX, NLD, SWE, CHE, BEL, ZAF, TUR, NOR, AUT, DNK, FIN, GRC, PRT, IDN, THA, CHN, BRA, SAU, IRN. **S26** (the first 26) is the frozen reference. The UAE is excluded: its Maddison series misses 1991–92 (Sid, 11 October 2026); there is no S31 run. |
| Inclusion rule | Maddison real GDP per capita and population complete for every year 1950–2022, no interpolation, no splices (enforced in `src/ef/data/maddison.py`; per-economy report `docs/data_validation.md`) |
| Data | Maddison Project Database 2023, `sbgraves237/maddisondata` at commit `3ed424b6`, `MaddisonData.rda` sha256 `63a3cff9…` (`data/sources.yaml`). Channel tests: the repaired atlas panel built by `make data` (Global Macro Database read as float64) |
| Cycle | log real GDP per capita minus its 1950–2022 mean; Butterworth band-pass, order 2, 2.04–9 years, forward–backward (scipy defaults); run-in span 1950–2022 |
| Statistics window | 1970–2022 (T = 53) |
| Rolling windows | may start in 1962 or later, never earlier: at least 12 years of filter run-in (section 3) |
| Recessions | 1975, 1982, 1991, 2009, 2020 (Kose, Sugawara and Terrones 2020). Downturns 1998, 2001, 2012 for description only |
| Nulls | Circular shift of the recession indicator (k = 1…52; floor 1/53 = 0.019). 5,000 spectrum-preserving surrogate economy sets (floor 1/5001 = 0.0002), drawn in the as-run order |
| Seeds | As run, per test: arc bootstrap 11, amplitude 404, decomposition 707, structure 909, MST 303, phase lags 505, early warning 101, coupling 202, channel anatomy 2610. The same seeds for S26, S30 and every variant |
| Directions | As in section 4, fixed now |

## 3. Conventions

**Phase conventions.** Convention **P** is primary: band-pass and Hilbert transform on 1950–2022, statistics on
1970–2022. Sensitivity, reported beside P for every test that uses phases or swing sizes:

| | Definition | Used for |
|---|---|---|
| W | band-pass on 1950–2022, cut to the window, then Hilbert | all phase-based tests |
| N | band-pass and Hilbert on 1970–2022 only | all tests (for the network and decomposition tests N is the only variant: they use no Hilbert transform) |
| E | as P, each cycle mirrored by **9 years** at both ends before the Hilbert transform | all phase-based tests |
| C | for each year t, band-pass and Hilbert on 1950…t only, keeping year t (past data only) | circular-shift tests only: surrogates are cycles, which cannot be re-filtered year by year. Required for every lead claim (CLAUDE.md rule 7): A1, A2, G1 |

Surrogates under P and E are drawn from the 1950–2022 cycles and passed through the same steps as the real data
(as `structure_tests.py` did); under W and N from the window cycles.

**Rolling windows.** One rule for every rolling statistic (Sid, 11 October 2026): a window may start in 1962 or
later, never earlier, so every window has at least 12 years of filter run-in (the band-pass starts in 1950). This is
the primary setting for the network measure, the decomposition, and the early-warning and coupling tests.

| Test | Window | First defined year | Recessions used |
|---|---|---|---|
| MST length and largest eigenvalue (E1–E6) | 10 years | 1971 | pre-crisis trends: 1975 (partly defined: 1971–74 of 1967–74), 1982, 1991, 2009, 2020 |
| Decomposition (D1–D9) | 10 years | 1971 | recession windows: 1975, 1982, 1991, 2009, 2020 |
| Lag-1 autocorrelation and variance of r (F1, F2) | 15 years | 1976 | pre-crisis trends: 1982 (partly defined: 1976–81 of 1974–81), 1991, 2009, 2020; 1975 has no defined year |
| Recovery rate, coupling test (F4) | 12 years | 1973 | post-crisis windows: 1975, 1982, 1991, 2009, 2020 |

The tipping tests keep every recession they had when first run. A partly defined pre-crisis window is kept as it was
run: pairs of years with a missing value count as zero, which pulls that recession's trend towards zero.

**Two consequences.** The MST decade comparison stays 1979–89 against 2013–22: 1979–89 is the first decade whose
windows all lie inside 1970–2022, and both means (0.677 and 0.379) are the same under either rule. The decomposition,
as first run, used windows inside 1970–2022 and so four recession windows (1982–2020); under the one rule the 1975
recession window (1966–75) enters, so D1, D3, D4, D7, D8 and D9 will change. Their stored values become sensitivity
numbers. They have not been recomputed under the new rule before this pre-registration was signed.

**Sensitivity: strict inside 1970–2022.** Every rolling test is also run with windows kept inside 1970–2022 and with
any partly defined pre-crisis window dropped (`tau_pre(strict=True)`):

| Test | First defined year | Recessions used |
|---|---|---|
| MST and largest eigenvalue | 1979 | 1991, 2009, 2020 |
| Decomposition | 1979 | 1982, 1991, 2009, 2020 (the setting as first run) |
| Autocorrelation and variance | 1984 | 2009, 2020 |
| Coupling test | 1981 | 1982, 1991, 2009, 2020 |

## 4. Tests, directions and what counts as replication

**Reading the last column.** For a test that was significant on S26, *replicates* means the same sign and p < 0.05 on
S30; *weakens* means the same sign with p ≥ 0.05; *reverses* means the opposite sign. For an S26 null, *stays null*
means p ≥ 0.05; if it becomes significant that is reported as a change, not claimed as a finding. Descriptive
quantities have no test; the criterion says what would count as the same qualitative statement.

| ID | Test | Statistic and direction | Null | S26 (as run) | Counts as the same on S30 if |
|---|---|---|---|---|---|
| A1 | Arc, lead-2 | corr(r(t), G(t+2)), upper | shift | +0.230, p 0.038 | same sign, p < 0.05 |
| A2 | Arc, lead-1 | corr(r(t), G(t+1)), upper | shift | +0.216, p 0.019 | same sign, p < 0.05 |
| A3 | Arc, crisis year | corr(r(t), G(t)), upper | shift | +0.149, p 0.189 | stays null |
| A4 | Arc, after-1 | corr(r(t+1), G(t)), lower | shift | +0.078, p 0.679 | stays null |
| A5 | Arc, after-2 | corr(r(t+2), G(t)), lower | shift | −0.277, p 0.019 | same sign, p < 0.05 |
| A6, A7 | Superposed epoch; mean r in recessions, downturns, normal years (bootstrap 95% CI, 10,000) | descriptive | — | 0.70 / 0.35; 0.65, 0.37, 0.54 | recession mean above normal |
| A8, A9 | Bonferroni and Benjamini–Hochberg over A1–A5: **the primary family** | — | — | 0.094 / 0.189; q 0.047 / 0.063 | reported as is |
| B1–B15 | Bands 2–8 and 3–10 years; HP filter (λ = 100); growth rates; split sample 1970–95 and 1996–2022; leave each recession out; without 2009 and 2020 | A1, A2, A3, A5 | shift | `docs/results_registry.md` §2 | reported as a table; no claim rests on a single row |
| B-LOO | Leave each of the 30 economies out in turn (S26 did USA, DEU, JPN only) | A1, A2, A3, A5 | shift | — | reported as a table |
| C1 | r against mean swing size, detrended (σ = 8 years) | Pearson, upper | shift; surrogates | +0.608, p 0.019 (W surrogate p 0.0006) | positive, p < 0.05 (shift) |
| C2 | Same, raw | Pearson, upper | shift | +0.530, p 0.019 | positive, p < 0.05 |
| D1, D3 | Cross term's share of the recession excess in world variance; weights: **within-window mean GDP** (the Methods) and equal | descriptive | — | 82.4% / 96.9% (windows inside 1970–2022, four recessions) | above 50% under both weights |
| D4 | Cross share of world variance, recession vs normal windows | descriptive | — | 0.723 vs 0.669; 0.880 vs 0.818 (same windows) | recession share above normal |
| D6 | Nominal surrogate p of the share ratio, and tests of the unnormalized Δcross and Δown | upper | surrogates | 0.48 / 0.35; 0.0002 | disclosure only (Methods 7.6) |
| D7, D8 | Cross term's rise split into correlation, swing size and interaction | descriptive | — | 35/50/14%; 41/46/13% (same windows; end-of-window weights) | both correlation and swing size positive |
| D9 | Mean pairwise correlation and cycle s.d., normal → recession windows | descriptive | — | 0.376 → 0.490; × 1.14 (same windows) | both rise |
| D10 | Fibrillation identity |Z| = Ā × R_A | holds exactly | — | below 10⁻¹⁸ | below 10⁻¹² |
| D11 | Share of the recession excess in log world swing² from alignment vs swing size | upper (each part) | surrogates | 39.3% / 60.7%; p 0.103 / 0.0002 | swing part positive with p < 0.05 |
| D12 | corr(R_A, r) | descriptive | — | +0.942 | positive |
| E1 | MST mean edge length, decade means 1979–89 vs 2013–22 (the same under either window rule) | descriptive | — | 0.677 vs 0.379 (1.8×) | 1979–89 above 2013–22 |
| E4 | Pre-crisis MST contraction, Kendall τ over 8 years, raw and detrended (σ = 8) | lower | surrogates | null (τ −0.171, p 0.167 as run; detrended not reproduced, open issue 23) | stays null |
| E6 | Pre-crisis trend in the largest eigenvalue | upper | surrogates | τ +0.10, p 0.306 | stays null |
| E7 | Spread (s.d.) of phase leads | **lower** | surrogates | 0.403 yr, p 0.0002 (W) | p < 0.05 lower tail |
| E9 | Mean cycle period | descriptive | — | 5.85 yr | reported |
| E10, E11 | Fiedler blocs; arc within and between blocs | descriptive; exploratory | shift | λ2 0.868 | reported |
| F1 | Pre-crisis trend in lag-1 autocorrelation of r | upper | surrogates | τ −0.152, p 0.757 | stays null |
| F2 | Pre-crisis trend in variance of r | upper | surrogates | τ +0.295, p 0.107 | stays null |
| F4 | Post-crisis change in the recovery rate (coupling as bifurcation parameter) | lower | surrogates | +0.098, p 0.542 | stays null |
| F5 | Implied coupling K/Kc around onsets | descriptive | — | 6.4 / 7.1 | reported |
| G1 | Short-rate synchronization, lead-2 (atlas panel) | upper | shift | +0.266, p 0.019 (18 economies) | same sign, p < 0.05; **and under C** |
| G2 | Investment synchronization, lead-2 | upper | shift | +0.293, p 0.038 | exploratory |
| G3 | Real GDP (GMD) synchronization, lead-1 / after-2 | upper / lower | shift | +0.237 / −0.332 | as A2 / A5 |
| G4 | Each channel's synchronization against surrogates (2,000, seed 2610) | upper | surrogates | all p 0.0005 | p < 0.05 |
| G5 | Mean pairwise cycle correlation before and after 1990, by channel | descriptive | — | registry §7 | rises |
| G7, G8 | Economies contracting in recession years; coupling to the rest | descriptive | — | registry §7 | reported |

Channel tests (G) run on the repaired atlas panel (open issue 12), on S26 and on S30. An economy enters a channel only
if that channel has continuous data from 1965 to 2022 (the as-run rule); the number of economies per channel is
reported. Missing values are never filled in beyond the as-run two-year interpolation.

## 5. Mandatory checks for the wider sample (Sid, 11 October 2026)

1. **Leave each added economy out.** Every test in section 4 is rerun under P on S30 without China, without Brazil,
   without Saudi Arabia and without Iran (four runs). A result *depends on* an economy if dropping it reverses the
   sign or moves p across 0.05.
2. **Iran and Saudi Arabia in the swing-size tests.** Their cycles are 2.9× and 2.2× the median size of the 26, so
   C1, C2, D1, D3, D4, D7, D8 and D11 are reported on S30, S30 without Iran, S30 without Saudi Arabia and S30 without
   both.

## 6. Open-issue checks folded in

| Issue | Check |
|---|---|
| 1 | Every phase-based test under P, W, N, E and C (section 3) |
| 2 | The arc with 2020 excluded (B14 and the after-2 lag) shown beside the full arc, and under E |
| 4 | Decomposition weights are the within-window mean GDP the Methods state; the end-of-window version is not rerun |
| 6 | The surrogate p of the recession cross share is not reported as evidence for the share claim |
| 8 | The phase-lead spread is tested in the lower tail (the stated question) |
| 9 | Every robustness row saved as JSON |
| 12 | Channel anatomy on the repaired panel |
| 13 | Norway, Switzerland and South Africa with Maddison growth replaced by GMD real GDP per capita growth for 1991–2011: A1–A5, C1, D1 and D3 on S26 and S30 |
| 14 | A1, A2 and G1 under C (past-only phases) |
| 21, 23 | MST decade means 1979–89 vs 2013–22; windows from 1962 (primary) and inside 1970–2022 (sensitivity); detrended trend with σ = 8 |
| 22 | The early-warning battery is two indicators (F1, F2) plus the coupling test (F4); the restoring time is dropped |

## 7. Not rerun

H1–H4 (superseded history); D2 (end-of-window weights, kept as the as-run record); D5 (not a test of the claim); E2
and E5 (single-year endpoints; the irreproducible "p = 0.47"); F3 (dropped); G6 (the US–Japan comparison is about two
economies, not the sample).

## 8. Reporting

- One file per test and variant: `results/<sample>/<convention>/<test>.json` (variants as subfolders, for example
  `results/S30_minus_IRN/P/`), each with its config, seed, code version and timestamp.
- `results/COMPARISON.md`: one row per registry ID with columns S26 · S30, flagging every sign change and every
  crossing of p = 0.05, in plain words; then the sensitivity tables.
- Everything run is reported, nulls included, with the same prominence (rule 1). p-values at a floor are labelled as
  floors (rule 4). The lead rests on 2009 and 2020 (n ≈ 2) and is described that way (rule 5).
- Multiplicity: A1–A5 on S30 under P is the primary family (Bonferroni and Benjamini–Hochberg); all other p-values
  are robustness or exploratory and are reported raw with that label.
- No change to `docs/methods.md`; text changes go to `docs/methods_proposed_edits.md`.

## Sign-off

- [x] Sid has read this pre-registration, including the rolling-window rule and its two consequences in section 3.
- Signed off on: 11 October 2026

## Amendments

Amendments 1 and 2 were approved by Sid on 11 October 2026, after the Phase 3 run.

### Amendment 1 — implementation clarifications (11 October 2026, after sign-off, before any S30 run)

Written by Claude to settle details the signed text leaves open; no test has been run on S30 before it, so no result
predates it. None changes a hypothesis, direction, sample, window rule or replication criterion. For Sid's review with
the Phase 3 results.

1. **Tests without a Hilbert transform** (MST, largest eigenvalue, decomposition) depend on the band-pass span only.
   Conventions W, E and C do not apply to them; N means the band-pass on 1970–2022 only, so their windows start in
   1970.
2. **Rolling tests with a Hilbert transform** (early-warning, coupling): W applies the Hilbert transform to the test's
   span (1962–2022) after the 1950–2022 band-pass, as first run; N uses 1970–2022 only for both steps, so windows start
   in 1970; E mirrors the 1950–2022 cycle by 9 years and keeps 1962–2022.
3. **Convention C** (past data only) is run for the circular-shift tests: the arc (A1–A5), the r–swing-size shift tests
   (C1, C2) and channel synchronization (G1–G3). Surrogate tests and the robustness rows are not run under C.
4. **Issue 2 under E**: the full robustness table (B1–B15) is also run under E.
5. **Channel anatomy on the repaired panel** (issue 12; S26 and S30): real GDP, consumption, investment, exports and
   imports as logs of the panel's real series; budget spending as log(spending share × real GDP); budget balance and
   short rate as levels; real money as a log index cumulated from the panel's real money growth, a missing year's
   growth interpolated linearly only within the as-run two-year limit. An economy enters a channel only with
   continuous data from 1965, as before. Short-rate, investment and real GDP synchronization (G1–G3) follow
   `atlas/sync.py` on the chosen sample.
6. **G7 and G8 on S30**: G7 counts the sample's economies with negative growth in each recession year; G8 averages,
   over the sample, each economy's correlation with the mean standardized cycle of the rest of the sample (the atlas
   used the 26 as the rest for everyone).
7. **Issue 13**: for Norway, Switzerland and South Africa, Maddison's year-on-year growth of GDP per capita in
   1991–2011 is replaced by GMD's real GDP per capita growth, and levels are re-chained from 1990; population is unchanged.
8. **D6**: the share statistic Δcross / (Δown + Δcross) and the unnormalized Δcross and Δown, each against the
   decomposition's 5,000 surrogates (seed 707), upper tail, both weightings; reported as disclosure only.
9. **E4 detrended**: L minus its Gaussian-smoothed copy (σ = 8 years) over the years L is defined, then the same trend.
10. **Variant folders**: `results/<sample>[_minus_<ISO>…|_strict|_gmd_growth]/<convention>/<test>.json`.

### Amendment 2 — past-only phases for short channel histories (11 October 2026, before any S30 run)

Under C an economy's channel phase in year t needs at least 16 years of that channel's data up to t (the band-pass
cannot run on fewer). Some short-rate series start in 1965, so their past-only phase is undefined until 1980. In each
year, r(t) under C is computed over the economies whose phase is defined, and the number of economies is recorded
per year. Under P nothing changes.

