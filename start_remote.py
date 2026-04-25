"""
PSA x Collectr Tracer — Remote Access Launcher
Uses Cloudflare Tunnel (cloudflared) — FREE, no account, no auth token needed.
Gives a public *.trycloudflare.com URL anyone can open from any device.
Sends a notification email to recipients once the tunnel is live.
"""

import sys
import os
import re
import time
import threading
import webbrowser
import subprocess
import urllib.request
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent / "scripts"))

PORT = 5000
HERE = Path(__file__).parent
CLOUDFLARED = HERE / "cloudflared.exe"
CLOUDFLARED_URL = (
    "https://github.com/cloudflare/cloudflared/releases/latest/download/"
    "cloudflared-windows-amd64.exe"
)

# ── Email config ──────────────────────────────────────────────────────────────
EMAIL_SENDER     = "techcraftlab.bkk@gmail.com"
EMAIL_RECIPIENTS = ["toy.theeranan@icloud.com", "patipat.arc@gmail.com"]


# ── Load .env helper ──────────────────────────────────────────────────────────

def load_env():
    """Load key=value pairs from .env file into os.environ (if not already set)."""
    env_file = HERE / ".env"
    if not env_file.exists():
        return
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = val


# ── Email notification ────────────────────────────────────────────────────────

def send_notification_email(public_url: str):
    """Send a professional HTML notification email with the live Cloudflare URL."""
    load_env()
    app_password = os.environ.get("GMAIL_APP_PASSWORD", "")
    if not app_password:
        print("[EMAIL] ⚠  GMAIL_APP_PASSWORD not set — skipping email notification.")
        print("[EMAIL]    Add it to your .env file to enable emails.")
        return

    now = datetime.now().strftime("%d %b %Y  %H:%M")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>PSA × Collectr Tracer — Dashboard Ready</title>
