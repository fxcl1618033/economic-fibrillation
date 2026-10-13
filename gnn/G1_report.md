# G1 report — simulated worlds with known coupling

Status: **for Sid's review.** Pre-registered in `docs/preregistration_G1.md` (commit 9c532fc; amendment 1, 30b095e, a numerical bound set before any test ran), then calibrated and run: 8,000 simulated worlds (two models × four settings × 1,000), each through the 20 Paper 1 p-values under two ways of dating recessions. Code `src/ef/gnn/simulator.py` and `src/ef/gnn/g1.py`; `make gnn-g1` reruns it (about 80 minutes on this Mac). Every number below is read from `gnn/G1/`.

## In short

- **The κ = 0 check, recessions on the real calendar** (dates that have nothing to do with a simulated world): most tests reject at about the rate they should (3.8% for circular shifts, 5% for surrogates). Each of the five arc lags rejects in 2.9–6.2% of uncoupled worlds (details in section 3). The gate in `gnn/README.md` is met by 17 of 20 tests in the Kuramoto worlds and 17 of 20 in the Stuart–Landau worlds. **The exception that matters is the identity's swing-size test**, which rejects in 13.8–18.9% of uncoupled worlds where it should reject in 5%. The cause is an edge effect: the pipeline inflates swing sizes in 2019–2020, two years from the end of the data, and 2020 is a recession year. The real S31 result is far larger than this lean (section 6).
- **Five lags tested at once:** at least one of the five arc lags rejects in 17.3–18.4% of uncoupled worlds. Paper 1 already says no single lag survives a multiplicity correction; this is the same fact in numbers.
- **Recessions dated from each world's own output** (the five worst years for world GDP per capita, as Kose, Sugawara and Terrones date the real ones): with no coupling at all, the two-sided arc test rejects at the crisis year in 8.2–8.9% and at lead-1 in 8.5–8.6% of worlds, about 2.3 times its exact rate. The worst years for world output are years in which cycles happen to line up, so dating recessions that way builds part of the result in. **The past-only lead-1 test does not do this** (2.3–2.9%).
- **Known coupling:** the pipeline's r rises smoothly with the trade coupling κ and with the common forcing φ. Both reach the real mean r (0.48) at κ\* = 15.5 (Kuramoto) or 20.6 (Stuart–Landau), and φ\* = 1.95 or 0.99. With own-dated recessions the two-sided lead-1 rejection rises to 15.0–20.6% with trade links and 32.5–41.9% with common forcing. **The past-only lead-1 test never rejects more often than chance, in any setting** (0.8–4.6%; no interval lies above 3.8%).
- **Some "at recessions" tests answer a different question.** The cross-term test rejects in 97.1–99.3% of trade-coupled worlds (GDP weights) even with the real calendar, which is unrelated to those worlds. The same holds for r against swing size and the clustering of phase leads. These tests detect co-movement in general; they say nothing about recessions in particular.

## 1. The worlds and the calibration

Thirty-one economies (S31) and a world node. Each economy is an oscillator with its own observed mean period (4.8–8.0 years) and swing size, on its own linear trend in log GDP per capita, with Maddison's population. Trade links pull economy i towards economy j in proportion to j's exports to i as a share of i's GDP (the G0 primary weight, the real matrix of each year; years before 1970 use 1970's; masked links are no links). The world node forces every economy equally. Calibration used no recession year (pre-registration, steps 1–3):

| | Real S31 | Kuramoto | Stuart–Landau |
|---|---|---|---|
| Spread of annual phase steps (median sd, radians) | 0.996 | 1.030 | 1.053 |
| Swing-size variation (median coefficient of variation) | 0.659 | 0.437 | 0.507 |
| Mean r, no coupling | 0.484 (real, with whatever coupling it has) | 0.159 | 0.166 |
| Noise σ | — | 1.58 | 0.0734 |
| μ (Stuart–Landau growth rate) | — | — | −1 |
| κ\* (trade links only; mean r → 0.484) | — | 15.5 | 20.6 |
| φ\* (common forcing only; mean r → 0.484) | — | 1.95 | 0.985 |
| Mean r at κ\* / at φ\* | 0.484 | 0.487 / 0.485 | 0.484 / 0.484 |

