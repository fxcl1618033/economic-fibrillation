# Proposed edits to the Methods

`docs/methods.md` is not changed. Each edit below quotes the current text, gives the proposed text and the reason.

**Second draft, 11 October 2026, after Phase 3 and Sid's decisions on it.** S30 is Paper 1's main sample (Sid), so
every number below is the 30-economy value under convention P unless it says otherwise; the original 26 move to a new
§7.8. Sources: `results/S30/P/*.json` and `results/COMPARISON.md` (pre-registered run, code 07bbdd8) and
`results/FOLLOWUP.md` (the leave-one-crisis-out check Sid asked for, not pre-registered).

The edits are in Methods order. Each heading carries its label from the first draft so they can be traced:

| Label | What | Section | Status |
|---|---|---|---|
| A1 | Bonferroni value | §7.4 | decided (0.094); S30 values added |
| A2 | MST windows and decade means | §6.5 | decided; S30 values replace S26 (1.6× instead of 1.8×) |
| A3 | One window rule for all rolling statistics | §7.7 | decided; Phase 3 sensitivity numbers filled in |
| A4 | Early-warning battery: two indicators plus the coupling test | §6.7 | decided; **rewritten for Sid's decision on the variance result** |
| B1 | The arc depends on the phase convention | §1, §6.3, §7.2 | drafted from Sid's decision on the arc's wording |
| B2 | The earlier amplitude convention is known | §8 | drafted |
| B3 | The cross-term split | §6.1 | drafted with S30 values |
| B4 | Data citation | §8 | drafted |
| B5 | The detrended pre-crisis MST test | §6.5 | drafted with the Phase 3 value |
| C | Phase 3 numbers | every section | filled in |
| N1 | The expected value of r under random phases | §3 | **new**: a small correction found while drafting |
| N2 | The cross-share formula needs equal variances | §6.1 | **new**: a correction that matters on S30 (Iran) |
| N3 | Surrogates follow convention P | §5.2 | **new**: one sentence |
| L1–L3 | Results and Limitations text | outside the Methods | drafted from Sid's decisions; for the paper, not for `methods.md` |

---

## §1 Data (C, B1)

**Current (first paragraph):** "We use annual real GDP per capita from the Maddison Project Database (2023 release),
PPP-adjusted, for a fixed panel of $N = 26$ economies: Australia, Austria, Belgium, Canada, Denmark, Finland, France,
Germany, Greece, India, Indonesia, Italy, Japan, Mexico, the Netherlands, Norway, Portugal, South Africa, South Korea,
Spain, Sweden, Switzerland, Thailand, Turkey, the United Kingdom and the United States. The panel is balanced: every
economy has an uninterrupted annual observation from 1950 to 2022, so no interpolation, gap-filling or
unbalanced-panel weighting enters the pipeline at any stage."

**Proposed:** "We use annual real GDP per capita from the Maddison Project Database (2023 release), PPP-adjusted, for a
fixed panel of $N = 30$ economies: Australia, Austria, Belgium, Brazil, Canada, China, Denmark, Finland, France,
Germany, Greece, India, Indonesia, Iran, Italy, Japan, Mexico, the Netherlands, Norway, Portugal, Saudi Arabia, South
Africa, South Korea, Spain, Sweden, Switzerland, Thailand, Turkey, the United Kingdom and the United States. The panel
is balanced: every economy has an uninterrupted annual observation from 1950 to 2022, so no interpolation, gap-filling
or unbalanced-panel weighting enters the pipeline at any stage. An earlier version of this analysis used the first 26
of these economies. Brazil, China, Iran and Saudi Arabia were added for a more representative sample, and the sample,
the phase convention, the tests and their directions were written down before any test was run on them (§8). The
United Arab Emirates was considered and left out because its Maddison series misses 1991–1992. Results on the original
26 are reported in §7.8."

**Current (end of third paragraph):** "It is a consequential choice rather than a formality: recomputing phases on a
1970–2022 series alone, with no run-in, changes the order parameter materially in individual years and shifts the
synchronization–amplitude coefficient of §6.2 by roughly $0.08$ (§7.2)."

**Proposed:** "It is a consequential choice rather than a formality: recomputing phases on a 1970–2022 series alone,
with no run-in, changes the order parameter materially in individual years, shifts the synchronization–amplitude
coefficient of §6.2 by roughly $0.1$ and moves the lead–lag profile of §6.3 (§7.2)."

**Why:** Sid's decision that S30 is the main sample; the reason for adding the four is the decision log's of 9 October
("stronger, more representative evidence") — **Sid may want to name it more precisely**. The run-in shift is
$0.641 - 0.535 = 0.106$ on S30 ($0.608 - 0.531 = 0.077$ on S26). The clause on the lead–lag profile is the short form
of B1; the numbers are in §7.2.

## §3 Synchronization measure (C, N1)

**Current:** "Treating the 26 economies as a population of phase oscillators, …" and "with $N = 26$ the expected value
under independent uniform phases is $\approx N^{-1/2} \approx 0.20$."

