# G0 data card — the yearly graph dataset on S31

Stage G0 of the GNN track (`gnn/README.md`). Built by `python -m ef.gnn.report` (`src/ef/gnn/dataset.py`) into `build/gnn/g0/` (git-ignored; rebuilt from the pinned sources). Status: **for Sid's review**; nothing is trained.

## What it is

- **Years:** 53 yearly graphs, 1970–2022.
- **Nodes:** the 31 economies of S31 (United States, United Kingdom, Germany, France, Italy, Japan, Canada, Spain, Australia, South Korea, India, Mexico, Netherlands, Sweden, Switzerland, Belgium, South Africa, Turkey, Norway, Austria, Denmark, Finland, Greece, Portugal, Indonesia, Thailand, China, Brazil, Saudi Arabia, Iran, Russia) and one world node.
- **Edge types:** trade (economy → economy), bank (lender → borrower), oil (economy → world node). No correlation edges (Sid, 11 October 2026: correlation edges carry the target).
- **Missing values:** masked, never filled. `mask` is True where a value is observed; every cell also has a gap class (`gnn/G0_missing_data.md`).
- **Files:** `nodes.npz` (X: years × nodes × features, mask, gap, years, nodes, features); `edges_trade.csv`, `edges_bank.csv`, `edges_oil.csv` (one row per directed pair and year, NaN = masked, `gap` = class). `ef.gnn.dataset.load()` reads them. PyTorch Geometric objects are built in G3; this environment has no torch.

## Node features

| Feature | Nodes | Source | Note |
|---|---|---|---|
| `phase_sin` | economies | Maddison 2023, log GDP per capita; band-pass and Hilbert transform on data up to each year (convention C) | sin of the past-only phase; past data only |
| `phase_cos` | economies | Maddison 2023, log GDP per capita; band-pass and Hilbert transform on data up to each year (convention C) | cos of the past-only phase; past data only |
| `log_amplitude` | economies | Maddison 2023, log GDP per capita; band-pass and Hilbert transform on data up to each year (convention C) | log of the past-only cycle amplitude (swing size); past data only |
| `row_phase_sin` | economies | Maddison 2023, log GDP per capita; band-pass and Hilbert transform on data up to each year (convention C) | sin of the rest-of-world past-only mean phase; past data only |
| `row_phase_cos` | economies | Maddison 2023, log GDP per capita; band-pass and Hilbert transform on data up to each year (convention C) | cos of the rest-of-world past-only mean phase; past data only |
| `growth` | economies | atlas panel with Russia (`build/data/atlas_s31`; Global Macro Database and IMF sources, repaired) | real GDP growth, %; year t's value |
| `c_C` | economies | atlas panel with Russia (`build/data/atlas_s31`; Global Macro Database and IMF sources, repaired) | consumption contribution to growth, pp; year t's value |
| `c_I` | economies | atlas panel with Russia (`build/data/atlas_s31`; Global Macro Database and IMF sources, repaired) | investment contribution, pp; year t's value |
| `c_NX` | economies | atlas panel with Russia (`build/data/atlas_s31`; Global Macro Database and IMF sources, repaired) | net-export contribution, pp; year t's value |
| `govexp_GDP` | economies | atlas panel with Russia (`build/data/atlas_s31`; Global Macro Database and IMF sources, repaired) | government spending, % of GDP; year t's value |
| `govdef_GDP` | economies | atlas panel with Russia (`build/data/atlas_s31`; Global Macro Database and IMF sources, repaired) | budget balance, % of GDP; year t's value |
| `govdebt_GDP` | economies | atlas panel with Russia (`build/data/atlas_s31`; Global Macro Database and IMF sources, repaired) | government debt, % of GDP; year t's value |
| `infl` | economies | atlas panel with Russia (`build/data/atlas_s31`; Global Macro Database and IMF sources, repaired) | inflation, %; year t's value |
| `strate` | economies | atlas panel with Russia (`build/data/atlas_s31`; Global Macro Database and IMF sources, repaired) | short-term interest rate, %; year t's value |
| `ltrate` | economies | atlas panel with Russia (`build/data/atlas_s31`; Global Macro Database and IMF sources, repaired) | long-term interest rate, %; year t's value |
| `real_money_growth` | economies | atlas panel with Russia (`build/data/atlas_s31`; Global Macro Database and IMF sources, repaired) | real money growth, log points x 100; year t's value |
| `exports_GDP` | economies | atlas panel with Russia (`build/data/atlas_s31`; Global Macro Database and IMF sources, repaired) | exports, % of GDP; year t's value |
| `imports_GDP` | economies | atlas panel with Russia (`build/data/atlas_s31`; Global Macro Database and IMF sources, repaired) | imports, % of GDP; year t's value |
| `CA_GDP` | economies | atlas panel with Russia (`build/data/atlas_s31`; Global Macro Database and IMF sources, repaired) | current account, % of GDP; year t's value |
| `unemp` | economies | atlas panel with Russia (`build/data/atlas_s31`; Global Macro Database and IMF sources, repaired) | unemployment rate, %; year t's value |
| `r_past` | world | past-only phases of the 31 | order parameter r(t) of the 31 past-only phases |
| `world_phase_sin` | world | past-only phases of the 31 | sin of the world mean past-only phase |
| `world_phase_cos` | world | past-only phases of the 31 | cos of it |
| `us_strate` | world | atlas panel, United States | US short-term interest rate, % |
| `us_real_strate` | world | atlas panel, United States | US real short rate, % |
| `oil_real_2015usd` | world | atlas global factors | real crude oil price, 2015 US dollars |
| `world_growth` | world | atlas global factors | world growth, % (GDP-weighted over the 26 of the atlas, not the 31) |

