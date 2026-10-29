"""KDE Classic Vector: desktop shell icons that still came from the KDE Classic bitmaps (alignment, text and
list formatting, layers, mail, templates, wizard, Spectacle, desktop sharing ...), redrawn as vectors,
plus aliases where the meaning matches an icon already drawn.

Arrows follow STYLE.md (teal); the 'new' sparkle, pencil and badges are shared with the other sets.
"""
import math, os
from gen import Icon, INK, LW, circle, rrect
from actions import _mpath
from uitrace import _sparkle, _new_badge, _pencil, _iso_cube
from settingstrace import _teal, _arrow_pts, _double_arrow, _page, _lines, _badge, _no, _poly


def _ic(fn):
    def f():
        ic = Icon()
        fn(ic)
        return ic
    return f


ORANGE = [(0, "#ffd8a8"), (.5, "#f8a050"), (1, "#a85a14")]
LILAC = [(0, "#ffffff"), (.45, "#c8c8f8"), (1, "#6a6ac0")]


def _guide(ic, d):
    ic.add(f'<path d="{d}" stroke="{INK}" stroke-width="3.4"/><path d="{d}" stroke="#ffe010" stroke-width="1.8" stroke-dasharray="4 4"/>')


def _objects(ic, rect, circ):
    x, y, w, h = rect
    d = f"M{x},{y}H{x + w}V{y + h}H{x}Z"
    ic.shadow(d, 2, 1.7)
    ic.path(d, ic.lg(ORANGE, 0, 0, 1, 1), INK, LW)
    cx, cy, r = circ
    ic.shadow(circle(cx, cy, r), 2, 1.7)
    ic.path(circle(cx, cy, r), ic.rg(LILAC, .4, .35, .8), INK, LW)


def align_left(ic):
    _objects(ic, (10, 5, 26, 24), (24, 45, 14))
    _guide(ic, "M10,2V62")


def align_right(ic):
    _objects(ic, (28, 5, 26, 24), (40, 45, 14))
    _guide(ic, "M54,2V62")


def align_hcenter(ic):
    _objects(ic, (19, 5, 26, 24), (32, 45, 14))
    _guide(ic, "M32,2V62")


def align_top(ic):
    _objects(ic, (5, 10, 24, 26), (45, 24, 14))
    _guide(ic, "M2,10H62")


def align_bottom(ic):
    _objects(ic, (5, 28, 24, 26), (45, 40, 14))
    _guide(ic, "M2,54H62")


def align_vcenter(ic):
    _objects(ic, (5, 19, 24, 26), (45, 32, 14))
    _guide(ic, "M2,32H62")


