"""KDE Classic Vector: session and power buttons (Leave screen, launcher, panel).

Drawn in the style of KDE 3's own Lock and Exit buttons: a glossy rounded tile in a colour of its
own, with a bold white symbol. Each has a 64 px drawing and bolder 16/22 px versions.
"""
import math
from gen import Icon, INK, circle, rrect

TILE = {   # light, mid, dark
    "blue": ("#9ad0ff", "#2a6ac8", "#0e2e6a"), "amber": ("#ffd890", "#d8820e", "#6a3a04"),
    "teal": ("#a8f0e8", "#1a9a9a", "#064a4a"), "night": ("#8aa0f0", "#2a3aa8", "#0a1050"),
    "violet": ("#e0b8ff", "#8a3ad0", "#3a0e6a"), "green": ("#b8f0a0", "#2f9a2e", "#0e4a12"),
    "red": ("#ffb0a0", "#c8301a", "#5a0a04"),
}


def tile(ic, colour, small):
    c = TILE[colour]
    t = rrect(5, 5, 54, 54, 11)
    if not small:
        ic.shadow(t, 2.6, 2.4)
    ic.path(t, ic.lg([(0, c[0]), (.45, c[1]), (1, c[2])], 0, 0, .35, 1), INK, 3.2 if small else 1.6)
    # gloss over the top half
    ic.add('<path d="M9,17Q9,9 17,9H47Q55,9 55,17V27Q32,34 9,27Z" fill="#fff" fill-opacity="' + (".22" if small else ".3") + '"/>')


def glyph(ic, d, w, small, fill=False):
    """White symbol with a thin dark edge so it holds up on the light top of the tile."""
    k = 1.35 if small else 1
    if fill:
        ic.add(f'<path d="{d}" fill="#fff" stroke="#000" stroke-opacity=".35" stroke-width="{2.2 * k:.2f}" stroke-linejoin="round"/>')
        ic.add(f'<path d="{d}" fill="#fff"/>')
    else:
        ic.add(f'<path d="{d}" fill="none" stroke="#000" stroke-opacity=".35" stroke-width="{(w + 2.2) * k:.2f}" stroke-linecap="round" stroke-linejoin="round"/>')
        ic.add(f'<path d="{d}" fill="none" stroke="#fff" stroke-width="{w * k:.2f}" stroke-linecap="round" stroke-linejoin="round"/>')


def power(ic, small):
    tile(ic, "red", small)
    glyph(ic, "M24.5,21.5A14,14 0 1 0 39.5,21.5 M32,15.5V32", 5.2, small)


def logout(ic, small):
    tile(ic, "amber", small)
    glyph(ic, "M30,16H18.5V48H30", 4.6, small)                         # door frame
    glyph(ic, "M24,32H46M38.5,24.5L46,32L38.5,39.5", 4.8, small)       # arrow out


def switch_user(ic, small):
    tile(ic, "teal", small)
    for cx, cy, s in ((24.5, 25, 1.0), (40, 29, .9)):
        head = circle(cx, cy, 5.6 * s)
        body = (f"M{cx - 10 * s},{cy + 21 * s}C{cx - 10 * s},{cy + 12 * s} {cx - 6 * s},{cy + 8.5 * s} {cx},{cy + 8.5 * s}"
                f"C{cx + 6 * s},{cy + 8.5 * s} {cx + 10 * s},{cy + 12 * s} {cx + 10 * s},{cy + 21 * s}Z")
        glyph(ic, head + body, 0, small, fill=True)


def suspend(ic, small):
    tile(ic, "night", small)
    glyph(ic, "M38,15.5A17,17 0 1 0 47.5,40A13.5,13.5 0 1 1 38,15.5Z", 0, small, fill=True)


def hibernate(ic, small):
    tile(ic, "violet", small)
    d = ""
    for k in range(3):
        a = math.radians(90 + k * 60)
        ca, sa = math.cos(a), math.sin(a)
        d += f"M{32 - 15 * ca:.2f},{32 - 15 * sa:.2f}L{32 + 15 * ca:.2f},{32 + 15 * sa:.2f}"
        for sgn in (1, -1):        # little branches near each tip
            ex, ey = 32 + sgn * 10 * ca, 32 + sgn * 10 * sa
            for side in (1, -1):
                b = a + side * math.radians(40)
                d += f"M{ex:.2f},{ey:.2f}L{ex + sgn * 5 * math.cos(b):.2f},{ey + sgn * 5 * math.sin(b):.2f}"
    glyph(ic, d, 3.4, small)


def reboot(ic, small):
    tile(ic, "green", small)
    glyph(ic, "M44.9,26.2A14,14 0 1 0 45.5,36.5", 5, small)
    glyph(ic, "M49.6,22.2L48.2,31.4L40.4,26.6Z", 0, small, fill=True)    # arrowhead on the arc's start, pointing clockwise


def lock(ic, small):
    tile(ic, "blue", small)
    glyph(ic, "M24.5,31V24.5A7.5,7.5 0 0 1 39.5,24.5V31", 4.6, small)
    glyph(ic, "M20.5,30.5H43.5V47H20.5Z", 0, small, fill=True)
    ic.path("M32,35.4A2.4,2.4 0 0 1 33.3,39.8V42.4H30.7V39.8A2.4,2.4 0 0 1 32,35.4Z", TILE["blue"][2], None)


def _icon(fn):
    def f(small=False):
        ic = Icon()
        fn(ic, small)
        return ic
    return f


SESSION = {
    "system-shutdown": _icon(power), "system-log-out": _icon(logout), "system-switch-user": _icon(switch_user),
    "system-suspend": _icon(suspend), "system-hibernate": _icon(hibernate), "system-reboot": _icon(reboot),
    "system-lock-screen": _icon(lock),
}
SESSION_ALIASES = {
    "system-suspend-hibernate": "system-hibernate", "system-suspend-hybrid": "system-hibernate",
    "system-restart": "system-reboot", "system-log-out-rtl": "system-log-out", "application-exit": "system-log-out",
    "lock": "system-lock-screen", "xfsm-lock": "system-lock-screen", "system-sleep": "system-suspend",
    "gnome-session-halt": "system-shutdown", "gnome-session-reboot": "system-reboot", "gnome-session-logout": "system-log-out",

}


def write(out):
    import os
    n = 0
    for sub, size, small in (("scalable", 64, False), ("22x22", 22, True), ("16x16", 16, True)):
        d = f"{out}/{sub}/actions"
        os.makedirs(d, exist_ok=True)
        for name, fn in SESSION.items():
            open(f"{d}/{name}.svg", "w").write(fn(small).svg(size))
            n += sub == "scalable"
        for a, t in SESSION_ALIASES.items():
            if not os.path.exists(f"{d}/{a}.svg"):
                os.symlink(f"{t}.svg", f"{d}/{a}.svg")
    return n
