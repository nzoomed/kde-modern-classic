"""KDE Classic Vector: weather icons for the Weather Report widget.

KDE 3 had no weather set, so these are new, built from a small kit of parts in the theme's glossy style:
sun, moon, white and grey clouds, rain drops, snow flakes, hail, lightning, wind and fog. Each Breeze
weather name is composed from those parts, so day/night and scattered/storm variants stay consistent.
"""
import math, os
from gen import Icon, INK, LW, circle

SUN = ("#fffbe0", "#ffd21a", "#e8800a")
CLOUD_W = ("#ffffff", "#e4e8ee", "#a8b0bc")
CLOUD_G = ("#d9dce0", "#9aa0a8", "#4c5158")
CLOUD_D = ("#a8adb4", "#5c6168", "#2a2d33")


def sun(ic, cx, cy, r, rays=True):
    if rays:
        d = ""
        for k in range(12):
            a = 2 * math.pi * k / 12
            r1, r2 = r * 1.25, r * (1.7 if k % 2 == 0 else 1.5)
            w = .16 if k % 2 == 0 else .12
            p = [(cx + r1 * math.cos(a - w), cy + r1 * math.sin(a - w)), (cx + r2 * math.cos(a), cy + r2 * math.sin(a)),
                 (cx + r1 * math.cos(a + w), cy + r1 * math.sin(a + w))]
            d += "M" + "L".join(f"{x:.2f},{y:.2f}" for x, y in p) + "Z"
        ic.path(d, ic.lg([(0, "#fff36a"), (1, "#f0a010")]), INK, .9)
    ic.shadow(circle(cx, cy, r), 1.8, 1.6)
    ic.path(circle(cx, cy, r), ic.rg([(0, SUN[0]), (.5, SUN[1]), (1, SUN[2])], .38, .32, .8), INK, 1.3)


def moon(ic, cx, cy, r):
    d = (f"M{cx + r * .2:.2f},{cy - r:.2f}A{r},{r} 0 1 0 {cx + r:.2f},{cy + r * .35:.2f}"
         f"A{r * .78:.2f},{r * .78:.2f} 0 1 1 {cx + r * .2:.2f},{cy - r:.2f}Z")
    ic.shadow(d, 1.8, 1.6)
    ic.path(d, ic.lg([(0, "#fffbe0"), (.6, "#f0e090"), (1, "#c8a830")], 0, 0, 1, 1), INK, 1.3)


def cloud(ic, cx, cy, s, cols=CLOUD_W):
    d = (f"M{cx - 20 * s:.2f},{cy + 9 * s:.2f}"
         f"A{8 * s:.2f},{8 * s:.2f} 0 0 1 {cx - 15 * s:.2f},{cy - 5 * s:.2f}"
         f"A{11 * s:.2f},{11 * s:.2f} 0 0 1 {cx + 4 * s:.2f},{cy - 10 * s:.2f}"
         f"A{9 * s:.2f},{9 * s:.2f} 0 0 1 {cx + 17 * s:.2f},{cy - 1 * s:.2f}"
         f"A{6.5 * s:.2f},{6.5 * s:.2f} 0 0 1 {cx + 16 * s:.2f},{cy + 9 * s:.2f}Z")
    ic.shadow(d, 2.2, 1.8)
    ic.path(d, ic.lg([(0, cols[0]), (.55, cols[1]), (1, cols[2])], 0, 0, 0, 1), INK, LW)
    ic.add(f'<path d="M{cx - 15 * s:.2f},{cy - 2 * s:.2f}A{9 * s:.2f},{9 * s:.2f} 0 0 1 {cx - 2 * s:.2f},{cy - 8 * s:.2f}" '
           f'fill="none" stroke="#fff" stroke-opacity=".8" stroke-width="{1.6 * s:.2f}" stroke-linecap="round"/>')