The Kuramoto worlds match the phase-step target; their swing sizes vary only through noise and filtering (0.44 against the real 0.66). The Stuart–Landau calibration ends at the edge of its grid (μ = −1, a damped oscillator kept going by noise) with a swing-size variation of 0.51: as the pre-registration expected, Gaussian noise cannot make swings as uneven as the real ones. Neither model has crises.

## 2. What the pipeline sees of known coupling

Mean r over 1970–2022 and by period, 200 worlds per row (multiples ⅛, ¼ and 4 in `gnn/G1/r_curve.csv`):

| Model | Coupling | × calibrated | Mean r | 1970s | 1980s | 1990s | 2000s | 2010–2022 |
|---|---|---|---|---|---|---|---|---|
| Kuramoto | κ (trade links) | 0 | 0.160 | 0.166 | 0.163 | 0.158 | 0.161 | 0.155 |
| Kuramoto | κ (trade links) | 0.5 | 0.267 | 0.237 | 0.240 | 0.262 | 0.288 | 0.298 |
| Kuramoto | κ (trade links) | 1 | 0.489 | 0.392 | 0.434 | 0.464 | 0.556 | 0.575 |
| Kuramoto | κ (trade links) | 2 | 0.798 | 0.660 | 0.743 | 0.792 | 0.892 | 0.879 |
| Kuramoto | φ (common forcing) | 0.5 | 0.294 | 0.298 | 0.297 | 0.292 | 0.309 | 0.280 |
| Kuramoto | φ (common forcing) | 1 | 0.483 | 0.495 | 0.482 | 0.482 | 0.498 | 0.464 |
| Kuramoto | φ (common forcing) | 2 | 0.738 | 0.740 | 0.741 | 0.737 | 0.758 | 0.720 |
| Stuart–Landau | κ (trade links) | 0 | 0.159 | 0.159 | 0.160 | 0.158 | 0.158 | 0.161 |
| Stuart–Landau | κ (trade links) | 0.5 | 0.340 | 0.315 | 0.329 | 0.339 | 0.349 | 0.360 |
| Stuart–Landau | κ (trade links) | 1 | 0.482 | 0.444 | 0.463 | 0.484 | 0.496 | 0.513 |
| Stuart–Landau | κ (trade links) | 2 | 0.658 | 0.611 | 0.634 | 0.663 | 0.678 | 0.695 |
| Stuart–Landau | φ (common forcing) | 0.5 | 0.312 | 0.313 | 0.318 | 0.321 | 0.306 | 0.307 |
| Stuart–Landau | φ (common forcing) | 1 | 0.487 | 0.490 | 0.495 | 0.495 | 0.479 | 0.476 |
| Stuart–Landau | φ (common forcing) | 2 | 0.694 | 0.702 | 0.702 | 0.703 | 0.690 | 0.679 |
| **Real S31** | | | **0.484** | **0.387** | **0.349** | **0.344** | **0.688** | **0.616** |

r follows both couplings without a jump, so the pipeline reads coupling strength. The two kinds differ over time: with trade links r rises as trade grows (Kuramoto 0.42 in 1970–1995 to 0.57 in 2010–2022; Stuart–Landau 0.46 to 0.51), while common forcing gives a flat r. The real r rises more (0.37 to 0.62). That is a description, not a test.

## 3. The κ = 0 check

Share of uncoupled worlds (κ = φ = 0) in which each test rejects at p ≤ 0.05, with its 95% interval; 1,000 worlds per cell. **Bold**: the interval lies above the exact rate. Real dates (A) are unrelated to the worlds; own dates (B) are each world's five worst years for world GDP per capita.

