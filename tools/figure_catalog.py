"""
Catalogue of every Economic Fibrillation figure made up to 11 October 2026.

One entry per figure: where it lives, what it shows, the numbers printed on it, the script and data
behind it, and a status. tools/build_figure_docs.py turns this into the category folders,
docs/FIGURES.md and the compiled PDFs in figures/compiled/.

Status values
  current      paper data (Maddison 2023) and the paper's conventions; numbers match docs/methods.md
  relabel      numbers are right but an annotation on the figure is out of date (see note)
  convW        computed with the windowed-Hilbert convention W (Hilbert applied to 1970-2022 only);
               the paper uses convention P (Hilbert on 1950-2022). See docs/open_issues.md, issue 1
  superseded   earlier data (World Bank current dollars) or an earlier crisis definition; kept as history
  descriptive  atlas material (Global Macro Database); describes, does not test
  unverified   the series drawn matches no stored results file; redraw before use
"""

FIGSRC = "figures/_sources/analysis"                  # original files as saved (vector PDFs where drawn as vectors)
COMP = "figures/_sources/companion"                    # images extracted from the companion book, in book order
ATL_IMG = "figures/_sources/figure_atlas_july"          # recovered from the July Figure Atlas PDF
ATLAS_FIG = "atlas/fig"

STATUS = {
    "current":     ("Current", "2A78D6"),
    "relabel":     ("Needs relabelling", "C98A00"),
    "convW":       ("Convention W", "EB6834"),
    "superseded":  ("Superseded", "898781"),
    "descriptive": ("Descriptive", "1BAF7A"),
    "unverified":  ("Unverified series", "8A5CC2"),
}

CATEGORIES = [
 (1, "method", "Method: from GDP to oscillators",
  "How each economy's GDP becomes a phase oscillator and how the Kuramoto order parameter r(t) measures "
  "synchronization, with the first evidence that the measured synchronization is not chance. The four companion-book "
  "figures use Maddison real GDP per capita, the paper's data; one of them (F1.4) draws a series that matches no stored "
  "results file and should be redrawn. The six "
  "first-pass figures used World Bank GDP in current dollars, which mixes real output with inflation and exchange "
  "rates; they are kept as the record of the first run."),
 (2, "crisis_arc", "The crisis arc: synchronization around global recessions",
  "The paper's primary test. Crises are the Kose–Terrones global recessions (1975, 1982, 1991, 2009 and 2020), "
  "with the milder global downturns of 1998, 2001 and 2012 shown for contrast. Significance comes from the "
  "circular-shift permutation (53 configurations, so the smallest possible p is 1/53 = 0.019). Figures F2.1–F2.6 "
  "use the paper's convention P. The three companion figures F2.7–F2.9 were drawn with convention W, and under W "
  "the arc is not significant: see the table below and docs/open_issues.md, issue 1."),
 (3, "crisis_dating_history", "How the crisis definition was chosen (history)",
  "Before settling on Kose–Terrones global recessions the project tried three other datings: hand-picked global and "
  "regional crisis windows on current-dollar GDP, the same windows on Maddison real GDP, and systemic banking "
  "crises from the Jordà–Schularick–Taylor database. These figures are the record of why the paper dates crises by "
  "real activity. None of their numbers is a Paper 1 result. Two captions in the July Figure Atlas PDF quoted older "
  "p-values (0.06 and 0.038) than the figures themselves show (0.038 and 0.020); the figures and the results files "
  "agree, and the values below follow them."),
 (4, "amplitude_diversification", "What moves in a crisis: swing size, alignment and diversification",
  "Three ways to split the jump in world output variance in a global recession: synchronization against swing size "
  "(amplitude), the exact identity |Z| = Ā × R_A (world swing = average national swing × amplitude-weighted "
  "alignment), and the variance decomposition into an own term (each economy's volatility) and a cross term "
  "(co-movement). The corrected reading: 82–83% (GDP-weighted) to 97% (equal-weighted) of the excess crisis variance "
  "arrives through the cross term, but within the cross term's rise, bigger swings contribute 46–50%, higher "
  "correlation 35–41% and their interaction 13–14%. So the defensible phrase is amplification transmitted by "
  "alignment. The older slogan 'correlation events, not volatility events', printed on F4.4 and F4.6, is wrong."),
 (5, "network_phase", "Network geometry and phase structure",
  "The correlation network of the 26 business cycles, summarized by the mean edge length of its minimum spanning "
  "tree (distance √(2(1−ρ)), 10-year windows), and the phase lead of each economy against the world cycle. The "
  "network has tightened over five decades but does not contract before crises, and the economies are too tightly "
  "phase-locked for an epicenter to be recovered."),
 (6, "tipping_nulls", "Tipping tests: the honest nulls",
  "Tests for the early-warning signature of a bifurcation (B-tipping): rising autocorrelation and variance of r(t) "
  "before crises, and slower recovery when the implied Kuramoto coupling is treated as the bifurcation parameter. All "
  "are null against 5,000 spectrum-preserving surrogate economy sets. In the Ashwin et al. (2012) taxonomy this "
  "points away from B-tipping and towards noise- or rate-induced transitions. A third variant (restoring time, "
  "csd_fast.py) was also null; its script and figure were lost with the September workspace."),
 (7, "inside_economies", "Inside the economies: channels and global forces",
  "What happens underneath GDP: which demand, budget, money and interest-rate channels synchronize across economies "
  "and when, a two-economy case study (the United States and Japan), and the global series from the atlas. The "
  "channel anatomy holds the one lead that survives across decades: synchronized short-rate rises two years before "
  "global recessions (p = 0.019, 18 economies)."),
 (8, "country_atlas", "Country atlas: 31 economy dashboards",
  "One nine-panel dashboard per economy (growth, demand contributions, budget, debt, inflation and rates, real money, "
  "trade, current account, the economy's cycle against the rest), for the 26 and the five added economies (China, "
  "Brazil, Saudi Arabia, the United Arab Emirates and Iran). The compiled document for this category is the "
  "rebuilt 39-page atlas itself, which carries the text, tables and data notes for every page."),
]

