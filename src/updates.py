"""KDE Classic Vector: Discover's update states and app icon, redrawn around the open cardboard box -
updates are a box with a coloured arrow badge (blue / orange / red by priority, green tick when up to date),
and Discover itself is the open box with software inside. Runs after pim.
"""
import os
from gen import Icon, INK, LW, circle, rrect
from settingstrace import _badge, _ok


def _ic(fn):
    def f():
        ic = Icon()
        fn(ic)
        return ic
    return f


BOX = "translate(-1,-4) scale(1.12)"          # the open box, enlarged to fill the canvas


def _box(ic, inside=None, tf=BOX):
    from discover import _open_box
    ic.add(f'<g transform="{tf}">')
    _open_box(ic, inside)
    ic.add("</g>")


def _disc(ic, colour, glyph):
    """The previous update disc (same proportions, slim arrow) shrunk into the lower right corner."""
    from dolphin import badge
    k = .5
    ic.add(f'<g transform="translate({48 - 32 * k},{48 - 32 * k}) scale({k})">')
    badge(ic, colour, glyph)
    ic.add("</g>")


ARROW, TICK = "M32,16V45M21,35L32,46L43,35", "M19,33L28,42L45,23"


def update_low(ic):     _box(ic); _disc(ic, "blue", ARROW)
def update_medium(ic):  _box(ic); _disc(ic, "amber", ARROW)
def update_high(ic):    _box(ic); _disc(ic, "red", ARROW)
def update_none(ic):    _box(ic); _disc(ic, "green", TICK)


def update_busy(ic):
    """Checking for updates: the box with a grey badge of three dots."""
    _box(ic)
    _badge(ic, 48, 48, 13, "grey", "")
    for x in (42, 48, 54):
        ic.path(circle(x, 48, 2.2), "#ffffff", None)


# ------------------------------------------------------------------ Discover
def _cubes(ic):
    from uitrace import _iso_cube
    _iso_cube(ic, 17, 0, 10, ("#ffd0c4", "#e8573d", "#b02a1a", "#5e1408"))
    _iso_cube(ic, 36, -4, 10, ("#c4ecff", "#3d9ad8", "#1a5c9e", "#0a2c5e"))
    _iso_cube(ic, 27, 8, 10, ("#d0f5c8", "#4fae5a", "#22703a", "#0e3a18"))


APP_BOX = "translate(-1,3) scale(1.08)"


def discover_cubes(ic):
    """Option A: the open box with three coloured blocks (the apps) rising out of it."""
    _box(ic, _cubes, APP_BOX)


def _goods(ic):
    from pim import _embed
    _embed(ic, "internet-web-browser", "translate(2,-8) scale(.5) rotate(-12 32 32)")
    _embed(ic, "applications-games", "translate(26,-6) scale(.46) rotate(10 32 32)")
    _embed(ic, "accessories-text-editor", "translate(13,0) scale(.46)")


def discover_goods(ic):
    """Option B: the open box with software poking out of it - a browser globe, a game and an editor."""
    _box(ic, _goods, APP_BOX)


UP = {"status": {"update-low": update_low, "update-medium": update_medium, "update-high": update_high,
                 "update-none": update_none, "update-busy": update_busy}}
DISCOVER_STYLE = "cubes"           # "cubes" (blocks rising out) or "goods"; None keeps the parcel


def write(out):
    import pim
    pim.OUT = out
    reg = {k: dict(v) for k, v in UP.items()}
    if DISCOVER_STYLE:
        reg.setdefault("apps", {})["plasmadiscover"] = {"cubes": discover_cubes, "goods": discover_goods}[DISCOVER_STYLE]
    n = 0
    for ctx, icons in reg.items():
        for name, fn in icons.items():
            for c in os.listdir(f"{out}/scalable"):
                p = f"{out}/scalable/{c}/{name}.svg"
                if os.path.lexists(p):
                    os.remove(p)
            open(f"{out}/scalable/{ctx}/{name}.svg", "w").write(_ic(fn)().svg(64))
            n += 1
    # the -symbolic names follow the drawings into status/ (earlier modules linked them in actions/)
    for name in reg.get("status", {}):
        for c in os.listdir(f"{out}/scalable"):
            p = f"{out}/scalable/{c}/{name}-symbolic.svg"
            if os.path.lexists(p):
                os.remove(p)
        os.symlink(f"{name}.svg", f"{out}/scalable/status/{name}-symbolic.svg")
    return n
