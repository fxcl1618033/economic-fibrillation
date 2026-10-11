"""Maddison 2023 panels for the samples in configs/default.yaml: real GDP per capita and population, 1950-2022.

No interpolation and no splicing: an economy enters a sample only if both series are complete for every year
(the inclusion rule; open issue 17, decided 11 October 2026). A gap raises an error instead of being filled.
"""
import os

import numpy as np
import pandas as pd
import pyreadr

from ef import config


def load(path=None):
    """The whole Maddison table: ISO, year, gdppc (2011 int-$), pop (thousands)."""
    md = pyreadr.read_r(path or config.raw_file('maddison'))['MaddisonData']
    md['year'] = md['year'].astype(int)
    return md


def gaps(md, iso, years=None):
    """Years in the span with no gdppc or no pop, for one economy."""
    y0, y1 = years or config.load()['years']
    d = md[(md.ISO == iso) & md.year.between(y0, y1)].set_index('year').reindex(range(y0, y1 + 1))
    return {'gdppc': [int(y) for y in d.index[d.gdppc.isna()]], 'pop': [int(y) for y in d.index[d['pop'].isna()]]}


def panel(sample, md=None, years=None):
    """Long panel (year, iso, gdppc, pop) for a sample, in the sample's order. Raises if any year is missing."""
    md = load() if md is None else md
    y0, y1 = years or config.load()['years']
    isos = config.sample(sample) if isinstance(sample, str) else list(sample)
    bad = {i: g for i in isos if any((g := gaps(md, i, (y0, y1))).values())}
    if bad: raise ValueError(f"incomplete Maddison series (inclusion rule): {bad}")
    rows = [md[(md.ISO == i) & md.year.between(y0, y1)].sort_values('year') for i in isos]
    out = pd.concat(rows, ignore_index=True)[['year', 'ISO', 'gdppc', 'pop']].rename(columns={'ISO': 'iso'})
    out[['gdppc', 'pop']] = out[['gdppc', 'pop']].astype(np.float64)
    return out


def wide(long, var='gdppc'):
    """Year x economy table of one variable, columns in sample order."""
    return long.pivot(index='year', columns='iso', values=var)[list(dict.fromkeys(long.iso))]


def write(out_dir, samples=('S26', 'S30'), md=None):
    """Write maddison_<sample>.csv for each sample; return their paths."""
    md = load() if md is None else md
    paths = {}
    for s in samples:
        p = os.path.join(out_dir, f'maddison_{s}.csv'); panel(s, md).to_csv(p, index=False); paths[s] = p
    return paths


def read(path):
    """Read a panel written by write(). float_precision='round_trip' returns exactly the values written; pandas'
    default reader can be off in the last digit (up to 1.5e-11 here), enough to break a 1e-12 comparison."""
    return pd.read_csv(path, float_precision='round_trip')
