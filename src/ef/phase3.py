"""Phase 3: run every pre-registered test and variant (docs/preregistration_S30.md, configs/runs/phase3.yaml).

    python -m ef.phase3 [--config configs/runs/phase3.yaml] [--out results]

Writes results/<sample or variant>/<convention>/<test>.json, each with the sample's economies, the settings, the seed,
the code version and the time, then results/COMPARISON.md (ef.comparison). Needs `make data` (the atlas panel).
"""
import argparse
import copy
import datetime
import json
import os
import time

from ef import channels, config
from ef.paper1 import TESTS, code_version, load_data, load_run_config

NO_HILBERT = ('mst', 'diversification', 'cross_split')        # band-pass only (amendment 1.1)
SURROGATE_PHASE = ('amplitude', 'structure', 'phase_lags', 'csd', 'bifurcation')
SWING = ('amplitude', 'diversification', 'cross_split', 'structure')


class Writer:
    def __init__(self, root):
        self.root, self.version, self.n = root, code_version(), 0

    def __call__(self, variant, convention, test, D, settings, results):
        d = os.path.join(self.root, variant, convention); os.makedirs(d, exist_ok=True)
        rec = {'sample': variant, 'economies': D.isos, 'convention': convention, 'test': test, 'settings': settings,
               'seed': settings.get('seed') if isinstance(settings, dict) else None, 'code_version': self.version,
               'run_at': datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'), 'results': results}
        json.dump(rec, open(os.path.join(d, f'{test}.json'), 'w'), indent=1, default=float); self.n += 1


def primary_tests(cfg):
    """The tests as configured, with convention P made explicit for the band-pass-only tests."""
    tests = copy.deepcopy(cfg['tests'])
    for n in NO_HILBERT: tests[n].setdefault('convention', 'P')
    return tests


def run_tests(D, cfg, tests, names, write, variant, convention, log):
    for n in names:
        t0 = time.time(); write(variant, convention, n, D, tests[n], TESTS[n](D, cfg, tests[n]))
        log(f"  {variant}/{convention}/{n} ({time.time() - t0:.1f}s)")


def run(cfg_path, out, atlas_dir, log=print):
    cfg = load_run_config(cfg_path); write = Writer(out); V = cfg['variants']; rec = cfg['recessions']
    base = primary_tests(cfg)

    def chan(D, variant, conv='P'):
        if not cfg.get('channels'): return            # not run on S31 (amendment 3.4)
        t0 = time.time()
        write(variant, conv, 'channels', D, {'panel': cfg['channels']['panel'], 'coverage_from': 1965, 'seed': cfg['channels']['seed']},
              channels.run(atlas_dir, D.isos, rec, conv))
        log(f"  {variant}/{conv}/channels ({time.time() - t0:.1f}s)")

    for sample in cfg['samples']:
        D = load_data(sample)
        log(f"{sample}: primary (P)"); run_tests(D, cfg, base, list(base), write, sample, 'P', log); chan(D, sample)
        for conv in V['conventions']:
            log(f"{sample}: convention {conv}")
            if conv == 'C': chan(D, sample, 'C'); continue
            t = {}
            for n in SURROGATE_PHASE:
                t[n] = dict(base[n], convention=conv)
                if conv == 'N' and 'window' in t[n]: t[n]['window'] = [1970, 2022]          # amendment 1.2
            if conv == 'E': t['robustness'] = dict(base['robustness'], convention='E')      # amendment 1.4
            if conv == 'N':
                for n in NO_HILBERT: t[n] = dict(base[n], convention='N', window=[1970, 2022])  # amendment 1.1
            run_tests(D, cfg, t, list(t), write, sample, conv, log)
        st = V['strict_inside_1970_2022']; log(f"{sample}: strict inside 1970-2022")
        t = {n: dict(base[n], window=st['window'], strict=st['strict']) for n in st['tests']}
        run_tests(D, cfg, t, list(t), write, f'{sample}_strict', 'P', log)
        sw = V['gmd_growth_swap']; log(f"{sample}: GMD growth for {sw['economies']} {sw['years']}")
        Dg = load_data(sample, gmd_growth=sw); run_tests(Dg, cfg, base, sw['tests'], write, f'{sample}_gmd_growth', 'P', log)

    b0 = V.get('base', 'S30')
    for iso in V['drop_one_added']:
        log(f"{b0} without {iso}: every test (P)")
        D = load_data(b0, drop=[iso]); run_tests(D, cfg, base, list(base), write, f'{b0}_minus_{iso}', 'P', log); chan(D, f'{b0}_minus_{iso}')
    for drops in V['swing_size']:
        if len(drops) == 1 and drops[0] in V['drop_one_added']: continue                   # already run with every test
        name = f'{b0}_minus_' + '_'.join(drops); log(f"{name}: swing-size tests (P)")
        run_tests(load_data(b0, drop=drops), cfg, base, SWING, write, name, 'P', log)
    le = V.get('late_entry')
    if le:                                                                                  # amendment 3.5
        log(f"{le['name']}: {le['economy']} from {le['from']} (P, circular shift only)")
        t = {n: dict(base[n]) for n in le['tests']}
        if 'amplitude' in t: t['amplitude']['surrogates'] = 0
        run_tests(load_data(b0, late={le['economy']: le['from']}), cfg, t, le['tests'], write, le['name'], 'P', log)
    return write.n


def main(argv=None):
    root = config.repo_root()
    ap = argparse.ArgumentParser(); ap.add_argument('--config', default=os.path.join(root, 'configs/runs/phase3.yaml'))
    ap.add_argument('--out', default=os.path.join(root, 'results')); ap.add_argument('--atlas', default=os.path.join(config.load()['paths']['build'], 'data/atlas'))
    args = ap.parse_args(argv)
    if not os.path.exists(os.path.join(args.atlas, 'panel.csv')): raise SystemExit("run make data first (the atlas panel)")
    t0 = time.time(); n = run(args.config, args.out, args.atlas)
    print(f"wrote {n} result files under {args.out} in {time.time() - t0:.0f}s")
    from ef import comparison
    print(f"wrote {comparison.write(args.out)}")


if __name__ == '__main__':
    main()
