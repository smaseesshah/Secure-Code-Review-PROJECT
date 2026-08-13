import subprocess
import sys
import time
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading

# Landing page HTML serving as the hub
LANDING_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Secure Code Review Lab Hub</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0f172a; color: #f8fafc; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .card-container { display: flex; gap: 2rem; }
        .card { background: #1e293b; border-radius: 12px; padding: 2rem; width: 280px; text-align: center; border: 1px solid #334155; transition: transform 0.2s; }
        .card:hover { transform: translateY(-5px); }
        .card.vuln { border-top: 4px solid #ef4444; }
        .card.sec { border-top: 4px solid #10b981; }
        h2 { margin-top: 0; }
        a { display: inline-block; margin-top: 1rem; padding: 0.75rem 1.5rem; border-radius: 6px; text-decoration: none; font-weight: bold; color: white; }
        .btn-vuln { background: #ef4444; }
        .btn-sec { background: #10b981; }
    </style>
</head>
<body>
    <div class="card-container">
        <div class="card vuln">
            <h2>Vulnerable App</h2>
            <p>TaskVault v1.0 containing live security flaws for code review and testing.</p>
            <p><strong>Port: 3000</strong></p>
            <a href="http://127.0.0.1:3000" target="_blank" class="btn-vuln">Open Vulnerable App</a>
        </div>
        <div class="card sec">
            <h2>Secure App</h2>
            <p>TaskVault v2.0 with all identified security vulnerabilities remediated.</p>
            <p><strong>Port: 4000</strong></p>
            <a href="http://127.0.0.1:4000" target="_blank" class="btn-sec">Open Secure App</a>
        </div>
    </div>
</body>
</html>
"""

class LandingHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(LANDING_HTML.encode('utf-8'))

def run_hub():
    server = HTTPServer(('127.0.0.1', 8000), LandingHandler)
    server.serve_forever()

if __name__ == '__main__':
    print("🚀 Starting Secure Code Review Lab Environment...")

    # Start Vulnerable App (Port 3000)
    p1 = subprocess.Popen([sys.executable, "app.py"], cwd="vulnerable-app")
    print("  [+] Vulnerable App starting on http://127.0.0.1:3000")

    # Start Secure App (Port 4000)
    p2 = subprocess.Popen([sys.executable, "app.py"], cwd="secure-app")
    print("  [+] Secure App starting on http://127.0.0.1:4000")

    # Start Landing Page Server (Port 8000)
    threading.Thread(target=run_hub, daemon=True).start()
    print("  [+] Lab Central Hub online at http://127.0.0.1:8000")

    time.sleep(2)
    webbrowser.open("http://127.0.0.1:8000")

    try:
        p1.wait()
        p2.wait()
    except KeyboardInterrupt:
        print("\nStopping all lab processes...")
        p1.terminate()
        p2.terminate()