| Test | Exact rate | Kuramoto, real dates (A) | Kuramoto, own dates (B) | Stuart–Landau, real dates (A) | Stuart–Landau, own dates (B) |
|---|---|---|---|---|---|
| Arc, lead-2 | 3.8% | 3.3% (2.4–4.6) | **5.2% (4.0–6.8)** | 3.6% (2.6–4.9) | **5.3% (4.1–6.9)** |
| Arc, lead-1 | 3.8% | 2.9% (2.0–4.1) | **8.5% (6.9–10.4)** | 4.4% (3.3–5.9) | **8.6% (7.0–10.5)** |
| Arc, crisis year | 3.8% | 4.4% (3.3–5.9) | **8.9% (7.3–10.8)** | 3.3% (2.4–4.6) | **8.2% (6.7–10.1)** |
| Arc, after-1 | 3.8% | 4.5% (3.4–6.0) | 4.2% (3.1–5.6) | 3.6% (2.6–4.9) | 2.6% (1.8–3.8) |
| Arc, after-2 | 3.8% | **6.2% (4.9–7.9)** | 3.9% (2.9–5.3) | 4.6% (3.5–6.1) | 4.3% (3.2–5.7) |
| Arc, lead-2, past-only phases | 3.8% | 4.1% (3.0–5.5) | 3.3% (2.4–4.6) | 3.4% (2.4–4.7) | 3.5% (2.5–4.8) |
| Arc, lead-1, past-only phases | 3.8% | 3.5% (2.5–4.8) | 2.9% (2.0–4.1) | 3.8% (2.8–5.2) | 2.3% (1.5–3.4) |
| r with swing size (shifts) | 3.8% | **6.2% (4.9–7.9)** | **6.2% (4.9–7.9)** | **5.7% (4.4–7.3)** | **5.7% (4.4–7.3)** |
| r with swing size (surrogates) | 5.0% | 5.5% (4.2–7.1) | 5.5% (4.2–7.1) | 5.4% (4.2–7.0) | 5.4% (4.2–7.0) |
| Cross term at recessions, GDP weights | 5.0% | 5.3% (4.1–6.9) | **8.9% (7.3–10.8)** | 5.4% (4.2–7.0) | **10.8% (9.0–12.9)** |
| Cross term at recessions, equal weights | 5.0% | 4.6% (3.5–6.1) | **6.8% (5.4–8.5)** | 4.6% (3.5–6.1) | **6.8% (5.4–8.5)** |
| Identity: alignment at recessions | 5.0% | 4.8% (3.6–6.3) | **11.4% (9.6–13.5)** | **6.5% (5.1–8.2)** | **12.1% (10.2–14.3)** |
| Identity: swing size at recessions | 5.0% | **13.8% (11.8–16.1)** | **7.5% (6.0–9.3)** | **18.9% (16.6–21.4)** | **14.9% (12.8–17.2)** |
| MST contraction before recessions | 5.0% | 2.8% (1.9–4.0) | 5.0% (3.8–6.5) | 4.1% (3.0–5.5) | 3.8% (2.8–5.2) |
| MST contraction, detrended | 5.0% | 3.0% (2.1–4.3) | 5.1% (3.9–6.6) | 4.5% (3.4–6.0) | 3.7% (2.7–5.1) |
| MST fragility before recessions | 5.0% | 4.9% (3.7–6.4) | 5.3% (4.1–6.9) | 5.2% (4.0–6.8) | 5.1% (3.9–6.6) |
| Phase leads clustered | 5.0% | 3.0% (2.1–4.3) | 3.0% (2.1–4.3) | 5.3% (4.1–6.9) | 5.3% (4.1–6.9) |
| Slowing down: autocorrelation of r | 5.0% | 5.1% (3.9–6.6) | 5.7% (4.4–7.3) | 4.2% (3.1–5.6) | 4.5% (3.4–6.0) |
| Slowing down: variance of r | 5.0% | 5.1% (3.9–6.6) | 5.0% (3.8–6.5) | 6.1% (4.8–7.8) | 5.5% (4.2–7.1) |
| Slower recovery after recessions | 5.0% | 4.8% (3.6–6.3) | 5.2% (4.0–6.8) | 4.5% (3.4–6.0) | 4.0% (3.0–5.4) |
| Any of the five arc lags | — | 18.4% (16.1–20.9) | 26.2% (23.6–29.0) | 17.3% (15.1–19.8) | 25.0% (22.4–27.8) |
| Any of lead-2, lead-1, crisis | — | 9.9% (8.2–11.9) | 20.2% (17.8–22.8) | 10.2% (8.5–12.2) | 20.1% (17.7–22.7) |

