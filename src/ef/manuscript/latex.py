"""The editable LaTeX version of Paper 1 and its PDF.

    python -m ef.manuscript.build pdf      # -> paper1/manuscript/latex/paper1.tex (+ figures/), latex/paper1.pdf, paper1.pdf

paper1/manuscript/latex/ is self-contained: paper1.tex, the figures it includes (vector PDF) and nothing else, so it
compiles with XeLaTeX on this Mac or on Overleaf (set the compiler to XeLaTeX). The text comes from the rendered
sections (paper1/manuscript/NN_*.md), converted by pandoc; the preamble below is ours, written to be read and edited.

Hand edits to latex/paper1.tex are protected: the build remembers the hash of the file it last wrote and, if the file
has changed since, writes paper1.generated.tex beside it instead of overwriting.
"""
import hashlib
import os
import re
import shutil
import subprocess

from ef import config

ROOT = config.repo_root()
MS = os.path.join(ROOT, 'paper1', 'manuscript')
OUT = os.path.join(MS, 'latex')
STAMP = os.path.join(OUT, '.generated.sha256')
BODY = ['01_introduction', '02_data', '03_methods', '04_results', '05_discussion', '06_limitations', '07_future_work',
        '08_ai_disclosure', '09_references', '10_appendix']

PREAMBLE = r"""% Economic Fibrillation, Paper 1 -- editable LaTeX source.
% Compile with pdfLaTeX, XeLaTeX or LuaLaTeX (run twice). On Overleaf the default settings work.
% Generated from paper1/manuscript/ by `python -m ef.manuscript.build pdf`; every number came from a results file
% (paper1/manuscript/numbers.csv). Edit freely: a later build will not overwrite this file once you have changed it.
\documentclass[11pt,a4paper]{article}

% ---------------------------------------------------------------- page and fonts
% Compiles with pdfLaTeX (Overleaf's default) and with XeLaTeX or LuaLaTeX, which use the OpenType fonts.
\usepackage[margin=2.2cm]{geometry}
\usepackage{amsmath}
\usepackage{iftex}
\ifPDFTeX
  \usepackage[T1]{fontenc}
  \usepackage[utf8]{inputenc}
  \usepackage{tgpagella}             % TeX Gyre Pagella
  \usepackage{newpxmath}             % Palatino-style maths to match
  \usepackage{newunicodechar}        % the few symbols typed directly in the text
__UNICODE__
\else
  \usepackage{fontspec}
  \usepackage{unicode-math}
  \setmainfont{texgyrepagella}[Extension=.otf, UprightFont=*-regular, BoldFont=*-bold,
    ItalicFont=*-italic, BoldItalicFont=*-bolditalic]
  \setmathfont{latinmodern-math.otf}
\fi
\usepackage{microtype}
\setlength{\emergencystretch}{3em}
\setcounter{secnumdepth}{0}          % sections carry their numbers in their titles

% ---------------------------------------------------------------- figures, tables, boxes, links
\usepackage{graphicx}
\usepackage{array,calc,longtable,booktabs}
\usepackage{etoolbox}
\AtBeginEnvironment{longtable}{\scriptsize}
\usepackage[font=small,labelformat=empty]{caption}
\usepackage[most]{tcolorbox}
\usepackage{xcolor}
\definecolor{boxgrey}{HTML}{F4F3EF}
\definecolor{linkblue}{HTML}{2A78D6}
\usepackage[colorlinks=true,linkcolor=linkblue,urlcolor=linkblue,citecolor=linkblue]{hyperref}
\usepackage{bookmark}

% helpers the converted text uses
\makeatletter
\newsavebox\pandoc@box
\newcommand*\pandocbounded[1]{\sbox\pandoc@box{#1}%
  \Gscale@div\@tempa{\textheight}{\dimexpr\ht\pandoc@box+\dp\pandoc@box\relax}%
  \Gscale@div\@tempb{\linewidth}{\wd\pandoc@box}%
  \ifdim\@tempb\p@<\@tempa\p@\let\@tempa\@tempb\fi
  \ifdim\@tempa\p@<\p@\scalebox{\@tempa}{\usebox\pandoc@box}\else\usebox{\pandoc@box}\fi}
\def\fps@figure{htbp}
\makeatother
\providecommand{\tightlist}{\setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}}
\newcounter{none}                    % uncaptioned tables (\def\LTcaptype{none})

% ---------------------------------------------------------------- title block
\title{\bfseries __TITLE__}
\author{__AUTHOR__}
\date{__DATE__}
\hypersetup{pdftitle={__PLAINTITLE__}, pdfauthor={__AUTHOR__}}

\begin{document}
\maketitle

\begin{abstract}
__ABSTRACT__

\medskip
\noindent\textbf{Keywords:} __KEYWORDS__
\end{abstract}

"""