</head>
<body style="margin:0;padding:0;background:#F0F2F7;font-family:'Segoe UI',Arial,sans-serif;">

  <!-- Wrapper -->
  <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#F0F2F7;padding:32px 16px;">
    <tr><td align="center">

      <!-- Card -->
      <table width="600" cellpadding="0" cellspacing="0" border="0"
             style="background:#ffffff;border-radius:12px;overflow:hidden;
                    box-shadow:0 4px 24px rgba(27,42,74,.12);max-width:600px;width:100%;">

        <!-- Header -->
        <tr>
          <td style="background:linear-gradient(135deg,#1B2A4A 0%,#2D4A8A 100%);
                     padding:32px 40px;text-align:center;">
            <div style="font-size:28px;margin-bottom:8px;">🎴</div>
            <h1 style="margin:0;color:#ffffff;font-size:22px;font-weight:700;
                       letter-spacing:.5px;">PSA × Collectr Tracer</h1>
            <p style="margin:6px 0 0;color:rgba(255,255,255,.65);font-size:13px;">
              Your live portfolio dashboard is ready
            </p>
          </td>
        </tr>

        <!-- Status pill -->
        <tr>
          <td style="padding:0 40px;">
            <table width="100%" cellpadding="0" cellspacing="0" border="0">
              <tr>
                <td align="center" style="padding:20px 0 0;">
                  <span style="display:inline-block;background:#E8F5E9;color:#2E7D32;
                               border-radius:20px;padding:6px 18px;font-size:13px;font-weight:600;">
                    ✅ &nbsp;Tunnel Active — {now}
                  </span>
                </td>
              </tr>
            </table>
          </td>
        </tr>

        <!-- Body -->
        <tr>
          <td style="padding:28px 40px 8px;">
            <p style="margin:0 0 16px;color:#1A2030;font-size:15px;line-height:1.6;">
              Hi there,
            </p>
            <p style="margin:0 0 20px;color:#3A4560;font-size:14px;line-height:1.7;">
              The <strong>PSA × Collectr Tracer</strong> dashboard is now live and accessible
              from any device worldwide. Click the button below to view your real-time
              Pokemon card portfolio intelligence — prices, signals, and P&amp;L all in one place.
            </p>
          </td>
        </tr>

        <!-- CTA Button -->
        <tr>
          <td style="padding:8px 40px 28px;text-align:center;">
            <a href="{public_url}" target="_blank"
               style="display:inline-block;background:linear-gradient(135deg,#4A90E2,#2D6FBF);
                      color:#ffffff;text-decoration:none;font-size:15px;font-weight:700;
                      padding:14px 36px;border-radius:8px;letter-spacing:.3px;
                      box-shadow:0 4px 14px rgba(74,144,226,.4);">
              🚀 &nbsp;Open Dashboard
            </a>
            <p style="margin:12px 0 0;font-size:11px;color:#9BA4C0;">
              or copy this link:&nbsp;
              <a href="{public_url}" style="color:#4A90E2;word-break:break-all;">{public_url}</a>
            </p>
          </td>
        </tr>

        <!-- Divider -->
        <tr>
          <td style="padding:0 40px;">
            <hr style="border:none;border-top:1px solid #E8EAF2;margin:0;">
          </td>
        </tr>

        <!-- Info row -->
        <tr>
          <td style="padding:20px 40px;">
            <table width="100%" cellpadding="0" cellspacing="0" border="0">
              <tr>
                <td width="50%" style="padding:0 8px 0 0;vertical-align:top;">
                  <div style="background:#F7F9FC;border-radius:8px;padding:14px 16px;">
                    <div style="font-size:11px;color:#9BA4C0;font-weight:600;
                                text-transform:uppercase;letter-spacing:.5px;margin-bottom:4px;">
                      Access
                    </div>
                    <div style="font-size:13px;color:#1A2030;font-weight:600;">
                      Worldwide 🌏
                    </div>
                    <div style="font-size:12px;color:#6B7694;margin-top:2px;">
                      Any phone, tablet, browser
                    </div>
                  </div>
                </td>
                <td width="50%" style="padding:0 0 0 8px;vertical-align:top;">
                  <div style="background:#F7F9FC;border-radius:8px;padding:14px 16px;">
                    <div style="font-size:11px;color:#9BA4C0;font-weight:600;
                                text-transform:uppercase;letter-spacing:.5px;margin-bottom:4px;">
                      Note
                    </div>
                    <div style="font-size:13px;color:#1A2030;font-weight:600;">
                      Temporary URL ⏳
                    </div>
                    <div style="font-size:12px;color:#6B7694;margin-top:2px;">
                      Changes on each restart
                    </div>
                  </div>
                </td>
              </tr>
            </table>
          </td>
        </tr>

        <!-- Footer -->
        <tr>
          <td style="background:#F7F9FC;padding:16px 40px;text-align:center;
                     border-top:1px solid #E8EAF2;">
            <p style="margin:0;font-size:11px;color:#9BA4C0;">
              PSA × Collectr Tracer &nbsp;·&nbsp; TechCraftLab &nbsp;·&nbsp;
              This is an automated notification — do not reply.
            </p>
          </td>
        </tr>

      </table>
    </td></tr>
  </table>

