"""
Build the categorized figure set from tools/figure_catalog.py:

  figures/NN_<category>/F<cat>-<nn>_<name>.png   (+ the vector .pdf where one exists)
  figures/compiled/EF_Figures_NN_<Title>.pdf     one figure book per category, plus 00 index
  docs/FIGURES.md                                the same catalogue as text, for Claude Code

Run from the repository root:
    python3 tools/build_figure_docs.py            # sources are in figures/_sources/ and atlas/fig/
Needs xelatex with TeX Gyre Pagella, Inter and Latin Modern Math (the atlas fonts) and pdftoppm.
"""
import argparse, os, re, shutil, subprocess, sys, json
sys.path.insert(0, os.path.dirname(__file__))
import figure_catalog as C

ap = argparse.ArgumentParser()
ap.add_argument("--build", default="build/figbooks", help="folder for LaTeX intermediates")
ap.add_argument("--date", default="11 October 2026")
args = ap.parse_args()
ROOT = os.getcwd()
BUILD = os.path.abspath(args.build); os.makedirs(BUILD, exist_ok=True)

SHORT = {1: "Method", 2: "Crisis_Arc", 3: "Crisis_Dating_History", 4: "Amplitude_and_Diversification",
         5: "Network_and_Phase", 6: "Tipping_Nulls", 7: "Inside_the_Economies", 8: "Country_Atlas"}
CAT = {c[0]: c for c in C.CATEGORIES}

def fid(e):  # F2.5 -> F2-05
    c, n = e["id"][1:].split(".")
    return f"F{c}-{int(n):02d}"

# ------------------------------------------------------------------ 1. place files
placed = []
for e in C.F:
    src = e["src"]
    if not src.startswith("/"): src = os.path.join(ROOT, src)
    if not os.path.exists(src):
        hint = " (run `make atlas-figs`, or unzip economic-fibrillation-atlas-figures.zip into the repository)" if src.startswith("atlas/fig") else ""
        raise SystemExit(f"missing source for {e['id']}: {src}{hint}")
    folder = f"figures/{e['cat']:02d}_{CAT[e['cat']][1]}"; os.makedirs(folder, exist_ok=True)
    stem = f"{fid(e)}_{e['name']}"
    if src.endswith(".pdf"):
        shutil.copy(src, f"{folder}/{stem}.pdf")
        subprocess.run(["pdftoppm", "-r", "170", "-png", "-singlefile", src, f"{folder}/{stem}"], check=True)
        e["files"] = [f"{folder}/{stem}.pdf", f"{folder}/{stem}.png"]; e["tex_img"] = f"{ROOT}/{folder}/{stem}.pdf"
    else:
        shutil.copy(src, f"{folder}/{stem}.png")
        e["files"] = [f"{folder}/{stem}.png"]; e["tex_img"] = f"{ROOT}/{folder}/{stem}.png"
    e["fid"] = fid(e); placed.append(e)

# country dashboards (category 8): copy, no captions beyond the economy name
meta = json.load(open("atlas/meta.json"))
names = {o[0]: o[1] for o in meta["order"] + meta.get("extra", [])}
atlas_rows = []
os.makedirs("figures/08_country_atlas", exist_ok=True)
for i, iso in enumerate(C.ATLAS_ORDER, 1):
    dst = f"figures/08_country_atlas/F8-{i:02d}_{iso}.png"
    shutil.copy(f"atlas/fig/{iso}.png", dst)
    atlas_rows.append((f"F8.{i}", iso, names.get(iso, iso), dst))

