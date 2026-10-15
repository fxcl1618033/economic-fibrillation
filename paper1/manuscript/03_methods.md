## 3 Methods

### 3.1 Cycle extraction

For each economy $i$ we take the natural log of real GDP per capita, $y_i(t) = \ln \mathrm{GDPpc}_i(t)$, and remove its
sample mean. We isolate business-cycle frequencies with a second-order Butterworth band-pass filter applied by
forward–backward filtering (`filtfilt`), which is zero-phase and therefore introduces no artificial lead or lag between
economies — a necessary property, since the phase relationships between economies are the object of study.

The pass-band is 2–9 years. In normalized frequency units at an annual sampling rate
($f_{\mathrm{Nyq}} = 0.5\ \mathrm{yr}^{-1}$) the band edges are $f_{\mathrm{low}} = 1/9\ \mathrm{yr}^{-1}$ and
$f_{\mathrm{high}} = 0.49\ \mathrm{yr}^{-1}$. The upper edge is set at 0.49 rather than the nominal 0.5 because a
Butterworth design requires the critical frequency to lie strictly inside the open interval $(0, f_{\mathrm{Nyq}})$;
the resulting cycle band is thus effectively 2.04–9 years. The band brackets the conventional business-cycle range and
is not tuned to any outcome; §3.6.1 reports the sensitivity of every result to the band edges.

Write the filtered cycle for economy $i$ as $c_i(t)$. We form the analytic signal by Hilbert transform,
$$ z_i(t) = c_i(t) + \mathrm{i}\,\mathcal{H}[c_i](t) = A_i(t)\,e^{\mathrm{i}\theta_i(t)}, $$
which yields an instantaneous phase $\theta_i(t) = \arg z_i(t)$ and an instantaneous amplitude $A_i(t) = |z_i(t)|$
for each economy and year.

### 3.2 Synchronization measure

Treating the 31 economies as a population of phase oscillators, we measure collective synchronization by the Kuramoto
order parameter
$$ r(t)\,e^{\mathrm{i}\psi(t)} = \frac{1}{N}\sum_{i=1}^{N} e^{\mathrm{i}\theta_i(t)}, $$
where $r(t) \in [0,1]$ is the modulus of the mean phase vector and $\psi(t)$ is the collective phase. $r = 0$
corresponds to uniformly dispersed phases and $r = 1$ to identical phases. We also define the mean cycle amplitude
$\bar{A}(t) = N^{-1}\sum_i A_i(t)$, a measure of how large the swings are, independent of whether they are aligned.
Throughout, $A_i(t)$ denotes a single economy's instantaneous amplitude and $\bar{A}(t)$ the cross-sectional mean; no
other amplitude symbol is used.

Because $r(t)$ is a modulus, it is non-negative and biased away from zero in finite samples; with $N = 31$ its
root-mean-square under independent uniform phases is exactly $N^{-1/2} \approx$ 0.18 (its mean is
about 0.16). We therefore never interpret the level of $r$ against zero, only its variation over
time and against matched surrogates (§3.4).

### 3.3 Crisis dating

Crisis years are taken exogenously from the Kose–Terrones definition of a **global recession** (Kose and Terrones
2015; Kose, Sugawara and Terrones 2020), which identifies contractions in world real GDP per capita accompanied by
broad-based declines in other measures of global activity. This yields five dates in our window: **1975, 1982, 1991,
2009 and 2020**. The first four are those of Kose, Sugawara and Terrones (2020), written before the pandemic; 2020 is
dated as a global recession under the same definition by the World Bank (2020). These dates are fixed before any statistic is computed and are never adjusted, re-weighted, or
selected on the basis of the synchronization series. We use only the crisis *onset* years; no crisis is assigned a
duration.

The count matters for interpretation and is stated plainly: five events in 53 years. Every crisis-conditioned test in
this paper therefore rests on five degrees of freedom at most, and the leave-one-out analysis of §3.6.3 shows that the
effective count for the pre-crisis result is smaller still.

### 3.4 Null models

Two nulls are used, for two different purposes, and a third is used where the end of the sample matters (§3.4.4).

**3.4.1 Circular-shift permutation.** For any test that correlates a continuous series with the crisis indicator, we
build the null by circularly shifting the crisis indicator vector $G$ — a binary vector with ones at the five crisis
years — through all $T-1 = 52$ non-identity rotations, recomputing the statistic each time (53 configurations in
total, counting the unshifted one). This preserves both the autocorrelation of the continuous series and the number
and relative spacing of the crisis dates, and destroys only their alignment with the series. The $p$-value is the
fraction of shifts whose statistic equals or exceeds the observed one, with the usual $+1$ correction in numerator and
denominator.

