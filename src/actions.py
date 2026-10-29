"""KDE Classic Vector: core toolbar and menu actions, redrawn as vectors from the KDE Classic bitmaps
(arrows, refresh, copy/cut/paste, undo/redo, delete, find, new/open/save, stop, zoom, tabs, dialogs ...).

Arrows follow STYLE.md: KDE Classic's teal-blue (#0087AE) with the pale #C5E4EF highlight, crisp mitred
corners, dark outline. Arrows with a meaning keep their colour (green undo/redo/refresh, as the originals).
"""
import math, os
from gen import Icon, INK, LW, circle, rrect, e_house

TEAL = ("#c5e4ef", "#10a8c8", "#0087ae", "#00526e")
GREEN = ("#c8f8b0", "#4cc03a", "#1e8a14", "#0e4a0a")


def _mpath(ic, d, fill, w=LW, extra=""):
    """A filled path with a crisp mitred outline (Icon.path always rounds its joins)."""
    ic.add(f'<path d="{d}" fill="{fill}" stroke="{INK}" stroke-width="{w}" stroke-linejoin="miter" stroke-miterlimit="8"{extra}/>')


def _ic(fn):
    def f():
        ic = Icon()
        fn(ic)
        return ic
    return f


def _block_arrow(ic, angle):
    """KDE Classic's fat block arrow. The outline is the same for all four directions (turned about the
    centre), but it is lit the same way each time, as in the originals: light from the top-left, shadow
    to the lower right, highlight along whichever edges face up or left."""
    pts = [(6, 24), (32, 24), (32, 10), (58, 32), (32, 54), (32, 40), (6, 40)]
    a = math.radians(angle)
    rot = [(32 + (x - 32) * math.cos(a) - (y - 32) * math.sin(a), 32 + (x - 32) * math.sin(a) + (y - 32) * math.cos(a)) for x, y in pts]
    d = "M" + "L".join(f"{x:.2f},{y:.2f}" for x, y in rot) + "Z"
    ic.shadow(d, 2.4, 2)
    _mpath(ic, d, ic.lg([(0, TEAL[0]), (.35, TEAL[1]), (.7, TEAL[2]), (1, TEAL[3])], 0, 0, .35, 1), LW * 1.3)
    # highlight: inset each edge whose outward normal points up or left (polygon is clockwise on screen)
    n = len(rot)
    cx = sum(x for x, _ in rot) / n
    cy = sum(y for _, y in rot) / n
    hl = ""
    for i in range(n):
        (x0, y0), (x1, y1) = rot[i], rot[(i + 1) % n]
        ex, ey = x1 - x0, y1 - y0
        L = math.hypot(ex, ey)
        nx, ny = ey / L, -ex / L                       # outward normal for a clockwise polygon
        if nx * ((x0 + x1) / 2 - cx) + ny * ((y0 + y1) / 2 - cy) < 0:   # make sure it points outward
            nx, ny = -nx, -ny
        if ny < -.3 or nx < -.3:                       # faces up or left
            ix, iy = -nx * 2.2, -ny * 2.2
            t0, t1 = 2.6 / L, 1 - 2.6 / L
            hl += (f"M{x0 + ex * t0 + ix:.2f},{y0 + ey * t0 + iy:.2f}"
                   f"L{x0 + ex * t1 + ix:.2f},{y0 + ey * t1 + iy:.2f}")
    ic.add(f'<path d="{hl}" fill="none" stroke="#ffffff" stroke-opacity=".8" stroke-width="1.6" stroke-linecap="round"/>')


def go_next(ic): _block_arrow(ic, 0)
def go_down(ic): _block_arrow(ic, 90)
def go_previous(ic): _block_arrow(ic, 180)
def go_up(ic): _block_arrow(ic, 270)


def go_home(ic):
    """Home: KDE Classic's little house with the brown door."""
    ic.add('<g transform="translate(3,-51.5) scale(1.95)">')
    e_house(ic, 0, 27, 1.0)
    ic.add("</g>")


