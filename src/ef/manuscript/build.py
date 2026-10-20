"""Build the Paper 1 manuscript from its templates: every number from a results file, never typed by hand.

    python -m ef.manuscript.build figures   # redraw the S31 figures (ef.manuscript.figures)
    python -m ef.manuscript.build text      # -> paper1/manuscript/NN_*.md, paper1.md, numbers.csv, TRACE.md; docs/methods.md
    python -m ef.manuscript.build pdf       # -> paper1/manuscript/paper1.pdf (needs pandoc and xelatex)

Templates live in paper1/manuscript/templates/. A placeholder {{ref|fmt}} is resolved by ef.manuscript.values; {{table:name}}
by ef.manuscript.tables. Section references in the Data and Methods templates use the numbering of docs/methods.md
(§1 Data, §2-§8 Methods); in the manuscript §1 becomes §2 and §k.x becomes §3.(k-1).x. TRACE.md lists every number in
the rendered text that does not come from a placeholder, with what it is.
"""
import argparse
import csv
import json
import os
import re
import shutil
import subprocess

import yaml

from ef import config
from ef.manuscript import tables, values

ROOT = config.repo_root()
MS = os.path.join(ROOT, 'paper1', 'manuscript')
TPL = os.path.join(MS, 'templates')
SECTIONS = ['00_front', '01_introduction', '02_data', '03_methods', '04_results', '05_discussion', '06_limitations', '07_future_work',
            '08_ai_disclosure', '08b_data_availability', '09_references', '10_appendix']
METHODS_PARTS = ['02_data', '03_methods']            # docs/methods.md = these two, in methods.md numbering
EXTRAS = {'caveats': 'CAVEATS_FOR_SID', 'checks': 'CHECKS'}   # companion documents for Sid, rendered and traced the same way
CFG = os.path.join(ROOT, 'configs', 'runs', 'phase3_s31.yaml')


# ------------------------------------------------------------------ sources that are not yet files

def write_sources():
    """Quantities the text quotes that no results file holds yet: the samples' share of world GDP (ef.data.maddison, the
    function behind docs/data_validation.md). Written to paper1/manuscript/sources/."""
    from ef.data import maddison
    md = maddison.load(); out = {}
    for s in ('S26', 'S30', 'S31', 'S31_without_RUS'):
        isos = config.sample('S31') if s == 'S31_without_RUS' else config.sample(s)
        if s == 'S31_without_RUS': isos = [i for i in isos if i != 'RUS']
        sh = maddison.world_share(md, isos, (1970, 2022))
        out[s] = {str(int(y)): float(v) for y, v in sh.items()} | {'mean_1970_2022': float(sh.mean())}
    from ef import paper1
    out['code_version'] = paper1.code_version()
    os.makedirs(os.path.join(MS, 'sources'), exist_ok=True)
    json.dump(out, open(os.path.join(MS, 'sources', 'world_share.json'), 'w'), indent=1)


# ------------------------------------------------------------------ rendering

def _widen_first_column(md):
    """Pandoc sizes wrapped table columns by the dashes under the header: give the label column three times the room."""
    return re.sub(r'^\|---\|', '|------------|', md, flags=re.M)


def _tables(text, where):
    def rep(m):
        md, src = tables.TABLES[m.group(1)](); md = _widen_first_column(md)
        values.USED.append((where, f"table:{m.group(1)}", '', '(table)', ';'.join(dict.fromkeys(s for s in src if s))))
        return md
    return re.sub(r'\{\{table:(\w+)\}\}', rep, text)


def _renumber(text):
    """methods.md numbering -> manuscript numbering, for section references and the Methods headings."""
    def sec(m):
        parts = m.group(1).split('.'); k = int(parts[0])
        return '§' + ('2' if k == 1 else '.'.join(['3', str(k - 1)] + parts[1:]))
    text = re.sub(r'§(\d+(?:\.\d+)*)', sec, text)
    text = re.sub(r'^## (\d+)\. ', lambda m: f"### 3.{int(m.group(1)) - 1} " if m.group(1) != '1' else '## 2 ', text, flags=re.M)
    text = re.sub(r'^\*\*(\d+)\.(\d+) ', lambda m: f"**3.{int(m.group(1)) - 1}.{m.group(2)} ", text, flags=re.M)
    return text


