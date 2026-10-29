"""KDE Classic Vector: the last of Dolphin's toolbar, dialog, tab and help icons, redrawn as vectors from the
KDE Classic bitmaps they used to fall back to (bookmarks, configure, warnings, tabs, playback, text format ...).

Shared parts: the yellow "new" sparkle (bookmark-new, tab-new, window-new, code-class), the yellow warning
triangle, the grey tab strip and the orange pencil. Lighting from the top-left, Qt-SVG safe.
"""
import math, os
from gen import Icon, INK, LW, circle, rrect
from actions import _mpath

STEEL = ("#ffffff", "#c3c7cd", "#7b818a", "#3c4148")


def _ic(fn):
    def f():
        ic = Icon()
        fn(ic)
        return ic
    return f


def _poly(pts):
    return "M" + "L".join(f"{x:.2f},{y:.2f}" for x, y in pts) + "Z"


# ------------------------------------------------------------------ shared parts
def _sparkle(ic, cx, cy, r):
    """KDE Classic's 'new' sparkle: a glowing yellow burst with long and short rays and a white heart."""
    ic.path(circle(cx, cy, r * .95), ic.rg([(0, "#fffbd0"), (.5, "#fff36a"), (1, "#fff36a")], .5, .5, .5), None, ' fill-opacity=".35"')
    pts = []
    for k in range(24):
        a = 2 * math.pi * k / 24 - math.pi / 2
        rr = r if k % 4 == 0 else (r * .62 if k % 2 == 0 else r * .42)
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d = _poly(pts)
    ic.shadow(d, 1.8, 1.5)
    ic.path(d, ic.rg([(0, "#ffffff"), (.3, "#fffb9a"), (.65, "#f8e020"), (1, "#c89a04")], .5, .5, .55), "#6a5004", 1)
    ic.path(circle(cx, cy, r * .2), "#ffffff", None)


def _new_badge(ic, cx, cy, r):
    """'New': a green plus badge (2026-10-27: replaces the yellow sparkle on new-item actions, which read poorly
    at small sizes; the sparkle stays where it means magic or a class, not 'new'). Same style as Group New."""
    from shell import _badge
    rb = r * .82
    k = rb * .55
    _badge(ic, cx, cy, rb, "green", f"M{cx - k:.2f},{cy:.2f}H{cx + k:.2f}M{cx:.2f},{cy - k:.2f}V{cy + k:.2f}")


def _pencil(ic, transform):
    """The orange KDE Classic pencil, drawn upright with its point at (6,52), placed by `transform`."""
    ic.add(f'<g transform="{transform}">')
    ic.shadow("M0,0H12V42L6,52L0,42Z", 2, 1.6)
    ic.path("M0,0H12V42L6,52L0,42Z", ic.lg([(0, "#ffd08a"), (.5, "#f08a1a"), (1, "#a84c04")], 0, 0, 1, 0), INK, 1.3)
    ic.add('<path d="M4,2V40" stroke="#fff" stroke-opacity=".55" stroke-width="1.2"/>')
    ic.path("M0,42L6,52L12,42Z", "#f4d8b0", INK, 1)
    ic.path("M4.4,48.4L6,52L7.6,48.4Z", INK, None)
    ic.path("M0,-2Q0,-5 3,-5H9Q12,-5 12,-2V2H0Z", "#ff8aa0", INK, 1)
    ic.path("M0,1H12V4H0Z", ic.lg([(0, "#ffffff"), (1, "#8a9098")], 0, 0, 1, 0), INK, .8)
    ic.add("</g>")


def _warn_tri(ic, x0=4, y0=5, x1=60, y1=57, corner=True):
    """KDE Classic's warning sign: a flat yellow triangle, black edge, the lower right corner in shadow."""
    cx = (x0 + x1) / 2
    d = f"M{cx},{y0}L{x1},{y1}H{x0}Z"
    ic.shadow(d, 2.6, 2.2)
    ic.path(d, ic.lg([(0, "#ffff8a"), (.3, "#ffff10"), (1, "#f0e000")], 0, 0, .4, 1), INK, LW * 1.4)
    if corner:
        w = (x1 - x0) * .2
        ic.path(f"M{x1 - w * .55},{y1 - w * 1.0}L{x1 - 1.6},{y1 - .9}H{x1 - w * 1.15}Z", "#b8a800", None)
    h = y1 - y0
    bw = (x1 - x0) * .085
    top, bot = y0 + h * .3, y0 + h * .7
    ic.path(f"M{cx - bw},{top}Q{cx},{top - bw * 1.2} {cx + bw},{top}L{cx + bw * .45},{bot}H{cx - bw * .45}Z", INK, None)
    ic.path(circle(cx, y0 + h * .82, bw * .95), INK, None)


def _tabs(ic, y=30, h=14, active=0):
    """A strip of two KDE Classic tabs over the page they belong to."""
    page = f"M2,{y + h}H62V62H2Z"
    ic.path(page, ic.lg([(0, "#ffffff"), (1, "#e4e6e9")]), None)
    ic.add(f'<path d="M2,{y + h}H62" stroke="#9aa0a8" stroke-width="2"/>')
    tabs = [(4, 32), (30, 58)]
    order = [1 - active, active]
    for i in order:
        a, b = tabs[i]
        d = f"M{a},{y + h}L{a + 6},{y}H{b - 6}L{b},{y + h}Z"
        lit = i == active
        cols = [(0, "#f4f5f7"), (1, "#c3c7cd")] if lit else [(0, "#a8adb4"), (1, "#5c6168")]
        ic.shadow(d, 1.8, 1.4)
        _mpath(ic, d, ic.lg(cols), 1.4)
        ic.add(f'<path d="M{a + 7},{y + 2}H{b - 7}" stroke="#fff" stroke-opacity="{.9 if lit else .45}" stroke-width="1.4"/>')
    a, b = tabs[active]
    ic.add(f'<path d="M{a + 1.5},{y + h}H{b - 1.5}" stroke="#f4f5f7" stroke-width="2.4"/>')


