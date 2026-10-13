# Proposed edits to the Methods

`docs/methods.md` is not changed. Each edit below quotes the current text, gives the proposed text and the reason.

**Fourth draft, 13 October 2026: S31 is the main sample.** Pre-registration amendment 3 (Sid) made S31 = S30 + Russia
the main sample, with S30 as the reported comparison. Every number below is the 31-economy value under convention P,
with the S30 value beside it where the paper should show both ("S30: …"); the original 26 are in §7.8 and Appendix
Table A1. No primary result changes sign or crosses p = 0.05 between S30 and S31 (`results/COMPARISON.md` §25).
Sources: `results/S31/P/*.json` (code 2a686a3) and `results/S30/P/*.json` (code 07bbdd8), `results/COMPARISON.md`,
`results/FOLLOWUP.md` (the leave-one-crisis-out check Sid asked for, not pre-registered) and
`docs/data_validation.md` (share of world GDP, Russia's data).

**The paper's framing (Sid, second round):** the mechanism is loss of diversification, not bifurcation tipping; the
tipping tests are the "what it isn't" that led to it. Results say "loss of diversification"; the Discussion proposes
"diversification-type tipping" as our own term (D2).

The edits are in Methods order. Each heading carries its label from the first draft so they can be traced:

| Label | What | Section | Status |
|---|---|---|---|
| A1 | Bonferroni value; what the multiplicity correction can and cannot show | §7.4 | decided; rewritten for Sid's second-round decision |
| A2 | MST windows and decade means | §6.5 | decided; S31 values (S30 beside) replace S26 (1.6× instead of 1.8×) |
| A3 | One window rule for all rolling statistics | §7.7 | decided; Phase 3 sensitivity numbers filled in |
| A4 | Early-warning battery: two indicators plus the coupling test | §6.7 | decided; the variance rise read as consistent with loss of diversification (Sid) |
| B1 | The arc depends on the phase convention | §1, §6.3, §7.2 | decided wording (Sid) |
| B2 | The earlier amplitude convention is known | §8 | drafted |
| B3 | The cross-term split | §6.1 | decided: "co-movement and larger swings contribute about equally"; the interpretation goes to the Discussion (Sid) |
| B4 | Data citation | §8 | drafted |
| B5 | The detrended pre-crisis MST test | §6.5 | drafted with the Phase 3 value |
| C | Phase 3 numbers | every section | filled in |
| N1–N3 | Expected r under random phases; the cross-share formula needs equal variances; surrogates follow P | §3, §6.1, §5.2 | approved (Sid) |
| — | Why the five economies were added (Russia by amendment 3); share of world GDP | §1 | drafted from Sid's wording; Russia settled (S31) |
| — | The original 26, S30 and the added economies | §7.8, Appendix Table A1 | decided: one paragraph, full table in an Appendix (Sid); now with S31 |
| L1–L7 | Results and Limitations text | outside the Methods | drafted from Sid's decisions; for the paper, not for `methods.md` |
| D1–D2 | Discussion text: the mechanism and "diversification-type tipping" | outside the Methods | drafted from Sid's framing |

---

## §1 Data (C, B1)

**Current (first paragraph):** "We use annual real GDP per capita from the Maddison Project Database (2023 release),
PPP-adjusted, for a fixed panel of $N = 26$ economies: Australia, Austria, Belgium, Canada, Denmark, Finland, France,
Germany, Greece, India, Indonesia, Italy, Japan, Mexico, the Netherlands, Norway, Portugal, South Africa, South Korea,
Spain, Sweden, Switzerland, Thailand, Turkey, the United Kingdom and the United States. The panel is balanced: every
economy has an uninterrupted annual observation from 1950 to 2022, so no interpolation, gap-filling or
unbalanced-panel weighting enters the pipeline at any stage."

**Proposed:** "We use annual real GDP per capita from the Maddison Project Database (2023 release), PPP-adjusted, for a
fixed panel of $N = 31$ economies: Australia, Austria, Belgium, Brazil, Canada, China, Denmark, Finland, France,
Germany, Greece, India, Indonesia, Iran, Italy, Japan, Mexico, the Netherlands, Norway, Portugal, Russia, Saudi
Arabia, South Africa, South Korea, Spain, Sweden, Switzerland, Thailand, Turkey, the United Kingdom and the United
States. The panel is balanced: every economy has an uninterrupted annual observation from 1950 to 2022, so no
interpolation, gap-filling or unbalanced-panel weighting enters the pipeline at any stage. An earlier version of this
analysis used the first 26 of these economies. China, Russia and Brazil are the largest economies missing from them,
and Saudi Arabia and Iran add the oil-exporting Middle East; Russia, the second largest, was first left out by
oversight, not by the inclusion rule, and was added before any test was run on it. The inclusion rule, the phase
convention, the tests and their directions were written down before any test was run on the added economies (§8); the
rule admits an economy only with a complete Maddison series for 1950–2022, which excluded the United Arab Emirates (its
series misses 1991–1992). Russia's values before 1991 are back-cast estimates for the Soviet period, not market
national accounts, so every test that allows it is also run with Russia's phases computed from 1992 only (§7.8). In
Maddison's PPP figures the original 26 produced $67\%$ of world GDP in 1970 and $51\%$ in 2022; the 31 produce $81\%$
and $80\%$ (without Russia, $76\%$ and $77\%$). Every result is also given without Russia, for the 30 (§7.8 and
Appendix Table A1)."

**Current (end of third paragraph):** "It is a consequential choice rather than a formality: recomputing phases on a
1970–2022 series alone, with no run-in, changes the order parameter materially in individual years and shifts the
synchronization–amplitude coefficient of §6.2 by roughly $0.08$ (§7.2)."

**Proposed:** "It is a consequential choice rather than a formality: recomputing phases on a 1970–2022 series alone,
with no run-in, changes the order parameter materially in individual years, shifts the synchronization–amplitude
coefficient of §6.2 by roughly $0.1$ and moves the lead–lag profile of §6.3 (§7.2)."

**Why:** Sid's decisions: S31 is the main sample (amendment 3, 13 October 2026), with his reason for Russia. World GDP
shares from `docs/data_validation.md` (`ef.data.maddison.world_share`: GDP per capita × population; the former USSR,
Czechoslovakia and Yugoslavia counted as Maddison's aggregates so nothing is counted twice; the 26, 30 and 31 produce
62%, 78% and 81% of world GDP on average over 1970–2022). Open issue 24 (Russia) is settled by the amendment. On the
back-cast: the validation report found that Russia's pre-1991 Maddison values are not a fixed share of Maddison's own
USSR series (Russia's share rises from 41% in 1950 to 62% in 1980) and that the Maddison documentation we found does
not say how they were made; "back-cast estimates for the Soviet period" is as far as the text can go.

The run-in shift is
$0.646 - 0.547 = 0.099$ on S31 ($0.641 - 0.535 = 0.106$ on S30; $0.608 - 0.531 = 0.077$ on S26). The clause on the lead–lag profile is the short form
of B1; the numbers are in §7.2.

## §3 Synchronization measure (C, N1)

**Current:** "Treating the 26 economies as a population of phase oscillators, …" and "with $N = 26$ the expected value
under independent uniform phases is $\approx N^{-1/2} \approx 0.20$."

**Proposed:** "Treating the 31 economies as a population of phase oscillators, …" and "with $N = 31$ its
root-mean-square under independent uniform phases is exactly $N^{-1/2} \approx 0.18$ (its mean is about $0.16$)."

**Why (N1, new):** under independent uniform phases $E[r^2] = 1/N$ exactly, so $N^{-1/2}$ is the root-mean-square of
$r$, not its mean; the mean is $\sqrt{\pi/(4N)}$, 0.16 for 31 or 30 economies (0.17 for 26). The point of the sentence (do
not read the level of $r$ against zero) is unchanged.

## §5.2 Spectrum-preserving surrogates (C, N3)

**Current:** "we generate 5,000 surrogate 26-economy sets by Fourier phase randomization."

**Proposed:** "we generate 5,000 surrogate 31-economy sets by Fourier phase randomization." Add at the end of the
paragraph: "Surrogates are drawn from each economy's 1950–2022 cycle and pass through the same Hilbert transform and
1970–2022 window as the data, so real and surrogate phases share one convention (§7.2)."

**Why (N3, new):** the pre-registration fixed this; several first-run scripts drew surrogates under convention W while
the data used P. It is why the amplitude link's surrogate p moved from 0.0006 to the floor 0.0002 on S26.

## §6.1 Loss-of-diversification decomposition (C, N2, B3)

**Current (first paragraph):** "The world output cycle is the weighted aggregate of the 26 band-passed economy cycles,"

**Proposed:** "… of the 31 band-passed economy cycles,"

**Current (second paragraph, from "That is algebraically guaranteed"):** "That is algebraically guaranteed: for equal
weights the cross share is $\mathrm{cross}/\mathrm{total} = (N-1)\bar\rho / (1 + (N-1)\bar\rho)$, so with $N = 26$ the
$325$ covariance pairs outnumber the $26$ variances by more than an order of magnitude and the cross-term dominates at
any $\bar\rho$ above a few hundredths. Observed $\bar\rho$ ranges from $0.13$ to $0.88$ across our windows, which alone
forces a cross share between $0.76$ and $0.96$. Reporting a high cross share as a finding would therefore be reporting
arithmetic."

**Proposed:** "That is close to algebraically guaranteed: for equal weights and equal cycle variances the cross share
is $\mathrm{cross}/\mathrm{total} = (N-1)\bar\rho / (1 + (N-1)\bar\rho)$, so with $N = 31$ the $465$ covariance pairs
outnumber the $31$ variances by more than an order of magnitude and the cross-term dominates at any $\bar\rho$ above a
few hundredths. Observed $\bar\rho$ ranges from $0.08$ to $0.77$ across our windows, which alone would force a cross
share between $0.69$ and $0.96$ if the economies swung equally. Unequal swings lower the share wherever one economy
dominates the own-term: the equal-weighted share ranges from $0.19$ to $0.95$ and stays below $0.40$ in most windows
ending 1985–1996, when Iran's cycle alone supplies between a fifth and two-fifths of the own-term. Reporting a high
cross share as a finding would therefore still be reporting arithmetic."

**Why (N2, new):** the formula holds only when every economy's cycle variance is the same. On S26 it gave 0.76–0.96
while the actual equal-weighted share ran from 0.62 to 0.95 (lowest in 1999, Indonesia, Turkey and Thailand); on S30
the gap is large because of Iran (S30: ρ̄ 0.08–0.81, share 0.21–0.95). Values from `ef.decomposition.rolling`, windows from 1962.

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
weightings: $84.3\%$ GDP-weighted and $97.0\%$ equal-weighted (S30: $83.3\%$ and $96.8\%$). The underlying
cross-shares are $0.706$ in crisis windows against $0.620$ in normal windows (GDP-weighted), and $0.783$ against $0.691$
(equal-weighted). The direction is consistent across weightings, and the gap is a shift of about nine percentage points
on a base of about two-thirds. The equal-weighted figure is the larger because equal weights give the 465 covariance
pairs their maximum
leverage; …" (rest unchanged)

**New paragraph after it (B3):** "The cross-term is not the same thing as correlation: it rises when economies move
together and when they swing harder. Changing only the pairwise correlations from their normal-window means to their
crisis-window means (mean correlation $0.291 \to 0.385$) supplies $46\%$ of the cross-term's crisis rise
GDP-weighted ($50\%$ equal-weighted); changing only the cycle sizes (mean cycle s.d. $\times 1.10$) supplies $40\%$
($37\%$); their interaction supplies the remaining $14\%$ ($13\%$). On the 30 without Russia the split is $44$, $41$
and $15\%$. The two parts are of similar size, and which is
larger depends on the sample: on the original 26 economies the larger swings supplied more ($53\%$ against $33\%$;
§7.8). Co-movement and larger swings contribute about equally."

**Why:** S31 values (`results/S31/P/diversification.json`, `cross_split.json`), S30 beside. The weights are the Methods'
within-window mean GDP, as stated. On B3: the first draft's 35/50/14% was S26 with four recessions and end-of-window
weights. Sid's decision: Methods and Results say "co-movement and larger swings contribute about equally";
"amplification transmitted by alignment" is kept as interpretation in the Discussion only (D1).

## §6.2 Synchronization–amplitude coupling (C)

**Current:** "The two versions agree closely — $+0.530$ raw against $+0.608$ detrended, at the same $p = 0.019$ — so
the result does not hinge on the detrending choice; … Significance is assessed by the circular-shift null of §5.1
applied to the paired series, and separately against the surrogate ensemble of §5.2."

**Proposed:** "The two versions agree in sign and significance — $+0.472$ raw against $+0.646$ detrended, both at the
floor $p = 0.019$ (S30: $+0.458$ and $+0.641$) — so the result does not hinge on the detrending choice; … Significance is assessed by the
circular-shift null of §5.1 applied to the paired series, and separately against the surrogate ensemble of §5.2
($p = 2\times10^{-4}$, the ensemble floor)."

**Why:** S31 values, S30 beside. "Agree closely" no longer fits a gap of 0.17.

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

**Proposed:** "$31\times31$ Pearson correlation matrix" in the first sentence, and: "Windows may start in 1962 and
never earlier, so that each has at least twelve years of filter run-in (§7.7); $L(t)$ is therefore defined from 1971.
Two questions are asked of $L$: whether it trends secularly — reported as a description via decade means, $0.687$ in
1979–89 (the first decade whose windows all lie inside the 1970–2022 analysis window) against $0.424$ in 2013–2022, a
factor of $1.6\times$ (S30: $0.680$ against $0.421$, also $1.6\times$) — and whether contraction coincides with the pre-crisis windows. The latter is quantified by a
Kendall-$\tau$ trend over the 8 years preceding each onset, averaged over crises (1975's window has four of its eight
years defined), and tested one-sided downward against the surrogate ensemble of §5.2, both on raw $L$ and on $L$ minus
a Gaussian-smoothed copy of itself ($\sigma = 8$ years). Both are null: $\tau = -0.157$, $p = 0.21$ on raw $L$ and
$\tau = +0.014$, $p = 0.56$ detrended (S30: $-0.143$, $p = 0.22$; $+0.057$, $p = 0.66$)."

**Why:** Sid's decisions on the window rule and the decade comparison (A2), with S31 values. **The headline factor is
1.6× (S31 and S30) instead of 1.8× (S26)**: the added economies are less tightly tied to the rest in the last decade
(0.424 against 0.379); see §7.8. B5: the first-run detrended value ($-0.086$, $p = 0.316$) did not reproduce with any smoothing
width tried (open issue 23); the pre-registration fixed $\sigma = 8$, which the Methods now state. I propose not
mentioning the irreproducible value in the paper (it was never published); it stays in the registry and decision log.

## §6.6 Phase-lag structure (C)

**Current:** "… giving a mean cycle period of 5.85 years) … The test statistic is the standard deviation of these 26
lags, observed at $0.403$ years … the observed $0.403$ yr lies below all 5,000 surrogate values (surrogate mean
$0.942$, minimum $0.446$), giving $p = 2\times10^{-4}$, the ensemble resolution floor."

**Proposed:** "… giving a mean cycle period of 5.93 years) … The test statistic is the standard deviation of these 31
lags, observed at $0.546$ years … the observed $0.546$ yr lies below all 5,000 surrogate values (surrogate mean
$0.992$, minimum $0.554$), giving $p = 2\times10^{-4}$, the ensemble resolution floor (S30: $0.535$ yr,
$p = 4\times10^{-4}$)."

**Why:** the first-run 0.403 was computed under convention W; under P it is 0.445 on S26 (§7.8), 0.535 on S30 and 0.546 on S31. Russia trails the world cycle by 0.76 years. The
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

Two of the three tests are null. Lag-1 autocorrelation shows no pre-crisis rise ($\tau = -0.152$, $p = 0.79$), and
the recovery rate does not fall after onsets (change $+0.002$, $p = 0.50$). The variance of $r(t)$ does rise before
crises ($\tau = +0.438$, $p = 0.031$; S30: $+0.420$, $p = 0.037$), but without the rise in autocorrelation. Critical slowing down raises both
together, because both follow from a slower return to equilibrium; variance alone also rises when the shocks that move
$r(t)$ grow larger. A rise in variance without a rise in autocorrelation is therefore not the slowing-down signature.
It is what loss of diversification (§6.1) would produce: when shocks to the economies stop cancelling, $r(t)$ swings
more widely without returning more slowly. This is a reading of the result, not a separate test. The variance rise
also rests on the two modern events, like the lead of §6.3: the windows before 2009 and 2020 alone
give $\tau = +0.857$ ($p = 0.003$), those before 1982 and 1991 give $\tau = +0.018$ ($p = 0.51$), and dropping either
2009 or 2020 leaves it short of significance ($p = 0.21$ and $0.13$). It is significant under convention P and the
edge-robust E ($p = 0.045$) but not under W or N ($p = 0.135$ and $0.073$; on S30, E gives $p = 0.054$; §7.2). Annual data over 8-year pre-crisis windows give
these estimators very few effective degrees of freedom, so the nulls are weak evidence in the statistical sense and we
do not read them as establishing an absence."

**Current (second paragraph, sentences that change):** "Rising autocorrelation and variance are the specific
signature of a system approaching a *bifurcation* …" and "The absence of the slowing-down fingerprint is therefore
consistent with a non-bifurcation transition, …"

**Proposed:** "Rising autocorrelation and variance together are the specific signature of a system approaching a
*bifurcation* …" and "The absence of that joint fingerprint is therefore consistent with a non-bifurcation transition,
…" (the Ashwin et al. taxonomy stands).

**Current (last sentence of the section):** "We record the classification here and leave the mechanism argument to the
Discussion; nothing in this paper identifies which non-bifurcation route applies."

**Proposed:** "We report these tests as what the transition is not. The mechanism the paper proposes is loss of
diversification (§6.1), argued in the Discussion; nothing in this paper tests whether that mechanism has a
threshold."

**Why:** Sid's decisions: restoring time dropped (open issue 22); the variance result reported as it is, rising
variance without rising autocorrelation, so not the slowing-down signature. The first-run null for variance
($+0.295$, $p = 0.107$) was computed under convention W; under P it is significant on both samples ($+0.438$,
$p = 0.033$ on S26). The leave-one-crisis-out numbers come from the follow-up Sid asked for (`results/FOLLOWUP.md`,
same seed and surrogates as the pre-registered test; not pre-registered). The "2009 and 2020 alone" value is also the
pre-registered strict version (§7.7), which keeps only fully defined windows. The coupling test was run and reported in
the registry but not described in the Methods; this adds it. Second round (Sid): the paper's mechanism is loss of
diversification, not bifurcation tipping, and the variance rise is presented as consistent with it (shocks stop
cancelling) rather than with slowing recovery.

## §7.1 Filter band (C)

**Current:** "The pre-crisis lead is present in all three bands but its $p$-value moves across the conventional
threshold: lead-1 gives $p = 0.019$ (2–9 yr), $0.057$ (2–8 yr) and $0.038$ (3–10 yr). The post-crisis decline is not
robust to the band: the lag $-2$ coefficient is $-0.28$ ($p=0.019$) at 2–9 years but only $-0.02$ ($p=0.45$) at 3–10
years."

**Proposed:** "The pre-crisis lead is present in all three bands (lead-1 between $+0.19$ and $+0.25$) but its
$p$-value moves across the conventional threshold: lead-1 gives $p = 0.019$ (2–9 yr), $0.094$ (2–8 yr) and $0.019$
(3–10 yr). The post-crisis decline is not robust to the band: the lag $-2$ coefficient is $-0.26$ ($p = 0.057$) at 2–9
years, $-0.27$ ($p = 0.019$) at 2–8 years and $0.00$ ($p = 0.51$) at 3–10 years."

**Why:** S31 values (`results/S31/P/robustness.json`). Lead-1 at 2–8 years: p 0.094 on S31, 0.113 on S30, 0.057 on S26.

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
band-pass leaves the lead result materially unchanged (lead-1 $+0.29$, $p = 0.019$). Using first differences of log GDP
per capita instead weakens the lead-2 term to $p = 0.057$ and eliminates the post-crisis decline entirely ($+0.04$,
$p = 0.68$). The post-crisis result is thus method-dependent in a way the pre-crisis result is not.

The phase convention matters too. Besides the convention used throughout (P: band-pass and Hilbert transform on
1950–2022, statistics on 1970–2022) we compute four others: W, the Hilbert transform on 1970–2022 only, after the same
band-pass; N, both steps on 1970–2022 only, with no run-in; E, an edge-robust version of P that mirrors each cycle by
nine years (the longest period in the band) at both ends before the Hilbert transform; and C, phases from past data
only, recomputing the band-pass and Hilbert transform on the data up to each year and keeping that year's phase. C uses
no future data, so a lead that survives it is not an artifact of the two-sided filters.

| Convention | Lead-2 | Lead-1 | Lag $-2$ | $r$–$\bar A$, detrended | S30 lead-1 |
|---|---|---|---|---|---|
| P | $+0.235$ (0.038) | $+0.231$ (0.019) | $-0.258$ (0.057) | $+0.646$ (0.019) | $+0.217$ (0.019) |
| W | $+0.216$ (0.057) | $+0.204$ (0.019) | $-0.165$ (0.113) | $+0.566$ (0.019) | $+0.184$ (0.057) |
| N | $+0.216$ (0.038) | $+0.192$ (0.057) | $-0.190$ (0.094) | $+0.547$ (0.019) | $+0.173$ (0.094) |
| E | $+0.233$ (0.038) | $+0.236$ (0.019) | $-0.160$ (0.132) | $+0.583$ (0.019) | $+0.226$ (0.019) |
| C | $-0.044$ (0.585) | $+0.379$ (0.038) | $-0.159$ (0.170) | $+0.726$ (0.019) | $+0.369$ (0.038) |

Lead-1 is significant under P, W, E and C and falls short under N ($p = 0.057$); on the 30 without Russia it also
falls short under W ($p = 0.057$). It is the one result
of §6.3 that survives phases built from past data only, and it is the one we interpret. Lead-2 does not survive
past-only phases, and the post-crisis fall is significant under none of the five conventions. The
synchronization–amplitude link is significant at the floor under every convention, which moves its size between
$+0.547$ and $+0.726$. We report P throughout, on the ground that the edge transients its run-in removes are an
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

**Proposed:** "Lead-1 survives removal of 1975, 1982 and 1991 ($p = 0.019$ each; without 1975 it is $p = 0.057$ on
the 30 without Russia), but dropping either 2009 or 2020 destroys its significance ($p = 0.23$ and $0.28$), and
dropping both leaves no lead at all ($-0.02$, $p = 0.49$). A split-sample fit tells the same story: 1970–1995 (crises
1975, 1982, 1991) shows no significant lead (lead-1 $+0.24$, $p = 0.15$), while 1996–2022 (crises 2009, 2020) does
($+0.38$, $p = 0.037$, the floor for 27 years)." Add at the end of the paragraph: "The variance rise of §6.7 rests on the same two events."

**Why:** S31 values. Without 1975, lead-1 is p 0.019 on S31 and S26 but 0.057 on S30: a crossing between S30 and S31 (`results/COMPARISON.md` §25).

## §7.4 Multiplicity (A1, C)

**Current:** "Across the five lags of §6.3, no coefficient survives a Bonferroni correction (lead-1 and lag $-2$:
$p_{\mathrm{adj}} = 0.095$; lead-2: $0.189$). Under Benjamini–Hochberg control of the false discovery rate, lead-1 and
lag $-2$ reach $q = 0.047$ and lead-2 $q = 0.063$. The permutation floor of §5.1 caps how much correction the raw values
can absorb: $0.019$ is already the smallest value the test can return."

