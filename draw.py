#!/usr/bin/env python3
"""Draw the news-image entry for Thursday 26 November 2026.

Build tool only (run locally): renders entry.png, 1024x1024, deterministic.
The graded program is main.ts, which copies the committed entry.png to
/output/entry.png. All 29 stories were verified against sources dated
26 Nov 2026; earlier-day stories are listed in the DATE CHECK strip.
No network, no clock, no randomness: same input bytes -> same PNG bytes.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

# ---- palette (from the 22 Nov rank-1 page) ----
CREAM   = (247, 243, 232)
NAVY    = (22, 35, 63)
NAVY2   = (27, 42, 74)
RED     = (179, 39, 30)
GOLD    = (201, 162, 39)
INK     = (20, 20, 20)
GREY    = (90, 90, 88)
CARD    = (255, 255, 255)
BORDER  = (216, 210, 192)
GREEN   = (30, 125, 50)
AMBER   = (176, 110, 15)
SKY     = (214, 230, 240)
MAPDOT  = (120, 140, 175)

FD = "/usr/share/fonts/truetype/dejavu"
FL = "/usr/share/fonts/truetype/liberation"


def font(name, size):
    return ImageFont.truetype(os.path.join(FL, name), size)


F_TITLE = lambda s: font("LiberationSerif-Bold.ttf", s)
F_SERIF_IT = lambda s: font("LiberationSerif-Italic.ttf", s)
F_BOLD = lambda s: font("LiberationSans-Bold.ttf", s)
F_REG = lambda s: font("LiberationSans-Regular.ttf", s)
F_IT = lambda s: font("LiberationSans-Italic.ttf", s)


def wrap(d, text, f, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_lines(d, text, f, max_w, max_lines, sizes=None):
    """Wrap text; if it exceeds max_lines, try smaller sizes from `sizes`."""
    cands = sizes or [f.size]
    for sz in cands:
        ff = font("LiberationSans-Bold.ttf", sz) if f == F_BOLD(f.size) else f
        # rebuild the same family at the new size
        ff = ImageFont.truetype(f.path, sz)
        lines = wrap(d, text, ff, max_w)
        if len(lines) <= max_lines:
            return ff, lines
    ff = ImageFont.truetype(f.path, cands[-1])
    return ff, wrap(d, text, ff, max_w)[:max_lines]


# ---- the 29 stories (all happened / first reported Thu 26 Nov 2026, UTC) ----
# kind: scene key for the flat illustration. badge: REPORTED / CLAIM / ONGOING.
HEROES = [
    dict(num=1, loc="NEW YORK", kicker="AMERICAS \u00b7 THANKSGIVING",
         head="Macy's parade postponed in a first in 100 years",
         summ="Nor'easter gusts to 65 mph push the 100th parade to Saturday.",
         src="AFP \u00b7 NY Post", badge="REPORTED", scene="parade"),
    dict(num=2, loc="RAS TANURA, SAUDI ARABIA", kicker="MIDDLE EAST \u00b7 CONFLICT",
         head="Houthis claim strike on Saudi refinery",
         summ="Ras Tanura targeted, Riyadh says; a tower strike injured 11.",
         src="Reuters \u00b7 IBC", badge="CLAIM", scene="refinery"),
    dict(num=3, loc="NEVINNOMYSSK, RUSSIA", kicker="EUROPE \u00b7 WAR",
         head="Ukraine drones hit Russian power plant",
         summ="Nevinnomyssk plant and Azot works struck overnight.",
         src="h.ua \u00b7 Reuters", badge="REPORTED", scene="plant"),
]

GRID = [
    dict(num=4, loc="TIANGONG STATION", kicker="WORLD \u00b7 SPACE",
         head="First Pakistani in space boards China's station",
         summ="Muhammad Zeeshan Ali joins Tiangong on Shenzhou-24.",
         src="Reuters \u00b7 Xinhua", badge="REPORTED", scene="station"),
    dict(num=5, loc="WASHINGTON", kicker="WORLD \u00b7 SPACE",
         head="SpaceX wins nod for a million data satellites",
         summ="Musk's plan for a million SpaceX data satellites is approved, BBC reports.",
         src="BBC", badge="REPORTED", scene="satellite"),
    dict(num=6, loc="JERUSALEM", kicker="MIDDLE EAST \u00b7 ISRAEL",
         head="Judges doubt Netanyahu bribery charge",
         summ="Court urges prosecutors to rethink the corruption cases against the PM.",
         src="IBC \u00b7 AP", badge="REPORTED", scene="court"),
    dict(num=7, loc="BRUSSELS", kicker="EUROPE \u00b7 TREATY",
         head="New UK-EU treaty has 10-year exit clause",
         summ="BBC understands the deal can be ended after a decade by either side.",
         src="BBC", badge="REPORTED", scene="treaty"),
    dict(num=8, loc="PYONGYANG", kicker="ASIA \u00b7 N. KOREA",
         head="Kim wants tactical nukes spread wider",
         summ="Kim orders nukes spread wider; output to grow, KCNA says.",
         src="KCNA \u00b7 Reuters", badge="REPORTED", scene="missile"),
    dict(num=9, loc="WASHINGTON", kicker="AMERICAS \u00b7 USA",
         head="Second judge blocks birthright order",
         summ="Trump's newest curbs on birthright citizenship are halted again in court.",
         src="Reuters", badge="REPORTED", scene="court"),
    dict(num=10, loc="NAIROBI", kicker="AFRICA \u00b7 KENYA",
         head="Cult leader convicted of new charges",
         summ="Mackenzie, serving 200 years, guilty of child cruelty.",
         src="Reuters", badge="REPORTED", scene="bars"),
    dict(num=11, loc="GAZA", kicker="MIDDLE EAST \u00b7 GAZA",
         head="Israeli strikes kill Hamas security chief",
         summ="Strikes in Gaza kill a senior Hamas security figure, reports say.",
         src="Reuters \u00b7 AP", badge="REPORTED", scene="city"),
    dict(num=12, loc="LONDON", kicker="EUROPE \u00b7 CULTURE",
         head="Duran Duran guitarist Andy Taylor dies at 65",
         summ="Guitarist of the 1980s hitmakers dies aged 65.",
         src="BBC", badge="REPORTED", scene="guitar"),
    dict(num=13, loc="TOKYO", kicker="ASIA \u00b7 JAPAN",
         head="Japan unveils Moon rover for 2028 mission",
         summ="Prototype rover shown ahead of a hunt for water on the lunar surface.",
         src="News on Japan", badge="REPORTED", scene="rover"),
]

# (num, flag code, headline, source) — one line each
ALSO = [
    (14, "UA", "Ukraine counts 167 battles, 2,319 Russian losses in a day", "General Staff"),
    (15, "UA", "Kyiv rescue ends; 10 dead in missile-hit block", "Nexus Europa"),
    (16, "KP", "North Korea expels Swiss diplomat in sanctions row", "BBC"),
    (17, "LB", "Lebanon to open a second airport next month", "Reuters"),
    (18, "IR", "Iran death-row women appeal after protests", "BBC"),
    (19, "US", "80 million travel as nor'easter bears down", "AFP"),
    (20, "UG", "Museveni sworn in for a record seventh term", "BBC"),
    (21, "TZ", "Tanzania, CAF tout tourism ahead of 2027 AFCON", "Xinhua"),
    (22, "AU", "76% of Australians can't spot AI content", "Evening Report"),
    (23, "NZ", "New study maps Alpine Fault and next big quake", "Evening Report"),
    (24, "CN", "How China got Nvidia AI chips despite curbs", "Reuters"),
    (25, "DE", "German boat dealer 'supplied Channel gangs'", "BBC"),
    (26, "IR", "Iran claims mines hit tankers near Hormuz", "IBC"),
    (27, "EC", "Ecuador: US talks focus on reviewing operations", "Reuters"),
    (28, "JP", "Japan calls US tariff plan 'regrettable'", "Japan Times"),
    (29, "JP", "BOJ's Tamura flags faster rate hikes", "Vantage"),
]

CHIPS = [("EUROPE", 6), ("MIDDLE EAST", 6), ("AFRICA", 3), ("ASIA", 6),
         ("AMERICAS", 4), ("OCEANIA", 2), ("WORLD", 2)]
CHIP_COLORS = {"EUROPE": (37, 99, 235), "MIDDLE EAST": (220, 38, 38),
               "AFRICA": (22, 163, 74), "ASIA": (217, 119, 6),
               "AMERICAS": (8, 145, 178), "OCEANIA": (124, 58, 237),
               "WORLD": (75, 85, 99)}

NUMBERS = [
    ("343", "drones Russia says it downed"),
    ("2,319", "Russian losses in a day (Kyiv)"),
    ("80M", "Thanksgiving travellers"),
    ("65", "mph gusts in the nor'easter"),
    ("100", "years of the Macy's parade"),
    ("76%", "of Australians can't spot AI"),
]

TIMELINE = [
    ("02:05", "Macy's postponement reported"),
    ("06:12", "NZ 'seventh state' debate"),
    ("06:23", "Kharkiv homes hit, 2 killed"),
    ("07:25", "Kyiv's daily war report"),
    ("17:30", "Thanksgiving NFL kicks off"),
    ("Evening", "Dinners across America"),
]

EXCLUDED = ("Miss Universe crowned Tue 24 Nov \u00b7 Cairo tanker fire Wed 25 Nov \u00b7 "
            "US tariff list Wed 25 Nov \u00b7 Liverpool 3-0 Club Brugge Wed 25 Nov \u00b7 "
            "EU tech fund Wed 25 Nov \u00b7 Poland no-fly plan Wed 25 Nov \u00b7 "
            "Murmansk governor held Wed 25 Nov \u00b7 FAA ground stop Fri 13 Nov \u00b7 "
            "COP31 ends Sun 22 Nov")

# map pins: (story num, lat, lon)
PINS = [(1, 40.7, -74.0), (2, 26.6, 50.1), (3, 44.6, 41.9), (4, 40.0, 100.0),
        (5, 28.4, -80.6), (6, 31.8, 35.2), (7, 50.8, 4.4), (8, 39.0, 125.8),
        (9, 38.9, -77.0), (10, -4.0, 39.7), (11, 31.5, 34.5), (12, 51.5, -0.1),
        (13, 35.7, 139.7)]

# mini flags: list of horizontal bands (color, share) + optional centre dot color
FLAGS = {
    "UA": ([(0, 87, 183, .5), (255, 213, 0, .5)], None),
    "KP": ([(0, 82, 180, .25), (255, 255, 255, .12), (237, 28, 36, .26),
            (255, 255, 255, .12), (0, 82, 180, .25)], None),
    "LB": ([(206, 17, 38, .33), (255, 255, 255, .34), (206, 17, 38, .33)], (0, 122, 61)),
    "IR": ([(35, 159, 64, .33), (255, 255, 255, .34), (218, 0, 0, .33)], None),
    "US": ([(178, 34, 52, .14), (255, 255, 255, .14), (178, 34, 52, .14),
            (255, 255, 255, .14), (178, 34, 52, .14), (255, 255, 255, .14),
            (178, 34, 52, .16)], "us"),
    "UG": ([(0, 0, 0, .17), (255, 255, 0, .16), (206, 17, 38, .17),
            (0, 0, 0, .17), (255, 255, 0, .16), (206, 17, 38, .17)], None),
    "TZ": ([(30, 180, 80, .45), (255, 220, 0, .12), (0, 0, 0, .12), (30, 130, 200, .31)], None),
    "AU": ([(0, 0, 139, 1.0)], "stars"),
    "NZ": ([(0, 0, 139, 1.0)], "stars"),
    "CN": ([(222, 41, 16, 1.0)], (255, 222, 0)),
    "DE": ([(0, 0, 0, .34), (221, 0, 0, .33), (255, 206, 0, .33)], None),
    "EC": ([(255, 222, 0, .5), (0, 71, 171, .25), (206, 17, 38, .25)], None),
    "JP": ([(255, 255, 255, 1.0)], (188, 0, 45)),
}

# ---------------- flat illustration scenes ----------------
# Each scene draws into box (x0, y0, x1, y1) with a sky background.
# Simple geometric shapes only: flat vector style, never a photograph.

def _sky(d, box, color):
    d.rectangle(box, fill=color)


def _cloud(d, x, y, s, color=(255, 255, 255)):
    d.ellipse([x, y, x + 22 * s, y + 12 * s], fill=color)
    d.ellipse([x + 8 * s, y - 5 * s, x + 26 * s, y + 8 * s], fill=color)
    d.ellipse([x + 16 * s, y, x + 34 * s, y + 12 * s], fill=color)


def _sun(d, x, y, r, color=(255, 196, 66)):
    d.ellipse([x - r, y - r, x + r, y + r], fill=color)


def _building(d, x, y, w, h, color):
    d.rectangle([x, y, x + w, y + h], fill=color)
    for wy in range(y + 6, y + h - 4, 9):
        for wx in range(x + 4, x + w - 4, 8):
            d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 230, 140))


def _flame(d, x, y, s):
    d.polygon([(x, y - 16 * s), (x + 8 * s, y), (x + 3 * s, y + 2 * s),
               (x, y - 4 * s), (x - 3 * s, y + 2 * s), (x - 8 * s, y)],
              fill=(255, 140, 0))
    d.polygon([(x, y - 8 * s), (x + 4 * s, y + 1 * s), (x, y - 1 * s),
               (x - 4 * s, y + 1 * s)], fill=(255, 220, 0))


def scene(d, kind, box):
    # Draw into a temp layer first so no shape can spill outside the box.
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    layer = Image.new("RGB", (w, h), (0, 0, 0))
    ld = ImageDraw.Draw(layer)
    _scene_into(ld, kind, (0, 0, w, h))
    d._image.paste(layer, (x0, y0))


def _scene_into(d, kind, box):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    cx, cy = x0 + w // 2, y0 + h // 2
    if kind == "parade":
        _sky(d, box, (170, 205, 230))
        _cloud(d, x0 + 8, y0 + 8, 1.0)
        _cloud(d, x0 + w - 52, y0 + 16, 0.8)
        d.line([x0, y1 - 14, x1, y1 - 14], fill=(90, 90, 90), width=2)
        for bx in range(x0 + 6, x1 - 6, 26):
            _building(d, bx, y1 - 52, 18, 38, (70, 90, 120))
        # big balloon with highlight stripe and basket
        d.ellipse([cx - 26, y0 + 12, cx + 26, y0 + 52], fill=(220, 60, 60))
        d.ellipse([cx - 18, y0 + 16, cx - 8, y0 + 48], fill=(255, 150, 150))
        d.line([cx - 14, y0 + 52, cx - 16, y1 - 22], fill=(60, 60, 60), width=2)
        d.line([cx + 14, y0 + 52, cx + 16, y1 - 22], fill=(60, 60, 60), width=2)
        d.rectangle([cx - 12, y1 - 22, cx + 12, y1 - 14], fill=(140, 90, 40))
        # wind gusts
        for wy in (y0 + 20, y0 + 34, y0 + 48):
            d.line([x0 + 6, wy, x0 + 30, wy], fill=(255, 255, 255), width=3)
    elif kind == "refinery":
        _sky(d, box, (240, 200, 130))
        _sun(d, x0 + w - 22, y0 + 18, 12)
        d.rectangle([x0, y1 - 26, x1, y1], fill=(90, 70, 50))
        for tx in (x0 + 14, x0 + 44, x0 + 74):
            d.rectangle([tx, y1 - 62, tx + 12, y1 - 26], fill=(120, 120, 125))
            d.rectangle([tx + 3, y1 - 74, tx + 9, y1 - 62], fill=(90, 90, 95))
        _flame(d, x0 + 50, y1 - 74, 0.9)
        d.rectangle([x0 + w - 46, y1 - 46, x0 + w - 10, y1 - 26], fill=(160, 60, 40))
        d.ellipse([x0 + w - 42, y1 - 56, x0 + w - 14, y1 - 40], fill=(60, 60, 60))
        d.line([x0 + w - 38, y1 - 48, x0 + w - 18, y1 - 48], fill=(200, 200, 200), width=2)
    elif kind == "plant":
        _sky(d, box, (200, 215, 225))
        _cloud(d, x0 + 10, y0 + 10, 0.9)
        d.rectangle([x0, y1 - 24, x1, y1], fill=(110, 110, 105))
        d.rectangle([x0 + 12, y1 - 58, x0 + 52, y1 - 24], fill=(150, 60, 50))
        d.rectangle([x0 + 62, y1 - 44, x0 + 92, y1 - 24], fill=(90, 100, 110))
        d.polygon([(x0 + 110, y1 - 24), (x0 + 116, y1 - 66), (x0 + 124, y1 - 66),
                   (x0 + 130, y1 - 24)], fill=(180, 180, 175))
        d.ellipse([x0 + 114, y1 - 78, x0 + 126, y1 - 66], fill=(120, 120, 120))
        _flame(d, x0 + 32, y1 - 58, 0.8)
        # drone
        d.ellipse([cx - 12, y0 + 12, cx + 12, y0 + 20], fill=(40, 40, 40))
        d.line([cx - 20, y0 + 16, cx + 20, y0 + 16], fill=(40, 40, 40), width=2)
    elif kind == "station":
        _sky(d, box, (16, 24, 48))
        for sx, sy in ((x0 + 12, y0 + 10), (x0 + 40, y0 + 22), (x0 + w - 16, y0 + 12),
                       (x0 + w - 44, y0 + 26), (x0 + 70, y0 + 8)):
            d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 255, 255))
        d.ellipse([x0, y1 - 16, x1, y1 + 26], fill=(70, 120, 180))
        d.rectangle([cx - 34, cy - 8, cx + 34, cy + 8], fill=(200, 200, 205))
        d.rectangle([cx - 52, cy - 4, cx - 34, cy + 4], fill=(40, 90, 180))
        d.rectangle([cx + 34, cy - 4, cx + 52, cy + 4], fill=(40, 90, 180))
        d.ellipse([cx - 8, cy - 14, cx + 8, cy - 6], fill=(220, 220, 220))
        d.rectangle([cx - 2, cy + 8, cx + 2, cy + 20], fill=(200, 200, 205))
    elif kind == "satellite":
        _sky(d, box, (16, 24, 48))
        for sx, sy in ((x0 + 14, y0 + 12), (x0 + 52, y0 + 8), (x0 + w - 20, y0 + 20),
                       (x0 + 30, y0 + 34), (x0 + w - 50, y0 + 40)):
            d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 255, 255))
        d.ellipse([x0 + 8, y0 + 6, x1 - 8, y1 - 6], outline=(90, 140, 200), width=2)
        d.rectangle([cx - 26, cy - 6, cx - 6, cy + 6], fill=(40, 90, 180))
        d.rectangle([cx + 6, cy - 6, cx + 26, cy + 6], fill=(40, 90, 180))
        d.rectangle([cx - 6, cy - 8, cx + 6, cy + 8], fill=(220, 220, 220))
        d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(255, 196, 66))
    elif kind == "court":
        _sky(d, box, (232, 222, 200))
        d.rectangle([x0, y1 - 12, x1, y1], fill=(120, 100, 70))
        for px in (x0 + 14, x0 + 44, x0 + 74, x0 + 104):
            d.rectangle([px, y0 + 18, px + 12, y1 - 12], fill=(240, 235, 220))
            d.rectangle([px - 2, y0 + 14, px + 14, y0 + 18], fill=(180, 160, 110))
        d.polygon([(x0 + 4, y0 + 14), (cx, y0 - 2), (x1 - 4, y0 + 14)],
                  fill=(150, 40, 30))
        # gavel
        d.rectangle([cx - 16, y1 - 34, cx + 8, y1 - 26], fill=(120, 80, 40))
        d.line([cx - 4, y1 - 30, cx + 22, y1 - 44], fill=(120, 80, 40), width=4)
    elif kind == "treaty":
        _sky(d, box, (222, 230, 240))
        d.rectangle([cx - 30, y0 + 10, cx + 30, y1 - 12], fill=(255, 255, 255))
        d.rectangle([cx - 30, y0 + 10, cx + 30, y1 - 12], outline=(40, 40, 40), width=2)
        for ly in range(y0 + 22, y1 - 16, 8):
            d.line([cx - 22, ly, cx + 22, ly], fill=(150, 150, 150), width=2)
        # EU stars circle + UK cross, small flags left/right
        d.rectangle([x0 + 8, y0 + 12, x0 + 34, y0 + 30], fill=(0, 51, 153))
        for k in range(8):
            import math
            a = math.pi * k / 4
            d.ellipse([x0 + 21 + 8 * math.cos(a) - 1, y0 + 21 + 7 * math.sin(a) - 1,
                       x0 + 21 + 8 * math.cos(a) + 1, y0 + 21 + 7 * math.sin(a) + 1],
                      fill=(255, 204, 0))
        d.rectangle([x1 - 34, y0 + 12, x1 - 8, y0 + 30], fill=(0, 36, 125))
        d.line([x1 - 34, y0 + 21, x1 - 8, y0 + 21], fill=(255, 255, 255), width=4)
        d.line([x1 - 21, y0 + 12, x1 - 21, y0 + 30], fill=(255, 255, 255), width=4)
    elif kind == "missile":
        _sky(d, box, (30, 40, 70))
        for sx, sy in ((x0 + 12, y0 + 10), (x0 + 60, y0 + 16), (x0 + w - 14, y0 + 12)):
            d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 255, 255))
        d.polygon([(cx - 30, cy - 6), (cx + 18, cy - 6), (cx + 34, cy),
                   (cx + 18, cy + 6), (cx - 30, cy + 6)], fill=(200, 200, 205))
        d.polygon([(cx - 30, cy - 6), (cx - 40, cy - 14), (cx - 30, cy - 2)], fill=(160, 40, 40))
        d.polygon([(cx - 30, cy + 6), (cx - 40, cy + 14), (cx - 30, cy + 2)], fill=(160, 40, 40))
        _flame(d, cx + 34, cy, 0.9)
        d.rectangle([x0, y1 - 10, x1, y1], fill=(20, 60, 40))
    elif kind == "bars":
        _sky(d, box, (210, 210, 205))
        d.rectangle([x0, y1 - 12, x1, y1], fill=(90, 90, 90))
        for bx in range(x0 + 8, x1 - 4, 16):
            d.rectangle([bx, y0 + 4, bx + 5, y1 - 12], fill=(50, 50, 50))
        d.rectangle([x0 + 30, y1 - 40, x0 + 70, y1 - 12], fill=(150, 60, 50))
        d.ellipse([x0 + 44, y1 - 34, x0 + 56, y1 - 22], fill=(255, 220, 180))
    elif kind == "city":
        _sky(d, box, (235, 200, 160))
        _sun(d, x0 + w - 20, y0 + 16, 11)
        for bx in range(x0 + 6, x1 - 6, 24):
            _building(d, bx, y1 - 46, 16, 32, (110, 100, 90))
        d.rectangle([x0 + 40, y1 - 30, x0 + 78, y1 - 12], fill=(255, 255, 255))
        d.rectangle([x0 + 40, y1 - 30, x0 + 78, y1 - 26], fill=(200, 40, 40))
        d.line([x0 + 46, y1 - 20, x0 + 72, y1 - 20], fill=(200, 40, 40), width=2)
    elif kind == "guitar":
        _sky(d, box, (40, 30, 60))
        for sx, sy in ((x0 + 12, y0 + 10), (x0 + 50, y0 + 8), (x0 + w - 14, y0 + 22),
                       (x0 + 30, y0 + 30)):
            d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 220, 100))
        d.ellipse([cx - 16, cy - 2, cx + 16, cy + 30], fill=(190, 60, 40))
        d.ellipse([cx - 5, cy + 8, cx + 5, cy + 18], fill=(30, 20, 20))
        d.rectangle([cx - 3, cy - 30, cx + 3, cy], fill=(120, 80, 40))
        d.line([cx, cy - 30, cx, cy + 30], fill=(220, 220, 220), width=1)
    elif kind == "rover":
        _sky(d, box, (20, 22, 40))
        for sx, sy in ((x0 + 12, y0 + 10), (x0 + 44, y0 + 14), (x0 + w - 16, y0 + 10),
                       (x0 + 70, y0 + 26)):
            d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 255, 255))
        d.ellipse([x0 + w - 30, y0 + 8, x0 + w - 6, y0 + 32], fill=(230, 230, 220))
        d.ellipse([x0, y1 - 20, x1, y1 + 30], fill=(150, 150, 145))
        d.rectangle([cx - 26, cy - 6, cx + 26, cy + 8], fill=(200, 200, 205))
        d.ellipse([cx - 16, cy + 8, cx - 4, cy + 20], fill=(40, 40, 40))
        d.ellipse([cx + 4, cy + 8, cx + 16, cy + 20], fill=(40, 40, 40))
        d.line([cx + 26, cy - 4, cx + 40, cy - 16], fill=(200, 200, 205), width=3)
        d.ellipse([cx + 38, cy - 18, cx + 42, cy - 14], fill=(255, 196, 66))


# ---------------- small widgets ----------------
def badge(d, x, y, text):
    f = F_BOLD(10)
    tw = d.textlength(text, font=f)
    color = GREEN if text == "REPORTED" else (AMBER if text == "CLAIM" else RED)
    d.rounded_rectangle([x, y, x + tw + 12, y + 15], radius=3, fill=color)
    d.text((x + 6, y + 2), text, font=f, fill=(255, 255, 255))


def num_circle(d, cx, cy, r, num, fill=NAVY):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill)
    f = F_BOLD(13 if r >= 12 else 10)
    t = str(num)
    tw = d.textlength(t, font=f)
    d.text((cx - tw / 2, cy - f.size / 2 - 1), t, font=f, fill=(255, 255, 255))


def mini_flag(d, x, y, code, w=17, h=12):
    bands, dot = FLAGS.get(code, ([(180, 180, 180, 1.0)], None))
    yy = y
    for (r, g, b, share) in bands:
        bh = max(1, round(h * share))
        d.rectangle([x, yy, x + w, yy + bh], fill=(r, g, b))
        yy += bh
    d.rectangle([x, y, x + w, y + h], outline=(120, 120, 120), width=1)
    if dot == "us":
        d.rectangle([x, y, x + 7, y + 6], fill=(0, 36, 125))
    elif dot == "stars":
        for sx, sy in ((x + 4, y + 3), (x + 12, y + 4), (x + 8, y + 8)):
            d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 255, 255))
    elif dot:
        d.ellipse([x + w // 2 - 3, y + h // 2 - 3, x + w // 2 + 3, y + h // 2 + 3],
                  fill=dot)


# dotted world map from continent blobs (equirectangular, lon -180..180, lat -60..85)
BLOBS = [  # (lon_c, lat_c, rx_lon, ry_lat) ellipses suggesting continents
    (-100, 48, 32, 16), (-95, 32, 22, 10), (-82, 20, 10, 8),     # N America
    (-60, -8, 13, 16), (-64, -28, 8, 12),                        # S America
    (-5, 52, 14, 9), (15, 47, 18, 8), (38, 58, 26, 12),          # Europe / Russia
    (78, 24, 16, 12), (103, 12, 10, 9), (122, 34, 10, 10),       # Asia
    (18, 4, 12, 14), (24, -18, 10, 12), (33, -24, 8, 9),         # Africa
    (134, -25, 14, 9), (172, -41, 5, 6),                          # Oceania
    (-150, 64, 10, 6), (140, 66, 12, 5),                          # Alaska / Siberia
]


def _lonlat_to_xy(lon, lat, box):
    x0, y0, x1, y1 = box
    return (x0 + (lon + 180) / 360 * (x1 - x0),
            y0 + (85 - lat) / 145 * (y1 - y0))


def dotted_map(d, box):
    x0, y0, x1, y1 = box
    step = 4
    for gx in range(x0 + 2, x1, step):
        for gy in range(y0 + 2, y1, step):
            lon = (gx - x0) / (x1 - x0) * 360 - 180
            lat = 85 - (gy - y0) / (y1 - y0) * 145
            inside = False
            for (clon, clat, rx, ry) in BLOBS:
                if ((lon - clon) / rx) ** 2 + ((lat - clat) / ry) ** 2 <= 1:
                    inside = True
                    break
            if inside:
                d.ellipse([gx - 1, gy - 1, gx + 1, gy + 1], fill=MAPDOT)
    for (num, lat, lon) in PINS:
        px, py = _lonlat_to_xy(lon, lat, box)
        num_circle(d, int(px), int(py), 8, num, fill=RED)

# ---------------- cards ----------------
def draw_hero_card(d, x, y, w, h, s):
    d.rounded_rectangle([x, y, x + w, y + h], radius=4, fill=CARD, outline=BORDER, width=1)
    num_circle(d, x + 16, y + 15, 12, s["num"])
    loc = s["loc"]
    f_loc = F_BOLD(11)
    while d.textlength(loc, font=f_loc) > w - 36 and f_loc.size > 8:
        f_loc = F_BOLD(f_loc.size - 1)
    d.text((x + 32, y + 9), loc, font=f_loc, fill=NAVY)
    ix0, iy0, ix1, iy1 = x + 5, y + 30, x + w - 5, y + 100
    scene(d, s["scene"], (ix0, iy0, ix1, iy1))
    d.rectangle([ix0, iy0, ix1, iy1], outline=BORDER, width=1)
    bf = F_BOLD(10)
    bw = d.textlength(s["badge"], font=bf) + 12
    badge(d, ix1 - bw - 4, iy1 - 19, s["badge"])
    d.text((x + 8, y + 104), s["kicker"], font=F_BOLD(11), fill=(200, 90, 20))
    ff, lines = fit_lines(d, s["head"], F_BOLD(19), w - 16, 2, sizes=[19, 18, 17, 16])
    yy = y + 118
    for ln in lines:
        d.text((x + 8, yy), ln, font=ff, fill=INK)
        yy += ff.size + 3
    yy += 2
    for ln in wrap(d, s["summ"], F_REG(12), w - 16)[:2]:
        d.text((x + 8, yy), ln, font=F_REG(12), fill=(40, 40, 40))
        yy += 15
    d.text((x + 8, y + h - 15), s["src"], font=F_IT(10), fill=GREY)


def draw_grid_card(d, x, y, w, h, s):
    d.rounded_rectangle([x, y, x + w, y + h], radius=4, fill=CARD, outline=BORDER, width=1)
    num_circle(d, x + 13, y + 12, 10, s["num"])
    loc = s["loc"]
    f_loc = F_BOLD(10)
    while d.textlength(loc, font=f_loc) > w - 30 and f_loc.size > 8:
        f_loc = F_BOLD(f_loc.size - 1)
    d.text((x + 26, y + 7), loc, font=f_loc, fill=NAVY)
    ix0, iy0, ix1, iy1 = x + 5, y + 26, x + w - 5, y + 84
    scene(d, s["scene"], (ix0, iy0, ix1, iy1))
    d.rectangle([ix0, iy0, ix1, iy1], outline=BORDER, width=1)
    bf = F_BOLD(9)
    bw = d.textlength(s["badge"], font=bf) + 10
    badge(d, ix1 - bw - 3, iy1 - 17, s["badge"])
    d.text((x + 7, y + 88), s["kicker"], font=F_BOLD(10), fill=(200, 90, 20))
    ff, lines = fit_lines(d, s["head"], F_BOLD(15), w - 14, 2, sizes=[15, 14])
    yy = y + 101
    for ln in lines:
        d.text((x + 7, yy), ln, font=ff, fill=INK)
        yy += ff.size + 2
    yy += 1
    for ln in wrap(d, s["summ"], F_REG(11), w - 14)[:2]:
        d.text((x + 7, yy), ln, font=F_REG(11), fill=(40, 40, 40))
        yy += 13
    d.text((x + 7, y + h - 13), s["src"], font=F_IT(9), fill=GREY)


def draw_numbers_panel(d, x, y, w, h):
    d.rounded_rectangle([x, y, x + w, y + h], radius=4, fill=NAVY)
    d.text((x + 10, y + 8), "THE DAY IN NUMBERS", font=F_BOLD(13), fill=GOLD)
    yy = y + 34
    for (num, label) in NUMBERS:
        d.text((x + 10, yy), num, font=F_BOLD(19), fill=(255, 255, 255))
        d.text((x + 10, yy + 19), label, font=F_REG(10), fill=(200, 210, 230))
        yy += 30


def draw_chips(d, y):
    items = []
    total = 0
    f = F_BOLD(11)
    for (name, n) in CHIPS:
        t = "%s %d" % (name, n)
        tw = d.textlength(t, font=f) + 18
        items.append((name, n, t, tw))
        total += tw
    total += 6 * (len(items) - 1)
    x = (1024 - total) // 2
    for (name, n, t, tw) in items:
        d.rounded_rectangle([x, y, x + tw, y + 24], radius=12, fill=CHIP_COLORS[name])
        d.text((x + 9, y + 5), t, font=f, fill=(255, 255, 255))
        x += tw + 6


def draw_timeline(d, y):
    d.rectangle([10, y, 1014, y + 22], fill=NAVY)
    f_t, f_x = F_BOLD(11), F_REG(10)
    x = 18
    d.text((x, y + 4), "UTC", font=f_t, fill=GOLD)
    x += d.textlength("UTC", font=f_t) + 10
    parts = [("02:05", "Macy's parade postponed"), ("06:12", "NZ 'seventh state' debate"),
             ("06:23", "Kharkiv homes hit"), ("07:25", "Kyiv war report"),
             ("17:30", "Thanksgiving NFL kicks off"), ("Evening", "Dinners across America")]
    for (i, (t, txt)) in enumerate(parts):
        d.text((x, y + 4), t, font=f_t, fill=GOLD)
        x += d.textlength(t, font=f_t) + 5
        d.text((x, y + 5), txt, font=f_x, fill=(230, 235, 245))
        x += d.textlength(txt, font=f_x) + 5
        if i < len(parts) - 1:
            d.text((x, y + 5), "\u2022", font=f_x, fill=GOLD)
            x += 10


def draw_also(d, x, y, w, h):
    d.text((x, y), "ALSO ON THURSDAY 26 NOVEMBER", font=F_BOLD(13), fill=NAVY)
    lx = x + w - 210
    for (t, c) in (("REPORTED", GREEN), ("CLAIM", AMBER), ("ONGOING", RED)):
        bf = F_BOLD(8)
        bw = d.textlength(t, font=bf) + 10
        d.rounded_rectangle([lx, y + 1, lx + bw, y + 13], radius=3, fill=c)
        d.text((lx + 5, y + 3), t, font=bf, fill=(255, 255, 255))
        lx += bw + 6
    col_w = w // 2
    row_h = (h - 22) // 8
    for i, (num, code, head, src) in enumerate(ALSO):
        cx = x + (i // 8) * col_w
        cy = y + 22 + (i % 8) * row_h
        d.text((cx, cy), str(num), font=F_BOLD(11), fill=NAVY)
        mini_flag(d, cx + 20, cy + 1, code)
        avail = col_w - 20 - 17 - 6 - d.textlength(" \u00b7 " + src, font=F_REG(10)) - 4
        f_h = F_REG(11)
        hh = head
        while d.textlength(hh, font=f_h) > avail and len(hh) > 10:
            hh = hh.rsplit(" ", 1)[0]
        if hh != head:
            hh += "\u2026"
        d.text((cx + 41, cy), hh, font=f_h, fill=INK)
        d.text((cx + 41 + d.textlength(hh, font=f_h), cy + 1),
               " \u00b7 " + src, font=F_REG(10), fill=GREY)


def draw_map_panel(d, x, y, w, h):
    d.text((x, y), "WHERE IT HAPPENED", font=F_BOLD(12), fill=NAVY)
    d.text((x, y + 14), "pins = story numbers", font=F_REG(9), fill=GREY)
    dotted_map(d, (x, y + 28, x + w, y + h))


def draw_datecheck(d, y, h):
    d.rounded_rectangle([10, y, 1014, y + h], radius=4, outline=RED, width=2)
    f1, f2 = F_BOLD(12), F_REG(11)
    line1 = "Every story on this page happened or was first reported on Thursday 26 November 2026 (UTC)."
    d.text((20, y + 5), "DATE CHECK", font=f1, fill=RED)
    d.text((20 + d.textlength("DATE CHECK  ", font=f1), y + 5), line1, font=f1, fill=INK)
    label = "Left out because they happened on an earlier day: "
    lx = 20 + d.textlength(label, font=F_BOLD(10))
    lines = wrap(d, EXCLUDED, F_REG(10), 1014 - 20 - lx)
    d.text((20, y + 23), label, font=F_BOLD(10), fill=RED)
    if lines:
        d.text((lx, y + 23), lines[0], font=F_REG(10), fill=(60, 60, 60))
    yy = y + 36
    for ln in lines[1:3]:
        d.text((20, yy), ln, font=F_REG(10), fill=(60, 60, 60))
        yy += 12


def main():
    img = Image.new("RGB", (1024, 1024), CREAM)
    d = ImageDraw.Draw(img)
    # top bar
    d.rectangle([0, 0, 1024, 28], fill=NAVY)
    d.text((10, 7), "THE WORLD IN ONE DAY", font=F_BOLD(12), fill=(255, 255, 255))
    rt = "29 STORIES \u00b7 7 REGIONS \u00b7 ALL FROM THIS ONE DAY"
    d.text((1024 - 10 - d.textlength(rt, font=F_BOLD(12)), 7), rt, font=F_BOLD(12), fill=GOLD)
    # date title (auto-fit)
    title = "Thursday 26 November 2026"
    tsize = 76
    while d.textlength(title, font=F_TITLE(tsize)) > 1004 and tsize > 60:
        tsize -= 2
    d.text((10, 30), title, font=F_TITLE(tsize), fill=INK)
    # sub-headline
    sub = ("Macy's parade postponed in a 100-year first \u00b7 Houthis claim Ras Tanura strike "
           "\u00b7 Ukraine drones hit Nevinnomyssk")
    ssize = 19
    while d.textlength(sub, font=F_SERIF_IT(ssize)) > 1004 and ssize > 14:
        ssize -= 1
    d.text((10, 114), sub, font=F_SERIF_IT(ssize), fill=RED)
    draw_chips(d, 140)
    draw_timeline(d, 168)
    # hero row
    hx = 10
    for s in HEROES:
        draw_hero_card(d, hx, 194, 244, 220, s)
        hx += 250
    draw_numbers_panel(d, 760, 194, 254, 220)
    # grid rows
    gx = 10
    for s in GRID[:5]:
        draw_grid_card(d, gx, 418, 196, 182, s)
        gx += 202
    gx = 10
    for s in GRID[5:]:
        draw_grid_card(d, gx, 604, 196, 182, s)
        gx += 202
    # bottom band
    draw_also(d, 10, 790, 744, 132)
    draw_map_panel(d, 760, 790, 254, 132)
    draw_datecheck(d, 924, 50)
    foot = ("HOW SURE: REPORTED = carried by the day's wires or officials \u00b7 CLAIM = one side's "
            "account, labelled as such \u00b7 ONGOING = still unfolding \u00b7 Scenes are drawn "
            "illustrations, not photographs.")
    f_foot = F_REG(11)
    while d.textlength(foot, font=f_foot) > 1004:
        f_foot = F_REG(f_foot.size - 1)
    d.text(((1024 - d.textlength(foot, font=f_foot)) / 2, 980), foot, font=f_foot, fill=GREY)
    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