def _thin_x(ic, cx, cy, r):
    d = f"M{cx - r},{cy - r}L{cx + r},{cy + r}M{cx + r},{cy - r}L{cx - r},{cy + r}"
    ic.add(f'<path d="{d}" stroke="#8a1010" stroke-width="3.6" stroke-linecap="round"/>')
    ic.add(f'<path d="{d}" stroke="#f05a4a" stroke-width="1.8" stroke-linecap="round"/>')


def _scroll(ic):
    """History: an old parchment scroll, rolled at the top and bottom, tilted."""
    ic.add('<g transform="rotate(-14 32 32)">')
    body = "M14,14H48V48Q40,52 31,48Q22,44 14,48Z"
    ic.shadow(body, 2.4, 2)
    ic.path(body, ic.lg([(0, "#fffaf0"), (.55, "#f0e2c4"), (1, "#c8a878")], 0, 0, 1, 1), "#4a3418", LW)
    for k in range(5):
        y = 22 + k * 5
        ic.add(f'<path d="M19,{y}H{43 - (k % 2) * 6}" stroke="#a88c60" stroke-width="1.3" stroke-dasharray="4 1.4"/>')
    top = "M10,10Q10,6 14,6H50Q54,6 54,10Q54,14 50,14H14Q10,14 10,10Z"
    ic.path(top, ic.lg([(0, "#fffaf0"), (.5, "#e8d4ac"), (1, "#8a6a3a")]), "#4a3418", LW)
    ic.path(circle(14, 10, 2.6), ic.rg([(0, "#fff8e0"), (1, "#a88450")]), "#4a3418", 1)
    ic.add('<path d="M14,10m-1,0a1,1 0 1 1 1,1" fill="none" stroke="#4a3418" stroke-width=".8"/>')
    bot = "M10,51Q10,47 14,47Q22,44 31,48Q40,52 48,47H50Q54,47 54,51Q54,55 50,55H14Q10,55 10,51Z"
    ic.path(bot, ic.lg([(0, "#f0e2c4"), (.5, "#d4b886"), (1, "#7a5a2a")]), "#4a3418", LW)
    ic.path(circle(50, 51, 2.6), ic.rg([(0, "#fff8e0"), (1, "#a88450")]), "#4a3418", 1)
    ic.add("</g>")


def _key(ic, x, y, s):
    """A blank beige keycap seen from above at an angle (isometric), wider at the base."""
    BR = "#5a4a30"
    a, h = s * .74, s * .52
    T = [(x - a, y), (x, y - a / 2), (x + a, y), (x, y + a / 2)]
    B = [(x - s, y + h), (x, y + h - s / 2), (x + s, y + h), (x, y + h + s / 2)]
    out = _poly([B[0], T[0], T[1], T[2], B[2], B[3]])
    ic.shadow(out, 2, 1.6)
    ic.path(_poly([T[0], T[3], B[3], B[0]]), ic.lg([(0, "#f4f0e0"), (1, "#c4bc9e")], 0, 0, .3, 1), None)
    ic.path(_poly([T[3], T[2], B[2], B[3]]), ic.lg([(0, "#b8ae8c"), (1, "#7e7252")], 0, 0, .3, 1), None)
    ic.path(_poly(T), ic.lg([(0, "#d8d0b0"), (.6, "#fffef8"), (1, "#ece6cc")], 0, 0, 1, 1), BR, .9)
    ic.add(f'<path d="M{T[3][0]:.2f},{T[3][1]:.2f}L{B[3][0]:.2f},{B[3][1]:.2f}" stroke="#fff" stroke-opacity=".5" stroke-width="1"/>')
    ic.path(out, "none", BR, LW)


def _iso_cube(ic, x, y, s, cols):
    """A small glossy cube in isometric view, top vertex at (x, y)."""
    k = s * .87
    top = _poly([(x, y), (x + k, y + s / 2), (x, y + s), (x - k, y + s / 2)])
    left = _poly([(x - k, y + s / 2), (x, y + s), (x, y + 2 * s), (x - k, y + 1.5 * s)])
    right = _poly([(x + k, y + s / 2), (x, y + s), (x, y + 2 * s), (x + k, y + 1.5 * s)])
    ic.shadow(_poly([(x, y), (x + k, y + s / 2), (x + k, y + 1.5 * s), (x, y + 2 * s), (x - k, y + 1.5 * s), (x - k, y + s / 2)]), 2, 1.6)
    ic.path(top, ic.lg([(0, "#ffffff"), (.4, cols[0]), (1, cols[1])], 0, 0, 1, 1), INK, 1.1)
    ic.path(left, ic.lg([(0, cols[1]), (1, cols[2])], 0, 0, 0, 1), INK, 1.1)
    ic.path(right, ic.lg([(0, cols[2]), (1, cols[3])], 0, 0, 0, 1), INK, 1.1)