**Proposed:** "Across the five lags of §6.3, no coefficient survives a Bonferroni correction (lead-1:
$p_{\mathrm{adj}} = 0.094$; lead-2: $0.189$; lag $-2$: $0.283$) or Benjamini–Hochberg control of the false discovery
rate ($q = 0.094$ for lead-2, lead-1 and lag $-2$). This is partly built into the test. With 53 circular shifts the
smallest $p$ the test can return is $1/53 = 0.019$, so no single lag can pass a Bonferroni correction over five lags
($5/53 = 0.094$), and a lag can pass Benjamini–Hochberg only if another lag also reaches the floor, as lead-1 and lag
$-2$ did together on the original 26 economies ($q = 0.047$; §7.8). Corrected significance is therefore not what
supports lead-1. Its support is that it survives phases built from past data only (§7.2) and the removal of any one
economy (§7.5); with past-only phases and China left out together it is $p = 0.057$ (Appendix Table A1), on the 31
as on the 30. It does not
survive the removal of 2009 or 2020 (§7.3)."

**Why:** A1 (0.094, not 0.095) with S31 values, and Sid's second-round decision to state plainly what multiplicity can
and cannot show. **On S31, as on S30, nothing survives either correction**; under amendment 3, A1–A5 on S31 is the
primary family. **Precision, for Sid:** "no single lag can pass Bonferroni or Benjamini–Hochberg" holds for Bonferroni always,
but for Benjamini–Hochberg only for a lag on its own: on S26 two lags at the floor passed together ($q = 0.047$), so the
text says when it can pass. The exact condition with five lags: a second lag at the floor, or four lags at 0.038 or
below. Past-only lead-1 without China: $+0.357$ ($p = 0.057$) on S31, $+0.345$ ($p = 0.057$) on S30. S31's Bonferroni and Benjamini–Hochberg values are S30's exactly (the same raw p-values).

