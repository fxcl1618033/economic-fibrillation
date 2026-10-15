<!-- Appendix: every robustness table, sample comparison, leave-one-out, the phase-convention table, the kappa = 0 table, the
     edge-matched comparison and the multiplicity note (Sid, 15 October 2026). Every table is built from results files by
     ef.manuscript.tables. -->
## Appendix

All values are convention P unless a row says otherwise; one-sided $p$ in brackets. Circular-shift $p$-values have a
floor of $1/53 = 0.019$ (for the split samples of 26 and 27 years, 0.038 and 0.037); surrogate $p$-values with 5,000 draws have
a floor of 0.0002, with 2,000 draws 0.0005.

### Table A1. Key results by sample

The original 26 economies, the 30 (without Russia), the 31, the 31 without each added economy, with Russia's phases from
1992 only and without Iran and Saudi Arabia together. "—": not run (the variant without Iran and Saudi Arabia was
pre-registered for the swing-size tests only, the one with Russia from 1992 for the circular-shift tests only).

{{table:A1}}

### Table A2. Robustness of the arc

Correlation of $r(t)$ with the recession indicator at each lag (one-sided $p$; after-2 tested downward). 2–9 year band
unless stated.

*The 31 economies.*

{{table:robust_S31}}

*The 30 economies (without Russia).*

{{table:robust_S30}}

*The original 26 economies.*

{{table:robust_S26}}

### Table A3. Leave one economy out (31 economies)

{{table:loo_S31}}

### Table A4. Surrogates with ends

Each test whose statistic uses a year from 2019 to 2022, with its $p$ against the null used in the paper and, after the
arrow, against 5,000 surrogates with ends (§3.4.4). **Bold**: the two fall on opposite sides of 0.05. Multivariate
surrogates for the arcs, independent ones otherwise.

{{table:edge}}

### Table A5. Multiplicity

Raw one-sided $p$, Bonferroni-adjusted $p$ and Benjamini–Hochberg $q$ over the five lags of the arc.

{{table:multiplicity}}

*Note.* With 53 circular shifts the smallest raw $p$ is $1/53 = 0.019$, so the smallest Bonferroni-adjusted value over
five lags is $5/53 = 0.094$: no single lag can pass Bonferroni at 0.05. Under Benjamini–Hochberg a lag at the floor
passes only if a second lag is also at the floor (or four lags are at 0.038 or below), which happened on the original
26 (lead-1 and after-2) and not on the 30 or the 31. Corrected significance is therefore not what supports lead-1; its
support is that it survives past-only phases and the removal of any one economy, and it rests on 2009 and 2020.

### Table A6. Mean synchronization by period type and around recessions

Mean $r$ with 95% bootstrap intervals (10,000 draws), and the superposed epoch: mean $r$ from four years before to four
years after the five recessions. Descriptive.

{{table:meanr}}

### Table A7. Effective number of independent economies

$N_{\mathrm{eff}} = 1/E[r^2]$ over each group of years (Box 1), with two-sided (P) and past-only (C) phases; the year
before means the years before the five recessions. Descriptive.

{{table:neff}}

*By recession year, 31 economies:*

{{table:neff_recessions}}

### Table A8. The variance and autocorrelation trends by recession

The early-warning trends of §3.5.7 with each recession alone, left out, or in pairs (31 economies; same surrogates and
seed as the pre-registered test). Not pre-registered; asked for after the main run.

{{table:csd_by_event}}

### Table A9. Rolling windows kept inside 1970–2022

{{table:strict}}

### Table A10. Channels inside the economies

Synchronization of three channels from the Global Macro Database (an economy enters a channel only with continuous data
from 1965), with two-sided phases and with phases from past data only. Description only: no channel lead survives
past-only phases except real GDP's lead-1.

{{table:channels}}

### Table A11. G1b: the escape layer, every setting and sensitivity

Past-only lead-1 on 1,000 simulated worlds per row (§5.4). Differences in percentage points, paired by world.

{{table:g1b}}

### Table A12. The arc under every phase convention

Every lag, three samples (Table 2 gives the summary for the 31).

{{table:conv_full}}

### Table A13. Test size in every G1 setting

The share of 1,000 simulated worlds in which each test rejects at $p \le 0.05$, for each model (K: Kuramoto; SL:
Stuart–Landau) and coupling (none, common forcing $\varphi^*$, trade links at half and at the full calibrated $\kappa^*$).
**Bold**: the 95% interval lies above the correct rate (3.8% for circular shifts, 5% for 199 surrogates). Only the
"none" columns measure size; the others show what each test does when coupling is there. Table 1 (§3.4.3) is the
"none" columns with both dating rules.

{{table:g1_full}}

### Supplementary figures

Redrawn for this version (31 economies, convention P): F1.3, F2.5, F4.1, F4.4, F5.1 and F6.1 (main text); F4.5 (both
weightings) and F5.4 (Methods diagnostics). Every other figure in the project's figure catalogue (`docs/FIGURES.md`)
predates the 31-economy sample and is supplementary only; its status there says whether it uses the 26 economies,
convention W or superseded data.
