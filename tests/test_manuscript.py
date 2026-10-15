"""The Paper 1 manuscript: every number traces to a results file, the committed text is what the templates give, and the
main text keeps to the agreed shape."""
import os
import re

import pytest

from ef.manuscript import build, values

MS = build.MS


@pytest.fixture(scope='module')
def rendered():
    return build.build_text(write=False)


def test_no_untraced_numbers(rendered):
    _, _, untraced = rendered
    assert untraced == [], untraced


def test_committed_text_is_a_fresh_render(rendered):
    final, methods, _ = rendered
    for name, txt in final.items():
        f = os.path.join(MS, f"{build.EXTRAS.get(name, name)}.md")
        assert open(f).read() == txt, f"{f} is stale: run `make paper1-text`"
    assert open(os.path.join(build.ROOT, 'docs', 'methods.md')).read() == methods


def test_every_placeholder_resolves():
    for f in os.listdir(build.TPL):
        t = re.sub(r'<!--.*?-->', '', open(os.path.join(build.TPL, f)).read(), flags=re.S)
        for ref in re.findall(r'\{\{([^{}]+)\}\}', t):
            if ref.startswith(('table:', 'lit:')): continue
            values.resolve_value(ref.partition('|')[0])


def test_abstract_under_200_words(rendered):
    final, _, _ = rendered
    a = final['00_front'].split('**Abstract.**')[1].split('**Keywords')[0]
    assert len(re.findall(r"[A-Za-z0-9][\w'’.–−+%-]*", a)) < 200


def test_main_text_figures(rendered):
    final, _, _ = rendered
    main = "".join(final[s] for s in build.SECTIONS if s not in ('10_appendix',))
    figs = re.findall(r'!\[\*\*Figure \d+ \((F\d\.\d)\)\.\*\*.*?\]\(([^)]+)\)', main, flags=re.S)
    assert 1 <= len(figs) <= 6
    for fid, path in figs:
        assert os.path.exists(os.path.normpath(os.path.join(MS, path))), path


def test_methods_file_stays_read_only():
    assert not os.access(os.path.join(build.ROOT, 'docs', 'methods.md'), os.W_OK) or os.geteuid() == 0


def test_latex_title_block_and_figures():
    """The editable LaTeX version: classic title block, a standard abstract, six vector figures that exist in latex/."""
    from ef.manuscript import latex
    title, author, date, abstract, keywords = latex.front(open(os.path.join(MS, '00_front.md')).read())
    assert title and author == 'Siddhant Shinde' and abstract and keywords
    tex = open(os.path.join(latex.OUT, 'paper1.tex')).read()
    assert '\\maketitle' in tex and '\\begin{abstract}' in tex and '\\documentclass[11pt,a4paper]{article}' in tex
    figs = re.findall(r'\\includegraphics\[[^\]]*\]\{([^}]+)\}', tex)
    assert len(figs) == 6 and all(f.endswith('.pdf') and os.path.exists(os.path.join(latex.OUT, f)) for f in figs)
