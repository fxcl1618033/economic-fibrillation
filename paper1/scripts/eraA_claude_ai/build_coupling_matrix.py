"""
build_coupling_matrix.py
========================
Turns the raw BIS Locational Banking Statistics file into a directed coupling
matrix K_ij for the networked Kuramoto model.

    K_ij  =  strength with which economy j influences economy i
          =  (claims of banks located in j on borrowers in i), normalised

Rows    = borrowers (all 26 economies)
Columns = lenders   (the 20 with public bilateral data)

USAGE
-----
  # 1. Look at the file first — BIS renames columns between portal versions.
  python3 build_coupling_matrix.py --file <bis_file.csv> --inspect

  # 2. Set the FILTERS dict below to match what --inspect printed, then:
  python3 build_coupling_matrix.py --file <bis_file.csv> --year 2007 --norm gdp

NOTE: the FILTERS below are written from the documented LBS dimensions, but BIS
has changed column naming (data.bis.org vs the old warehouse). ALWAYS run
--inspect first and reconcile. The script will tell you which filters matched
nothing rather than silently returning an empty matrix.
"""

import argparse, sys
import numpy as np
import pandas as pd

# ------------------------------------------------------------------ your panel
LENDERS_2008 = ['US','GB','DE','FR','IT','JP','CA','ES','AU','KR','MX','NL','SE',
                'CH','BE','AT','DK','FI','GR']                      # 19
LENDERS_2020 = LENDERS_2008 + ['ZA']                                # 20
BORROWERS    = LENDERS_2020 + ['IN','ID','TR','NO','PT','TH']       # 26

ISO2_TO_NAME = {
 'US':'United States','GB':'United Kingdom','DE':'Germany','FR':'France','IT':'Italy',
 'JP':'Japan','CA':'Canada','ES':'Spain','AU':'Australia','KR':'South Korea',
 'MX':'Mexico','NL':'Netherlands','SE':'Sweden','CH':'Switzerland','BE':'Belgium',
 'AT':'Austria','DK':'Denmark','FI':'Finland','GR':'Greece','ZA':'South Africa',
 'IN':'India','ID':'Indonesia','TR':'Turkey','NO':'Norway','PT':'Portugal','TH':'Thailand',
}

# ------------------------------------------------------------------ FILTERS
# Reconcile these against --inspect output. Value = what to keep.
# Set a value to None to skip that filter.
FILTERS = {
 'FREQ':          'Q',      # quarterly
 'L_MEASURE':     'S',      # S = amounts outstanding (stocks). NOT flows.
 'L_POSITION':    'C',      # C = claims (assets). 'L' = liabilities (mirror trick)
 'L_INSTR':       'A',      # A = all instruments
 'L_DENOM':       'TO1',    # all currencies
 'L_CURR_TYPE':   'A',      # all currency types
 'L_CP_SECTOR':   'A',      # A = all sectors. Use 'B' for banks-only robustness run
 'L_PARENT_CTY':  '5J',     # all parent countries (locational BY RESIDENCE)
 'L_REP_BANK_TYPE': 'A',    # all reporting banks
}
COL_REPORTER   = 'L_REP_CTY'      # the lender  -> becomes the COLUMN
COL_COUNTERPTY = 'L_CP_COUNTRY'   # the borrower -> becomes the ROW


def inspect(path):
    """Print structure so you can reconcile FILTERS."""
    df = pd.read_csv(path, nrows=5000, low_memory=False)
    print("=" * 70)
    print("COLUMNS")
    print("=" * 70)
    for c in df.columns:
        print("  ", c)
    print()
    dim_cols = [c for c in df.columns if not _is_period(c)]
    per_cols = [c for c in df.columns if _is_period(c)]
    print(f"dimension columns: {len(dim_cols)}   period columns: {len(per_cols)}")
    if per_cols:
        print(f"period range: {per_cols[0]}  ->  {per_cols[-1]}")
    print()
    print("=" * 70)
    print("UNIQUE VALUES per dimension column (first 5k rows)")
    print("=" * 70)
    for c in dim_cols:
        u = df[c].dropna().unique()
        show = ", ".join(map(str, u[:12])) + (" ..." if len(u) > 12 else "")
        print(f"  {c:22s} ({len(u):>4} vals): {show}")
    print()
    print("Now set FILTERS at the top of this script to match, then rerun without --inspect.")


def _is_period(c):
    c = str(c)
    return ("-Q" in c) or (c[:4].isdigit() and len(c) in (4, 7))


