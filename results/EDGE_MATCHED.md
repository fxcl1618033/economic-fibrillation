# Edge-matched nulls — pre-registration amendment 4

Status: **for Sid's review.** Amendment 4 (`docs/preregistration_S30.md`, commit 864317a) listed the tests and fixed the null before anything ran; the code (fc63e87) was committed before the runs. `make edge-null` reruns everything (`python -m ef.edge_null validate | run | report`). Every number below is read from `results/edge_matched/` and `gnn/G1/`. The current p-values are unchanged and stay as reported (rule 6); the edge-matched p is a second null beside them.

## In short

- **The swing-size test's lean is gone under the edge-matched null.** In uncoupled G1 worlds on the real calendar it rejects in 1.5% (Kuramoto) and 4.8% (Stuart–Landau) of worlds, against 13.8% and 18.9% with the current surrogates. **The real result stands:** p = 0.0002 on S31, 0.0002 on S30 and 0.0002 on S26, the floor; the edge-matched null reproduces the lean (its mean is +0.045) and the real statistic (1.02) is far beyond it.
- **Validation.** Every edge-matched null rejects at about its correct 5% in uncoupled worlds, with one exception just above: Share of the excess from the cross term, GDP weights (Stuart–Landau, 6.4%). The multivariate arc null also holds in trade-coupled worlds (lead-1 4.4% and 4.9%), where circular shifts over-reject after-2 (11.6% in Kuramoto worlds); after-2 is 6.5% there with the new null, still a little high.
- **No claim of the paper changes.** The two-sided lead-1 stays below 0.05 (p 0.033 on S31, 0.043 on S30, 0.042 on S26; it was 0.019, the floor of the circular shifts, on all three). The past-only lead-1, which carries the lead claim, is not on the list. r with swing size, the cross term, Δcross and the variance rise keep their side of 0.05.
- **6 p-values cross 0.05, none of them a claim:** Arc, after-2, convention P on S31 (0.057 → 0.039); Arc, lead-1, convention W on S31 (0.019 → 0.056); Arc within the Fiedler blocs, lead-1 on S30 (0.019 → 0.050); Real-GDP channel arc, crisis year on S31 (0.094 → 0.046); Real-GDP channel arc, crisis year on S30 (0.094 → 0.050); Δown at recessions, GDP weights on S31 (0.038 → 0.053). Section 4 reads each one.
- **Resolution.** A circular-shift p moves in steps of 1/53 = 0.019 (0.019, 0.038, 0.057, …); an edge-matched p in steps of 1/5,001. Part of every arc crossing is this change of resolution, not new evidence.

## 1. The tests and the null

A test is on the list if a recession term of its statistic uses a year from 2019 to 2022 (amendment 4.1): the arc at lead-1, the crisis year, after-1 and after-2 (under P, and W, N and E); the bloc arcs; the real-GDP channel arc; the cross term (D5, D6); the identity (D11); MST contraction and fragility (E4, E6); the slowing-down trends (F1, F2); the recovery rate (F4); and, outside the rule, r with swing size (C1). Not listed: lead-2, every past-only (convention C) test, the phase-lead spread and the robustness variants.

The edge-matched surrogates are built from each economy's growth rates: a long series (8 × 72 values) with the same periodogram and random phases, a 72-year window from a random start, cumulated from the real 1950 level, then the same band-pass, Hilbert transform, convention and windows as the data. So the surrogates have ends, and the filters treat their last years as they treat 2019–2022. Tests whose current null is independent surrogates get the independent version; the arcs, whose current null is circular shifts, get the multivariate version (one random phase per frequency for every economy, which keeps co-movement and so r's level and persistence). 5,000 surrogates per sample, floor 0.0002.

## 2. Validation on the G1 worlds (amendment 4.3)

Share of the 1,000 uncoupled G1 worlds per model (κ = φ = 0, the worlds of `gnn/G1/`) in which each test rejects at p ≤ 0.05 on the real calendar, with its 95% interval; 199 surrogates per world. **Bold**: the interval lies above the correct rate (3.8% for circular shifts, 5% for surrogates). The current-null columns are the G1 results for the same worlds.