**Proposed:** "Treating the 30 economies as a population of phase oscillators, …" and "with $N = 30$ its
root-mean-square under independent uniform phases is exactly $N^{-1/2} \approx 0.18$ (its mean is about $0.16$)."

**Why (N1, new):** under independent uniform phases $E[r^2] = 1/N$ exactly, so $N^{-1/2}$ is the root-mean-square of
$r$, not its mean; the mean is $\sqrt{\pi/(4N)}$, 0.16 for 30 economies (0.17 for 26). The point of the sentence (do
not read the level of $r$ against zero) is unchanged.

## §5.2 Spectrum-preserving surrogates (C, N3)

**Current:** "we generate 5,000 surrogate 26-economy sets by Fourier phase randomization."

**Proposed:** "we generate 5,000 surrogate 30-economy sets by Fourier phase randomization." Add at the end of the
paragraph: "Surrogates are drawn from each economy's 1950–2022 cycle and pass through the same Hilbert transform and
1970–2022 window as the data, so real and surrogate phases share one convention (§7.2)."

**Why (N3, new):** the pre-registration fixed this; several first-run scripts drew surrogates under convention W while
the data used P. It is why the amplitude link's surrogate p moved from 0.0006 to the floor 0.0002 on S26.

## §6.1 Loss-of-diversification decomposition (C, N2, B3)

**Current (first paragraph):** "The world output cycle is the weighted aggregate of the 26 band-passed economy cycles,"

**Proposed:** "… of the 30 band-passed economy cycles,"

**Current (second paragraph, from "That is algebraically guaranteed"):** "That is algebraically guaranteed: for equal
weights the cross share is $\mathrm{cross}/\mathrm{total} = (N-1)\bar\rho / (1 + (N-1)\bar\rho)$, so with $N = 26$ the
$325$ covariance pairs outnumber the $26$ variances by more than an order of magnitude and the cross-term dominates at
any $\bar\rho$ above a few hundredths. Observed $\bar\rho$ ranges from $0.13$ to $0.88$ across our windows, which alone
forces a cross share between $0.76$ and $0.96$. Reporting a high cross share as a finding would therefore be reporting
arithmetic."

**Proposed:** "That is close to algebraically guaranteed: for equal weights and equal cycle variances the cross share
is $\mathrm{cross}/\mathrm{total} = (N-1)\bar\rho / (1 + (N-1)\bar\rho)$, so with $N = 30$ the $435$ covariance pairs
outnumber the $30$ variances by more than an order of magnitude and the cross-term dominates at any $\bar\rho$ above a
few hundredths. Observed $\bar\rho$ ranges from $0.08$ to $0.81$ across our windows, which alone would force a cross
share between $0.70$ and $0.96$ if the economies swung equally. Unequal swings lower the share wherever one economy
dominates the own-term: the equal-weighted share ranges from $0.21$ to $0.95$ and stays below $0.40$ in the windows
ending 1985–1995, when Iran's cycle alone supplies between a fifth and two-fifths of the own-term. Reporting a high
cross share as a finding would therefore still be reporting arithmetic."

**Why (N2, new):** the formula holds only when every economy's cycle variance is the same. On S26 it gave 0.76–0.96
while the actual equal-weighted share ran from 0.62 to 0.95 (lowest in 1999, Indonesia, Turkey and Thailand); on S30
the gap is large because of Iran. Values from `ef.decomposition.rolling`, windows from 1962.

**Current (end of third paragraph):** "Because the 10-year window is taken entirely inside the analysis window, the
decomposition is defined from 1979 onward, leaving four of the five global recessions (1982, 1991, 2009, 2020) inside
its support; 1975 falls before the first complete window and does not enter this test. This is a material reduction in
an already small event count and is carried into the interpretation."

**Proposed:** "Windows may start in 1962 and never earlier (§7.7), so the decomposition is defined from 1971 and all
five global recessions enter it. The 1975 window (1966–1975) draws on run-in years; the version with windows kept
inside 1970–2022, which loses 1975, is reported in §7.7."

**Current (fourth paragraph):** "Across 1979--2022 the cross-term supplies the great majority of the excess crisis
variance under both weightings: $82.4\%$ GDP-weighted and $96.9\%$ equal-weighted. The underlying cross-shares are
$0.723$ in crisis windows against $0.669$ in normal windows (GDP-weighted), and $0.880$ against $0.818$
(equal-weighted). The direction is consistent across weightings and the gap is in the third decimal place of the share
--- a shift of five to six percentage points on a base already above two-thirds, exactly as the algebraic baseline
above would lead one to expect. The equal-weighted figure is the larger because equal weights give the 325 covariance
pairs their maximum leverage; …"

**Proposed:** "Across 1971–2022 the cross-term supplies the great majority of the excess crisis variance under both
weightings: $83.3\%$ GDP-weighted and $96.8\%$ equal-weighted. The underlying cross-shares are $0.707$ in crisis
windows against $0.619$ in normal windows (GDP-weighted), and $0.771$ against $0.671$ (equal-weighted). The direction
is consistent across weightings, and the gap is a shift of nine to ten percentage points on a base of about
two-thirds. The equal-weighted figure is the larger because equal weights give the 435 covariance pairs their maximum
leverage; …" (rest unchanged)