## §7.5 Leave-one-economy-out (C)

**Current:** "Removing the United States, Germany or Japan individually leaves the lead–lag profile essentially
unchanged (lead-1 $p = 0.038$, $0.019$, $0.019$ respectively). No single large economy drives the result."

**Proposed:** "Removing any one of the 31 economies leaves lead-1 between $+0.22$ and $+0.25$ with $p \le 0.038$ (the
United States, Germany and Japan: $p = 0.019$ each). No single economy drives the result, including each of the five
added in this version (§7.8)."

**Why:** the pre-registered run leaves every economy out, not only three.

## §7.6 Surrogate test of the decomposition (C)

**Current:** "Against 5,000 surrogate sets, 2,385 draws exceed the observed equal-weighted share and 1,741 exceed the
GDP-weighted share — nominal $p$-values of $0.48$ and $0.35$, … Tested on the unnormalized components instead, both
$\Delta_{\text{cross}}$ and $\Delta_{\text{own}}$ exceed every one of the 5,000 surrogates ($p = 2\times10^{-4}$, the
ensemble resolution floor), but that test is uninformative …" and, in the second paragraph, "on four events".

**Proposed:** "Against 5,000 surrogate sets, 2,390 draws equal or exceed the observed equal-weighted share and 1,581
the GDP-weighted share — nominal $p$-values of $0.48$ and $0.32$, … Tested on the unnormalized components instead,
$\Delta_{\text{cross}}$ exceeds every one of the 5,000 surrogates under both weightings ($p = 2\times10^{-4}$, the
ensemble resolution floor), and so does $\Delta_{\text{own}}$ equal-weighted (GDP-weighted it exceeds all but 191,
$p = 0.038$), but that test is uninformative …" and "on five events".

