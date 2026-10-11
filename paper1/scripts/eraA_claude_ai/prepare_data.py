"""
prepare_data.py — load the GDP panel for the economic-fibrillation analysis.

Two data options:
  (A) World Bank current-US$ GDP  — the CSV shipped alongside this script (works offline).
  (B) Maddison 2023 real GDP per capita (constant 2011 int-$) — fetched live from
      Our World in Data. Better for a paper; needs internet. Flip USE_REAL_GDP = True.

Output (both options): a wide DataFrame `panel`, index = Year, columns = countries,
restricted to 1970-2023, with no missing values.
"""

import pandas as pd

USE_REAL_GDP = False   # <-- set True to use Maddison 2023 real GDP per capita

# The 26 economies (World Bank names). Maddison uses the same English names.
COUNTRIES = ['United States','United Kingdom','Germany','France','Italy','Japan',
 'Canada','Spain','Australia','South Korea','India','Mexico','Netherlands','Sweden',
 'Switzerland','Belgium','South Africa','Turkey','Norway','Austria','Denmark','Finland',
 'Greece','Portugal','Indonesia','Thailand']

Y0, Y1 = 1970, 2023

if not USE_REAL_GDP:
    # ---- Option A: World Bank current-US$ (local CSV) ----
    df = pd.read_csv('gdp_panel_long_1970_2023.csv')
    panel = df.pivot(index='Year', columns='Country', values='GDP_current_USD')
    panel = panel[COUNTRIES]
    UNIT = 'GDP, current US$ (World Bank)'
else:
    # ---- Option B: Maddison 2023 real GDP per capita (constant 2011 int-$) ----
    url = ("https://ourworldindata.org/grapher/gdp-per-capita-maddison-project-database.csv"
           "?v=1&csvType=full&useColumnShortNames=true")
    raw = pd.read_csv(url, storage_options={'User-Agent': 'research/1.0'})
    # columns: Entity, Code, Year, <gdp per capita short name>
    valcol = [c for c in raw.columns if c not in ('Entity', 'Code', 'Year')][0]
    raw = raw.rename(columns={'Entity': 'Country', valcol: 'value'})
    # Maddison uses 'South Korea' as 'South Korea'? OWID entity names mostly match;
    # adjust here if a KeyError appears (e.g. 'Turkey' vs 'Turkiye').
    raw = raw[raw['Country'].isin(COUNTRIES)]
    panel = raw.pivot(index='Year', columns='Country', values='value')
    missing = [c for c in COUNTRIES if c not in panel.columns]
    if missing:
        print('NOTE: name mismatch for', missing, '-> check OWID entity spelling')
    panel = panel[[c for c in COUNTRIES if c in panel.columns]]
    UNIT = 'Real GDP per capita, constant 2011 int-$ (Maddison 2023)'

panel = panel.loc[(panel.index >= Y0) & (panel.index <= Y1)]
panel = panel.dropna(axis=1, how='any')  # keep only fully-covered countries

print('Series :', UNIT)
print('Shape  :', panel.shape, '(years x countries)')
print('Years  :', int(panel.index.min()), '-', int(panel.index.max()))
print('Countries kept:', len(panel.columns))
print(panel.iloc[:3, :4])
