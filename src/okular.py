"""KDE Classic Vector: Okular - its page-layout modes, colour modes, annotation tools and the other toolbar
icons it asks for that the rest of the set did not already cover. Runs after kdeapps, so aliases can point
anywhere.
"""
import math, os
from gen import Icon, INK, LW, circle, rrect
from settingstrace import _teal, _arrow_pts, _badge, _poly, _double_arrow


def _ic(fn):
    def f():
        ic = Icon()
        fn(ic)
        return ic
    return f


def _pg(ic, x, y, w, h, lines=True):
    """A small printed page (the copy icon's page), with text lines scaled to its size."""
    d = f"M{x},{y}H{x + w - w * .25:.2f}L{x + w},{y + w * .25:.2f}V{y + h}H{x}Z"
    ic.shadow(d, 1.8, 1.5)
    ic.path(d, ic.lg([(0, "#ffffff"), (.55, "#ffffff"), (1, "#f8e0c8")], 0, 0, 1, 1), INK, LW)
    ic.path(f"M{x + w - w * .25:.2f},{y}V{y + w * .25:.2f}H{x + w}", "#d9dce0", INK, 1)
    if lines:
        n = int((h - w * .25 - 4) / 3.6)
        for k in range(n):
            yy = y + w * .25 + 3 + k * 3.6
            ic.add(f'<path d="M{x + 3},{yy:.1f}H{x + w - 3 - (k % 3) * 2.5:.1f}" stroke="#3c4148" stroke-width="1.3" stroke-dasharray="2.4 1"/>')


# ------------------------------------------------------------------ page layouts
def view_pages_single(ic):
    _pg(ic, 14, 3, 36, 58)


def view_pages_facing(ic):
    _pg(ic, 3, 8, 28, 46)
    _pg(ic, 33, 8, 28, 46)


def view_pages_facing_first_centered(ic):
    """Facing pages, first centred: one page on its own at the top, then a facing pair below."""
    _pg(ic, 21, 2, 22, 28)
    _pg(ic, 8, 34, 22, 28)
    _pg(ic, 34, 34, 22, 28)


def view_pages_continuous(ic):
    """Continuous: pages running on down the screen, with a teal arrow scrolling down."""
    _pg(ic, 10, -30, 30, 48)
    _pg(ic, 10, 25, 30, 39)
    _teal(ic, _poly(_arrow_pts(53, 6, 53, 56, 3.4, 8.5, 10)))


def view_pages_overview(ic):
    for x in (4, 34):
        for y in (2, 33):
            _pg(ic, x, y, 26, 29)


# ------------------------------------------------------------------ zoom
def zoom_fit_width(ic):
    """Fit width: a page with a teal arrow spanning it from edge to edge."""
    _pg(ic, 10, 4, 44, 56)
    _teal(ic, _double_arrow(2, 34, 62, 34, 3.6, 9, 10))


# ------------------------------------------------------------------ colour modes
def color_mode_black_white(ic):
    """Black and white: a disc split into black and white halves."""
    c = circle(32, 32, 26)
    ic.shadow(c, 2.4, 2)
    ic.path(c, "#ffffff", None)
    ic.path("M32,6A26,26 0 0,1 32,58Z", ic.lg([(0, "#5c6168"), (1, "#000000")], 0, 0, 1, 1), None)
    ic.path(c, "none", INK, LW * 1.4)


def color_mode_invert_text(ic):
    """Invert lightness: a page in negative - pale text lines on a black sheet."""
    d = "M10,3H43L54,14V61H10Z"
    ic.shadow(d, 2.2, 1.8)
    ic.path(d, ic.lg([(0, "#3c4148"), (1, "#000000")], 0, 0, 1, 1), INK, LW)
    ic.path("M43,3V14H54", "#5c6168", INK, 1)
    for k in range(9):
        ic.add(f'<path d="M15,{20 + k * 4.4}H{48 - (k % 3) * 5}" stroke="#ffffff" stroke-width="1.6" stroke-dasharray="3 1.2"/>')


