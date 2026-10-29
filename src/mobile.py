"""KDE Classic Vector: mobile broadband signal icons (Plasma's network applet with a mobile modem).

Generated: five glossy signal bars (green when lit, grey when not) for 0-100 %, a small coloured tag for the
network type (G, E, 3G, H, H+, 4G, 5G) using the file-type tag lettering, and a padlock when the SIM is locked.
"""
import os
from gen import Icon, INK, circle, rrect

LEVELS = (0, 20, 40, 60, 80, 100)
TECH = {"gprs": ("g", "slate"), "edge": ("e", "teal"), "umts": ("3g", "blue"), "hsdpa": ("h", "violet"),
        "hsupa": ("h", "violet"), "hspa": ("h+", "indigo"), "lte": ("4g", "orange"), "5g": ("5g", "red")}


def bars(ic, lit, colour=("#c8f8a8", "#3fae2a", "#145a0c"), off=("#ffffff", "#c3c7cd", "#7b818a")):
    for k in range(5):
        h = 12 + k * 10.5
        x, y = 6 + k * 11, 59 - h
        c = colour if k < lit else off
        d = rrect(x, y, 8.4, h, 1.6)
        ic.shadow(d, 1.4, 1.2)
        ic.path(d, ic.lg([(0, c[0]), (.5, c[1]), (1, c[2])], 0, 0, 1, 0), INK, 1.1)


def padlock(ic):
    from dolphin import locked
    ic.add('<g transform="translate(-1,17) scale(.33)">')
    locked(ic)
    ic.add("</g>")


def signal(level, tech=None, lock=False):
    from filetypes import e_label
    ic = Icon()
    bars(ic, level // 20)
    if tech:
        text, col = TECH[tech]
        e_label(text, col, k=1.7 if len(text) == 1 else 1.45, x1=34 if len(text) > 1 else 24, y1=17)(ic)
    if lock:
        padlock(ic)
    return ic


def available():
    ic = Icon()
    bars(ic, 0)
    ic.path(circle(12, 14, 9), ic.rg([(0, "#c8f8a8"), (.55, "#3fae2a"), (1, "#145a0c")], .4, .32, .8), INK, 1.3)
    return ic


def on():
    ic = Icon()
    bars(ic, 5, colour=("#ffffff", "#9aa0a8", "#3c4148"))
    return ic


def off():
    from shell import _badge
    ic = Icon()
    bars(ic, 0)
    _badge(ic, 13, 14, 11, "red", "M8.5,9.5L17.5,18.5M17.5,9.5L8.5,18.5")
    return ic


def write(out):
    d = f"{out}/scalable/status"
    os.makedirs(d, exist_ok=True)
    n = 0
    def put(name, ic):
        nonlocal n
        open(f"{d}/{name}.svg", "w").write(ic.svg(64))
        if not os.path.exists(f"{d}/{name}-symbolic.svg"):
            os.symlink(f"{name}.svg", f"{d}/{name}-symbolic.svg")
        n += 1
    for lv in LEVELS:
        put(f"network-mobile-{lv}", signal(lv))
        put(f"network-mobile-{lv}-locked", signal(lv, lock=True))
        for t in TECH:
            put(f"network-mobile-{lv}-{t}", signal(lv, t))
            put(f"network-mobile-{lv}-{t}-locked", signal(lv, t, True))
    put("network-mobile-available", available())
    put("network-mobile-on", on())
    put("network-mobile-off", off())
    for a, t in (("network-mobile", "network-mobile-100"), ("network-mobile-symbolic", "network-mobile-100")):
        if not os.path.exists(f"{d}/{a}.svg"):
            os.symlink(f"{t}.svg", f"{d}/{a}.svg")
    return n