# ------------------------------------------------------------------ 2. LaTeX helpers
FORMULAS = [
    ("|Z(t)| = Ā(t) × R_A(t)", r"$|Z(t)| = \bar{A}(t)\times R_A(t)$"),
    ("|Z| = Ā × R_A", r"$|Z| = \bar{A}\times R_A$"),
    ("r(t) = |(1/N) Σ exp(iθ_i(t))|", r"$r(t) = \bigl|\tfrac{1}{N}\sum_i e^{\mathrm{i}\theta_i(t)}\bigr|$"),
    ("θ(t) = arg z(t)", r"$\theta(t) = \arg z(t)$"),
    ("K/K_c = 1/(1 − r²)", r"$K/K_c = 1/(1-r^2)$"),
    ("√(2(1−ρ))", r"$\sqrt{2(1-\rho)}$"),
    ("10⁻¹⁹", r"$10^{-19}$"), ("10⁻⁴", r"$10^{-4}$"),
    ("swing²", r"swing$^2$"), ("R_A", r"$R_A$"), ("K/K_c", r"$K/K_c$"), ("Ā(t)", r"$\bar{A}(t)$"), ("Ā", r"$\bar{A}$"),
    ("z(t)", r"$z(t)$"), ("A(t)", r"$A(t)$"), ("r(t)", r"$r(t)$"), ("R(t)", r"$R(t)$"), ("L(t)", r"$L(t)$"), ("C(t)", r"$C(t)$"),
]
SYM = {"θ": r"\theta", "ρ": r"\rho", "τ": r"\tau", "λ": r"\lambda", "σ": r"\sigma", "π": r"\pi", "Σ": r"\Sigma",
       "Δ": r"\Delta", "≈": r"\approx", "×": r"\times", "±": r"\pm", "≥": r"\geq", "≤": r"\leq", "★": r"\star", "√": r"\surd"}

def tex(s):
    keep = []
    for raw, lat in FORMULAS:
        while raw in s:
            keep.append(lat); s = s.replace(raw, f"\x00{len(keep)-1}\x00", 1)
    s = (s.replace("\\", r"\textbackslash{}").replace("&", r"\&").replace("%", r"\%").replace("$", r"\$")
          .replace("#", r"\#").replace("_", r"\_").replace("{", r"\{").replace("}", r"\}").replace("~", r"\textasciitilde{}")
          .replace("^", r"\^{}"))
    for k, v in SYM.items(): s = s.replace(k, f"${v}$")
    s = s.replace("→", r"$\rightarrow$").replace("−", r"\textminus{}").replace("'", "’")
    s = re.sub(r"\x00(\d+)\x00", lambda m: keep[int(m.group(1))], s)
    return s

def path_tex(s):
    return tex(s).replace("/", r"/\allowbreak{}").replace(r"\_", r"\_\allowbreak{}")

PREAMBLE = r"""\documentclass[10pt]{article}
\usepackage[a4paper,top=14mm,bottom=16mm,left=16mm,right=16mm,footskip=7mm]{geometry}
\usepackage{fontspec}
\setmainfont{texgyrepagella}[Extension=.otf,UprightFont=*-regular,BoldFont=*-bold,ItalicFont=*-italic,BoldItalicFont=*-bolditalic,Ligatures=TeX,Numbers=Lining]
\setsansfont{Inter}[Numbers={Lining}]
\usepackage{unicode-math}\setmathfont{latinmodern-math.otf}
\usepackage{xcolor,graphicx,booktabs,tabularx,array,fancyhdr,enumitem,longtable}
\usepackage[hidelinks]{hyperref}
\definecolor{ink}{HTML}{0B0B0B}\definecolor{ink2}{HTML}{52514E}\definecolor{muted}{HTML}{898781}
\definecolor{rule}{HTML}{C3C2B7}\definecolor{band}{HTML}{F4F3EE}\definecolor{accent}{HTML}{2A78D6}
\color{ink}\setlength{\parindent}{0pt}\setlength{\parskip}{3pt}\raggedbottom
\pagestyle{fancy}\fancyhf{}\renewcommand{\headrulewidth}{0pt}
\fancyfoot[L]{\sffamily\fontsize{7}{8}\selectfont\color{muted}Economic Fibrillation · FOOTER}
\fancyfoot[R]{\sffamily\fontsize{7}{8}\selectfont\color{muted}\thepage}
\newcommand{\chip}[2]{\leavevmode\mbox{\sffamily\fontsize{7}{8}\selectfont\bfseries\color[HTML]{#1}\MakeUppercase{#2}}}
\begin{document}
"""

def chip(status):
    lab, col = C.STATUS[status]
    return rf"\chip{{{col}}}{{{tex(lab)}}}"