def _wheel(ic, cx=32, cy=32, r=22):
    cols = ("#e0281a", "#ec9a3a", "#e8c43a", "#4fae5a", "#3cc4d4", "#2a6ac8", "#9a62d8", "#d83a9a")
    for k, c in enumerate(cols):
        t0, t1 = 2 * math.pi * k / 8 - math.pi / 2, 2 * math.pi * (k + 1) / 8 - math.pi / 2
        d = (f"M{cx},{cy}L{cx + r * math.cos(t0):.2f},{cy + r * math.sin(t0):.2f}"
             f"A{r},{r} 0 0,1 {cx + r * math.cos(t1):.2f},{cy + r * math.sin(t1):.2f}Z")
        ic.path(d, ic.lg([(0, "#ffffff"), (.4, c), (1, c)], 0, 0, 1, 1), None)
    ic.path(circle(cx, cy, r), "none", INK, LW)
    ic.path(circle(cx, cy, 6), ic.rg([(0, "#ffffff"), (1, "#c3c7cd")], .4, .35, .8), INK, 1)


def _hue_shift(ic, clockwise):
    _wheel(ic, 30, 34, 20)
    from actions import _curl_points
    # a teal arc running round the top of the wheel, pointing the way the hues turn
    pts = []
    a0, a1 = (200, 340) if clockwise else (340, 200)
    n = 24
    for i in range(n + 1):
        a = math.radians(a0 + (a1 - a0) * i / n)
        pts.append((30 + 27 * math.cos(a), 34 + 27 * math.sin(a)))
    w = 3.4
    out = [(30 + (27 + w) * math.cos(math.atan2(y - 34, x - 30)), 34 + (27 + w) * math.sin(math.atan2(y - 34, x - 30))) for x, y in pts]
    inn = [(30 + (27 - w) * math.cos(math.atan2(y - 34, x - 30)), 34 + (27 - w) * math.sin(math.atan2(y - 34, x - 30))) for x, y in pts]
    ex, ey = pts[-1]
    ang = math.atan2(ey - 34, ex - 30)
    tx, ty = -math.sin(ang), math.cos(ang)          # tangent, direction of increasing angle
    if not clockwise:
        tx, ty = -tx, -ty
    hx, hy = ex + tx * 11, ey + ty * 11
    nx, ny = math.cos(ang), math.sin(ang)
    head = [(ex + nx * 9, ey + ny * 9), (hx, hy), (ex - nx * 9, ey - ny * 9)]
    _teal(ic, _poly(out[:-1] + [out[-1]] + [head[0], head[1], head[2]] + [inn[-1]] + inn[::-1][1:]))


def color_mode_hue_shift_positive(ic): _hue_shift(ic, True)
def color_mode_hue_shift_negative(ic): _hue_shift(ic, False)


# ------------------------------------------------------------------ annotation tools
def _colour_bar(ic, col="#e0281a"):
    ic.path("M4,52H60V61H4Z", ic.lg([(0, "#ffffff"), (.3, col), (1, col)], 0, 0, 0, 1), INK, LW)


def format_text_color(ic):
    """Text colour: a bold letter A over a red colour bar."""
    d = "M8,46L26,4H38L56,46H45L41,36H23L19,46ZM26,27H38L32,12Z"
    ic.shadow(d, 2.2, 1.8)
    ic.path(d, ic.lg([(0, "#4c5158"), (1, "#000000")]), INK, .8, ' fill-rule="evenodd"')
    _colour_bar(ic)