**Real calendar.** Tests whose interval lies above the exact rate: Arc, after-2 (Kuramoto 6.2%); r with swing size (shifts) (Kuramoto 6.2%, Stuart–Landau 5.7%); Identity: alignment at recessions (Stuart–Landau 6.5%); Identity: swing size at recessions (Kuramoto 13.8%, Stuart–Landau 18.9%). The swing-size test is the serious one, and the reason is an edge effect, found after the runs with a check that was not pre-registered (`python -m ef.gnn.g1 checks`, 300 uncoupled worlds per model). Under convention P the pipeline's swing size is inflated just before the end of the data and collapses at the end: 2 log Abar differs from its average by +0.10 in 2019, +0.18 in 2020, −0.13 in 2021 and −1.52 in 2022 (Kuramoto; Stuart–Landau alike). The test compares recession years, 2020 among them, with all other years, 2022 among them, against surrogates that are circular and have no ends. So in every world the statistic leans one way: it averages +0.061 (Kuramoto) and +0.064 (Stuart–Landau) where the null is centred on 0, and +0.027 and +0.031 with 2020 left out. The spread is about right (0.072 across worlds against 0.086 in the null, Kuramoto), and only the upper tail over-rejects. Some tests reject less often than they should (MST contraction and phase leads in the Kuramoto worlds), which only makes them conservative.

**Own dates.** The arc's crisis year and lead-1 over-reject in both models. So do the identity's alignment term (11.4–12.1%) and the cross term with GDP weights (8.9–10.8%). The mechanism shows in r itself: in uncoupled worlds r averages 0.159 overall but 0.170 in a world's own recession years (Kuramoto; Stuart–Landau 0.160 and 0.173). The effect is real but modest: about twice the exact rate, not a guaranteed rejection. The past-only arc does not over-reject.

## 4. With coupling

Rejection rate (%) at p ≤ 0.05 in every setting; **bold** where the interval lies above the exact rate. Own-dated recessions first, because they are how the real dates were made:

| Test | Exact | Kura. null | Kura. forcing | Kura. κ*/2 | Kura. κ* | Stua. null | Stua. forcing | Stua. κ*/2 | Stua. κ* |
|---|---|---|---|---|---|---|---|---|---|
| Arc, lead-2 | 3.8 | **5.2** | **7.4** | 3.0 | 3.3 | **5.3** | **8.9** | 3.6 | 3.7 |
| Arc, lead-1 | 3.8 | **8.5** | **32.5** | **10.8** | **15.0** | **8.6** | **41.9** | **16.3** | **20.6** |
| Arc, crisis year | 3.8 | **8.9** | **29.6** | **13.5** | **16.8** | **8.2** | **38.1** | **19.1** | **25.1** |
| Arc, after-1 | 3.8 | 4.2 | 1.5 | 2.6 | 0.8 | 2.6 | 1.7 | 2.0 | 3.5 |
| Arc, after-2 | 3.8 | 3.9 | **5.7** | **5.9** | 3.8 | 4.3 | **6.2** | **5.7** | **5.9** |
| Arc, lead-2, past-only phases | 3.8 | 3.3 | 2.4 | 1.9 | 1.3 | 3.5 | 3.3 | 3.1 | 1.4 |
| Arc, lead-1, past-only phases | 3.8 | 2.9 | 2.5 | 1.8 | 1.7 | 2.3 | 1.8 | 2.0 | 0.8 |
| r with swing size (shifts) | 3.8 | **6.2** | **96.2** | **25.1** | **74.6** | **5.7** | **99.9** | **66.5** | **98.2** |
| r with swing size (surrogates) | 5.0 | 5.5 | **98.1** | **26.1** | **81.1** | 5.4 | **100.0** | **74.5** | **98.8** |
| Cross term at recessions, GDP weights | 5.0 | **8.9** | **100.0** | **60.1** | **98.1** | **10.8** | **100.0** | **90.5** | **99.1** |
| Cross term at recessions, equal weights | 5.0 | **6.8** | **100.0** | **83.9** | **100.0** | **6.8** | **100.0** | **99.4** | **100.0** |
| Identity: alignment at recessions | 5.0 | **11.4** | **11.2** | **13.1** | 5.5 | **12.1** | **17.9** | **18.7** | **11.7** |
| Identity: swing size at recessions | 5.0 | **7.5** | **62.0** | **13.6** | **43.8** | **14.9** | **75.1** | **65.7** | **86.9** |
| MST contraction before recessions | 5.0 | 5.0 | **9.3** | **8.5** | **28.5** | 3.8 | **10.1** | **8.2** | **12.6** |
| MST contraction, detrended | 5.0 | 5.1 | **6.5** | 5.8 | **10.2** | 3.7 | **6.8** | 5.2 | 5.8 |
| MST fragility before recessions | 5.0 | 5.3 | **8.2** | **6.9** | **23.9** | 5.1 | **9.8** | **9.8** | **11.8** |
| Phase leads clustered | 5.0 | 3.0 | **100.0** | **64.6** | **99.7** | 5.3 | **100.0** | **95.6** | **100.0** |
| Slowing down: autocorrelation of r | 5.0 | 5.7 | 4.2 | 5.0 | **6.6** | 4.5 | 3.4 | 5.0 | 4.0 |
| Slowing down: variance of r | 5.0 | 5.0 | 5.6 | **10.1** | 5.8 | 5.5 | 5.9 | **7.9** | **7.2** |
| Slower recovery after recessions | 5.0 | 5.2 | 0.9 | 1.4 | 0.7 | 4.0 | 1.4 | 1.5 | 1.5 |
| Any of the five arc lags | — | 26.2 | 57.3 | 29.8 | 31.1 | 25.0 | 65.8 | 37.6 | 46.0 |
| Any of lead-2, lead-1, crisis | — | 20.2 | 54.0 | 23.4 | 27.5 | 20.1 | 62.9 | 32.3 | 39.8 |

Real calendar (dates unrelated to the worlds):

