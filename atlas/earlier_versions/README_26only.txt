The 26 economies, 1970-2022 -- data and scripts behind the atlas
===================================================================

Files
  panel.csv    one row per economy-year (26 economies x 1950-2022). Key columns:
               growth (real GDP growth, %), c_C / c_I / c_NX (contributions to growth, pp),
               govexp_GDP / govrev_GDP / govdef_GDP / govdebt_GDP (repaired budget and debt, % GDP;
               the original GMD versions are kept with the suffix _gmd), fiscal_hist / debt_hist
               (True where an older IMF series was spliced in), strate / ltrate / infl,
               money_growth and real_money_growth (log points), exports_GDP / imports_GDP, CA_GDP,
               cycle / phase (2-9 year band-pass of log real GDP and its Hilbert phase),
               row_cycle (average standardized cycle of the other 25).
  global.csv   world aggregates by year (GDP-weighted growth, number contracting, real oil price,
               imports % GDP, inflation median and quartiles, US and median short rates, share of
               economies raising rates, US real effective exchange rate, crisis onsets).
  stats.json   every number printed on the country pages.
  meta.json    country order and, for each economy, every repair applied ("fixes").
  sync.json    synchronization r(t) for real GDP, investment and short rates, and the
               lead-lag permutation tests against the five global recession years.

Scripts (run in this order, Python 3, from this folder)
  data.py       builds panel.csv, global.csv, meta.json from the Global Macro Database and the
                IMF / Penn World Table source files (paths at the top of the script)
  stats.py      builds stats.json
  sync.py       builds sync.json
  figs.py       draws fig/*.png  (python3 figs.py all)
  build_tex.py  writes atlas.tex; compile with xelatex twice

Sources: Global Macro Database (Mueller, Xu, Lehbib & Chen 2025, Sept 2026 release); IMF World
Economic Outlook; IMF Public Finances in Modern History (Mauro et al. 2015); IMF Historical Public
Debt Database (Abbas et al. 2010); Penn World Table 10.01; BP Statistical Review via Our World in
Data and EIA Brent (oil).