def head(kicker, title, intro):
    return (rf"\thispagestyle{{fancy}}{{\sffamily\color{{muted}}\fontsize{{8.5}}{{10}}\selectfont {kicker}}}\par\vspace{{3mm}}"
            rf"{{\raggedright\sffamily\bfseries\fontsize{{22}}{{26}}\selectfont {title}\par}}\vspace{{4mm}}"
            rf"{{\fontsize{{10.5}}{{14}}\selectfont {intro}}}\par\vspace{{3mm}}{{\color{{rule}}\rule{{\textwidth}}{{0.5pt}}}}\par" + "\n")

def legend():
    rows = " \\\\[1pt]\n".join(rf"{chip(k)} & {{\fontsize{{8.5}}{{11}}\selectfont {tex(d)}}}" for k, d in [
        ("current", "Paper data (Maddison 2023) and the paper's conventions; numbers match docs/methods.md."),
        ("relabel", "Numbers right, but an annotation on the figure is out of date (said in the caption)."),
        ("convW", "Hilbert transform applied to 1970–2022 only (convention W); the paper uses P."),
        ("superseded", "Earlier data or crisis definition; the record of how the paper got here."),
        ("descriptive", "Atlas material from the Global Macro Database; describes, does not test."),
        ("unverified", "The series drawn matches no stored results file; redraw before use.")])
    return (r"{\sffamily\bfseries\fontsize{9}{11}\selectfont Status key}\par\vspace{1mm}"
            r"\begin{tabularx}{\textwidth}{@{}>{\raggedright\arraybackslash}p{34mm}X@{}}" + rows + r"\end{tabularx}\par\vspace{2mm}" + "\n")

def contents(items):
    rows = " \\\\\n".join(rf"{{\sffamily\bfseries\color{{accent}} {e['id']}}} & {tex(e['title'])} & {chip(e['status'])}" for e in items)
    return (r"{\sffamily\bfseries\fontsize{9}{11}\selectfont In this book}\par\vspace{1mm}{\fontsize{8.8}{11}\selectfont"
            r"\begin{tabularx}{\textwidth}{@{}l>{\raggedright\arraybackslash}X>{\raggedright\arraybackslash}p{30mm}@{}}" + rows + r"\end{tabularx}}\par" + "\n")

def block(e):
    h = "0.34\\textheight"
    return rf"""
\par\noindent\begin{{minipage}}{{\textwidth}}
\vspace{{5mm}}{{\color{{rule}}\rule{{\textwidth}}{{0.4pt}}}}\par\vspace{{1.5mm}}
{{\sffamily\fontsize{{8.5}}{{10}}\selectfont\bfseries\color{{accent}}{e['id']}}}\enspace{chip(e['status'])}\par\vspace{{0.6mm}}
{{\raggedright\sffamily\bfseries\fontsize{{10.5}}{{13}}\selectfont {tex(e['title'])}\par}}\vspace{{2mm}}
\begin{{center}}\includegraphics[width=\linewidth,height={h},keepaspectratio]{{{e['tex_img']}}}\end{{center}}\vspace{{-1mm}}
{{\fontsize{{9.6}}{{12.6}}\selectfont {tex(e['caption'])}}}\par\vspace{{1.2mm}}
{{\sffamily\fontsize{{7.8}}{{10}}\selectfont\raggedright
{{\bfseries Numbers}}\enspace {tex(e['numbers'])}\par
{{\bfseries Made by}}\enspace {path_tex(e['made_by'])}\enspace·\enspace{{\bfseries Data}}\enspace {tex(e['data'])}\par
{{\color{{muted}}{{\bfseries File}}\enspace {path_tex(e['files'][0])}}}\par}}
\end{{minipage}}\par
"""