UNICODE = {'−': r'\ensuremath{-}', '→': r'\ensuremath{\rightarrow}', '×': r'\ensuremath{\times}', '≤': r'\ensuremath{\le}',
           '≥': r'\ensuremath{\ge}', '≈': r'\ensuremath{\approx}', '±': r'\ensuremath{\pm}', '√': r'\ensuremath{\surd}',
           'κ': r'\ensuremath{\kappa}', 'Δ': r'\ensuremath{\Delta}', 'λ': r'\ensuremath{\lambda}', 'τ': r'\ensuremath{\tau}',
           'μ': r'\ensuremath{\mu}', 'φ': r'\ensuremath{\varphi}', 'ρ': r'\ensuremath{\rho}', 'σ': r'\ensuremath{\sigma}',
           'θ': r'\ensuremath{\theta}', 'ψ': r'\ensuremath{\psi}', 'Ā': r'\={A}', '…': r'\ldots{}', '·': r'\textperiodcentered{}',
           '§': r'\S{}', 'à': r'\`{a}', '–': r'\textendash{}', '—': r'\textemdash{}', '’': "'", '‘': '`', '“': '``', '”': "''"}


def _pandoc(md, shift=0):
    """Markdown to LaTeX: one line per paragraph (the editor wraps), real dashes instead of -- and ---."""
    cmd = ['pandoc', '-f', 'markdown', '-t', 'latex', '--wrap=none']
    if shift: cmd.append(f'--shift-heading-level-by={shift}')
    tex = subprocess.run(cmd, input=md, capture_output=True, text=True, check=True).stdout
    return tex.replace('---', '—').replace('--', '–')


def unicode_block(tex):
    """pdfLaTeX definitions for every non-ASCII character the text uses (XeLaTeX and LuaLaTeX need none)."""
    chars = sorted({c for c in tex if ord(c) > 127})
    unknown = [c for c in chars if c not in UNICODE]
    if unknown: raise SystemExit(f"no pdfLaTeX definition for: {' '.join(unknown)} (add them to ef.manuscript.latex.UNICODE)")
    return "\n".join(f"  \\newunicodechar{{{c}}}{{{UNICODE[c]}}}" for c in chars)


def front(md):
    """Title, author, date line, abstract and keywords from the rendered 00_front.md."""
    title = re.search(r'^# (.+)$', md, flags=re.M).group(1).strip()
    author = re.search(r'^\*\*([^*]+)\*\*\s*$', md, flags=re.M).group(1).strip()
    date = re.search(r'^\*(Draft[^*]+)\*\s*$', md, flags=re.M).group(1).strip()
    abstract = md.split('**Abstract.**', 1)[1].split('**Keywords:**', 1)[0].strip()
    keywords = md.split('**Keywords:**', 1)[1].strip()
    return title, author, date, abstract, keywords


FIG = re.compile(r'!\[(?P<cap>.*?)\]\(\.\./\.\./figures/[^/]+/(?P<stem>[^)]+?)\.png\)', flags=re.S)


def body_md():
    """The sections after the front matter, with figures pointing at latex/figures/*.pdf at the full text width."""
    md = "\n\n".join(open(os.path.join(MS, f'{s}.md')).read() for s in BODY)
    stems = [m.group('stem') for m in FIG.finditer(md)]
    md = FIG.sub(lambda m: f"![{m.group('cap')}](figures/{m.group('stem')}.pdf){{width=100%}}", md)
    return md, stems


