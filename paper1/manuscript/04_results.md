## 4 Results

Synchronization among the 31 economies is far from constant (Figure 1, F1.3). The order parameter ranges from
0.01 (1985) to 0.95 (2019) and averages
0.60 in global-recession years, 0.48 in normal years and
0.30 in the milder global downturns of 1998, 2001 and 2012 (descriptive; 95% bootstrap
intervals in Appendix Table A6). In the two most recent recessions nearly every economy contracted together:
25 of the 31 in 2009 and 28 in 2020, against
9 in 1982 and 9 in 1991 (Global Macro
Database real GDP). Five results follow; every other test, including those that came out null, is reported in the
Methods (§3.5–§3.6) and the Appendix.

![**Figure 1 (F1.3).** The Kuramoto order parameter $r(t)$ of the 31 economies, 1970–2022, convention P. Grey bands:
the five global recessions. Dotted line: the mean of $r$ under independent random phases.](../../figures/01_method/F1-03_order_parameter_s31.png)

### 4.1 Synchronization and swing size move together

When the economies' cycles are more aligned, they are also larger. After removing slow trends, the correlation between
$r(t)$ and the mean swing size $\bar A(t)$ is +0.646 over 1970–2022 (Figure 2, F4.1).
No circular shift of one series against the other does better ($p =$ 0.019, the floor), and no
one of 5,000 sets of spectrum-preserving surrogate economies does either ($p =$ 0.0002, the
floor). The link holds on the 30 (+0.641) and the original 26
(+0.608), without Iran and Saudi Arabia, whose swings are the largest
(+0.625), and under every phase convention, including phases from past data
only (+0.726); its size depends on the convention (§3.6.2). This test uses no
recession dates.

![**Figure 2 (F4.1).** Synchronization and swing size. (a) $r(t)$ and the mean swing size $\bar A(t)$, each minus a
Gaussian-smoothed trend ($\sigma = 8$ years) and standardized; grey bands: global recessions. (b) The same 53 years as
pairs, recession years in blue, with the least-squares line.](../../figures/04_amplitude_diversification/F4-01_amplitude_s31.png)

### 4.2 Recession variance is mostly co-movement

In global recessions the world economy loses diversification: the economies' cycles stop offsetting one another. On
rolling 10-year windows the variance of the GDP-weighted world cycle splits exactly into an own term (each economy's
volatility) and a cross term (co-movement). The cross term supplies
84.3% of the extra world variance in recession windows
(97.0% with equal weights; on the 30,
83.3% and 96.8%;
Figure 3, F4.4). This is a descriptive magnitude, not a significance claim: the share has no proper null (§3.6.6), and
the cross term dominates world variance in any period because 465 pairs outnumber 31 variances (§3.5.1). What is
specific to recessions is the gap: the cross term's share of world variance is
0.706 in recession windows against
0.620 in normal ones.

The cross term rises for two reasons, and they are of similar size. Raising only the pairwise correlations from their
normal to their recession means supplies 46% of its rise; raising only
the swing sizes supplies 40%; their interaction the remaining
14%. We read this as **amplification transmitted by alignment**: larger
swings matter for world output because they are aligned, and which of the two parts is larger depends on the sample
(on the original 26, swing size 53% against correlation
33%).

The same arithmetic can be written for a single year (Box 1, §5.2). If a common shock reaches each economy according to
where it is in its cycle, the world response has the variance of $N_{\mathrm{eff}} = 1/r^2$ independent economies:
with the phases spread out the 31 economies behave like 31, with the phases aligned they behave like one. Over
1970–2022, $N_{\mathrm{eff}} = 1/E[r^2]$ is about 3.5 on average,
2.4 in recession years and
2.1 in the year before, and
1.1 in 2020 (descriptive; Appendix Table A7). The dip is carried by
2009 (1.37) and 2020
(1.11); the earlier recession years are not low
(1975 5.1, 1982 5.4,
1991 9.8). Averaged over the decomposition's windows the variance law
gives the cross term 84.1% of the extra
recession variance, against the 84.3% measured:
the loss of diversification is this arithmetic, and it is an accounting of the recession excess, not a cause of it.

![**Figure 3 (F4.4).** Loss of diversification. (a) Variance of the GDP-weighted world cycle on 10-year windows,
split into the own term (grey) and the cross term (blue); grey bands: windows ending in a recession year. (b) The cross
term's share of world variance in normal and recession windows, with GDP and with equal weights. No p-value is shown:
the share has no proper null (§3.6.6).](../../figures/04_amplitude_diversification/F4-04_diversification_s31.png)