This null has a hard resolution limit that must be quoted alongside any $p$ it produces: with 52 shifts, the smallest
attainable $p$-value is $1/53 = 0.019$. A reported $p = 0.019$ therefore means "no shift beat the observed value" and
cannot be read as evidence of a smaller effect size than $p = 0.019$; it is a floor, not a measurement.

**3.4.2 Spectrum-preserving surrogate economy sets.** For tests concerning the structure of the oscillator population,
we generate 5,000 surrogate 31-economy sets by Fourier phase randomization (Theiler et al. 1992). We take the real FFT
of each economy's band-passed cycle, retain the amplitude spectrum exactly, replace each non-trivial Fourier phase with
an independent draw from $U(0, 2\pi)$ (holding the DC and, for even record length, Nyquist phases real), and invert the
transform. Each surrogate economy therefore has the same power spectrum, and hence the same autocorrelation and cycle
periodicity, as its real counterpart, but its phase relationship to every other economy is destroyed. Phases are
randomized independently across economies, so the surrogate ensemble is the null of *spectrally identical but mutually
unsynchronized* economies. Surrogate $p$-values with 5,000 draws have a floor of $1/5001 = 2\times10^{-4}$.
Surrogates are drawn from each economy's 1950–2022 cycle and pass through the same Hilbert transform and 1970–2022
window as the data, so real and surrogate phases share one convention (§3.6.2).

**3.4.3 Size of the tests on simulated worlds.** To check that each test rejects at its nominal rate when there is
nothing to find, we ran every test on 1,000 simulated 31-economy worlds of each of two kinds — phase oscillators
(Kuramoto) and phase-and-amplitude oscillators (Stuart–Landau) — with no coupling between economies and no common
forcing. Each economy keeps its observed mean period, swing size and trend, and the noise is set so that the
year-to-year spread of phase steps matches the data; the simulated series pass through the same band-pass, Hilbert
transform and tests as the data, with 199 surrogates per test. Table 1 gives the share of worlds in which each test
rejects at $p \le 0.05$. With the real recession dates, which are unrelated to a simulated world, a correct test
rejects in 3.8% of worlds when its null is the circular shift (below 0.05 only $1/53$ and $2/53$ are possible) and in
5% when it is 199 surrogates. Of the 20 tests, 17 stay at or below that
rate in the Kuramoto worlds and 17 in the Stuart–Landau worlds. The exceptions are the
swing-size term of the identity (13.8%–18.9%),
which leans on the last years of the sample and is checked against surrogates with ends in §3.4.4; the circular-shift
test of $r$ against swing size (5.7%–6.2%);
and, in one kind of world each, the lag $-2$ arc (6.2%) and the alignment term
(6.5%). At least one of the five arc lags rejects in
17.3%–18.4% of uncoupled worlds, the multiplicity of
§3.6.4 in numbers. With recession years taken instead from each simulated world's own output, the way global recessions
are dated, the two-sided crisis-year and lead-1 arcs reject in
8.2%–8.9% and
8.5%–8.6% of uncoupled worlds (Limitations).

**Table 1.** Share of 1,000 uncoupled simulated worlds in which each test rejects at $p \le 0.05$. **Bold**: the 95%
interval lies above the correct rate. Real dates: 1975, 1982, 1991, 2009, 2020. Own dates: each world's five years of
lowest growth in world GDP per capita, at least five years apart.

| Test | Correct rate | Kuramoto, real dates | Stuart–Landau, real dates | Kuramoto, own dates | Stuart–Landau, own dates |
|------------|---|---|---|---|---|
| Arc, lead-2 | 3.8% | 3.3% | 3.6% | **5.2%** | **5.3%** |
| Arc, lead-1 | 3.8% | 2.9% | 4.4% | **8.5%** | **8.6%** |
| Arc, crisis year | 3.8% | 4.4% | 3.3% | **8.9%** | **8.2%** |
| Arc, after-1 | 3.8% | 4.5% | 3.6% | 4.2% | 2.6% |
| Arc, after-2 | 3.8% | **6.2%** | 4.6% | 3.9% | 4.3% |
| Arc, lead-2, past-only phases | 3.8% | 4.1% | 3.4% | 3.3% | 3.5% |
| Arc, lead-1, past-only phases | 3.8% | 3.5% | 3.8% | 2.9% | 2.3% |
| r with swing size (shifts) | 3.8% | **6.2%** | **5.7%** | **6.2%** | **5.7%** |
| r with swing size (surrogates) | 5.0% | 5.5% | 5.4% | 5.5% | 5.4% |
| Cross term at recessions, GDP weights | 5.0% | 5.3% | 5.4% | **8.9%** | **10.8%** |
| Cross term at recessions, equal weights | 5.0% | 4.6% | 4.6% | **6.8%** | **6.8%** |
| Identity: alignment at recessions | 5.0% | 4.8% | **6.5%** | **11.4%** | **12.1%** |
| Identity: swing size at recessions | 5.0% | **13.8%** | **18.9%** | **7.5%** | **14.9%** |
| MST contraction before recessions | 5.0% | 2.8% | 4.1% | 5.0% | 3.8% |
| MST contraction, detrended | 5.0% | 3.0% | 4.5% | 5.1% | 3.7% |
| MST fragility before recessions | 5.0% | 4.9% | 5.2% | 5.3% | 5.1% |
| Phase leads clustered | 5.0% | 3.0% | 5.3% | 3.0% | 5.3% |
| Slowing down: autocorrelation of r | 5.0% | 5.1% | 4.2% | 5.7% | 4.5% |
| Slowing down: variance of r | 5.0% | 5.1% | 6.1% | 5.0% | 5.5% |
| Slower recovery after recessions | 5.0% | 4.8% | 4.5% | 5.2% | 4.0% |
| Any of the five arc lags | — | 18.4% | 17.3% | 26.2% | 25.0% |
| Any of lead-2, lead-1, crisis | — | 9.9% | 10.2% | 20.2% | 20.1% |