# ------------------------------------------------------------------ bookmarks
def _ribbon(ic):
    """KDE Classic's bookmark: a grey metal strip lying diagonally, a V cut in its upper end, hatched
    in the middle."""
    ic.add('<g transform="translate(31,31) rotate(45)">')
    d = "M-36,-9H30V9H-36L-28,0Z"
    ic.shadow(d, 2.6, 2.2)
    _mpath(ic, d, ic.lg([(0, "#f4f5f7"), (.3, "#c3c7cd"), (.7, "#8a9098"), (1, "#3c4148")], 0, 0, 0, 1), LW * 1.2)
    ic.add('<path d="M-20,-9V9" stroke="#3c4148" stroke-width="1.2"/><path d="M-18.8,-8V8" stroke="#fff" stroke-opacity=".6" stroke-width="1"/>')
    for k in range(5):
        x = -10 + k * 6
        ic.add(f'<path d="M{x},4L{x + 6},-4" stroke="#5c6168" stroke-width="1.6" stroke-linecap="round"/>'
               f'<path d="M{x + .8},5L{x + 6.8},-3" stroke="#fff" stroke-opacity=".7" stroke-width="1" stroke-linecap="round"/>')
    ic.add('<path d="M-31,-7H28" stroke="#fff" stroke-opacity=".8" stroke-width="1.2"/>')
    ic.add("</g>")


def bookmarks(ic):
    _ribbon(ic)


def bookmark_new(ic):
    _ribbon(ic)
    _new_badge(ic, 46, 46, 15)


# ------------------------------------------------------------------ development
def code_class(ic):
    """New class: three blue building blocks, one in cyan, and the 'new' sparkle."""
    BLUE = ("#8ac8ff", "#2a7ae8", "#0a4ac0", "#062a78")
    CYAN = ("#c8fcff", "#40d8f0", "#10a0c0", "#06607a")
    _iso_cube(ic, 20, 3, 12, BLUE)
    _iso_cube(ic, 42, 9, 11, CYAN)
    _iso_cube(ic, 19, 29, 12, BLUE)
    _sparkle(ic, 45, 45, 15)


def _screwdriver(ic, t):
    """The red-handled flathead screwdriver, drawn upright (blade up, handle down) and placed by `t`."""
    shaft = "M-2.2,-24H2.2V4H-2.2Z"
    tip = "M-2.2,-24L-2.9,-28L-1,-36H1L2.9,-28L2.2,-24Z"      # flat blade: flares a little, then narrows to the edge
    handle = "M-5.6,8Q-6.4,6 -4.4,4H4.4Q6.4,6 5.6,8L6.4,26Q6.4,31 0,31Q-6.4,31 -6.4,26Z"
    ic.shadow(shaft + tip + handle, 2.4, 2, transform=t)
    ic.add(f'<g transform="{t}">')
    steel = ic.lg([(0, "#5c6168"), (.4, "#ffffff"), (1, "#7b818a")], 0, 0, 1, 0)
    ic.path(shaft, steel, INK, 1.1)
    _mpath(ic, tip, steel, 1.1)
    ic.add('<path d="M-2.9,-28H2.9M0,-28.5V-35.4" stroke="#4c5158" stroke-opacity=".5" stroke-width=".7"/>')   # ground faces of the blade
    ic.path(handle, ic.lg([(0, "#7a0804"), (.35, "#ff6a4a"), (.6, "#e0200a"), (1, "#6a0402")], 0, 0, 1, 0), INK, LW * 1.1)
    for x in (-3, 0, 3):
        ic.add(f'<path d="M{x},10V27" stroke="#5a0402" stroke-opacity=".5" stroke-width="1"/>')
    ic.add('<path d="M-3.8,9V26" stroke="#fff" stroke-opacity=".55" stroke-width="1.2" stroke-linecap="round"/>')
    ic.path("M-4.4,2H4.4V6H-4.4Z", ic.lg([(0, "#8a9098"), (.4, "#ffffff"), (1, "#5c6168")], 0, 0, 1, 0), INK, 1)
    ic.add("</g>")


def _blue_spanner(ic, t):
    """The pale blue open-ended spanner from Utilities, drawn handle-left / jaw-right and placed by `t`."""
    blue = ("#d8f8ff", "#7ad0dc", "#2a8aa0", "#0e4a58")
    sp = ("M0,-3.6H36L38,-7.4A9.4,9.4 0 0 1 52.6,-5.2L46.4,-3.2V3.2L52.6,5.2A9.4,9.4 0 0 1 38,7.4L36,3.6H0"
          "A3.6,3.6 0 0 1 0,-3.6Z")
    ic.shadow(sp, 2.4, 2, transform=t)
    ic.add(f'<g transform="{t}">')
    ic.path(sp, ic.lg([(0, blue[0]), (.35, blue[1]), (.75, blue[2]), (1, blue[3])], 0, 0, 0, 1), INK, LW * 1.2)
    ic.add('<path d="M1,-2H35" stroke="#fff" stroke-opacity=".75" stroke-width="1.2" stroke-linecap="round"/>')
    ic.add("</g>")


CONFIGURE_STYLE = "upright"      # "diagonal" (original), "upright", "upright-spanner", "crossed"