Predictive use: phases and amplitude use data up to year t only (rule 7). The atlas features are year t's values as published, without filtering; they carry no two-sided filter. The atlas's own `cycle`, `phase`, `row_cycle` and `row_phase` columns are two-sided and are not used. `world_growth` weights the 26 of the atlas, not the 31.

## Edges

| Type | Direction | Attributes | Source | Normalisation |
|---|---|---|---|---|
| trade | exporter → importer | `exports_fob_usd` (exporter's report), `mirror_imports_cif_usd` (importer's report), IMF-estimate flags, proxy-unit flag | IMF IMTS, `imf_imts_s31` (downloaded 13 October 2026) | raw US dollars; shares (of the exporter's exports or GDP) are chosen in G3 |
| bank | lender → borrower | `claims_all_sectors_usd`, `claims_on_banks_usd` (year-end Q4 stocks) | BIS LBS, `bis_lbs` (June 2026 file) | raw US dollars; the BIS spec's row shares are chosen in G3 |
| oil | economy → world | `net_oil_exports_share_gdp` | **none pinned yet** | masked |

Bank filters (data/sources.yaml `read_with`): stocks, claims, all instruments, all currencies, all parent countries, all reporting banks, cross-border; all sectors, and banks only as a second attribute. Lenders: the fixed 10 reporting since 1977-Q4 (Sid); the expanding set is a sensitivity check for later.

## Sources, verified against data/sources.yaml (sha256)

| Source | File | Pinned at | Checksum |
|---|---|---|---|
| maddison | `data/MaddisonData.rda` | 3ed424b63c | ok |
| gmd | `data/final/data_final.dta` | 2930dade4a | ok |
| gmd | `data/clean/aggregators/IMF/IMF_WEO.dta` | 2930dade4a | ok |
| gmd | `data/clean/aggregators/IMF/IMF_FPP.dta` | 2930dade4a | ok |
| gmd | `data/clean/aggregators/IMF/IMF_HDD.dta` | 2930dade4a | ok |
| gmd | `data/clean/aggregators/JST/JST.dta` | 2930dade4a | ok |
| pwt | `data/pwt10.01.rda` | 957b298fd7 | ok |
| oil_bp | `datasets/Crude Oil Consumption vs. Price - BP Statistics (2016)/Crude Oil Consumption vs. Price - BP Statistics (2016).csv` | 6155d4ca1e | ok |
| oil_brent | `data/brent-year.csv` | b1d944f943 | ok |
| bis_lbs | `WS_LBS_D_PUB_csv_col.zip` | 2026-07-15 | ok |
| bis_lbs | `WS_LBS_D_PUB_csv_col.csv` | 2026-07-15 | ok |
| imf_imts_s31 | `IMTS_S31_annual.csv` | 2026-10-13 | ok |
| imf_imts_s31 | `query_url.txt` | 2026-10-13 | ok |

## Coverage in one line each

- Node features: 94.2% of economy-feature-years observed; phases complete; the largest gaps are long rates, demand contributions and budget series before the 1990s (details in the missing-data report).
- Trade: 96.4% of directed pair-years observed; Russia from 1992.
- Bank: 83.4% of lender-borrower-years observed, 96.1% from 1977.
- Oil: links present, weights masked (no source).

## Open for Sid

1. **Oil exposure source.** Net oil exports as a share of GDP needs country oil production and consumption. Candidate: the Our World in Data energy dataset (GitHub `owid/energy-data`, pinnable by commit, oil production and consumption by country from 1965), or the Energy Institute Statistical Review. Not added without approval.
2. **Russia before 1992.** Trade and bank links are masked. The USSR's trade (IMF, from 1955) and the BIS claims on the USSR are in the pinned files; using them for Russia would be a substitution, not data for Russia.
3. **Belgium and South Africa before 1997–98** use the IMF's Belgium-Luxembourg and South African Customs Union units (decided 11 October 2026); the rows are flagged.
4. **Edge weights.** Raw US dollars are stored; the normalisation (row shares, or the partner's share of GDP) is a G3 modelling choice to be fixed before any training.