# ------------------------------------------------------------------ text and lists
def _letter_a(ic, x, y, h, col="#14171c"):
    w = h * .8
    d = f"M{x},{y + h}L{x + w / 2},{y}L{x + w},{y + h}M{x + w * .22},{y + h * .62}H{x + w * .78}"
    ic.add(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{h * .17:.2f}" stroke-linejoin="miter" stroke-linecap="square"/>')


def font_size_more(ic):
    _letter_a(ic, 4, 36, 20)
    _letter_a(ic, 28, 16, 40)
    _teal(ic, _poly(_arrow_pts(10, 28, 30, 10, 2.6, 7, 8)), 1.2)


def font_size_less(ic):
    _letter_a(ic, 2, 16, 40)
    _letter_a(ic, 40, 36, 20)
    _teal(ic, _poly(_arrow_pts(30, 8, 50, 28, 2.6, 7, 8)), 1.2)


def _bars(ic, x0):
    for k in range(3):
        y = 12 + k * 18
        ic.path(rrect(x0, y, 60 - x0, 7, 1.5), ic.lg([(0, "#8a9098"), (1, "#3c4148")]), INK, 1)


def list_ordered(ic):
    _bars(ic, 22)
    digits = ["M6,10L10,7V20", "M5,29Q6,25 9.5,25Q13,25 13,28.6Q13,31 5,38H13.6", "M5,44H13L8.6,49Q13.6,49 13.6,53Q13.6,57 9,57Q6,57 5,55"]
    for d in digits:
        ic.add(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>')
    for y in (19.5, 37.5, 55.5):
        ic.path(circle(17, y, 1.6), INK, None)


def list_unordered(ic):
    _bars(ic, 22)
    for y in (15.5, 33.5, 51.5):
        ic.path(circle(10, y, 5.4), ic.rg([(0, "#e0f0ff"), (.45, "#3a7ae0"), (1, "#0a1a70")], .38, .32, .8), INK, 1.1)


def subscript(ic):
    """Subscript: a black x with a small lowered 2."""
    x = "M6,6H20V9.5H17.5L24,18.5L30.5,9.5H28V6H40V9.5H36L27,22L37,35H40V38.6H26V35H28.4L22,26L15.4,35H18V38.6H5V35H9L19,22L10,9.5H6Z"
    ic.shadow(x, 2.2, 1.8)
    ic.path(x, ic.lg([(0, "#4c5158"), (1, "#000000")]), INK, .8)
    two = "M44,44Q44,36 51,36Q58,36 58,42.4Q58,47.6 49.6,53H58.6V57H43.4V54Q54,46.4 54,42.6Q54,39.6 51,39.6Q48,39.6 48,44Z"
    ic.shadow(two, 1.8, 1.5)
    ic.path(two, ic.lg([(0, "#3a6ad8"), (1, "#0a1a80")]), INK, .8)


def text_frame(ic):
    """Text frame: a serif T inside a dashed frame with corner handles."""
    ic.add(f'<path d="M6,6H58V58H6Z" fill="#fff" fill-opacity=".7" stroke="{INK}" stroke-width="1.4" stroke-dasharray="4 3"/>')
    for x, y in ((6, 6), (58, 6), (6, 58), (58, 58)):
        ic.path(f"M{x - 3},{y - 3}H{x + 3}V{y + 3}H{x - 3}Z", "#2a5ae0", INK, .9)
    t = "M14,14H50V26H46.6Q46,19 40,18.6H36V46Q36,48.6 40,49V52H24V49Q28,48.6 28,46V18.6H24Q18,19 17.4,26H14Z"
    ic.shadow(t, 2, 1.7)
    ic.path(t, ic.lg([(0, "#4c5158"), (1, "#000000")]), INK, .8)


def percent(ic):
    d = ("M18,6A10,12 0 1 0 18.01,6ZM18,12A4,6 0 1 1 17.99,12Z"
         "M46,34A10,12 0 1 0 46.01,34ZM46,40A4,6 0 1 1 45.99,40Z"
         "M44,4H51L20,60H13Z")
    ic.shadow(d, 2.2, 1.8)
    ic.add(f'<path d="{d}" fill="{ic.lg([(0, "#4c5158"), (1, "#000000")])}" fill-rule="evenodd" stroke="{INK}" stroke-width=".8"/>')


def sort_descending(ic):
    """Sort descending: a red Z over a blue A with the arrow pointing up."""
    for d, col in (("M10,10H26L10,30H26", "#e0281a"), ("M10,54L18,34L26,54M13.2,46.4H22.8", "#2a3ae8")):
        ic.add(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>')
        ic.add(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>')
    ic.add(f'<path d="M44,56V12M36,20L44,10L52,20" fill="none" stroke="{INK}" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/>')


# ------------------------------------------------------------------ shapes and layers
def eraser(ic):
    """Eraser: a red rubber in a blue sleeve, lying diagonally."""
    ic.add('<g transform="translate(32,32) rotate(-40)">')
    body = "M-28,-9H24L28,-5V9H-24L-28,5Z"
    ic.shadow(body, 2.4, 2)
    ic.path("M-28,-9H-2V9H-24L-28,5Z", ic.lg([(0, "#ff9a8a"), (.45, "#d8180a"), (1, "#6a0402")], 0, 0, 0, 1), INK, LW)
    ic.path("M-2,-9H24L28,-5V9H-2Z", ic.lg([(0, "#d8d8ff"), (.45, "#6a6af0"), (1, "#20208a")], 0, 0, 0, 1), INK, LW)
    ic.path("M-28,5L-24,9V12H-28Z", "#ffc0c0", None)
    ic.add('<path d="M-25,-6.4H22" stroke="#fff" stroke-opacity=".6" stroke-width="1.4"/>')
    ic.add("</g>")


def polygon(ic):
    """Polygon: a grey five-sided shape with its corner nodes."""
    pts = [(32, 5), (58, 26), (54, 58), (10, 58), (6, 26)]
    d = _poly(pts)
    ic.shadow(d, 2.4, 2)
    ic.path(d, ic.lg([(0, "#ffffff"), (.5, "#c3c7cd"), (1, "#7b818a")], 0, 0, 1, 1), INK, LW * 1.4)
    for x, y in pts:
        ic.path(f"M{x - 3},{y - 3}H{x + 3}V{y + 3}H{x - 3}Z", "#ffffff", INK, 1.1)


def edit_image(ic):
    """Edit image: a picture with the orange pencil working on it."""
    from gen import e_picture
    ic.add('<g transform="translate(-4,-36) scale(1.55)">')
    e_picture(ic)
    ic.add("</g>")
    _pencil(ic, "translate(52,10) rotate(40) translate(-6,0) scale(.9)")


def ungroup(ic):
    """Ungroup: a square and a circle pulled apart, each with its own selection handles."""
    sq = "M6,22H32V48H6Z"
    ic.shadow(sq, 2, 1.7)
    ic.path(sq, ic.lg([(0, "#ffffff"), (1, "#c3c7cd")], 0, 0, 1, 1), INK, LW)
    ic.shadow(circle(44, 20, 13), 2, 1.7)
    ic.path(circle(44, 20, 13), ic.rg([(0, "#ffffff"), (1, "#c3c7cd")], .4, .35, .8), INK, LW)
    for x, y in ((6, 22), (32, 22), (6, 48), (32, 48), (31, 7), (57, 7), (31, 33), (57, 33)):
        ic.path(f"M{x - 2.6},{y - 2.6}H{x + 2.6}V{y + 2.6}H{x - 2.6}Z", "#2a5ae0", INK, .8)


def shear(ic):
    """Shear: an olive slab slanted over, with blue arrows pushing its top and bottom opposite ways."""
    d = "M20,22H58L44,42H6Z"
    ic.shadow(d, 2.2, 1.8)
    ic.path(d, ic.lg([(0, "#d8d880"), (.5, "#8a8a20"), (1, "#3a3a04")], 0, 0, 1, 1), INK, LW)
    _teal(ic, _poly(_arrow_pts(34, 12, 62, 12, 2.4, 6.4, 8)), 1.1)
    _teal(ic, _poly(_arrow_pts(30, 52, 2, 52, 2.4, 6.4, 8)), 1.1)


def _layers(ic):
    for k in (2, 1, 0):
        y = 14 + k * 12
        d = f"M16,{y}H58L48,{y + 12}H6Z"
        ic.shadow(d, 2, 1.6)
        ic.path(d, ic.lg([(0, "#c8d0ff"), (.5, "#3a4ae0"), (1, "#0a1a80")] if k == 0 else [(0, "#e4e8ff"), (1, "#8a90d0")], 0, 0, 1, 1), INK, LW)


def layer_new(ic):
    _layers(ic)
    _new_badge(ic, 48, 48, 14)


def layer_delete(ic):
    _layers(ic)
    from dolphin import _red_x
    _red_x(ic, 47, 47, 10)


def flip_horizontal(ic):
    """Flip horizontally: a solid teal triangle left of the mirror line and its outline reflected right."""
    _teal(ic, "M27,10L6,32L27,54Z")
    ic.add(f'<path d="M32,4V60" stroke="{INK}" stroke-width="1.6" stroke-dasharray="4 2.4"/>')
    ic.path("M37,10L58,32L37,54Z", "#ffffff", INK, LW)


def enum(ic):
    """New enumeration: a small grey block and the 'new' sparkle."""
    _iso_cube(ic, 26, 6, 15, ("#f4f5f7", "#a8a8c0", "#6a6a88", "#36364a"))
    _sparkle(ic, 46, 46, 15)


# ------------------------------------------------------------------ documents and mail
def appointment_new(ic):
    """New appointment: a calendar page with its blue heading and a green plus badge."""
    p = "M5,6H55V58H5Z"
    ic.shadow(p, 2.4, 2)
    ic.path(p, ic.lg([(0, "#ffffff"), (1, "#e4e6e9")], 0, 0, 1, 1), INK, LW)
    ic.path("M5,6H55V16H5Z", ic.lg([(0, "#8ab0ff"), (.5, "#1a3ae0"), (1, "#0a1a80")]), INK, LW)
    for k in range(1, 5):
        ic.add(f'<path d="M5,{16 + k * 8.4:.1f}H55M{5 + k * 10},16V58" stroke="#a8adb4" stroke-width="1"/>')
    _new_badge(ic, 30, 33, 16)


def _template_page(ic, x=10, y=4, w=40, h=54):
    _page(ic, x, y, w, h)
    ic.add(f'<path d="M{x + 5},{y + 14}H{x + w - 14}V{y + 22}H{x + 5}Z" fill="none" stroke="#2a5ae0" stroke-width="1.2" stroke-dasharray="2.4 1.6"/>')
    for k in range(4):
        ic.add(f'<path d="M{x + 5},{y + 30 + k * 6}H{x + w - 6 - (k % 2) * 8}" stroke="#2a5ae0" stroke-width="1.2" stroke-dasharray="2.4 1.6"/>')


def new_from_template(ic):
    """New from template: a page laid out with dashed placeholders, and a green plus badge."""
    _template_page(ic, 6, 4, 40, 54)
    _new_badge(ic, 46, 46, 15)


def save_as_template(ic):
    """Save as template: the floppy disk in front of a template page."""
    from actions import save
    _template_page(ic, 24, 2, 36, 46)
    ic.add('<g transform="translate(0,22) scale(.62)">')
    save(ic)
    ic.add("</g>")


def _envelope(ic, x=4, y=16, w=48, h=36):
    e = f"M{x},{y}H{x + w}V{y + h}H{x}Z"
    ic.shadow(e, 2.4, 2)
    ic.path(e, ic.lg([(0, "#fffdf6"), (1, "#e8dcc4")], 0, 0, 1, 1), INK, LW)
    ic.add(f'<path d="M{x + .6},{y + .6}L{x + w / 2},{y + h * .58}L{x + w - .6},{y + .6}M{x + .6},{y + h - .6}L{x + w * .38},{y + h * .5}'
           f'M{x + w - .6},{y + h - .6}L{x + w * .62},{y + h * .5}" fill="none" stroke="#8a7a5c" stroke-width="1.2" stroke-linejoin="round"/>')


def mail_new(ic):
    _envelope(ic, 3, 20, 50, 36)
    _new_badge(ic, 47, 17, 15)


def mail_sent(ic):
    _envelope(ic, 3, 20, 44, 36)
    _teal(ic, _poly(_arrow_pts(50, 58, 50, 6, 4.4, 11, 13)))


def highscores(ic):
    """High scores: a silver trophy cup on a page."""
    _page(ic, 8, 4, 44, 56)
    cup = "M18,14H44Q44,30 34,34V42H38L40,48H22L24,42H28V34Q18,30 18,14Z"
    ic.shadow(cup, 2.2, 1.8)
    for s in (1, -1):
        h = f"M{31 + s * 13},17Q{31 + s * 20},17 {31 + s * 18},24Q{31 + s * 16},29 {31 + s * 9},30"
        ic.add(f'<path d="{h}" fill="none" stroke="{INK}" stroke-width="3.6"/><path d="{h}" fill="none" stroke="#c3c7cd" stroke-width="1.8"/>')
    ic.path(cup, ic.lg([(0, "#5c6168"), (.35, "#ffffff"), (.6, "#c3c7cd"), (1, "#4c5158")], 0, 0, 1, 0), INK, LW)
    ic.path(rrect(19, 48, 24, 6, 1.5), ic.lg([(0, "#3c4148"), (1, "#0a0c10")]), INK, 1)


# ------------------------------------------------------------------ help, tools and apps
def whats_this(ic):
    """What's this: the black mouse pointer with the blue question mark beside it."""
    from settingstrace import help_browser
    ic.add('<g transform="translate(26,4) scale(.6)">')
    help_browser(ic)
    ic.add("</g>")
    p = "M6,6V48L16,38L24,56L31,53L23,35H37Z"
    ic.shadow(p, 2.2, 1.8)
    _mpath(ic, p, ic.lg([(0, "#4c5158"), (1, "#000000")], 0, 0, 1, 1), 1.6)
    ic.add('<path d="M9,12V40" stroke="#fff" stroke-opacity=".5" stroke-width="1.2"/>')


def wizard(ic):
    """Wizard: a black magic wand with a white tip and the sparkle at its end."""
    ic.add('<g transform="translate(9,55) rotate(-135)">')
    ic.shadow("M-3,-2H3V44H-3Z", 2, 1.6)
    ic.path("M-3,0H3V44H-3Z", ic.lg([(0, "#5c6168"), (.4, "#2c3036"), (1, "#000000")], 0, 0, 1, 0), INK, 1.1)
    ic.path("M-3,36H3V44H-3Z", ic.lg([(0, "#c3c7cd"), (.4, "#ffffff"), (1, "#8a9098")], 0, 0, 1, 0), INK, 1)
    ic.add("</g>")
    _sparkle(ic, 50, 14, 12.5)


def krfb(ic):
    """Desktop sharing: a monitor with a watching eye on its screen."""
    m = rrect(3, 6, 58, 48, 3)
    ic.shadow(m, 2.6, 2.2)
    ic.path(m, ic.lg([(0, "#ffffff"), (.5, "#c3c7cd"), (1, "#7b818a")], 0, 0, 1, 1), INK, LW)
    ic.path("M8,11H56V46H8Z", ic.lg([(0, "#ffffff"), (1, "#d8e4f0")], 0, 0, 1, 1), INK, 1)
    eye = "M12,28.5Q32,10 52,28.5Q32,47 12,28.5Z"
    ic.path(eye, "#ffffff", INK, 1.4)
    ic.path(circle(32, 28.5, 9), ic.rg([(0, "#a8d0ff"), (.6, "#1a4ae0"), (1, "#0a1a60")], .4, .35, .8), INK, 1)
    ic.path(circle(32, 28.5, 4), "#000000", None)
    ic.path(circle(29.6, 26, 1.8), "#ffffff", None)
    for x in (12, 17, 22):
        ic.path(f"M{x},49H{x + 3}V51H{x}Z", "#e0281a", None)


def cookies(ic):
    """Cookies: KDE 3's joke icon - a chocolate birthday cake with one candle."""
    ic.add('<path d="M6,46A26,7 0 0 0 58,46V50A26,7 0 0 1 6,50Z" fill="#d9dce0" stroke="#141414" stroke-width="1.2"/>')
    side = "M10,30V44A22,6 0 0 0 54,44V30Z"
    ic.shadow(side, 2.4, 2)
    ic.path(side, ic.lg([(0, "#3a1a04"), (.35, "#a8642a"), (.6, "#7a3e10"), (1, "#2a1002")], 0, 0, 1, 0), INK, LW)
    ic.path("M10,30A22,6 0 0 1 54,30A22,6 0 0 1 10,30Z", ic.lg([(0, "#ffffff"), (1, "#e4dcd0")]), INK, LW)
    ic.add('<path d="M10,30Q12,38 15,31Q18,38 22,32Q26,39 30,33Q34,39 38,33Q42,38 46,32Q50,37 54,30" fill="#ffffff" stroke="#141414" stroke-width="1"/>')
    ic.path(rrect(29.5, 12, 5, 18, 1.5), ic.lg([(0, "#ffffff"), (1, "#e4e6e9")], 0, 0, 1, 0), INK, 1)
    for y in (14, 19, 24):
        ic.add(f'<path d="M29.5,{y + 2}L34.5,{y}" stroke="#e0200a" stroke-width="2"/>')
    ic.path("M32,3Q36,8 32,11Q28,8 32,3Z", ic.lg([(0, "#fffbb0"), (.5, "#ffc010"), (1, "#e0400a")]), "#7a3004", .9)


def babelfish(ic):
    """Set language: KDE 3's Babel fish - a little yellow and orange fish."""
    body = "M8,32Q20,12 40,18Q48,21 52,28L60,18V46L52,36Q48,43 40,46Q20,52 8,32Z"
    ic.shadow(body, 2.4, 2)
    ic.path(body, ic.lg([(0, "#fffbb0"), (.4, "#ffc010"), (.8, "#e0500a"), (1, "#8a2004")], 0, 0, .3, 1), INK, LW)
    ic.add('<path d="M28,20Q24,32 28,44M34,19.6Q30,32 34,45" fill="none" stroke="#a83a04" stroke-width="1.2"/>')
    ic.path(circle(17, 29, 4.6), "#ffffff", INK, 1.1)
    ic.path(circle(18, 29.6, 2.4), "#000000", None)
    ic.add('<path d="M12,22Q20,16 30,17" fill="none" stroke="#fff" stroke-opacity=".75" stroke-width="1.6" stroke-linecap="round"/>')
    ic.add(f'<path d="M10,38Q14,40 17,38" fill="none" stroke="{INK}" stroke-width="1.2" stroke-linecap="round"/>')


def spectacle(ic):
    """Screenshot (Spectacle): KDE 3's green camera held in front of a window."""
    w = "M24,4H60V36H24Z"
    ic.shadow(w, 2.2, 1.8)
    ic.path(w, ic.lg([(0, "#ffffff"), (1, "#e4e6e9")], 0, 0, 1, 1), INK, LW)
    ic.path("M24,4H60V11H24Z", ic.lg([(0, "#8ab0ff"), (.5, "#1a3ae0"), (1, "#0a1a80")]), INK, LW)
    cam = rrect(3, 22, 46, 34, 5)
    ic.path(rrect(10, 17, 12, 7, 2), ic.lg([(0, "#5c6168"), (1, "#14171c")]), INK, 1)
    ic.shadow(cam, 2.6, 2.2)
    ic.path(cam, ic.lg([(0, "#b8f8a0"), (.4, "#3fbf2a"), (1, "#0e5a08")], 0, 0, .4, 1), INK, LW * 1.2)
    ic.path(circle(26, 39, 11), ic.lg([(0, "#ffffff"), (1, "#5c6168")], 0, 0, 1, 1), INK, 1.2)
    ic.path(circle(26, 39, 7.6), ic.rg([(0, "#8ab0d0"), (.5, "#1a2a40"), (1, "#000000")], .38, .32, .8), INK, 1)
    ic.path(circle(23.4, 36.4, 2), "#ffffff", None, ' fill-opacity=".8"')
    ic.path("M8,27H16V31H8Z", ic.lg([(0, "#e8f6ff"), (1, "#5a8ab0")]), INK, .9)
    ic.path(rrect(36, 25, 9, 6, 1.5), ic.lg([(0, "#ff8a7a"), (1, "#a8180a")]), INK, .9)


# ------------------------------------------------------------------ registry
DS = {
    "actions": {"align-horizontal-left": align_left, "align-horizontal-right": align_right,
                "align-horizontal-center": align_hcenter, "align-vertical-top": align_top,
                "align-vertical-bottom": align_bottom, "align-vertical-center": align_vcenter,
                "format-font-size-more": font_size_more, "format-font-size-less": font_size_less,
                "format-list-ordered": list_ordered, "format-list-unordered": list_unordered,
                "format-text-subscript": subscript, "insert-text-frame": text_frame, "percent": percent,
                "view-sort-descending": sort_descending, "draw-eraser": eraser, "draw-polygon": polygon,
                "edit-image": edit_image, "gnumeric-ungroup": ungroup, "shear": shear, "layer-new": layer_new,
                "layer-delete": layer_delete, "object-flip-horizontal": flip_horizontal, "enum": enum,
                "appointment-new": appointment_new, "document-new-from-template": new_from_template,
                "document-save-as-template": save_as_template, "mail-message-new": mail_new, "mail-sent": mail_sent,
                "games-highscores": highscores, "help-whatsthis": whats_this, "tools-wizard": wizard,
                "set-language": babelfish},
    "apps": {"krfb": krfb, "preferences-web-browser-cookies": cookies, "spectacle": spectacle},
}
EFFECTS = ("dialog-parent dimscreen fade fadedesktop login logout maximize screenshot translucency windowaperture").split()
DS_ALIASES = {
    "activities-symbolic": "apps/preferences-desktop-activities", "virtual-desktops-symbolic": "apps/preferences-desktop-virtual",
    "class": "actions/code-class", "contents": "actions/help-contents", "flag": "actions/mark-location",
    "view-calendar-holiday": "actions/mark-location", "input-keyboard-battery": "devices/input-keyboard",
    "input-keyboard-brightness": "devices/input-keyboard", "input-mouse-battery": "devices/input-mouse",
    "ksmserver": "actions/system-log-out", "mediacontrol": "apps/audio-speakers",
    "object-rotate-left-symbolic": "actions/object-rotate-left", "transform-rotate": "actions/object-rotate-left",
    "online": "status/network-connect", "preferences": "apps/preferences-system", "smartphone-symbolic": "devices/smartphone",
    "tools-symbolic": "actions/configure", "unlock": "emblems/object-unlocked", "user-desktop-symbolic": "places/user-desktop",
    "user-identity-symbolic": "apps/preferences-desktop-user", "user-trash-symbolic": "places/user-trash",
    "video-television": "apps/tv", "view-sort-ascending": "actions/view-sort", "view-sort-ascending-symbolic": "actions/view-sort",
    "view-sort-descending-symbolic": "actions/view-sort-descending", "viewimage": "actions/view-preview",
    "viewpdf": "mimetypes/application-pdf", "zoom": "actions/zoom-in", "tools-wizard-symbolic": "actions/tools-wizard",
    "org.kde.spectacle": "apps/spectacle", "mail-send": "actions/mail-sent", "mail-message-new-symbolic": "actions/mail-message-new",
    "appointment-new-symbolic": "actions/appointment-new", "set-language-symbolic": "actions/set-language",
    "edit-image-symbolic": "actions/edit-image", "format-list-ordered-symbolic": "actions/format-list-ordered",
    "format-list-unordered-symbolic": "actions/format-list-unordered", "help-whatsthis-symbolic": "actions/help-whatsthis",
    "draw-eraser-symbolic": "actions/draw-eraser", "krfb-symbolic": "apps/krfb", "org.kde.krfb": "apps/krfb",
    **{f"preferences-system-windows-effect-{e}": "apps/preferences-desktop-effects" for e in EFFECTS},
}


def write(out):
    n = 0
    for ctx, icons in DS.items():
        d = f"{out}/scalable/{ctx}"
        os.makedirs(d, exist_ok=True)
        for name, fn in icons.items():
            open(f"{d}/{name}.svg", "w").write(_ic(fn)().svg(64))
            n += 1
    missing = []
    for a, t in DS_ALIASES.items():
        ctx, name = t.split("/")
        d = f"{out}/scalable/{ctx}"
        if not os.path.exists(f"{d}/{name}.svg"):
            missing.append(t)
            continue
        if not any(os.path.lexists(f"{out}/scalable/{c}/{a}.svg") for c in os.listdir(f"{out}/scalable")):
            os.symlink(f"{name}.svg", f"{d}/{a}.svg")
    if missing:
        print("desktoptrace: alias targets missing:", missing)
    return n