**New paragraph after it (B3):** "The cross-term is not the same thing as correlation: it rises when economies move
together and when they swing harder. Changing only the pairwise correlations from their normal-window means to their
crisis-window means (mean correlation $0.294 \to 0.392$) supplies $44\%$ of the cross-term's crisis rise
GDP-weighted ($49\%$ equal-weighted); changing only the cycle sizes (mean cycle s.d. $\times 1.11$) supplies $41\%$
($38\%$); their interaction supplies the remaining $15\%$ ($13\%$). The two parts are of similar size, and which is
larger depends on the sample: on the original 26 economies the larger swings supplied more ($53\%$ against $33\%$;
§7.8). The crisis excess is therefore co-movement and larger swings together — amplification transmitted by alignment
— not a pure correlation event."

**Why:** Phase 3 values (`results/S30/P/diversification.json`, `cross_split.json`). The weights are the Methods'
within-window mean GDP, as stated. On B3: the first draft's 35/50/14% was S26 with four recessions and end-of-window
weights. **For Sid:** on S30 correlation slightly outweighs swing size (44 against 41), so "amplification transmitted
by alignment" puts the emphasis the other way from the S30 numbers; the sentence above keeps it because both parts are
near equal. A plainer alternative: "co-movement and larger swings contribute about equally."

## §6.2 Synchronization–amplitude coupling (C)

**Current:** "The two versions agree closely — $+0.530$ raw against $+0.608$ detrended, at the same $p = 0.019$ — so
the result does not hinge on the detrending choice; … Significance is assessed by the circular-shift null of §5.1
applied to the paired series, and separately against the surrogate ensemble of §5.2."

**Proposed:** "The two versions agree in sign and significance — $+0.458$ raw against $+0.641$ detrended, both at the
floor $p = 0.019$ — so the result does not hinge on the detrending choice; … Significance is assessed by the
circular-shift null of §5.1 applied to the paired series, and separately against the surrogate ensemble of §5.2
($p = 2\times10^{-4}$, the ensemble floor)."

**Why:** S30 values. "Agree closely" no longer fits a gap of 0.18.

## §6.3 Crisis-relative lead–lag profile (B1)

**Add at the end of the first paragraph:** "Because the band-pass and the Hilbert transform both use data after year
$t$, a lead found this way is not a forecast; every lead is re-tested with phases built from past data only (§7.2)."

**Why:** rule 7 of the project and Sid's decision that the claimed result is the rise one year before recessions,
which survives past-only phases.

## §6.5 Network geometry (A2, B5, C)

**Current (from "Because the 10-year window"):** "Because the 10-year window needs nine years of run-in, $L(t)$ is
defined from 1971 onward. Two questions are asked of $L$: whether it trends secularly — reported as a description via
decade means ($0.706$ in the 1970s against $0.379$ in 2013–2022, a factor of $1.9\times$; the single-year endpoints
$0.771$ and $0.250$ are noisy individual windows and are not the interpreted quantity) — and whether contraction
coincides with the pre-crisis windows. The latter is quantified by a Kendall-$\tau$ trend over the 8 years preceding
each onset, averaged over crises, and tested one-sided downward against the surrogate ensemble of §5.2, both on raw $L$
and on Gaussian-detrended $L$. Both are null: $\tau = -0.171$, $p = 0.167$ on raw $L$ and $\tau = -0.086$, $p = 0.316$
detrended."

Also "$26\times26$ Pearson correlation matrix" in the first sentence.

**Proposed:** "$30\times30$ Pearson correlation matrix" in the first sentence, and: "Windows may start in 1962 and
never earlier, so that each has at least twelve years of filter run-in (§7.7); $L(t)$ is therefore defined from 1971.
Two questions are asked of $L$: whether it trends secularly — reported as a description via decade means, $0.680$ in
1979–89 (the first decade whose windows all lie inside the 1970–2022 analysis window) against $0.421$ in 2013–2022, a
factor of $1.6\times$ — and whether contraction coincides with the pre-crisis windows. The latter is quantified by a
Kendall-$\tau$ trend over the 8 years preceding each onset, averaged over crises (1975's window has four of its eight
years defined), and tested one-sided downward against the surrogate ensemble of §5.2, both on raw $L$ and on $L$ minus
a Gaussian-smoothed copy of itself ($\sigma = 8$ years). Both are null: $\tau = -0.143$, $p = 0.22$ on raw $L$ and
$\tau = +0.057$, $p = 0.66$ detrended."