def configure(ic, style=None):
    """Configure: a steel gear with the red-handled flathead screwdriver (and in some styles the blue spanner)."""
    from settings import _gear
    style = style or CONFIGURE_STYLE
    g = ("#ffffff", "#b4b9c0", "#5c6168")
    if style == "diagonal":
        _gear(ic, 29, 29, 24, colours=g)
        _screwdriver(ic, "translate(34,34) rotate(45)")
    elif style == "upright":
        _gear(ic, 28, 32, 27, colours=g)
        _screwdriver(ic, "translate(47,33) scale(.92)")
    elif style == "upright-spanner":
        _gear(ic, 22, 30, 21, colours=g)
        _blue_spanner(ic, "translate(41,62) rotate(-90) scale(.98)")
        _screwdriver(ic, "translate(55,33) scale(.9)")
    elif style == "crossed":
        _gear(ic, 23, 23, 20, colours=g)
        _blue_spanner(ic, "translate(18,60) rotate(-48) scale(.92)")
        _screwdriver(ic, "translate(42,38) rotate(-40) scale(.86)")


def configure_shortcuts(ic):
    """Configure shortcuts: a small pile of large blank keycaps, as KDE 3's key bindings icon."""
    for x, y in ((22, 10), (43, 13), (15, 28), (35, 30), (48, 40)):
        _key(ic, x, y + 2, 14)


# ------------------------------------------------------------------ dialogs
def dialog_warning(ic):
    _warn_tri(ic)


def data_warning(ic):
    """Data warning: the warning sign in front of a sheet of data."""
    ic.shadow("M4,4H40V40H4Z", 2.2, 1.8)
    ic.path("M4,4H40V40H4Z", ic.lg([(0, "#ffffff"), (1, "#e4e6e9")]), INK, LW)
    ic.path("M4,4H40V11H4Z", ic.lg([(0, "#d9dce0"), (1, "#9aa0a8")]), INK, 1)
    for k in range(1, 4):
        ic.add(f'<path d="M4,{11 + k * 7}H40M{4 + k * 9},11V40" stroke="#9aa0a8" stroke-width="1"/>')
    _warn_tri(ic, 18, 16, 62, 60)


def emblem_warning(ic):
    """Warning emblem: the warning sign as a glossy badge with rounded corners, so it reads at emblem size."""
    d = "M28,6.4Q32,0 36,6.4L61,50Q64,57 56,57H8Q0,57 3,50Z"
    ic.shadow(d, 2.2, 1.8)
    ic.path(d, ic.lg([(0, "#fffbd0"), (.3, "#ffe020"), (.75, "#f0b000"), (1, "#a87000")], 0, 0, .3, 1), INK, LW * 1.6)
    ic.add('<path d="M10,49L30,12" stroke="#fff" stroke-opacity=".7" stroke-width="2" stroke-linecap="round"/>')
    ic.path("M28,20Q32,17 36,20L34,40H30Z", INK, None)
    ic.path(circle(32, 47.5, 3.6), INK, None)


def dialog_error(ic):
    """Error: KDE Classic's red disc with a thick white cross."""
    ic.shadow(circle(32, 32, 28), 2.8, 2.4)
    ic.path(circle(32, 32, 28), ic.rg([(0, "#ffb0a0"), (.35, "#ff2a1a"), (.8, "#c80a04"), (1, "#7a0402")], .38, .32, .8), INK, LW * 1.2)
    ic.add('<path d="M12,22C15,11 28,5 40,8C28,8 18,13 12,22Z" fill="#fff" fill-opacity=".45"/>')
    d = "M20,15L32,27L44,15L49,20L37,32L49,44L44,49L32,37L20,49L15,44L27,32L15,20Z"
    ic.path(d, "#8a0a04", None, ' transform="translate(1.2,1.2)" fill-opacity=".6"')
    ic.path(d, ic.lg([(0, "#ffffff"), (1, "#f0e4e4")]), None)


def dialog_cancel(ic):
    """Cancel: KDE Classic's red cross in two brush strokes."""
    s1 = "M6,9Q9,4 13,7Q34,26 57,52Q59,57 54,58Q31,36 8,14Q4,12 6,9Z"
    s2 = "M53,5Q58,5 58,9Q35,32 15,57Q11,61 7,57Q7,54 10,50Q30,27 53,5Z"
    for d in (s2, s1):
        ic.shadow(d, 2.2, 1.8)
        ic.path(d, ic.lg([(0, "#ff7a6a"), (.4, "#f01a0a"), (1, "#8a0402")], 0, 0, .3, 1), "#4a0402", 1.2)
    ic.add('<path d="M9,9Q30,27 54,54M52,8Q31,29 11,54" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width="1.4" stroke-linecap="round"/>')


def dialog_close(ic):
    """Close: a grey glass button with a white cross."""
    o = rrect(5, 5, 54, 54, 10)
    ic.shadow(o, 2.6, 2.2)
    ic.path(o, ic.lg([(0, "#c3c7cd"), (.5, "#6c727a"), (1, "#2c3036")], 0, 0, 1, 1), INK, LW * 1.3)
    ic.path(rrect(10, 10, 44, 44, 7), ic.lg([(0, "#9aa0a8"), (.5, "#7b818a"), (1, "#b4b9c0")], 0, 0, 1, 1), "#3c4148", 1)
    ic.add('<path d="M13,30V16Q13,13 16,13H48" fill="none" stroke="#fff" stroke-opacity=".55" stroke-width="1.6" stroke-linecap="round"/>')
    d = "M22,18L32,28L42,18L46,22L36,32L46,42L42,46L32,36L22,46L18,42L28,32L18,22Z"
    ic.path(d, "#2c3036", None, ' transform="translate(1.4,1.4)" fill-opacity=".6"')
    ic.path(d, ic.lg([(0, "#ffffff"), (1, "#d9dce0")]), "#4c5158", .8)