**Why:** S31 values, seed 707 as run (S30: 2,331 and 1,593; all but 173, p 0.035). The first-run counts (2,385 and 1,741) came from a random stream not in the
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
and 2020, stays null ($\tau = +0.095$, $p = 0.65$ raw; $+0.333$, $p = 0.91$ detrended). The decomposition loses the 1975
window and gives $86.8\%$ GDP-weighted and $96.9\%$ equal-weighted. Lag-1 autocorrelation ($\tau = -0.107$,
$p = 0.64$) and the coupling test ($+0.065$, $p = 0.52$) stay null; the variance trend, now on 2009 and 2020 only, is
$+0.857$ ($p = 0.003$)."

**Why:** Sid's rolling-window rule (A3), with the strict values filled in (`results/S31_strict/P/`; S30 in `results/S30_strict/P/`, the same conclusions).

## §7.8 The original 26, the 30 and the five added economies (new section, C)

**Proposed:** "**7.8 The original 26, the 30 and the five added economies.** Every test was also run on the original 26
economies and on the 30 without Russia, under the same conventions; on the 31 with each added economy left out; with
Iran and Saudi Arabia, whose cycles are $2.9$ and $2.2$ times the median size of the 26, left out together; and with
Russia's phases computed from 1992 only, so that its back-cast Soviet-era values cannot drive the result (Appendix
Table A1). Without Russia no primary result changes sign or crosses $p = 0.05$: lead-1 is $+0.217$ ($p = 0.019$), the
synchronization–amplitude link $+0.641$, the network tightens by $1.6\times$. With Russia's phases from 1992, lead-1 is
$+0.224$ ($p = 0.019$) and the synchronization–amplitude link $+0.655$. On the 26 the lead–lag profile is almost the
same (lead-1 $+0.216$, $p = 0.019$; with past-only phases $+0.374$, $p = 0.038$), lead-1 and lag $-2$ pass
Benjamini–Hochberg together ($q = 0.047$), the network tightens by $1.8\times$, and the larger swings supply more of
the cross-term's crisis rise than the higher correlations ($53\%$ against $33\%$). Leaving out one added economy moves
lead-2 and past-only lead-1 to $p = 0.057$ without China; the fall after recessions (lag $-2$, $p = 0.057$ on the 31)
crosses to $p < 0.05$ without most single economies and with Russia from 1992, which marks it as sitting on the
threshold rather than as stronger (§7.1–7.2). The alignment share of the excess in world swing is sample-sensitive:
$39\%$ on the 26, $19\%$ on the 30, $33\%$ on the 30 without Iran and $28\%$ on the 31. Replacing Maddison's
1991–2011 growth for Norway, Switzerland and South Africa, which runs two to three points above national accounts,
with the Global Macro Database's changes no conclusion (on the 31, lead-2 moves to $p = 0.057$ and lag $-2$ to
$p = 0.038$)."

