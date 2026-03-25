"""
Yahoo Email Analysis Agent — Read Only
=======================================
This agent reads your Yahoo inbox, analyzes each email with Claude,
and prints a report. It does NOT delete, move, or send anything.

Requirements:
    pip install anthropic

Yahoo App Password setup:
    1. Go to https://login.yahoo.com/account/security
    2. Scroll to "App passwords" and click Generate
    3. Name it "Python Agent" and copy the password
    4. Paste it below as YAHOO_APP_PASSWORD

Usage:
    python email_agent.py
"""

import imaplib
import email
from email.header import decode_header
from datetime import datetime
import anthropic

# ── CONFIG ───────────────────────────────────────────────────────────────────

YAHOO_EMAIL        = "your_email@rocketmail.com"    # <-- your Yahoo email
YAHOO_APP_PASSWORD = "your_app_password_here"       # <-- your Yahoo app password (NOT your real password)
ANTHROPIC_API_KEY  = "your_anthropic_api_key_here"  # <-- your Anthropic API key

EMAILS_TO_FETCH    = 50

# ── COLORS ───────────────────────────────────────────────────────────────────

GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
RESET  = "\033[0m"

# ── EMAIL FETCHING ────────────────────────────────────────────────────────────

def decode_str(value):
    """Safely decode an email header string."""
    if value is None:
        return ""
    decoded, encoding = decode_header(value)[0]
    if isinstance(decoded, bytes):
        return decoded.decode(encoding or "utf-8", errors="replace")
    return decoded


def get_email_body(msg):
    """Extract plain text body from an email message."""
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                try:
                    body = part.get_payload(decode=True).decode("utf-8", errors="replace")
                    break
                except Exception:
                    continue
    else:
        try:
            body = msg.get_payload(decode=True).decode("utf-8", errors="replace")
        except Exception:
            body = ""
    # Trim long bodies — we only need enough for Claude to make a decision
    return body.strip()[:1500]


def fetch_emails():
    """Connect to Yahoo via IMAP and fetch the most recent emails."""
    print(f"\n{CYAN}Connecting to Yahoo Mail...{RESET}")

    try:
        mail = imaplib.IMAP4_SSL("imap.mail.yahoo.com", 993)
        mail.login(YAHOO_EMAIL, YAHOO_APP_PASSWORD)
        mail.select("INBOX", readonly=True)  # readonly=True means we CANNOT modify anything
    except imaplib.IMAP4.error as e:
        print(f"{RED}Login failed: {e}{RESET}")
        print(f"{YELLOW}Make sure you're using an App Password, not your real Yahoo password.{RESET}")
        return []

    # Fetch the most recent N email IDs
    _, data = mail.search(None, "ALL")
    email_ids = data[0].split()
    recent_ids = email_ids[-EMAILS_TO_FETCH:]  # last 50

    emails = []
    total = len(recent_ids)

    print(f"{CYAN}Fetching {total} emails...{RESET}\n")

    for i, eid in enumerate(reversed(recent_ids), 1):  # newest first
        _, msg_data = mail.fetch(eid, "(RFC822)")
        raw = msg_data[0][1]
        msg = email.message_from_bytes(raw)

        sender  = decode_str(msg.get("From", ""))
        subject = decode_str(msg.get("Subject", "(no subject)"))
        date    = msg.get("Date", "")
        body    = get_email_body(msg)

        emails.append({
            "id": i,
            "sender":  sender,
            "subject": subject,
            "date":    date,
            "body":    body,
        })

        print(f"  {DIM}Fetched {i}/{total}: {subject[:60]}{RESET}", end="\r")

    mail.logout()
    print(f"\n{GREEN}✓ Fetched {total} emails successfully.{RESET}\n")
    return emails


# ── CLAUDE ANALYSIS ───────────────────────────────────────────────────────────

def analyze_email(client, em):
    """Send a single email to Claude and get a category + reason."""

    prompt = f"""Analyze this email and classify it into exactly one of these categories:
- NORMAL: Legitimate email (personal, work, receipts, notifications from known services)
- UNSUBSCRIBE: Marketing, newsletters, promotions — not harmful but likely unwanted clutter
- SPAM: Unsolicited junk, suspicious offers, or unclear origin
- MALWARE: Phishing attempts, suspicious links, fake alerts, scams, or anything potentially dangerous

Respond in this exact format (nothing else):
CATEGORY: <one of: NORMAL, UNSUBSCRIBE, SPAM, MALWARE>
REASON: <one sentence explaining why>

Email details:
From: {em['sender']}
Subject: {em['subject']}
Date: {em['date']}
Body preview:
{em['body'][:800]}
"""

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=100,
        messages=[{"role": "user", "content": prompt}],
    )

    text = response.content[0].text.strip()

    # Parse the response
    category = "NORMAL"
    reason   = "Could not parse response."

    for line in text.splitlines():
        if line.startswith("CATEGORY:"):
            category = line.replace("CATEGORY:", "").strip()
        elif line.startswith("REASON:"):
            reason = line.replace("REASON:", "").strip()

    return category, reason


# ── REPORT PRINTING ───────────────────────────────────────────────────────────