# ------------------------------------------------------------------ documents and history
def document_open_recent(ic):
    _scroll(ic)


def edit_clear_history(ic):
    """Clear history: the history scroll with a red cross."""
    _scroll(ic)
    from dolphin import _red_x
    _red_x(ic, 47, 47, 10)


def document_properties(ic):
    """Properties: a ruled form with a header row, and the orange pencil."""
    ic.shadow("M5,4H45V60H5Z", 2.4, 2)
    ic.path("M5,4H45V60H5Z", ic.lg([(0, "#ffffff"), (.6, "#fcfaf6"), (1, "#e4dccc")], 0, 0, 1, 1), INK, LW)
    ic.path("M7,6H43V13H7Z", ic.lg([(0, "#e4e6e9"), (1, "#a8adb4")]), None)
    for k in range(7):
        ic.add(f'<path d="M7,{13 + k * 6.6}H43" stroke="#b4b9c0" stroke-width="1"/>')
    ic.add('<path d="M18,6V58M31,6V58" stroke="#b4b9c0" stroke-width="1"/>')
    _pencil(ic, "translate(49,6) rotate(38) translate(-6,0)")


def view_preview(ic):
    """Preview: a page with its picture thumbnail held up in front."""
    from filetypes import page
    from gen import e_picture
    ic.add('<g transform="translate(-8,-4)">')
    page(ic)
    ic.add("</g>")
    ic.add('<g transform="translate(16,-12) scale(1.3)">')
    e_picture(ic)
    ic.add("</g>")


# ------------------------------------------------------------------ editing
def emblem_readonly(ic):
    """Read-only: the pencil struck out with a red cross."""
    _pencil(ic, "translate(48,4) rotate(40) translate(-6,0) scale(1.1)")
    from dolphin import _red_x
    _red_x(ic, 32, 32, 18)


def format_text_bold(ic):
    """Bold: a heavy black serif B."""
    outer = ("M8,7H34C47,7 53,12.5 53,20.5C53,26.5 49,30 43,31.6C51,33 56,38 56,45.2C56,52.6 49.6,57 37.6,57H8V52.6H14V11.4H8Z")
    holes = ("M26,11.4V29.6H32.4C38.4,29.6 40.8,26 40.8,20.6C40.8,14.6 37.6,11.4 32,11.4Z"
             "M26,33.8V52.6H34C40.4,52.6 43.4,49 43.4,43.4C43.4,37.4 40,33.8 33.4,33.8Z")
    ic.shadow(outer, 2.4, 2)
    ic.add(f'<path d="{outer}{holes}" fill="{ic.lg([(0, "#6c727a"), (.35, "#1e2024"), (1, "#000000")], 0, 0, .4, 1)}" fill-rule="evenodd" stroke="{INK}" stroke-width="1"/>')
    ic.add('<path d="M17,13V50" stroke="#fff" stroke-opacity=".35" stroke-width="1.4"/>')


def format_text_superscript(ic):
    """Superscript: a black x with a small raised 2."""
    x = "M6,26H20V29.5H17.5L24,38.5L30.5,29.5H28V26H40V29.5H36L27,42L37,55H40V58.6H26V55H28.4L22,46L15.4,55H18V58.6H5V55H9L19,42L10,29.5H6Z"
    ic.shadow(x, 2.2, 1.8)
    ic.path(x, ic.lg([(0, "#4c5158"), (1, "#000000")]), INK, .8)
    two = "M44,14Q44,6 51,6Q58,6 58,12.4Q58,17.6 49.6,23H58.6V27H43.4V24Q54,16.4 54,12.6Q54,9.6 51,9.6Q48,9.6 48,14Z"
    ic.shadow(two, 1.8, 1.5)
    ic.path(two, ic.lg([(0, "#3a6ad8"), (1, "#0a1a80")]), INK, .8)


# ------------------------------------------------------------------ help
def help_about(ic):
    """About: the blue information sphere in front of a small application window."""
    w = "M4,6H44V44H4Z"
    ic.shadow(w, 2.4, 2)
    ic.path(w, ic.lg([(0, "#fffef4"), (1, "#fff4c4")], 0, 0, 1, 1), INK, LW)
    ic.path("M4,6H44V14H4Z", ic.lg([(0, "#e4e6e9"), (1, "#8a9098")]), INK, LW)
    for k in range(3):
        ic.add(f'<path d="M9,{20 + k * 5}H{30 - k * 4}" stroke="#a8adb4" stroke-width="1.6"/>')
    cx, cy, r = 40, 40, 20
    ic.shadow(circle(cx, cy, r), 2.6, 2.2)
    ic.path(circle(cx, cy, r), ic.rg([(0, "#8ab8f0"), (.45, "#2a5ab0"), (1, "#081c50")], .35, .28, .85), INK, LW)
    ic.add(f'<path d="M{cx - 14},{cy - 6}C{cx - 12},{cy - 16} {cx},{cy - 21} {cx + 9},{cy - 17}C{cx + 2},{cy - 18} {cx - 8},{cy - 15} {cx - 14},{cy - 6}Z" fill="#fff" fill-opacity=".5"/>')
    ic.path(circle(cx, cy - 10, 3.3), "#ffffff", None)
    ic.path(f"M{cx - 5},{cy - 4}H{cx + 2.6}V{cy + 9}H{cx + 5.2}V{cy + 12.6}H{cx - 5.4}V{cy + 9}H{cx - 2.6}V{cy - .6}H{cx - 5}Z", "#ffffff", None)


