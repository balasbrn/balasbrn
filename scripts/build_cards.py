#!/usr/bin/env python3
"""Render the profile's stats, languages and activity cards as SVG files.

Runs in GitHub Actions (see .github/workflows/profile-cards.yml) and writes
assets/generated/{stats,languages,activity}-{dark,light}.svg. The SVGs are
committed to this repo, so the profile never depends on a third-party card
service being up.

Standard library only. Token: METRICS_TOKEN (a fine-grained PAT, optional,
lets private repos count toward languages) or else GITHUB_TOKEN.

    python scripts/build_cards.py               # live data from the GitHub API
    python scripts/build_cards.py --sample      # synthetic data, for a local preview
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import random
import sys
import urllib.request
from html import escape
from pathlib import Path

LOGIN = os.environ.get("PROFILE_LOGIN", "balasbrn")
OUT = Path(__file__).resolve().parent.parent / "assets" / "generated"
# Generated report pages and notebooks inflate byte counts without saying
# much about the code, so they are left out of the language card.
EXCLUDED_LANGUAGES = {"HTML", "CSS", "Jupyter Notebook", "Makefile", "Dockerfile", "Shell", "PowerShell", "Batchfile"}
TOP_LANGUAGES = 6

THEMES = {
    "dark": {
        "bg": "#0d1117", "border": "#30363d", "title": "#e6edf3", "text": "#c9d1d9",
        "muted": "#8b949e", "accent": "#2dd4bf", "accent2": "#f59e0b",
        "ramp": ["#161b22", "#0f3d3a", "#14706a", "#1fa99c", "#5eead4"],
    },
    "light": {
        "bg": "#ffffff", "border": "#d0d7de", "title": "#1f2328", "text": "#24292f",
        "muted": "#57606a", "accent": "#0f766e", "accent2": "#b45309",
        "ramp": ["#ebedf0", "#b2ece5", "#5fcfc1", "#14a394", "#0b5f57"],
    },
}
FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,monospace"

QUERY = """
query($login: String!, $cursor: String) {
  user(login: $login) {
    contributionsCollection {
      totalCommitContributions
      totalPullRequestContributions
      totalPullRequestReviewContributions
      totalIssueContributions
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
    repositories(first: 100, after: $cursor, ownerAffiliations: OWNER, isFork: false) {
      pageInfo { hasNextPage endCursor }
      nodes {
        isPrivate
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name color } }
        }
      }
    }
  }
}
"""


# --------------------------------------------------------------------- data

def graphql(token: str, variables: dict) -> dict:
    body = json.dumps({"query": QUERY, "variables": variables}).encode()
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=body,
        headers={"Authorization": f"bearer {token}", "User-Agent": "profile-cards"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        payload = json.load(resp)
    if payload.get("errors"):
        raise RuntimeError(payload["errors"])
    return payload["data"]["user"]


def fetch_live(token: str) -> dict:
    cursor = None
    first = None
    languages: dict[str, dict] = {}
    while True:
        user = graphql(token, {"login": LOGIN, "cursor": cursor})
        first = first or user
        for repo in user["repositories"]["nodes"]:
            for edge in repo["languages"]["edges"]:
                name = edge["node"]["name"]
                entry = languages.setdefault(name, {"size": 0, "color": edge["node"]["color"] or "#8b949e"})
                entry["size"] += edge["size"]
        page = user["repositories"]["pageInfo"]
        if not page["hasNextPage"]:
            break
        cursor = page["endCursor"]
    cc = first["contributionsCollection"]
    days = [
        (dt.date.fromisoformat(d["date"]), d["contributionCount"])
        for w in cc["contributionCalendar"]["weeks"]
        for d in w["contributionDays"]
    ]
    return {
        "total": cc["contributionCalendar"]["totalContributions"],
        "commits": cc["totalCommitContributions"],
        "prs": cc["totalPullRequestContributions"],
        "reviews": cc["totalPullRequestReviewContributions"],
        "days": days,
        "languages": languages,
    }


def fetch_sample() -> dict:
    rng = random.Random(42)
    today = dt.date.today()
    start = today - dt.timedelta(days=364 + (today.weekday() + 1) % 7)
    days = []
    for i in range((today - start).days + 1):
        d = start + dt.timedelta(days=i)
        ramp = i / 365  # activity grows through the year
        active = rng.random() < 0.25 + 0.6 * ramp
        days.append((d, rng.randint(1, int(3 + 14 * ramp)) if active else 0))
    total = sum(c for _, c in days)
    return {
        "total": total, "commits": int(total * 0.8), "prs": 214, "reviews": 37, "days": days,
        "languages": {
            "Python": {"size": 4_200_000, "color": "#3572A5"},
            "C#": {"size": 900_000, "color": "#178600"},
            "TypeScript": {"size": 650_000, "color": "#3178c6"},
            "C": {"size": 300_000, "color": "#555555"},
            "C++": {"size": 120_000, "color": "#f34b7d"},
            "Rust": {"size": 60_000, "color": "#dea584"},
        },
    }


def streaks(days: list[tuple[dt.date, int]]) -> tuple[int, int]:
    longest = run = 0
    for _, count in days:
        run = run + 1 if count else 0
        longest = max(longest, run)
    current = 0
    tail = list(reversed(days))
    if tail and tail[0][1] == 0:  # today may simply not have started yet
        tail = tail[1:]
    for _, count in tail:
        if not count:
            break
        current += 1
    return current, longest


# --------------------------------------------------------------------- cards

def frame(width: int, height: int, t: dict, title: str, body: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="{escape(title)}">'
        f'<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="10" '
        f'fill="{t["bg"]}" stroke="{t["border"]}"/>'
        f'<text x="24" y="36" font-family="{FONT}" font-size="15" font-weight="600" '
        f'fill="{t["title"]}">{escape(title)}</text>{body}</svg>\n'
    )


def stats_card(data: dict, t: dict) -> str:
    current, longest = streaks(data["days"])
    active = sum(1 for _, c in data["days"] if c)
    rows = [
        ("Contributions", f'{data["total"]:,}'),
        ("Public commits", f'{data["commits"]:,}'),
        ("Pull requests", f'{data["prs"]:,}'),
        ("Active days", f"{active} / {len(data['days'])}"),
        ("Current streak", f"{current} day" + ("" if current == 1 else "s")),
        ("Longest streak", f"{longest} day" + ("" if longest == 1 else "s")),
    ]
    body = []
    for i, (label, value) in enumerate(rows):
        col, row = divmod(i, 3)
        x, y = 24 + col * 220, 70 + row * 44
        body.append(
            f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="12" fill="{t["muted"]}">{label}</text>'
            f'<text x="{x}" y="{y + 20}" font-family="{MONO}" font-size="18" font-weight="600" '
            f'fill="{t["accent"] if i < 3 else t["text"]}">{escape(value)}</text>'
        )
    return frame(460, 200, t, "Activity · last 12 months", "".join(body))


def languages_card(data: dict, t: dict) -> str:
    langs = {k: v for k, v in data["languages"].items() if k not in EXCLUDED_LANGUAGES}
    top = sorted(langs.items(), key=lambda kv: kv[1]["size"], reverse=True)[:TOP_LANGUAGES]
    total = sum(v["size"] for _, v in top) or 1
    body, x = [], 24.0
    width = 412
    body.append(f'<clipPath id="bar"><rect x="24" y="60" width="{width}" height="10" rx="5"/></clipPath><g clip-path="url(#bar)">')
    for name, v in top:
        w = width * v["size"] / total
        body.append(f'<rect x="{x:.2f}" y="60" width="{w + 0.5:.2f}" height="10" fill="{v["color"]}"/>')
        x += w
    body.append("</g>")
    for i, (name, v) in enumerate(top):
        col, row = divmod(i, 3)
        lx, ly = 24 + col * 220, 104 + row * 30
        pct = 100 * v["size"] / total
        body.append(
            f'<circle cx="{lx + 5}" cy="{ly - 4}" r="5" fill="{v["color"]}"/>'
            f'<text x="{lx + 18}" y="{ly}" font-family="{FONT}" font-size="13" fill="{t["text"]}">{escape(name)}</text>'
            f'<text x="{lx + 190}" y="{ly}" text-anchor="end" font-family="{MONO}" font-size="12" '
            f'fill="{t["muted"]}">{pct:.1f}%</text>'
        )
    return frame(460, 200, t, "Languages · by code size", "".join(body))


def activity_card(data: dict, t: dict) -> str:
    days = data["days"]
    cell, gap = 11, 3
    left, top = 44, 70
    max_count = max((c for _, c in days), default=0) or 1
    first = days[0][0]
    offset = (first.weekday() + 1) % 7  # GitHub weeks start on Sunday
    body, months_seen = [], set()
    for i, (d, count) in enumerate(days):
        week, dow = divmod(i + offset, 7)
        level = 0 if count == 0 else 1 + min(3, int(4 * count / (max_count + 1)))
        x, y = left + week * (cell + gap), top + dow * (cell + gap)
        body.append(
            f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2" fill="{t["ramp"][level]}">'
            f"<title>{d.isoformat()}: {count}</title></rect>"
        )
        if d.day <= 7 and dow == 0 and (d.year, d.month) not in months_seen:
            months_seen.add((d.year, d.month))
            body.append(
                f'<text x="{x}" y="{top - 8}" font-family="{FONT}" font-size="10" '
                f'fill="{t["muted"]}">{d.strftime("%b")}</text>'
            )
    for dow, label in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        body.append(
            f'<text x="{left - 8}" y="{top + dow * (cell + gap) + 9}" text-anchor="end" '
            f'font-family="{FONT}" font-size="10" fill="{t["muted"]}">{label}</text>'
        )
    weeks = (len(days) + offset + 6) // 7
    width = left + weeks * (cell + gap) + 24
    legend_y = top + 7 * (cell + gap) + 18
    lx = width - 24 - 5 * (cell + gap) - 70
    body.append(f'<text x="{lx}" y="{legend_y + 9}" font-family="{FONT}" font-size="10" fill="{t["muted"]}">Less</text>')
    for i, colour in enumerate(t["ramp"]):
        body.append(f'<rect x="{lx + 30 + i * (cell + gap)}" y="{legend_y}" width="{cell}" height="{cell}" rx="2" fill="{colour}"/>')
    body.append(
        f'<text x="{lx + 30 + 5 * (cell + gap) + 4}" y="{legend_y + 9}" font-family="{FONT}" font-size="10" fill="{t["muted"]}">More</text>'
        f'<text x="24" y="{legend_y + 9}" font-family="{FONT}" font-size="11" fill="{t["muted"]}">'
        f'{data["total"]:,} contributions · updated {dt.date.today().isoformat()}</text>'
    )
    return frame(width, legend_y + 30, t, "Contribution calendar", "".join(body))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--sample", action="store_true", help="use synthetic data instead of the API")
    parser.add_argument("--out", type=Path, default=OUT)
    args = parser.parse_args()

    if args.sample:
        data = fetch_sample()
    else:
        token = os.environ.get("METRICS_TOKEN") or os.environ.get("GITHUB_TOKEN")
        if not token:
            print("Set METRICS_TOKEN or GITHUB_TOKEN, or pass --sample.", file=sys.stderr)
            return 1
        data = fetch_live(token)

    args.out.mkdir(parents=True, exist_ok=True)
    for name, theme in THEMES.items():
        (args.out / f"stats-{name}.svg").write_text(stats_card(data, theme), encoding="utf-8")
        (args.out / f"languages-{name}.svg").write_text(languages_card(data, theme), encoding="utf-8")
        (args.out / f"activity-{name}.svg").write_text(activity_card(data, theme), encoding="utf-8")
    print(f"Wrote 6 cards to {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