| Test | Exact | Kura. null | Kura. forcing | Kura. κ*/2 | Kura. κ* | Stua. null | Stua. forcing | Stua. κ*/2 | Stua. κ* |
|---|---|---|---|---|---|---|---|---|---|
| Arc, lead-2 | 3.8 | 3.3 | 4.2 | 3.6 | 2.3 | 3.6 | 3.7 | 4.7 | 4.5 |
| Arc, lead-1 | 3.8 | 2.9 | 3.8 | 4.4 | 3.6 | 4.4 | **5.2** | **5.3** | 4.0 |
| Arc, crisis year | 3.8 | 4.4 | 3.7 | 3.1 | 3.0 | 3.3 | 3.3 | 3.0 | 3.3 |
| Arc, after-1 | 3.8 | 4.5 | 4.4 | 4.3 | **5.9** | 3.6 | 3.8 | 4.5 | 4.4 |
| Arc, after-2 | 3.8 | **6.2** | **7.0** | **6.6** | **11.6** | 4.6 | **6.4** | **7.7** | **6.4** |
| Arc, lead-2, past-only phases | 3.8 | 4.1 | 4.1 | 3.1 | 3.1 | 3.4 | 3.2 | 3.9 | 3.4 |
| Arc, lead-1, past-only phases | 3.8 | 3.5 | 3.9 | 4.2 | 2.9 | 3.8 | 4.2 | 4.6 | 3.5 |
| r with swing size (shifts) | 3.8 | **6.2** | **96.2** | **25.1** | **74.6** | **5.7** | **99.9** | **66.5** | **98.2** |
| r with swing size (surrogates) | 5.0 | 5.5 | **98.1** | **26.1** | **81.1** | 5.4 | **100.0** | **74.5** | **98.8** |
| Cross term at recessions, GDP weights | 5.0 | 5.3 | **99.9** | **56.8** | **97.1** | 5.4 | **100.0** | **88.8** | **99.3** |
| Cross term at recessions, equal weights | 5.0 | 4.6 | **100.0** | **89.6** | **100.0** | 4.6 | **100.0** | **99.4** | **100.0** |
| Identity: alignment at recessions | 5.0 | 4.8 | 0.8 | 3.7 | 0.8 | **6.5** | 1.2 | 2.7 | 1.6 |
| Identity: swing size at recessions | 5.0 | **13.8** | **27.1** | **15.5** | **21.0** | **18.9** | **29.4** | **30.0** | **35.6** |
| MST contraction before recessions | 5.0 | 2.8 | 5.1 | **7.5** | **17.3** | 4.1 | **6.7** | **7.5** | **7.2** |
| MST contraction, detrended | 5.0 | 3.0 | 3.9 | 4.9 | **6.5** | 4.5 | 5.3 | 5.9 | 4.3 |
| MST fragility before recessions | 5.0 | 4.9 | 5.7 | **7.2** | **15.3** | 5.2 | 5.2 | **9.2** | **8.2** |
| Phase leads clustered | 5.0 | 3.0 | **100.0** | **64.6** | **99.7** | 5.3 | **100.0** | **95.6** | **100.0** |
| Slowing down: autocorrelation of r | 5.0 | 5.1 | 3.8 | 5.8 | 5.8 | 4.2 | 3.3 | 6.0 | 3.9 |
| Slowing down: variance of r | 5.0 | 5.1 | 5.1 | **9.4** | **6.7** | 6.1 | 4.9 | **7.4** | **7.5** |
| Slower recovery after recessions | 5.0 | 4.8 | 0.7 | 0.9 | 0.5 | 4.5 | 0.7 | 1.3 | 1.3 |
| Any of the five arc lags | — | 18.4 | 20.2 | 18.7 | 22.8 | 17.3 | 19.3 | 20.2 | 19.5 |
| Any of lead-2, lead-1, crisis | — | 9.9 | 10.9 | 9.8 | 7.8 | 10.2 | 10.8 | 11.0 | 10.7 |

Three kinds of behaviour. (1) **The arc** responds to coupling only when recessions come from the world itself: under own dates, crisis-year rejections go from 8.2–8.9% with no coupling to 16.8–25.1% with trade links and 29.6–38.1% with common forcing; on the real calendar they stay near the exact rate. (2) **Tests of co-movement** (cross term, r against swing size, phase leads) reject in most coupled worlds on either calendar; the recession years play no part. (3) **Trend tests** pick up the growing trade network: MST contraction before "recessions" rejects in 17.3% of Kuramoto trade worlds on the real calendar, and 6.5% once detrended. The slowing-down tests stay within a few points of 5% (at most 10.1%), and the slower-recovery test rejects in less than 2% of worlds in every coupled setting.

## 5. The pre-registered hypotheses

