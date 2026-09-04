#!/usr/bin/env python3
"""
fetch_contributions.py
Scrapes the public GitHub contribution calendar (no API key needed)
and computes total contributions, current streak, longest streak,
and best day. Saves everything to data/contributions.json.
"""
import json
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

USERNAME = os.environ.get("GITHUB_PROFILE_USERNAME", "priyanshu18611")
URL = f"https://github.com/users/{USERNAME}/contributions"


def fetch_calendar():
    resp = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    days = []
    for cell in soup.select("td.ContributionCalendar-day, rect.ContributionCalendar-day"):
        date = cell.get("data-date")
        count = cell.get("data-count")
        level = cell.get("data-level")
        if date is None:
            continue
        days.append({
            "date": date,
            "count": int(count) if count is not None else 0,
            "level": int(level) if level is not None else 0,
        })
    days.sort(key=lambda d: d["date"])
    return days


def compute_metrics(days):
    total = sum(d["count"] for d in days)
    best_day = max(days, key=lambda d: d["count"], default=None)

    longest_streak = current_streak = streak = 0
    prev_date = None
    today = datetime.utcnow().date()

    for d in days:
        date = datetime.strptime(d["date"], "%Y-%m-%d").date()
        if d["count"] > 0:
            if prev_date is not None and (date - prev_date).days == 1:
                streak += 1
            else:
                streak = 1
            longest_streak = max(longest_streak, streak)
            prev_date = date
        else:
            streak = 0
            prev_date = date

    # current streak = trailing run of contribution days up to today
    for d in reversed(days):
        if d["count"] > 0:
            current_streak += 1
        else:
            break

    return {
        "total_contributions": total,
        "longest_streak": longest_streak,
        "current_streak": current_streak,
        "best_day": best_day,
        "generated_at": today.isoformat(),
    }


def main():
    days = fetch_calendar()
    metrics = compute_metrics(days)
    output = {"username": USERNAME, "days": days, "metrics": metrics}

    os.makedirs("data", exist_ok=True)
    with open("data/contributions.json", "w") as f:
        json.dump(output, f, indent=2)

    print(f"Saved data/contributions.json ({metrics['total_contributions']} contributions, "
          f"streak {metrics['current_streak']}/{metrics['longest_streak']})")


if __name__ == "__main__":
    main()