**Why:** Sid's decisions: one paragraph here, the full table in an Appendix; S30 as the reported comparison
(amendment 3). The leave-outs were mandatory under the pre-registration. On the 31, lag $-2$ is significant without 20
of the 31 economies (`results/COMPARISON.md` §25). The S26 values are under the pre-registered conventions, so several
differ from the first-run values the current Methods quote; old and new are in the decision log (rule 6).

## Appendix Table A1 (new)

**Proposed:** "**Table A1.** Key results on the original 26 economies, the 30 (without Russia), the 31, and the 31
without each added economy, with Russia's phases from 1992 only and without Iran and Saudi Arabia together.
Convention P; one-sided $p$ in brackets (circular-shift floor $0.019$, surrogate floor $0.0002$)."

| Quantity | S26 | S30 | S31 | S31 without China | without Brazil | without Saudi Arabia | without Iran | without Russia (= S30) | Russia from 1992 | without Iran and Saudi Arabia |
|---|---|---|---|---|---|---|---|---|---|---|
| A1 Arc lead-2 | +0.230 (0.038) | +0.226 (0.038) | +0.235 (0.038) | +0.226 (0.057) | +0.225 (0.038) | +0.252 (0.019) | +0.244 (0.038) | +0.226 (0.038) | +0.229 (0.038) | — |
| A2 Arc lead-1 | +0.216 (0.019) | +0.217 (0.019) | +0.231 (0.019) | +0.231 (0.019) | +0.224 (0.019) | +0.229 (0.038) | +0.241 (0.019) | +0.217 (0.019) | +0.224 (0.019) | — |
| A13 Lead-1, past data only | +0.374 (0.038) | +0.369 (0.038) | +0.379 (0.038) | +0.357 (0.057) | +0.391 (0.038) | +0.403 (0.038) | +0.373 (0.038) | +0.369 (0.038) | — | — |
| A5 Arc after-2 (lower) | −0.277 (0.019) | −0.236 (0.057) | −0.258 (0.057) | −0.262 (0.038) | −0.274 (0.019) | −0.260 (0.038) | −0.274 (0.019) | −0.236 (0.057) | −0.254 (0.038) | — |
| C1 r–swing size, detrended | +0.608 (0.019; surr. 0.0002) | +0.641 (0.019; surr. 0.0002) | +0.646 (0.019; surr. 0.0002) | +0.656 (0.019; surr. 0.0002) | +0.628 (0.019; surr. 0.0002) | +0.625 (0.019; surr. 0.0002) | +0.650 (0.019; surr. 0.0002) | +0.641 (0.019; surr. 0.0002) | +0.655 (0.019) | +0.625 (0.019; surr. 0.0002) |
| D1 Cross share of excess, GDP weights | 80.2% | 83.3% | 84.3% | 83.1% | 83.4% | 83.8% | 84.0% | 83.3% | — | 83.5% |
| D3 Same, equal weights | 96.5% | 96.8% | 97.0% | 96.9% | 96.8% | 97.3% | 96.7% | 96.8% | — | 97.0% |
| D7 Cross-term rise: correlation / swing / interaction | 33 / 53 / 14% | 44 / 41 / 15% | 46 / 40 / 14% | 41 / 45 / 14% | 45 / 42 / 14% | 45 / 41 / 14% | 44 / 42 / 14% | 44 / 41 / 15% | — | 43 / 43 / 14% |
| D11 Alignment share of swing excess (p) | 39.3% (0.103) | 18.9% (0.356) | 28.5% (0.239) | 32.6% (0.179) | 24.7% (0.276) | 28.6% (0.242) | 38.3% (0.119) | 18.9% (0.356) | — | 41.4% (0.095) |
| E1 MST decade means 1979–89 vs 2013–22 | 0.677 vs 0.379 (1.79×) | 0.680 vs 0.421 (1.62×) | 0.687 vs 0.424 (1.62×) | 0.682 vs 0.418 (1.63×) | 0.694 vs 0.414 (1.67×) | 0.685 vs 0.416 (1.65×) | 0.684 vs 0.412 (1.66×) | 0.680 vs 0.421 (1.62×) | — | — |
| E7 Phase-lead spread (lower p) | 0.445 yr (0.0002) | 0.535 yr (0.0004) | 0.546 yr (0.0002) | 0.535 yr (0.0006) | 0.542 yr (0.0004) | 0.545 yr (0.0006) | 0.474 yr (0.0002) | 0.535 yr (0.0004) | — | — |
| F1 Autocorrelation trend | +0.027 (0.456) | −0.098 (0.676) | −0.152 (0.789) | −0.205 (0.839) | −0.098 (0.684) | +0.009 (0.487) | −0.152 (0.764) | −0.098 (0.676) | — | — |
| F2 Variance trend | +0.438 (0.033) | +0.420 (0.037) | +0.438 (0.031) | +0.438 (0.033) | +0.402 (0.045) | +0.438 (0.031) | +0.420 (0.037) | +0.420 (0.037) | — | — |
| F4 Recovery-rate change | +0.078 (0.534) | +0.024 (0.507) | +0.002 (0.502) | −0.022 (0.480) | −0.017 (0.472) | +0.027 (0.498) | +0.068 (0.517) | +0.024 (0.507) | — | — |
| G1 Short-rate synchronization, lead-2 [economies] | +0.266 (0.019) [18] | +0.273 (0.019) [19] | +0.273 (0.019) [19] | +0.273 (0.019) [19] | +0.266 (0.019) [18] | +0.273 (0.019) [19] | +0.273 (0.019) [19] | +0.273 (0.019) [19] | — | — |