**Why:** Sid's decisions on the window rule and the decade comparison (A2), with S30 values. **The headline factor is
now 1.6× (S30) instead of 1.8× (S26)**: the added economies are less tightly tied to the rest in the last decade (0.421
against 0.379); see §7.8. B5: the first-run detrended value ($-0.086$, $p = 0.316$) did not reproduce with any smoothing
width tried (open issue 23); the pre-registration fixed $\sigma = 8$, which the Methods now state. I propose not
mentioning the irreproducible value in the paper (it was never published); it stays in the registry and decision log.

## §6.6 Phase-lag structure (C)

**Current:** "… giving a mean cycle period of 5.85 years) … The test statistic is the standard deviation of these 26
lags, observed at $0.403$ years … the observed $0.403$ yr lies below all 5,000 surrogate values (surrogate mean
$0.942$, minimum $0.446$), giving $p = 2\times10^{-4}$, the ensemble resolution floor."

**Proposed:** "… giving a mean cycle period of 5.95 years) … The test statistic is the standard deviation of these 30
lags, observed at $0.535$ years … the observed $0.535$ yr lies below 4,999 of the 5,000 surrogate values (surrogate
mean $0.988$, minimum $0.523$), giving $p = 4\times10^{-4}$, twice the ensemble resolution floor."

**Why:** the first-run 0.403 was computed under convention W; under P it is 0.445 on S26 (§7.8) and 0.535 on S30. The
conclusion (near-simultaneous movement, no recoverable epicenter) is unchanged.

## §6.7 Critical slowing down (A4, rewritten for Sid's decision on the variance result)

**Current (first paragraph):** "We test the standard early-warning battery — rising lag-1 autocorrelation, rising
variance, and rising restoring-time — on the pre-crisis windows. All three are reported as null in Results. Annual
data over 8-year pre-crisis windows gives these estimators very few effective degrees of freedom, so the null is weak
evidence in the statistical sense and we do not read it as establishing an absence."

**Proposed (replaces it with two paragraphs):** "We test the standard early-warning battery — rising lag-1
autocorrelation and rising variance of the fluctuations of $r(t)$ around a Gaussian-smoothed trend ($\sigma = 5$
years), on trailing 15-year windows — over the 8 years before each onset, with the trend measure and surrogate test of
§6.5, one-sided upward. A third indicator often added, the restoring time, was considered and dropped: estimated as
$1/(-\ln\varphi)$ from the same lag-1 autocorrelation $\varphi$, it is an increasing function of $\varphi$, so its trend
test repeats the autocorrelation's and adds no independent evidence. We complement the two indicators with a test that
treats coupling as the bifurcation parameter: inverting the mean-field Kuramoto relation $r = \sqrt{1 - K_c/K}$ gives
an implied coupling $K/K_c = 1/(1 - r^2)$, and critical slowing down would show as a fall in the recovery rate
$\lambda = -\ln\varphi$ in the years just after each onset relative to all other years, tested one-sided against the
surrogate ensemble of §5.2. Windows may start in 1962 (§7.7), so the pre-crisis windows of 1982 (six of eight years
defined), 1991, 2009 and 2020 enter; 1975 has none.

Two of the three tests are null. Lag-1 autocorrelation shows no pre-crisis rise ($\tau = -0.098$, $p = 0.68$), and
the recovery rate does not fall after onsets (change $+0.024$, $p = 0.51$). The variance of $r(t)$ does rise before
crises ($\tau = +0.420$, $p = 0.037$), but without the rise in autocorrelation. Critical slowing down raises both
together, because both follow from a slower return to equilibrium; variance alone also rises when the shocks that move
$r(t)$ grow larger. A rise in variance without a rise in autocorrelation is therefore not the slowing-down signature.
The variance rise also rests on the two modern events, like the lead of §6.3: the windows before 2009 and 2020 alone
give $\tau = +0.857$ ($p = 0.005$), those before 1982 and 1991 give $\tau = -0.018$ ($p = 0.53$), and dropping either
2009 or 2020 leaves it short of significance ($p = 0.20$ and $0.18$). It is significant under convention P but not under
W, N or the edge-robust E ($p = 0.11$, $0.075$ and $0.054$; §7.2). Annual data over 8-year pre-crisis windows give
these estimators very few effective degrees of freedom, so the nulls are weak evidence in the statistical sense and we
do not read them as establishing an absence."

**Current (second paragraph, sentences that change):** "Rising autocorrelation and variance are the specific
signature of a system approaching a *bifurcation* …" and "The absence of the slowing-down fingerprint is therefore
consistent with a non-bifurcation transition, …"

**Proposed:** "Rising autocorrelation and variance together are the specific signature of a system approaching a
*bifurcation* …" and "The absence of that joint fingerprint is therefore consistent with a non-bifurcation transition,
…" (the rest of the paragraph, the Ashwin et al. taxonomy, stands).

**Why:** Sid's decisions: restoring time dropped (open issue 22); the variance result reported as it is, rising
variance without rising autocorrelation, so not the slowing-down signature. The first-run null for variance
($+0.295$, $p = 0.107$) was computed under convention W; under P it is significant on both samples ($+0.438$,
$p = 0.033$ on S26). The leave-one-crisis-out numbers come from the follow-up Sid asked for (`results/FOLLOWUP.md`,
same seed and surrogates as the pre-registered test; not pre-registered). The "2009 and 2020 alone" value is also the
pre-registered strict version (§7.7), which keeps only fully defined windows. The coupling test was run and reported in
the registry but not described in the Methods; this adds it.

