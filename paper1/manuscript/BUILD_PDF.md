# Building the PDF

The PDF step stopped on 15 October 2026 because these tools are missing on this Mac: **Homebrew, MacTeX (xelatex),
pandoc, poppler and the Inter font**. Nothing was worked around. Install them, in a terminal, in this order (the first
asks for your password):

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

`paper1-figures` redraws the figures (with Inter once it is installed; until then matplotlib falls back to DejaVu
Sans; if the figures still come out in DejaVu Sans, matplotlib's font cache predates Inter: delete
`~/.matplotlib/fontlist-*.json` and run it again), `paper1-text` regenerates the text and `docs/methods.md`, and `paper1-pdf` runs pandoc with xelatex on
`paper1/manuscript/paper1.md` (TeX Gyre Pagella for text, Inter for sans, Latin Modern Math). The same install lets
`tools/build_figure_docs.py` rebuild `docs/FIGURES.md` and the figure books with the redrawn figures.