"— : not run. The variant without Iran and Saudi Arabia together was pre-registered for the swing-size tests only, and
the variant with Russia from 1992 for the circular-shift tests only. With Maddison's 1991–2011 growth for Norway,
Switzerland and South Africa replaced by the Global Macro Database's: on the 31, lead-2 $+0.239$ ($0.057$), lead-1
$+0.237$ ($0.019$), lag $-2$ $-0.277$ ($0.038$), C1 $+0.641$, D1 $84.2\%$, D3 $97.0\%$; on the 30, lead-2 $+0.230$
($0.038$), lead-1 $+0.224$ ($0.019$), lag $-2$ $-0.256$ ($0.075$), C1 $+0.635$, D1 $83.3\%$, D3 $96.8\%$."

**Why:** values from `results/<variant>/P/*.json` (formatted from those files; row labels are registry IDs). For the
paper, the row labels become plain names. "Without Russia" reproduces S30 in every result file (checked).

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
code version. The sample, phase convention, tests and test directions were written down and signed before any test
was run on the added economies, and extended by a dated amendment before Russia was added; every pre-registered test
is reported. The earlier results on
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
2013–22 (blue), $0.687$ against $0.424$, a factor of $1.6\times$. Panel **b**: the phase-lag spread against its
5,000-member surrogate null — the observed $0.546$ yr lies below every surrogate ($p = 2\times10^{-4}$, the floor)."
Panel **c** unchanged in wording (its values become S31's: Bonferroni 0.189, 0.094, 0.943, 1.0, 0.283, the same as
S30's).

**Why:** the figure is redrawn from the S31 results in Phase 4 (open issue 18).

---

## Outside the Methods: Results, Limitations and Discussion text (L1–L7, D1–D2)

For the paper's Results, Limitations and Discussion sections (`docs/paper_plan.md`), not for `docs/methods.md`.
Drafted from Sid's decisions of 11 October 2026 (both rounds).

### L1. Results: the pre-crisis rise (Sid's wording)

"Synchronization rises in the year before global recessions (lead-1 $+0.231$ on the 31 economies, $p = 0.019$, the
floor of the permutation test; $+0.217$ on the 30 without Russia). It does not pass a correction for testing five lags,
which with 53 circular shifts a lag cannot do on its own (§7.4); its support is that it survives phases built from past
data only ($+0.379$, $p = 0.038$) and the removal of any one of the 31 economies, and it holds under the edge-robust
convention and with Russia's phases from 1992 only. With past-only phases and China left out together it is
$p = 0.057$. It rests on 2009 and 2020: without either it is not significant (§7.3). It is a property of the tightly
coupled modern economy, not a fifty-year regularity, and not a forecast. The two-year lead (lead-2 $+0.235$,
$p = 0.038$) does not survive past-only phases and is not claimed."