## §7.1 Filter band (C)

**Current:** "The pre-crisis lead is present in all three bands but its $p$-value moves across the conventional
threshold: lead-1 gives $p = 0.019$ (2–9 yr), $0.057$ (2–8 yr) and $0.038$ (3–10 yr). The post-crisis decline is not
robust to the band: the lag $-2$ coefficient is $-0.28$ ($p=0.019$) at 2–9 years but only $-0.02$ ($p=0.45$) at 3–10
years."

**Proposed:** "The pre-crisis lead is present in all three bands (lead-1 between $+0.18$ and $+0.24$) but its
$p$-value moves across the conventional threshold: lead-1 gives $p = 0.019$ (2–9 yr), $0.113$ (2–8 yr) and $0.019$
(3–10 yr). The post-crisis decline is not robust to the band: the lag $-2$ coefficient is $-0.24$ ($p = 0.057$) at 2–9
years, $-0.26$ ($p = 0.038$) at 2–8 years and $+0.02$ ($p = 0.57$) at 3–10 years."

**Why:** S30 values (`results/S30/P/robustness.json`). Lead-1 at 2–8 years is weaker on S30 (p 0.113) than on S26
(0.057).

## §7.2 Detrending method and phase convention (C, B1)

**Current:** "Substituting an HP filter ($\lambda = 100$) for the band-pass leaves the lead result materially unchanged
(lead-1 $+0.27$, $p=0.019$). Using first differences of log GDP per capita instead weakens the lead-2 term to $p=0.094$
and eliminates the post-crisis decline entirely ($-0.01$, $p=0.51$). The post-crisis result is thus method-dependent in
a way the pre-crisis result is not. Separately, as noted in §1, the run-in convention moves this coefficient
materially: computing both $r$ and $\bar{A}$ on the 1970–2022 window without run-in gives $+0.531$ detrended against
$+0.608$ with run-in, at the same $p = 0.019$. We report the run-in-protected value throughout, on the ground that the
edge transients it removes are an artifact, not because it is the larger; the sign and significance of the result are
the same either way."

**Proposed (retitled "Detrending method and phase convention"):** "Substituting an HP filter ($\lambda = 100$) for the
band-pass leaves the lead result materially unchanged (lead-1 $+0.27$, $p = 0.019$). Using first differences of log GDP
per capita instead weakens the lead-2 term to $p = 0.075$ and eliminates the post-crisis decline entirely ($+0.04$,
$p = 0.68$). The post-crisis result is thus method-dependent in a way the pre-crisis result is not.

The phase convention matters too. Besides the convention used throughout (P: band-pass and Hilbert transform on
1950–2022, statistics on 1970–2022) we compute four others: W, the Hilbert transform on 1970–2022 only, after the same
band-pass; N, both steps on 1970–2022 only, with no run-in; E, an edge-robust version of P that mirrors each cycle by
nine years (the longest period in the band) at both ends before the Hilbert transform; and C, phases from past data
only, recomputing the band-pass and Hilbert transform on the data up to each year and keeping that year's phase. C uses
no future data, so a lead that survives it is not an artifact of the two-sided filters.

| Convention | Lead-2 | Lead-1 | Lag $-2$ | $r$–$\bar A$, detrended |
|---|---|---|---|---|
| P | $+0.226$ (0.038) | $+0.217$ (0.019) | $-0.236$ (0.057) | $+0.641$ (0.019) |
| W | $+0.204$ (0.075) | $+0.184$ (0.057) | $-0.131$ (0.170) | $+0.549$ (0.019) |
| N | $+0.204$ (0.019) | $+0.173$ (0.094) | $-0.158$ (0.132) | $+0.535$ (0.019) |
| E | $+0.224$ (0.038) | $+0.226$ (0.019) | $-0.136$ (0.170) | $+0.577$ (0.019) |
| C | $-0.021$ (0.528) | $+0.369$ (0.038) | $-0.161$ (0.170) | $+0.723$ (0.019) |

Lead-1 is significant under P, E and C and falls short under W and N ($p = 0.057$ and $0.094$). It is the one result
of §6.3 that survives phases built from past data only, and it is the one we interpret. Lead-2 does not survive
past-only phases, and the post-crisis fall is significant under none of the five conventions. The
synchronization–amplitude link is significant at the floor under every convention, which moves its size between
$+0.535$ and $+0.723$. We report P throughout, on the ground that the edge transients its run-in removes are an
artifact, not because it gives the larger values."

**Why:** B1, with Sid's decision on the arc's wording: a robust rise one year before recessions, which survives
past-only phases, and a fragile post-crisis collapse, moved to Limitations (L3). The first draft's "short" option
(W numbers only) is superseded: E and C were pre-registered and run, and C is what rule 7 needs. Under N, lead-2
has a smaller coefficient than under P but a smaller p (0.019 against 0.038): each convention's p comes from shifting
its own r(t), so p-values need not order with coefficients.

