
import os
import time
import threading
from urllib.request import urlopen
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT = int(os.environ.get("PORT", "10000"))
TARGET_URL = os.environ.get("TARGET_URL", "").strip()


class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/health"):
            body = b'{"status":"ok","service":"pinger"}'

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_error(404)

    def log_message(self, format, *args):
        pass


def run_http_server():
    server = ThreadingHTTPServer(
        ("0.0.0.0", PORT),
        HealthHandler
    )
    print(f"Pinger HTTP server started on port {PORT}")
    server.serve_forever()


def ping_bot():
    while True:
        if TARGET_URL:
            try:
                with urlopen(TARGET_URL, timeout=20) as response:
                    print("Bot ping:", response.status)
            except Exception as exc:
                print("Bot ping failed:", repr(exc))

        time.sleep(60)


if __name__ == "__main__":
    threading.Thread(
        target=ping_bot,
        daemon=True
    ).start()

    run_http_server()