| Test | Registry | Kuramoto, current null | Kuramoto, edge-matched | Stuart–Landau, current null | Stuart–Landau, edge-matched |
|---|---|---|---|---|---|
| Arc, lead-1, convention P | A2 | 2.9% (2.0–4.1) | 5.4% (4.2–7.0) | 4.4% (3.3–5.9) | 6.1% (4.8–7.8) |
| Arc, crisis year, convention P | A3 | 4.4% (3.3–5.9) | 5.6% (4.3–7.2) | 3.3% (2.4–4.6) | 4.8% (3.6–6.3) |
| Arc, after-1, convention P | A4 | 4.5% (3.4–6.0) | 5.1% (3.9–6.6) | 3.6% (2.6–4.9) | 5.6% (4.3–7.2) |
| Arc, after-2, convention P | A5 | **6.2% (4.9–7.9)** | 5.9% (4.6–7.5) | 4.6% (3.5–6.1) | 4.8% (3.6–6.3) |
| Arc within the Fiedler blocs, lead-1 | E11 | — | 5.3% (4.1–6.9) | — | 5.8% (4.5–7.4) |
| Arc between the Fiedler blocs, lead-1 | E11 | — | 4.5% (3.4–6.0) | — | 3.6% (2.6–4.9) |
| Cross share at recessions, GDP weights | D5 | 5.3% (4.1–6.9) | 5.8% (4.5–7.4) | 5.4% (4.2–7.0) | 6.1% (4.8–7.8) |
| Cross share at recessions, equal weights | D5 | 4.6% (3.5–6.1) | 4.4% (3.3–5.9) | 4.6% (3.5–6.1) | 4.8% (3.6–6.3) |
| Share of the excess from the cross term, GDP weights | D6 | — | 4.0% (3.0–5.4) | — | **6.4% (5.0–8.1)** |
| Share of the excess from the cross term, equal weights | D6 | — | 3.4% (2.4–4.7) | — | 4.3% (3.2–5.7) |
| Δcross at recessions, GDP weights | D6 | — | 5.5% (4.2–7.1) | — | 6.0% (4.7–7.6) |
| Δcross at recessions, equal weights | D6 | — | 5.8% (4.5–7.4) | — | 5.3% (4.1–6.9) |
| Δown at recessions, GDP weights | D6 | — | 1.6% (1.0–2.6) | — | 4.7% (3.6–6.2) |
| Δown at recessions, equal weights | D6 | — | 1.5% (0.9–2.5) | — | 4.8% (3.6–6.3) |
| Identity: alignment at recessions | D11 | 4.8% (3.6–6.3) | 4.3% (3.2–5.7) | **6.5% (5.1–8.2)** | 5.8% (4.5–7.4) |
| Identity: swing size at recessions | D11 | **13.8% (11.8–16.1)** | 1.5% (0.9–2.5) | **18.9% (16.6–21.4)** | 4.8% (3.6–6.3) |
| MST contraction before recessions | E4 | 2.8% (1.9–4.0) | 3.5% (2.5–4.8) | 4.1% (3.0–5.5) | 4.8% (3.6–6.3) |
| MST contraction, detrended | E4 | 3.0% (2.1–4.3) | 4.1% (3.0–5.5) | 4.5% (3.4–6.0) | 4.6% (3.5–6.1) |
| MST fragility before recessions | E6 | 4.9% (3.7–6.4) | 5.2% (4.0–6.8) | 5.2% (4.0–6.8) | 5.3% (4.1–6.9) |
| Slowing down: autocorrelation of r | F1 | 5.1% (3.9–6.6) | 5.3% (4.1–6.9) | 4.2% (3.1–5.6) | 4.2% (3.1–5.6) |
| Slowing down: variance of r | F2 | 5.1% (3.9–6.6) | 5.0% (3.8–6.5) | 6.1% (4.8–7.8) | 6.1% (4.8–7.8) |
| Slower recovery after recessions | F4 | 4.8% (3.6–6.3) | 5.4% (4.2–7.0) | 4.5% (3.4–6.0) | 5.1% (3.9–6.6) |
| r with swing size, detrended (outside the rule) | C1 | 5.5% (4.2–7.1) | 5.6% (4.3–7.2) | 5.4% (4.2–7.0) | 5.5% (4.2–7.1) |

The multivariate arc null in the 1,000 trade-coupled G1 worlds per model (κ\*), real calendar:

| Test | Kuramoto κ\*, circular shifts | Kuramoto κ\*, edge-matched (multivariate) | Stuart–Landau κ\*, circular shifts | Stuart–Landau κ\*, edge-matched |
|---|---|---|---|---|
| Arc, lead-1, convention P | 3.6% (2.6–4.9) | 4.4% (3.3–5.9) | 4.0% (3.0–5.4) | 4.9% (3.7–6.4) |
| Arc, crisis year, convention P | 3.0% (2.1–4.3) | 3.9% (2.9–5.3) | 3.3% (2.4–4.6) | 4.6% (3.5–6.1) |
| Arc, after-1, convention P | **5.9% (4.6–7.5)** | 5.4% (4.2–7.0) | 4.4% (3.3–5.9) | 6.3% (5.0–8.0) |
| Arc, after-2, convention P | **11.6% (9.8–13.7)** | **6.5% (5.1–8.2)** | **6.4% (5.0–8.1)** | 4.7% (3.6–6.2) |
| Arc within the Fiedler blocs, lead-1 | — | 4.6% (3.5–6.1) | — | 5.1% (3.9–6.6) |
| Arc between the Fiedler blocs, lead-1 | — | 3.1% (2.2–4.4) | — | 4.7% (3.6–6.2) |

The G1 run drew the cross-term and MST surrogates from the 1962–2022 cycles (the as-run scheme); Phase 3 draws them from the 1950–2022 cycles and cuts them. Both, on the same uncoupled worlds:

| Test | Kuramoto, as G1 ran it (1962–2022 cycles) | Kuramoto, Phase 3 scheme (1950–2022 cycles, cut) | Stuart–Landau, as G1 ran it | Stuart–Landau, Phase 3 scheme |
|---|---|---|---|---|
| Cross share at recessions, GDP weights | 5.3% (4.1–6.9) | 5.6% (4.3–7.2) | 5.4% (4.2–7.0) | 5.3% (4.1–6.9) |
| Cross share at recessions, equal weights | 4.6% (3.5–6.1) | 4.6% (3.5–6.1) | 4.6% (3.5–6.1) | 5.0% (3.8–6.5) |
| MST contraction before recessions | 2.8% (1.9–4.0) | 3.6% (2.6–4.9) | 4.1% (3.0–5.5) | 4.3% (3.2–5.7) |
| MST contraction, detrended | 3.0% (2.1–4.3) | 3.5% (2.5–4.8) | 4.5% (3.4–6.0) | 4.8% (3.6–6.3) |
| MST fragility before recessions | 4.9% (3.7–6.4) | 4.8% (3.6–6.3) | 5.2% (4.0–6.8) | 5.3% (4.1–6.9) |

The two schemes agree to within a point, so the G1 rows stand as reported.

## 3. Real data: the current and the edge-matched p

Statistic, current p and edge-matched p; **bold** where the two fall on opposite sides of 0.05. Circular-shift p (the arcs, rows A–G3 under "p now") has floor 0.019; surrogate p has floor 0.0002. Δcross and Δown are in units of world variance (tiny numbers); the share ratio is a fraction.