# convention table printed on the crisis-arc document (values from paper1/results/runin_convention_check.json)
CONVENTION_TABLE = [
 ("P · paper: filter and Hilbert on 1950–2022", "+0.230 (0.038)", "+0.216 (0.019)", "+0.149 (0.189)", "+0.078 (0.679)", "−0.277 (0.019)", "+0.608"),
 ("W · filter from 1950, Hilbert on 1970–2022", "+0.210 (0.057)", "+0.178 (0.094)", "+0.112 (0.208)", "+0.088 (0.698)", "−0.144 (0.170)", "+0.509"),
 ("N · filter and Hilbert on 1970–2022", "+0.210 (0.038)", "+0.178 (0.094)", "+0.124 (0.189)", "+0.089 (0.679)", "−0.197 (0.094)", "+0.531"),
]

F = []
def add(**k): F.append(k)

# ---------------------------------------------------------------- 1 METHOD
add(id="F1.1", cat=1, name="pipeline_japan_real", src=f"{COMP}/rId21.png", status="current",
    title="From growth to phase: the measurement pipeline (Japan)",
    caption="(a) Japan's real GDP per capita rises smoothly; on its own it is not an oscillator. (b) The 2–9 year "
            "Butterworth band-pass (order 2, forward–backward) leaves the business-cycle wobble (red); its Hilbert "
            "partner (gold) is the same wobble shifted by a quarter cycle. (c) The instantaneous phase θ(t) = arg z(t) "
            "sweeps from −π to π once per cycle. (d) The analytic signal z(t) drawn in the complex plane: a rotating "
            "phasor whose angle is the phase and whose length is the amplitude A(t).",
    numbers="Illustration of Methods §2; no test.",
    made_by="Companion-book figure A1 (plotting script lost with the September workspace)",
    data="Maddison 2023, Japan, 1960–2022")
add(id="F1.2", cat=1, name="all_26_oscillators", src=f"{COMP}/rId24.png", status="current",
    title="All 26 economies as oscillators",
    caption="(a) The band-passed cycle of every economy, with the five global recession years in red. (b) The phase "
            "of every economy by year, one row per economy, colour giving the position in the cycle. A vertical stripe "
            "of one colour is a year in which the economies share a phase; the clearest stripes are around 2009 and 2020.",
    numbers="Descriptive.", made_by="Companion-book figure A2", data="Maddison 2023, 26 economies, 1970–2022")
add(id="F1.3", cat=1, name="order_parameter_real", src=f"{COMP}/rId28.png", status="current",
    title="The Kuramoto order parameter r(t), 1970–2022",
    caption="r(t) = |(1/N) Σ exp(iθ_i(t))| for the 26 economies, computed with the paper's convention P (filter and "
            "Hilbert transform on 1950–2022, statistics on 1970–2022). Pink bands are the five global recessions. With "
            "26 independent oscillators the expected r is about 0.20, so only the variation over time is interpreted.",
    numbers="Lowest r = 0.02 (1985); highest r = 0.98 (2020).",
    made_by="Companion-book figure A3; the series is r_by_year in paper1/results/kose_terrones_results.json",
    data="Maddison 2023")
add(id="F1.4", cat=1, name="real_vs_chance_real", src=f"{COMP}/rId32.png", status="unverified",
    title="The real world is far more synchronized than chance",
    caption="The observed r(t) (red) against the range produced by surrogate worlds in which every economy keeps its "
            "own power spectrum but its phases are randomized independently, so all alignment is destroyed (grey). "
            "This companion rendering used 2,000 surrogates; the paper's surrogate tests use 5,000. Its red line matches "
            "neither stored r(t) series (it shows about 0.40 in 1977, where convention P gives 0.17 and W 0.14), so the "
            "series behind it cannot be identified. Redraw from the convention-P series with 5,000 surrogates before using it.",
    numbers="As drawn: observed r above the chance range in most years and far above it in 2009 and 2020 (not verified).",
    made_by="Companion-book figure A4", data="Maddison 2023")