**3.4.4 Surrogates with ends.** The surrogates of §3.4.2 are circular: they have no first or last year, so the band-pass
and the Hilbert transform treat their ends differently from the data's, where the last years of the sample are the
least reliable. For every test whose statistic uses a year from 2019 to 2022 — the crisis year 2020, a lead or lag
reaching those years, or a window ending in them — we also compare the statistic with surrogates that have ends. Each
economy's growth rates are given random Fourier phases on a series eight times longer than the sample, with the same
periodogram; a 72-year stretch from a random start is cumulated from the real 1950 level and passed through the same
band-pass, Hilbert transform and windows as the data. For tests whose null is independent surrogates the phases are
drawn independently for every economy; for the lead–lag arcs, whose null is the circular shift, one random phase per
frequency is shared by every economy, which keeps their co-movement and so the level and persistence of $r(t)$ and
randomizes only the timing. We draw 5,000 such surrogates (floor 0.0002). On uncoupled simulated worlds (§3.4.3) these
nulls reject at about 5%, including the swing-size term (1.5% and
4.8%). On the 31 economies no result we claim changes side of 0.05: the
swing-size term and $r$ against swing size stay at the floor ($p =$
0.0002), the variance rise of §3.5.7 is
$p =$ 0.029, and the two-sided lead-1 moves from the circular-shift
floor 0.019 to
$p =$ 0.033
(0.043 on the 30,
0.042 on the 26). In all, 6 p-values of
sensitivity or unclaimed results move across 0.05 (Appendix Table A4); the one that matters for the text is the lag
$-2$ arc on the 31 (0.057 →
0.039; Limitations).

### 3.5 Tests

**3.5.1 Loss-of-diversification decomposition.** The world output cycle is the weighted aggregate of the 31 band-passed
economy cycles,
$$ C_w(t) = \sum_{i=1}^{N} w_i\, c_i(t), $$
with weights $w_i \ge 0$, $\sum_i w_i = 1$. On each rolling 10-year window its variance decomposes exactly into an
own-term and a cross-term,
$$ \mathrm{Var}[C_w] \;=\; \underbrace{\sum_{i} w_i^2\, \sigma_i^2}_{\text{own}} \;+\; \underbrace{\sum_{i \ne j} w_i w_j\, \sigma_{ij}}_{\text{cross}}, $$
where $\sigma_i^2$ is economy $i$'s within-window cycle variance and $\sigma_{ij}$ the pairwise covariance. Variances
are computed with the population convention (dividing by the window length $W = 10$). The own-term is what world output
would fluctuate by if the 31 economies were uncorrelated; the cross-term is the co-movement surcharge. The
decomposition is an identity, not a model, and holds window by window.

The test is deliberately *not* "does world variance rise with average correlation." That is close to algebraically
guaranteed: for equal weights and equal cycle variances the cross share is
$\mathrm{cross}/\mathrm{total} = (N-1)\bar\rho / (1 + (N-1)\bar\rho)$, so with $N = 31$ the 465 covariance pairs
outnumber the 31 variances by more than an order of magnitude and the cross-term dominates at any $\bar\rho$ above a
few hundredths. Observed $\bar\rho$ ranges from 0.08 to 0.77 across our windows, which
alone would force a cross share between 0.69 and 0.96 if the economies swung equally.
Unequal swings lower the share wherever one economy dominates the own-term: the equal-weighted share ranges from
0.19 to 0.95 and stays below 0.40 in 9 of the
12 windows ending 1985–1996, when Iran's cycle alone supplies between
19% and 42% of the own-term. Reporting a high cross share
as a finding would therefore still be reporting arithmetic. The non-circular question is which term supplies the
*excess* variance in global-recession years relative to normal years:
$$ \Delta_{\text{own}} = \langle \text{own}\rangle_{\mathrm{crisis}} - \langle \text{own}\rangle_{\mathrm{normal}}, \qquad \Delta_{\text{cross}} = \langle \text{cross}\rangle_{\mathrm{crisis}} - \langle \text{cross}\rangle_{\mathrm{normal}}, $$
summarized as the cross-term's share of the excess, $\Delta_{\text{cross}} / (\Delta_{\text{own}} + \Delta_{\text{cross}})$.

