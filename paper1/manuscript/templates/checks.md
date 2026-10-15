<!-- CHECKS.md: the checks run on the complete draft before handing it over (Part D of Sid's instructions of 15 October 2026). -->
# Checks on the complete draft — 15 October 2026

## 1. Every number traces to a results file

The manuscript is rendered from templates by `python -m ef.manuscript.build text`. Every result in the text is a
placeholder naming its results file and key; `numbers.csv` lists each one with its value, how it is printed and its
source, and `TRACE.md` classifies every other digit in the text (settings from the config files, years, section and
table numbers, citation details). The trace finds no number that is neither a placeholder nor a classified setting.
`tests/test_manuscript.py` checks this on every test run, and that the committed text equals a fresh render.

Limits of the check: the classification of literal digits is by rule, so a hand-typed year or a single digit would be
classified as a date or a count rather than flagged. Results that are years (for example the year of the lowest $r$,
{{@argmin_r:S31,min|yr}}) are placeholders. Words such as "five" or "two" are not checked.

## 2. Methods against Results

Because the Methods and the Results draw on the same results files through the same placeholders, a number cannot
disagree between them. The checks below are about wording, made by reading both against each other.

**Found and corrected in the Methods (they came from the fifth draft of the edits):**

- §5.4 said that among the p-values crossing 0.05 under surrogates with ends "the largest change" was the lag $-2$ arc
  ({{results/edge_matched/S31.json#tests/arc.P.after2/p_current|p}} → {{results/edge_matched/S31.json#tests/arc.P.after2/p_edge|p}}).
  It is not: the real-GDP channel's crisis year moves from {{results/edge_matched/S31.json#tests/G3.same/p_current|p}}
  to {{results/edge_matched/S31.json#tests/G3.same/p_edge|p}} and convention W's lead-1 from
  {{results/edge_matched/S31.json#tests/arc.W.lead1/p_current|p}} to {{results/edge_matched/S31.json#tests/arc.W.lead1/p_edge|p}}.
  It now reads "the one that matters for the text".
- §7.2 said lead-1 "is the one result of §6.3 that survives phases built from past data only". Under past-only phases
  the crisis year also reaches the floor ({{S31/P/conventions#C/arc/crisis/corr|c3}}, $p =$
  {{S31/P/conventions#C/arc/crisis/p|p}}). It now says that lead-1 is the one *lead* that survives, reports the crisis
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
{{S31_minus_CHN/P/conventions#C/arc/lead1/p|p}}, and the two-sided value with both nulls
({{S31/P/arc#arc/lead1/p|p}} and {{results/edge_matched/S31.json#tests/arc.P.lead1/p_edge|p}}); the G1b verdict
({{@g1b_verdict:network,primary,verdict|raw}}) everywhere it appears; the floors quoted with every circular-shift and
surrogate p in the main text; the main text has six figures, each with its catalogue ID.

## 3. The PDF

`paper1.pdf` is built by `make paper1-pdf` (pandoc and xelatex; TeX Gyre Pagella, Inter, Latin Modern Math, loaded by
file name in `header.tex` because XeTeX on macOS finds TeX Live's own fonts only that way). The LaTeX log has no
missing characters; ten lines are slightly too wide, all in the wide appendix tables. The figures are drawn in Inter.
`docs/FIGURES.md` and the figure books are not rebuilt: the redrawn figures are listed in `tools/figure_catalog.py`
(`REDRAWN_S31`) but not yet merged into its entries.