add(id="F1.5", cat=1, name="pipeline_japan_current_usd", src=f"{FIGSRC}/fig1_pipeline.pdf", status="superseded",
    title="First pass: the Hilbert pipeline on current-dollar GDP (Japan)",
    caption="The same four steps as F1.1, run in July on World Bank GDP in current US dollars (1970–2023). Nominal "
            "dollar GDP mixes real output, inflation and exchange-rate swings, which is why the paper moved to Maddison "
            "real GDP per capita.",
    numbers="Illustration only.", made_by="paper1/scripts/eraA_claude_ai/hilbert_oscillators.py (reproduces hilbert_output.csv exactly)",
    data="World Bank NY.GDP.MKTP.CD via datasets/gdp")
add(id="F1.6", cat=1, name="all_26_current_usd", src=f"{FIGSRC}/fig2_all_economies.pdf", status="superseded",
    title="First pass: all 26 economies on current-dollar GDP",
    caption="Every economy's cyclical component and the phase heat map, from the current-dollar first pass. Red lines "
            "mark 2008 and 2020.",
    numbers="Descriptive.", made_by="hilbert_oscillators.py", data="World Bank current US$")
add(id="F1.7", cat=1, name="order_parameter_current_usd", src=f"{FIGSRC}/fig3_order_parameter.pdf", status="superseded",
    title="First pass: R(t) on current-dollar GDP, 1970–2023",
    caption="The order parameter from the first pass. Its level differs a lot from the real-GDP series (for example "
            "0.72 against 0.28 in 1970) because exchange-rate and inflation swings move nominal dollar GDP together "
            "across countries.",
    numbers="Peak 0.91 (2019); trough 0.24 (2012), from crisis_results.json.",
    made_by="hilbert_oscillators.py", data="World Bank current US$")
add(id="F1.8", cat=1, name="surrogate_band_current_usd", src=f"{FIGSRC}/fig_surrogate_band.pdf", status="superseded",
    title="First pass: real synchronization against 5,000 surrogates",
    caption="Observed R(t) against the 95% band of 5,000 spectrum-preserving surrogate economy sets; dots mark years "
            "above the surrogate 95th percentile. The method is the paper's; the data are the superseded current-dollar series.",
    numbers="2009 and 2020 at the surrogate floor, p = 0.0002.",
    made_by="paper1/scripts/eraA_claude_ai/surrogate_test.py (reproduces surrogate_results.csv exactly)",
    data="World Bank current US$")
add(id="F1.9", cat=1, name="surrogate_convergence", src=f"{FIGSRC}/fig_convergence.pdf", status="superseded",
    title="First pass: Monte Carlo convergence of the surrogate p-value",
    caption="The running p-value for 2009 and 2020 as the number of surrogate worlds grows to 5,000. It settles at the "
            "floor 1/5001, showing that 5,000 draws are enough for a p-value of this size.",
    numbers="Final p = 0.0002 for both years.", made_by="surrogate_test.py", data="World Bank current US$")
add(id="F1.10", cat=1, name="null_histograms", src=f"{FIGSRC}/fig_null_hist.pdf", status="superseded",
    title="First pass: where the real R sits in the chance distribution",
    caption="Histograms of R under the no-coupling null for 2009 and 2020, with the observed value in red, far in the tail.",
    numbers="2009: R = 0.74, p = 0.0002. 2020: R = 0.81, p = 0.0002.", made_by="surrogate_test.py", data="World Bank current US$")

# ---------------------------------------------------------------- 2 CRISIS ARC
add(id="F2.1", cat=2, name="sync_vs_global_recessions", src=f"{FIGSRC}/kfig1_overview.pdf", status="current",
    title="Synchronization against Kose–Terrones global recessions and downturns",
    caption="r(t) for the 26 economies (convention P) with the five global recessions in red and the three global "
            "downturns in orange. The dotted line is the normal-year mean.",
    numbers="Normal-year mean r = 0.54.",
    made_by="paper1/scripts/eraA_claude_ai/kose_terrones_test.py → kose_terrones_results.json (reproduces exactly)",
    data="Maddison 2023")
add(id="F2.2", cat=2, name="sync_by_period_type", src=f"{FIGSRC}/kfig2_groups.pdf", status="current",
    title="Mean synchronization by period type",
    caption="Mean r in global-recession years, global-downturn years and normal years, with 95% bootstrap intervals. "
            "Recessions are the most synchronized and milder downturns the least, below normal years. The intervals "
            "overlap, so this is description rather than a test.",
    numbers="Recessions 0.65 [0.45, 0.86]; downturns 0.37 [0.23, 0.62]; normal 0.54 [0.47, 0.61].",
    made_by="kose_terrones_test.py", data="Maddison 2023")
add(id="F2.3", cat=2, name="leadlag_profile", src=f"{FIGSRC}/kfig3_leadlag.pdf", status="current",
    title="Does synchronization lead global recessions?",
    caption="Correlation of r(t) with the recession indicator shifted by −4 to +4 years (positive lag: synchronization "
            "comes first). The dashed line is the 95% chance level from the circular-shift permutation. The profile "
            "peaks at +1 and +2 years.",
    numbers="See F2.5 for the tested values.", made_by="kose_terrones_test.py", data="Maddison 2023")
