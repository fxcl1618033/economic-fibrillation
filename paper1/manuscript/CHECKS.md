# Checks on the complete draft — 15 October 2026

## 1. Every number traces to a results file

The manuscript is rendered from templates by `python -m ef.manuscript.build text`. Every result in the text is a
placeholder naming its results file and key; `numbers.csv` lists each one with its value, how it is printed and its
source, and `TRACE.md` classifies every other digit in the text (settings from the config files, years, section and
table numbers, citation details). The trace finds no number that is neither a placeholder nor a classified setting.
`tests/test_manuscript.py` checks this on every test run, and that the committed text equals a fresh render.

Limits of the check: the classification of literal digits is by rule, so a hand-typed year or a single digit would be
classified as a date or a count rather than flagged. Results that are years (for example the year of the lowest $r$,
1985) are placeholders. Words such as "five" or "two" are not checked.

## 2. Methods against Results

Because the Methods and the Results draw on the same results files through the same placeholders, a number cannot
disagree between them. The checks below are about wording, made by reading both against each other.

**Found and corrected in the Methods (they came from the fifth draft of the edits):**

- §5.4 said that among the p-values crossing 0.05 under surrogates with ends "the largest change" was the lag $-2$ arc
  (0.057 → 0.039).
  It is not: the real-GDP channel's crisis year moves from 0.094
  to 0.046 and convention W's lead-1 from
  0.019 to 0.056.
  It now reads "the one that matters for the text".
- §7.2 said lead-1 "is the one result of §6.3 that survives phases built from past data only". Under past-only phases
  the crisis year also reaches the floor (+0.417, $p =$
  0.019). It now says that lead-1 is the one *lead* that survives, reports the crisis
  year and says why it is not interpreted; the Results say the same.
- §4 cited Kose, Sugawara and Terrones (2020) for all five recession dates, while that paper lists four; the
  Limitations already gave the World Bank (2020) for 2020. §4 and the Introduction now cite both.

**Differences of emphasis, left as they are and flagged for you:**

- The Methods (§6.7, edit A4, which you approved on 11 October) read the variance rise as what loss of diversification
  would produce; the Results (claim 5, your list of 15 October) read it as consistent with noise-induced tipping. Box 1
  and §5.1 join the two: noise-induced tipping is larger disturbances with unchanged restoring forces, which is what
  shocks that stop cancelling would give. If you want one wording throughout, change §6.7.
- The Methods (§6.1) say "co-movement and larger swings contribute about equally"; the Results add "amplification
  transmitted by alignment" as your 15 October list asks. They do not contradict each other.

**Checked and consistent:** the five claims and their numbers in the Abstract, Introduction, Results, Discussion and
Limitations; the lead stated past-only first with $n \approx 2$ in the same sentence, China-out
0.057, and the two-sided value with both nulls
(0.019 and 0.033); the G1b verdict
(partly) everywhere it appears; the floors quoted with every circular-shift and
surrogate p in the main text; the main text has six figures, each with its catalogue ID.

## 3. What could not be done

- The PDF (`BUILD_PDF.md`): LaTeX, pandoc, poppler and Inter are not installed.
- `docs/FIGURES.md` and the figure books: their builder needs poppler and LaTeX; the redrawn figures are listed in
  `tools/figure_catalog.py` (`REDRAWN_S31`) and in Appendix "Supplementary figures".