## §7.3 Leave-one-crisis-out (C)

**Current:** "It survives removal of 1975, 1982 and 1991, but dropping either 2009 or 2020 destroys the lead-1
significance, and dropping both leaves no lead at all. A split-sample fit tells the same story: 1970–1995 (crises
1975, 1982, 1991) shows no significant lead, while 1996–2022 (crises 2009, 2020) does."

**Proposed:** "Lead-1 survives removal of 1982 and 1991 ($p = 0.019$) and weakens to $p = 0.057$ without 1975, but
dropping either 2009 or 2020 destroys its significance ($p = 0.23$ and $0.32$), and dropping both leaves no lead at all
($-0.03$, $p = 0.53$). A split-sample fit tells the same story: 1970–1995 (crises 1975, 1982, 1991) shows no
significant lead (lead-1 $+0.21$, $p = 0.15$), while 1996–2022 (crises 2009, 2020) does ($+0.37$, $p = 0.037$, the
floor for 27 years)." Add at the end of the paragraph: "The variance rise of §6.7 rests on the same two events."

**Why:** S30 values. New on S30: without 1975, lead-1 is p 0.057 (on S26 it stayed at 0.019).

## §7.4 Multiplicity (A1, C)

**Current:** "Across the five lags of §6.3, no coefficient survives a Bonferroni correction (lead-1 and lag $-2$:
$p_{\mathrm{adj}} = 0.095$; lead-2: $0.189$). Under Benjamini–Hochberg control of the false discovery rate, lead-1 and
lag $-2$ reach $q = 0.047$ and lead-2 $q = 0.063$. The permutation floor of §5.1 caps how much correction the raw values
can absorb: $0.019$ is already the smallest value the test can return."

**Proposed:** "Across the five lags of §6.3, no coefficient survives a Bonferroni correction (lead-1:
$p_{\mathrm{adj}} = 0.094$; lead-2: $0.189$; lag $-2$: $0.283$) or Benjamini–Hochberg control of the false discovery
rate ($q = 0.094$ for lead-2, lead-1 and lag $-2$). On the original 26 economies lead-1 and lag $-2$ reached
$q = 0.047$ (§7.8). The permutation floor of §5.1 caps how much correction the raw values can absorb: $0.019$ is
already the smallest value the test can return, so with five lags no coefficient can pass Bonferroni
($5/53 = 0.094$)."

**Why:** A1 (0.094, not 0.095) with S30 values. **On S30 nothing survives either correction**; under the
pre-registration A1–A5 on S30 is the primary family, so this is the multiplicity statement the paper must make.

## §7.5 Leave-one-economy-out (C)

**Current:** "Removing the United States, Germany or Japan individually leaves the lead–lag profile essentially
unchanged (lead-1 $p = 0.038$, $0.019$, $0.019$ respectively). No single large economy drives the result."

**Proposed:** "Removing any one of the 30 economies leaves lead-1 between $+0.21$ and $+0.23$ with $p \le 0.038$ (the
United States, Germany and Japan: $p = 0.019$ each). No single economy drives the result, including each of the four
added in this version (§7.8)."

**Why:** the pre-registered run leaves every economy out, not only three.

## §7.6 Surrogate test of the decomposition (C)

**Current:** "Against 5,000 surrogate sets, 2,385 draws exceed the observed equal-weighted share and 1,741 exceed the
GDP-weighted share — nominal $p$-values of $0.48$ and $0.35$, … Tested on the unnormalized components instead, both
$\Delta_{\text{cross}}$ and $\Delta_{\text{own}}$ exceed every one of the 5,000 surrogates ($p = 2\times10^{-4}$, the
ensemble resolution floor), but that test is uninformative …" and, in the second paragraph, "on four events".

**Proposed:** "Against 5,000 surrogate sets, 2,331 draws equal or exceed the observed equal-weighted share and 1,593
the GDP-weighted share — nominal $p$-values of $0.47$ and $0.32$, … Tested on the unnormalized components instead,
$\Delta_{\text{cross}}$ exceeds every one of the 5,000 surrogates under both weightings ($p = 2\times10^{-4}$, the
ensemble resolution floor), and so does $\Delta_{\text{own}}$ equal-weighted (GDP-weighted it exceeds all but 173,
$p = 0.035$), but that test is uninformative …" and "on five events".

**Why:** S30 values, seed 707 as run. The first-run counts (2,385 and 1,741) came from a random stream not in the
repository (decision log, 11 October).

## §7.7 Window convention of the rolling statistics (A3, C)

**Current:** "**7.7 Window-convention sensitivity of the network measure.** $L(t)$ is reported on 10-year windows, and
its early values depend on whether the window is allowed to reach back into the 1950–69 run-in. Restricting windows to
1970 onward, $L$ is defined from 1979 and the decade-mean comparison becomes $0.652$ (1979–89) against $0.379$
(2013–2022). The convention is stated wherever $L$ is quoted."

