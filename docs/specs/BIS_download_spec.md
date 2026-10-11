# BIS Locational Banking Statistics — Download Spec
### For the coupling map (K_ij) in the Economic Fibrillation paper

---

## 1. What you are getting

A **directed connection map**: how much banks located in country *j* have lent to
borrowers in country *i*. This becomes the coupling strength `K_ij` in the
networked Kuramoto model — the road the crisis travels along.

**Dataset:** BIS **Locational Banking Statistics (LBS), by residence**
**Home:** https://data.bis.org/topics/LBS
**Cost:** free
**Citation:** Bank for International Settlements, *Locational Banking Statistics*
(LBS), by residence. Accessed [date]. https://data.bis.org/topics/LBS

---

## 2. Two ways to get it

### Option A — bulk file (recommended)
On the BIS Data Portal, find the **LBS bulk download** (a zipped CSV of the full
dataset, "WS_LBS_D_PUB"). One file, everything in it, you filter locally with
`build_coupling_matrix.py`. Large (hundreds of MB unzipped) but done once.

### Option B — interactive query
BIS Data Portal → LBS → tables & dashboards → build a query with the filters in
§3 → export CSV. Smaller file, but you must re-query if you change anything.

**Take Option A.** You will want to re-slice this several times.

---

## 3. The exact filters

| Dimension | Choose | Why |
|---|---|---|
| Measure / position type | **Amounts outstanding (stocks)**, not flows | You want the standing exposure = the strength of the link |
| Balance sheet position | **Claims** (assets) | "who lent to whom". Also grab **Liabilities** if you later want the mirror trick |
| Instrument | **All instruments** | Loans + debt securities; the full pipe |
| Currency | **All currencies (TO1)** | Don't restrict to USD on pass one |
| Counterparty sector | **All sectors** (primary)<br>**Banks only** (robustness) | All sectors = total exposure. Bank-only = pure interbank contagion — worth a second run |
| Reporting country (lender) | Your 20 (see §4) | These are the rows |
| Counterparty country (borrower) | Your 26 | These are the columns |
| Frequency | **Quarterly** → keep **Q4 only** | Q4 snapshot matches your annual GDP data |
| Period | **1977 → latest** | You'll only really use ~1997 onward |

---

## 4. The country lists (verified against the BIS reporter list)

### Lenders — rows (20 usable)
United States, United Kingdom, Germany, France, Italy, Japan, Canada, Spain,
Australia, South Korea, Mexico, Netherlands, Sweden, Switzerland, Belgium,
Austria, Denmark, Finland, Greece, South Africa

**For the 2008 analysis, drop South Africa** (its LBS data starts Q3 2009 —
after the crisis). → **19 lenders for GFC, 20 for COVID.**

### Borrowers — columns (all 26)
All of your original panel. Non-reporters still appear as counterparties.

### Excluded as lenders (state this in Methods)
| Economy | Reason |
|---|---|
| Thailand | Not an LBS reporting country |
| India | Reports; bilateral detail not published |
| Indonesia | Reports; bilateral detail not published |
| Turkey | Reports; bilateral detail not published |
| Norway | Reports; bilateral detail not published |
| Portugal | Reports; bilateral detail not published |

### First-available quarter (why 2008/2020 and not the oil shocks)
- Q4 1977: US, UK, Germany, France, Italy, Japan, Canada, Netherlands, Sweden,
  Switzerland, Belgium, Austria, Denmark
- Q4 1983: Spain, Finland
- Q4 1997: Australia
- Q4 2003: Mexico, Greece
- Q1 2005: South Korea
- Q3 2009: South Africa

---

## 5. Traps to watch for (this data is messy)

1. **Breaks in series.** When a new country joins the reporting population, totals
   jump for reasons that are not economics. The BIS flags these. Do not read a
   break as a shock.
2. **Currency valuation.** Stocks are in USD. A falling euro shrinks reported
   euro-area claims without any lending changing. If this bites, use the BIS's
   **exchange-rate-adjusted changes**, or normalise (see §6).
3. **Intragroup positions.** LBS is unconsolidated — it includes a bank lending to
   its own foreign branch. That is real funding, but it inflates links between
   financial centres (UK, Luxembourg, Switzerland). Note it as a limitation.
4. **Financial centres.** The UK and Switzerland look enormously connected partly
   because they are booking hubs, not because their economies are. Expect it.
5. **Confidentiality suppression.** Even among the public 31, individual cells can
   be suppressed. They appear blank, not zero. Do not fill with 0 silently.

---

## 6. Turning claims into K_ij (normalisation)

Raw claims are in billions of USD and scale with country size — the US will
dominate everything. Pick a normalisation and justify it:

- **`raw`** — claims as-is. Only for a first look.
- **`row`** — each borrower's exposures sum to 1. Answers "where does *i*'s
  foreign funding come from?" Good default for a spreading model.
- **`gdp`** — claims of *j* on *i*, divided by *i*'s GDP. Answers "how much of
  *i*'s economy is funded by *j*?" **Most economically meaningful** — and you
  already have the GDP panel to do it.

`build_coupling_matrix.py` implements all three. Start with `gdp`, check `row`.

---

## 7. Once you have the file

```bash
python3 build_coupling_matrix.py --file WS_LBS_D_PUB_csv_col.csv --inspect
# read the printed column names, set the FILTER codes at the top of the script
python3 build_coupling_matrix.py --file WS_LBS_D_PUB_csv_col.csv --year 2007 --norm gdp
```

Output: `K_matrix_<year>.csv` — a 26×26 (rows = borrower, cols = lender) matrix
ready to drop into the networked Kuramoto model, plus a heatmap to eyeball it.

---

## 8. The Methods sentence you will write

> The coupling network is constructed from BIS Locational Banking Statistics
> (claims, amounts outstanding, all instruments and currencies, Q4 snapshots).
> Bilateral positions are published for 31 of the 48 LBS reporting countries;
> accordingly the lender set is restricted to the 19 (2008) / 20 (2020) economies
> in our panel with public bilateral data, while all 26 economies are retained as
> borrowers. Thailand is not an LBS reporter; India, Indonesia, Turkey, Norway
> and Portugal report but their bilateral detail is not published. We verify that
> the Kuramoto order parameter computed on the lender subsample is
> indistinguishable from the full 26-economy panel (see Robustness).