def underline_squiggle(ic):
    """Squiggly underline: the underline letter U with a wavy red line beneath."""
    d = "M8,4H26V8H22V30Q22,40 32,40Q42,40 42,30V8H38V4H56V8H50V30Q50,47 32,47Q14,47 14,30V8H8Z"
    ic.shadow(d, 2.2, 1.8)
    ic.path(d, ic.lg([(0, "#4c5158"), (1, "#000000")]), INK, .8)
    w = "M4,56" + "".join(f"Q{7 + 8 * k},{50 if k % 2 == 0 else 62} {11 + 8 * k},56" for k in range(7))
    ic.add(f'<path d="{w}" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
           f'<path d="{w}" fill="none" stroke="#e0281a" stroke-width="3" stroke-linecap="round"/>')


def edit_line_width(ic):
    """Line width: three strokes, thin to thick."""
    for y, h in ((10, 2), (24, 5), (42, 10)):
        ic.path(f"M6,{y}H58V{y + h}H6Z", ic.lg([(0, "#5c6168"), (1, "#000000")], 0, 0, 0, 1), INK, .8)


def snap_angle(ic):
    """Snap to angle: two arms from a corner with the angle marked and ticks every 15 degrees."""
    ox, oy = 8, 56
    for a in range(0, 91, 15):
        r = math.radians(-a)
        x0, y0 = ox + 34 * math.cos(r), oy + 34 * math.sin(r)
        x1, y1 = ox + 40 * math.cos(r), oy + 40 * math.sin(r)
        ic.add(f'<path d="M{x0:.1f},{y0:.1f}L{x1:.1f},{y1:.1f}" stroke="{INK}" stroke-width="1.8"/>')
    ic.add(f'<path d="M{ox + 22},{oy}A22,22 0 0,0 {ox + 22 * math.cos(math.radians(-45)):.1f},{oy + 22 * math.sin(math.radians(-45)):.1f}" '
           f'fill="none" stroke="#e0281a" stroke-width="2.6"/>')
    for a in (0, -45):
        r = math.radians(a)
        d = f"M{ox},{oy}L{ox + 54 * math.cos(r):.1f},{oy + 54 * math.sin(r):.1f}"
        ic.add(f'<path d="{d}" stroke="{INK}" stroke-width="5.4" stroke-linecap="round"/>'
               f'<path d="{d}" stroke="#3d9ad8" stroke-width="3" stroke-linecap="round"/>')
    ic.path(circle(ox, oy, 4), ic.rg([(0, "#ffffff"), (1, "#7b818a")], .4, .35, .8), INK, 1.2)


def mail_attachment(ic):
    """Attachment: a steel paper clip."""
    d = "M40,14V46Q40,58 30,58Q20,58 20,46V12Q20,4 28,4Q36,4 36,12V44Q36,50 30,50Q24,50 24,44V18"
    ic.add(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="6.4" stroke-linecap="round" stroke-linejoin="round" transform="rotate(30 30 32)"/>'
           f'<path d="{d}" fill="none" stroke="url(#clipsteel)" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round" transform="rotate(30 30 32)"/>'
           f'<path d="{d}" fill="none" stroke="#ffffff" stroke-opacity=".6" stroke-width="1" stroke-linecap="round" transform="rotate(30 30 32) translate(-.6,-.6)"/>')
    ic.defs.append('<linearGradient id="clipsteel" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffffff"/>'
                   '<stop offset=".5" stop-color="#a8adb4"/><stop offset="1" stop-color="#5c6168"/></linearGradient>')


def document_edit_sign(ic):
    """Sign: a page with a signature line, a red signature scrawled on it and the orange pencil."""
    from uitrace import _pencil
    _pg(ic, 4, 4, 42, 56, lines=False)
    for k in range(4):
        ic.add(f'<path d="M9,{20 + k * 4.4}H{40 - (k % 3) * 4}" stroke="#3c4148" stroke-width="1.4" stroke-dasharray="3 1.2"/>')
    ic.add(f'<path d="M9,52H40" stroke="{INK}" stroke-width="1.2"/>'
           '<path d="M10,48Q13,38 16,46Q18,52 21,42Q23,36 25,46Q27,52 31,44L36,47" fill="none" stroke="#1a3ab0" stroke-width="2" stroke-linecap="round"/>')
    _pencil(ic, "translate(44,4) rotate(30 6 26) scale(.85)")


