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
        # ponytail: strip leading lecture numbers (e.g. "02 — ", "28 - ")
        title = re.sub(r'^\d+\s*[—\-]\s*', '', title)
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
    .btn-reset {{
      margin-top: 0.8rem;
      background: #21262d;
      color: #8b949e;
      border: 1px solid #30363d;
      padding: 0.35rem 0.8rem;
      border-radius: 6px;
      cursor: pointer;
      font-family: inherit;
      font-size: 0.8rem;
      transition: all 0.15s ease;
    }}
    .btn-reset:hover {{ background: #30363d; color: #f0f6fc; }}
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
      cursor: grab;
      transition: transform 0.15s ease, background 0.15s ease;
    }}
    .card:hover {{ background: #1c2128; transform: translateY(-3px); }}
    .card:active {{ cursor: grabbing; }}
    .card h2 {{ font-size: 0.98rem; font-weight: 600; color: #f0f6fc; line-height: 1.45; word-break: break-word; }}
  </style>
</head>
<body>
  <header>
    <h1>FinMath Study Notes</h1>
    <p class="subtitle">Probability Theory, Measure Theory &amp; Stochastic Processes</p>
    <button id="reset-btn" class="btn-reset">Reset Order</button>
  </header>
  <main><div class="grid">{''.join(cards)}</div></main>
  <script>
    // ponytail: Native HTML5 drag-and-drop with localStorage order persistence
    document.addEventListener('DOMContentLoaded', () => {{
      const grid = document.querySelector('.grid');
      let cards = Array.from(grid.querySelectorAll('.card'));
      
      cards.forEach(c => {{
        const h2 = c.querySelector('h2');
        if (h2) h2.textContent = h2.textContent.replace(/^\\d+\\s*[—\\-]\\s*/, '');
      }});

      const saved = JSON.parse(localStorage.getItem('finmath_order') || '[]');
      if (saved.length) {{
        const map = new Map(cards.map(c => [c.getAttribute('href'), c]));
        saved.forEach(href => {{ if (map.has(href)) grid.appendChild(map.get(href)); }});
        cards.forEach(c => {{ if (!grid.contains(c)) grid.appendChild(c); }});
        cards = Array.from(grid.querySelectorAll('.card'));
      }}

      let dragged = null;
      cards.forEach(card => {{
        card.setAttribute('draggable', 'true');
        card.addEventListener('dragstart', (e) => {{
          dragged = card;
          card.style.opacity = '0.4';
        }});
        card.addEventListener('dragend', () => {{
          if (dragged) dragged.style.opacity = '1';
          dragged = null;
          saveOrder();
        }});
        card.addEventListener('dragover', (e) => e.preventDefault());
        card.addEventListener('drop', (e) => {{
          e.preventDefault();
          if (dragged && dragged !== card) {{
            const children = Array.from(grid.children);
            const fromIdx = children.indexOf(dragged);
            const toIdx = children.indexOf(card);
            if (fromIdx < toIdx) grid.insertBefore(dragged, card.nextSibling);
            else grid.insertBefore(dragged, card);
          }}
        }});
      }});

      function saveOrder() {{
        const order = Array.from(grid.querySelectorAll('.card')).map(c => c.getAttribute('href'));
        localStorage.setItem('finmath_order', JSON.stringify(order));
      }}

      document.getElementById('reset-btn')?.addEventListener('click', () => {{
        localStorage.removeItem('finmath_order');
        location.reload();
      }});
    }});
  </script>
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
    # ponytail: scans ports 8000-8009, falls back to dynamic port 0 if all occupied
    for p in list(range(8000, 8010)) + [0]:
        try:
            with socketserver.TCPServer(("", p), Handler) as httpd:
                port = httpd.server_address[1]
                print(f"Serving at http://localhost:{port}", flush=True)
                webbrowser.open(f"http://localhost:{port}")
                try:
                    httpd.serve_forever()
                except KeyboardInterrupt:
                    print("\nServer stopped.")
                break
        except OSError:
            continue