Two weightings are computed and both are reported. **GDP-weighted** ($w_i$ proportional to the economy's within-window
mean real GDP, i.e. GDP per capita times population) is the primary framing, since it is the actual world economy.
**Equal-weighted** ($w_i = 1/N$) is the robustness check and ties directly to the equal-weight order parameter of §3.2,
which gives every economy one vote. Windows may start in 1962 and never earlier (§3.6.7), so the decomposition is defined
from 1971 and all five global recessions enter it. The 1975 window (1966–1975) draws on run-in years; the version with
windows kept inside 1970–2022, which loses 1975, is reported in §3.6.7.

Across 1971–2022 the cross-term supplies the great majority of the excess crisis variance under both weightings:
84.3% GDP-weighted and
97.0% equal-weighted (S30:
83.3% and 96.8%).
The underlying cross-shares are 0.706 in crisis windows against
0.620 in normal windows (GDP-weighted), and
0.783 against 0.691
(equal-weighted). The direction is consistent across weightings, and the gap is a shift of about
9%
on a base of about two-thirds. The equal-weighted figure is the larger because equal weights give the 465 covariance
pairs their maximum leverage; the GDP-weighted figure, in which a few large economies carry most of the own-term, is the
one we treat as describing the world economy.

The cross-term is not the same thing as correlation: it rises when economies move together and when they swing harder.
Changing only the pairwise correlations from their normal-window means to their crisis-window means (mean correlation
0.291 → 0.385) supplies
46% of the cross-term's crisis rise GDP-weighted
(50% equal-weighted); changing only the cycle sizes (mean cycle s.d.
× 1.10) supplies
40% (37%); their
interaction supplies the remaining 14%
(13%). On the 30 without Russia the split is
44%, 41% and
15%. The two parts are of similar size, and which is larger depends on the
sample: on the original 26 economies the larger swings supplied more (53%
against 33%; §3.6.8). Co-movement and larger swings contribute about
equally.

Significance is assessed against the spectrum-preserving surrogate ensemble of §3.4.2. §3.6.6 reports the outcome of that
test, which does not behave as a well-posed significance test for the share statistic, and states what we do and do
not claim as a result.

**3.5.2 Synchronization–amplitude coupling.** We correlate $r(t)$ with $\bar{A}(t)$ over 1970–2022 by Pearson
correlation, in two versions: on the raw series, and after removing a slow trend from each by subtracting a
Gaussian-smoothed copy ($\sigma = 8$ yr). The detrended version is the headline: both series carry secular drift over
five decades, and the raw correlation cannot distinguish co-movement at business-cycle timescales from two coincident
long-run trends. The two versions agree in sign and significance —
+0.472 raw against +0.646 detrended, both at the floor
$p =$ 0.019 (S30: +0.458 and +0.641)
— so the result does not hinge on the detrending choice; we report the detrended value because it isolates
business-cycle timescales, not because it is the larger. Significance is assessed by the circular-shift null of §3.4.1
applied to the paired series, and separately against the surrogate ensemble of §3.4.2
($p =$ 0.0002, the ensemble floor). This test uses no crisis dates at all.

**3.5.3 Crisis-relative lead–lag profile.** For each lag $\ell \in \{+2, +1, 0, -1, -2\}$ we correlate $r(t)$ with the
crisis indicator shifted by $\ell$, so that positive $\ell$ tests whether synchronization *precedes* crises and
negative $\ell$ whether it falls after them. Leading lags are tested one-sided upward and trailing lags one-sided
downward, matching the pre-registered direction of the hypothesis; the contemporaneous lag is tested upward.
Significance uses §3.4.1. Because the band-pass and the Hilbert transform both use data after year $t$, a lead found this
way is not a forecast; every lead is re-tested with phases built from past data only (§3.6.2).

Five lags are tested, and the raw $p$-values are reported as such alongside a multiplicity correction over the five
(§3.6.4). We report the raw values because they are the natural output of the permutation scheme, and the corrected
values because five lags were in fact examined.

**3.5.4 Composite crisis epoch.** We average $r$ and $\bar{A}$ over a $\pm 4$-year window centred on each of the five
crisis onsets and take the mean across events, giving a composite epoch profile for each quantity. The peak lag of each
profile is read off directly. This is a descriptive alignment, not a test, and is reported with no $p$-value.