**Proposed:** "**7.7 Window convention of the rolling statistics.** Every rolling statistic — the network measure
(§6.5), the decomposition (§6.1) and the early-warning and coupling tests (§6.7) — uses windows that may start in 1962
and never earlier, leaving at least twelve years of filter run-in. As a sensitivity check each is recomputed with
windows kept inside 1970–2022, dropping any pre-crisis window that is then only partly defined. For $L$ this changes no
value from 1979 onward, so the decade means of §6.5 are unaffected; the pre-crisis contraction test, now on 1991, 2009
and 2020, stays null ($\tau = +0.119$, $p = 0.69$ raw; $+0.381$, $p = 0.94$ detrended). The decomposition loses the 1975
window and gives $85.9\%$ GDP-weighted and $96.7\%$ equal-weighted. Lag-1 autocorrelation ($\tau = -0.036$,
$p = 0.55$) and the coupling test ($+0.102$, $p = 0.53$) stay null; the variance trend, now on 2009 and 2020 only, is
$+0.857$ ($p = 0.005$)."

**Why:** Sid's rolling-window rule (A3), with the Phase 3 strict values filled in (`results/S30_strict/P/`).

## §7.8 The original 26 economies and the four added ones (new section, C)

**Proposed:** "**7.8 The original 26 economies and the four added ones.** Every test was also run on the original 26
economies, under the same conventions. The lead–lag profile is almost the same: lead-2 $+0.230$ ($p = 0.038$), lead-1
$+0.216$ ($p = 0.019$), lag $-2$ $-0.277$ ($p = 0.019$); with phases from past data only, lead-1 is $+0.374$
($p = 0.038$) and lead-2 $+0.007$ ($p = 0.45$). Under Benjamini–Hochberg, lead-1 and lag $-2$ reach $q = 0.047$. The
synchronization–amplitude link is $+0.608$ detrended ($+0.530$ raw; $p = 0.019$; surrogate $p = 2\times10^{-4}$). The
cross-term supplies $80.2\%$ of the excess crisis variance GDP-weighted and $96.5\%$ equal-weighted ($82.4\%$ and
$96.9\%$ with windows inside 1970–2022), and inside it the larger swings supply more than the higher correlations
($53\%$ against $33\%$, interaction $14\%$). The network tightens by $1.8\times$ (decade means $0.677$ against $0.379$).
The phase-lead spread is $0.445$ years ($p = 2\times10^{-4}$, the floor). Lag-1 autocorrelation shows no pre-crisis
rise ($+0.027$, $p = 0.46$), while variance does ($+0.438$, $p = 0.033$; without 2009 and 2020, $+0.125$,
$p = 0.41$).

Each of the four added economies was left out in turn. Lead-1 stays at $p \le 0.038$ in every case; lead-2 moves to
$p = 0.057$ without China and lag $-2$ to $p = 0.019$ without Brazil; the synchronization–amplitude link stays between
$+0.621$ and $+0.649$ and the variance trend at $p \le 0.043$. Iran and Saudi Arabia have cycles $2.9$ and $2.2$ times
the median size of the original 26. The order parameter uses phases only, but the decomposition weighs swing size, so
the two were also left out together: the synchronization–amplitude link is then $+0.620$, the cross-term's share of
the excess $82.5\%$ GDP-weighted and $96.8\%$ equal-weighted, and its rise splits $41\%$ correlation, $44\%$ swing size.
Finally, Maddison's per-capita growth for Norway, Switzerland and South Africa runs two to three points above national
accounts in 1991–2011; replacing it with the Global Macro Database's real GDP per capita growth leaves lead-1 at
$+0.224$ ($p = 0.019$) and changes no conclusion."

**Why:** the pre-registration made the leave-out of each added economy and of Iran and Saudi Arabia together
mandatory (Sid). The S26 values are under the pre-registered conventions, so several differ from the first-run values
the current Methods quote; old and new are in the decision log (rule 6). **For Sid:** this section is long for a
Methods; part of it could be a table in the Appendix.

## §8 Reproducibility (B2, B4, C)

**Current:** "The input data are the Maddison Project Database (2023 release) as distributed in the `MaddisonData` R
package (v1.1.0). The pipeline is deterministic apart from the surrogate ensembles, which are seeded. Rebuilt from the
raw database, it reproduces the order-parameter series to floating-point round-off ($3\times10^{-16}$) and reproduces
every lead–lag coefficient and $p$-value exactly. The equal-weighted variance decomposition of §6.1 reproduces to
$1.5\times10^{-18}$.

Two quantities in earlier internal result files could not be reproduced from the raw data and are reported here at
their rebuilt values: the synchronization–amplitude correlation (§6.2, rebuilt $+0.608$ detrended) and the
correlation between mean pairwise cycle correlation and the order parameter (rebuilt $+0.45$ to $+0.51$ depending on
the run-in convention). We were unable to recover the exact amplitude convention behind the earlier figures; the
qualitative conclusions are unaffected in both cases, and the rebuilt values are the ones stated throughout."

