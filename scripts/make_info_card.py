#!/usr/bin/env python3
"""
make_info_card.py
Generates info-card.svg: a neofetch-style terminal card with
gold key labels and silver values, staggered fade-in animation.
"""

GOLD = "#D4AF37"
SILVER = "#C0C0C0"
BG = "#0d0d0d"
BORDER = "#2a2a2a"

INFO = [
    ("OS", "Bihar/India OS 5.0 LTS"),
    ("Host", "Shershah Engineering College"),
    ("Role", "Full-Stack Developer / ML Enthusiast"),
    ("Stack", "MERN, Flask, TensorFlow, SQL, Power BI"),
    ("Email", "priyanshu6202018611@gmail.com"),
    ("LinkedIn", "linkedin.com/in/priyanshuroy18"),
    ("GitHub", "github.com/priyanshu18611"),
    ("Portfolio", "priyanshu18611.github.io/portfolio"),
]

WIDTH = 520
LINE_H = 34
TOP_PAD = 70


def escape(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;"))


def build_svg():
    height = TOP_PAD + len(INFO) * LINE_H + 30
    rows = []
    for i, (key, value) in enumerate(INFO):
        y = TOP_PAD + i * LINE_H
        delay = round(i * 0.12, 2)
        rows.append(f"""
  <g class="info-row" style="animation-delay:{delay}s">
    <text x="30" y="{y}" font-family="Fira Code, monospace" font-size="14" fill="{GOLD}" font-weight="bold">{escape(key)}</text>
    <text x="160" y="{y}" font-family="Fira Code, monospace" font-size="14" fill="{SILVER}">{escape(value)}</text>
  </g>""")

    svg = f"""<svg width="{WIDTH}" height="{height}" viewBox="0 0 {WIDTH} {height}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      .info-row {{
        opacity: 0;
        animation: fadeInRow 0.5s ease-out forwards;
      }}
      @keyframes fadeInRow {{
        from {{ opacity: 0; transform: translateX(-6px); }}
        to {{ opacity: 1; transform: translateX(0); }}
      }}
    </style>
  </defs>
  <rect x="0" y="0" width="{WIDTH}" height="{height}" rx="14" fill="{BG}" stroke="{BORDER}" stroke-width="1.5"/>
  <circle cx="24" cy="22" r="5" fill="#ff5f56"/>
  <circle cx="42" cy="22" r="5" fill="#ffbd2e"/>
  <circle cx="60" cy="22" r="5" fill="#27c93f"/>
  <text x="90" y="27" font-family="Fira Code, monospace" font-size="13" fill="{GOLD}">The Cipher Stack</text>
  <line x1="20" y1="45" x2="{WIDTH - 20}" y2="45" stroke="{BORDER}" stroke-width="1"/>
  {''.join(rows)}
</svg>"""
    return svg


def main():
    svg = build_svg()
    with open("info-card.svg", "w") as f:
        f.write(svg)
    print("Saved info-card.svg")


if __name__ == "__main__":
    main()