def convention_table():
    rows = " \\\\\n".join(" & ".join(tex(x) for x in r) for r in C.CONVENTION_TABLE)
    return (r"\vspace{1mm}{\sffamily\bfseries\fontsize{9}{11}\selectfont Where the Hilbert transform is applied changes the arc}\par"
            r"{\fontsize{8.6}{11}\selectfont The same data, filter and permutation test under three conventions (correlation, one-sided p in brackets). "
            r"Recomputed 11 October 2026 by tools/check\_runin\_conventions.py; P reproduces kose\_terrones\_results.json and W reproduces amplitude\_results.json exactly.}\par\vspace{1mm}"
            r"{\sffamily\fontsize{7.6}{9.5}\selectfont\setlength{\tabcolsep}{3pt}\begin{tabularx}{\textwidth}{@{}>{\raggedright\arraybackslash}X rrrrrr@{}}\toprule "
            r"Convention & Lead-2 & Lead-1 & Crisis & After-1 & After-2 & $r$–$\bar{A}$ \\ \midrule " + rows + r" \\ \bottomrule\end{tabularx}}\par\vspace{2mm}" + "\n")

def compile_tex(name, body, footer):
    p = os.path.join(BUILD, name + ".tex")
    open(p, "w").write(PREAMBLE.replace("FOOTER", footer) + body + "\n\\end{document}\n")
    for _ in range(2):
        r = subprocess.run(["xelatex", "-interaction=nonstopmode", "-halt-on-error", name + ".tex"], cwd=BUILD, capture_output=True, text=True)
        if r.returncode: print(r.stdout[-3000:]); raise SystemExit(f"xelatex failed on {name}")
    log = open(os.path.join(BUILD, name + ".log"), errors="ignore").read()
    miss = sorted(set(re.findall(r"Missing character: There is no (.) ", log)))
    over = len(re.findall(r"Overfull \\hbox", log))
    return os.path.join(BUILD, name + ".pdf"), miss, over

# ------------------------------------------------------------------ 3. one book per category
os.makedirs("figures/compiled", exist_ok=True)
report = []
for c in C.CATEGORIES:
    k, slug, title, intro = c
    out = f"figures/compiled/EF_Figures_{k:02d}_{SHORT[k]}.pdf"
    if k == 8:
        atlas_pdf = "atlas/The 26 Economies 1970-2022 - Atlas.pdf"
        if os.path.exists(atlas_pdf): shutil.copy(atlas_pdf, out); report.append((out, "atlas copy", [], 0))
        else: report.append((out, "skipped: atlas PDF absent, run `make atlas-pdf`", [], 0))
        continue
    items = [e for e in placed if e["cat"] == k]
    body = head(f"ECONOMIC FIBRILLATION · FIGURE BOOK {k:02d} OF 08 · {args.date.upper()}", tex(title), tex(intro))
    if k == 2: body += convention_table()
    body += legend() + contents(items) + r"\clearpage" + "".join(block(e) for e in items)
    pdf, miss, over = compile_tex(f"book{k:02d}", body, f"Figure book {k:02d} · {tex(title)}")
    shutil.copy(pdf, out); report.append((out, f"{len(items)} figures", miss, over))

# ------------------------------------------------------------------ 4. index book (00)
rows = []
for c in C.CATEGORIES:
    k = c[0]
    rows.append(rf"\multicolumn{{3}}{{@{{}}l}}{{\rule{{0pt}}{{14pt}}\sffamily\bfseries\fontsize{{9.5}}{{12}}\selectfont Book {k:02d} · {tex(c[2])}}} \\")
    if k == 8:
        rows.append(rf"{{\sffamily\color{{accent}}\bfseries F8.1–F8.31}} & One dashboard per economy: {tex(', '.join(r[2] for r in atlas_rows))} & {chip('descriptive')} \\")
        continue
    for e in [e for e in placed if e["cat"] == k]:
        rows.append(rf"{{\sffamily\color{{accent}}\bfseries {e['id']}}} & {tex(e['title'])} & {chip(e['status'])} \\")