def help_contents(ic):
    """Contents: KDE Classic's teal cloth handbook, redrawn over lines traced from the original bitmap.
    The left half stands upright and side-on; on the right the page block and back board lie flat, facing
    us, with the top page lifting up from the spine and curling at its foot."""
    teal = ic.lg([(0, "#6ad0d0"), (.45, "#1a8a90"), (1, "#0a3a40")], 0, 0, 1, 1)
    lboard = "M2,1.6L25,20.4V61.6L2,44Z"
    rboard = "M25,17H59.6Q62,17 62,19.4V57.4Q62,60 59.6,60H25Z"
    ic.shadow(lboard + rboard, 2.6, 2.2)
    ic.path(rboard, teal, INK, LW * 1.2)
    ic.path(lboard, teal, INK, LW * 1.2)
    ic.add('<path d="M3.8,5.6V42.6L24,58" fill="none" stroke="#b8f0f0" stroke-opacity=".75" stroke-width="1.1"/>')
    # right: the flat page block, its edges stacked down the right-hand side
    block = "M25,18.4H57.6V56H25Z"
    ic.path(block, ic.lg([(0, "#fbf4e4"), (.6, "#eadcbc"), (1, "#c8b48a")], 0, 0, 1, 1), INK, LW)
    for x in (50.6, 53, 55.4):
        ic.add(f'<path d="M{x},19.6V{50 + (x - 50) * .6:.2f}Q{x - 1},{53.4 + (x - 50) * .3:.2f} {x - 4},{54.6}" fill="none" stroke="#a8946a" stroke-width=".8"/>')
    # the top page lifting from the spine, its foot curling down into the block
    page = "M25,20.4L47.6,7.4V41Q41,42.6 36.4,47Q31,52 25.6,55.6Z"
    ic.path(page, ic.lg([(0, "#ffffff"), (.5, "#fbf6ea"), (1, "#e6d6b0")], 0, 0, .3, 1), INK, LW)
    for k in range(3):
        ic.add(f'<path d="M{47.4 - k * 1.2:.2f},{43.2 + k * 2.2:.2f}Q{40 - k},{45 + k * 2.4:.2f} {35.4 - k * 1.4:.2f},{50.6 + k * 1.8:.2f}" fill="none" stroke="#a8946a" stroke-width=".8"/>')
    # left: the upright page, white above and cream below, shaded into the gutter
    left = "M7.6,4.6L25,20.4V55.2L7.6,40.6Z"
    ic.path(left, ic.lg([(0, "#ffffff"), (.55, "#faf4e4"), (1, "#dcc8a0")], 0, 0, .3, 1), INK, LW)
    ic.add('<path d="M22.8,20.6V53.6" stroke="#c8b48a" stroke-width="2.6" stroke-opacity=".7"/>')
    ic.add('<path d="M25,20.4V56" stroke="#6a5a3a" stroke-width="1.4"/>')
    ic.add('<path d="M9.6,8.6V39.6" stroke="#fff" stroke-width="1.2"/>')


# ------------------------------------------------------------------ playback
def media_playback_pause(ic):
    """Pause: two rounded grey bars, glossy down the middle."""
    for x in (7, 37):
        o = rrect(x, 6, 20, 52, 5)
        ic.shadow(o, 2.4, 2)
        ic.path(o, ic.lg([(0, "#2c3036"), (.5, "#6c727a"), (1, "#141414")], 0, 0, 1, 0), INK, LW)
        ic.path(rrect(x + 4.5, 11, 11, 42, 4), ic.lg([(0, "#7b818a"), (.4, "#ffffff"), (.65, "#c3c7cd"), (1, "#5c6168")], 0, 0, 1, 0), "#2c3036", .8)


def media_playback_start(ic):
    """Play: a bevelled grey triangle pointing right."""
    o = "M12,5L59,32L12,59Z"
    ic.shadow(o, 2.6, 2.2)
    _mpath(ic, o, ic.lg([(0, "#8a9098"), (.5, "#4c5158"), (1, "#141414")], 0, 0, 1, 1), LW * 1.2)
    ic.path("M17.5,14.5L48.5,32L17.5,49.5Z", ic.lg([(0, "#ffffff"), (.45, "#c3c7cd"), (1, "#6c727a")], 0, 0, .6, 1), "#2c3036", .9)


# ------------------------------------------------------------------ menus and windows
def menu_edit(ic):
    """Menu editor: a K menu list with highlighted entries, a submenu beside it, and the pencil."""
    m = "M12,4H40V60H12Z"
    ic.shadow(m, 2.4, 2)
    ic.path(m, ic.lg([(0, "#e4e6e9"), (1, "#a8adb4")], 0, 0, 1, 0), INK, LW)
    for k in range(8):
        y = 7 + k * 6.6
        hi = k in (2, 5)
        ic.path(f"M15,{y}H37V{y + 4.6}H15Z", ic.lg([(0, "#8af0f0"), (1, "#10a0a8")]) if hi else ic.lg([(0, "#ffffff"), (1, "#c3c7cd")]), "#4c5158", .7)
    s = "M40,14H58V40H40Z"
    ic.shadow(s, 2.2, 1.8)
    ic.path(s, ic.lg([(0, "#e4e6e9"), (1, "#a8adb4")], 0, 0, 1, 0), INK, LW)
    for k in range(3):
        y = 17 + k * 7.4
        ic.path(f"M43,{y}H55V{y + 5}H43Z", ic.lg([(0, "#8af0f0"), (1, "#10a0a8")]) if k == 1 else ic.lg([(0, "#ffffff"), (1, "#c3c7cd")]), "#4c5158", .7)
    _pencil(ic, "translate(28,30) rotate(40) scale(.78) translate(-6,0)")


