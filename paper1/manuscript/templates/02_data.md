<!-- Data: docs/methods.md §1 with the fifth-draft edits (docs/methods_proposed_edits.md, §1 Data). Section references use methods.md numbering. -->
## 1. Data

We use annual real GDP per capita from the Maddison Project Database (2023 release; Bolt and van Zanden 2024),
PPP-adjusted, for a fixed panel of $N = 31$ economies: Australia, Austria, Belgium, Brazil, Canada, China, Denmark,
Finland, France, Germany, Greece, India, Indonesia, Iran, Italy, Japan, Mexico, the Netherlands, Norway, Portugal,
Russia, Saudi Arabia, South Africa, South Korea, Spain, Sweden, Switzerland, Thailand, Turkey, the United Kingdom and
the United States. The panel is balanced: every economy has an uninterrupted annual observation from 1950 to 2022, so
no interpolation, gap-filling or unbalanced-panel weighting enters the pipeline at any stage. An earlier version of
this analysis used the first 26 of these economies. China, Russia and Brazil are the largest economies missing from
them, and Saudi Arabia and Iran add the oil-exporting Middle East; Russia, the second largest, was first left out by
oversight, not by the inclusion rule, and was added before any test was run on it. The inclusion rule, the phase
convention, the tests and their directions were written down before any test was run on the added economies (§8); the
rule admits an economy only with a complete Maddison series for 1950–2022, which excluded the United Arab Emirates
(its series misses 1991–1992). Russia's values before 1991 are back-cast estimates for the Soviet period, not market
national accounts, so every test that allows it is also run with Russia's phases computed from 1992 only (§7.8). In
Maddison's PPP figures the original 26 produced {{paper1/manuscript/sources/world_share.json#S26/1970|pct0}} of world
GDP in 1970 and {{paper1/manuscript/sources/world_share.json#S26/2022|pct0}} in 2022; the 31 produce
{{paper1/manuscript/sources/world_share.json#S31/1970|pct0}} and {{paper1/manuscript/sources/world_share.json#S31/2022|pct0}}
(without Russia, {{paper1/manuscript/sources/world_share.json#S31_without_RUS/1970|pct0}} and
{{paper1/manuscript/sources/world_share.json#S31_without_RUS/2022|pct0}}). Every result is also given without Russia,
for the 30 (§7.8 and Appendix Table A1).

We do not assert a price base year, and none is needed. The pipeline operates on demeaned logs: any multiplicative
rebasing constant $\kappa$ common to a series enters as $\ln(\kappa\,\mathrm{GDPpc}) = \ln\kappa + \ln \mathrm{GDPpc}$
and is removed exactly by the subsequent mean subtraction. Every quantity in this paper — cycles, phases, correlations,
order parameter — is therefore invariant to the choice of base year and to PPP rebasing.

Two distinct date ranges are used deliberately and should not be conflated. Filtering and phase extraction are
performed on the full 1950–2022 series, so that the band-pass filter and the Hilbert transform have run-in on both
sides of the analysis window. All statistics are then computed on the **1970–2022** window ($T = 53$ annual
observations), discarding the first two decades. This protects every reported quantity from the filter and Hilbert
edge transients, which are severe in short annual records. It is a consequential choice rather than a formality:
recomputing phases on a 1970–2022 series alone, with no run-in, changes the order parameter materially in individual
years, shifts the synchronization–amplitude coefficient of §6.2 by roughly
{{@diff:S31/P/amplitude#corr_detrended;S31/N/amplitude#corr_detrended|f1}} and moves the lead–lag profile of §6.3
(§7.2).
