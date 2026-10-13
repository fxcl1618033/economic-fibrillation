# Follow-up checks (not pre-registered)

Asked for by Sid after reading the Phase 3 results. Exploratory: these p-values are raw, not part of any
pre-registered family, and change no pre-registered result. Floors: 5,000 surrogates give p ≥ 0.0002.

## 1. Which recessions carry the rise in the variance of r(t)? (registry F2)

Kendall-type trend τ of the variance (and lag-1 autocorrelation) of r(t)'s fluctuations over the eight years
before each recession, averaged over the recessions in each row; one-sided p (rising) against the same 5,000
surrogates as Phase 3 (seed 101), convention P, 15-year windows from 1962. The 1975 recession has no defined
pre-window; 1982's is partly defined (S26: 6/8, S30: 6/8, S31: 6/8 years).

| Recessions | S26 variance τ (p) | S30 variance τ (p) | S31 variance τ (p) | S26 AR(1) τ (p) | S30 AR(1) τ (p) | S31 AR(1) τ (p) |
|---|---|---|---|---|---|---|
| All recessions used (as Phase 3) | +0.438 (0.0332) | +0.420 (0.0372) | +0.438 (0.0310) | +0.027 (0.4559) | -0.098 (0.6763) | -0.152 (0.7894) |
| 1982 alone | +0.321 (0.2853) | +0.464 (0.1266) | +0.393 (0.2052) | +0.250 (0.3135) | +0.250 (0.3169) | +0.250 (0.3167) |
| 1991 alone | -0.071 (0.5449) | -0.500 (0.7508) | -0.357 (0.6681) | +0.000 (0.5207) | -0.571 (0.8438) | -0.643 (0.8876) |
| 2009 alone | +0.643 (0.1984) | +0.857 (0.0744) | +0.929 (0.0392) | +0.071 (0.4715) | +0.071 (0.4841) | -0.071 (0.5553) |
| 2020 alone | +0.857 (0.0794) | +0.857 (0.0736) | +0.786 (0.1166) | -0.214 (0.6319) | -0.143 (0.5877) | -0.143 (0.5975) |
| Without 1982 | +0.476 (0.0512) | +0.405 (0.0844) | +0.452 (0.0654) | -0.048 (0.5665) | -0.214 (0.7894) | -0.286 (0.8740) |
| Without 1991 | +0.607 (0.0098) | +0.726 (0.0012) | +0.702 (0.0014) | +0.036 (0.4525) | +0.060 (0.4249) | +0.012 (0.4911) |
| Without 2009 | +0.369 (0.1232) | +0.274 (0.2002) | +0.274 (0.2060) | +0.012 (0.4931) | -0.155 (0.7205) | -0.179 (0.7632) |
| Without 2020 | +0.298 (0.1544) | +0.274 (0.1760) | +0.321 (0.1250) | +0.107 (0.3603) | -0.083 (0.6555) | -0.155 (0.7570) |
| Without 2009 and 2020 | +0.125 (0.4083) | -0.018 (0.5277) | +0.018 (0.5135) | +0.125 (0.3895) | -0.161 (0.7001) | -0.196 (0.7485) |
| 2009 and 2020 alone | +0.750 (0.0188) | +0.857 (0.0050) | +0.857 (0.0028) | -0.071 (0.5947) | -0.036 (0.5505) | -0.107 (0.6439) |

Source: `results/followup/<sample>/P/csd_by_event.json` (`ef.paper1.run_csd_by_event`).