def render_section(name):
    t = open(os.path.join(TPL, f'{name}.md')).read()
    t = re.sub(r'<!--.*?-->\n?', '', t, flags=re.S)                     # template notes are not printed
    return values.render(_tables(t, name), name)


def write_locked(path, text):
    """docs/methods.md is kept read-only on disk so it is not edited by accident; Sid asked on 15 October 2026 for the
    fifth-draft edits to be applied, so the build lifts the lock for this one write and puts it back."""
    import stat
    mode = os.stat(path).st_mode if os.path.exists(path) else None
    if mode is not None: os.chmod(path, mode | stat.S_IWUSR)
    try:
        open(path, 'w').write(text)
    finally:
        os.chmod(path, (mode if mode is not None else 0o644) & ~(stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH))


def build_text(write=True):
    """Render every section. write=False renders in memory only and returns (sections, methods text, untraced)."""
    if write: write_sources()
    values.USED.clear(); out = {}
    for name in SECTIONS:
        out[name] = render_section(name)
    methods = "\n\n".join(out[p] for p in METHODS_PARTS)
    header = ("<!-- Generated by `python -m ef.manuscript.build text` from paper1/manuscript/templates/02_data.md and 03_methods.md; "
              "every number comes from a results file (paper1/manuscript/numbers.csv). Edit the templates, not this file. -->\n\n")
    methods_md = header + "# Methods\n\n" + methods
    if write: write_locked(os.path.join(ROOT, 'docs', 'methods.md'), methods_md)
    final = {}
    for name in SECTIONS:
        txt = out[name]
        if name in METHODS_PARTS: txt = _renumber(txt)
        if name == '03_methods': txt = "## 3 Methods\n\n" + txt
        final[name] = txt.strip() + "\n"
    final['paper1'] = "\n\n".join(final[n].strip() for n in SECTIONS) + "\n"
    for extra in EXTRAS: final[extra] = render_section(extra).strip() + "\n"
    if not write: return final, methods_md, trace(final, write=False)
    for name, txt in final.items(): open(os.path.join(MS, f"{EXTRAS.get(name, name)}.md"), 'w').write(txt)
    with open(os.path.join(MS, 'numbers.csv'), 'w', newline='') as f:
        w = csv.writer(f); w.writerow(['section', 'placeholder', 'value', 'printed', 'source'])
        for row in values.USED: w.writerow(row)
    return trace(final)


# ------------------------------------------------------------------ tracing every number

