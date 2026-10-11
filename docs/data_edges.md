# Edge data for the GNN — what the two new sources hold

11 October 2026. Both files are pinned in `data/sources.yaml` (`downloads`) and verified by `make fetch`. Nothing is
built on them yet; this note records what G0 must handle. Counts are for the 30 S30 economies (870 directed pairs).

## Bank lending: BIS Locational Banking Statistics

The end-December 2025 release (30 April 2026; bulk file dated 10 June 2026, data 1977-Q4 to 2025-Q4), downloaded by
Sid on 15 July. Cross-border claims of banks located
in a reporting country on residents of a counterparty country, quarterly stocks in millions of US dollars.

| Year-end | Directed pairs with a value | Economies reporting as lenders |
|---|---|---|
| 1977 | 262 | 10 |
| 1990 | 315 | 11 |
| 2000 | 315 | 12 |
| 2007 | 470 | 18 |
| 2020 | 568 | 21 |

- **No bank data before end-1977.** The 1975 recession has no bank edges.
- **Main edge set (Sid's decision):** the 10 lenders reporting since 1977 — France, Belgium, Sweden, Switzerland,
  Germany, Denmark, the Netherlands, the United States, the United Kingdom and Japan. The expanding set is a
  sensitivity check only, because its growth comes from new reporters, not from more banking.
- **Later lenders:** Finland 1983, Australia 1997, Brazil 2002, Greece and Mexico 2003, South Korea 2005, Austria and
  Canada 2007, South Africa 2009, Spain 2012-Q2, Italy 2014-Q4. Italy and Spain report to the BIS from 1977 and 1983, but their
  country-by-country detail is public only from these dates.
- **Never lenders:** China, India, Indonesia, Iran, Norway, Portugal, Saudi Arabia, Thailand and Turkey. Their banks'
  lending is invisible; their borrowing from reporters is seen.
- **Suppressed cells are blank, not zero.** Decide explicitly how to treat them before building edges.
- **Filters** that select the series: in `data/sources.yaml` (`read_with`).

## Trade: IMF International Trade in Goods by partner country (IMTS)

The successor to Direction of Trade Statistics, retrieved through the IMF's SDMX 3.0 API on 11 October 2026. Annual
goods exports (FOB) and imports (CIF) in US dollars, 1948–2025, with the world as a partner for totals.

| Year | Pairs with reported exports | Pairs with partner-reported imports | Either |
|---|---|---|---|
| 1960 | 714 | 740 | 795 |
| 1970 | 756 | 764 | 834 |
| 1975 | 787 | 819 | 856 |
| 1982 | 850 | 852 | 858 |
| 1991 | 850 | 851 | 859 |
| 2000 onwards | 868–869 | 867–870 | 868–870 |

- **Mirror flows fill gaps.** Economy i's exports to j can be read from i's own report or from j's imports from i.
  The two differ by freight and insurance (CIF is larger than FOB) and by reporting errors; G0 should prefer one and
  use the other only to fill gaps, and record which.
- **Missing is not always zero.** In 1970 the missing pairs mostly involve China (16 of 36). Many are true zeros,
  such as US–China trade before 1972, not unreported values.
- **Belgium** is reported as Belgium-Luxembourg (code TX126) up to 1996 and as Belgium from 1997, so its links include
  Luxembourg before 1997: a level break.
- **South Africa** reports as the South African Common Customs Area (TX198: with Botswana, Lesotho, Namibia and
  Eswatini) up to 1997 and as South Africa from 1998. As a partner of others it is always South Africa.
- **Estimates:** 1,346 of 131,093 rows are IMF estimates (STATUS `e`).
- **Revisions:** the IMF revises these data, so a new download would differ. The pinned copy lives in `data/raw/` and,
  compressed, in `data/archive/imf_imts/` (committed), from which `make fetch` restores it.

## Oil

Oil exposure links each economy to the world node (Sid's decision), as net oil exports relative to GDP. No source is
pinned for it yet; that is a G0 task.

## Still to decide in G0

- Normalisation of each edge type: the share of the reporter's total (row shares) or the partner's share of GDP, as
  `docs/specs/BIS_download_spec.md` describes.
- Annual timing of bank stocks (year-end, or the mean of four quarters).
- Whether to smooth trade weights over a few years, as GVAR studies do, so one odd year does not move an edge.