**3.5.5 Network geometry.** On 10-year rolling windows we compute the $31\times31$ Pearson correlation matrix of the
band-passed cycles, convert it to the standard ultrametric-compatible distance $d_{ij} = \sqrt{2(1-\rho_{ij})}$
(Mantegna 1999), build the minimum spanning tree by Prim's algorithm, and record its mean edge length
$L(t) = (N-1)^{-1}\sum_{e \in \mathrm{MST}} d_e$. Falling $L$ indicates a tightening network. Windows may start in 1962
and never earlier, so that each has at least twelve years of filter run-in (§3.6.7); $L(t)$ is therefore defined from
1971. Two questions are asked of $L$: whether it trends secularly — reported as a description via decade means,
0.687 in 1979–89 (the first decade whose windows all lie inside the 1970–2022
analysis window) against 0.424 in 2013–2022, a factor of
1.6× (S30: 0.680 against 0.421,
also 1.6×) — and whether contraction coincides with the pre-crisis windows. The latter is quantified
by a Kendall-$\tau$ trend over the 8 years preceding each onset, averaged over crises (1975's window has four of its
eight years defined), and tested one-sided downward against the surrogate ensemble of §3.4.2, both on raw $L$ and on $L$
minus a Gaussian-smoothed copy of itself ($\sigma = 8$ years). Both are null: $\tau =$ −0.157,
$p =$ 0.206 on raw $L$ and $\tau =$ +0.014,
$p =$ 0.561 detrended (S30: −0.143, $p =$ 0.219;
+0.057, $p =$ 0.659). The test is described here so that
it is on record as having been run and failed, not inferred from its absence.

**3.5.6 Phase-lag structure.** For each economy we compute its mean phase offset from the collective phase,
$\langle \arg e^{\mathrm{i}(\theta_i - \psi)}\rangle$, and convert it to years by dividing by the mean angular
frequency $\bar\omega$ (estimated as the mean year-on-year phase increment across economies, giving a mean cycle period
of 5.93 years). An economy with a consistently positive offset sits ahead of the
collective phase; whether that constitutes economic leadership is a question for later work and is not addressed here.
The test statistic is the standard deviation of these 31 lags, observed at 0.546 years: a large
spread would leave leader–follower structure recoverable, a small spread implies the economies move
near-simultaneously. It is compared to the surrogate ensemble of §3.4.2. Because the scientific question is whether the
observed spread is *smaller* than chance, the test is one-sided **downward**: the observed
0.546 yr lies below all 5,000 surrogate values (surrogate mean 0.992,
minimum 0.554), giving $p =$ 0.0002, the ensemble resolution
floor (S30: 0.535 yr, $p =$ 0.0004). The economies are phase-locked
tightly enough that no epicenter is recoverable.

**3.5.7 Critical slowing down.** We test the standard early-warning battery (Scheffer et al. 2009) — rising lag-1
autocorrelation and rising variance of the fluctuations of $r(t)$ around a Gaussian-smoothed trend ($\sigma = 5$
years), on trailing 15-year windows — over the 8 years before each onset, with the trend measure and surrogate test of
§3.5.5, one-sided upward. A third indicator often added, the restoring time, was considered and dropped: estimated as
$1/(-\ln\varphi)$ from the same lag-1 autocorrelation $\varphi$, it is an increasing function of $\varphi$, so its
trend test repeats the autocorrelation's and adds no independent evidence. We complement the two indicators with a test
that treats coupling as the bifurcation parameter: inverting the mean-field Kuramoto relation $r = \sqrt{1 - K_c/K}$
gives an implied coupling $K/K_c = 1/(1 - r^2)$, and critical slowing down would show as a fall in the recovery rate
$\lambda = -\ln\varphi$ in the years just after each onset relative to all other years, tested one-sided against the
surrogate ensemble of §3.4.2. Windows may start in 1962 (§3.6.7), so the pre-crisis windows of 1982 (six of eight years
defined), 1991, 2009 and 2020 enter; 1975 has none.