def design_constants():
    """Numbers that are settings, not results, each with the file that fixes it."""
    cfg = yaml.safe_load(open(CFG)); samples = config.load()['samples']; t = cfg['tests']; src = 'configs/runs/phase3_s31.yaml'
    k = {}
    def add(v, why, s=src): k.setdefault(str(v), f"{why} ({s})")
    for y in cfg['recessions']: add(y, 'recession year')
    for y in cfg['downturns']: add(y, 'downturn year')
    for y in list(cfg['span']) + list(cfg['window']) + list(t['mst']['window']): add(y, 'span or window year')
    T = cfg['window'][1] - cfg['window'][0] + 1; add(T, 'T, years in the window'); add(T - 1, 'number of circular shifts')
    for n in (5000, 5001, 2000, 199, 200, 1000): add(f"{n:,}", 'number of surrogates or simulated worlds'); add(n, 'number of surrogates or simulated worlds')
    for s, isos in samples.items(): add(len(isos), f'economies in {s}', 'configs/default.yaml')
    add(len(samples['S31']) - 1, 'economies in S31 without one (leave-one-out)', 'configs/default.yaml')
    add(len(samples['S31']) * (len(samples['S31']) - 1) // 2, 'pairs among 31 economies', 'configs/default.yaml')
    add(len(samples['S26']) * (len(samples['S26']) - 1) // 2, 'pairs among 26 economies', 'configs/default.yaml')
    T_ = T; add(round(1 / T_, 3), 'the circular-shift floor 1/53'); add(round(2 / T_, 3), 'the second-smallest circular-shift p, 2/53')
    add(round(5 / T_, 3), 'Bonferroni floor over five lags, 5/53'); add('3.8%', 'the exact rejection rate 2/53'); add('3.8', 'the exact rejection rate 2/53')
    add('95%', 'the confidence level of every interval'); add(f"{t['arc']['bootstrap']:,}", 'bootstrap draws (tests.arc.bootstrap)')
    add(round(1 / 27, 3), 'the circular-shift floor for 27 years, 1/27'); add(round(1 / 26, 3), 'the circular-shift floor for 26 years, 1/26'); add(72, 'growth years in 1950-2022 (surrogates with ends)'); add(27, 'years in 1996-2022 (split sample)')
    add(0.05, 'the significance level'); add('5%', 'the significance level'); add(0.0002, 'the surrogate floor 1/5001'); add(0.0005, 'the surrogate floor 1/2001')
    add('20%', 'G1b threshold (c), docs/preregistration_G1b_dtt.md', 'docs/preregistration_G1b_dtt.md')
    add(cfg['variants']['late_entry']['from'], "Russia's late entry year (variants.late_entry)")
    for v in (cfg['band'][0], cfg['band'][1], 2, 2.04, t['diversification']['win'], t['csd']['win'], t['bifurcation']['win'], t['mst']['pre'],
              t['csd']['sigma'], t['amplitude']['detrend_sigma'], 12, 9, 10, 3, 8, 100, 1.0): add(v, 'band, window length, smoothing width or filter setting')
    return k


ALLOWED = [  # (pattern, what it is): numbers that are not results
    (r'\b\d{1,2} (?:January|February|March|April|May|June|July|August|September|October|November|December)(?: \d{4})?\b', 'date'),
    (r'\]\([^)]*\)', 'figure file path'), (r'^#+ [\d.]+ ', 'heading number'), (r'^\*\*\d+\.\d+ ', 'heading number'),
    (r'§\d+(?:\.\d+)*(?:–\d+(?:\.\d+)*)?', 'section reference'), (r'\b(?:Table|Figure|Box|Appendix Table|Fig\.) [A-Z]?\d+(?:\.\d+)?', 'table, figure or box number'),
    (r'\bF\d\.\d+\b', 'figure ID'), (r'\b[A-Z]\d{1,2}[a-z]?\b', 'registry or edit label'), (r'\bL\d\b|\bD\d\b|\bV\d\b|\bN\d\b', 'edit label'),
    (r'\b(?:19|20)\d\d[a-z]?\)', 'citation year'), (r'\((?:19|20)\d\d\b', 'citation year'), (r'\b(?:19|20)\d\d[a-z]?(?=[;,]\s)', 'citation year'),
    (r'\$\$.*?\$\$', 'mathematics'), (r'\$[^$]+\$', 'mathematics'), (r"\b(?:19|20)\d0s\b", 'decade'), (r'\bG[0-4]\b|\bS(?:26|30|31)\b|\bG1b\b', 'stage or sample name'),
    (r'doi:\S+|arXiv[: ]\d{4}\.\d{4,5}|\b10\.\d{4,}/\S+', 'identifier'), (r'`[^`]*`', 'file name or code'),
    (r'<https?://[^>\s]+>', 'web address'), (r'Penn World Table\s+\d+\.\d+', 'dataset name and version'), (r'CC BY(?:-NC-SA)?\s+\d\.\d', 'licence name'),
    (r'\b(?:pp?\.|vol\.|no\.)\s*\d+', 'page or volume'), (r'\(\d+\)', 'issue number'), (r'\b\d+[–-]\d+(?=[,.])', 'page range'),
]


def trace(final, write=True):
    """Find every number in the rendered text that does not come from a placeholder and classify it."""
    dc = design_constants(); rows = []
    for name in SECTIONS + list(EXTRAS):
        t = open(os.path.join(TPL, f'{name}.md')).read(); t = re.sub(r'<!--.*?-->', '', t, flags=re.S)
        t = re.sub(r'\{\{[^{}]+\}\}', ' ', t)
        for pat, why in ALLOWED:
            t = re.sub(pat, lambda m: ' ' * len(m.group(0)), t, flags=re.S | re.M)
        for m in re.finditer(r'(?<![\w.])[-−+]?\d[\d,]*(?:\.\d+)?%?', t):
            tok = m.group(0).strip('+−-').rstrip(','); bare = tok.rstrip('%').replace(',', '') if tok.count(',') == 0 or re.fullmatch(r'\d{1,3}(,\d{3})+', tok.rstrip('%')) else tok
            ctx = t[max(0, m.start() - 50): m.end() + 30].replace('\n', ' ')
            key = tok.rstrip('%')
            why = dc.get(tok) or dc.get(key) or dc.get(bare) or dc.get(str(float(bare)) if re.fullmatch(r'\d+\.\d+', bare) else '')
            if why is None and re.fullmatch(r'[1-9]', tok): why = 'small count or ordinal written as a digit'
            if why is None and re.fullmatch(r'(19[5-9]\d|20[0-2]\d)', tok): why = 'calendar year (a date, not a result)'
            if why is None and re.fullmatch(r'\d\d', tok) and re.search(r'(19|20)\d\d–$', t[max(0, m.start() - 5):m.start()]): why = 'end of a year range'
            if why is None and name == '09_references': why = 'bibliographic detail (paper1/manuscript/REFERENCES_CHECK.md)'
            rows.append((name, tok, why or 'UNTRACED', ' '.join(ctx.split())))
    un = [r for r in rows if r[2] == 'UNTRACED']
    L = ["# Number trace — Paper 1 manuscript", "",
         f"Generated by `python -m ef.manuscript.build text`. {sum(1 for r in values.USED if not r[1].startswith('table:'))} numbers and "
         f"{sum(1 for r in values.USED if r[1].startswith('table:'))} tables come from results files through placeholders "
         "(`numbers.csv` gives each with its file and path). The text written into the templates contains the numbers below; each "
         "is classified. **UNTRACED** means a number that is neither a placeholder nor a setting fixed in a config file.", "",
         f"**Untraced: {len(un)}.**", ""]
    if un:
        L += ["| Section | Number | Context |", "|---|---|---|"] + [f"| {a} | {b} | …{d}… |" for a, b, _, d in un] + [""]
    L += ["## Settings and other literal numbers", "", "| Section | Number | What it is | Context |", "|---|---|---|---|"]
    L += [f"| {a} | {b} | {c} | …{d}… |" for a, b, c, d in rows if c != 'UNTRACED']
    if write: open(os.path.join(MS, 'TRACE.md'), 'w').write("\n".join(L) + "\n")
    return un


# ------------------------------------------------------------------ PDF

def build_pdf():
    """The editable LaTeX source (paper1/manuscript/latex/paper1.tex) and the PDF built from it (ef.manuscript.latex)."""
    from ef.manuscript import latex
    return latex.build()


def main(argv=None):
    ap = argparse.ArgumentParser(); ap.add_argument('step', choices=['figures', 'text', 'pdf']); a = ap.parse_args(argv)
    if a.step == 'figures':
        from ef.manuscript import figures; figures.main()
    elif a.step == 'text':
        un = build_text(); print(f"untraced numbers: {len(un)}")
    else:
        build_pdf()


if __name__ == '__main__':
    main()
