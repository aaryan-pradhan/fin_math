# FinMath Study Notes

Self-study notes on **probability theory**, **measure theory**, and **stochastic processes**, rendered as clean, readable HTML documents.

Textbooks are dense. Lectures move on. These notes stick.

## Cross-Platform Localhost Hub (Windows, macOS, Linux)

To open the master dashboard and serve all notes locally on any operating system:

```bash
python main.py
```
*(or `python3 main.py` on macOS/Linux)*

This will:
1. Auto-scan all `*.html` notes in the directory.
2. Dynamically build/update `index.html`.
3. Launch `http://localhost:8000` in your default browser.

### Adding New Notes
Whenever you create a new note (e.g. `11_martingales.html`), simply refresh `http://localhost:8000` — it will automatically appear on the dashboard without touching any code!