add(id="F2.4", cat=2, name="fibrillation_signature_epoch", src=f"{FIGSRC}/kfig4_epoch.pdf", status="current",
    title="The fibrillation signature: rise, peak and shatter (superposed epoch, n = 5)",
    caption="Mean r around the five recession onsets (thick line), with each recession in colour. Synchronization "
            "climbs to its peak the year before onset and collapses two years after. Descriptive alignment, no p-value.",
    numbers="Peak 0.70 at t−1; 0.35 at t+2; drop 0.35.", made_by="kose_terrones_test.py", data="Maddison 2023")
add(id="F2.5", cat=2, name="fibrillation_arc_tested", src=f"{FIGSRC}/kfig5_arc.pdf", status="current",
    title="The tested arc: two years before to two years after",
    caption="Correlation of r(t) with the recession indicator at each timing, one-sided in the predicted direction. "
            "Leads and the crisis year are tested upward, lags downward. 0.019 is the permutation floor, so it means "
            "'no shift did better', not a smaller p. Over five lags no coefficient survives Bonferroni (lead-1 and "
            "after-2: adjusted p = 0.095); Benjamini–Hochberg gives q = 0.047 for both. The arc is significant under "
            "convention P only (table above).",
    numbers="Lead-2 +0.23 (p = 0.038); lead-1 +0.22 (0.019); crisis year +0.15 (0.189); after-1 +0.08 (0.679); after-2 −0.28 (0.019).",
    made_by="kose_terrones_test.py", data="Maddison 2023")
add(id="F2.6", cat=2, name="leave_one_crisis_out", src=f"{FIGSRC}/robustness_loo.pdf", status="current",
    title="Leave-one-crisis-out: the lead is carried by 2009 and 2020",
    caption="The lead-1 correlation refitted with each recession dropped in turn. It survives dropping 1975, 1982 or "
            "1991 and disappears without 2009 or 2020. The effective event count behind the pre-crisis claim is about "
            "two, both in the modern era, which is why the paper states it as a property of today's tightly coupled economy.",
    numbers="All five +0.22 (0.019); without 1975 +0.21 (0.019); without 1982 +0.24 (0.019); without 1991 +0.27 (0.019); "
            "without 2009 +0.12 (0.208); without 2020 +0.11 (0.264); without both −0.01 (0.491).",
    made_by="paper1/scripts/eraA_claude_ai/robustness.py (prints all checks; saves only the baseline)", data="Maddison 2023")
add(id="F2.7", cat=2, name="companion_sync_vs_recessions", src=f"{COMP}/rId36.png", status="convW",
    title="Companion version: synchronization against recessions and downturns",
    caption="The companion book's version of F2.1. It was computed with convention W, so its r(t) differs from F2.1 "
            "in many years (1970: 0.53 here against 0.28 in F2.1).",
    numbers="Descriptive.", made_by="Companion-book figure A5", data="Maddison 2023")
add(id="F2.8", cat=2, name="companion_signature_epoch", src=f"{COMP}/rId39.png", status="convW",
    title="Companion version: rise, peak and shatter",
    caption="The companion book's version of F2.4, drawn with convention W. The shatter is shallower than under the "
            "paper's convention.",
    numbers="Peak 0.69 at t−1; 0.46 at t+2 (convention P gives 0.70 and 0.35).",
    made_by="Companion-book figure A6", data="Maddison 2023")
add(id="F2.9", cat=2, name="companion_tested_arc", src=f"{COMP}/rId42.png", status="convW",
    title="Companion version: the tested arc (not significant under W)",
    caption="The companion book's version of F2.5, drawn with convention W. None of its bars reaches p < 0.05, although "
            "its title and the companion text say the rise and collapse are significant. Either redraw it with "
            "convention P or change the companion text; see docs/open_issues.md, issue 1.",
    numbers="Lead-2 +0.21 (0.057); lead-1 +0.18 (0.094); crisis year +0.11 (0.208); after-1 +0.09 (0.698); after-2 −0.14 (0.170).",
    made_by="Companion-book figure A7", data="Maddison 2023")

# ---------------------------------------------------------------- 3 CRISIS-DATING HISTORY
for i,(nm,ti,cap,num) in enumerate([
 ("cfig1_overview","Current dollars: synchronization with hand-picked crisis windows",
  "R(t) on current-dollar GDP with four global crisis windows (green: 1973–75, 1980–82, 2007–09, 2020) and two "
  "regional ones (yellow: 1997–98, 2011–12).","Descriptive."),
 ("cfig2_zoom","Current dollars: each global crisis, zoomed","Synchronization before, during and after each of the four global windows.","Descriptive."),
 ("cfig3_composite","Current dollars: composite around global-crisis onsets","Mean R across the four global crises, ±1 s.d., against the normal-year average.","Descriptive."),
 ("cfig4_permutation","Current dollars: global-crisis windows against randomly placed windows",
  "The contrast between mean R in global-crisis years and all other years, against 20,000 random placements of windows "
  "of the same lengths. (The July Figure Atlas caption said p ≈ 0.06; the figure and crisis_results.json say 0.038.)",
  "Real contrast +0.103; p = 0.038."),
 ("cfig5_groups","Current dollars: mean synchronization by period type","Mean R with 95% bootstrap intervals.","Global 0.75; regional 0.45; normal 0.67."),
],1):
    add(id=f"F3.{i}", cat=3, name=nm, src=f"{FIGSRC}/{nm}.pdf", status="superseded", title=ti, caption=cap, numbers=num,
        made_by="paper1/scripts/eraA_claude_ai/crisis_analysis.py → crisis_results.json (reproduces exactly)", data="World Bank current US$")
