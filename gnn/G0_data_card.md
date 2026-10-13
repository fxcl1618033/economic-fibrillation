# G0 data card — the yearly graph dataset on S31

Stage G0 of the GNN track (`gnn/README.md`). Built by `python -m ef.gnn.report` (`src/ef/gnn/dataset.py`) into `build/gnn/g0/` (git-ignored; rebuilt from the pinned sources). Status: **for Sid's review**; nothing is trained.

## What it is

- **Years:** 53 yearly graphs, 1970–2022.
- **Nodes:** the 31 economies of S31 (United States, United Kingdom, Germany, France, Italy, Japan, Canada, Spain, Australia, South Korea, India, Mexico, Netherlands, Sweden, Switzerland, Belgium, South Africa, Turkey, Norway, Austria, Denmark, Finland, Greece, Portugal, Indonesia, Thailand, China, Brazil, Saudi Arabia, Iran, Russia) and one world node.
- **Edge types:** trade (economy → economy), bank (lender → borrower), oil (economy → world node). No correlation edges (Sid, 11 October 2026: correlation edges carry the target).
- **Missing values:** masked, never filled. `mask` is True where a value is observed; every cell and every edge weight also has a gap class (`gnn/G0_missing_data.md`).
- **Files:** `nodes.npz` (X: years × nodes × features, mask, gap, years, nodes, features); `edges_trade.csv`, `edges_bank.csv`, `edges_oil.csv` (one row per directed pair and year, NaN = masked); `gdp_current_usd.csv` (the denominators). `ef.gnn.dataset.load()` reads them; `ef.gnn.dataset.model_inputs()` returns only what a model may read. PyTorch Geometric objects are built in G3; this environment has no torch.

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

## Edges and their weights

**Normalisation, fixed by Sid on 13 October 2026 before any training:** the primary weight is the flow as a share of the receiving economy's nominal GDP; the sensitivity weight is the flow as a share of the exporter's or lender's total; raw US dollars are never model inputs. The `raw_*` columns are kept for checking only, and `model_inputs()` leaves them out.

| Type | Direction | Primary weight (`w_`) | Sensitivity weight (`s_`) | Raw columns (never inputs) | Source |
|---|---|---|---|---|---|
| trade | exporter → importer | `w_exports_share_dst_gdp` (exporter's report, FOB) and `w_mirror_share_dst_gdp` (importer's report, CIF), each ÷ the importer's GDP | `s_exports_share_src_total`, `s_mirror_share_src_total`: each ÷ the exporter's goods exports to the world, as the exporter reports them | `raw_exports_fob_usd`, `raw_mirror_imports_cif_usd` | IMF IMTS, `imf_imts_s31` |
| bank | lender → borrower | `w_claims_share_dst_gdp`: year-end (Q4) cross-border claims on all sectors ÷ the borrower's GDP | `s_claims_share_src_total`: ÷ the lender's cross-border claims on all countries | `raw_claims_usd`, `raw_lender_claims_all_countries_usd` | BIS LBS, `bis_lbs` |
| oil | economy → world | `w_net_oil_exports_share_gdp`: net oil exports ÷ the economy's own GDP (below) | the same weight (no second normalisation is defined for oil) | `raw_oil_production_twh`, `raw_oil_consumption_twh`, `raw_net_oil_twh`, `raw_net_oil_value_usd` | Our World in Data energy, `owid_energy` |

Trade: the exporter's and the importer's reports of the same flow are two attributes of one trade edge, each with its own mask (decided by Sid, 13 October 2026, for G3); neither is filled from the other. The mirror's sensitivity weight divides an importer's figure by an exporter's total (the only world total available for the exporter). Bank: the BIS publishes bilateral claims for all sectors and for non-banks only, so no banks-only attribute is built. Filters: stocks, claims, all instruments, all currencies, all parent countries, all reporting banks, cross-border (`data/sources.yaml`, `read_with`). Lenders: the fixed 10 reporting since 1977-Q4 (Sid); the expanding set is a sensitivity check for later.

**Denominator.** Nominal GDP in current US dollars from the World Bank (NY.GDP.MKTP.CD, the pinned `wb_gdp_current_usd` file). It is missing for Brazil 1970–1988, Iran 1991–1992 and Russia before 1988; weights that need those years are masked, not filled from another source. A fresh World Bank download (approved by Sid on condition that it matched the pinned file exactly where both have data) does not match: it carries revisions of more than 0.1% in 853 of 1,604 shared economy-years, so it is pinned but not used, and Brazil stays masked (missing-data report, section 5). The Global Macro Database's nominal GDP over its exchange rate was the alternative and was not used: against the World Bank it is 6 times larger for Iran by 2022 (the official rial rate) and about a third larger for Turkey and a fifth for Indonesia in most years.

## Oil exposure: the conversion

Net oil exports as a share of nominal GDP (Sid, 13 October 2026), positive for net exporters:

    w = (oil production − oil consumption) [TWh] × 630,267 barrels per TWh × crude price [US$ of the year per barrel]
        ÷ nominal GDP [current US$, World Bank]

