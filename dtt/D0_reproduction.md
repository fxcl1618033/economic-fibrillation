# D0 — bringing in the DTT report and reproducing it

## What came in

Only the report: `dtt/legacy/DTT_Unified_Simulation_Report.pdf` (frozen, sha256 4e96a7cb…; see `dtt/legacy/README.md`).
**There is no code**, so the report's tables cannot be rerun from their own code. Following Sid's instruction, D0 goes
straight to D1: the rows Sid listed (sections B–F) are compared below with a clean implementation of the equations the
report states (`src/ef/dtt.py`, seed 1310; `python -m ef.dtt_runs reproduce`). That is a reproduction of the report's
*specification*, not of its runs: Monte Carlo rows can at best agree within sampling error, and details the report does
not state are my choices, listed with each section.

**Marks** (fixed in `src/ef/dtt_runs.py` before the run): **EXACT** — the same number to the digits the report prints
(deterministic quantities only); **CLOSE** — for Monte Carlo quantities, a two-sided 95% test cannot tell the two apart
(proportions: pooled two-proportion test; median tipping times: difference within 1.96 × the combined bootstrap
standard error; mean R²: difference within 1.96 × √2 × my standard error over 40 ensembles); **DIFFERENT** — otherwise.
My runs use about ten times the report's trials where that is cheap, so CLOSE mostly tests the report's numbers.

## Findings that need no code

- **Figure I4 is the mislabelled one, not its table.** The figure's y-axis ("absolute difference between sweep means")
  rises to 0.7, but the table printed under it gives max |state_up − state_down| = 2.977e-6, mean 9.6e-8, max
  |output_up − output_down| = 3.1e-6, and the *same* half-level crossing (g = 0.9) for both sweeps; the text says
  "effectively no hysteresis". The table is consistent with itself and with the text; a curve that reaches 0.7 cannot
  be a difference between two sweeps whose crossings coincide and whose largest gap is 3e-6. So the figure plots some
  other quantity under a wrong label. Which quantity cannot be determined without the code: its curve is neither the
  state (which reaches 0.9998 at g = 2, half-level at 0.9) nor the I3 branch gap (zero below g ≈ 1.25).
