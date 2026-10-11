"""Build every derived data file from the pinned sources, then check it against the stored files.

    python -m ef.data.build [--out build/data]

GMD values are read as float64 (ef.data.gmd); --float32 reproduces the as-run scripts' precision byte for byte.

1. verify the sha256 of every pinned file the build reads (stop if any differs);
2. channel anatomy of the 26 (ef.data.channels)          -> panel26_results.json
3. atlas panel, global factors, statistics, sync (ef.data.atlas) -> atlas/panel.csv, global.csv, meta.json, stats.json, sync.json
4. Maddison panels for S26 and S30 (ef.data.maddison)     -> maddison_S26.csv, maddison_S30.csv
5. compare 2-3 with the stored files (EXACT or MATCH, src/ef/repro.py) and write BUILD.md; exit 1 on DIFFERS.
"""
import argparse
import hashlib
import os
import sys
import warnings

import yaml

from ef import config
from ef.data import atlas, channels, maddison
from ef.repro import compare

USED = ['maddison', 'gmd', 'pwt', 'oil_bp', 'oil_brent']


def sha256(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''): h.update(chunk)
    return h.hexdigest()


def verify(ids=USED):
    """Check the sha256 of every file of the given sources against data/sources.yaml."""
    bad = []
    for s in yaml.safe_load(open(config.load()['paths']['sources']))['sources']:
        if s['id'] not in ids: continue
        for f in s['files']:
            p = config.raw_file(s['id'], f['path'])
            if not os.path.exists(p) or sha256(p) != f['sha256']: bad.append(f"{s['id']}: {f['path']}")
    if bad: sys.exit("pinned files missing or changed (run make fetch):\n  " + "\n  ".join(bad))


def main(argv=None):
    cfg = config.load()
    ap = argparse.ArgumentParser(); ap.add_argument('--out', default=os.path.join(cfg['paths']['build'], 'data'))
    ap.add_argument('--quiet', action='store_true')
    ap.add_argument('--float32', action='store_true', help='read GMD as float32, as the frozen as-run scripts did')
    args = ap.parse_args(argv); out = args.out; v = not args.quiet; f64 = not args.float32
    os.makedirs(os.path.join(out, 'atlas'), exist_ok=True)
    warnings.filterwarnings('ignore', message='invalid value encountered in log')   # log of zero or negative values -> NaN, as in the as-run scripts

    verify(); print("pinned sources verified")
    p26 = os.path.join(out, 'panel26_results.json')
    channels.run(p26, verbose=v, float64=f64); print(f"wrote {p26}")
    A = os.path.join(out, 'atlas')
    atlas.build_panel(A, p26, verbose=v, float64=f64); atlas.build_stats(A, verbose=v); atlas.build_sync(A, verbose=v, float64=f64)
    print(f"wrote {A}/panel.csv, global.csv, meta.json, stats.json, sync.json")
    for s, p in maddison.write(out).items(): print(f"wrote {p}")

    root = cfg['root']; checksums = yaml.safe_load(open(cfg['paths']['sources']))['derived_checksums']
    rows = [('panel26_results.json', p26, os.path.join(root, 'paper1/results/panel26_results.json'))]
    rows += [(f'atlas/{f}', os.path.join(A, f), os.path.join(root, 'atlas', f)) for f in ('panel.csv', 'global.csv', 'meta.json', 'stats.json', 'sync.json')]
    rep = ["# Data build", "", "Each derived file against the stored copy (made on Linux x86). EXACT: within 1e-9 (byte-identical where noted); "
           "MATCH: floating-point rounding only, no p-value changed (rules in `src/ef/repro.py`).", "", "| File | Result | Note |", "|---|---|---|"]
    bad = []
    for name, new, old in rows:
        same = sha256(new) == checksums.get(name, sha256(old))
        t = compare(new, old); st = 'EXACT' if same else t.status()
        rep.append(f"| {name} | {st} | {'byte-identical' if same else t.note()} |")
        if st == 'DIFFERS': bad.append(name)
    open(os.path.join(out, 'BUILD.md'), 'w').write("\n".join(rep) + "\n")
    print("\n".join(rep))
    if bad: sys.exit(f"derived files not reproduced: {bad}")


if __name__ == '__main__':
    main()