for i,(nm,ti,cap,num) in enumerate([
 ("rfig1_overview","Real GDP: synchronization with the same hand-picked windows","The same windows on Maddison real GDP per capita (convention P).","Descriptive."),
 ("rfig2_zoom","Real GDP: each global crisis, zoomed","The 2007–09 and 2020 shapes are cleaner in real terms; the oil shocks are muted.","Descriptive."),
 ("rfig3_composite","Real GDP: composite around global-crisis onsets","Mean r across the four global crises, ±1 s.d.","Descriptive."),
 ("rfig4_permutation","Real GDP: global-crisis windows against randomly placed windows",
  "As F3.4 on real GDP. (The July Figure Atlas caption said p = 0.038; the figure and crisis_results_real.json say 0.020.)",
  "Real contrast +0.202; p = 0.020."),
 ("rfig5_groups","Real GDP: mean synchronization by period type","Mean r with 95% bootstrap intervals.","Global 0.70; regional 0.30; normal 0.52."),
],6):
    add(id=f"F3.{i}", cat=3, name=nm, src=f"{FIGSRC}/{nm}.pdf", status="superseded", title=ti, caption=cap, numbers=num,
        made_by="paper1/scripts/eraA_claude_ai/real_gdp_analysis.py → crisis_results_real.json (reproduces exactly)", data="Maddison 2023")
add(id="F3.11", cat=3, name="dfig1_r_vs_C", src=f"{FIGSRC}/dfig1_r_vs_C.pdf", status="superseded",
    title="Banking crises: synchronization against banking-crisis intensity C(t)",
    caption="r(t) for the 17 JST economies (1970–2016) against C(t), the share of them in a systemic banking crisis. "
            "Dating crises from bank failures breaks the circularity of hand-picked windows, but the crises cluster on "
            "one global event (2008).",
    numbers="Descriptive.", made_by="paper1/scripts/eraA_claude_ai/crisis_dating_test.py → crisis_dating_results.json (not re-verified: needs jst.xlsx)",
    data="Jordà–Schularick–Taylor Macrohistory Database")
add(id="F3.12", cat=3, name="dfig2_leadlag", src=f"{FIGSRC}/dfig2_leadlag.pdf", status="superseded",
    title="Banking crises: lead–lag profile",
    caption="Cross-correlation of r(t) with C(t); positive lags mean synchronization comes first. No lag clears the "
            "permutation chance level, because there is essentially one global banking crisis.",
    numbers="Same year +0.23 (p = 0.106); lead-1 +0.21 (0.149); lead-2 +0.13 (0.298).", made_by="crisis_dating_test.py", data="JST")
add(id="F3.13", cat=3, name="dfig3_epoch", src=f"{ATL_IMG}/dfig3_epoch.png", status="superseded",
    title="Banking crises: synchronization around banking-crisis onsets",
    caption="Superposed epoch around the 1991 and 2007 banking-crisis onsets and their mean. Recovered from the July "
            "Figure Atlas PDF; the original file was not kept.",
    numbers="Descriptive.", made_by="crisis_dating_test.py", data="JST")
add(id="F3.14", cat=3, name="dfig4_onset_breadth", src=f"{FIGSRC}/dfig4_onset_breadth.pdf", status="superseded",
    title="Banking crises: the one crisis that went global began at peak synchronization",
    caption="Synchronization at each banking-crisis onset against how widely the crisis eventually spread. The 2007–08 "
            "crisis began near peak synchronization and reached most of the 17; crises that began at ordinary "
            "synchronization stayed contained. One event, so this is an anecdote, not a test.",
    numbers="2007–08: onset r ≈ 0.96, breadth ≈ 0.59.", made_by="crisis_dating_test.py", data="JST")
add(id="F3.15", cat=3, name="compare_definitions", src=f"{FIGSRC}/compare_definitions.pdf", status="superseded",
    title="Two crisis definitions, two verdicts",
    caption="(A) The banking definition captures one global event (2008); Kose–Terrones captures five. (B) Their lead–lag "
            "profiles: only the real-activity definition shows a significant lead. This is the figure that justifies "
            "the paper's choice of crisis dating.",
    numbers="Kose–Terrones significant at lead-1 and lead-2; banking never.", made_by="comparison of the two results files (plotting script not kept)", data="Maddison 2023 and JST")
add(id="F3.16", cat=3, name="compare_leadstats", src=f"{FIGSRC}/compare_leadstats.pdf", status="superseded",
    title="Synchronization–crisis correlation by timing, both definitions",
    caption="Correlations at the crisis year and one and two years before, for the banking definition (n = 1) and "
            "Kose–Terrones (n = 5).",
    numbers="Banking: p = 0.11, 0.15, 0.30. Kose–Terrones: p = 0.19, 0.02, 0.04.", made_by="as F3.15", data="Maddison 2023 and JST")

