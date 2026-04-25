"""
remote-web-email-notify — reusable email helper
================================================
Sends a branded HTML email announcing that a local web app is now reachable
through a public tunnel URL (Cloudflare Tunnel, ngrok, Tailscale Funnel, etc.).

Drop this file into any project via:
    skills/remote-web-email-notify/notify_email.py

Then call:
    from notify_email import send_notification_email
    send_notification_email("https://abc-123.trycloudflare.com")

Credentials come from a `.env` file at the project root (same folder as the
launcher that imports this module) OR at a custom path via `env_path=`.

Required .env keys:
    GMAIL_APP_PASSWORD   — 16-char Google App Password
    EMAIL_SENDER         — Gmail address that owns the App Password
    EMAIL_RECIPIENTS     — comma-separated recipient list

Optional .env keys:
    PROJECT_NAME         — shown in subject + header
    PROJECT_EMOJI        — decorative icon (default: 🚀)
"""

from __future__ import annotations

import os
import smtplib
import sys
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import Iterable, Optional


# ── .env loader (no external deps) ────────────────────────────────────────────

def _load_env(env_path: Optional[Path] = None) -> None:
    """Load key=value pairs from a .env file into os.environ (non-destructive)."""
    if env_path is None:
        # Default: .env next to the script that imported this module (the project root).
        # Falls back to this file's parent/parent if that doesn't exist.
        caller_dir = Path(sys.argv[0]).resolve().parent if sys.argv and sys.argv[0] else Path.cwd()
        candidates = [caller_dir / ".env", Path.cwd() / ".env", Path(__file__).resolve().parent.parent.parent / ".env"]
        env_path = next((p for p in candidates if p.exists()), None)
    else:
        env_path = Path(env_path)

    if not env_path or not env_path.exists():
        return

    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = val


# ── Template loader ───────────────────────────────────────────────────────────

_DEFAULT_TEMPLATE = Path(__file__).resolve().parent / "email_template.html"


def _render_template(template_path: Path, **placeholders: str) -> str:
    """Replace {{key}} tokens in an HTML template file."""
    html = template_path.read_text(encoding="utf-8")
    for key, val in placeholders.items():
        html = html.replace("{{" + key + "}}", str(val))
    return html


# ── Public API ────────────────────────────────────────────────────────────────

def send_notification_email(
    public_url: str,
    project_name: Optional[str] = None,
    subject: Optional[str] = None,
    recipients: Optional[Iterable[str]] = None,
    template_path: Optional[str] = None,
    env_path: Optional[str] = None,
) -> bool:
    """
    Send the "your web app is live" email.

    Returns True on success, False on any handled failure (missing creds,
    SMTP auth error, etc.). Never raises — safe to call from a background
    thread inside a tunnel launcher.
    """
    _load_env(Path(env_path) if env_path else None)

    app_password = os.environ.get("GMAIL_APP_PASSWORD", "").strip()
    sender = os.environ.get("EMAIL_SENDER", "").strip()
    env_recipients = os.environ.get("EMAIL_RECIPIENTS", "").strip()
    env_project = os.environ.get("PROJECT_NAME", "").strip() or "Dashboard"
    emoji = os.environ.get("PROJECT_EMOJI", "").strip() or "🚀"

    # Resolve effective values
    project_name = project_name or env_project
    if recipients is None:
        recipients = [r.strip() for r in env_recipients.split(",") if r.strip()]
    else:
        recipients = list(recipients)

    # Guard clauses with clear diagnostics
    if not app_password:
        print("[EMAIL] ⚠  GMAIL_APP_PASSWORD not set — skipping email notification.")
        print("[EMAIL]    Add it to your .env file to enable emails.")
        return False
    if not sender:
        print("[EMAIL] ⚠  EMAIL_SENDER not set in .env — skipping.")
        return False
    if not recipients:
        print("[EMAIL] ⚠  EMAIL_RECIPIENTS empty — no one to email. Skipping.")
        return False

    now = datetime.now().strftime("%d %b %Y  %H:%M")
    tpl = Path(template_path) if template_path else _DEFAULT_TEMPLATE
    if not tpl.exists():
        print(f"[EMAIL] ❌  Template not found: {tpl}")
        return False

    html = _render_template(
        tpl,
        public_url=public_url,
        project_name=project_name,
        project_emoji=emoji,
        timestamp=now,
        sender=sender,
    )

    subject = subject or f"{emoji} {project_name} — Dashboard Live ({now})"

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = ", ".join(recipients)
        msg.attach(MIMEText(html, "html"))

        with smtplib.SMTP("smtp.gmail.com", 587) as s:
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login(sender, app_password)
            s.sendmail(sender, recipients, msg.as_string())

        print(f"[EMAIL] ✅  Notification sent → {', '.join(recipients)}")
        return True

    except smtplib.SMTPAuthenticationError:
        print("[EMAIL] ❌  Authentication failed — check GMAIL_APP_PASSWORD in .env")
        return False
    except Exception as e:
        print(f"[EMAIL] ❌  Failed to send: {e}")
        return False


# ── CLI entry point (optional) ────────────────────────────────────────────────
# Usage:  python notify_email.py https://abc-123.trycloudflare.com

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python notify_email.py <public_url> [project_name]")
        sys.exit(1)
    url = sys.argv[1]
    name = sys.argv[2] if len(sys.argv) > 2 else None
    ok = send_notification_email(url, project_name=name)
    sys.exit(0 if ok else 1)