def _curl_points(cx, cy, R, t, a_head, sweep, head_len, head_w, kx=1.0, ky=1.0, taper=1.15, rot=0.0, mirror=False, N=48,
                 head_dir=None):
    """Outline points of a curling arrow: a band round part of an ellipse that tapers to a sharp tail,
    ending in a broad arrowhead at angle a_head (degrees, screen coordinates); the band runs clockwise
    from the head through `sweep` degrees to the tail."""
    outer, inner = [], []
    for i in range(N + 1):
        s = i / N
        th = math.radians(a_head + sweep * s)
        w = t * (1 - s ** taper)
        outer.append((cx + (R * kx + w) * math.cos(th), cy + (R * ky + w) * math.sin(th)))
        inner.append((cx + (R * kx - w) * math.cos(th), cy + (R * ky - w) * math.sin(th)))
    th0 = math.radians(a_head)
    bx, by = cx + R * kx * math.cos(th0), cy + R * ky * math.sin(th0)
    tx, ty = kx * math.sin(th0), -ky * math.cos(th0)
    L = math.hypot(tx, ty); tx, ty = tx / L, ty / L
    if head_dir is not None:                             # point the head in an exact direction (degrees)
        tx, ty = math.cos(math.radians(head_dir)), math.sin(math.radians(head_dir))
    nx, ny = -ty, tx
    if nx * math.cos(th0) + ny * math.sin(th0) < 0:
        nx, ny = -nx, -ny
    tip = (bx + tx * head_len, by + ty * head_len)
    if head_dir is not None:
        # cut the band square along the head's base line, so the back edges of both barbs and the end of
        # the band lie on one straight line across the arrow (45 degrees for a head aimed diagonally)
        def trim(curve):
            f = [(x - bx) * tx + (y - by) * ty for x, y in curve]
            for i in range(len(curve) - 1):
                if f[i] >= 0 > f[i + 1]:
                    k = f[i] / (f[i] - f[i + 1])
                    (x0, y0), (x1, y1) = curve[i], curve[i + 1]
                    return [(x0 + (x1 - x0) * k, y0 + (y1 - y0) * k)] + curve[i + 1:]
                if f[i] < 0:
                    return curve[i:]
            return curve
        outer, inner = trim(outer), trim(inner)
    pts = outer + inner[::-1] + [(bx - nx * head_w, by - ny * head_w), tip, (bx + nx * head_w, by + ny * head_w)]
    out = []
    for x, y in pts:
        if mirror:
            x = 64 - x
        if rot:
            r = math.radians(rot)
            x, y = 32 + (x - 32) * math.cos(r) - (y - 32) * math.sin(r), 32 + (x - 32) * math.sin(r) + (y - 32) * math.cos(r)
        out.append((x, y))
    return out


def _curved_arrow(ic, cols, grad=None, **geo):
    """Draw a curling arrow (see _curl_points) filled glossy and lit from the top, with a soft highlight
    along its upper edge."""
    pts = _curl_points(**geo)
    d = "M" + "L".join(f"{x:.2f},{y:.2f}" for x, y in pts) + "Z"
    ic.shadow(d, 2.2, 1.8)
    stops, vec = grad or ([(0, cols[0]), (.3, cols[1]), (.7, cols[2]), (1, cols[3])], (0, 0, .25, 1))
    _mpath(ic, d, ic.lg(stops, *vec), LW * 1.2)



GREY = ("#ffffff", "#b4b9c0", "#6c727a", "#2c3036")


_CURLS = None
CURL_GREEN = ("#b5dec2", "#55b070", "#1e974a", "#0e4f2a")     # colour-picked from KDE Classic's undo/refresh
CURL_GREY = ("#d8d8d8", "#9a9a9a", "#4a4a4a", "#0a0a0a")      # the refresh grey arrow, darkening to near black


def _traced_curl(ic, name):
    """The curled arrows use outlines traced straight from the KDE Classic bitmaps (traced/curls.json),
    filled with the theme's glossy green or grey, lit from the top."""
    global _CURLS
    if _CURLS is None:
        import json
        _CURLS = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "traced", "curls.json")))
    for colour, d, _ in sorted(_CURLS[name], key=lambda p: p[0] == "green"):      # grey first, green on top
        cols = CURL_GREEN if colour == "green" else GREY
        ic.shadow(d, 2.2, 1.8)
        ic.path(d, ic.lg([(0, cols[0]), (.3, cols[1]), (.7, cols[2]), (1, cols[3])], 0, 0, .25, 1), INK, LW * 1.2)


# Smooth curves fitted to the KDE Classic bitmaps (best overlap with each original's outline;
# fitting script kept with the kit as tools/fitcurl.py, results in traced/curls_fit.json).
# undo/redo head: as in the original, a right-angled point (length = half-width) aimed exactly down-left
UNDO_GEO = dict(cx=34.8, cy=34.27, R=19.66, t=8.47, a_head=218.68, sweep=238.18, head_len=19, head_w=19, head_dir=135,
                kx=1.133, ky=.907, taper=1.572)
REFRESH_GEO = dict(cx=38.02, cy=22.53, R=18.16, t=7.85, a_head=174.86, sweep=158.57, head_len=18.76, head_w=17.6,
                   kx=1.113, ky=1.009, taper=1.587)