def drops(ic, pts, frozen=False):
    for x, y in pts:
        d = f"M{x},{y - 4.6}C{x + 3.4},{y + .4} {x + 3.2},{y + 3.6} {x},{y + 3.6}C{x - 3.2},{y + 3.6} {x - 3.4},{y + .4} {x},{y - 4.6}Z"
        ic.path(d, ic.lg([(0, "#ffffff" if frozen else "#c8ecff"), (.5, "#a8d8f0" if frozen else "#3a9ae0"), (1, "#3a7ab0" if frozen else "#0c4a9a")]), INK, .9)


def flakes(ic, pts, r=3.8):
    for x, y in pts:
        d = "".join(f"M{x - r * math.cos(a):.2f},{y - r * math.sin(a):.2f}L{x + r * math.cos(a):.2f},{y + r * math.sin(a):.2f}"
                    for a in (math.radians(90), math.radians(30), math.radians(150)))
        ic.add(f'<path d="{d}" stroke="#2a5a9a" stroke-width="3" stroke-linecap="round"/>')
        ic.add(f'<path d="{d}" stroke="#ffffff" stroke-width="1.5" stroke-linecap="round"/>')


def hailstones(ic, pts):
    for x, y in pts:
        ic.path(circle(x, y, 2.6), ic.rg([(0, "#ffffff"), (1, "#a8c8e0")], .4, .35, .8), INK, .9)


def bolt(ic, x, y, s=1.0):
    d = (f"M{x + 4 * s:.2f},{y:.2f}L{x - 5 * s:.2f},{y + 13 * s:.2f}H{x + 1 * s:.2f}L{x - 3 * s:.2f},{y + 24 * s:.2f}"
         f"L{x + 9 * s:.2f},{y + 9 * s:.2f}H{x + 3 * s:.2f}L{x + 9 * s:.2f},{y:.2f}Z")
    ic.path(d, ic.lg([(0, "#fffbe0"), (.5, "#ffd21a"), (1, "#c87a04")]), INK, 1.1)