# ---------------------------------------------------------------- 4 AMPLITUDE / DIVERSIFICATION
add(id="F4.1", cat=4, name="amplitude", src=f"{FIGSRC}/amplitude.pdf", status="convW",
    title="Amplitude: does the world swing harder when it swings together?",
    caption="(A) r(t) and the mean cycle amplitude Ā(t). (B) r against Ā. (C) Two-stage epoch: r peaks a year before "
            "onset and amplitude peaks in the onset year. Drawn with convention W, which gives the '+0.51' quoted in "
            "early drafts; the paper's convention P gives +0.608 (detrended, p = 0.019) and Methods §6.2 uses that value.",
    numbers="Convention W: ρ = +0.51 detrended (+0.47 raw); p = 0.0006 against 5,000 surrogates.",
    made_by="paper1/scripts/eraA_claude_ai/amplitude_test.py → amplitude_results.json (reproduces exactly)", data="Maddison 2023")
add(id="F4.2", cat=4, name="companion_amplitude", src=f"{COMP}/rId46.png", status="convW",
    title="Companion version: the world swings harder when it swings together",
    caption="The companion book's version of F4.1 (A) and (B), also convention W.",
    numbers="ρ = +0.51, p = 0.0006 (convention W).", made_by="Companion-book figure A8", data="Maddison 2023")
add(id="F4.3", cat=4, name="fibrillation_identity", src=f"{FIGSRC}/fibrillation_identity.png", status="current",
    title="The fibrillation identity: world swing = national swing × alignment",
    caption="|Z(t)| = Ā(t) × R_A(t) holds exactly (error 4 × 10⁻¹⁹). Left: the three series relative to their own averages. "
            "Right: each recession's excess in log world swing², split into bigger swings and tighter alignment. Across "
            "the five recessions 61% of the excess comes from swing size and 39% from alignment; alignment alone is not "
            "significant against surrogates (p = 0.103), swing size is (p = 0.0002). R_A correlates +0.94 with r.",
    numbers="Swing / alignment by crisis: 1975 +0.91/+0.52; 1982 +0.36/+0.60; 1991 +0.18/−0.53; 2009 +1.24/+1.28; 2020 +2.36/+1.40.",
    made_by="paper1/scripts/eraB_claude_code/structure_tests.py → structure_results.json (reproduces exactly; plotting script lost)",
    data="Maddison 2023")
add(id="F4.4", cat=4, name="diversification_gdp_weighted", src=f"{FIGSRC}/diversification.pdf", status="relabel",
    title="Loss of diversification (GDP-weighted)",
    caption="(A) World output variance in 10-year windows split into the own term (individual volatility) and the cross "
            "term (co-movement). (B) The excess variance in global-recession windows: 0.13 from the own term against "
            "0.64 from the cross term (× 10⁻⁴), so about 83% arrives through co-movement. (C) The crisis cross-term share "
            "(0.72) against 5,000 surrogates. Two corrections: the title's 'not volatility-driven' is wrong once the cross "
            "term is split (swing size supplies about half of its rise), and the p = 0.0002 in (C) only says the economies "
            "are correlated at all, not that crises are special (Methods §6.1 and §7.6).",
    numbers="Cross share of excess 82.6% with end-of-window weights (82.4% with the within-window mean weights Methods §6.1 states); "
            "cross share 0.72 in crisis windows against 0.67 in normal windows; 1975 is outside the window support.",
    made_by="paper1/scripts/eraA_claude_ai/diversification.py → diversification_results.json (reproduces exactly)", data="Maddison 2023")
add(id="F4.5", cat=4, name="diversification_both_weightings", src=f"{FIGSRC}/diversification_compare.pdf", status="relabel",
    title="Loss of diversification under both weightings",
    caption="(A) Share of the excess crisis variance supplied by the cross term, GDP-weighted and equal-weighted. (B) Cross-term "
            "share of world variance in recession and normal windows. The 'p = 0.0002' label is the same weak test as F4.4 (C).",
    numbers="83% GDP-weighted and 97% equal-weighted; cross shares 0.72 vs 0.67 (GDP) and 0.88 vs 0.82 (equal).",
    made_by="diversification.py and diversification_equal.py", data="Maddison 2023")
add(id="F4.6", cat=4, name="companion_diversification", src=f"{COMP}/rId50.png", status="relabel",
    title="Companion version: loss of diversification",
    caption="The companion book's restyled F4.4, with the same superseded title wording and the same panel C.",
    numbers="As F4.4.", made_by="Companion-book figure (lovedones/diversification.png)", data="Maddison 2023")
add(id="F4.7", cat=4, name="companion_diversification_compare", src=f"{COMP}/rId53.png", status="relabel",
    title="Companion version: robust to the weighting scheme",
    caption="The companion book's restyled F4.5.",
    numbers="As F4.5.", made_by="Companion-book figure (lovedones/diversification_compare.png)", data="Maddison 2023")