| Test | Registry | S31: statistic | S31: p now | S31: p edge-matched | S30: statistic | S30: p now | S30: p edge-matched | S26: statistic | S26: p now | S26: p edge-matched |
|---|---|---|---|---|---|---|---|---|---|---|
| Arc, lead-1, convention P | A2 | +0.231 | 0.019 | 0.033 | +0.217 | 0.019 | 0.043 | +0.216 | 0.019 | 0.042 |
| Arc, crisis year, convention P | A3 | +0.159 | 0.189 | 0.116 | +0.161 | 0.189 | 0.108 | +0.149 | 0.189 | 0.123 |
| Arc, after-1, convention P | A4 | +0.099 | 0.717 | 0.760 | +0.111 | 0.755 | 0.786 | +0.078 | 0.679 | 0.707 |
| Arc, after-2, convention P | A5 | -0.258 | 0.057 | **0.039** | -0.236 | 0.057 | 0.054 | -0.277 | 0.019 | 0.026 |
| Arc, lead-1, convention W | A10 | +0.204 | 0.019 | **0.056** | +0.184 | 0.057 | 0.079 | +0.178 | 0.094 | 0.085 |
| Arc, crisis year, convention W | A10 | +0.134 | 0.189 | 0.161 | +0.130 | 0.226 | 0.167 | +0.112 | 0.208 | 0.198 |
| Arc, after-1, convention W | A10 | +0.109 | 0.774 | 0.784 | +0.121 | 0.774 | 0.806 | +0.088 | 0.698 | 0.734 |
| Arc, after-2, convention W | A10 | -0.165 | 0.113 | 0.142 | -0.131 | 0.170 | 0.204 | -0.144 | 0.170 | 0.177 |
| Arc, lead-1, convention N | A11 | +0.192 | 0.057 | 0.071 | +0.173 | 0.094 | 0.093 | +0.178 | 0.094 | 0.083 |
| Arc, crisis year, convention N | A11 | +0.135 | 0.208 | 0.156 | +0.133 | 0.189 | 0.158 | +0.124 | 0.189 | 0.168 |
| Arc, after-1, convention N | A11 | +0.105 | 0.755 | 0.775 | +0.116 | 0.774 | 0.800 | +0.089 | 0.679 | 0.737 |
| Arc, after-2, convention N | A11 | -0.190 | 0.094 | 0.101 | -0.158 | 0.132 | 0.151 | -0.197 | 0.094 | 0.088 |
| Arc, lead-1, convention E | A12 | +0.236 | 0.019 | 0.029 | +0.226 | 0.019 | 0.037 | +0.220 | 0.019 | 0.038 |
| Arc, crisis year, convention E | A12 | +0.159 | 0.189 | 0.110 | +0.164 | 0.170 | 0.103 | +0.152 | 0.170 | 0.118 |
| Arc, after-1, convention E | A12 | +0.101 | 0.755 | 0.780 | +0.107 | 0.755 | 0.794 | +0.075 | 0.717 | 0.719 |
| Arc, after-2, convention E | A12 | -0.160 | 0.132 | 0.090 | -0.136 | 0.170 | 0.120 | -0.170 | 0.113 | 0.080 |
| Arc within the Fiedler blocs, lead-1 | E11 | +0.250 | 0.019 | 0.023 | +0.212 | 0.019 | **0.050** | +0.182 | 0.057 | 0.082 |
| Arc between the Fiedler blocs, lead-1 | E11 | +0.066 | 0.358 | 0.354 | +0.135 | 0.151 | 0.152 | +0.180 | 0.038 | 0.025 |
| Real-GDP channel arc, lead-1 | G3 | +0.254 | 0.019 | 0.020 | +0.245 | 0.019 | 0.023 | +0.237 | 0.019 | 0.025 |
| Real-GDP channel arc, crisis year | G3 | +0.208 | 0.094 | **0.046** | +0.202 | 0.094 | **0.050** | +0.192 | 0.094 | 0.061 |
| Real-GDP channel arc, after-2 | G3 | -0.320 | 0.019 | 0.018 | -0.291 | 0.019 | 0.029 | -0.332 | 0.019 | 0.015 |
| Cross share at recessions, GDP weights | D5 | +0.706 | 0.0002 | 0.0002 | +0.707 | 0.0002 | 0.0002 | +0.704 | 0.0002 | 0.0002 |
| Cross share at recessions, equal weights | D5 | +0.783 | 0.0002 | 0.0002 | +0.771 | 0.0002 | 0.0002 | +0.876 | 0.0002 | 0.0002 |
| Share of the excess from the cross term, GDP weights | D6 | +0.843 | 0.316 | 0.319 | +0.833 | 0.319 | 0.313 | +0.802 | 0.344 | 0.349 |
| Share of the excess from the cross term, equal weights | D6 | +0.970 | 0.478 | 0.476 | +0.968 | 0.466 | 0.459 | +0.965 | 0.476 | 0.466 |
| Δcross at recessions, GDP weights | D6 | +4.17e-05 | 0.0002 | 0.0002 | +4.48e-05 | 0.0002 | 0.0002 | +5.72e-05 | 0.0002 | 0.0002 |
| Δcross at recessions, equal weights | D6 | +4.72e-05 | 0.0002 | 0.0002 | +4.97e-05 | 0.0002 | 0.0002 | +5.22e-05 | 0.0002 | 0.0002 |
| Δown at recessions, GDP weights | D6 | +7.78e-06 | 0.038 | **0.053** | +8.96e-06 | 0.035 | 0.047 | +1.41e-05 | 0.0002 | 0.0002 |
| Δown at recessions, equal weights | D6 | +1.46e-06 | 0.0002 | 0.0004 | +1.65e-06 | 0.0002 | 0.0004 | +1.88e-06 | 0.0002 | 0.0002 |
| Identity: alignment at recessions | D11 | +0.406 | 0.239 | 0.228 | +0.241 | 0.356 | 0.355 | +0.654 | 0.103 | 0.105 |
| Identity: swing size at recessions | D11 | +1.021 | 0.0002 | 0.0002 | +1.033 | 0.0002 | 0.0002 | +1.010 | 0.0002 | 0.0002 |
| MST contraction before recessions | E4 | -0.157 | 0.206 | 0.185 | -0.143 | 0.219 | 0.216 | -0.171 | 0.168 | 0.166 |
| MST contraction, detrended | E4 | +0.014 | 0.561 | 0.524 | +0.057 | 0.659 | 0.624 | -0.057 | 0.356 | 0.338 |
| MST fragility before recessions | E6 | +0.129 | 0.271 | 0.252 | +0.086 | 0.338 | 0.336 | +0.100 | 0.311 | 0.299 |
| Slowing down: autocorrelation of r | F1 | -0.152 | 0.789 | 0.770 | -0.098 | 0.676 | 0.678 | +0.027 | 0.456 | 0.456 |
| Slowing down: variance of r | F2 | +0.438 | 0.031 | 0.029 | +0.420 | 0.037 | 0.037 | +0.438 | 0.033 | 0.036 |
| Slower recovery after recessions | F4 | +2.26e-03 | 0.502 | 0.478 | +0.024 | 0.507 | 0.488 | +0.078 | 0.534 | 0.517 |
| r with swing size, detrended (outside the rule) | C1 | +0.646 | 0.0002 | 0.0002 | +0.641 | 0.0002 | 0.0002 | +0.608 | 0.0002 | 0.0006 |