def window_new(ic):
    """New window: a window with KDE Classic's violet title bar and a green plus badge."""
    w = "M4,6H56V54H4Z"
    ic.shadow(w, 2.6, 2.2)
    ic.path(w, ic.lg([(0, "#ffffff"), (1, "#e4e6e9")], 0, 0, 1, 1), INK, LW * 1.3)
    ic.path("M4,6H56V16H4Z", ic.lg([(0, "#c8a8f0"), (.5, "#8040c0"), (1, "#4a1a80")]), INK, LW * 1.3)
    ic.add('<path d="M6,8.5H54" stroke="#fff" stroke-opacity=".5" stroke-width="1.2"/>')
    _new_badge(ic, 44, 44, 17)


# ------------------------------------------------------------------ tabs
def tab_new(ic):
    _tabs(ic)
    _new_badge(ic, 44, 17, 14)


def tab_close(ic):
    _tabs(ic)
    _thin_x(ic, 18, 16, 10)


def tab_close_other(ic):
    _tabs(ic, active=0)
    _thin_x(ic, 44, 16, 10)


def tab_detach(ic):
    """Detach tab: the tab strip at the top, its page pulled out below as a window of its own."""
    for a, b, lit in ((30, 58, False), (4, 32, True)):
        d = f"M{a},18L{a + 6},5H{b - 6}L{b},18Z"
        ic.shadow(d, 1.8, 1.4)
        _mpath(ic, d, ic.lg([(0, "#f4f5f7"), (1, "#c3c7cd")] if lit else [(0, "#a8adb4"), (1, "#5c6168")]), 1.4)
    ic.add('<path d="M2,18H62" stroke="#9aa0a8" stroke-width="2"/>')
    w = "M6,26H62V62H6Z"
    ic.shadow(w, 2.4, 2)
    ic.path(w, ic.lg([(0, "#ffffff"), (1, "#e4e6e9")], 0, 0, 1, 1), INK, LW * 1.2)
    ic.path("M6,26H62V34H6Z", ic.lg([(0, "#8ab0ff"), (.5, "#1a3ae0"), (1, "#0a1a80")]), INK, LW * 1.2)
    ic.add('<path d="M10,30H40" stroke="#fff" stroke-opacity=".8" stroke-width="1.6"/>')


# ------------------------------------------------------------------ terminal and calendar
def terminal_monitor(ic):
    """Konsole's grey monitor with a shell prompt (no seashell)."""
    mon = rrect(3, 4, 50, 44, 3)
    ic.shadow(mon, 2.6, 2.2)
    ic.path(mon, ic.lg([(0, "#ffffff"), (.5, "#c3c7cd"), (1, "#7b818a")], 0, 0, 1, 1), INK, LW)
    ic.path("M8,9H48V40H8Z", ic.lg([(0, "#3a3f46"), (1, "#060708")], 0, 0, 1, 1), INK, 1)
    ic.add('<path d="M12,15L16,18L12,21M18,21.5H24" fill="none" stroke="#e4e6e9" stroke-width="1.8" stroke-linecap="square"/>')
    ic.path("M8,43H14V45H8Z", "#4fae5a", None)


def utilities_terminal(ic):
    """Terminal: KDE 3's Konsole - a grey monitor with a shell prompt, and a seashell in front."""
    terminal_monitor(ic)
    # scallop shell: ribs fanning out from the hinge at the bottom
    hx, hy, R = 44, 61, 20
    pts = []
    for k in range(15):
        a = math.radians(-158 + 136 * k / 14)
        rr = R if k % 2 == 0 else R - 2.2
        pts.append((hx + rr * .95 * math.cos(a), hy + rr * 1.2 * math.sin(a)))
    d = f"M{hx - 4},{hy}" + "".join(f"L{x:.2f},{y:.2f}" for x, y in pts) + f"L{hx + 4},{hy}Z"
    ic.shadow(d, 2.2, 1.8)
    ic.path(d, ic.rg([(0, "#fffaf0"), (.55, "#f4d8a8"), (1, "#c88a4a")], .45, .9, .9), "#5a3418", LW)
    for k in range(0, 15, 2):
        x, y = pts[k]
        ic.add(f'<path d="M{hx},{hy - 1}L{x * .85 + hx * .15:.2f},{y * .85 + hy * .15:.2f}" stroke="#a86a32" stroke-width="1"/>')
    ic.path(f"M{hx - 6},{hy - 1}H{hx + 6}L{hx + 4},{hy + 2.4}H{hx - 4}Z", ic.lg([(0, "#f4d8a8"), (1, "#a86a32")]), "#5a3418", .9)