Two of the three tests are null. Lag-1 autocorrelation shows no pre-crisis rise ($\tau =$ −0.152,
$p =$ 0.789), and the recovery rate does not fall after onsets (change
+0.002, $p =$ 0.502). The variance of $r(t)$ does rise
before crises ($\tau =$ +0.438, $p =$ 0.031; S30: +0.420,
$p =$ 0.037), but without the rise in autocorrelation. Critical slowing down raises both together,
because both follow from a slower return to equilibrium; variance alone also rises when the shocks that move $r(t)$
grow larger. A rise in variance without a rise in autocorrelation is therefore not the slowing-down signature. It is
what loss of diversification (§3.5.1) would produce: when shocks to the economies stop cancelling, $r(t)$ swings more
widely without returning more slowly. This is a reading of the result, not a separate test. The variance rise also
rests on the two modern events, like the lead of §3.5.3: the windows before 2009 and 2020 alone give
$\tau =$ +0.857
($p =$ 0.003), those before 1982 and 1991 give
$\tau =$ +0.018
($p =$ 0.513), and dropping either 2009 or 2020 leaves it short
of significance ($p =$ 0.206 and
0.125). It is significant under convention P and the edge-robust E
($p =$ 0.045) but not under W or N ($p =$ 0.135 and 0.073; on S30, E
gives $p =$ 0.054; §3.6.2). Annual data over 8-year pre-crisis windows give these estimators very few
effective degrees of freedom, so the nulls are weak evidence in the statistical sense and we do not read them as
establishing an absence.

It is not, however, an empty result. Rising autocorrelation and variance together are the specific signature of a
system approaching a *bifurcation* — the slow eigenvalue going to zero as a fixed point loses stability. In the
taxonomy of Ashwin et al. (2012) this is B-tipping, and it is only one of three routes; noise-induced (N-) and
rate-induced (R-) tipping produce no such precursor, because in neither case does the system's restoring rate vanish
before the transition. The absence of that joint fingerprint is therefore consistent with a non-bifurcation
transition, and is informative about *which class* of tipping is in play even where it is uninformative about
proximity to a threshold. We report these tests as what the transition is not. The mechanism the paper proposes is
loss of diversification (§3.5.1), argued in the Discussion; nothing in this paper tests whether that mechanism has a
threshold.

### 3.6 Robustness and disclosure

Every check in this section was run on the final pipeline, and all outcomes are reported whether or not they support
the paper's claims.

**3.6.1 Filter band.** Results are recomputed for pass-bands of 2–8 and 3–10 years. The pre-crisis lead is present in all
three bands (lead-1 between +0.19 and +0.25) but
its $p$-value moves across the conventional threshold: lead-1 gives $p =$ 0.019
(2–9 yr), 0.094 (2–8 yr) and 0.019
(3–10 yr). The post-crisis decline is not robust to the band: the lag $-2$ coefficient is
−0.26 ($p =$ 0.057) at 2–9 years,
−0.27 ($p =$ 0.019) at 2–8 years and
+0.00 ($p =$ 0.509) at 3–10 years.

**3.6.2 Detrending method and phase convention.** Substituting an HP filter ($\lambda = 100$) for the band-pass leaves
the lead result materially unchanged (lead-1 +0.29,
$p =$ 0.019). Using first differences of log GDP per capita instead
weakens the lead-2 term to $p =$ 0.057 and eliminates the post-crisis decline
entirely (+0.04, $p =$ 0.679). The
post-crisis result is thus method-dependent in a way the pre-crisis result is not.

The phase convention matters too. Besides the convention used throughout (P: band-pass and Hilbert transform on
1950–2022, statistics on 1970–2022) we compute four others: W, the Hilbert transform on 1970–2022 only, after the same
band-pass; N, both steps on 1970–2022 only, with no run-in; E, an edge-robust version of P that mirrors each cycle by
nine years (the longest period in the band) at both ends before the Hilbert transform; and C, phases from past data
only, recomputing the band-pass and Hilbert transform on the data up to each year and keeping that year's phase. C uses
no future data, so a lead that survives it is not an artifact of the two-sided filters.

**Table 2.** The arc and the synchronization–swing-size link under each phase convention (31 economies; the last column
the 30). Correlation, one-sided $p$ in brackets (circular shifts, floor 0.019).

| Convention | Lead-2 | Lead-1 | Lag $-2$ | $r$–$\bar A$, detrended | S30 lead-1 |
|------------|---|---|---|---|---|
| P | +0.235 (0.038) | +0.231 (0.019) | −0.258 (0.057) | +0.646 (0.019) | +0.217 (0.019) |
| W | +0.216 (0.057) | +0.204 (0.019) | −0.165 (0.113) | +0.566 (0.019) | +0.184 (0.057) |
| N | +0.216 (0.038) | +0.192 (0.057) | −0.190 (0.094) | +0.547 (0.019) | +0.173 (0.094) |
| E | +0.233 (0.038) | +0.236 (0.019) | −0.160 (0.132) | +0.583 (0.019) | +0.226 (0.019) |
| C | −0.044 (0.585) | +0.379 (0.038) | −0.159 (0.170) | +0.726 (0.019) | +0.369 (0.038) |