## 4. The crossings, one by one

- **Arc, after-2, convention P, S31: 0.057 → 0.039.** After-2 (A5) is already a Limitation. Under the edge-matched null it is significant on S31 but not on S30, and the new null still over-rejects after-2 slightly in trade-coupled Kuramoto worlds; the move from 0.057 is mostly resolution (0.057 is the third-smallest circular-shift p). It stays a Limitation, not a result.
- **Arc, lead-1, convention W, S31: 0.019 → 0.056.** Lead-1 under convention W (A10) is a sensitivity convention; the lead claim rests on the past-only phases, which are not affected.
- **Arc within the Fiedler blocs, lead-1, S30: 0.019 → 0.050.** The within-bloc arc (E11) is exploratory; it lands on 0.050 on S30 and stays below 0.05 on S31.
- **Real-GDP channel arc, crisis year, S31: 0.094 → 0.046.** The real-GDP channel's crisis-year arc is not a registered result (the registry reports lead-1 and after-2 for this channel); it moves from 0.094 to the 0.05 line.
- **Real-GDP channel arc, crisis year, S30: 0.094 → 0.050.** The real-GDP channel's crisis-year arc is not a registered result (the registry reports lead-1 and after-2 for this channel); it moves from 0.094 to the 0.05 line.
- **Δown at recessions, GDP weights, S31: 0.038 → 0.053.** Δown with GDP weights (D6) is a disclosure value; it moves from 0.038 to 0.053 on S31 (S30 stays below 0.05). The validation shows this null is, if anything, conservative.

## 5. What it changes for Paper 1

- The swing-size p (D11) can be quoted: it stays at the floor under a null with the same ends.
- Lead-1's two-sided p is no longer the floor value but stays below 0.05 on every sample; the claim rests on the past-only version in any case (proposed edits, L8).
- After-2 stays in Limitations (L3); its edge-matched p is added there.
- The proposed Methods edits gain §5.3 (the κ = 0 table as a validation of test size) and §5.4 (this null), and the Limitations L8 and L9 (Sid, 14 October 2026).
