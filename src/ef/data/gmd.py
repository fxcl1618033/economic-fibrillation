"""Read Global Macro Database files (Stata .dta) with every single-precision column converted to double precision.

GMD stores its numbers as float32, which holds about seven significant digits: a published 11.15 is stored as
11.1499996. Each float32 value is converted to float64 through its shortest decimal form ("11.15"), which is the
value the source published whenever it had seven or fewer significant digits (rates, shares, most levels) and is
otherwise as close as float32 allows. The conversion is exact and the same on every machine, and converting back
gives the identical float32. Every log and ratio taken afterwards is computed in double precision, so results no
longer depend on how a chip rounds float32 logs (decisions of 11 October 2026).

The plain binary conversion (float32 -> float64) would instead keep the storage error at full precision and moves
four printed atlas values across a rounding boundary (Sweden's peak unemployment 11.15 would print as 11.1).

float64=False keeps float32, which is what the frozen as-run scripts did; the tests use it to show the port is
byte-identical to them.
"""
import numpy as np
import pandas as pd


def read(path, columns=None, float64=True):
    df = pd.read_stata(path, columns=columns)
    if float64:
        for c in df.select_dtypes('float32').columns:
            df[c] = df[c].to_numpy().astype(str).astype(np.float64)   # shortest decimal that round-trips to the float32
    return df