# ---------------------------------------------------------------- 5 NETWORK / PHASE
add(id="F5.1", cat=5, name="mst_network", src=f"{FIGSRC}/mst_network.pdf", status="relabel",
    title="Correlation-network topology: the minimum spanning tree of 26 business cycles",
    caption="(A) Mean MST edge length L(t), 10-year windows, with a linear trend: the network tightens for 50 years. "
            "(B) L around crisis onsets. Two annotations are out of date. '~3× tighter' compares the noisy single-year "
            "endpoints (0.781 in 1971, 0.249 in 2022); decade means give 1.9× (0.706 in the 1970s, 0.379 in 2013–22). "
            "'p = 0.47' could not be reproduced; the stored test is τ = −0.171, p = 0.167 (raw) and τ = −0.086, p = 0.316 "
            "(detrended). Both say no pre-crisis contraction.",
    numbers="Most central economies (mean MST degree): France 2.85, Netherlands 2.65, Finland 2.62.",
    made_by="paper1/scripts/eraA_claude_ai/mst_network.py → mst_results.json (reproduces exactly)", data="Maddison 2023")
add(id="F5.2", cat=5, name="companion_network_tightening", src=f"{COMP}/rId57.png", status="current",
    title="Companion version: the network has tightened about twice since the 1980s",
    caption="L(t) from 1979 with its long-run trend. With windows kept inside 1970–2022 the decade-mean comparison is "
            "0.652 (1979–89) against 0.379 (2013–22), about 1.7×; '~2×' is a fair round figure (Methods §7.7).",
    numbers="1.7× (1979–89 base) to 1.9× (1970s base).", made_by="Companion-book figure A9", data="Maddison 2023")
add(id="F5.3", cat=5, name="phase_lags", src=f"{FIGSRC}/phase_lags.pdf", status="convW",
    title="Pairwise phase lags: is there an epicenter?",
    caption="(A) Each economy's mean phase lead over the world cycle in years (mean period 5.85 years). Nearly all sit "
            "within ±0.5 years; Turkey is the outlier at +1.4. (B) The spread of leads (s.d. 0.40 years) against "
            "uncoupled surrogates (mean 0.94, minimum 0.45). The economies are phase-locked far more tightly than chance, "
            "so no leader can be recovered. The figure's p = 0.0002 is the correct lower-tail value; "
            "phase_lag_results.json stores p_spread = 1.0, which is the upper tail. Computed with convention W (phases from "
            "1970–2022 only), although Methods §1 states P for every phase; Methods §6.6 quotes this W value. Recompute under P.",
    numbers="Spread 0.403 years; lower-tail p = 0.0002 (all 5,000 surrogates larger).",
    made_by="paper1/scripts/eraA_claude_ai/phase_lags.py → phase_lag_results.json (reproduces exactly)", data="Maddison 2023")

# ---------------------------------------------------------------- 6 TIPPING NULLS
add(id="F6.1", cat=6, name="critical_slowing_down", src=f"{FIGSRC}/csd_surrogate_null.pdf", status="current",
    title="Critical slowing down of synchronization: null",
    caption="Trend (Kendall τ) of the lag-1 autocorrelation and of the variance of r(t) over the 8 years before each "
            "recession (rolling 15-year windows, Gaussian detrending σ = 5), averaged over recessions, against 5,000 "
            "surrogate sets. Neither rises more than chance. Per recession, the variance trend is positive only for "
            "2009 (+0.43) and 2020 (+0.79). Phases here come from a Hilbert transform on 1962–2022 (eight years of run-in), "
            "not the full 1950 run-in of convention P.",
    numbers="AR(1): τ = −0.15, p = 0.757. Variance: τ = +0.29, p = 0.107.",
    made_by="paper1/scripts/eraA_claude_ai/csd_surrogate.py → csd_surrogate_results.json (reproduces exactly)", data="Maddison 2023")
add(id="F6.2", cat=6, name="kuramoto_coupling_bifurcation", src=f"{FIGSRC}/kuramoto_bifurcation.pdf", status="current",
    title="Kuramoto coupling as the bifurcation parameter: no slowing",
    caption="(A) Implied coupling K/K_c = 1/(1 − r²) around each recession: far above critical before 2009 and 2020, "
            "then back to about 1. Because K/K_c is a monotone transform of r, (A) restates r rather than adding a "
            "measurement. (B) The recovery rate λ stays flat. (C) Post-crisis change in λ against 5,000 surrogates: no slowing. "
            "Phases from a Hilbert transform on 1962–2022, as in F6.1.",
    numbers="Mean K/K_c: 6.4 at t−1 and 7.1 at t0; Δλ = +0.10, p = 0.54.",
    made_by="paper1/scripts/eraA_claude_ai/kuramoto_bifurcation.py → kuramoto_bifurcation_results.json (reproduces exactly)", data="Maddison 2023")