### L2. Results: the channels inside the economies (Sid: the rate lead dropped as a lead claim)

"With two-sided phases, short-term interest rates are most synchronized two years before global recessions ($+0.273$,
$p = 0.019$, 19 economies with continuous rates), investment two and one years before ($+0.270$ and $+0.262$, 28
economies) and real GDP one year before ($+0.254$, $p = 0.019$, 30 economies). We report this ordering as a
description only. With phases from past data only neither two-year rise survives (short rates $+0.165$, $p = 0.15$;
investment $-0.110$, $p = 0.72$), so we make no claim that rates or investment signal recessions in advance. On these
real GDP series (the Global Macro Database, not Maddison), the past-only lead-1 is $+0.319$ ($p = 0.038$; $+0.311$,
$p = 0.057$ without Russia). Russia enters only the real GDP channel: its other series start after 1965."

### L3. Limitations: the fall after recessions (Sid: moved to Limitations)

"Synchronization falls in the two years after a global recession (lag $-2$: $-0.258$ on the 31 economies,
$p = 0.057$; $-0.236$, $p = 0.057$ on the 30; $-0.277$, $p = 0.019$ on the original 26), but this half of the arc does
not hold up. It is not significant on the 31 or the 30; it disappears with the 3–10 year band and with growth rates
(§7.1–7.2); it is significant under none of the alternative phase conventions, including phases from past data only
(§7.2); and without 2020 it is $-0.18$ ($p = 0.15$). On the 31 it sits on the threshold: leaving out any of 20 of the
31 economies, or computing Russia's phases from 1992, takes it to $p = 0.019$–$0.038$. It also sits where the filters
are least reliable: the lag $-2$ test for 2020 uses $r(2022)$, the last observation. We report it and do not claim it."

