## 5 Discussion

### 5.1 What the transition is, and what it is not

We first asked whether global recessions arrive the way a system approaches a bifurcation, with recovery slowing as a
threshold nears. They do not: before recessions the autocorrelation of synchronization does not rise, and after them
the recovery rate does not fall (§4.5). That "what it isn't" led to the account the paper proposes: loss of
diversification. In recessions the economies' cycles stop offsetting one another, and co-movement supplies most of the
extra world variance (§4.2). Because co-movement and larger swings contribute about equally, we read the recession
excess as amplification transmitted by alignment: shocks that would have cancelled across economies are passed along
instead. The rise in the variance of synchronization before recessions, without a rise in its autocorrelation, fits
the same reading — when shocks stop cancelling, synchronization swings more widely without recovering more slowly —
and in the taxonomy of Ashwin et al. (2012) it is what noise-induced rather than bifurcation-induced tipping would
show. This is a reading of the data, not a separate test, and it rests on 2009 and 2020.

### 5.2 Box 1: loss of diversification as arithmetic

> **Box 1 | Why aligned cycles stop diversifying**
>
> Let economy $i$'s cycle have phase $\theta_i$ and swing size $A_i$, and let a shock reach every economy according to
> where it is in its cycle: economy $i$ responds with $q_i = \sigma A_i\, u\cdot v_i$, where $v_i = (\cos\theta_i,
> \sin\theta_i)$ and $u$ is a unit direction drawn at random. The same disturbance pushes an economy near its peak down
> and one near its trough up, so economies at opposite points of their cycles cancel in the world average. If only a
> share $\rho$ of the shock is common and the rest is independent across economies (each with variance
> $\sigma^2A_i^2/2$), the variance of the world-average response $\bar q$, given the phases, is
> $$ \mathrm{Var}(\bar q) = \frac{\sigma^2}{2}\Big[\rho\,|Z_A|^2 + (1-\rho)\,\frac{\overline{A^2}}{N}\Big], \qquad Z_A = \frac{1}{N}\sum_i A_i e^{\mathrm{i}\theta_i}. $$
> The first term is the common shock, the second the independent part. Because $|Z_A| = \bar A\, R_A$, with
> $R_A = |\sum_i A_i e^{\mathrm{i}\theta_i}| / \sum_i A_i$ the alignment weighted by swing size, the common term is
> the square of an exact identity: world swing equals mean swing size times alignment. With equal swing sizes and a
> fully common shock, $\mathrm{Var}(\bar q) = \sigma^2 r^2/2$, against $\sigma^2/(2N)$ if the responses were
> independent. The world then varies like
> $$ N_{\mathrm{eff}} = 1/r^2 $$
> independent economies: the number that would give the same world variance if they did not move together. With a
> common share $\rho$, $N_{\mathrm{eff}} = 1/(\rho r^2 + (1-\rho)/N)$. Alignment matters only for the common part of
> shocks. The independent part is the averaging-out of Lucas (1977), which fails when a few units are large (Gabaix
> 2011) or central in the input–output network (Acemoglu et al. 2012); here it fails for a third reason: the
> economies' cycles line up.
>
> On the 31 economies $N_{\mathrm{eff}} = 1/E[r^2]$ is about 3.5 over
> 1970–2022, 2.4 in recession years and
> 2.1 the year before
> (1.1 in 2020); 2009 and 2020 pull these down, and the earlier
> recessions are not low. Averaged over the 10-year windows of §4.2, the law gives the cross term
> 84.1% of the extra world variance in
> recession windows, against 84.3% measured.
>
> **It is arithmetic, not a mechanism.** Any year in which cycles happen to line up has a larger world swing, coupled
> or not, and recessions dated from world output are such years even in simulated worlds with no coupling (§5.4).
>
> *Interpretation, not a test:* in the taxonomy of Ashwin et al. (2012), a transition caused by larger disturbances
> while the restoring forces stay the same is noise-induced tipping, which does not show critical slowing down — and the
> autocorrelation of synchronization does not rise before recessions, nor does recovery slow after them (§4.5).

The law is exact for the stated shock, which we check against simulation (the code is in the repository); its link to
the decomposition is exact year by year (with equal weights and swing sizes, the cross share is $1 - N_{\mathrm{eff}}/N$)
and close, not exact, over the decomposition's windows. With GDP weights the independent term becomes
$(1-\rho)\sum_i w_i^2A_i^2/2$, a Herfindahl-type concentration — Gabaix's granular channel — and the common term
$\rho\,|\sum_i w_iA_ie^{\mathrm{i}\theta_i}|^2/2$ is the alignment channel. The two are complements, not rivals.

