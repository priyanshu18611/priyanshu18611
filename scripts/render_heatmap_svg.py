#!/usr/bin/env python3
"""
render_heatmap_svg.py
Reads data/contributions.json and renders contrib-heatmap.svg:
a gold/dark themed contribution heatmap matching the profile theme.
"""
import json
from datetime import datetime
from collections import defaultdict

BG = "#0d0d0d"
BORDER = "#2a2a2a"
GOLD = "#D4AF37"
LEVEL_COLORS = ["#1a1a1a", "#4a3a10", "#8a6a18", "#c99820", GOLD]

CELL = 11
GAP = 3
LEFT_PAD = 40
TOP_PAD = 40


def load_data():
    with open("data/contributions.json") as f:
        return json.load(f)


def build_svg(data):
    days = data["days"]
    metrics = data["metrics"]

    weeks = defaultdict(dict)
    min_date = None
    for d in days:
        date = datetime.strptime(d["date"], "%Y-%m-%d").date()
        if min_date is None or date < min_date:
            min_date = date
        week_index = (date - min_date).days // 7
        weekday = date.weekday()  # Mon=0
        weeks[week_index][weekday] = d

    num_weeks = max(weeks.keys(), default=0) + 1
    width = LEFT_PAD + num_weeks * (CELL + GAP) + 20
    height = TOP_PAD + 7 * (CELL + GAP) + 60

    cells = []
    for w_idx, week in weeks.items():
        for wd, d in week.items():
            x = LEFT_PAD + w_idx * (CELL + GAP)
            y = TOP_PAD + wd * (CELL + GAP)
            color = LEVEL_COLORS[min(d["level"], 4)]
            cells.append(
                f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2" '
                f'fill="{color}"><title>{d["date"]}: {d["count"]} contributions</title></rect>'
            )

    footer = (f'Total: {metrics["total_contributions"]}   '
              f'Current streak: {metrics["current_streak"]}   '
              f'Longest streak: {metrics["longest_streak"]}')

    svg = f"""<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="{width}" height="{height}" rx="14" fill="{BG}" stroke="{BORDER}" stroke-width="1.5"/>
  {''.join(cells)}
  <text x="{LEFT_PAD}" y="{height - 20}" font-family="Fira Code, monospace" font-size="12" fill="{GOLD}">{footer}</text>
</svg>"""
    return svg


def main():
    data = load_data()
    svg = build_svg(data)
    with open("contrib-heatmap.svg", "w") as f:
        f.write(svg)
    print("Saved contrib-heatmap.svg")


if __name__ == "__main__":
    main()
