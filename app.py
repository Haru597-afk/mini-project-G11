#!/usr/bin/env python3
"""
Math Jungle War local web server.

Run:
    python app.py

The server opens the original HTML game in your default browser.
No third-party Python packages are required.
"""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import os
import threading
import webbrowser

HOST = "127.0.0.1"
PORT = int(os.environ.get("PORT", "8000"))
PROJECT_DIR = Path(__file__).resolve().parent


class GameHandler(SimpleHTTPRequestHandler):
    """Serve the game files from this project's directory."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(PROJECT_DIR), **kwargs)

    def log_message(self, format_string, *args):
        # Keep the terminal output short and readable.
        print(f"[Math Jungle War] {self.address_string()} - {format_string % args}")


def main():
    server = ThreadingHTTPServer((HOST, PORT), GameHandler)
    url = f"http://{HOST}:{PORT}/"

    print("=" * 54)
    print("  Math Jungle War")
    print(f"  เปิดเกมในเบราว์เซอร์: {url}")
    print("  หยุดเซิร์ฟเวอร์ด้วย Ctrl+C")
    print("=" * 54)

    # Open the browser shortly after the server begins listening.
    threading.Timer(0.8, lambda: webbrowser.open(url)).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nกำลังปิดเซิร์ฟเวอร์...")
    finally:
        server.server_close()
        print("ปิดเซิร์ฟเวอร์แล้ว")


if __name__ == "__main__":
    main()
