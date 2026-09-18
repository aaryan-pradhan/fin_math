# FinMath Study Notes

Self-study notes on probability theory, measure theory, and stochastic processes. Vocabulary in `CONTEXT.md`.

- `toc.json` — Modules and Note order. The only place order lives.
- `note.css` / `note.js` — shared style and MathJax for every Note.
- `python main.py` — rebuilds `index.html` from `toc.json`. Open `index.html` directly.

## Opening

```sh
python main.py      # rebuild index.html (only needed after editing toc.json)
open index.html     # macOS; opens in your default browser
```

No server is needed. `index.html` links to every Note. MathJax loads from a CDN, so the equations need internet access.

Adding a Note: write `<snake_case>.html` with the skeleton in the math-buddy skill, add its name to a Module in `toc.json`, run `python main.py`. Notes missing from `toc.json` show under "Unsorted".