def print_report(results):
    """Print a clean grouped report to the terminal."""

    normal      = [r for r in results if r["category"] == "NORMAL"]
    unsubscribe = [r for r in results if r["category"] == "UNSUBSCRIBE"]
    spam        = [r for r in results if r["category"] == "SPAM"]
    malware     = [r for r in results if r["category"] == "MALWARE"]

    divider = "─" * 65

    print(f"\n{BOLD}{'═' * 65}")
    print(f"  EMAIL ANALYSIS REPORT — {YAHOO_EMAIL}")
    print(f"{'═' * 65}{RESET}\n")

    # ── NORMAL ──
    print(f"{GREEN}{BOLD}✅  NORMAL  ({len(normal)} emails){RESET}")
    print(divider)
    if normal:
        for r in normal:
            print(f"  {BOLD}{r['subject'][:55]}{RESET}")
            print(f"  {DIM}From: {r['sender'][:55]}{RESET}")
            print(f"  {DIM}→ {r['reason']}{RESET}\n")
    else:
        print(f"  {DIM}None{RESET}\n")

    # ── UNSUBSCRIBE ──
    print(f"{YELLOW}{BOLD}📧  UNSUBSCRIBE CANDIDATES  ({len(unsubscribe)} emails){RESET}")
    print(divider)
    if unsubscribe:
        for r in unsubscribe:
            print(f"  {BOLD}{r['subject'][:55]}{RESET}")
            print(f"  {DIM}From: {r['sender'][:55]}{RESET}")
            print(f"  {DIM}→ {r['reason']}{RESET}\n")
    else:
        print(f"  {DIM}None{RESET}\n")

    # ── SPAM ──
    print(f"{RED}{BOLD}🚨  SPAM  ({len(spam)} emails){RESET}")
    print(divider)
    if spam:
        for r in spam:
            print(f"  {BOLD}{r['subject'][:55]}{RESET}")
            print(f"  {DIM}From: {r['sender'][:55]}{RESET}")
            print(f"  {DIM}→ {r['reason']}{RESET}\n")
    else:
        print(f"  {DIM}None{RESET}\n")

    # ── MALWARE ──
    print(f"{RED}{BOLD}☠️   MALWARE / PHISHING  ({len(malware)} emails){RESET}")
    print(divider)
    if malware:
        for r in malware:
            print(f"  {BOLD}{r['subject'][:55]}{RESET}")
            print(f"  {DIM}From: {r['sender'][:55]}{RESET}")
            print(f"  {DIM}→ {r['reason']}{RESET}\n")
    else:
        print(f"  {DIM}None{RESET}\n")

    # ── SUMMARY ──
    print(f"{'═' * 65}")
    print(f"{BOLD}  SUMMARY{RESET}")
    print(f"{'═' * 65}")
    print(f"  ✅  Normal:               {len(normal)}")
    print(f"  📧  Unsubscribe:          {len(unsubscribe)}")
    print(f"  🚨  Spam:                 {len(spam)}")
    print(f"  ☠️   Malware / Phishing:   {len(malware)}")
    print(f"  {'─' * 30}")
    print(f"  📬  Total analyzed:       {len(results)}")
    print(f"{'═' * 65}\n")
    print(f"{DIM}This report is read-only. Nothing in your inbox was modified.{RESET}\n")


# ── REPORT SAVING ─────────────────────────────────────────────────────────────

def save_report(results):
    """Save a plain-text version of the report to a timestamped file."""

    normal      = [r for r in results if r["category"] == "NORMAL"]
    unsubscribe = [r for r in results if r["category"] == "UNSUBSCRIBE"]
    spam        = [r for r in results if r["category"] == "SPAM"]
    malware     = [r for r in results if r["category"] == "MALWARE"]

    divider = "─" * 65
    lines = []

    lines.append("=" * 65)
    lines.append(f"  EMAIL ANALYSIS REPORT — {YAHOO_EMAIL}")
    lines.append(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("=" * 65)
    lines.append("")

    for label, group in [
        ("NORMAL", normal),
        ("UNSUBSCRIBE CANDIDATES", unsubscribe),
        ("SPAM", spam),
        ("MALWARE / PHISHING", malware),
    ]:
        lines.append(f"{label}  ({len(group)} emails)")
        lines.append(divider)
        if group:
            for r in group:
                lines.append(f"  {r['subject'][:55]}")
                lines.append(f"  From: {r['sender'][:55]}")
                lines.append(f"  -> {r['reason']}")
                lines.append("")
        else:
            lines.append("  None")
            lines.append("")

    lines.append("=" * 65)
    lines.append("  SUMMARY")
    lines.append("=" * 65)
    lines.append(f"  Normal:              {len(normal)}")
    lines.append(f"  Unsubscribe:         {len(unsubscribe)}")
    lines.append(f"  Spam:                {len(spam)}")
    lines.append(f"  Malware / Phishing:  {len(malware)}")
    lines.append(f"  {'─' * 30}")
    lines.append(f"  Total analyzed:      {len(results)}")
    lines.append("=" * 65)
    lines.append("")
    lines.append("This report is read-only. Nothing in your inbox was modified.")

    filename = f"email_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return filename


# ── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    print(f"\n{BOLD}Yahoo Email Analysis Agent{RESET}")
    print(f"{DIM}Read-only mode — your inbox will not be modified.{RESET}")

    # 1. Fetch emails
    emails = fetch_emails()
    if not emails:
        return

    # 2. Analyze each email with Claude
    client  = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    results = []
    total   = len(emails)

    print(f"{CYAN}Analyzing {total} emails with Claude...{RESET}\n")

    for i, em in enumerate(emails, 1):
        print(f"  {DIM}Analyzing {i}/{total}: {em['subject'][:55]}{RESET}", end="\r")
        category, reason = analyze_email(client, em)
        results.append({**em, "category": category, "reason": reason})

    print(f"\n{GREEN}✓ Analysis complete.{RESET}")

    # 3. Print the report
    print_report(results)

    # 4. Save the report to a text file
    filename = save_report(results)
    print(f"{GREEN}✓ Report saved to: {filename}{RESET}\n")


if __name__ == "__main__":
    main()
