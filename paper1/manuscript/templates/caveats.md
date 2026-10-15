<!-- CAVEATS_FOR_SID.md: rendered and traced like the manuscript (every number from a results file). -->
# Caveats for Sid — Paper 1, complete draft of 15 October 2026

For each of the five claims: its weakest point, the question a referee will ask, and our honest answer. Then what
else you should know before you send the paper anywhere. Every number here comes from the same results files as the
paper (`numbers.csv`).

## Claim 1 — Synchronization and swing size move together ({{S31/P/amplitude#corr_detrended|c3}})

**Weakest point.** It may be a common cause rather than a link: a large shock that hits every economy at once both
lines up their phases and makes their swings bigger, so the correlation can come from the shocks themselves, not
from anything synchronization does. The size also depends on where the Hilbert transform is applied
({{S31/P/conventions#N/amp_detrended/0|c3}} to {{S31/P/conventions#C/amp_detrended/0|c3}} across conventions), and in
uncoupled simulated worlds the circular-shift version of this test rejects slightly too often
({{@g1_lo:null,A,amplitude.p_shift|pct1}}–{{@g1_hi:null,A,amplitude.p_shift|pct1}} against 3.8%).

**Referee:** "Isn't this mechanical? Big common shocks do both. And is it just 2009 and 2020?"

**Honest answer.** The paper claims co-movement, not causation, and says the test uses no recession dates. The
surrogate test (p = {{S31/P/amplitude#p_surrogate|p}}, the floor) rules out independent economies with the same
spectra, not a common shock. We never computed the correlation without 2009 and 2020; with Paper 1 locked that check
belongs to Paper 2. Say so if asked.

## Claim 2 — Recession excess variance is mostly co-movement ({{S31/P/diversification#gdp_mean/cross_fraction_of_excess|pct1}}; correlation {{S31/P/cross_split#gdp_mean/from_correlation|pct0}}, swing size {{S31/P/cross_split#gdp_mean/from_swing_size|pct0}})

**Weakest point.** Most of it is arithmetic. With 465 pairs against 31 variances the cross term dominates world
variance in any period; what is specific to recessions is the gap in the cross share
({{S31/P/diversification#gdp_mean/cross_share_crisis|f3}} against {{S31/P/diversification#gdp_mean/cross_share_normal|f3}}),
which has no proper null. In simulated trade-coupled worlds the cross-term test rejects in
{{@g1_lo:network,A,diversification.gdp_mean|pct1}}–{{@g1_hi:network,A,diversification.gdp_mean|pct1}} of worlds with
recession dates that have nothing to do with them. A "recession window" is the 10 years ending in a recession year, so
it is mostly not recession. $N_{\mathrm{eff}}$ is a transform of $r$ ($1/E[r^2]$) and adds no information beyond
$r$; its dip is carried by 2009 and 2020. The near-agreement of the variance law with the decomposition
({{dtt/results/d3_neff.json#S31/decomposition/gdp_mean/excess_from_cross_law|pct1}} against
{{dtt/results/d3_neff.json#S31/decomposition/gdp_mean/excess_from_cross|pct1}}) is partly built in: year by year they
are the same identity with equal swings.

**Referee:** "Isn't this just the algebra of correlated sums? What would you get for five random years?"

**Honest answer.** Yes, and the paper says so (Box 1: "arithmetic, not a mechanism"). We have no proper null for the
gap and report it as descriptive. "Amplification transmitted by alignment" is an interpretation; on 11 October you had
kept it for the Discussion only, and your list of 15 October puts it in the Results, which the draft follows (decision
log). The split depends on the sample: on the original 26 swing size supplied
{{S26/P/cross_split#gdp_mean/from_swing_size|pct0}} against {{S26/P/cross_split#gdp_mean/from_correlation|pct0}}.

## Claim 3 — The network tightened about {{@mst_ratio:S31|x1}}

**Weakest point.** It compares two decade means of a rolling statistic. The 2013–22 mean includes the windows that
contain 2020, where the tree length drops sharply ({{S31/P/mst#L_by_year/2019|f3}} in 2019,
{{S31/P/mst#L_by_year/2020|f3}} in 2020). The factor is {{@mst_ratio:S26|x1}} on the original 26 and {{@mst_ratio:S30|x1}} on
the 30, so it depends on the sample.

**Referee:** "Is the tightening just 2020 inside the last decade's windows?"

**Honest answer.** No, most of it comes earlier: the length is already {{S31/P/mst#L_by_year/2012|f3}} in 2012, against
{{S31/P/mst#L_decade_means/1979-1989|f3}} on average in 1979–89. But it is a description of a trend, with no test, and
the network does not contract before recessions ($p =$ {{S31/P/mst#p_contraction|p}}).

## Claim 4 — Synchronization rises in the year before recessions (past-only {{S31/P/conventions#C/arc/lead1/corr|c3}}, $p =$ {{S31/P/conventions#C/arc/lead1/p|p}}, $n \approx 2$)

**Weakest point.** Everything about it is thin. It rests on 2009 and 2020; $p =$ {{S31/P/conventions#C/arc/lead1/p|p}}
is the second-smallest value 53 shifts allow; without China it is {{S31_minus_CHN/P/conventions#C/arc/lead1/p|p}}; two
past-only leads were pre-registered, and doubling the p for them gives
{{@mul:2;S31/P/conventions#C/arc/lead1/p|p}}; the two-sided version is inflated by how recessions are dated (L8);
convention N loses it ($p =$ {{S31/P/conventions#N/arc/lead1/p|p}}); and in G1b a lead the size of the real one
appears in only {{@g1b_verdict:network,primary,share_at_real_p|pct1}} of worlds. The past-only correlation
({{S31/P/conventions#C/arc/lead1/corr|c3}}) is larger than the two-sided one ({{S31/P/arc#arc/lead1/corr|c3}}), and
under past-only phases the crisis year is also at the floor ({{S31/P/conventions#C/arc/crisis/corr|c3}}): a phase
estimated at the very end of its series behaves differently, and a referee may suspect the past-only convention itself.

**Referee:** "Two events, p = 0.038 from 53 shifts, two past-only tests: why is this more than chance?"

**Honest answer.** It may not be. The paper calls it a two-event observation, not a regularity or a forecast. What it
has is consistency: the same sign under every convention, under every single-economy leave-out and on all three
samples. If pressed on the past-only convention's end-point behaviour, the honest reply is that the crisis-year result
under it is not interpreted for exactly that reason, and that the lead-1 result does not depend on it alone (the
two-sided lead is at the floor and survives surrogates with ends at $p =$
{{results/edge_matched/S31.json#tests/arc.P.lead1/p_edge|p}}).

## Claim 5 — No critical slowing down (variance {{S31/P/csd#tau_var|c3}}, $p =$ {{S31/P/csd#p_var|p}}; autocorrelation {{S31/P/csd#tau_ar1|c3}}, $p =$ {{S31/P/csd#p_ar1|p}})

**Weakest point.** It is an absence of evidence from four pre-recession windows of eight annual points each, and we
never measured the tests' power. The variance rise rests on 2009 and 2020, is significant under P and E but not W or N,
and may partly be the secular rise in the volatility of $r$ since the 2000s (Figure 6 shows variance climbing almost
steadily from the mid-2000s), which the spectrum-preserving surrogates do not reproduce. "Consistent with
noise-induced tipping" is an interpretation: many processes with no tipping at all also show no slowing down.

**Referee:** "What power did these tests have to detect slowing down?"

**Honest answer.** We do not know: the simulations checked that the tests have the right size
({{@g1_rate:kuramoto,null,A,csd.p_ar1|pct1}} and {{@g1_rate:stuart_landau,null,A,csd.p_ar1|pct1}} for the
autocorrelation test) but not their power, because no simulated world was built to approach a bifurcation. The paper
labels the reading as interpretation and says the nulls are weak evidence.

## The mechanism check (G1b)

The verdict is **{{@g1b_verdict:network,primary,verdict|raw}}**, exactly as pre-registered: the past-only lead-1
rejects in {{@g1b_verdict:network,primary,rate|pct1}} of trade-coupled worlds, above chance and above both controls,
but criterion (c) fails ({{@g1b_verdict:network,primary,share_at_real_p|pct1}} against 20%). With 53 shifts, p ≤ 0.05
and p ≤ 0.038 are the same event, so (c) asked that the rejection rate itself reach 20% — a high bar that was set
before the run. One sensitivity (noise from $\bar A R_A$) first failed to calibrate because of a units problem; it was
rerun with a rescaled bracket before anything was reported (decision log). The paper claims no mechanism from G1b.

## Other things to know

- **The 2020 recession date.** Kose, Sugawara and Terrones (2020) list four global recessions (1975, 1982, 1991, 2009);
  the paper dates 2020 from the World Bank (2020) under the same definition. I could not read the World Bank's box that
  makes that classification; the reference is marked partly unverified.
- **References.** All were checked online (`REFERENCES_CHECK.md`); unverified details are marked: the journal version
  of Burkholz, Garas and Schweitzer, the World Bank box, and the content of Lucas (1977), which I verified only
  through the papers that cite it.
- **Your two late changes of wording** (claim 2's phrase in the Results; claim 5 read as noise-induced tipping) replace
  decisions of 11 October; both are logged.
- **The Methods are now generated.** `docs/methods.md` is written by the build from the templates, so edit
  `paper1/manuscript/templates/02_data.md` and `03_methods.md`, not the file. It stays read-only on disk.
- **Two errors in the fifth draft were corrected** while generating it, and a third inconsistency (the 2020 dating
  source) between the Methods and the Limitations; see `CHECKS.md`.
- **The number trace is automatic, with limits.** Placeholders cover every result; the remaining digits are classified
  by rule (years as dates, settings from the config files, small counts). Read `TRACE.md` to see each one.
- **Figures** use DejaVu Sans, because Inter is not installed; redraw them after installing Inter. `docs/FIGURES.md`
  and the figure books are not rebuilt (that needs poppler and LaTeX). The supplementary figures other than F4.5 and
  F5.4 still show the 26 economies or convention W.
- **The PDF is not built**: LaTeX, pandoc, poppler and Inter are missing (`BUILD_PDF.md`).
- **The title is a draft**, and so is every sentence: you are the author.