def boxed(tex):
    """Box 1 (a block quote in the Markdown) as a shaded box."""
    i = tex.find('Box 1 \\textbar'); i = tex.find('Box 1 |') if i < 0 else i
    if i < 0: return tex
    a = tex.rfind('\\begin{quote}', 0, i); b = tex.find('\\end{quote}', i)
    inner = tex[a + len('\\begin{quote}'):b]
    return (tex[:a] + '\\begin{tcolorbox}[enhanced,breakable,colback=boxgrey,colframe=boxgrey,boxrule=0pt,arc=0pt,'
            'left=10pt,right=10pt,top=8pt,bottom=8pt,before upper={\\setlength{\\parskip}{5pt}}]' + inner + '\\end{tcolorbox}' + tex[b + len('\\end{quote}'):])


def write_tex():
    """latex/paper1.tex and latex/figures/. Returns the path written (paper1.generated.tex if paper1.tex was edited)."""
    os.makedirs(os.path.join(OUT, 'figures'), exist_ok=True)
    title, author, date, abstract, keywords = front(open(os.path.join(MS, '00_front.md')).read())
    md, stems = body_md()
    for stem in stems:
        src = next(os.path.join(dp, f'{stem}.pdf') for dp, _, fs in os.walk(os.path.join(ROOT, 'figures')) if f'{stem}.pdf' in fs)
        shutil.copyfile(src, os.path.join(OUT, 'figures', f'{stem}.pdf'))
    lit = lambda s: _pandoc(s).strip()
    tex = (PREAMBLE.replace('__TITLE__', lit(title)).replace('__PLAINTITLE__', title).replace('__AUTHOR__', author)
           .replace('__DATE__', lit(date)).replace('__ABSTRACT__', lit(abstract)).replace('__KEYWORDS__', lit(keywords)))
    tex += boxed(_pandoc(md, shift=-1)) + "\n\\end{document}\n"
    tex = tex.replace('__UNICODE__', unicode_block(tex[tex.index('\\begin{document}'):] + title))
    target = os.path.join(OUT, 'paper1.tex')
    if os.path.exists(target) and os.path.exists(STAMP):
        if hashlib.sha256(open(target, 'rb').read()).hexdigest() != open(STAMP).read().strip():
            target = os.path.join(OUT, 'paper1.generated.tex')            # paper1.tex was edited by hand: keep it
    open(target, 'w').write(tex)
    if target.endswith('paper1.tex'): open(STAMP, 'w').write(hashlib.sha256(tex.encode()).hexdigest())
    return target


def compile_pdf(tex_path):
    """Two XeLaTeX runs in latex/; the PDF is copied to paper1/manuscript/paper1.pdf."""
    name = os.path.splitext(os.path.basename(tex_path))[0]
    for _ in range(2):
        r = subprocess.run(['xelatex', '-interaction=nonstopmode', '-halt-on-error', f'{name}.tex'], cwd=OUT, capture_output=True, text=True)
        if r.returncode != 0:
            raise SystemExit(f"xelatex failed; see {os.path.join(OUT, name + '.log')}\n" + r.stdout[-2000:])
    shutil.copyfile(os.path.join(OUT, f'{name}.pdf'), os.path.join(MS, 'paper1.pdf'))
    log = open(os.path.join(OUT, f'{name}.log'), errors='replace').read()
    return {'missing_characters': log.count('Missing character'), 'overfull': len(re.findall(r'Overfull \\hbox', log))}


def build():
    missing = [t for t in ('pandoc', 'xelatex') if shutil.which(t) is None]
    if missing:
        raise SystemExit("cannot build the PDF: missing " + ", ".join(missing) + ". See paper1/manuscript/BUILD_PDF.md for the install commands.")
    tex = write_tex(); info = compile_pdf(tex)
    print(f"wrote {os.path.relpath(tex, ROOT)}; PDF {os.path.relpath(os.path.join(MS, 'paper1.pdf'), ROOT)}; {info}")
    return tex, info
