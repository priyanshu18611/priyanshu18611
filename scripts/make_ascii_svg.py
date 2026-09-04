#!/usr/bin/env python3
"""
make_ascii_svg.py
Converts source-prepped.png into hxni-ascii.svg: a gold monospace
ASCII-art portrait in a dark terminal card, with a line-by-line
CSS keyframe reveal (SMIL clipPath wipe for GitHub <img> compatibility).
"""
from PIL import Image

RAMP = " .:-=+*cs#%@"
COLS = 90
CHAR_W = 6.2
CHAR_H = 11
GOLD = "#D4AF37"
BG = "#0d0d0d"
BORDER = "#2a2a2a"


def image_to_ascii(path: str, cols: int = COLS):
    img = Image.open(path).convert("L")
    aspect = img.height / img.width
    rows = int(cols * aspect * 0.5)  # correct for character aspect ratio
    img = img.resize((cols, rows))
    pixels = img.getdata()
    chars = []
    for i, p in enumerate(pixels):
        idx = int((p / 255) * (len(RAMP) - 1))
        chars.append(RAMP[idx])
    lines = ["".join(chars[i:i + cols]) for i in range(0, len(chars), cols)]
    return lines


def escape(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;"))


def build_svg(lines):
    width = int(COLS * CHAR_W) + 60
    height = int(len(lines) * CHAR_H) + 80

    text_elems = []
    for i, line in enumerate(lines):
        y = 50 + i * CHAR_H
        delay = round(i * 0.03, 2)
        text_elems.append(
            f'<text x="30" y="{y}" class="ascii-line" '
            f'style="animation-delay:{delay}s">{escape(line)}</text>'
        )

    svg = f"""<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      .ascii-line {{
        font-family: 'Fira Code', 'Courier New', monospace;
        font-size: 9px;
        fill: {GOLD};
        white-space: pre;
        opacity: 0;
        animation: fin 0.6s ease-out forwards;
      }}
      @keyframes fin {{
        from {{ opacity: 0; }}
        to {{ opacity: 1; }}
      }}
    </style>
  </defs>
  <rect x="0" y="0" width="{width}" height="{height}" rx="14" fill="{BG}" stroke="{BORDER}" stroke-width="1.5"/>
  <circle cx="24" cy="22" r="5" fill="#ff5f56"/>
  <circle cx="42" cy="22" r="5" fill="#ffbd2e"/>
  <circle cx="60" cy="22" r="5" fill="#27c93f"/>
  {''.join(text_elems)}
</svg>"""
    return svg


def main():
    lines = image_to_ascii("source-prepped.png")
    svg = build_svg(lines)
    with open("hxni-ascii.svg", "w") as f:
        f.write(svg)
    print("Saved hxni-ascii.svg")


if __name__ == "__main__":
    main()
