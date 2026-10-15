# Building the PDF

Built on 15 October 2026, after Sid installed Homebrew, MacTeX, pandoc, poppler and Inter. On a new Mac, install them
in a terminal window (not the chat box; the first two ask for your password), in this order:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

```bash
brew install --cask mactex-no-gui
```

```bash
brew install pandoc poppler
```

```bash
brew install --cask font-inter
```

MacTeX brings xelatex, TeX Gyre Pagella and Latin Modern Math. Open a new terminal afterwards so the TeX binaries are on
the path, then from the repository:

```bash
make paper1-figures paper1-text paper1-pdf
```

`paper1-figures` redraws the figures (vector PDF and 300-dpi PNG; if they come out in DejaVu Sans, matplotlib's font
cache predates Inter: delete `~/.matplotlib/fontlist-*.json` and run it again), `paper1-text` regenerates the text and
`docs/methods.md`, and `paper1-pdf` writes the editable LaTeX source `latex/paper1.tex` (with `latex/figures/`) and
compiles it with XeLaTeX into `paper1.pdf`.

**Editing in LaTeX.** `latex/` is self-contained: upload the folder to Overleaf (Menu → Compiler → XeLaTeX) or run
`xelatex paper1.tex` twice inside it. The fonts (TeX Gyre Pagella, Inter, Latin Modern Math) are all in TeX Live and are
loaded by file name, because XeTeX on macOS finds TeX Live's own fonts only that way. A later `make paper1-pdf` will not
overwrite a `paper1.tex` you have edited; it writes `paper1.generated.tex` beside it instead.