</body>
</html>"""

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"🎴 PSA × Collectr Tracer — Dashboard Live ({now})"
        msg["From"]    = EMAIL_SENDER
        msg["To"]      = ", ".join(EMAIL_RECIPIENTS)
        msg.attach(MIMEText(html, "html"))

        with smtplib.SMTP("smtp.gmail.com", 587) as s:
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login(EMAIL_SENDER, app_password)
            s.sendmail(EMAIL_SENDER, EMAIL_RECIPIENTS, msg.as_string())

        print(f"[EMAIL] ✅  Notification sent → {', '.join(EMAIL_RECIPIENTS)}")

    except smtplib.SMTPAuthenticationError:
        print("[EMAIL] ❌  Authentication failed — check GMAIL_APP_PASSWORD in .env")
    except Exception as e:
        print(f"[EMAIL] ❌  Failed to send: {e}")


# ── Cloudflared download ──────────────────────────────────────────────────────

def ensure_cloudflared():
    if CLOUDFLARED.exists():
        return str(CLOUDFLARED)
    print("[SETUP] Downloading cloudflared (~50 MB, one-time)...")
    try:
        urllib.request.urlretrieve(CLOUDFLARED_URL, str(CLOUDFLARED))
        print("[SETUP] cloudflared downloaded.\n")
        return str(CLOUDFLARED)
    except Exception as e:
        raise RuntimeError(f"Could not download cloudflared: {e}")


# ── Flask server ──────────────────────────────────────────────────────────────

def start_flask():
    import logging
    from webapp import app

    # Suppress Flask/Werkzeug dev-server banner + "development server" warning.
    # NOTE: do NOT set WERKZEUG_RUN_MAIN=true — that flag tells Werkzeug
    # "you are the reloaded child process, look up WERKZEUG_SERVER_FD",
    # which crashes with KeyError when no parent reloader exists.
    try:
        import flask.cli as _fcli
        _fcli.show_server_banner = lambda *a, **kw: None
    except Exception:
        pass
    try:
        import werkzeug.serving as _wsrv
        # Older werkzeug exposes a private banner fn — silence it too if present.
        if hasattr(_wsrv, "_log"):
            _orig = _wsrv._log
            def _quiet_log(level, msg, *a, **kw):
                if isinstance(msg, str) and "development server" in msg.lower():
                    return
                return _orig(level, msg, *a, **kw)
            _wsrv._log = _quiet_log
    except Exception:
        pass
    # Quiet werkzeug's per-request info lines to WARNING (keeps errors visible)
    logging.getLogger("werkzeug").setLevel(logging.WARNING)

    app.run(host="0.0.0.0", port=PORT, debug=False, use_reloader=False, threaded=True)


def wait_for_server(timeout=15):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            urllib.request.urlopen(f"http://localhost:{PORT}/api/status", timeout=1)
            return True
        except Exception:
            time.sleep(0.4)
    return False


# ── Tunnel ────────────────────────────────────────────────────────────────────

def start_tunnel(cf_path):
    """
    Launch cloudflared, parse the public URL from its stderr, print it.
    Returns the subprocess so caller can terminate it on exit.
    """
    proc = subprocess.Popen(
        [cf_path, "tunnel", "--url", f"http://localhost:{PORT}"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
    )

    public_url = None
    deadline = time.time() + 30
    while time.time() < deadline:
        line = proc.stderr.readline()
        if not line:
            break
        match = re.search(r"https://[a-zA-Z0-9\-]+\.trycloudflare\.com", line)
        if match:
            public_url = match.group(0)
            break

    if public_url:
        print()
        print("=" * 60)
        print("  ✅  PUBLIC URL READY — share this link:")
        print()
        print(f"      {public_url}")
        print()
        print("  Works on any phone, tablet, or browser worldwide.")
        print("  URL is temporary — changes each time you restart.")
        print("=" * 60)
        print()

        # Poll until the tunnel actually responds, then open Chrome + send email
        print("[INFO] Waiting for tunnel to be ready...", end="", flush=True)
        ready_deadline = time.time() + 30
        is_ready = False
        while time.time() < ready_deadline:
            try:
                urllib.request.urlopen(public_url + "/api/status", timeout=3)
                print(" ready!")
                is_ready = True
                break
            except Exception:
                print(".", end="", flush=True)
                time.sleep(1)

        if not is_ready:
            print(" timeout — proceeding anyway")

        # Open Chrome
        webbrowser.open(public_url)

        # Send email notification in background (non-blocking)
        threading.Thread(
            target=send_notification_email,
            args=(public_url,),
            daemon=True
        ).start()

    else:
        print("[WARN] Could not parse public URL. Check cloudflared output above.")
        print(f"[INFO] Local server still running at http://localhost:{PORT}")

    # Keep draining stderr so the process doesn't block
    def drain():
        for _ in proc.stderr:
            pass
    threading.Thread(target=drain, daemon=True).start()

    return proc


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  PSA x Collectr Tracer — Remote Access")
    print("=" * 60)
    print()

    cf_path = ensure_cloudflared()

    print("[1/2] Starting local server...")
    flask_thread = threading.Thread(target=start_flask, daemon=True)
    flask_thread.start()

    if not wait_for_server():
        print("[ERROR] Flask did not start in time.")
        sys.exit(1)

    print("[2/2] Opening Cloudflare Tunnel...")
    tunnel_proc = start_tunnel(cf_path)

    print("[INFO] Press Ctrl+C to stop.\n")
    try:
        while flask_thread.is_alive():
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[INFO] Shutting down tunnel and server...")
        tunnel_proc.terminate()
        print("[INFO] Goodbye!")


if __name__ == "__main__":
    main()
