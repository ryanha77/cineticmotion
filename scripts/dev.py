#!/usr/bin/env python3
"""Local dev server with live reload (no dependencies).

    python3 scripts/dev.py            # http://localhost:8000
    python3 scripts/dev.py --port 3000

- Edits to src/build.py trigger a rebuild (python3 src/build.py).
- Any change to *.html / assets/* reloads open browser tabs automatically.
- The reload snippet is injected only when served; generated files are untouched.
"""
import argparse, http.server, os, subprocess, sys, threading, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD = os.path.join(ROOT, "src", "build.py")
WATCH_EXT = {".html", ".css", ".js", ".png", ".jpg", ".jpeg", ".webp", ".svg", ".gif", ".mp4", ".xml", ".txt", ".py"}
SKIP_DIRS = {".git", ".github", "node_modules", "__pycache__"}

version = 0
cond = threading.Condition()

SNIPPET = b"""<script>(()=>{let v=null;const es=new EventSource('/__livereload');
es.onmessage=e=>{if(v!==null&&e.data!==v)location.reload();v=e.data};})();</script>"""


def snapshot():
    out = {}
    for d, dirs, files in os.walk(ROOT):
        dirs[:] = [x for x in dirs if x not in SKIP_DIRS]
        for f in files:
            if os.path.splitext(f)[1].lower() in WATCH_EXT:
                p = os.path.join(d, f)
                try:
                    out[p] = os.stat(p).st_mtime_ns
                except FileNotFoundError:
                    pass
    return out


def rebuild():
    print("[dev] src/build.py changed -> rebuilding", flush=True)
    r = subprocess.run([sys.executable, BUILD], cwd=ROOT, capture_output=True, text=True)
    if r.returncode != 0:
        print("[dev] BUILD FAILED:\n" + r.stderr, flush=True)
    else:
        print("[dev] build ok", flush=True)


def watcher():
    global version
    prev = snapshot()
    while True:
        time.sleep(0.4)
        cur = snapshot()
        if cur == prev:
            continue
        changed = {p for p in cur.keys() | prev.keys() if cur.get(p) != prev.get(p)}
        prev = cur
        if BUILD in changed:
            rebuild()
            prev = snapshot()  # absorb files written by the build
        names = ", ".join(sorted(os.path.relpath(p, ROOT) for p in changed)[:5])
        print(f"[dev] reload ({names})", flush=True)
        with cond:
            version += 1
            cond.notify_all()


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, fmt, *args):
        pass

    def do_GET(self):
        if self.path == "/__livereload":
            return self.sse()
        path = self.translate_path(self.path)
        if os.path.isdir(path):
            if not self.path.split("?")[0].endswith("/"):
                return super().do_GET()  # let base class redirect to trailing slash
            path = os.path.join(path, "index.html")
        elif not os.path.exists(path) and os.path.exists(path + ".html"):
            path += ".html"  # GitHub Pages style /cm-1 -> cm-1.html
        if path.endswith(".html") and os.path.isfile(path):
            with open(path, "rb") as fh:
                body = fh.read()
            i = body.lower().rfind(b"</body>")
            body = body[:i] + SNIPPET + body[i:] if i >= 0 else body + SNIPPET
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        return super().do_GET()

    def sse(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.end_headers()
        try:
            seen = -1
            while True:
                with cond:
                    if seen == version:
                        cond.wait(timeout=15)
                    v = version
                if v != seen:
                    self.wfile.write(f"data: {v}\n\n".encode())
                    seen = v
                else:
                    self.wfile.write(b": ping\n\n")
                self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError):
            pass


def lan_ip():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))  # no packet is sent; picks the LAN interface
        return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        s.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--host", default="0.0.0.0", help="127.0.0.1 = this computer only")
    args = ap.parse_args()
    threading.Thread(target=watcher, daemon=True).start()
    srv = http.server.ThreadingHTTPServer((args.host, args.port), Handler)
    srv.daemon_threads = True
    print(f"[dev] serving {ROOT}\n[dev] http://localhost:{args.port}/  (ko)  |  http://localhost:{args.port}/en/  (en)", flush=True)
    if args.host == "0.0.0.0":
        print(f"[dev] phone (same Wi-Fi): http://{lan_ip()}:{args.port}/", flush=True)
    print("[dev] Ctrl+C to stop", flush=True)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\n[dev] stopped")


if __name__ == "__main__":
    main()