Lead-1 is significant under P, W, E and C and falls short under N ($p =$ 0.057); on
the 30 without Russia it also falls short under W ($p =$ 0.057). Of the two leads it
is the one that survives phases built from past data only, and it is the one we interpret; lead-2 does not survive
them, and the post-crisis fall is significant under none of the five conventions. Under past-only phases the crisis
year also reaches the floor (+0.417, $p =$ 0.019,
against 0.189 under P). The past-only check was pre-registered for the leads only, and we do not
interpret this: a phase built from data up to the crisis year is estimated at the very end of its series, where the
recession itself sits. The
synchronization–amplitude link is significant at the floor under every convention, which moves its size between
+0.547 and +0.726. We report P throughout, on
the ground that the edge transients its run-in removes are an artifact, not because it gives the larger values.

**3.6.3 Leave-one-crisis-out.** Dropping each crisis in turn and refitting §3.5.3 shows that the pre-crisis lead is not
evenly carried by the five events. Lead-1 survives removal of 1975, 1982 and 1991 ($p =$
0.019, 0.019 and
0.019; without 1975 it is $p =$ 0.057 on the
30 without Russia), but dropping either 2009 or 2020 destroys its significance ($p =$
0.226 and 0.283), and dropping both leaves
no lead at all (−0.02, $p =$
0.491). A split-sample fit tells the same story: 1970–1995 (crises 1975,
1982, 1991) shows no significant lead (lead-1 +0.24, $p =$
0.154), while 1996–2022 (crises 2009, 2020) does
(+0.38, $p =$ 0.037, the
floor for 27 years). The effective event count behind the pre-crisis claim is therefore $n \approx 2$, both in the
modern era, and the claim is stated in the paper as an era-specific property of the tightly coupled economy rather
than a fifty-year regularity. The variance rise of §3.5.7 rests on the same two events.

**3.6.4 Multiplicity.** Across the five lags of §3.5.3, no coefficient survives a Bonferroni correction (lead-1:
$p_{\mathrm{adj}} =$ 0.094; lead-2: 0.189; lag $-2$:
0.283) or Benjamini–Hochberg control of the false discovery rate
($q =$ 0.094 for lead-2, lead-1 and lag $-2$). This is partly built into the test.
With 53 circular shifts the smallest $p$ the test can return is $1/53 = 0.019$, so no single lag can pass a Bonferroni
correction over five lags ($5/53 = 0.094$), and a lag can pass Benjamini–Hochberg only if another lag also reaches the
floor, as lead-1 and lag $-2$ did together on the original 26 economies ($q =$ 0.047;
§3.6.8). Corrected significance is therefore not what supports lead-1. Its support is that it survives phases built from
past data only (§3.6.2) and the removal of any one economy (§3.6.5); with past-only phases and China left out together it
is $p =$ 0.057 (Appendix Table A1), on the 31 as on the 30. It does not
survive the removal of 2009 or 2020 (§3.6.3).

**3.6.5 Leave-one-economy-out.** Removing any one of the 31 economies leaves lead-1 between
+0.22 and +0.25 with $p \le$
0.038 (the United States, Germany and Japan: $p =$ 0.019,
0.019 and 0.019). No single economy drives the
result, including each of the five added in this version (§3.6.8).

**3.6.6 Surrogate test of the decomposition.** The share statistic of §3.5.1 does not admit a well-behaved surrogate test,
and we report this rather than substituting a statistic that does. Its denominator
$\Delta_{\text{own}} + \Delta_{\text{cross}}$ is a difference of window means that is near zero and of either sign under
the surrogate null, so the ratio is unbounded and its null distribution is heavy-tailed and non-monotone in the
quantity of interest. Against 5,000 surrogate sets,
2,390 draws equal or exceed the observed equal-weighted share
and 1,581 the GDP-weighted share — nominal $p$-values of
0.48 and 0.32,
which reflect the pathology of the ratio rather than the strength of the effect. Tested on the unnormalized components
instead, $\Delta_{\text{cross}}$ exceeds every one of the 5,000 surrogates under both weightings
($p =$ 0.0002, the ensemble resolution floor), and so does
$\Delta_{\text{own}}$ equal-weighted (GDP-weighted it exceeds all but
191, $p =$ 0.038),
but that test is uninformative for our purpose: it rejects the null that crisis windows resemble phase-randomized ones
at all, which is a much weaker statement than the decomposition claim, and it rejects for the own-term too. In
simulated worlds with trade coupling it rejects even when the recession dates have nothing to do with the worlds
(Limitations).

We therefore state the decomposition result as a descriptive magnitude with an explicit floor, not as a significance
claim: the cross-term supplies the large majority of the excess crisis variance under both weightings, on five events,
and the algebraic baseline of §3.5.1 already guarantees a high cross share before any economics enters. What the data
add beyond arithmetic is the *gap* between crisis and normal windows (§3.5.1), which is modest in absolute terms. A
defensible significance test for this statistic — one whose null distribution is proper — is not available to us and
we do not report one.