- **Quantities:** `oil_production` and `oil_consumption` (primary energy consumption from oil), both in TWh, from the Our World in Data energy dataset (legacy release, commit f8de88a; Energy Institute Statistical Review 2025, and The Shift Data Portal for production of economies the Energy Institute does not list).
- **Production after 2016** (Sid, 13 October 2026): where OWID's production ends in 2016, 2017–2022 come from the EIA's International Energy Statistics (crude oil including lease condensate + natural gas plant liquids, barrels a day converted with the same factor) for the economies where the EIA and OWID agree over 1980–2016 within the tolerance fixed before the comparison: Germany, France, Spain, Netherlands, Sweden, Turkey, Austria, Greece. Japan and South Africa fail it and stay masked in 2017–2022. Flag: `production_from_eia`.
- **True-zero producers** (Sid): South Korea, Switzerland, Belgium, Finland and Portugal produce no oil in any year: OWID records zero in every year it lists (1980–2016) and so does the EIA (2004–2025). Their unlisted years are zero, not masked. Flag: `production_true_zero`.
- **Barrels:** the Energy Institute's factors, 1 tonne of oil equivalent = 11.63 MWh = 7.33 barrels, so 1 TWh = 1,000,000 ÷ 11.63 × 7.33 = 630,266.6 ≈ 630,267 barrels. The common alternative, 5.8 million Btu per barrel, gives 588,300 barrels per TWh, 6.7% fewer; it would scale every oil weight by 0.933 and change no sign or ranking.
- **Price:** EIA Brent (`oil_brent`, dollars of the day) from 1987, the first year it covers. Before 1987 no Brent series is pinned, so the BP series (`oil_bp`: Arabian Light posted at Ras Tanura to 1983, Brent dated 1984–86, in 2015 dollars) is converted back to dollars of the year with the US consumer price index (Global Macro Database). Check: over 1987–2015 the converted BP series differs from EIA Brent by 0.15% on average. Kept by Sid (13 October 2026) with source flags: each edge row records its price source (`oil_price_source`) and models see the flag `price_from_bp_series`. Prices: 1970 $1.80, 1974 $11.58, 1980 $36.82, 1986 $14.44, 1987 $18.53, 2022 $100.93.
- **What it approximates:** the value of net trade in crude oil and products at the crude price. It ignores stock changes, the different energy content of crude and refined products, and refinery gains; consumption includes bunkers and, in the Energy Institute's definition, some biofuels and coal- or gas-derived liquids.
- **Russia:** from 1985 (the Energy Institute reports the USSR before; not used, Sid). Its GDP denominator starts in 1988, so its weight runs 1988–2022.

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
| owid_energy | `owid-energy-data.csv` | f8de88a4f6 | ok |
| owid_energy | `owid-energy-codebook.csv` | f8de88a4f6 | ok |
| owid_energy | `README.md` | f8de88a4f6 | ok |
| wb_gdp_current_usd | `data/gdp.csv` | 36d761dc56 | ok |
| bis_lbs | `WS_LBS_D_PUB_csv_col.zip` | 2026-07-15 | ok |
| bis_lbs | `WS_LBS_D_PUB_csv_col.csv` | 2026-07-15 | ok |
| imf_imts_s31 | `IMTS_S31_annual.csv` | 2026-10-13 | ok |
| imf_imts_s31 | `query_url.txt` | 2026-10-13 | ok |
| eia_intl | `INTL.zip` | 2026-10-13 | ok |
| eia_intl | `INTL.txt` | 2026-10-13 | ok |
| wb_wdi_gdp_2026_10 | `API_NY.GDP.MKTP.CD_DS2_en_csv_v2_512.zip` | 2026-10-13 | ok |
| wb_wdi_gdp_2026_10 | `API_NY.GDP.MKTP.CD_DS2_en_csv_v2_512.csv` | 2026-10-13 | ok |
| wb_wdi_gdp_2026_10 | `Metadata_Country_API_NY.GDP.MKTP.CD_DS2_en_csv_v2_512.csv` | 2026-10-13 | ok |
| wb_wdi_gdp_2026_10 | `Metadata_Indicator_API_NY.GDP.MKTP.CD_DS2_en_csv_v2_512.csv` | 2026-10-13 | ok |

## Coverage in one line each

- Node features: 94.2% of economy-feature-years observed; phases complete; the largest gaps are long rates, demand contributions and budget series before the 1990s (details in the missing-data report).
- Trade: 96.4% of directed pair-years observed; primary weights 92.1% (exporter's report) and 92.7% (importer's report); Russia from 1992.
- Bank: 83.4% of lender-borrower-years observed (96.1% from 1977); primary weight 82.5%.
- Oil: weight observed in 96.3% of economy-years (88.5% before the EIA extension and the true-zero class); still masked: Russia 1970–1987, Brazil 1970–1988 and Iran 1991–1992 (GDP), Japan and South Africa 2017–2022, South Africa 1970–1979.

## Decided on 13 October 2026 (Sid)

- EIA production pinned and used within the tolerance fixed beforehand; the five true-zero producers.
- The BP-based price before 1987 kept, with source flags.
- Trade: both reports as two attributes of one edge in G3.
- A fresh World Bank download, used only if it matched the pinned file exactly: it does not (below).

## Open for Sid

1. **World Bank denominators.** The fresh download fails the exact-match check (revisions above 0.1% in 853 of 1,604 shared economy-years, in 29 economies; Turkey up to 39%, Iran up to 25%, Saudi Arabia up to 12%; Brazil matches except 1989, -3.0%). Brazil 1970–1988 therefore stays masked. Options: (a) keep the pinned file and the masks (current); (b) switch every denominator to the fresh vintage, which is complete for S31 from 1970 except Russia before 1988 and moves weights by the revisions; (c) take only the missing years from the fresh vintage (two vintages mixed; a 3% step for Brazil at 1989).
2. **Japan and South Africa, oil 2017–2022**, stay masked under the stated tolerance (Japan's 2012–16 differences reach 0.115; South Africa's median is 0.131). Changing the tolerance now would be choosing it after seeing the data.
3. **Belgium and South Africa before 1997–98** use the IMF's Belgium-Luxembourg and South African Customs Union units (decided 11 October 2026); the rows are flagged.
