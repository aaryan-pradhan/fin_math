"""Build index.html from toc.json. Run after adding or moving a Note."""
import glob, html, json, re

def title(name):
    m = re.search(r"<title>(.*?)</title>", open(f"{name}.html", encoding="utf-8").read(), re.S)
    return m.group(1).strip() if m else name.replace("_", " ").title()

def build():
    toc = json.load(open("toc.json", encoding="utf-8"))
    listed = {n for m in toc for n in m["notes"]}
    missing = [n for n in listed if not glob.glob(f"{n}.html")]
    if missing:
        raise SystemExit(f"toc.json lists missing Notes: {', '.join(missing)}")
    unsorted = sorted(f[:-5] for f in glob.glob("*.html") if f != "index.html" and f[:-5] not in listed)
    if unsorted:
        toc.append({"module": "Unsorted", "notes": unsorted})

    body = "".join(
        f'<h2>{html.escape(m["module"])}</h2>\n<ol>\n'
        + "".join(f'  <li><a href="{n}.html">{title(n)}</a></li>\n' for n in m["notes"])
        + "</ol>\n"
        for m in toc)
    open("index.html", "w", encoding="utf-8").write(f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>FinMath Notes</title>
<link rel="stylesheet" href="note.css">
</head>
<body>
<h1>FinMath Notes</h1>
<p class="lede">Probability, measure theory &amp; stochastic processes.</p>
{body}</body>
</html>
""")

if __name__ == "__main__":
    build()
    print("index.html written")
