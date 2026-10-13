"""Follow-up checks Sid asked for after reading the Phase 3 results. Not pre-registered: each is labelled so, and
none changes a pre-registered result.

    python -m ef.followup [--out results]

1. Leave-one-crisis-out for the early-warning trends (registry F1, F2), 11 October 2026: which recessions carry the
   rise in the variance of r(t)? Same settings, seed and surrogates as the Phase 3 test (configs/runs/phase3.yaml,
   convention P, windows from 1962), on S26 and S30.

Writes results/followup/<sample>/P/<test>.json and results/FOLLOWUP.md.
"""
import argparse
import os

from ef import config
from ef.paper1 import load_data, load_run_config, run_csd_by_event
from ef.phase3 import Writer, primary_tests

LABELS = {'all': 'All recessions used (as Phase 3)'}


def _label(s):
    if s in LABELS: return LABELS[s]
    kind, ev = s.split('_', 1); ev = ev.replace('_', ' and ')
    return f"{ev} alone" if kind == 'only' else f"Without {ev}"


def _order(sets):
    """All, then each event alone, then each left out, then the pairs."""
    keys = list(sets)
    single = lambda k: k.count('_') == 1 and k != 'all'
    return ['all'] + [k for k in keys if k.startswith('only_') and single(k)] + [k for k in keys if k.startswith('without_') and single(k)] \
        + [k for k in keys if not single(k) and k != 'all']


def report(res):
    """results/FOLLOWUP.md from {sample: run_csd_by_event result}."""
    S = list(res); L = ["# Follow-up checks (not pre-registered)", "",
                        "Asked for by Sid after reading the Phase 3 results. Exploratory: these p-values are raw, not part of any",
                        "pre-registered family, and change no pre-registered result. Floors: 5,000 surrogates give p ≥ 0.0002.", "",
                        "## 1. Which recessions carry the rise in the variance of r(t)? (registry F2)", "",
                        "Kendall-type trend τ of the variance (and lag-1 autocorrelation) of r(t)'s fluctuations over the eight years",
                        "before each recession, averaged over the recessions in each row; one-sided p (rising) against the same 5,000",
                        "surrogates as Phase 3 (seed 101), convention P, 15-year windows from 1962. The 1975 recession has no defined",
                        "pre-window; 1982's is partly defined (" + ', '.join(f"{s}: {res[s]['pre_crisis_events'].get(1982, '—')}" for s in S) + " years).", "",
                        "| Recessions | " + " | ".join(f"{s} variance τ (p)" for s in S) + " | " + " | ".join(f"{s} AR(1) τ (p)" for s in S) + " |",
                        "|---|" + "---|" * (2 * len(S))]
    for k in _order(res[S[0]]['sets']):
        cells = [f"{res[s]['sets'][k]['tau_var']:+.3f} ({res[s]['sets'][k]['p_var']:.4f})" for s in S] \
            + [f"{res[s]['sets'][k]['tau_ar1']:+.3f} ({res[s]['sets'][k]['p_ar1']:.4f})" for s in S]
        L.append(f"| {_label(k)} | " + " | ".join(cells) + " |")
    L += ["", "Source: `results/followup/<sample>/P/csd_by_event.json` (`ef.paper1.run_csd_by_event`).", ""]
    return "\n".join(L)


def run(cfg_path, out, log=print, samples=None):
    cfg = load_run_config(cfg_path); t = primary_tests(cfg)['csd']; write = Writer(os.path.join(out, 'followup')); res = {}
    for sample in samples or cfg['samples']:
        D = load_data(sample); res[sample] = run_csd_by_event(D, cfg, t)
        write(sample, 'P', 'csd_by_event', D, t | {'not_preregistered': 'leave-one-crisis-out, asked for by Sid on 11 October 2026'}, res[sample])
        log(f"  followup/{sample}/P/csd_by_event")
    path = os.path.join(out, 'FOLLOWUP.md'); open(path, 'w').write(report(res)); return path


def main(argv=None):
    root = config.repo_root()
    ap = argparse.ArgumentParser(); ap.add_argument('--config', default=os.path.join(root, 'configs/runs/phase3.yaml'))
    ap.add_argument('--out', default=os.path.join(root, 'results'))
    ap.add_argument('--samples', nargs='+', default=['S26', 'S30', 'S31'], help='S31 added 13 October 2026 (amendment 3)')
    args = ap.parse_args(argv)
    print(f"wrote {run(args.config, args.out, samples=args.samples)}")


if __name__ == '__main__':
    main()