### L4. Limitations: what multiplicity correction can show (Sid)

"No lag survives a correction for testing five lags. With 53 circular shifts the smallest $p$ the test can return is
$0.019$, so a single lag can never pass Bonferroni and passes Benjamini–Hochberg only alongside another lag at the
floor, which happened on the original 26 but not on the 30 or the 31. The pre-crisis rise therefore rests on its
survival under past-only phases and leave-one-economy-out, not on corrected significance, and on two events, 2009 and
2020."

### L5. Results: loss of diversification (Sid: the Results term)

"In global recessions the world economy loses diversification: the economies' cycles stop offsetting one another. The
co-movement (cross) term supplies $84.3\%$ of the extra world variance in recession windows GDP-weighted ($97.0\%$
equal-weighted; on the 30, $83.3\%$ and $96.8\%$), a descriptive magnitude (§7.6). Co-movement and larger swings
contribute about equally to that rise ($46\%$ and $40\%$ GDP-weighted, interaction $14\%$; on the 30, $44\%$ and
$41\%$; on the original 26, $33\%$ and $53\%$)."

### L6. Results: the alignment share is sample-sensitive (Sid: Results builds nothing on it)

"Splitting the recession excess in world swing (the identity $|Z| = \bar A R_A$) into alignment and swing size gives
an alignment share of $28\%$ on the 31, $19\%$ on the 30, $33\%$ on the 30 without Iran and $39\%$ on the original
26. The swing-size part is significant on every sample ($p = 0.0002$, the floor); the alignment part on none
($p = 0.10$–$0.36$). The share depends on which economies are in the sample, and we draw no conclusion from it."

### L7. Results: the variance of synchronization (Sid: consistent with loss of diversification)

"Before recessions the variance of synchronization rises ($\tau = +0.438$, $p = 0.031$; on the 30, $+0.420$,
$p = 0.037$) while its lag-1 autocorrelation does not ($-0.152$, $p = 0.79$). That is not the slowing-down signature,
which needs both; it is consistent with loss of diversification — shocks stop cancelling, so synchronization swings
more widely without recovering more slowly. It rests on 2009 and 2020 (before them alone $+0.857$, $p = 0.003$; before
1982 and 1991, $+0.018$, $p = 0.51$)."

The other Limitations items in `docs/paper_plan.md` (five events; annual data; the end of the sample is edge-affected)
stand; L4 and the variance rise's dependence on 2009 and 2020 join the item on the lead.

### D1. Discussion: what the transition is, and what it is not (Sid's framing)

"We first asked whether global recessions arrive the way a system approaches a bifurcation, with recovery slowing as a
threshold nears. They do not: before recessions the autocorrelation of synchronization does not rise, and after them
the recovery rate does not fall (§6.7). That 'what it isn't' led to the mechanism the paper proposes: loss of
diversification. In recessions the economies' cycles stop offsetting one another, and co-movement supplies most of the
extra world variance. Because co-movement and larger swings contribute about equally, we read the recession excess as
amplification transmitted by alignment: shocks that would have cancelled across economies are passed along instead.
The rise in the variance of synchronization before recessions, without a rise in its autocorrelation, fits the same
reading — when shocks stop cancelling, synchronization swings more widely without recovering more slowly — though it
rests on 2009 and 2020 and is a reading of the data, not a separate test."

### D2. Discussion: diversification-type tipping (Sid: our own term)

"We call a transition of this kind diversification-type tipping: a transition caused by losing the cancellation
between economies rather than by slowing recovery. It differs from bifurcation-induced tipping (B-tipping in the
taxonomy of Ashwin et al. 2012), which shows the slowing-down signature we do not find. This paper does not show that
loss of diversification has a threshold — a level of coupling beyond which cancellation fails abruptly rather than
gradually. Testing for one is future work, in the simulator of coupled economies planned for the graph-neural-network
study, where the coupling is known and can be raised step by step."

**Notes for Sid.** A quick search found no earlier use of the phrase "diversification-type tipping"; check again before
submission. In finance, "diversification" and systemic risk usually describe a different mechanism: institutions that
each diversify their portfolios become alike and more connected, so diversification itself spreads distress (for
example Burkholz, Garas and Schweitzer, arXiv 1503.00925, on damage diversification). One sentence in the Discussion
should set our sense — cycles that stop offsetting one another — apart from that one. D2 says nothing about noise- or
rate-induced tipping; `docs/paper_plan.md` still lists rate-induced tipping ("the rocket") as a Paper 2 hypothesis.