### 5.3 Diversification-type tipping

We call a transition of this kind diversification-type tipping: a transition caused by losing the cancellation between
economies rather than by slowing recovery. It differs from bifurcation-induced tipping, which shows the slowing-down
signature we do not find. In finance, "diversification" and systemic risk usually describe a different mechanism —
institutions that each diversify become alike and more connected, so diversification itself can spread distress
(Burkholz, Garas and Schweitzer 2016) — and our sense is narrower: cycles that stop offsetting one another. This paper
does not show that loss of diversification has a threshold, a level of coupling beyond which cancellation fails
abruptly rather than gradually.

### 5.4 The mechanism check: simulated worlds with known coupling

Two simulation studies, each pre-registered before it was run, ask what the tests can and cannot show.

**G1: worlds with known coupling.** We simulated 31 economies as phase oscillators (Kuramoto) and as phase-and-size
oscillators (Stuart–Landau) on the real trade network, calibrated to the real cycles, and ran every test of this paper
on 1,000 worlds per setting. With no coupling the tests reject at about their stated rates (Table 1, §3.4.3). Two
findings bear on the claims. First, when recessions are dated from each simulated world's own output, as global
recessions are, the two-sided crisis-year and lead-1 arcs reject in 8.2%–8.9%
and 8.5%–8.6% of uncoupled worlds, about twice the correct
rate, while the past-only lead-1 does not (2.3%–2.9%): this is
why the lead claim rests on the past-only version. Second, no G1 world produced the past-only lead: with own-dated
recessions it rejected in 1.7% of trade-coupled,
2.9% of uncoupled and 2.5% of
commonly forced Kuramoto worlds, never above chance.

**G1b: a synchrony-driven escape layer.** We then added the mechanism Box 1 suggests to the same Kuramoto worlds: a
recession is an escape of a world-level state from a stable well, $dx = (\mu + x - x^3)\,dt + \sigma\,r(t)\,dW$, so that
shocks grow with the worlds' true synchrony. $\sigma$ was set so that worlds have five recession years in 53 on
average, using only their number, never their timing; each escape resets the state and starts a two-year refractory
period. Before running we fixed what "reproduces the lead" means: (a) the past-only lead-1 rejects more often than
chance (the lower bound of its 95% interval above 3.8%); (b) more often than the same layer with constant noise and
with synchrony shuffled in time (both paired differences' intervals above zero); and (c) at least 20% of worlds reach
the real $p =$ 0.038. Some lead is expected by construction, since the layer makes
recessions likelier when synchrony is high; the question is how much survives annual sampling, 53 points, five events
and past-only phases.

The verdict, exactly as pre-registered, is **partly** (Appendix Table A11). In
trade-coupled worlds the past-only lead-1 rejects in 6.3% of worlds (95%
interval 5.0%–8.0%), above chance (a) and above
both controls (b: 3.5 percentage points more than with constant noise,
3.4 percentage points more than with shuffled synchrony). But only
6.3% of worlds reach the real $p$, against the 20% required (c fails),
and 1.3% reach the real correlation of
+0.379. Without trade coupling the layer leaves no past-only lead
(4.0% with no coupling, 3.2% with common
forcing only). Of eight pre-registered sensitivities on the trade-coupled worlds, 6 give the
same verdict and 2 do not reproduce the lead (one state per economy; refractory 4 years); none
reaches (c).

What this says, and no more: a synchrony-driven escape mechanism on coupled economies can leave a past-only lead that
our pipeline detects, and coupling is needed for it, but a lead as large as the real one is rare under it. Either the
real lead is an unusual draw — which, resting on two events, it may well be — or the real mechanism is stronger than,
or different from, the one simulated; the simulated recessions, for instance, do not feed back on the cycles they are
measured from. We claim no mechanism from this check.

### 5.5 Where this sits

The world business-cycle factor of Kose, Otrok and Whiteman (2003) measures how much economies move together; we ask
when they do, and whether togetherness itself is the danger. Treating national cycles as coupled oscillators follows
Selover and Jensen (1999), who described mode-locking of business cycles, and Ikeda, Aoyama and Yoshikawa (2013), who
fitted Kuramoto-type couplings between six economies' quarterly cycles; Pangallo (2025) shows that trade can
synchronize endogenous cycles across 24 countries. Morikawa, Morikawa and Nakamichi (2026) use the same Hilbert and
Kuramoto toolkit for a different question, the 1/f spectra of economic series. None of these relates synchronization to
the timing of global recessions or to the loss of diversification. We do not forecast: two-sided filters cannot support
a forecast, and the past-only lead rests on two events.
