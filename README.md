# FinMath Study Notes

Self-study notes on probability theory, measure theory, and stochastic processes.

## Quick Start & Automatic Indexing

Simply run the local server:
```bash
python main.py
```

### Adding New Lectures
To add a new lecture note:
1. Create a new `.html` file in this directory with your `<title>Lecture Title</title>`.
2. Run `python main.py`. `main.py` automatically scans all `.html` files in the directory and updates `index.html` with your new lecture card.

---

## Reordering & Customizing Lectures

- **Drag and Drop**: Drag any lecture card on `index.html` to swap positions.
- **Persistence**: Your custom card order is saved in your browser (`localStorage`) automatically.
- **Reset**: Click **Reset Order** in the header to restore default file order.