- **Figure F1's time axis cannot be matched to section F.** F1 is drawn on 0–40 "conditional simulation time" and its
  intermediate-coupling curve ends at 65%, but section F reports 800 steps, 93.5% events and median 202 steps for
  intermediate coupling (100%, median 34 steps, strong). No rescaling of the axis fits both curves: the medians read
  off F1 (about 25 and 6) have a ratio of about 4, the text's (202 and 34) about 6. F1 most likely shows a different run
  (its 0–40 range matches the cubic model's horizon of 40). The regenerated F1 (D2) is drawn in steps from the
  section F model.
- **Section C does not state its noise scale σ.** Figure C3 brackets it: the table's 23.6% at K = 0.8 lies between the
  σ = 0.75 and σ = 0.90 curves; σ = 0.82, the value of section D, is used below and checked.
- **The two K = 0 tipping rates disagree with each other** (section D 19/400 = 4.75%, section E 22/800 = 2.75%); the
  report says so ("distinct Monte Carlo runs").

## Reproduction from the report's equations

### Section B — mean R² and the variance law

My choices (not stated in the report): Euler–Maruyama step 0.01, a run-in of 50 time units, then R² averaged over 200 time units; 40 ensembles per K, as the report. *Report arithmetic*: the report's theoretical variance implies its mean R² (×2); its amplification (31 × mean R²) and N_eff (1 / mean R²) columns are checked against that to the printed digits.

| K | Report mean R² | My mean R² (SE) | Mark | Report's arithmetic | Report's MC ÷ theory | My MC ÷ theory |
|---|---|---|---|---|---|---|
| 0.000 | 0.0318 | 0.0313 (0.0005) | CLOSE | EXACT | 0.999 | 1.000 |
| 0.267 | 0.0398 | 0.0403 (0.0006) | CLOSE | EXACT | 1.004 | 0.999 |
| 0.533 | 0.0536 | 0.0518 (0.0013) | CLOSE | EXACT | 0.999 | 0.998 |
| 0.800 | 0.0733 | 0.0795 (0.0047) | CLOSE | EXACT | 0.996 | 0.999 |
| 1.067 | 0.0976 | 0.1106 (0.0088) | CLOSE | EXACT | 1.007 | 1.000 |
| 1.333 | 0.1711 | 0.1623 (0.0148) | CLOSE | EXACT | 1.002 | 1.000 |
| 1.600 | 0.3029 | 0.2796 (0.0224) | CLOSE | EXACT | 1.004 | 0.998 |
| 1.867 | 0.4403 | 0.4706 (0.0312) | CLOSE | EXACT | 1.004 | 1.001 |
| 2.133 | 0.6182 | 0.6609 (0.0190) | CLOSE | EXACT | 0.998 | 0.999 |
| 2.400 | 0.7532 | 0.6619 (0.0280) | DIFFERENT | EXACT | 1.004 | 1.000 |
| 2.667 | 0.8168 | 0.7924 (0.0124) | CLOSE | EXACT | 0.994 | 1.000 |
| 2.933 | 0.8625 | 0.8329 (0.0086) | DIFFERENT | EXACT | 0.998 | 1.000 |
| 3.200 | 0.8911 | 0.8719 (0.0059) | DIFFERENT | EXACT | 1.001 | 1.000 |

### Section C — escape with averaged noise σ√E[R²]

σ = 0.82 (not stated in section C; section D's value, bracketed by figure C3), T = 40, step 0.01, start in the lower well, tipping = first x ≥ 0. Each K twice: with the report's own mean R² (isolates the escape model) and with mine from section B (the whole chain). 10,000 trials per row.

| K | R² from | R² | Report | Mine | Mark | Report median | My median (± tolerance) | Mark |
|---|---|---|---|---|---|---|---|---|
| 0.000 | report | 0.0318 | 2/500 (0.40%) | 19/10000 (0.19%) | CLOSE | 9.14 | 9.41 (± 15.64) | CLOSE |
| 0.000 | mine | 0.0313 | 2/500 (0.40%) | 20/10000 (0.20%) | CLOSE | 9.14 | 17.44 (± 16.58) | CLOSE |
| 0.800 | report | 0.0733 | 118/500 (23.60%) | 2055/10000 (20.55%) | CLOSE | 26.54 | 20.09 (± 3.22) | DIFFERENT |
| 0.800 | mine | 0.0795 | 118/500 (23.60%) | 2614/10000 (26.14%) | CLOSE | 26.54 | 20.71 (± 3.41) | DIFFERENT |
| 1.333 | report | 0.1711 | 422/500 (84.40%) | 8447/10000 (84.47%) | CLOSE | 12.51 | 12.59 (± 1.39) | CLOSE |
| 1.333 | mine | 0.1623 | 422/500 (84.40%) | 8190/10000 (81.90%) | CLOSE | 12.51 | 13.46 (± 1.50) | CLOSE |
| 1.867 | report | 0.4403 | 500/500 (100.00%) | 9992/10000 (99.92%) | CLOSE | 4.67 | 4.50 (± 0.55) | CLOSE |
| 1.867 | mine | 0.4706 | 500/500 (100.00%) | 9994/10000 (99.94%) | CLOSE | 4.67 | 4.27 (± 0.46) | CLOSE |
| 3.200 | report | 0.8911 | 500/500 (100.00%) | 10000/10000 (100.00%) | CLOSE | 2.29 | 2.27 (± 0.27) | CLOSE |
| 3.200 | mine | 0.8719 | 500/500 (100.00%) | 10000/10000 (100.00%) | CLOSE | 2.29 | 2.31 (± 0.27) | CLOSE |

### Section D — the dynamic shared-shock model, g = σR(t)

N = 31, ω ~ Normal(0, 1), D = 0.02, μ = 0.2, σ = 0.82, step 0.01, T = 40, phases uniform at t = 0 (no run-in, as the report). 4,000 trials per K; the independent-noise control (g = σ/√N) 40,000.

| K | Report | Mine | Mark | Report median | My median (± tolerance) | Mark | My mean R(t) |
|---|---|---|---|---|---|---|---|
| 0.000 | 19/400 (4.75%) | 203/4000 (5.08%) | CLOSE | 27.71 | 18.42 (± 9.29) | CLOSE | 0.159 |
| 0.800 | 136/400 (34.00%) | 1279/4000 (31.97%) | CLOSE | 21.54 | 18.62 (± 3.24) | CLOSE | 0.240 |
| 1.333 | 296/400 (74.00%) | 2955/4000 (73.88%) | CLOSE | 14.64 | 13.42 (± 1.77) | CLOSE | 0.370 |
| 1.867 | 388/400 (97.00%) | 3864/4000 (96.60%) | CLOSE | 7.67 | 7.44 (± 0.70) | CLOSE | 0.616 |
| 3.200 | 400/400 (100.00%) | 4000/4000 (100.00%) | CLOSE | 3.82 | 3.82 (± 0.33) | CLOSE | 0.910 |
| control | 13/4000 (0.33%) | 118/40000 (0.29%) | CLOSE | 24.72 | 22.94 (± 11.24) | CLOSE | — |

### Section E — instantaneous R(t) against constant-RMS noise, same traces and Brownian increments

| K | Noise | Report | Mine | Mark | Report median | My median (± tolerance) | Mark |
|---|---|---|---|---|---|---|---|
| 0.000 | σR(t) | 22/800 (2.75%) | 203/4000 (5.08%) | DIFFERENT | 23.29 | 18.42 (± 8.68) | CLOSE |
| 0.000 | each trial's RMS | 5/800 (0.62%) | 28/4000 (0.70%) | CLOSE | 18.26 | 22.27 (± 14.46) | CLOSE |
| 0.000 | ensemble RMS | 4/800 (0.50%) | 19/4000 (0.47%) | CLOSE | 15.12 | 24.58 (± 15.76) | CLOSE |
| 0.800 | σR(t) | 263/800 (32.88%) | 1279/4000 (31.97%) | CLOSE | 16.19 | 18.62 (± 2.56) | CLOSE |
| 0.800 | each trial's RMS | 161/800 (20.12%) | 785/4000 (19.62%) | CLOSE | 16.86 | 17.96 (± 2.35) | CLOSE |
| 0.800 | ensemble RMS | 160/800 (20.00%) | 735/4000 (18.38%) | CLOSE | 19.28 | 19.41 (± 3.01) | CLOSE |
| 1.333 | σR(t) | 590/800 (73.75%) | 2955/4000 (73.88%) | CLOSE | 14.13 | 13.42 (± 1.35) | CLOSE |
| 1.333 | each trial's RMS | 531/800 (66.38%) | 2701/4000 (67.53%) | CLOSE | 12.79 | 12.27 (± 1.29) | CLOSE |
| 1.333 | ensemble RMS | 663/800 (82.88%) | 3332/4000 (83.30%) | CLOSE | 13.76 | 13.59 (± 1.28) | CLOSE |
| 1.867 | σR(t) | 773/800 (96.62%) | 3864/4000 (96.60%) | CLOSE | 7.85 | 7.44 (± 0.50) | CLOSE |
| 1.867 | each trial's RMS | 767/800 (95.88%) | 3868/4000 (96.70%) | CLOSE | 5.28 | 5.18 (± 0.56) | CLOSE |
| 1.867 | ensemble RMS | 797/800 (99.62%) | 3992/4000 (99.80%) | CLOSE | 5.29 | 5.02 (± 0.47) | CLOSE |
| 3.200 | σR(t) | 800/800 (100.00%) | 4000/4000 (100.00%) | CLOSE | 3.82 | 3.82 (± 0.25) | CLOSE |
| 3.200 | each trial's RMS | 800/800 (100.00%) | 4000/4000 (100.00%) | CLOSE | 2.24 | 2.39 (± 0.25) | CLOSE |
| 3.200 | ensemble RMS | 800/800 (100.00%) | 4000/4000 (100.00%) | CLOSE | 2.21 | 2.37 (± 0.25) | CLOSE |

### Section F — the stress-threshold prototype

x[t+1] = 0.9 x[t] + 0.25 √(V/31) ε[t] from x = 0, 800 steps, an event when |x| ≥ 0.8 two steps running (event time = the second step). V taken from the report's table: the oscillator settings behind its R and V (diffusion, run length) are not stated, and its V = 1 at K = 0 is not 31 × R² (= 0.80 for R = 0.1611), so the R → V step cannot be reproduced. 6,000 trials per row.

| Scenario | Innovation s.d. (report / mine) | Stationary s.d. (report / mine) | Report events | Mine | Mark | Report median steps | Mine (± tolerance) | Mark |
|---|---|---|---|---|---|---|---|---|
| asynchronous (K = 0) | 0.0449 / 0.0449 | 0.103 / 0.1030 | 0/600 (0.00%) | 0/6000 (0.00%) | CLOSE | — | — | — |
| intermediate (K = 1.5) | 0.1469 / 0.1469 | 0.337 / 0.3370 | 561/600 (93.50%) | 5552/6000 (92.53%) | CLOSE | 202.00 | 205.00 (± 20.49) | CLOSE |
| strong (K = 2.5) | 0.2342 / 0.2342 | 0.5372 / 0.5372 | 600/600 (100.00%) | 6000/6000 (100.00%) | CLOSE | 34.00 | 32.00 (± 3.36) | CLOSE |

### Section I3 (frozen section, checked for Sid's question) — the mean-field Ising model m = tanh(gm + h)

h = 0.08, g from 0 to 2.5 on 2501 points; the up-sweep follows the low-g branch, the down-sweep starts on the negative branch at g = 2.5. The fold of the negative branch is solved exactly (m = tanh(gm + h) with g(1 − m²) = 1).

| Quantity | Report | Mine | Mark |
|---|---|---|---|
| Up-sweep state at g = 2.5 | 0.9879 | 0.9879 | EXACT |
| Down-sweep state at g = 2.5 | -0.9829 | -0.9829 | EXACT |
| Down-sweep state at g = 0 | 0.07983 | 0.07983 | EXACT |
| Maximum branch gap | 1.970796 | 1.970796 | EXACT |
| Loop area | 2.273208 | 2.270750 | CLOSE (depends on the g grid and the quadrature; 0.1%) |
| Down-sweep jump (the fold) | near 1.25 | fold at g = 1.2549 (m = -0.451) | CLOSE: a real saddle-node |
| Up-sweep "jump" | near 0.915 | steepest point at g = 0.917; largest step between grid points 0.0013 | not a jump: the branch is continuous; 0.915 is where it is steepest |

## Count

Of 93 marked rows in sections B–F: 13 EXACT, 74 CLOSE, 6 DIFFERENT (B mean R², C median, E tipping).

**Reading.** The report reproduces from its own equations except for six rows; its headline numbers all reproduce.

- **Reproduced:** the variance law (Monte Carlo ÷ theory within 0.2% at every K, mine and the report's), the report's own arithmetic in section B (13 of 13 rows), section C's tipping rates, section D's sweep from about 5% to 100% (mine: 5.08% at K = 0, 31.97% at K = 0.8) and its independent-noise control (0.29% against the report's 0.33%), section E's gap between σR(t) and constant RMS at K = 0.8 (32.0% against 19.6%, the report 32.9% against 20.1%), section F's event counts and medians given its V, and the I3 Ising numbers.
- **Section B, mean R² at strong coupling** (K = 2.4: 0.7532 against my 0.6619, K = 2.933: 0.8625 against my 0.8329, K = 3.2: 0.8911 against my 0.8719): mine is lower. A diagnostic (not part of the marks) with a second seed gives K = 2.4: 0.6819; K = 2.933: 0.8452 (inside the tolerance); K = 3.2: 0.8562; halving the oscillator noise gives 0.6884; 0.8489; 0.8598, so the noise term is not the cause. The report does not say how the frequencies were drawn for each ensemble or how long it ran, so the cause is unknown. The variance law does not depend on it.
- **Section C, median tipping time at K = 0.8** (26.5 in the report; about 20 in mine, with the report's R² or mine): the tipping rates agree, the timing of the tips does not. With a constant noise and a constant hazard, tips spread evenly over the horizon and the median among them is near 20; 26.5 would need tips to come late.
- **Section E, K = 0 with σR(t)** (22/800 = 2.75% in the report; mine 5.08%): the report's own section D gives 4.75% for the same model and parameters, and mine agrees with that. The report already notes that its two K = 0 runs differ.
- **Not reproducible:** section F's step from coupling K to R and V (oscillator settings not stated, and V = 1 at K = 0 is not 31 × R²); figures F1 and I4 (see above).