def _tree(ic):
    for y, x in ((6, 6), (24, 18), (42, 18)):
        ic.path(rrect(x, y, 34 if x == 6 else 30, 12, 2), ic.lg([(0, "#ffffff"), (1, "#c3c7cd")], 0, 0, 0, 1), INK, 1.2)
    ic.add(f'<path d="M11,18V48H18M11,30H18" fill="none" stroke="{INK}" stroke-width="1.6"/>')


def expand_all(ic):
    _tree(ic)
    _badge(ic, 49, 49, 12, "green", "M49,43V55M43,49H55")


def collapse_all(ic):
    _tree(ic)
    _badge(ic, 49, 49, 12, "red", "M43,49H55")


OK = {
    "actions": {"view-pages-single": view_pages_single, "view-pages-facing": view_pages_facing,
                "view-pages-facing-first-centered": view_pages_facing_first_centered,
                "view-pages-continuous": view_pages_continuous, "view-pages-overview": view_pages_overview,
                "zoom-fit-width": zoom_fit_width, "color-mode-black-white": color_mode_black_white,
                "color-mode-invert-text": color_mode_invert_text,
                "color-mode-hue-shift-positive": color_mode_hue_shift_positive,
                "color-mode-hue-shift-negative": color_mode_hue_shift_negative,
                "format-text-color": format_text_color, "format-text-underline-squiggle": underline_squiggle,
                "edit-line-width": edit_line_width, "snap-angle": snap_angle, "mail-attachment": mail_attachment,
                "document-edit-sign": document_edit_sign, "expand-all": expand_all, "collapse-all": collapse_all},
}

OK_ALIASES = {
    "org.kde.okular": "okular", "go-down-search": "go-down", "go-up-search": "go-up",
    "dialog-text-and-font": "preferences-desktop-font", "font-face": "preferences-desktop-font",
    "preferences-system-performance": "speedometer", "tool-text": "draw-text", "note": "knotes",
    "draw-polyline": "draw-polygon", "view-certificate": "application-pkcs7-signature",
    "view-certificate-symbolic": "application-pkcs7-signature", "bookmarks-organize": "bookmarks",
    "view-table-of-contents-ltr": "view-list-tree", "view-table-of-contents-rtl": "view-list-tree",
    "draw-eraser-delete-objects": "draw-eraser", "invertimage": "contrast", "color-mode-invert-image": "contrast",
    "page-2sides": "actions/view-pages-facing", "page-zoom": "zoom-in", "trim-to-selection": "transform-crop",
    "view-pages-overview-symbolic": "actions/view-pages-overview", "zoom-fit-width-symbolic": "actions/zoom-fit-width",
    "mail-attachment-symbolic": "actions/mail-attachment", "document-edit-sign-symbolic": "actions/document-edit-sign",
}


def _find(out, name):
    for ctx in os.listdir(f"{out}/scalable"):
        if os.path.lexists(f"{out}/scalable/{ctx}/{name}.svg"):
            return ctx
    return None


def write(out):
    n = 0
    for ctx, icons in OK.items():
        d = f"{out}/scalable/{ctx}"
        for name, fn in icons.items():
            p = f"{d}/{name}.svg"
            if os.path.lexists(p):
                os.remove(p)
            open(p, "w").write(_ic(fn)().svg(64))
            n += 1
    missing = []
    for a, t in OK_ALIASES.items():
        ctx, name = t.split("/") if "/" in t else (_find(out, t), t)
        if ctx is None or not os.path.exists(f"{out}/scalable/{ctx}/{name}.svg"):
            missing.append(t)
            continue
        if _find(out, a) is None:
            os.symlink(f"{name}.svg", f"{out}/scalable/{ctx}/{a}.svg")
    if missing:
        print("okular: alias targets missing:", missing)
    return n
