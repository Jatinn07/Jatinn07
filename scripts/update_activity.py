#!/usr/bin/env python3
"""Generate a local, monochrome contribution calendar for the profile README."""
from __future__ import annotations

import json
import urllib.request
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "activity.svg"
USERNAME = "Jatinn07"
HEADERS = {"User-Agent": "Jatinn07-profile/1.0", "Accept": "application/vnd.github+json"}

def get_json(url: str):
    request = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))

def fetch_profile():
    data = get_json(f"https://api.github.com/users/{USERNAME}")
    return int(data.get("followers", 0)), int(data.get("following", 0))

def fetch_contributions():
    # The service returns GitHub's public daily contribution calendar as JSON.
    data = get_json(f"https://github-contributions-api.jogruber.de/v4/{USERNAME}?y=last")
    contributions = data.get("contributions")
    if not isinstance(contributions, list):
        raise ValueError("The contributions endpoint did not return a daily list.")
    total = data.get("total", {}).get("lastYear")
    if total is None:
        total = sum(int(row.get("count", 0)) for row in contributions)
    by_date = {}
    for row in contributions:
        try:
            by_date[date.fromisoformat(row["date"])] = max(0, min(4, int(row.get("level", 0))))
        except (KeyError, TypeError, ValueError):
            continue
    return int(total), by_date

def contribution_levels(by_date):
    today = date.today()
    start = today - timedelta(days=364)
    start -= timedelta(days=(start.weekday() + 1) % 7)  # Sunday, like GitHub.
    levels = {}
    for offset in range((today - start).days + 1):
        current = start + timedelta(days=offset)
        levels[(offset // 7, (current.weekday() + 1) % 7)] = by_date.get(current, 0)
    return levels

def render_svg(total, followers, following, levels):
    width, height = 1648, 190
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="1648" height="190" rx="16" fill="#070708" stroke="#39393C"/>',
        '<rect x="32" y="22" width="13" height="13" fill="#A59BAF"/>',
        '<text x="58" y="35" fill="#EAE9E7" font-family="DejaVu Sans Mono,monospace" font-size="21" letter-spacing="1">04 / GITHUB ACTIVITY</text>',
    ]
    cards = [
        (45, f"{total:,}", "CONTRIBUTIONS", "LAST 12 MONTHS"),
        (285, f"{followers:02d}", "FOLLOWERS", "GITHUB PROFILE"),
        (525, f"{following:02d}", "FOLLOWING", "GITHUB NETWORK"),
    ]
    for x, value, label, subtitle in cards:
        svg.append(f'<rect x="{x}" y="53" width="218" height="116" rx="10" fill="#0A0A0B" stroke="#343437"/>')
        svg.append(f'<text x="{x+20}" y="91" fill="#858589" font-family="DejaVu Sans Mono,monospace" font-size="13">{label}</text>')
        svg.append(f'<text x="{x+20}" y="133" fill="#F0EFED" font-family="Inter,Arial,sans-serif" font-weight="700" font-size="39">{value}</text>')
        svg.append(f'<text x="{x+20}" y="154" fill="#77777B" font-family="DejaVu Sans Mono,monospace" font-size="10" letter-spacing="1">{subtitle}</text>')

    gx, gy, cell, gap = 875, 82, 11, 4
    today = date.today()
    start = today - timedelta(days=364)
    start -= timedelta(days=(start.weekday() + 1) % 7)
    previous_month = None
    for col in range(53):
        current_month = start + timedelta(days=col * 7)
        if current_month.month != previous_month:
            month = current_month.strftime("%b").upper()
            svg.append(f'<text x="{gx+col*(cell+gap)}" y="64" fill="#88888B" font-family="DejaVu Sans Mono,monospace" font-size="11">{month}</text>')
            previous_month = current_month.month

    shades = ["#171719", "#414144", "#68686B", "#A0A0A2", "#E0E0E1"]
    for col in range(53):
        for row in range(7):
            x, y = gx + col*(cell+gap), gy + row*(cell+gap)
            if x + cell < 1612:
                level = max(0, min(4, int(levels.get((col,row), 0))))
                svg.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2" fill="{shades[level]}"/>')
    svg.append(f'<text x="{gx}" y="174" fill="#66666A" font-family="DejaVu Sans Mono,monospace" font-size="10" letter-spacing="1">{total:,} CONTRIBUTIONS IN THE LAST 12 MONTHS</text>')
    svg.append("</svg>")
    return "\n".join(svg)

def main():
    followers, following = fetch_profile()
    total, by_date = fetch_contributions()
    levels = contribution_levels(by_date)
    OUTPUT.write_text(render_svg(total, followers, following, levels), encoding="utf-8")
    print(f"Updated {OUTPUT}: {total} contributions, {followers} followers, {following} following.")

if __name__ == "__main__":
    main()
