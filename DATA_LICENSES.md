# Data: sources, licences and what is in this repository

Every source is pinned, with checksums, in `data/sources.yaml`; `python3 tools/fetch_data.py` fetches and verifies
them into `data/raw/`, which is not part of the repository. Three raw downloads are kept here in compressed form
(`data/archive/`) because their providers serve only the latest vintage. Everything else committed here is built by
the project's own code.

| Source | Licence or terms | In this repository |
|---|---|---|
| Maddison Project Database 2023 (Bolt and van Zanden 2024) | CC BY 4.0 | No raw file. Phases, r(t) and every Paper 1 statistic are built from it |
| Global Macro Database, 2026 release (Müller, Xu, Lehbib and Chen 2025) | GMD Research Use Terms (non-commercial; no re-hosting without the authors' written approval; work built on it keeps the same terms) | **No GMD series.** `atlas/panel.csv` and `atlas/global.csv` are rebuilt by `make data` or `make asrun` from the pinned release and are not distributed. Statistics and figures built on GMD are under CC BY-NC-SA 4.0 (list below) |
| Penn World Table 10.01 (Feenstra, Inklaar and Timmer 2015) | CC BY 4.0 | No raw file; used inside the atlas build |
| IMF, International Trade in Goods by partner country (IMTS) | IMF terms of use (attribution; no alteration; commercial reuse needs the IMF's permission) | Raw download in `data/archive/imf_imts/` and `data/archive/imf_imts_s31/` (see the IMF note below) |
| BIS Locational Banking Statistics | BIS terms of use for statistics (attribution; no implied endorsement) | No raw file (121 MB, kept outside git). Only lists of gaps in `gnn/G0/` (see the BIS note below) |
| U.S. Energy Information Administration, International Energy Statistics | US public domain | Raw bulk file in `data/archive/eia_intl/` |
| World Bank, World Development Indicators (GDP, current US dollars) | CC BY 4.0 | Raw download in `data/archive/wb_wdi_gdp/`; `paper1/data/gdp_panel_*.csv`; `gnn/G0/wb_vintage_comparison.csv.gz` |
| Our World in Data, energy dataset (legacy release) | OWID's own work CC BY 4.0; the Energy Institute and Shift Data Portal series it carries keep their own terms | Not distributed |
| BP Statistical Review crude oil price (OWID archive) and EIA Brent price (datasets/oil-prices) | BP: no licence stated; EIA: public domain, package PDDL | Only as standardized yearly changes inside results |
| Jordà–Schularick–Taylor Macrohistory Database | Free for non-commercial use; its terms forbid commercial resale | No raw file; only statistics (`paper1/results/crisis_dating_results.json`) and the category 03 history figures built from it |

## Outputs built on the Global Macro Database (CC BY-NC-SA 4.0)

Licensed under CC BY-NC-SA 4.0 (https://creativecommons.org/licenses/by-nc-sa/4.0/), following the GMD's terms; each
folder has a `LICENSE.md` note:

- `atlas/stats.json`, `atlas/sync.json`, `atlas/meta.json` (the atlas statistics and data repairs);
- `figures/07_inside_economies/` and its book `figures/compiled/EF_Figures_07_Inside_the_Economies.pdf`, with the two
  source images `figures/_sources/analysis/usjp_inside.png` and `anatomy26.png`;
- `results/S26_gmd_growth/`, `results/S30_gmd_growth/`, `results/S31_gmd_growth/`;
- `paper1/results/panel26_results.json` and `paper1/results/printed/usjp_output.txt` (the channel anatomy).

Please cite the database when you reuse them: Müller, K., Xu, C., Lehbib, M. and Chen, Z. (2025). The Global Macro
Database. NBER Working Paper 33714.

## IMF note

Source: International Monetary Fund, International Trade in Goods (by partner country) (IMTS), data.imf.org, through
the SDMX 3.0 API (https://api.imf.org/external/sdmx/3.0/data/dataflow/IMF.STA/IMTS; the exact queries are in
`query_url.txt`), retrieved 11 and 13 October 2026. The files in `data/archive/imf_imts*/` are the downloads as
received, compressed with gzip and otherwise unaltered. Material transformation: `gnn/G1/trade_network.npz` divides
these exports by World Bank GDP (current US dollars) and averages the exporter's and the importer's reports. Use is
subject to the IMF's terms (https://www.imf.org/en/About/copyright-and-terms); for commercial reuse ask the IMF
(copyright@imf.org).

## BIS note

Source: Bank for International Settlements, Locational Banking Statistics, data.bis.org (bulk file of the end-December
2025 release, dated 10 June 2026). The bank-lending edges are built from it on the user's machine and are not in this
repository; `gnn/G0/edge_gaps_bank.csv.gz` lists only where those edges are missing. Use of BIS statistics is subject
to the BIS terms (https://www.bis.org/terms_statistics.htm); the BIS does not endorse this work.