# green: very light along its top edge, deepening downwards; grey: light at the tail (lower left),
# darkening to near black at the head (upper right) - both as in the original
GREEN_LIT_TOP = ([(0, "#eef9f1"), (.18, "#b5dec2"), (.45, "#55b070"), (.75, "#1e974a"), (1, "#0e4f2a")], (0, 0, .2, 1))
GREY_TAIL_TO_HEAD = ([(0, "#e8e8e8"), (.35, "#a8a8a8"), (.7, "#4a4a4a"), (1, "#0a0a0a")], (0, 1, 1, 0))
REFRESH_TILT = 5.67     # degrees: turns the green head to point straight down (grey straight up)


def refresh(ic):
    """Refresh: KDE Classic's green arrow curling over the top with its head pointing down on the left,
    and the same arrow in grey turned round underneath."""
    ic.add(f'<g transform="translate(32,32) rotate({REFRESH_TILT}) scale(.88) translate(-32,-32)">')
    _curved_arrow(ic, CURL_GREY, grad=GREY_TAIL_TO_HEAD, rot=180, **REFRESH_GEO)
    _curved_arrow(ic, CURL_GREEN, grad=GREEN_LIT_TOP, **REFRESH_GEO)
    ic.add("</g>")


def undo(ic):
    """Undo: KDE Classic's green arrow sweeping up and back to the left, its tail tapering to a point."""
    ic.add('<g transform="translate(32,32) scale(.9) translate(-32,-32)">')
    _curved_arrow(ic, CURL_GREEN, grad=GREEN_LIT_TOP, **UNDO_GEO)
    ic.add("</g>")


def redo(ic):
    """Redo: the undo arrow mirrored."""
    ic.add('<g transform="translate(32,32) scale(.9) translate(-32,-32)">')
    _curved_arrow(ic, CURL_GREEN, grad=GREEN_LIT_TOP, mirror=True, **UNDO_GEO)
    ic.add("</g>")


def _page(ic, x, y, w, h, lines=True, tint=("#ffffff", "#f8e0c8")):
    d = f"M{x},{y}H{x + w - 9}L{x + w},{y + 9}V{y + h}H{x}Z"
    ic.shadow(d, 2.2, 1.8)
    ic.path(d, ic.lg([(0, tint[0]), (.55, tint[0]), (1, tint[1])], 0, 0, 1, 1), INK, LW)
    ic.path(f"M{x + w - 9},{y}V{y + 9}H{x + w}", "#d9dce0", INK, 1)
    if lines:
        for k in range(int((h - 14) / 4.4)):
            ic.add(f'<path d="M{x + 4},{y + 12 + k * 4.4}H{x + w - 6 - (k % 3) * 4}" stroke="#3c4148" stroke-width="1.6" stroke-dasharray="3 1.2"/>')


def copy(ic):
    """Copy: two printed pages, the second laid over the first."""
    _page(ic, 4, 4, 32, 40, tint=("#ffffff", "#e4e6e9"))
    _page(ic, 26, 20, 32, 40)


def cut(ic):
    """Cut: open scissors, handles on the left and blades to the right, as in KDE Classic."""
    ic.add('<g transform="translate(64,0) scale(-1,1)">')
    _cut_shape(ic)
    ic.add("</g>")


def _cut_shape(ic):
    """Open black-handled scissors, blades crossing (drawn blades-left, mirrored by cut())."""
    for sgn in (1, -1):
        blade = f"M30,{32 + sgn * 2}L6,{32 - sgn * 22}L10,{32 - sgn * 24}L36,{32 - sgn * 1}Z"
        ic.path(blade, ic.lg([(0, "#ffffff"), (.5, "#c3c7cd"), (1, "#5c6168")]), INK, 1.2)
    for sgn in (1, -1):
        cx, cy = 48, 32 + sgn * 13
        ic.add(f'<path d="M36,{32 + sgn * 2}L{cx - 5},{cy - sgn * 2}" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>')
        ic.path(circle(cx, cy, 10) + circle(cx, cy, 6), ic.lg([(0, "#5c6168"), (1, "#0a0c10")]), INK, 1.2, ' fill-rule="evenodd"')
    ic.path(circle(32, 32, 2.6), ic.rg([(0, "#ffffff"), (1, "#8a9098")]), INK, 1)