### 4.3 The network has tightened

The correlation network of the 31 business cycles has tightened over five decades. The mean edge length of its minimum
spanning tree fell from 0.687 in 1979–89 to 0.424
in 2013–22, a factor of 1.6× (Figure 4, F5.1; 1.6× on the 30 and
1.8× on the original 26). This is a description of a trend, not a test. The network does not contract
in the years before recessions ($\tau =$ −0.157, $p =$ 0.206; §3.5.5), and the
economies move too nearly together for a leader to be identified: the spread of their phase leads is
0.546 years, below every one of 5,000 surrogates ($p =$ 0.0002,
the floor; §3.5.6).

![**Figure 4 (F5.1).** The network has tightened. (a) Mean edge length of the minimum spanning tree of the 31 business
cycles on 10-year windows, with the decade means for 1979–89 and 2013–22 (orange). (b) The 465 pairwise cycle
correlations, averaged over the windows ending in each decade; dashed lines: medians.](../../figures/05_network_phase/F5-01_mst_s31.png)

### 4.4 Synchronization rises in the year before global recessions

With phases built from past data only — the version that uses no information from after each year — synchronization
is higher in the year before global recessions: the lead-1 correlation is +0.379
($p =$ 0.038 against 53 circular shifts, whose floor is 0.019), **and it rests on two
events, 2009 and 2020 ($n \approx 2$)**: without either the two-sided lead is not significant ($p =$
0.226 and 0.283), and without both it is
gone (−0.02). With China left out the past-only lead-1 is
+0.357 ($p =$ 0.057). With the
usual two-sided phases the lead-1 correlation is +0.231, at the floor of the circular-shift
null ($p =$ 0.019) and $p =$ 0.033 against
surrogates with ends (§3.4.4); it survives the removal of any one of the 31 economies ($p \le$
0.038; Appendix Table A3) and the edge-robust convention ($p =$
0.019), but not convention N ($p =$ 0.057), and it does
not pass a correction for testing five lags, which with 53 shifts a single lag cannot do (§3.6.4). We lead with the
past-only value because the two-sided arc is inflated by how recessions are dated (Limitations). On the 30 the
past-only lead-1 is +0.369 ($p =$ 0.038) and on the 26
+0.374 ($p =$ 0.038).

The rest of the arc is not claimed (Figure 5, F2.5). The two-year lead (lead-2 +0.235,
$p =$ 0.038) does not survive past-only phases (−0.044,
$p =$ 0.585). The crisis year is not significant with two-sided phases
($p =$ 0.189); with past-only phases it is at the floor
(+0.417, $p =$ 0.019), which was not a
pre-registered claim and is reported, not interpreted. The fall two years after recessions
(−0.258, $p =$ 0.057) is in the Limitations. This is a property of the
tightly coupled modern economy, observed twice; it is not a fifty-year regularity and not a forecast.

![**Figure 5 (F2.5).** The tested arc. Correlation of $r(t)$ with the recession indicator at each lag, with two-sided
phases (P, circles) and phases from past data only (C, diamonds). Filled: one-sided $p \le 0.05$ against 53 circular
shifts (floor 0.019); grey bars: the range of 90% of the shifted correlations.](../../figures/02_crisis_arc/F2-05_arc_tested_s31.png)

### 4.5 No critical slowing down

Before recessions the variance of synchronization rises ($\tau =$ +0.438, $p =$
0.031 against 5,000 surrogates; $p =$ 0.029 against
surrogates with ends) while its lag-1 autocorrelation does not ($\tau =$ −0.152, $p =$
0.789), and the recovery rate does not fall after recessions ($p =$
0.502; Figure 6, F6.1). Critical slowing down — the signature of a system approaching
a bifurcation — raises variance and autocorrelation together, because both come from a slower return to equilibrium.
A rise in variance alone is not that signature. *As an interpretation, not a test:* it is what noise-induced tipping
would show, where larger disturbances push the system across a threshold while its restoring forces stay the same
(Ashwin et al. 2012). The variance rise, like the lead, rests on 2009 and 2020 (before them alone
+0.857, $p =$
0.003; before 1982 and 1991,
+0.018, $p =$
0.513; Appendix Table A8), and it is significant under
conventions P and E but not W or N (§3.5.7).

![**Figure 6 (F6.1).** No critical slowing down. Variance (a) and lag-1 autocorrelation (b) of the fluctuations of
$r(t)$ on trailing 15-year windows. In colour: the eight years before each recession, over which the trend is tested;
grey bands: recession years.](../../figures/06_tipping_nulls/F6-01_early_warning_s31.png)
