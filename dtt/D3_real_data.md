# D3 — the effective number of economies on real data (descriptive only)

Computed by `python -m ef.dtt_real` (`src/ef/dtt_real.py`) from the Paper 1 pipeline: phases and swing sizes from the analytic signal, 1970–2022, convention P (the paper's) and C (past data only) beside it. **No p-values**: this describes, it does not test. Years: recessions 1975, 1982, 1991, 2009, 2020; lead-1 the year before each; normal years are neither recessions nor the downturns 1998, 2001, 2012 (Paper 1's definition).

## What is computed

- **N_eff = 1 / r²**, the report's effective number (equal swing sizes, the whole shock shared). Over a group of years it is summarized the report's way, **1 / E[r²]**, the variance-equivalent count. The arithmetic mean of the yearly 1/r² is not used: in years with r near 0 it explodes (it is 203 for S31 over all years). Medians of the yearly values are given beside.
- **1 / R_A²**, the amplitude-weighted version Sid asked for (1 / E[R_A²] over a group).
- **mean(A²) / |Z_A|²** (E[mean A²] / E[|Z_A|²] over a group), the count the variance law implies exactly when swing sizes differ. It equals (1 + CV_A²) / R_A², so it is 1/R_A² scaled up by the spread of swing sizes; with equal swing sizes the three coincide.

**Sid's cross-check (S26, convention P):** about 2.9 on average, 2.1 in recession years, 1.9 at lead-1, 1.04 in 2020. Computed: 2.88, 2.08, 1.86 and 1.042 — a match, with N_eff over a group taken as 1 / E[r²].

## N_eff = 1 / E[r²] by group (median of the yearly values in brackets)

| Sample | Convention | all years | recession years | lead-1 years | normal years | 2020 |
|---|---|---|---|---|---|---|
| S31 (N = 31) | P | 3.46 (4.48) | 2.36 (5.09) | 2.06 (2.61) | 3.50 (4.37) | 1.11 |
| S31 (N = 31) | C | 5.97 (13.38) | 2.18 (2.72) | 2.59 (2.62) | 7.17 (16.97) | 1.15 |
| S30 (N = 30) | P | 3.39 (4.25) | 2.30 (4.25) | 2.07 (2.59) | 3.44 (4.12) | 1.07 |
| S30 (N = 30) | C | 5.80 (10.14) | 2.23 (2.78) | 2.59 (2.73) | 6.89 (13.96) | 1.15 |
| S26 (N = 26) | P | 2.88 (3.60) | 2.08 (3.80) | 1.86 (2.55) | 2.90 (3.51) | 1.04 |
| S26 (N = 26) | C | 4.78 (8.32) | 1.75 (2.64) | 2.10 (2.71) | 5.80 (11.34) | 1.00 |

## Amplitude-weighted: 1 / E[R_A²], and the exact count E[mean A²] / E[|Z_A|²]

| Sample | Convention | all years | recession years | lead-1 years | normal years |
|---|---|---|---|---|---|
| S31 | P | 3.40 / 3.58 | 2.30 / 2.21 | 2.12 / 2.32 | 3.50 / 4.11 |
| S31 | C | 4.45 / 3.79 | 1.93 / 2.09 | 1.74 / 2.96 | 5.39 / 5.24 |
| S30 | P | 3.36 / 3.56 | 2.31 / 2.16 | 2.13 / 2.31 | 3.45 / 4.11 |
| S30 | C | 4.33 / 3.73 | 1.94 / 2.10 | 1.74 / 2.96 | 5.21 / 5.08 |
| S26 | P | 2.65 / 2.46 | 1.79 / 1.59 | 1.70 / 1.66 | 2.70 / 2.74 |
| S26 | C | 3.49 / 2.77 | 1.45 / 1.52 | 1.38 / 2.12 | 4.21 / 3.87 |

## Each recession year (S31)

| Year | N_eff, P | N_eff, C | the year before, P | the year before, C |
|---|---|---|---|---|
| 1975 | 5.09 | 2.72 | 2.61 | 2.62 |
| 1982 | 5.41 | 6.48 | 4.35 | 3.41 |
| 1991 | 9.83 | 5.71 | 9.51 | 4.31 |
| 2009 | 1.37 | 1.38 | 1.24 | 1.78 |
| 2020 | 1.11 | 1.15 | 1.10 | 2.15 |

**Reading.** On the 31 economies the world behaves, by this measure, like about 3.5 independent economies on average, 2.4 in recession years and 2.1 the year before, against 3.5 in normal years (convention P). The group values are pulled down by 2009 and 2020, when N_eff is close to 1; 1975, 1982 and 1991 are not low, and the median recession year is not below the median year. With past-only phases (C) the gap between normal years (7.2) and recession and lead-1 years (2.2, 2.6) is wider. Like every Paper 1 result on the lead, it rests on 2009 and 2020.

## N_eff and the variance decomposition's co-movement share

**Exact, instantaneous.** With equal weights and equal swing sizes, the variance law splits world variance into an own part 1/(2N) and the rest, so the co-movement (cross) share of world variance is exactly 1 − N_eff/N (checked on S31: largest error 5.7e-14). With weights wᵢ and swing sizes Aᵢ it is 1 − Σwᵢ²Aᵢ² / |Σwᵢ Aᵢ e^{iθᵢ}|².

**Over the decomposition's windows, close but not exact.** The decomposition (Methods 6.1) measures variance over 10-year windows in time, not over shock directions. The two coincide only when, inside a window, swing sizes and phase gaps are fixed and the common phase turns through whole cycles. On the real windows (Phase 3 settings, 1962–2022), the variance law averaged over each window against the decomposition itself:

| Sample | Weights | World variance, law ÷ actual (median) | Own variance, law ÷ actual (median) | Cross share: correlation across windows; mean gap | Cross share of the recession excess: actual / law |
|---|---|---|---|---|---|
| S31 | GDP (window mean) | 1.002 | 1.023 | 0.975; 2.3 points | 84.3% / 84.1% |
| S31 | equal | 1.007 | 1.021 | 0.987; 2.3 points | 97.0% / 96.4% |
| S30 | GDP (window mean) | 1.001 | 1.023 | 0.976; 2.2 points | 83.3% / 83.5% |
| S30 | equal | 1.004 | 1.020 | 0.989; 2.4 points | 96.8% / 96.1% |
| S26 | GDP (window mean) | 1.003 | 1.009 | 0.976; 1.7 points | 80.2% / 80.8% |
| S26 | equal | 0.998 | 1.014 | 0.986; 1.0 points | 96.5% / 97.0% |

So the decomposition's headline — the cross term supplies 84.3% of the extra world variance in recession windows on S31 (GDP weights) — is, to within a point (84.1% from the law), what the variance law gives when it is averaged over the same windows. That share is not a function of N_eff alone: it is ΔCROSS / (ΔOWN + ΔCROSS) between recession and normal windows, and own variances (swing sizes) rise in recessions too. What N_eff adds is the reading: a cross share of world variance of c means, with equal weights and swing sizes, the world varies like N(1 − c) independent economies of equal size.