**3.6.7 Window convention of the rolling statistics.** Every rolling statistic — the network measure (§3.5.5), the
decomposition (§3.5.1) and the early-warning and coupling tests (§3.5.7) — uses windows that may start in 1962 and never
earlier, leaving at least twelve years of filter run-in. As a sensitivity check each is recomputed with windows kept
inside 1970–2022, dropping any pre-crisis window that is then only partly defined. For $L$ this changes no value from
1979 onward, so the decade means of §3.5.5 are unaffected; the pre-crisis contraction test, now on 1991, 2009 and 2020,
stays null ($\tau =$ +0.095, $p =$ 0.654 raw;
+0.333, $p =$ 0.910 detrended). The
decomposition loses the 1975 window and gives 86.8%
GDP-weighted and 96.9% equal-weighted. Lag-1
autocorrelation ($\tau =$ −0.107, $p =$ 0.644) and the coupling test
(+0.065, $p =$ 0.520) stay null; the variance
trend, now on 2009 and 2020 only, is +0.857 ($p =$ 0.003).

**3.6.8 The original 26, the 30 and the five added economies.** Every test was also run on the original 26 economies and
on the 30 without Russia, under the same conventions; on the 31 with each added economy left out; with Iran and Saudi
Arabia, whose cycles are the largest relative to the median of the 26, left out together; and with Russia's phases
computed from 1992 only, so that its back-cast Soviet-era values cannot drive the result (Appendix Table A1). Without
Russia no primary result changes sign or crosses $p = 0.05$: lead-1 is +0.217
($p =$ 0.019), the synchronization–amplitude link +0.641, the
network tightens by 1.6×. With Russia's phases from 1992, lead-1 is
+0.224 ($p =$ 0.019) and the
synchronization–amplitude link +0.655. On the 26 the lead–lag profile is
almost the same (lead-1 +0.216, $p =$ 0.019; with past-only phases
+0.374, $p =$ 0.038), lead-1 and lag $-2$ pass
Benjamini–Hochberg together ($q =$ 0.047), the network tightens by
1.8×, and the larger swings supply more of the cross-term's crisis rise than the higher correlations
(53% against 33%).
Leaving out one added economy moves lead-2 and past-only lead-1 to $p =$ 0.057 without
China; the fall after recessions (lag $-2$, $p =$ 0.057 on the 31) crosses to $p < 0.05$ without
20 of the 31 single economies and with Russia from 1992, which marks it as sitting on
the threshold rather than as stronger (§3.6.1–7.2). The alignment share of the excess in world swing is sample-sensitive:
39% on the 26, 19% on the 30,
33% on the 30 without Iran and 28% on the 31.
Replacing Maddison's 1991–2011 growth for Norway, Switzerland and South Africa, which runs two to three points above
national accounts, with the Global Macro Database's changes no conclusion (on the 31, lead-2 moves to
$p =$ 0.057 and lag $-2$ to $p =$ 0.038).

### 3.7 Reproducibility

The input data are the Maddison Project Database (2023 release) as distributed in the `MaddisonData` R package
(repository `sbgraves237/maddisondata`, commit `3ed424b6`; the data file `MaddisonData.rda`, sha256 `63a3cff9…`, is
unchanged since October 2025). The pipeline rebuilds from these pinned files with one command and is deterministic
apart from the surrogate ensembles, which are seeded; every result is saved with its settings, seed and code version.
The sample, phase convention, tests and test directions were written down and signed before any test was run on the
added economies, and extended by a dated amendment before Russia was added; every pre-registered test is reported. The
earlier results on the 26 economies reproduce exactly from the rebuilt pipeline under the conventions they were first
run with, including every surrogate $p$-value.

Two quantities in earlier internal result files differ from the values stated here. The synchronization–amplitude
correlation of early drafts, +0.51, applied the Hilbert transform to the 1970–2022
window only after a 1950–2022 band-pass (convention W of §3.6.2); it reproduces exactly under that convention. The
correlation between mean pairwise cycle correlation and the order parameter quoted in early drafts did not reproduce
from the raw data; under the conventions stated here it is +0.50 on the 26
economies with equal weights (+0.51 on the 31). Neither changes a conclusion.

---

*Figure — Methods diagnostics (F5.4, supplementary).* Panel **a**: MST mean edge length by year from 1971 (grey) with
the decade means for 1979–89 and 2013–22 (blue), 0.687 against
0.424, a factor of 1.6×. Panel **b**: the phase-lag spread against
its 5,000-member surrogate null — the observed 0.546 yr lies below every surrogate
($p =$ 0.0002, the floor). Panel **c**: raw and Bonferroni-corrected $p$-values for the
five lags of §3.5.3, against the $1/53$ permutation floor (dotted) and 0.05 (dashed).