# ---------------------------------------------------------------- 7 INSIDE THE ECONOMIES
add(id="F7.1", cat=7, name="us_japan_inside", src=f"{FIGSRC}/usjp_inside.png", status="descriptive",
    title="Inside two economies: the United States and Japan",
    caption="(a, b) Each year's growth split into consumption, investment, government, exports and imports, with each "
            "part's share of the variance of growth. (c) US–Japan cycle correlation by channel, 1961–89 and 1990–2019: "
            "trade and investment carry the link. (d) Budgets as shock absorbers: deficits widen in every slump. "
            "(e) The absorbed shocks accumulate as debt. (f) Monetary room: Japan's short rate reaches zero in the 1990s, "
            "the US rate in 2009.",
    numbers="Variance shares US: I 68%, C 47%, G 2%, X 9%, M −26%; Japan: I 57%, C 41%, G 5%, X 10%, M −12%. "
            "Cycle–balance correlation US +0.45, Japan +0.35. Debt 1970→2022: US 33%→119%, Japan 8%→256%.",
    made_by="paper1/scripts/eraB_claude_code/usjp.py (plotting script lost)", data="Global Macro Database and Penn World Table 10.01")
add(id="F7.2", cat=7, name="channel_anatomy_26", src=f"{FIGSRC}/anatomy26.png", status="current",
    title="Anatomy of a global recession: which channel synchronizes, and when",
    caption="(a) For each channel, the correlation of its cross-country synchronization r(t) with recession onset two "
            "years before, one year before, in the recession year and two years after (★ p < 0.05, circular shift). "
            "Synchronized short-rate rises come two years before; investment and imports one to two years before; "
            "budgets in the recession year. (b) Every channel is more synchronized since 1990, budgets most of all. "
            "(c) The sequence: rates lock first, then demand, then budgets respond together.",
    numbers="Short rates (18 economies): +0.27 two years before, p = 0.019.",
    made_by="paper1/scripts/eraB_claude_code/panel26.py → panel26_results.json (reproduces exactly; plotting script lost)",
    data="Global Macro Database")
for i,(nm,ti,cap,num) in enumerate([
 ("global_real","Global forces I: growth, oil, trade, inflation and synchronization by channel",
  "World growth (GDP-weighted), how many of the 26 shrank each year, the real oil price, imports of the 26 as a share "
  "of their GDP, inflation across the 26, and r(t) for real GDP, investment and short rates. The last two to three "
  "years of each r(t) are less reliable because of the filter edge.",
  "25 of 26 shrank in 2020 and 22 in 2009, against 8–11 in 1975, 1982 and 1991. GDP r(t): lead-1 +0.24 (p = 0.019); "
  "investment lead-2 +0.29 (0.038); short rates lead-2 +0.27 (0.019)."),
 ("global_money","Global forces II: interest rates, the dollar and crisis onsets",
  "US and median short-term rates, the share of economies raising rates, the US real effective exchange rate, and "
  "banking and currency crisis onsets among the 26.","Descriptive."),
 ("overview_heat","The 26 side by side: coupling by decade and growth in each recession",
  "Left: each economy's correlation with the other 25, by decade. Right: real GDP growth in each global recession.",
  "Average coupling 0.46 (1970–89) and 0.75 (1990–2022)."),
 ("overview_extra","The five added economies: coupling to the 26 and growth in each recession",
  "As the overview heat map, for China, Brazil, Saudi Arabia, the United Arab Emirates and Iran, each compared with "
  "the 26 (never part of their averages).","Descriptive."),
],3):
    add(id=f"F7.{i}", cat=7, name=nm, src=f"{ATLAS_FIG}/{nm}.png", status="descriptive", title=ti, caption=cap, numbers=num,
        made_by="atlas/figs.py (from atlas/panel.csv, global.csv, stats.json, sync.json)", data="Global Macro Database and pinned sources")

# ---------------------------------------------------------------- 8 COUNTRY ATLAS
ATLAS_ORDER = ["USA","CAN","MEX","DEU","FRA","GBR","ITA","NLD","BEL","AUT","CHE","SWE","NOR","DNK","FIN","ESP","PRT","GRC",
               "TUR","JPN","KOR","AUS","IND","IDN","THA","ZAF","CHN","BRA","SAU","ARE","IRN"]


# ---------------------------------------------------------------- redrawn on S31 for the manuscript (15 October 2026)
# Drawn by `python -m ef.manuscript.build figures` (src/ef/manuscript/figures.py) from the S31 results under convention P,
# with corrected labels (open issues 4-7, 18). Each keeps its ID; the new file sits next to the earlier one, which is
# not overwritten. Not yet merged into the entries above: rebuilding docs/FIGURES.md and the figure books with
# tools/build_figure_docs.py needs pdftoppm (poppler) and xelatex, which are not installed (paper1/manuscript/BUILD_PDF.md).
REDRAWN_S31 = {
    "F1.3": "figures/01_method/F1-03_order_parameter_s31.png",
    "F2.5": "figures/02_crisis_arc/F2-05_arc_tested_s31.png",
    "F4.1": "figures/04_amplitude_diversification/F4-01_amplitude_s31.png",
    "F4.4": "figures/04_amplitude_diversification/F4-04_diversification_s31.png",
    "F4.5": "figures/04_amplitude_diversification/F4-05_diversification_weightings_s31.png",
    "F5.1": "figures/05_network_phase/F5-01_mst_s31.png",
    "F5.4": "figures/05_network_phase/F5-04_methods_diagnostics_s31.png",   # new ID: the Methods diagnostics figure (issue 18)
    "F6.1": "figures/06_tipping_nulls/F6-01_early_warning_s31.png",
}