**Proposed:** "The input data are the Maddison Project Database (2023 release) as distributed in the `MaddisonData` R
package (repository `sbgraves237/maddisondata`, commit `3ed424b6`; the data file `MaddisonData.rda`, sha256
`63a3cff9…`, is unchanged since October 2025). The pipeline rebuilds from these pinned files with one command and is
deterministic apart from the surrogate ensembles, which are seeded; every result is saved with its settings, seed and
code version. The sample, phase convention, tests and test directions for the 30 economies were written down and signed
before any test was run on the four added economies, and every pre-registered test is reported. The earlier results on
the 26 economies reproduce exactly from the rebuilt pipeline under the conventions they were first run with, including
every surrogate $p$-value.

Two quantities in earlier internal result files differ from the values stated here. The synchronization–amplitude
correlation of early drafts, $+0.51$, applied the Hilbert transform to the 1970–2022 window only after a 1950–2022
band-pass (convention W of §7.2); it reproduces exactly under that convention. The correlation between mean pairwise
cycle correlation and the order parameter was $+0.45$ to $+0.51$ on the 26 economies, depending on the run-in
convention. Neither changes a conclusion."

**Why:** B2 (open issue 3: the convention is now known) and B4 (open issue 15: the exact data citation). The last
sentence of the first paragraph replaces the specific round-off figures, which described one machine (the golden check
reproduces 101 of 101 values to $10^{-12}$; `docs/golden_check.md`).

## Methods diagnostics figure caption (C)

**Current:** "Panel **a**: MST mean edge length by year (grey) with decade means (blue) and the single-year endpoints
(red) that produce the $\sim3\times$ ratio; decade means give $1.9\times$ and are the interpreted quantity. Panel **b**:
the phase-lag spread against its 5,000-member surrogate null — the observed $0.403$ yr lies below every surrogate, a
lower-tail result at the ensemble floor."

**Proposed:** "Panel **a**: MST mean edge length by year from 1971 (grey) with the decade means for 1979–89 and
2013–22 (blue), $0.680$ against $0.421$, a factor of $1.6\times$. Panel **b**: the phase-lag spread against its
5,000-member surrogate null — the observed $0.535$ yr lies below all but one surrogate ($p = 4\times10^{-4}$)." Panel
**c** unchanged in wording (its values become S30's: Bonferroni 0.189, 0.094, 0.943, 1.0, 0.283).

**Why:** the figure is redrawn from the S30 results in Phase 4 (open issue 18).

---

## Outside the Methods: Results and Limitations text (L1–L3)

For the paper's Results and Limitations sections (`docs/paper_plan.md`), not for `docs/methods.md`. Drafted from Sid's
decisions of 11 October 2026.

### L1. Results: the pre-crisis rise (Sid's wording)

"Synchronization rises in the year before global recessions (lead-1 $+0.217$, $p = 0.019$, the floor of the
permutation test). The rise holds with any one of the 30 economies left out, under the edge-robust convention and with
phases built from past data only ($+0.369$, $p = 0.038$). It rests on 2009 and 2020: without either it is not
significant (§7.3). It is a property of the tightly coupled modern economy, not a fifty-year regularity, and not a
forecast. The two-year lead (lead-2 $+0.226$, $p = 0.038$) does not survive past-only phases and is not claimed."

### L2. Results: the channels inside the economies (Sid: the rate lead dropped as a lead claim)

"With two-sided phases, short-term interest rates are most synchronized two years before global recessions ($+0.273$,
$p = 0.019$, 19 economies with continuous rates), investment two and one years before ($+0.270$ and $+0.262$, 28
economies) and real GDP one year before ($+0.245$, $p = 0.019$, 29 economies). We report this ordering as a
description only. With phases from past data only neither two-year rise survives (short rates $+0.165$, $p = 0.15$;
investment $-0.110$, $p = 0.72$), so we make no claim that rates or investment signal recessions in advance. On these
real GDP series (the Global Macro Database, not Maddison), the past-only lead-1 is $+0.311$ ($p = 0.057$)."

### L3. Limitations: the fall after recessions (Sid: moved to Limitations)

"Synchronization falls in the two years after a global recession (lag $-2$: $-0.236$ on the 30 economies,
$p = 0.057$; $-0.277$, $p = 0.019$ on the original 26), but this half of the arc does not hold up. It is not
significant on the 30; it disappears with the 3–10 year band and with growth rates (§7.1–7.2); it is significant under
none of the alternative phase conventions, including phases from past data only (§7.2); and without 2020 it is
$-0.17$ ($p = 0.17$). It also sits where the filters are least reliable: the lag $-2$ test for 2020 uses $r(2022)$, the
last observation. We report it and do not claim it."

The other Limitations items in `docs/paper_plan.md` (the lead rests on 2009 and 2020; five events; annual data) stand;
the variance rise of §6.7 joins the first of them.