def paste(ic):
    """Paste: KDE Classic's clipboard with a gold clip and a printed page on it."""
    ic.shadow(rrect(6, 8, 38, 50, 3), 2.4, 2)
    ic.path(rrect(6, 8, 38, 50, 3), ic.lg([(0, "#8a9098"), (.5, "#5c6168"), (1, "#2c3036")], 0, 0, 1, 1), INK, LW)
    for k in range(9):
        ic.add(f'<path d="M10,{16 + k * 4.4}H40" stroke="#2c3036" stroke-width="1.6" stroke-dasharray="3 1.4" stroke-opacity=".7"/>')
    ic.path("M16,4H34L38,12H12Z", ic.lg([(0, "#fff4b0"), (.5, "#d8b040"), (1, "#6a5410")]), INK, 1.2)
    _page(ic, 26, 22, 32, 38)


def delete(ic):
    """Delete: a page with a big red cross on it."""
    _page(ic, 10, 4, 42, 56, lines=False)
    d = "M18,24L42,52M42,24L18,52"
    ic.add(f'<path d="{d}" stroke="#7a0a04" stroke-width="7" stroke-linecap="round"/><path d="{d}" stroke="#ec2a1a" stroke-width="4.4" stroke-linecap="round"/>')


def _magnifier(ic, cx=26, cy=26, r=16, handle=20):
    """KDE Classic's magnifier: the handle always runs straight out at 45 degrees from the lens."""
    ex, ey = cx + 11 + handle, cy + 11 + handle
    ic.add(f'<path d="M{cx + 11},{cy + 11}L{ex},{ey}" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>')
    ic.add(f'<path d="M{cx + 11},{cy + 11}L{ex},{ey}" stroke="#3c4148" stroke-width="6.8" stroke-linecap="round"/>')
    ic.add(f'<path d="M{cx + 10},{cy + 10}L{cx + 15},{cy + 15}" stroke="#3ac8e8" stroke-width="7" stroke-linecap="butt"/>')
    ic.shadow(circle(cx, cy, r + 4), 2.2, 1.8)
    ic.path(circle(cx, cy, r + 4), ic.lg([(0, "#ffffff"), (1, "#7b818a")], 0, 0, 1, 1), INK, LW)
    ic.path(circle(cx, cy, r), ic.rg([(0, "#f0faff"), (.6, "#bfe6f4"), (1, "#7ac8e4")], .35, .3, .8), INK, 1, ' fill-opacity=".9"')
    ic.add(f'<path d="M{cx - 9},{cy - 2}Q{cx - 8},{cy - 9} {cx - 1},{cy - 10}" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round"/>')


def find(ic):
    """Find: the magnifier following a trail of grey paw prints, as in KDE Classic."""
    for x, y in ((50, 8), (56, 14), (8, 54), (14, 60)):
        ic.path(circle(x, y, 2.6), "#6c727a", None)
        for dx, dy in ((-2.4, -3.6), (0, -4.4), (2.4, -3.6)):
            ic.path(circle(x + dx, y + dy, 1.1), "#6c727a", None)
    _magnifier(ic)


def _zoom(ic, mark):
    _magnifier(ic)
    ic.add(f'<path d="{mark}" stroke="{INK}" stroke-width="4.4" stroke-linecap="butt"/>')


def zoom_in(ic): _zoom(ic, "M4,54H18M11,47V61")
def zoom_out(ic): _zoom(ic, "M4,54H18")


def zoom_original(ic):
    """Actual size: the magnifier with 1:1 beside it."""
    _magnifier(ic)
    ic.add(f'<path d="M5,50L9,47V61M17,51V52M17,58V59M22,50L26,47V61" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="square"/>')


def new_document(ic):
    """New: a blank page fading from white to peach, as KDE Classic's."""
    _page(ic, 10, 4, 44, 56, lines=False)


def open_document(ic):
    """Open: KDE Classic's orange open folder with a black arrow swinging over it."""
    back = "M4,24Q4,22 6,22H18L21,25H48Q50,25 50,27V56H4Z"
    ic.shadow(back + "M10,32H62L54,58H4Z", 2.6, 2.2)
    ic.path(back, ic.lg([(0, "#ffe0b0"), (1, "#c87a2a")]), INK, LW)
    ic.path("M10,32H62L54,58H4Z", ic.lg([(0, "#d9dce0"), (.5, "#a8adb4"), (1, "#6c727a")], 0, 0, 0, 1), INK, LW)
    ic.add(f'<path d="M20,18Q34,4 50,12" fill="none" stroke="{INK}" stroke-width="3.4" stroke-linecap="round"/>')
    ic.path("M46,4L56,14L44,18Z", INK, None)


