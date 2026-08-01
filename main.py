import http.server
import socketserver
import webbrowser
import os
import glob
import re

PORT = 8000

def generate_index():
    # ponytail: pure stdlib scan of *.html to auto-build index.html for all OS (Win/Mac/Linux)
    files = sorted([f for f in glob.glob("*.html") if f != "index.html"])
    cards = []
    
    for f in files:
        # Extract title from filename (e.g. 01_starting_pieces.html -> 01 Starting Pieces)
        title = f.replace(".html", "").replace("_", " ").title()
        num = re.match(r"^(\d+)", f)
        badge = num.group(1) if num else "•"
        cards.append(f'''
      <a href="{f}" class="card">
        <span class="badge">{badge}</span>
        <div class="info">
          <h2>{title}</h2>
          <span class="file">{f}</span>
        </div>
      </a>''')

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>FinMath Notes — Master Hub</title>
  <style>
    body {{ font-family: system-ui, -apple-system, sans-serif; background: #0d1117; color: #c9d1d9; max-width: 900px; margin: 0 auto; padding: 2rem 1rem; }}
    h1 {{ color: #f0f6fc; text-align: center; margin-bottom: 2rem; font-size: 2rem; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1rem; }}
    .card {{ background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 1.2rem; display: flex; gap: 1rem; align-items: center; text-decoration: none; color: inherit; transition: border-color 0.2s, transform 0.2s; }}
    .card:hover {{ border-color: #58a6ff; transform: translateY(-2px); }}
    .badge {{ background: #1f6beb33; color: #58a6ff; font-weight: bold; padding: 0.4rem 0.7rem; border-radius: 6px; font-size: 0.9rem; min-width: 36px; text-align: center; }}
    .info h2 {{ font-size: 1rem; color: #f0f6fc; margin: 0 0 0.2rem 0; font-weight: 600; }}
    .file {{ font-size: 0.78rem; color: #8b949e; font-family: monospace; }}
  </style>
</head>
<body>
  <h1>FinMath Study Notes</h1>
  <div class="grid">
    {''.join(cards)}
  </div>
</body>
</html>'''

    with open("index.html", "w", encoding="utf-8") as out:
        out.write(html)

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Regenerate index on root request so new files like 11_*.html show automatically
        if self.path in ["/", "/index.html"]:
            generate_index()
        return super().do_GET()

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    generate_index()
    socketserver.TCPServer.allow_reuse_address = True
    
    # Try port 8000, fallback to 8001+ if in use
    port = PORT
    httpd = None
    for p in range(PORT, PORT + 10):
        try:
            httpd = socketserver.TCPServer(("", p), Handler)
            port = p
            break
        except OSError:
            continue

    if httpd:
        url = f"http://localhost:{port}"
        print(f"FinMath server running at {url}")
        webbrowser.open(url)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
