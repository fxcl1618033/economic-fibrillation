# Caveats for Sid — Paper 1, complete draft of 15 October 2026

For each of the five claims: its weakest point, the question a referee will ask, and our honest answer. Then what
else you should know before you send the paper anywhere. Every number here comes from the same results files as the
paper (`numbers.csv`).

## Claim 1 — Synchronization and swing size move together (+0.646)

**Weakest point.** It may be a common cause rather than a link: a large shock that hits every economy at once both
lines up their phases and makes their swings bigger, so the correlation can come from the shocks themselves, not
from anything synchronization does. The size also depends on where the Hilbert transform is applied
(+0.547 to +0.726 across conventions), and in
uncoupled simulated worlds the circular-shift version of this test rejects slightly too often
(5.7%–6.2% against 3.8%).

**Referee:** "Isn't this mechanical? Big common shocks do both. And is it just 2009 and 2020?"

**Honest answer.** The paper claims co-movement, not causation, and says the test uses no recession dates. The
surrogate test (p = 0.0002, the floor) rules out independent economies with the same
spectra, not a common shock. We never computed the correlation without 2009 and 2020; with Paper 1 locked that check
belongs to Paper 2. Say so if asked.

## Claim 2 — Recession excess variance is mostly co-movement (84.3%; correlation 46%, swing size 40%)

**Weakest point.** Most of it is arithmetic. With 465 pairs against 31 variances the cross term dominates world
variance in any period; what is specific to recessions is the gap in the cross share
(0.706 against 0.620),
which has no proper null. In simulated trade-coupled worlds the cross-term test rejects in
97.1%–99.3% of worlds with
recession dates that have nothing to do with them. A "recession window" is the 10 years ending in a recession year, so
it is mostly not recession. $N_{\mathrm{eff}}$ is a transform of $r$ ($1/E[r^2]$) and adds no information beyond
$r$; its dip is carried by 2009 and 2020. The near-agreement of the variance law with the decomposition
(84.1% against
84.3%) is partly built in: year by year they
are the same identity with equal swings.

**Referee:** "Isn't this just the algebra of correlated sums? What would you get for five random years?"

**Honest answer.** Yes, and the paper says so (Box 1: "arithmetic, not a mechanism"). We have no proper null for the
gap and report it as descriptive. "Amplification transmitted by alignment" is an interpretation; on 11 October you had
kept it for the Discussion only, and your list of 15 October puts it in the Results, which the draft follows (decision
log). The split depends on the sample: on the original 26 swing size supplied
53% against 33%.

## Claim 3 — The network tightened about 1.6×

**Weakest point.** It compares two decade means of a rolling statistic. The 2013–22 mean includes the windows that
contain 2020, where the tree length drops sharply (0.539 in 2019,
0.329 in 2020). The factor is 1.8× on the original 26 and 1.6× on
the 30, so it depends on the sample.

**Referee:** "Is the tightening just 2020 inside the last decade's windows?"

**Honest answer.** No, most of it comes earlier: the length is already 0.438 in 2012, against
0.687 on average in 1979–89. But it is a description of a trend, with no test, and
the network does not contract before recessions ($p =$ 0.206).

## Claim 4 — Synchronization rises in the year before recessions (past-only +0.379, $p =$ 0.038, $n \approx 2$)

**Weakest point.** Everything about it is thin. It rests on 2009 and 2020; $p =$ 0.038
is the second-smallest value 53 shifts allow; without China it is 0.057; two
past-only leads were pre-registered, and doubling the p for them gives
0.075; the two-sided version is inflated by how recessions are dated (L8);
convention N loses it ($p =$ 0.057); and in G1b a lead the size of the real one
appears in only 6.3% of worlds. The past-only correlation
(+0.379) is larger than the two-sided one (+0.231), and
under past-only phases the crisis year is also at the floor (+0.417): a phase
estimated at the very end of its series behaves differently, and a referee may suspect the past-only convention itself.

**Referee:** "Two events, p = 0.038 from 53 shifts, two past-only tests: why is this more than chance?"

**Honest answer.** It may not be. The paper calls it a two-event observation, not a regularity or a forecast. What it
has is consistency: the same sign under every convention, under every single-economy leave-out and on all three
samples. If pressed on the past-only convention's end-point behaviour, the honest reply is that the crisis-year result
under it is not interpreted for exactly that reason, and that the lead-1 result does not depend on it alone (the
two-sided lead is at the floor and survives surrogates with ends at $p =$
0.033).

## Claim 5 — No critical slowing down (variance +0.438, $p =$ 0.031; autocorrelation −0.152, $p =$ 0.789)

**Weakest point.** It is an absence of evidence from four pre-recession windows of eight annual points each, and we
never measured the tests' power. The variance rise rests on 2009 and 2020, is significant under P and E but not W or N,
and may partly be the secular rise in the volatility of $r$ since the 2000s (Figure 6 shows variance climbing almost
steadily from the mid-2000s), which the spectrum-preserving surrogates do not reproduce. "Consistent with
noise-induced tipping" is an interpretation: many processes with no tipping at all also show no slowing down.

**Referee:** "What power did these tests have to detect slowing down?"

**Honest answer.** We do not know: the simulations checked that the tests have the right size
(5.1% and 4.2% for the
autocorrelation test) but not their power, because no simulated world was built to approach a bifurcation. The paper
labels the reading as interpretation and says the nulls are weak evidence.

## The mechanism check (G1b)

The verdict is **partly**, exactly as pre-registered: the past-only lead-1
rejects in 6.3% of trade-coupled worlds, above chance and above both controls,
but criterion (c) fails (6.3% against 20%). With 53 shifts, p ≤ 0.05
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
- **Figures** were redesigned for print (vector PDF, journal style). F5.1's second panel is now the distribution of the
  465 pairwise correlations in the two decades instead of the tree itself, which was unreadable at that size.
  `docs/FIGURES.md` and the figure books are not rebuilt yet; the supplementary figures other than F4.5 and F5.4 still
  show the 26 economies or convention W.
- **The editable version** is `latex/paper1.tex` (with `latex/figures/`); `paper1.pdf` is compiled from it. If you
  edit the `.tex` directly, the numbers are no longer regenerated from the results files: either edit the templates and
  rebuild, or treat your edited `.tex` as the master from then on.
- **The title is a draft**, and so is every sentence: you are the author.
