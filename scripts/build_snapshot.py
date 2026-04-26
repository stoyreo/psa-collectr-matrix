#!/usr/bin/env python3
"""
Build a static snapshot.json from the portfolio engine.

Runs live_refresh() in-process (no Flask, no network server),
outputs JSON to web/public/snapshot.json for Vercel to serve.
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Add both scripts and parent directory to path
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from refresh_live import live_refresh
from webapp import build_response

def main():
    """Run the portfolio engine and write snapshot.json."""

    # Run the engine with static prices (no live fetch)
    print("[1/2] Running portfolio engine...")
    result = live_refresh(live_prices=None)

    # Wrap it using the same logic as /api/status
    print("[2/2] Building response...")
    payload = build_response(result, data_source="snapshot")

    # Write to web/public/snapshot.json
    output_dir = Path(__file__).parent.parent / "web" / "public"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "snapshot.json"
    output_file.write_text(
        json.dumps(payload, ensure_ascii=False, default=str, indent=2),
        encoding="utf-8"
    )

    card_count = len(payload.get("portfolio", []))
    ts = payload.get("ts_display", "unknown")
    print(f"✓ Snapshot written: {output_file.name} ({card_count} cards, {ts})")
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
