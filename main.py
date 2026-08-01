import http.server, socketserver, webbrowser, glob, re

def build():
    cards = []
    for idx, f in enumerate(sorted(glob.glob("*.html"))):
        if f == "index.html": continue
        title = f[:-5].replace("_", " ").title()
        try:
            with open(f, encoding="utf-8") as fp:
                m = re.search(r"<title>(.*?)</title>", fp.read(), re.I)
                if m: title = m.group(1).strip()
        except Exception: pass
        c = ["#388bfd", "#2ea043", "#a371f7", "#f0883e", "#58a6ff", "#f85149"][idx % 6]
        cards.append(f'<a href="{f}" class="card" style="border-left-color:{c}"><h2>{title}</h2></a>')

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>FinMath Notes</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: "MesloLGS NF", "Meslo LGS NF", "MesloLGSDNF", monospace;
      background: #0d1117;
      color: #c9d1d9;
      max-width: 960px;
      margin: 0 auto;
      padding: 3rem 1.5rem;
      line-height: 1.6;
    }}
    header {{ text-align: center; margin-bottom: 2.5rem; border-bottom: 1px solid #30363d; padding-bottom: 1rem; }}
    h1 {{ color: #f0f6fc; font-size: 2rem; margin-bottom: 0.3rem; }}
    .subtitle {{ color: #8b949e; font-size: 0.95rem; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(270px, 1fr)); gap: 1.25rem; }}
    .card {{
      background: #161b22;
      border: 1px solid #30363d;
      border-left: 5px solid;
      border-radius: 8px;
      padding: 1.4rem;
      text-decoration: none;
      color: inherit;
      display: flex;
      align-items: center;
      min-height: 100px;
      transition: transform 0.15s ease, background 0.15s ease;
    }}
    .card:hover {{ background: #1c2128; transform: translateY(-3px); }}
    .card h2 {{ font-size: 0.98rem; font-weight: 600; color: #f0f6fc; line-height: 1.45; word-break: break-word; }}
  </style>
</head>
<body>
  <header>
    <h1>FinMath Study Notes</h1>
    <p class="subtitle">Probability Theory, Measure Theory &amp; Stochastic Processes</p>
  </header>
  <main><div class="grid">{''.join(cards)}</div></main>
</body>
</html>'''

    with open("index.html", "w", encoding="utf-8") as out:
        out.write(html)

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path in ["/", "/index.html"]: build()
        return super().do_GET()

if __name__ == "__main__":
    build()
    socketserver.TCPServer.allow_reuse_address = True
    for p in range(8000, 8010):
        try:
            httpd = socketserver.TCPServer(("", p), Handler)
            print(f"Serving at http://localhost:{p}")
            webbrowser.open(f"http://localhost:{p}")
            httpd.serve_forever()
            break
        except (OSError, KeyboardInterrupt): pass