def view_calendar(ic):
    """Calendar: a day sheet with a big red date, and an hourglass."""
    p = "M3,14H38V58H3Z"
    ic.shadow(p, 2.4, 2)
    ic.path(p, ic.lg([(0, "#ffffff"), (1, "#e4e6e9")], 0, 0, 1, 1), INK, LW)
    ic.path("M3,14H38V21H3Z", ic.lg([(0, "#ff8a7a"), (1, "#c80a04")]), INK, LW)
    for x in (10, 20, 30):
        ic.path(rrect(x - 1.4, 10, 2.8, 8, 1.4), ic.lg([(0, "#ffffff"), (1, "#7b818a")], 0, 0, 1, 0), INK, .8)
    three = "M12,31Q13,25 20.5,25Q28,25 28,31.6Q28,36.4 23.4,38Q29,39.6 29,45.6Q29,53 20.4,53Q13,53 11.4,46.6"
    ic.add(f'<path d="{three}" fill="none" stroke="#5a0402" stroke-width="6.4" stroke-linecap="round" stroke-linejoin="round"/>')
    ic.add(f'<path d="{three}" fill="none" stroke="#f01a0a" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>')
    ic.add('<path d="M18,38H23" stroke="#5a0402" stroke-width="1"/>')
    # hourglass
    wood = ic.lg([(0, "#ffd8a0"), (.5, "#b86a28"), (1, "#5a2806")])
    glass = "M39,9H59Q59,22 50,32Q59,42 59,55H39Q39,42 48,32Q39,22 39,9Z"
    ic.shadow(glass, 2.2, 1.8)
    ic.path(glass, ic.lg([(0, "#ffffff"), (1, "#c8dce8")], 0, 0, 1, 0), INK, 1.1)
    ic.path("M40.6,54Q41,45 49,41Q57,45 57.4,54Z", ic.lg([(0, "#fff8a0"), (1, "#d8a810")]), None)
    ic.path("M43,15H55Q53,22 49,25Q45,22 43,15Z", ic.lg([(0, "#fff8a0"), (1, "#d8a810")]), None)
    ic.add('<path d="M49,26V41" stroke="#d8a810" stroke-width="1.2"/>')
    for x in (37.5, 60.5):
        ic.path(rrect(x - 1.5, 7, 3, 50, 1.5), wood, INK, .9)
    for y in (3, 55):
        ic.path(rrect(34, y, 30, 5, 2), wood, INK, 1.1)


# ------------------------------------------------------------------ registry
UI = {
    "actions": {
        "bookmarks": bookmarks, "bookmark-new": bookmark_new, "code-class": code_class, "configure": configure,
        "configure-shortcuts": configure_shortcuts, "dialog-cancel": dialog_cancel, "dialog-close": dialog_close,
        "document-open-recent": document_open_recent, "document-properties": document_properties,
        "edit-clear-history": edit_clear_history, "format-text-bold": format_text_bold,
        "format-text-superscript": format_text_superscript, "help-about": help_about, "help-contents": help_contents,
        "media-playback-pause": media_playback_pause, "media-playback-start": media_playback_start,
        "tab-new": tab_new, "tab-close": tab_close, "tab-close-other": tab_close_other, "tab-detach": tab_detach,
        "view-calendar": view_calendar, "view-preview": view_preview, "window-new": window_new,
    },
    "status": {"dialog-warning": dialog_warning, "data-warning": data_warning, "dialog-error": dialog_error},
    "emblems": {"emblem-readonly": emblem_readonly, "emblem-warning": emblem_warning},
    "apps": {"utilities-terminal": utilities_terminal, "preferences-desktop-menu-edit": menu_edit},
}
UI_ALIASES = {
    "actions": {"bookmarks-symbolic": "bookmarks", "bookmark-new-symbolic": "bookmark-new", "configure-symbolic": "configure",
                "dialog-cancel-symbolic": "dialog-cancel", "dialog-close-symbolic": "dialog-close",
                "document-open-recent-symbolic": "document-open-recent", "document-properties-symbolic": "document-properties",
                "help-about-symbolic": "help-about", "help-contents-symbolic": "help-contents",
                "media-playback-pause-symbolic": "media-playback-pause", "media-playback-start-symbolic": "media-playback-start",
                "tab-new-symbolic": "tab-new", "tab-close-symbolic": "tab-close", "window-new-symbolic": "window-new",
                "view-restore": "window-restore", "view-restore-symbolic": "window-restore",
                "dialog-scripts": "../mimetypes/application-x-shellscript", "help-contents-alternative": "help-contents"},
    "status": {"dialog-warning-symbolic": "dialog-warning", "dialog-error-symbolic": "dialog-error", "error": "dialog-error",
               "error-symbolic": "dialog-error", "data-error": "dialog-error", "security-low": "../emblems/object-unlocked",
               "data-warning-symbolic": "data-warning"},
    "emblems": {"emblem-readonly-symbolic": "emblem-readonly", "emblem-warning-symbolic": "emblem-warning"},
    "apps": {"utilities-terminal-symbolic": "utilities-terminal", "konsole": "utilities-terminal"},
}


def write(out):
    n = 0
    for ctx, icons in UI.items():
        d = f"{out}/scalable/{ctx}"
        os.makedirs(d, exist_ok=True)
        for name, fn in icons.items():
            open(f"{d}/{name}.svg", "w").write(_ic(fn)().svg(64))
            n += 1
    for ctx, al in UI_ALIASES.items():
        d = f"{out}/scalable/{ctx}"
        for a, t in al.items():
            if os.path.exists(os.path.normpath(f"{d}/{t}.svg")) and not os.path.lexists(f"{d}/{a}.svg"):
                os.symlink(f"{t}.svg", f"{d}/{a}.svg")
    return n