- **H1, size: met for most tests, not all.** On the real calendar, with no coupling, 17 of 20 tests (Kuramoto) and 17 of 20 (Stuart–Landau) reject at or below their exact rate. Over-rejecting in at least one model: Arc, after-2; r with swing size (shifts); Identity: alignment at recessions; Identity: swing size at recessions.
- **H2, selection: confirmed, modest.** With own-dated recessions and no coupling, crisis year 8.2–8.9% and lead-1 8.5–8.6% against an exact 3.8%; alignment 11.4–12.1% and cross term 8.9–10.8% against 5%. Not expected and found: the past-only lead-1 is free of it.
- **H3, known coupling: half confirmed.** r rises with κ and φ, and under own dates the arc's lead and crisis rates at κ\* exceed those at κ = 0. But on the real calendar the co-movement tests and the MST trend tests do not stay near their exact rate in coupled worlds: they react to coupling or to its growth, whatever the dates.
- **H4, forcing against trade links: they differ.** At the same mean r, common forcing gives larger arc rejections under own dates (32.5–41.9% at lead-1 against 15.0–20.6%) and a flat r over time; trade links give a rising r. Within one sample the Paper 1 tests still cannot tell them apart: each rejection seen in the real data occurs under both, at different rates, and the past-only lead-1 under neither above chance.

## 6. What this means for Paper 1 (for Sid to decide)

1. **The swing-size test leans towards rejection because 2020 sits at the end of the data, but the real result is far larger than the lean.** With no coupling and unrelated dates the test rejects in 13.8–18.9% of worlds (floor p in 0.5% of Kuramoto and 3.1% of Stuart–Landau worlds, against 0.5% for an exact test). The lean is about +0.06 in the statistic (+0.03 without 2020); the real S31 statistic is 1.02 (0.73 without 2020), against a null spread of about 0.09 in these worlds. So the real result very likely survives a correct null. Its p = 0.0002 should still be recomputed with a null that has the same ends (surrogates passed through the same band-pass and Hilbert transform) or under the edge-robust convention E before it is quoted. Real data have no crisis-free control for 2020, so how much of 2020's own swing is edge cannot be said from here.
2. **Lead-1 should rest on the past-only phases, as the paper now says.** Dating recessions from the same economies roughly doubles the two-sided lead-1 and crisis-year rejections, even with no coupling. The past-only lead-1 is free of that, and none of these worlds produces it above chance either (0.8–4.6% in every setting), while real S31 gives p = 0.038. So the real past-only result is not explained by how recessions are dated, nor by trade coupling or common forcing at the real level of synchronization. That leaves something these models lack, such as a build-up of alignment before crises, or chance; with two effective events (2009 and 2020) chance cannot be ruled out.
3. **After-2, already in Limitations, deserves even less weight.** On the real calendar it over-rejects in the Kuramoto worlds (6.2% uncoupled, 11.6% with trade links), and real S31 sits at p = 0.057.
4. **The cross-term test shows co-movement, not co-movement at recessions.** It reaches its floor in 90–97% of trade-coupled worlds on a calendar unrelated to them, and in about 1% of uncoupled worlds. The real floor p says the 31 cycles are not independent. The Results wording should claim no more than that.
5. **Trend tests catch trends.** A growing trade network alone makes MST contraction look like a pre-crisis signal on any calendar; detrending removes most of it.

## 7. Limits

- No crises: swings are more even than real ones (swing-size variation 0.44 and 0.51 against 0.66).
- Intrinsic periods are the observed ones, which real coupling may already have pulled together.
- Masked trade links are no links: Russia has none before 1992, and Brazil receives none before 1989.
- 199 surrogates per test (floor 0.005) instead of 5,000: a rejection at 0.05 is exact, but floors are coarser than Paper 1's.
- Own-dated recessions use a simple rank rule (five lowest-growth years, at least 5 years apart), not Kose, Sugawara and Terrones's full method.
- One noise level for every economy; the world node pulls every economy equally; trade links only (no banks or oil).

## Files

`gnn/G1/calibration.json` (targets, grids, κ\*, φ\*), `r_curve.csv`, `pvalues.csv.gz` (every p-value of every world), `rejections.csv` (the tables above with intervals), `world_stats.csv.gz` (r overall, in own-dated recession years and by period), `rule_b_recessions.csv.gz` (each world's own recession years).