counts = {s: sum(1 for e in placed if e["status"] == s) for s in C.STATUS}
intro = (f"Every graph made for Economic Fibrillation up to {args.date}: {len(placed)} analysis figures in seven "
         f"figure books, plus the {len(atlas_rows)} economy dashboards of the atlas (book 08). Each figure is stored "
         "once, in figures/NN_<category>/, as a PNG and, where it was drawn as a vector, a PDF. "
         f"Status: {counts['current']} current, {counts['relabel']} need relabelling, {counts['convW']} use the windowed-Hilbert "
         f"convention, {counts['superseded']} are superseded history, {counts['descriptive']} are descriptive atlas figures and "
         f"{counts['unverified']} draws a series that matches no stored results file. "
         "Lost with the September workspace and not recoverable: the restoring-time figure from csd_fast.py and the "
         "plotting scripts for the companion figures, F4.3, F7.1 and F7.2 (their results files survive and reproduce exactly).")
body = (head(f"ECONOMIC FIBRILLATION · FIGURE BOOK 00 · {args.date.upper()}", "Index of every figure", tex(intro)) + legend()
        + r"{\fontsize{8.8}{11.2}\selectfont\begin{longtable}{@{}l>{\raggedright\arraybackslash}p{118mm}>{\raggedright\arraybackslash}p{30mm}@{}}"
        + "\n".join(rows) + r"\end{longtable}}")
pdf, miss, over = compile_tex("book00", body, "Figure book 00 · Index")
shutil.copy(pdf, "figures/compiled/EF_Figures_00_Index.pdf"); report.append(("figures/compiled/EF_Figures_00_Index.pdf", "index", miss, over))

# ------------------------------------------------------------------ 5. docs/FIGURES.md
L = [f"# Figure index — Economic Fibrillation\n",
     f"Generated by `tools/build_figure_docs.py` from `tools/figure_catalog.py` on {args.date}. "
     f"{len(placed)} analysis figures in categories 1–7 plus {len(atlas_rows)} economy dashboards (category 8). "
     "Each category is also compiled as a PDF figure book in `figures/compiled/`.\n",
     "**Status key.** `current` = paper data and conventions, numbers match `docs/methods.md`. `relabel` = numbers right, an "
     "annotation on the figure is outdated. `convW` = Hilbert applied to 1970–2022 only (convention W); the paper uses P. "
     "`superseded` = earlier data or crisis definition, kept as history. `descriptive` = atlas material, no test. "
     "`unverified` = the series drawn matches no stored results file; redraw before use.\n",
     "**When you regenerate a figure**, keep its ID, put the new file in the same folder, update its catalogue entry "
     "(status, numbers, made_by) and rerun this builder. Never silently overwrite a superseded figure; it is the record.\n"]
for c in C.CATEGORIES:
    k = c[0]
    L.append(f"\n## {k:02d} · {c[2]}\n\n{c[3]}\n")
    if k == 2:
        L.append("\n| Convention | Lead-2 | Lead-1 | Crisis | After-1 | After-2 | r–Ā (detrended) |\n|---|---|---|---|---|---|---|")
        for r in C.CONVENTION_TABLE: L.append("| " + " | ".join(r) + " |")
        L.append("")
    if k == 8:
        L.append("| ID | Economy | File |\n|---|---|---|")
        for f_, iso, nm, dst in atlas_rows: L.append(f"| {f_} | {nm} ({iso}) | `{dst}` |")
        L.append("\nThe narrative version (text, tables and data notes) is `atlas/The 26 Economies 1970-2022 - Atlas.pdf`, "
                 "copied as `figures/compiled/EF_Figures_08_Country_Atlas.pdf`.")
        continue
    for e in [e for e in placed if e["cat"] == k]:
        L.append(f"\n### {e['id']} · {e['title']}\n")
        L.append(f"- **Status:** `{e['status']}`")
        L.append(f"- **Files:** " + ", ".join(f"`{x}`" for x in e["files"]))
        L.append(f"- **Shows:** {e['caption']}")
        L.append(f"- **Numbers:** {e['numbers']}")
        L.append(f"- **Made by:** {e['made_by']}")
        L.append(f"- **Data:** {e['data']}")
open("docs/FIGURES.md", "w").write("\n".join(L) + "\n")

for out, what, miss, over in report:
    print(f"{out:62s} {what:12s} missing-glyphs={''.join(miss) or '-'} overfull={over}")
print("placed", len(placed), "figures +", len(atlas_rows), "dashboards")
