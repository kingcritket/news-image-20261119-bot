"""Build entry.png for news-image-20261119 from three AI-generated scene
photos (assets/, no text baked in) plus PIL-drawn text.

Layout (1024x1024, mirrors the 18 Nov entry): navy date header, 2x2 grid
of three photo stories + an "ALSO TODAY" strip, navy footer. Every word on
the image is drawn here in Liberation Sans; the photos carry no text.

Stories, all verified against reporting of 19 November 2026:
  1. Trump, Xi & Putin meet in Shenzhen - first-ever trilateral, APEC
     (Yonhap, 19 Nov; Reuters, 18 Nov; China Foreign Ministry).
  2. Iran hits a U.S. base in Kuwait - drones target the Patriot site at
     Ali Al Salem; Bahrain intercepts another attack (Reuters, 19 Nov).
  3. GTA VI rolls out worldwide - midnight local launches from New
     Zealand; 17m+ copies, $1.65bn pre-release sales (Reuters, 19 Nov).
Strip: Jeffries picked as Speaker nominee 251-11; Cyclone Akvan nears
India (landfall due 20 Nov); NASA briefs on Voyager 1's one-light-day
milestone today; India and Japan hold 2+2 defence talks in Tokyo.
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")

NAVY = (26, 38, 92)
NAVY_DARK = (18, 28, 70)
GOLD = (212, 175, 55)
BG = (245, 243, 238)
PANEL_BORDER = (205, 200, 190)
INK = (26, 38, 92)
SUB_INK = (90, 90, 90)
WHITE = (255, 255, 255)

FONT_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_font(draw, text, path, start, max_width):
    """Largest bold size at or below `start` that fits `max_width`."""
    size = start
    while size > 10:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_width:
            return f
        size -= 1
    return font(path, size)


def wrap(draw, text, f, max_width):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=f) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def photo_panel(canvas, draw, img, box, headline, sub):
    """One photo story panel: image on top, headline + sub below."""
    x, y, w, h = box
    img_h = 320
    cap_h = h - img_h
    photo = img.resize((w, img_h), Image.LANCZOS)
    canvas.paste(photo, (x, y))
    draw.rectangle([x, y + img_h, x + w, y + h], fill=WHITE)
    draw.rectangle([x, y, x + w, y + h], outline=PANEL_BORDER, width=2)
    pad = 16
    max_w = w - 2 * pad
    hf = fit_font(draw, headline, FONT_BOLD, 31, max_w)
    draw.text((x + pad, y + img_h + 12), headline, font=hf, fill=INK)
    sf = font(FONT_REG, 18)
    lines = wrap(draw, sub, sf, max_w)
    ty = y + img_h + 12 + hf.size + 8
    for line in lines:
        draw.text((x + pad, ty), line, font=sf, fill=SUB_INK)
        ty += 23


def ring_icon(draw, cx, cy, r, colour, kind):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=colour, width=4)
    if kind == "capitol":
        # simple dome: arc + base line
        draw.arc([cx - r + 8, cy - r + 10, cx + r - 8, cy + r - 4],
                 start=180, end=360, fill=colour, width=4)
        draw.line([cx - r + 10, cy + 6, cx + r - 10, cy + 6],
                  fill=colour, width=4)
        draw.line([cx, cy - r + 12, cx, cy - r + 2], fill=colour, width=4)
    elif kind == "cyclone":
        draw.arc([cx - r + 8, cy - r + 8, cx + r - 8, cy + r - 8],
                 start=0, end=270, fill=colour, width=4)
        draw.arc([cx - r + 16, cy - r + 16, cx + r - 16, cy + r - 16],
                 start=90, end=360, fill=colour, width=4)
    elif kind == "planet":
        draw.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=colour)
        draw.line([cx - r + 4, cy + 8, cx + r - 4, cy - 8],
                  fill=colour, width=4)
    elif kind == "globe":
        draw.ellipse([cx - r + 8, cy - r + 8, cx + r - 8, cy + r - 8],
                     outline=colour, width=4)
        draw.line([cx, cy - r + 8, cx, cy + r - 8], fill=colour, width=3)


def strip_item(draw, x, y, w, icon, colour, kind, head, sub):
    ring_icon(draw, x + 26, y + 26, 22, colour, kind)
    tx = x + 62
    max_w = w - 62 - 8
    hf = fit_font(draw, head, FONT_BOLD, 25, max_w)
    draw.text((tx, y + 2), head, font=hf, fill=INK)
    sf = font(FONT_REG, 17)
    lines = wrap(draw, sub, sf, max_w)
    ty = y + 2 + hf.size + 6
    for line in lines:
        draw.text((tx, ty), line, font=sf, fill=SUB_INK)
        ty += 21
    return ty


def main():
    canvas = Image.new("RGB", (1024, 1024), BG)
    draw = ImageDraw.Draw(canvas)

    # Header: date band + gold rule.
    draw.rectangle([0, 0, 1024, 96], fill=NAVY)
    date_font = fit_font(draw, "THURSDAY, 19 NOVEMBER 2026",
                         FONT_BOLD, 62, 1024 - 48)
    tw = draw.textlength("THURSDAY, 19 NOVEMBER 2026", font=date_font)
    draw.text(((1024 - tw) / 2, 96 // 2 - date_font.size // 2 - 4),
              "THURSDAY, 19 NOVEMBER 2026", font=date_font, fill=WHITE)
    draw.rectangle([0, 96, 1024, 100], fill=GOLD)

    summit = Image.open(os.path.join(
        ASSETS,
        "media-generation-shenzhen-summit-0-d07aa62f-eed1-44d8-9bf9-06ba2faebea8.webp"
    )).convert("RGB")
    kuwait = Image.open(os.path.join(
        ASSETS,
        "media-generation-kuwait-base-night-0-ce8e839c-c296-473e-8428-370cae678660.webp"
    )).convert("RGB")
    vice = Image.open(os.path.join(
        ASSETS,
        "media-generation-vice-city-neon-0-78eb6891-2e75-4ab1-83ae-c67c6f3d8e63.webp"
    )).convert("RGB")

    # Top row: Shenzhen trilateral | Iran hits Kuwait base.
    photo_panel(canvas, draw, summit, (24, 116, 480, 420),
                "TRUMP, XI & PUTIN MEET",
                "FIRST-EVER TRILATERAL IN SHENZHEN AT THE APEC SUMMIT")
    photo_panel(canvas, draw, kuwait, (520, 116, 480, 420),
                "IRAN HITS U.S. BASE IN KUWAIT",
                "DRONES TARGET PATRIOT SITE AT ALI AL SALEM; BAHRAIN INTERCEPTS ANOTHER ATTACK")

    # Bottom-left: GTA VI rollout.
    photo_panel(canvas, draw, vice, (24, 552, 480, 420),
                "GTA VI ROLLS OUT WORLDWIDE",
                "13-YEAR WAIT ENDS \u2014 17M COPIES, $1.65BN ALREADY SOLD")

    # Bottom-right: also today.
    x, y, w, h = 520, 552, 480, 420
    draw.rectangle([x, y, x + w, y + h], fill=WHITE)
    draw.rectangle([x, y, x + w, y + h], outline=PANEL_BORDER, width=2)
    draw.rectangle([x, y, x + w, y + 56], fill=NAVY)
    hf = font(FONT_BOLD, 28)
    draw.text((x + 16, y + 12), "ALSO TODAY", font=hf, fill=WHITE)

    items = [
        ("capitol", NAVY, "JEFFRIES PICKED FOR SPEAKER",
         "DEMOCRATS VOTE 251\u201311; FIRST BLACK SPEAKER IN LINE"),
        ("cyclone", (150, 40, 40), "CYCLONE AKVAN NEARS INDIA",
         "LANDFALL DUE NOV 20; RED ALERTS, SCHOOLS SHUT"),
        ("planet", (20, 120, 90), "VOYAGER 1: NASA BRIEFING TODAY",
         "ONE LIGHT-DAY OUT; A SIGNAL TAKES 24 HOURS"),
        ("globe", NAVY, "INDIA & JAPAN HOLD 2+2 TALKS",
         "DEFENCE MINISTERS MEET IN TOKYO"),
    ]
    iy = y + 72
    for i, (kind, colour, head, sub) in enumerate(items):
        end = strip_item(draw, x + 12, iy, w - 24, None, colour, kind,
                         head, sub)
        iy = end + 18
        if i < len(items) - 1:
            draw.line([x + 16, iy - 9, x + w - 16, iy - 9],
                      fill=(220, 218, 210), width=2)

    # Footer.
    draw.rectangle([0, 988, 1024, 1024], fill=NAVY)
    ff = font(FONT_BOLD, 20)
    ft = "THE WORLD IN ONE IMAGE"
    fw = draw.textlength(ft, font=ff)
    draw.text(((1024 - fw) / 2, 994), ft, font=ff, fill=WHITE)

    canvas.save(os.path.join(HERE, "entry.png"), "PNG", optimize=True)


if __name__ == "__main__":
    main()
