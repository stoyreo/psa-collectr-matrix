"""
PSA x Collectr Tracer — Application Launcher
Entry point for the .exe build (PyInstaller).
Handles first-run setup, starts Flask, opens browser.
"""

import os
import sys
import time
import threading
import webbrowser
import subprocess

# ── Resolve base directory (works both frozen .exe and plain Python) ─────────
if getattr(sys, "frozen", False):
    # Running as PyInstaller .exe — _MEIPASS is the extracted bundle folder
    BASE_DIR = sys._MEIPASS
    # The actual .exe lives one level up from _MEIPASS in --onedir mode
    EXE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    EXE_DIR  = BASE_DIR

# Add scripts to Python path
sys.path.insert(0, os.path.join(BASE_DIR, "scripts"))
# Point working directory to EXE folder so relative paths (CSV, cache, output) resolve correctly
os.chdir(EXE_DIR)

PORT = 5000


def banner():
    print("=" * 60)
    print("  PSA x Collectr Tracer")
    print("  http://localhost:{}".format(PORT))
    print("=" * 60)


def ensure_playwright():
    """Install playwright + chromium browser on first run."""
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            b = p.chromium.launch(headless=True)
            b.close()
        return  # already good
    except Exception:
        pass

    print("\n[SETUP] First-run: installing Playwright browser (~120 MB)...")
    print("[SETUP] This takes 1–2 minutes and only happens once.\n")
    try:
        subprocess.run(
            [sys.executable, "-m", "playwright", "install", "chromium"],
            check=True
        )
        print("[SETUP] Browser installed successfully.\n")
    except Exception as e:
        print(f"[WARN]  Could not install playwright browser: {e}")
        print("[WARN]  Live Collectr refresh will use cached prices instead.\n")


def start_flask():
    """Start Flask in a background daemon thread."""
    # Import here so sys.path is already configured
    import importlib.util, types

    # Load webapp from BASE_DIR, passing correct template folder
    spec = importlib.util.spec_from_file_location(
        "webapp",
        os.path.join(BASE_DIR, "webapp.py"),
    )
    mod = importlib.util.module_from_spec(spec)

    # Override Flask template folder before webapp creates the app
    os.environ["FLASK_TEMPLATE_FOLDER"] = os.path.join(BASE_DIR, "templates")
    spec.loader.exec_module(mod)

    mod.app.run(
        host="0.0.0.0",
        port=PORT,
        debug=False,
        use_reloader=False,
        threaded=True,
    )


def wait_for_server(timeout=15):
    """Poll until Flask responds."""
    import urllib.request
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            urllib.request.urlopen(f"http://localhost:{PORT}/api/status", timeout=1)
            return True
        except Exception:
            time.sleep(0.4)
    return False


def main():
    banner()

    # First-run playwright setup (non-blocking if already installed)
    ensure_playwright()

    # Start Flask in background
    print("[INFO] Starting server...")
    t = threading.Thread(target=start_flask, daemon=True)
    t.start()

    # Wait for server to be ready
    if wait_for_server():
        print("[INFO] Server ready — opening browser")
        webbrowser.open(f"http://localhost:{PORT}")
    else:
        print(f"[WARN] Server slow to start — open http://localhost:{PORT} manually")

    print("[INFO] Press Ctrl+C to stop.\n")

    try:
        while t.is_alive():
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[INFO] Shutting down. Goodbye!")


if __name__ == "__main__":
    main()