def save(ic):
    """Save: KDE Classic's grey floppy disk - metal shutter at the top, label below, chamfered top-right corner."""
    d = "M6,6H52L58,12V58H6Z"
    ic.shadow(d, 2.6, 2.2)
    ic.path(d, ic.lg([(0, "#8a9098"), (.5, "#5c6168"), (1, "#2c3036")], 0, 0, 1, 1), INK, LW)
    ic.path("M16,6H46V26H16Z", ic.lg([(0, "#e4e6e9"), (.5, "#ffffff"), (1, "#a8adb4")], 0, 0, 1, 0), INK, 1.2)
    ic.path("M36,9H43V23H36Z", "#2c3036", INK, .8)
    ic.path("M12,34H52V58H12Z", ic.lg([(0, "#ffffff"), (1, "#d9dce0")]), INK, 1.2)
    for k in range(3):
        ic.add(f'<path d="M16,{40 + k * 5}H48" stroke="#9aa0a8" stroke-width="1.2"/>')


def stop(ic):
    """Stop: KDE Classic's red octagon with a white cross."""
    pts = [(32 + 27 * math.cos(math.radians(22.5 + 45 * k)), 32 + 27 * math.sin(math.radians(22.5 + 45 * k))) for k in range(8)]
    d = "M" + "L".join(f"{x:.2f},{y:.2f}" for x, y in pts) + "Z"
    ic.shadow(d, 2.6, 2.2)
    _mpath(ic, d, ic.rg([(0, "#ffb0a0"), (.5, "#d8201a"), (1, "#6a0804")], .4, .32, .8), LW * 1.3)
    ic.add('<path d="M14,22Q18,12 28,9" fill="none" stroke="#fff" stroke-opacity=".5" stroke-width="2.4" stroke-linecap="round"/>')
    x = "M21,21L43,43M43,21L21,43"
    ic.add(f'<path d="{x}" stroke="#000" stroke-opacity=".3" stroke-width="9" stroke-linecap="round"/><path d="{x}" stroke="#fff" stroke-width="6.6" stroke-linecap="round"/>')


ACTIONS = {
    "go-previous": go_previous, "go-next": go_next, "go-up": go_up, "go-down": go_down, "go-home": go_home,
    "view-refresh": refresh, "edit-copy": copy, "edit-cut": cut, "edit-paste": paste, "edit-undo": undo,
    "edit-redo": redo, "edit-delete": delete, "edit-find": find, "document-new": new_document,
    "document-open": open_document, "document-save": save, "process-stop": stop, "zoom-in": zoom_in,
    "zoom-out": zoom_out, "zoom-original": zoom_original,
}
ACTION_ALIASES = {
    "go-previous-symbolic": "go-previous", "go-next-symbolic": "go-next", "go-up-symbolic": "go-up", "go-down-symbolic": "go-down",
    "go-home-symbolic": "go-home", "go-next-rtl-symbolic": "go-previous", "go-previous-rtl-symbolic": "go-next",
    "go-next-symbolic-rtl": "go-previous", "go-previous-symbolic-rtl": "go-next", "go-previous-view": "go-previous",
    "go-next-view": "go-next", "go-parent-folder": "go-up", "view-refresh-symbolic": "view-refresh", "reload": "view-refresh",
    "edit-copy-symbolic": "edit-copy", "edit-duplicate": "edit-copy", "edit-cut-symbolic": "edit-cut",
    "edit-paste-symbolic": "edit-paste", "edit-undo-symbolic": "edit-undo", "edit-redo-symbolic": "edit-redo",
    "edit-delete-symbolic": "edit-delete", "edit-find-symbolic": "edit-find", "document-new-symbolic": "document-new",
    "document-open-symbolic": "document-open", "document-save-symbolic": "document-save", "process-stop-symbolic": "process-stop",
    "zoom-in-symbolic": "zoom-in", "zoom-out-symbolic": "zoom-out", "zoom-original-symbolic": "zoom-original",
    "edit-find-replace": "edit-find", "document-save-as": "document-save", "go-jump": "go-next",
}
ACTION_CROSS = {"list-remove": "value-decrease.svg", "list-remove-symbolic": "value-decrease.svg"}


def write(out):
    d = f"{out}/scalable/actions"
    os.makedirs(d, exist_ok=True)
    for name, fn in ACTIONS.items():
        open(f"{d}/{name}.svg", "w").write(_ic(fn)().svg(64))
    for a, t in {**ACTION_ALIASES, **ACTION_CROSS}.items():
        t = t if t.endswith(".svg") else f"{t}.svg"
        if os.path.exists(f"{d}/{t}") and not os.path.exists(f"{d}/{a}.svg"):
            os.symlink(t, f"{d}/{a}.svg")
    return len(ACTIONS)
