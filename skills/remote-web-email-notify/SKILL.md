---
name: remote-web-email-notify
description: Send a branded Gmail notification email when a locally-running web app (Flask/FastAPI/Streamlit/any HTTP server) becomes reachable via a public tunnel URL (Cloudflare Tunnel, ngrok, Tailscale Funnel, etc.). Use this skill whenever the user says: "email me when the web is live", "notify when tunnel ready", "send email when web hosted remotely", "email the public URL", "notify recipients when dashboard is up", "remote hosting email notification", or when integrating a public-URL email hand-off into ANY project that exposes a localhost server to the internet. Reusable across projects — drop the folder in, fill `.env`, import `send_notification_email(public_url, ...)`.
type: integration
version: 1.0.0
author: TechCraftLab
---

# remote-web-email-notify

Portable skill that emails a recipient list the moment a local web app becomes publicly reachable through a tunnel. Extracted from `PSA x Collectr Tracer/start_remote.py` and generalized so any project can reuse it.

## When to trigger this skill

Activate whenever the user asks for ANY of the following scenarios:

- "Send me an email when my local web app is hosted remotely"
- "Email the Cloudflare / ngrok / Tailscale public URL after the tunnel comes up"
- "Notify recipients by email when the dashboard goes live"
- "Add a tunnel-ready email hook to this Flask/FastAPI/Streamlit project"
- "Reuse the email launcher from PSA x Collectr Tracer in a new project"

## What the skill provides

A self-contained folder with four files. Copy the folder into any project and wire up one import:

```
skills/remote-web-email-notify/
├── SKILL.md              ← this file
├── notify_email.py       ← import and call send_notification_email(url)
├── email_template.html   ← edit to rebrand the email body
└── .env.example          ← copy to project root as .env and fill in
```

## Install into a new project (3 steps)

1. **Copy the folder** into the target project:
   ```
   <target-project>/skills/remote-web-email-notify/
   ```

2. **Create `.env`** at the target project root (same folder as the launcher script):
   ```bash
   cp skills/remote-web-email-notify/.env.example .env
   ```
   Then fill in:
   ```env
   GMAIL_APP_PASSWORD=xxxxxxxxxxxxxxxx       # 16-char Google App Password
   EMAIL_SENDER=techcraftlab.bkk@gmail.com
   EMAIL_RECIPIENTS=you@example.com,teammate@example.com
   PROJECT_NAME=My Awesome Dashboard
   PROJECT_EMOJI=🚀
   ```
   Gmail App Password: https://myaccount.google.com/apppasswords

3. **Call the helper** from your tunnel launcher:
   ```python
   import sys, threading
   from pathlib import Path
   sys.path.insert(0, str(Path(__file__).parent / "skills" / "remote-web-email-notify"))
   from notify_email import send_notification_email

   # After parsing the public URL from your tunnel process:
   threading.Thread(
       target=send_notification_email,
       args=(public_url,),
       daemon=True
   ).start()
   ```

## API

```python
send_notification_email(
    public_url: str,                    # required — the https://… tunnel URL
    project_name: str | None = None,    # overrides PROJECT_NAME env var
    subject: str | None = None,         # overrides default subject line
    recipients: list[str] | None = None,# overrides EMAIL_RECIPIENTS
    template_path: str | None = None,   # custom HTML template with {{placeholders}}
    env_path: str | None = None,        # custom .env location
) -> bool                               # True on success, False on failure
```

Placeholders available inside `email_template.html`:

- `{{public_url}}` — the live tunnel URL
- `{{project_name}}` — from env or argument
- `{{project_emoji}}` — decorative icon
- `{{timestamp}}` — "17 Apr 2026  14:32" format
- `{{sender}}` — EMAIL_SENDER value

## Trigger on hosting events (recommended pattern)

Emitted only when the tunnel URL responds with HTTP 200. Pattern from the original script:

```python
# Poll the tunnel URL until it actually answers
ready_deadline = time.time() + 30
while time.time() < ready_deadline:
    try:
        urllib.request.urlopen(public_url + "/api/status", timeout=3)
        break
    except Exception:
        time.sleep(1)

# Then fire the email (non-blocking thread so it never stalls the launcher)
threading.Thread(target=send_notification_email, args=(public_url,), daemon=True).start()
```

## Safety notes

- The skill **never commits `.env`**. Add `.env` to `.gitignore` in every host project.
- Gmail App Passwords are scoped — revoke in Google account settings if leaked.
- If `GMAIL_APP_PASSWORD` is missing the skill logs a warning and returns `False` (does NOT crash the launcher).
- If SMTP auth fails, the skill prints a clear diagnostic instead of raising.

## Verified projects using this skill

- `PSA x Collectr Tracer` — Cloudflare Tunnel + Flask dashboard (original source)