def wind(ic):
    for d in ("M4,48H34Q40,48 40,43Q40,39 36,39", "M4,55H44Q50,55 50,60", "M10,41H22"):
        ic.add(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="4.4" stroke-linecap="round"/>')
        ic.add(f'<path d="{d}" fill="none" stroke="#c3d0dc" stroke-width="2.4" stroke-linecap="round"/>')


def fog_bars(ic, y0, n, light=False):
    for k in range(n):
        y = y0 + k * 7
        x0, x1 = (8 + (k % 2) * 6, 56 - ((k + 1) % 2) * 6)
        d = f"M{x0},{y}H{x1}" if not light else f"M{x0},{y}Q{(x0 + x1) / 2 - 8},{y - 3} {(x0 + x1) / 2},{y}T{x1},{y}"
        ic.add(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>')
        ic.add(f'<path d="{d}" fill="none" stroke="{"#d9dce0" if light else "#9aa0a8"}" stroke-width="3" stroke-linecap="round"/>')


# ------------------------------------------------------------------ composition
def compose(name):
    """Build the icon for a Breeze weather name from the parts."""
    n = name[len("weather-"):]
    night = n.endswith("-night")
    day = n.endswith("-day")
    windy = "-wind" in n
    base = n.replace("-night", "").replace("-day", "").replace("-wind", "")
    ic = Icon()
    sky = moon if night else sun
    def peek(x=18, y=16, r=11):            # sun or moon behind a cloud
        if night:
            moon(ic, x, y, r)
        else:
            sun(ic, x, y, r * .75)
    if base == "clear":
        (moon(ic, 32, 30, 22) if night else sun(ic, 32, 30, 15)) if not windy else (moon(ic, 34, 24, 18) if night else sun(ic, 34, 24, 12))
    elif base == "few-clouds":
        (moon(ic, 24, 22, 17) if night else sun(ic, 24, 22, 12))
        cloud(ic, 40, 42, .85)
    elif base == "clouds":
        (moon(ic, 22, 20, 15) if night else sun(ic, 22, 20, 11))
        cloud(ic, 34, 38, 1.15)
    elif base == "many-clouds":
        cloud(ic, 22, 22, .85, CLOUD_G)
        cloud(ic, 36, 38, 1.1)
    elif base == "overcast":
        cloud(ic, 24, 22, .85, CLOUD_D)
        cloud(ic, 34, 36, 1.15, CLOUD_G)
    elif base == "fog":
        cloud(ic, 32, 20, 1.05, CLOUD_G)
        fog_bars(ic, 38, 3)
    elif base == "mist":
        fog_bars(ic, 18, 5, light=True)
    elif base == "none-available":
        cloud(ic, 32, 30, 1.25, CLOUD_G)
        ic.add(f'<path d="M27,24Q27,18 32,18Q37,18 37,23Q37,27 32.5,29V32" fill="none" stroke="#fff" stroke-width="3.4" stroke-linecap="round"/>')
        ic.path(circle(32.5, 37, 2), "#fff", None)
    else:
        scattered = "scattered" in base
        storm = "storm" in base
        if day or night:
            peek(17, 17, 10)
        cloud(ic, 32, 24, 1.15 if not scattered else 1.05, CLOUD_G if (storm or not scattered) else CLOUD_W)
        lo = 44
        if base.startswith("showers"):
            drops(ic, [(22, lo), (34, lo + 6), (46, lo)] if scattered else [(18, lo), (28, lo + 8), (38, lo), (48, lo + 8)])
        elif base.startswith("freezing"):
            drops(ic, [(20, lo), (40, lo + 4)] if scattered else [(18, lo), (30, lo + 7), (42, lo)], frozen=True)
            flakes(ic, [(30, lo + 2)] if scattered else [(50, lo + 8)], 3.4)
        elif base == "snow-rain":
            drops(ic, [(20, lo), (40, lo + 6)])
            flakes(ic, [(30, lo + 8), (48, lo)])
        elif base.startswith("snow"):
            flakes(ic, [(24, lo + 2), (42, lo + 6)] if scattered else [(18, lo), (30, lo + 8), (42, lo), (52, lo + 9)])
        elif base == "hail":
            hailstones(ic, [(18, lo), (28, lo + 7), (38, lo), (48, lo + 7), (24, lo + 13), (42, lo + 13)])
        elif base == "storm":
            drops(ic, [(16, lo), (48, lo + 4)])
        if storm:
            bolt(ic, 30, 34, 1.05)
    if windy:
        wind(ic)
    return ic


NAMES = """clear clear-night clear-wind clear-wind-night clouds clouds-night clouds-wind clouds-wind-night few-clouds
few-clouds-night few-clouds-wind few-clouds-wind-night fog freezing-rain freezing-rain-day freezing-rain-night
freezing-scattered-rain freezing-scattered-rain-day freezing-scattered-rain-night freezing-scattered-rain-storm
freezing-scattered-rain-storm-day freezing-scattered-rain-storm-night freezing-storm freezing-storm-day freezing-storm-night
hail many-clouds many-clouds-wind mist none-available overcast overcast-wind showers showers-day showers-night
showers-scattered showers-scattered-day showers-scattered-night showers-scattered-storm showers-scattered-storm-day
showers-scattered-storm-night snow snow-day snow-night snow-rain snow-scattered snow-scattered-day snow-scattered-night
snow-scattered-storm snow-scattered-storm-day snow-scattered-storm-night snow-storm snow-storm-day snow-storm-night
storm storm-day storm-night""".split()


def write(out):
    d = f"{out}/scalable/status"
    os.makedirs(d, exist_ok=True)
    for n in NAMES:
        name = f"weather-{n}"
        open(f"{d}/{name}.svg", "w").write(compose(name).svg(64))
        if not os.path.exists(f"{d}/{name}-symbolic.svg"):
            os.symlink(f"{name}.svg", f"{d}/{name}-symbolic.svg")
    for a, t in (("weather-severe-alert", "weather-storm"), ("weather-showers-scattered-night-symbolic", None)):
        if t and not os.path.exists(f"{d}/{a}.svg"):
            os.symlink(f"{t}.svg", f"{d}/{a}.svg")
    return len(NAMES)
