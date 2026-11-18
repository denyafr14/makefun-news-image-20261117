#!/usr/bin/env python3
"""Draw the 17 November 2026 world-news front page (1024x1024 PNG).

Flat newspaper infographic: masthead with the date, one panel per story,
each with a short headline, a one-line deck and a simple pictogram drawn
from PIL shapes only. No network, fully deterministic.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (251, 248, 241)
INK = (20, 20, 20)
NAVY = (27, 42, 74)
RED = (179, 39, 30)
GRAY = (90, 90, 90)
LIGHT = (233, 228, 218)
BLUE = (43, 108, 196)
GREEN = (46, 139, 87)
ORANGE = (224, 122, 31)

FONT_DIR = "/usr/share/fonts/truetype/noto"
F_BLACK = os.path.join(FONT_DIR, "NotoSans-Black.ttf")
F_BOLD = os.path.join(FONT_DIR, "NotoSans-Bold.ttf")
F_REG = os.path.join(FONT_DIR, "NotoSans-Regular.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def kicker(draw, x, y, text):
    f = font(F_BOLD, 17)
    draw.text((x, y), text, font=f, fill=RED)
    return y + 24


def panel(draw, x, y, w, h, kicker_text, headline, deck, pict, hl_size=24):
    """A story panel: bordered box, kicker, headline, deck, pictogram right."""
    draw.rectangle([x, y, x + w - 1, y + h - 1], outline=INK, width=2)
    px, py = x + 16, y + 14
    py = kicker(draw, px, py, kicker_text)
    hl_font = font(F_BOLD, hl_size)
    deck_font = font(F_REG, 18)
    text_w = w - 32 - (126 if pict else 0)
    hl_lines = wrap(draw, headline, hl_font, text_w)
    py = draw_lines(draw, hl_lines, px, py + 2, hl_font, INK, hl_size + 6)
    deck_lines = wrap(draw, deck, deck_font, text_w)
    draw_lines(draw, deck_lines, px, py + 4, deck_font, GRAY, 23)
    if pict:
        pict(draw, x + w - 14 - 120, y + h - 14 - 120, 120, 120)


# ---- pictograms (flat shapes, drawn in a box of width w, height h) ----
def pic_strike(d, x, y, w, h):
    # sea, island, missile arcs, orange burst
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(58, 110, 160))
    d.polygon([(x + w * 0.30, y + h * 0.62), (x + w * 0.48, y + h * 0.38),
               (x + w * 0.66, y + h * 0.62)], fill=(96, 84, 62))
    d.polygon([(x + w * 0.18, y + h * 0.30), (x + w * 0.42, y + h * 0.06),
               (x + w * 0.62, y + h * 0.22), (x + w * 0.80, y + h * 0.10)],
              fill=None, outline=(200, 60, 40), width=4)
    cx, cy, r = x + w * 0.52, y + h * 0.34, 26
    pts = []
    import math
    for i in range(12):
        ang = math.pi * i / 6
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=ORANGE)
    d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=(255, 214, 90))


def pic_bridge(d, x, y, w, h):
    # bridge deck with a collapsed middle span falling into the strait
    d.rectangle([x, y + h * 0.68, x + w, y + h], fill=(58, 110, 160))
    d.rectangle([x, y + h * 0.42, x + w * 0.34, y + h * 0.50], fill=NAVY)
    d.rectangle([x + w * 0.66, y + h * 0.42, x + w, y + h * 0.50], fill=NAVY)
    d.polygon([(x + w * 0.40, y + h * 0.50), (x + w * 0.48, y + h * 0.72),
               (x + w * 0.60, y + h * 0.50)], fill=(120, 120, 120))
    d.line([x + w * 0.10, y + h * 0.42, x + w * 0.10, y + h * 0.16], fill=NAVY, width=5)
    d.line([x + w * 0.90, y + h * 0.42, x + w * 0.90, y + h * 0.16], fill=NAVY, width=5)
    d.line([x + w * 0.10, y + h * 0.16, x + w * 0.34, y + h * 0.42], fill=NAVY, width=3)
    d.line([x + w * 0.90, y + h * 0.16, x + w * 0.66, y + h * 0.42], fill=NAVY, width=3)
    d.ellipse([x + w * 0.44, y + h * 0.10, x + w * 0.56, y + h * 0.22], fill=ORANGE)


def pic_summit(d, x, y, w, h):
    # three flags on poles: US blue, China red, Russia white-blue-red
    # US flag
    d.line([x + w * 0.18, y + h * 0.18, x + w * 0.18, y + h * 0.86], fill=INK, width=4)
    d.rectangle([x + w * 0.18, y + h * 0.18, x + w * 0.18 + 44, y + h * 0.44],
                fill=BLUE, outline=INK, width=2)
    # China flag
    d.line([x + w * 0.50, y + h * 0.18, x + w * 0.50, y + h * 0.86], fill=INK, width=4)
    d.rectangle([x + w * 0.50, y + h * 0.18, x + w * 0.50 + 44, y + h * 0.44],
                fill=RED, outline=INK, width=2)
    d.text((x + w * 0.50 + 15, y + h * 0.24), "*", font=font(F_BOLD, 22), fill=(255, 214, 90))
    # Russia flag: white / blue / red stripes
    d.line([x + w * 0.82, y + h * 0.18, x + w * 0.82, y + h * 0.86], fill=INK, width=4)
    fx0, fy0 = x + w * 0.82, y + h * 0.18
    d.rectangle([fx0, fy0, fx0 + 44, fy0 + 12], fill=(235, 235, 235), outline=INK, width=2)
    d.rectangle([fx0, fy0 + 12, fx0 + 44, fy0 + 24], fill=BLUE, outline=INK, width=2)
    d.rectangle([fx0, fy0 + 24, fx0 + 44, fy0 + 36], fill=RED, outline=INK, width=2)
    # table line
    d.rectangle([x + w * 0.05, y + h * 0.86, x + w * 0.95, y + h * 0.92], fill=NAVY)


def pic_chip(d, x, y, w, h):
    # microchip with pins and a rising green arrow
    s = w * 0.58
    cx, cy = x + w * 0.30, y + h * 0.52
    for i in range(4):
        off = -s / 2 + i * s / 3
        d.line([cx + off, cy - s / 2 - 14, cx + off, cy - s / 2], fill=INK, width=4)
        d.line([cx + off, cy + s / 2, cx + off, cy + s / 2 + 14], fill=INK, width=4)
        d.line([cx - s / 2 - 14, cy + off, cx - s / 2, cy + off], fill=INK, width=4)
        d.line([cx + s / 2, cy + off, cx + s / 2 + 14, cy + off], fill=INK, width=4)
    d.rectangle([cx - s / 2, cy - s / 2, cx + s / 2, cy + s / 2], fill=NAVY, outline=INK, width=2)
    d.rectangle([cx - s / 4, cy - s / 4, cx + s / 4, cy + s / 4], fill=(58, 110, 160))
    # rising arrow
    ax0, ay0 = x + w * 0.62, y + h * 0.78
    ax1, ay1 = x + w * 0.94, y + h * 0.22
    d.line([ax0, ay0, ax1, ay1], fill=GREEN, width=6)
    d.polygon([(ax1, ay1), (ax1 - 18, ay1 + 2), (ax1 - 2, ay1 + 18)], fill=GREEN)


def pic_plane(d, x, y, w, h):
    # side-view plane diving toward mountains, smoke trailing behind
    # mountains
    d.polygon([(x + w * 0.05, y + h * 0.92), (x + w * 0.30, y + h * 0.62),
               (x + w * 0.55, y + h * 0.92)], fill=(120, 120, 120))
    d.polygon([(x + w * 0.45, y + h * 0.92), (x + w * 0.72, y + h * 0.68),
               (x + w * 0.95, y + h * 0.92)], fill=(150, 150, 150))
    # smoke puffs trailing the tail (left)
    for i, r in enumerate((9, 12, 15)):
        cx = x + w * 0.06 + i * 14
        cy = y + h * 0.30 - i * 6
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(170, 170, 170))
    # fuselage: body bar with pointed nose (right), tail at left
    d.polygon([(x + w * 0.30, y + h * 0.36), (x + w * 0.82, y + h * 0.36),
               (x + w * 0.96, y + h * 0.42), (x + w * 0.82, y + h * 0.48),
               (x + w * 0.30, y + h * 0.48)], fill=NAVY)
    # tail fin (up, at left end) and wing (down, middle)
    d.polygon([(x + w * 0.30, y + h * 0.36), (x + w * 0.38, y + h * 0.18),
               (x + w * 0.46, y + h * 0.36)], fill=NAVY)
    d.polygon([(x + w * 0.52, y + h * 0.48), (x + w * 0.62, y + h * 0.66),
               (x + w * 0.70, y + h * 0.48)], fill=NAVY)
    # windows
    d.ellipse([x + w * 0.80, y + h * 0.385, x + w * 0.86, y + h * 0.435],
              fill=(255, 214, 90))


def pic_virus(d, x, y, w, h):
    # spiked virus circle with a red cross badge
    import math
    cx, cy, r = x + w * 0.42, y + h * 0.50, 34
    for i in range(10):
        ang = 2 * math.pi * i / 10
        x1, y1 = cx + r * math.cos(ang), cy + r * math.sin(ang)
        x2, y2 = cx + (r + 16) * math.cos(ang), cy + (r + 16) * math.sin(ang)
        d.line([x1, y1, x2, y2], fill=RED, width=5)
        d.ellipse([x2 - 6, y2 - 6, x2 + 6, y2 + 6], fill=RED)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(224, 122, 31))
    d.ellipse([cx - 12, cy - 14, cx + 2, cy], fill=(255, 214, 90))
    d.ellipse([cx + 8, cy + 6, cx + 18, cy + 16], fill=(255, 214, 90))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 36  # margin

    # ---------- masthead ----------
    d.text((W // 2, 24), "THE WORLD TODAY", font=font(F_BLACK, 60),
           fill=INK, anchor="mt")
    d.line([M, 100, W - M, 100], fill=INK, width=3)
    d.line([M, 105, W - M, 105], fill=INK, width=1)
    d.text((W // 2, 114), "TUESDAY  •  17 NOVEMBER 2026",
           font=font(F_BOLD, 32), fill=RED, anchor="mt")
    d.text((W // 2, 156), "The day's world news — six stories that mattered most",
           font=font(F_REG, 20), fill=GRAY, anchor="mt")
    d.line([M, 188, W - M, 188], fill=INK, width=2)

    # ---------- lead story (full width) ----------
    lx, ly, lw, lh = M, 202, W - 2 * M, 196
    d.rectangle([lx, ly, lx + lw - 1, ly + lh - 1], outline=INK, width=2)
    px, py = lx + 18, ly + 14
    py = kicker(d, px, py, "LEAD  •  MIDDLE EAST")
    hl = font(F_BOLD, 33)
    hl_lines = wrap(d, "US strikes Iran missile site as drones hit Bahrain base",
                    hl, lw - 36 - 250)
    py = draw_lines(d, hl_lines, px, py + 2, hl, INK, 40)
    dk = font(F_REG, 21)
    dk_lines = wrap(d, "Washington calls the Qeshm Island strike self-defence; "
                       "Tehran's third drone attack on Bahrain in five days.",
                    dk, lw - 36 - 250)
    draw_lines(d, dk_lines, px, py + 6, dk, GRAY, 27)
    pic_strike(d, lx + lw - 18 - 220, ly + 18, 220, lh - 36)

    # ---------- grid: 2 x 2 ----------
    gx, gy = M, 412
    gw, gh = (W - 2 * M - 14) // 2, 208
    gap = 14
    panel(d, gx, gy, gw, gh, "WAR IN EUROPE",
          "Ukraine hits Crimea bridge again; span falls",
          "Second day of drone strikes closes the Kerch crossing; road and rail traffic halted.",
          pic_bridge)
    panel(d, gx + gw + gap, gy, gw, gh, "DIPLOMACY  •  ASIA",
          "Trump flies to Asia for talks with Xi and Putin",
          "Nuclear risks, sanctions and Ukraine on the agenda at the APEC summit in Shenzhen.",
          pic_summit)
    panel(d, gx, gy + gh + gap, gw, gh, "TECH  •  BUSINESS",
          "Nvidia posts record sales; Huang will not return",
          "Revenue tops $115bn, about double a year ago, but the board rules out a comeback.",
          pic_chip)
    panel(d, gx + gw + gap, gy + gh + gap, gw, gh, "DISASTER  •  RUSSIA",
          "Russian military plane crashes; all 19 aboard killed",
          "An-12 transport goes down in Siberia's Kemerovo region; officials blame a fault.",
          pic_plane)

    # ---------- bottom strip: health ----------
    bx, by, bw, bh = M, 856, W - 2 * M, 100
    d.rectangle([bx, by, bx + bw - 1, by + bh - 1], outline=INK, width=2)
    pic_virus(d, bx + 14, by + 8, 92, bh - 16)
    tx = bx + 118
    kicker(d, tx, by + 12, "HEALTH  •  UNITED STATES")
    hl2 = font(F_BOLD, 27)
    d.text((tx, by + 38), "US loses measles-free status after 26 years",
           font=hl2, fill=INK)
    dk2 = font(F_REG, 20)
    d.text((tx, by + 72), "More than 5,400 cases and 10 deaths — the most since the early 1990s.",
           font=dk2, fill=GRAY)

    # ---------- footer ----------
    d.line([M, 968, W - M, 968], fill=INK, width=1)
    d.text((W // 2, 976), "Sources: BBC, CBS News, NPR, Al Jazeera, Reuters  •  17 November 2026",
           font=font(F_REG, 16), fill=GRAY, anchor="mt")

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
