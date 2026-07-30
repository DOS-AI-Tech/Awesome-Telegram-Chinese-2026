#!/usr/bin/env python3
"""Validate Telegram links referenced in data/*.json.

Usage:
    python3 scripts/link_checker.py [--data-dir data] [--timeout 10] [--delay 1.0]

    # optional, but strongly recommended — see "Modes" below
    export TELEGRAM_BOT_TOKEN=123456:AAExampleTokenFromBotFather
    python3 scripts/link_checker.py

Exits non-zero if any link is found invalid, so it can be wired into CI.

Modes
-----
Public @username links (bots/channels/public groups) can be verified two ways:

1. Bot API mode (reliable) — used automatically when TELEGRAM_BOT_TOKEN is
   set. Calls the official `getChat` endpoint, which actually looks up the
   entity server-side. Create a free bot via @BotFather to get a token; the
   bot does not need to join anything to look up public entities.

2. Web-scrape fallback (best-effort only) — used when no token is
   configured, or for private invite links (t.me/+hash, t.me/joinchat/...)
   which the Bot API cannot resolve at all.

   IMPORTANT CAVEAT, confirmed by testing against real Telegram responses:
   t.me's web preview is optimistic. It renders a generic "contact
   @username" / "click to join this group" page for ANY syntactically
   valid username or invite hash, WITHOUT confirming server-side that the
   account/chat actually exists — that confirmation only happens later,
   inside the Telegram app, when the deep link (tg://resolve, tg://join)
   is actually followed. So the scrape fallback can only reliably catch:
     - malformed t.me URLs / usernames that fail Telegram's own syntax
       rules (these fall back to the plain telegram.org homepage), and
     - network-level failures (timeout, DNS error, non-200 status).
   It CANNOT reliably tell you a made-up-but-well-formed username or a
   long-expired invite link is actually invalid. Results from this mode
   are labeled "UNCONFIRMED" rather than "OK" to reflect that.
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)

BOT_API_BASE = "https://api.telegram.org"

USERNAME_RE = re.compile(r"^https?://t\.me/(?!\+|joinchat/)([A-Za-z0-9_]{5,32})/?$")
INVITE_RE = re.compile(r"^https?://t\.me/(\+[A-Za-z0-9_-]+|joinchat/[A-Za-z0-9_-]+)/?$")


@dataclass
class CheckResult:
    ok: bool
    confirmed: bool  # True if a definitive server-side answer was obtained
    reason: str


def load_entries(data_dir: Path):
    entries = []
    for json_file in sorted(data_dir.glob("*.json")):
        if json_file.name == "maintainer.json":
            continue
        try:
            items = json.loads(json_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            print(f"::warning:: failed to parse {json_file}: {exc}", file=sys.stderr)
            continue
        for item in items:
            item["_source"] = json_file.name
            entries.append(item)
    return entries


def check_via_bot_api(username: str, token: str, timeout: float) -> CheckResult:
    query = urllib.parse.urlencode({"chat_id": f"@{username}"})
    api_url = f"{BOT_API_BASE}/bot{token}/getChat?{query}"
    try:
        with urllib.request.urlopen(api_url, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        try:
            payload = json.loads(exc.read().decode("utf-8"))
        except (json.JSONDecodeError, ValueError):
            return CheckResult(ok=False, confirmed=False, reason=f"Bot API HTTP {exc.code}")
    except (urllib.error.URLError, TimeoutError) as exc:
        return CheckResult(ok=False, confirmed=False, reason=f"Bot API network error: {exc.reason}")

    if payload.get("ok"):
        return CheckResult(ok=True, confirmed=True, reason="confirmed via Bot API getChat")

    description = payload.get("description", "unknown error")
    return CheckResult(ok=False, confirmed=True, reason=f"Bot API: {description}")


def check_via_scrape(url: str, timeout: float) -> CheckResult:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            status = response.status
            body = response.read(200_000).decode("utf-8", errors="ignore")
    except urllib.error.HTTPError as exc:
        return CheckResult(ok=False, confirmed=False, reason=f"HTTP {exc.code}")
    except (urllib.error.URLError, TimeoutError) as exc:
        return CheckResult(ok=False, confirmed=False, reason=f"network error: {exc.reason}")

    if status != 200:
        return CheckResult(ok=False, confirmed=False, reason=f"HTTP {status}")

    # A real bot/channel/group preview renders a "tgme_page_wrap" block.
    # A malformed username/invite instead falls back to the plain
    # telegram.org homepage, which has no tgme_page_wrap at all. This is a
    # weak signal — see the module docstring for what it cannot catch.
    if "tgme_page_wrap" not in body:
        return CheckResult(ok=False, confirmed=False, reason="no tgme_page_wrap block found (malformed link)")

    return CheckResult(ok=True, confirmed=False, reason="page reachable, existence unconfirmed")


def check_url(url: str, token: str | None, timeout: float) -> CheckResult:
    username_match = USERNAME_RE.match(url)
    if username_match and token:
        return check_via_bot_api(username_match.group(1), token, timeout)
    return check_via_scrape(url, timeout)


TME_RE = re.compile(r"^https?://t\.me/")


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--data-dir", default="data", type=Path)
    parser.add_argument("--timeout", default=10.0, type=float)
    parser.add_argument("--delay", default=1.0, type=float, help="seconds between requests, be polite")
    args = parser.parse_args()

    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if token:
        print("Using Telegram Bot API for public @username links (reliable mode).\n")
    else:
        print(
            "No TELEGRAM_BOT_TOKEN set — falling back to web-scrape heuristic "
            "for @username links. This mode cannot reliably confirm a "
            "made-up-but-well-formed username is invalid; see the script's "
            "docstring. Set TELEGRAM_BOT_TOKEN for real validation.\n"
        )

    entries = load_entries(args.data_dir)
    if not entries:
        print(f"No entries found under {args.data_dir}/*.json")
        return 0

    failures = []
    unconfirmed = 0
    for i, entry in enumerate(entries):
        url = entry.get("url", "")
        name = entry.get("name", url)
        if not TME_RE.match(url):
            print(f"[SKIP]       {name} -> {url} (not a t.me link)")
            continue

        result = check_url(url, token, args.timeout)
        if result.ok and result.confirmed:
            label = "OK"
        elif result.ok:
            label = "UNCONFIRMED"
            unconfirmed += 1
        else:
            label = "FAIL"
        print(f"[{label:11}] {name} -> {url} ({result.reason})")
        if not result.ok:
            failures.append((entry.get("_source"), name, url, result.reason))

        if i < len(entries) - 1:
            time.sleep(args.delay)

    print()
    if failures:
        print(f"{len(failures)} link(s) failed validation:")
        for source, name, url, reason in failures:
            print(f"  - [{source}] {name} ({url}): {reason}")
        return 1

    checked = sum(1 for e in entries if TME_RE.match(e.get("url", "")))
    print(f"All {checked} checked link(s) passed ({unconfirmed} unconfirmed — see notes above).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