def build(path, year, norm, lenders):
    print(f"loading {path} ... (large file, be patient)")
    df = pd.read_csv(path, low_memory=False)
    print(f"  raw rows: {len(df):,}")

    # --- apply filters, loudly ---
    for col, val in FILTERS.items():
        if val is None:
            continue
        if col not in df.columns:
            print(f"  ! filter column '{col}' NOT in file — skipping (reconcile with --inspect)")
            continue
        before = len(df)
        df = df[df[col].astype(str) == str(val)]
        print(f"  filter {col} == {val!r}: {before:,} -> {len(df):,}")
        if len(df) == 0:
            sys.exit(f"\nERROR: filter {col}=={val!r} removed everything. "
                     f"Run --inspect and fix FILTERS.")

    # --- find the period column for this year (Q4 snapshot) ---
    per_cols = [c for c in df.columns if _is_period(c)]
    target = None
    for cand in (f"{year}-Q4", f"{year}Q4", str(year)):
        if cand in per_cols:
            target = cand
            break
    if target is None:
        sys.exit(f"ERROR: no period column for {year}. Available near it: "
                 f"{[c for c in per_cols if str(year) in str(c)]}")
    print(f"  using period column: {target}")

    # --- pivot to borrower x lender ---
    sub = df[[COL_COUNTERPTY, COL_REPORTER, target]].copy()
    sub[target] = pd.to_numeric(sub[target], errors="coerce")
    sub = sub.dropna(subset=[target])
    mat = sub.pivot_table(index=COL_COUNTERPTY, columns=COL_REPORTER,
                          values=target, aggfunc="sum")

    # --- restrict to our panel ---
    rows = [b for b in BORROWERS if b in mat.index]
    cols = [l for l in lenders if l in mat.columns]
    missing_rows = [b for b in BORROWERS if b not in mat.index]
    missing_cols = [l for l in lenders if l not in mat.columns]
    if missing_rows:
        print(f"  ! borrowers absent from data: {missing_rows}")
    if missing_cols:
        print(f"  ! lenders absent from data:   {missing_cols}")
    K = mat.loc[rows, cols].astype(float)

    # suppressed cells are blank, NOT zero — keep as NaN, report them
    n_nan = int(K.isna().sum().sum())
    print(f"  matrix {K.shape[0]}x{K.shape[1]}  |  suppressed/missing cells: {n_nan}")

    # no self-coupling
    for c in K.columns:
        if c in K.index:
            K.loc[c, c] = np.nan

    # --- normalise ---
    if norm == "raw":
        Kn = K
    elif norm == "row":
        Kn = K.div(K.sum(axis=1), axis=0)          # each borrower's mix sums to 1
    elif norm == "gdp":
        gdp = _load_gdp(year)
        miss = [r for r in K.index if r not in gdp]
        if miss:
            print(f"  ! no GDP for {miss} — those rows will be NaN")
        Kn = K.div(pd.Series({r: gdp.get(r, np.nan) for r in K.index}), axis=0)
    else:
        sys.exit(f"unknown norm: {norm}")

    out = f"K_matrix_{year}_{norm}.csv"
    Kn.rename(index=ISO2_TO_NAME, columns=ISO2_TO_NAME).to_csv(out)
    print(f"\nwrote {out}   (rows = borrowers, cols = lenders)")

    _heatmap(Kn, year, norm)
    _summary(Kn)
    return Kn


def _load_gdp(year):
    """GDP (current US$) for the normalisation, from the panel we already built."""
    try:
        g = pd.read_csv("gdp_panel_long_1970_2023.csv")
    except FileNotFoundError:
        sys.exit("ERROR: gdp_panel_long_1970_2023.csv not found — needed for --norm gdp")
    g = g[g.Year == year]
    name_to_iso = {v: k for k, v in ISO2_TO_NAME.items()}
    return {name_to_iso[r.Country]: float(r.GDP_current_USD)
            for r in g.itertuples() if r.Country in name_to_iso}


def _heatmap(K, year, norm):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(10, 9))
    d = K.rename(index=ISO2_TO_NAME, columns=ISO2_TO_NAME)
    v = np.log10(d.values + 1e-12) if norm == "raw" else d.values
    im = ax.imshow(v, cmap="magma", aspect="auto")
    ax.set_xticks(range(d.shape[1])); ax.set_xticklabels(d.columns, rotation=90, fontsize=7)
    ax.set_yticks(range(d.shape[0])); ax.set_yticklabels(d.index, fontsize=7)
    ax.set_xlabel("lender  (banks located in)"); ax.set_ylabel("borrower  (claims on)")
    ax.set_title(f"BIS coupling map K_ij — {year}, norm={norm}", loc="left")
    fig.colorbar(im, ax=ax, fraction=0.03, pad=0.02)
    fig.savefig(f"K_matrix_{year}_{norm}.png", bbox_inches="tight", dpi=140)
    plt.close(fig)
    print(f"wrote K_matrix_{year}_{norm}.png")


def _summary(K):
    print("\n--- who transmits most (column sums = total lending out) ---")
    out = K.sum(axis=0).sort_values(ascending=False)
    for k, v in out.head(6).items():
        print(f"   {ISO2_TO_NAME.get(k,k):18s} {v:.3f}")
    print("--- who is most exposed (row sums = total borrowing in) ---")
    inn = K.sum(axis=1).sort_values(ascending=False)
    for k, v in inn.head(6).items():
        print(f"   {ISO2_TO_NAME.get(k,k):18s} {v:.3f}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True, help="raw BIS LBS csv")
    ap.add_argument("--inspect", action="store_true", help="print structure and exit")
    ap.add_argument("--year", type=int, default=2007)
    ap.add_argument("--norm", default="gdp", choices=["raw", "row", "gdp"])
    a = ap.parse_args()

    if a.inspect:
        inspect(a.file)
    else:
        lenders = LENDERS_2008 if a.year <= 2008 else LENDERS_2020
        build(a.file, a.year, a.norm, lenders)
