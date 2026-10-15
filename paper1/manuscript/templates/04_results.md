<!-- Results: Sid's five main-text claims (15 October 2026), S31 main, S30 and S26 as sensitivity, convention P primary.
     Drafts L1, L5, L7 of docs/methods_proposed_edits.md, rewritten to Sid's defaults. -->
## 4 Results

Synchronization among the 31 economies is far from constant (Figure 1, F1.3). The order parameter ranges from
{{@min_r:S31,min|f2}} ({{@argmin_r:S31,min|yr}}) to {{@min_r:S31,max|f2}} ({{@argmin_r:S31,max|yr}}) and averages
{{S31/P/arc#mean_ci/recession/0|f2}} in global-recession years, {{S31/P/arc#mean_ci/normal/0|f2}} in normal years and
{{S31/P/arc#mean_ci/downturn/0|f2}} in the milder global downturns of 1998, 2001 and 2012 (descriptive; 95% bootstrap
intervals in Appendix Table A6). In the two most recent recessions nearly every economy contracted together:
{{S31/P/channels#contracting/2009|int}} of the 31 in 2009 and {{S31/P/channels#contracting/2020|int}} in 2020, against
{{S31/P/channels#contracting/1982|int}} in 1982 and {{S31/P/channels#contracting/1991|int}} in 1991 (Global Macro
Database real GDP). Five results follow; every other test, including those that came out null, is reported in the
Methods (§3.5–§3.6) and the Appendix.

![**Figure 1 (F1.3).** The Kuramoto order parameter $r(t)$ of the 31 economies, 1970–2022, convention P. Red bands: the
five global recessions. The dotted line is the mean of $r$ under independent random phases.](../../figures/01_method/F1-03_order_parameter_s31.png)

### 4.1 Synchronization and swing size move together

When the economies' cycles are more aligned, they are also larger. After removing slow trends, the correlation between
$r(t)$ and the mean swing size $\bar A(t)$ is {{S31/P/amplitude#corr_detrended|c3}} over 1970–2022 (Figure 2, F4.1).
No circular shift of one series against the other does better ($p =$ {{S31/P/amplitude#p_shift|p}}, the floor), and no
one of 5,000 sets of spectrum-preserving surrogate economies does either ($p =$ {{S31/P/amplitude#p_surrogate|p}}, the
floor). The link holds on the 30 ({{S30/P/amplitude#corr_detrended|c3}}) and the original 26
({{S26/P/amplitude#corr_detrended|c3}}), without Iran and Saudi Arabia, whose swings are the largest
({{S31_minus_IRN_SAU/P/amplitude#corr_detrended|c3}}), and under every phase convention, including phases from past data
only ({{S31/P/conventions#C/amp_detrended/0|c3}}); its size depends on the convention (§3.6.2). This test uses no
recession dates.

![**Figure 2 (F4.1).** Synchronization $r(t)$ and mean swing size $\bar A(t)$, each minus a Gaussian-smoothed trend
($\sigma = 8$ years) and standardized. Red bands: global recessions.](../../figures/04_amplitude_diversification/F4-01_amplitude_s31.png)

### 4.2 Recession variance is mostly co-movement

In global recessions the world economy loses diversification: the economies' cycles stop offsetting one another. On
rolling 10-year windows the variance of the GDP-weighted world cycle splits exactly into an own term (each economy's
volatility) and a cross term (co-movement). The cross term supplies
{{S31/P/diversification#gdp_mean/cross_fraction_of_excess|pct1}} of the extra world variance in recession windows
({{S31/P/diversification#equal/cross_fraction_of_excess|pct1}} with equal weights; on the 30,
{{S30/P/diversification#gdp_mean/cross_fraction_of_excess|pct1}} and {{S30/P/diversification#equal/cross_fraction_of_excess|pct1}};
Figure 3, F4.4). This is a descriptive magnitude, not a significance claim: the share has no proper null (§3.6.6), and
the cross term dominates world variance in any period because 465 pairs outnumber 31 variances (§3.5.1). What is
specific to recessions is the gap: the cross term's share of world variance is
{{S31/P/diversification#gdp_mean/cross_share_crisis|f3}} in recession windows against
{{S31/P/diversification#gdp_mean/cross_share_normal|f3}} in normal ones.

The cross term rises for two reasons, and they are of similar size. Raising only the pairwise correlations from their
normal to their recession means supplies {{S31/P/cross_split#gdp_mean/from_correlation|pct0}} of its rise; raising only
the swing sizes supplies {{S31/P/cross_split#gdp_mean/from_swing_size|pct0}}; their interaction the remaining
{{S31/P/cross_split#gdp_mean/interaction|pct0}}. We read this as **amplification transmitted by alignment**: larger
swings matter for world output because they are aligned, and which of the two parts is larger depends on the sample
(on the original 26, swing size {{S26/P/cross_split#gdp_mean/from_swing_size|pct0}} against correlation
{{S26/P/cross_split#gdp_mean/from_correlation|pct0}}).

The same arithmetic can be written for a single year (Box 1, §5.2). If a common shock reaches each economy according to
where it is in its cycle, the world response has the variance of $N_{\mathrm{eff}} = 1/r^2$ independent economies:
with the phases spread out the 31 economies behave like 31, with the phases aligned they behave like one. Over
1970–2022, $N_{\mathrm{eff}} = 1/E[r^2]$ is about {{dtt/results/d3_neff.json#S31/P/all years/neff|f1}} on average,
{{dtt/results/d3_neff.json#S31/P/recession years/neff|f1}} in recession years and
{{dtt/results/d3_neff.json#S31/P/lead-1 years/neff|f1}} in the year before, and
{{dtt/results/d3_neff.json#S31/P/by_year/2020/neff|f1}} in 2020 (descriptive; Appendix Table A7). The dip is carried by
2009 ({{dtt/results/d3_neff.json#S31/P/by_year/2009/neff|f2}}) and 2020
({{dtt/results/d3_neff.json#S31/P/by_year/2020/neff|f2}}); the earlier recession years are not low
(1975 {{dtt/results/d3_neff.json#S31/P/by_year/1975/neff|f1}}, 1982 {{dtt/results/d3_neff.json#S31/P/by_year/1982/neff|f1}},
1991 {{dtt/results/d3_neff.json#S31/P/by_year/1991/neff|f1}}). Averaged over the decomposition's windows the variance law
gives the cross term {{dtt/results/d3_neff.json#S31/decomposition/gdp_mean/excess_from_cross_law|pct1}} of the extra
recession variance, against the {{dtt/results/d3_neff.json#S31/decomposition/gdp_mean/excess_from_cross|pct1}} measured:
the loss of diversification is this arithmetic, and it is an accounting of the recession excess, not a cause of it.

![**Figure 3 (F4.4).** (a) World cycle variance on 10-year windows split into the own term and the cross term,
GDP-weighted. (b) The cross term's share of world variance in normal and recession windows. No p-value is shown: the
share has no proper null (§3.6.6).](../../figures/04_amplitude_diversification/F4-04_diversification_s31.png)

### 4.3 The network has tightened

The correlation network of the 31 business cycles has tightened over five decades. The mean edge length of its minimum
spanning tree fell from {{S31/P/mst#L_decade_means/1979-1989|f3}} in 1979–89 to {{S31/P/mst#L_decade_means/2013-2022|f3}}
in 2013–22, a factor of {{@mst_ratio:S31|x1}} (Figure 4, F5.1; {{@mst_ratio:S30|x1}} on the 30 and
{{@mst_ratio:S26|x1}} on the original 26). This is a description of a trend, not a test. The network does not contract
in the years before recessions ($\tau =$ {{S31/P/mst#tau_L|c3}}, $p =$ {{S31/P/mst#p_contraction|p}}; §3.5.5), and the
economies move too nearly together for a leader to be identified: the spread of their phase leads is
{{S31/P/phase_lags#sd|f3}} years, below every one of 5,000 surrogates ($p =$ {{S31/P/phase_lags#p_spread_lower|p}},
the floor; §3.5.6).

![**Figure 4 (F5.1).** (a) Mean edge length of the minimum spanning tree of the 31 business cycles on 10-year windows,
with the decade means for 1979–89 and 2013–22. (b) The tree for 2013–2022.](../../figures/05_network_phase/F5-01_mst_s31.png)

### 4.4 Synchronization rises in the year before global recessions

With phases built from past data only — the version that uses no information from after each year — synchronization
is higher in the year before global recessions: the lead-1 correlation is {{S31/P/conventions#C/arc/lead1/corr|c3}}
($p =$ {{S31/P/conventions#C/arc/lead1/p|p}} against 53 circular shifts, whose floor is 0.019), **and it rests on two
events, 2009 and 2020 ($n \approx 2$)**: without either the two-sided lead is not significant ($p =$
{{S31/P/robustness#without 2009/lead1/1|p}} and {{S31/P/robustness#without 2020/lead1/1|p}}), and without both it is
gone ({{S31/P/robustness#without 2009 AND 2020/lead1/0|c2}}). With China left out the past-only lead-1 is
{{S31_minus_CHN/P/conventions#C/arc/lead1/corr|c3}} ($p =$ {{S31_minus_CHN/P/conventions#C/arc/lead1/p|p}}). With the
usual two-sided phases the lead-1 correlation is {{S31/P/arc#arc/lead1/corr|c3}}, at the floor of the circular-shift
null ($p =$ {{S31/P/arc#arc/lead1/p|p}}) and $p =$ {{results/edge_matched/S31.json#tests/arc.P.lead1/p_edge|p}} against
surrogates with ends (§3.4.4); it survives the removal of any one of the 31 economies ($p \le$
{{@loo_range:S31,lead1,p,max|p}}; Appendix Table A3) and the edge-robust convention ($p =$
{{S31/P/conventions#E/arc/lead1/p|p}}), but not convention N ($p =$ {{S31/P/conventions#N/arc/lead1/p|p}}), and it does
not pass a correction for testing five lags, which with 53 shifts a single lag cannot do (§3.6.4). We lead with the
past-only value because the two-sided arc is inflated by how recessions are dated (Limitations). On the 30 the
past-only lead-1 is {{S30/P/conventions#C/arc/lead1/corr|c3}} ($p =$ {{S30/P/conventions#C/arc/lead1/p|p}}) and on the 26
{{S26/P/conventions#C/arc/lead1/corr|c3}} ($p =$ {{S26/P/conventions#C/arc/lead1/p|p}}).

The rest of the arc is not claimed (Figure 5, F2.5). The two-year lead (lead-2 {{S31/P/arc#arc/lead2/corr|c3}},
$p =$ {{S31/P/arc#arc/lead2/p|p}}) does not survive past-only phases ({{S31/P/conventions#C/arc/lead2/corr|c3}},
$p =$ {{S31/P/conventions#C/arc/lead2/p|p}}). The crisis year is not significant with two-sided phases
($p =$ {{S31/P/arc#arc/crisis/p|p}}); with past-only phases it is at the floor
({{S31/P/conventions#C/arc/crisis/corr|c3}}, $p =$ {{S31/P/conventions#C/arc/crisis/p|p}}), which was not a
pre-registered claim and is reported, not interpreted. The fall two years after recessions
({{S31/P/arc#arc/after2/corr|c3}}, $p =$ {{S31/P/arc#arc/after2/p|p}}) is in the Limitations. This is a property of the
tightly coupled modern economy, observed twice; it is not a fifty-year regularity and not a forecast.

![**Figure 5 (F2.5).** Correlation of $r(t)$ with the recession indicator at each lag, with two-sided phases
(convention P) and phases from past data only (convention C). One-sided $p$ against 53 circular shifts (floor 0.019);
bold: $p \le 0.05$.](../../figures/02_crisis_arc/F2-05_arc_tested_s31.png)

### 4.5 No critical slowing down

Before recessions the variance of synchronization rises ($\tau =$ {{S31/P/csd#tau_var|c3}}, $p =$
{{S31/P/csd#p_var|p}} against 5,000 surrogates; $p =$ {{results/edge_matched/S31.json#tests/F2/p_edge|p}} against
surrogates with ends) while its lag-1 autocorrelation does not ($\tau =$ {{S31/P/csd#tau_ar1|c3}}, $p =$
{{S31/P/csd#p_ar1|p}}), and the recovery rate does not fall after recessions ($p =$
{{S31/P/bifurcation#p_slowing_post|p}}; Figure 6, F6.1). Critical slowing down — the signature of a system approaching
a bifurcation — raises variance and autocorrelation together, because both come from a slower return to equilibrium.
A rise in variance alone is not that signature. *As an interpretation, not a test:* it is what noise-induced tipping
would show, where larger disturbances push the system across a threshold while its restoring forces stay the same
(Ashwin et al. 2012). The variance rise, like the lead, rests on 2009 and 2020 (before them alone
{{followup/S31/P/csd_by_event#sets/only_2009_2020/tau_var|c3}}, $p =$
{{followup/S31/P/csd_by_event#sets/only_2009_2020/p_var|p}}; before 1982 and 1991,
{{followup/S31/P/csd_by_event#sets/without_2009_2020/tau_var|c3}}, $p =$
{{followup/S31/P/csd_by_event#sets/without_2009_2020/p_var|p}}; Appendix Table A8), and it is significant under
conventions P and E but not W or N (§3.5.7).

![**Figure 6 (F6.1).** Variance (a) and lag-1 autocorrelation (b) of the fluctuations of $r(t)$ on trailing 15-year
windows. Yellow: the eight years before each recession, over which the trend is measured.](../../figures/06_tipping_nulls/F6-01_early_warning_s31.png)
