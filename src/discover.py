"""KDE Classic Vector: Discover (software centre) icons - category sidebar and app/update pages.

Categories follow KDE 3's K-menu package_* icons where they exist (games box and joystick, typewriter,
crossed hammer and wrench, playing cards, checkers board, tank, mortarboard, ladybird, K gear).
"""
import math, os
from gen import Icon, INK, LW, circle, rrect, e_globe


def _ic(fn):
    def f():
        ic = Icon()
        fn(ic)
        return ic
    return f


def _star(cx, cy, r1, r2, n=5, rot=-90):
    pts = []
    for k in range(n * 2):
        a = math.radians(rot + 180 * k / n)
        r = r1 if k % 2 == 0 else r2
        pts.append(f"{cx + r * math.cos(a):.2f},{cy + r * math.sin(a):.2f}")
    return "M" + "L".join(pts) + "Z"


def _glossy(ic, d, c, w=LW):
    ic.path(d, ic.lg([(0, c[0]), (.5, c[1]), (1, c[2])], 0, 0, 1, 1), INK, w)


METAL = ("#ffffff", "#b4b9c0", "#5c6168")
WOOD = ("#f0b070", "#b8662a", "#5a2806")


# ------------------------------------------------------------------ main categories
def development(ic):
    """Development: a code window (green text on dark) with a spanner across the corner."""
    ic.shadow("M4,8H52V48H4Z", 2.6, 2.2)
    ic.path("M4,8H52V48H4Z", ic.lg([(0, "#3c4148"), (1, "#14171c")]), INK, LW)
    ic.path("M4,8H52V15H4Z", ic.lg([(0, "#9fc8f0"), (1, "#3a6ac0")]), INK, LW)
    rows = ((9, 26, "#7ae07a"), (13, 32, "#e8e070"), (13, 22, "#7ae07a"), (9, 18, "#9fd4ff"), (9, 30, "#7ae07a"))
    for k, (x0, x1, c) in enumerate(rows):
        ic.add(f'<path d="M{x0},{20 + k * 5.6}H{x1}" stroke="{c}" stroke-width="2.2" stroke-linecap="round"/>')
    ic.add('<path d="M38,24L33,29L38,34M44,24L49,29L44,34" fill="none" stroke="#ff9a5a" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>')
    _spanner(ic, 46, 46, 1.0)


def _spanner(ic, cx, cy, k, angle=-45):
    """A silver open-ended spanner, drawn along its own axis then turned."""
    d = ("M-3,-18A8,8 0 1 1 3,-18L3,-12.5L6,-15.5A8,8 0 0 0 -6,-15.5L-3,-12.5Z"
         "M-3,-12.5H3V14A3,3 0 0 1 -3,14Z")
    head = "M0,-26A9,9 0 1 0 0.01,-26ZM-3,-29H3V-21H-3Z"
    t = f"translate({cx},{cy}) rotate({angle}) scale({k})"
    body = "M-3.4,-14V15Q-3.4,18 0,18Q3.4,18 3.4,15V-14Z"
    jaw = "M-9,-20A9,9 0 0 1 9,-20L6,-14H-6Z M-3.6,-29.5V-22H3.6V-29.5A9,9 0 0 1 9,-20H-9A9,9 0 0 1 -3.6,-29.5Z"
    ic.add(f'<g transform="{t}">')
    ic.shadow(body + "M-9,-20A9,9 0 1 1 9,-20L6,-14H-6Z", 1.8, 1.6)
    ic.path(body, ic.lg([(0, METAL[2]), (.4, METAL[0]), (1, METAL[2])], 0, 0, 1, 0), INK, 1.2)
    ic.path("M-9,-20A9,9 0 0 1 -3.6,-28.6V-21H3.6V-28.6A9,9 0 0 1 9,-20L6,-14H-6Z",
            ic.lg([(0, METAL[2]), (.4, METAL[0]), (1, METAL[2])], 0, 0, 1, 0), INK, 1.2)
    ic.add("</g>")


def engineering(ic):
    """Engineering: a drafting compass standing on a blueprint."""
    ic.add('<g transform="matrix(1,0,-.3,.8,12,12)">')
    ic.shadow("M4,8H52V52H4Z", 2.6, 2.2)
    ic.path("M4,8H52V52H4Z", ic.lg([(0, "#6aa8f0"), (1, "#1a4ea0")]), INK, LW)
    grid = "".join(f"M{4 + k * 8},8V52" for k in range(1, 6)) + "".join(f"M4,{8 + k * 8}H52" for k in range(1, 6))
    ic.add(f'<path d="{grid}" stroke="#fff" stroke-opacity=".35" stroke-width=".7"/>')
    ic.add('<path d="M12,44V20H28L40,32V44Z" fill="none" stroke="#fff" stroke-width="1.6"/>')
    ic.add('<circle cx="34" cy="20" r="6" fill="none" stroke="#fff" stroke-width="1.4"/>')
    ic.add("</g>")
    legs = "M32,10L20,52M32,10L46,50"
    ic.add(f'<path d="{legs}" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>')
    ic.add(f'<path d="{legs}" stroke="#d9dce0" stroke-width="2.8" stroke-linecap="round"/>')
    ic.add(f'<path d="M20,52L19,57" stroke="{INK}" stroke-width="1.6" stroke-linecap="round"/>')
    ic.path("M44.6,46L48,46L47.4,53L45.6,52Z", "#3c4148", INK, .8)
    ic.path(circle(32, 10, 4.4), ic.rg([(0, "#fff8c0"), (1, "#a87a10")]), INK, 1.2)
    ic.add(f'<path d="M32,5.6V1.5" stroke="{INK}" stroke-width="3.2" stroke-linecap="round"/>')


def physics(ic):
    """Physics: an atom - a glossy red nucleus with three electron orbits, each with its blue electron."""
    for k, rot in enumerate((0, 60, 120)):
        ic.add(f'<g transform="rotate({rot} 32 32)">')
        ic.add(f'<ellipse cx="32" cy="32" rx="27" ry="10" fill="none" stroke="{INK}" stroke-width="4.2"/>')
        ic.add('<ellipse cx="32" cy="32" rx="27" ry="10" fill="none" stroke="#7ad0e8" stroke-width="2.2"/>')
        ic.add("</g>")
    for rot in (0, 60, 120):
        a = math.radians(rot)
        ex, ey = 32 + 27 * math.cos(a), 32 + 27 * math.sin(a)
        ic.path(circle(ex, ey, 4.4), ic.rg([(0, "#c8e4ff"), (.5, "#2a6ae0"), (1, "#0a1a70")], .4, .35, .8), INK, 1.1)
    ic.shadow(circle(32, 32, 8), 1.8, 1.5)
    ic.path(circle(32, 32, 8), ic.rg([(0, "#ffd0c0"), (.45, "#e8200a"), (1, "#6a0402")], .38, .32, .8), INK, 1.3)


def science(ic):
    """Science: a glass flask with bubbling green liquid."""
    flask = "M26,6H38V10H36V24L52,52Q54,58 48,58H16Q10,58 12,52L28,24V10H26Z"
    liquid = "M21.4,38H42.6L50.4,51.5Q51.6,55.4 47.4,55.4H16.6Q12.4,55.4 13.6,51.5Z"
    ic.shadow(flask, 2.6, 2.2)
    ic.path(flask, ic.lg([(0, "#ffffff"), (1, "#d8eef8")], 0, 0, 1, 1), INK, LW, ' fill-opacity=".9"')
    ic.path(liquid, ic.lg([(0, "#b8ff90"), (.5, "#3fbf2a"), (1, "#0e6a10")]), None)
    ic.add('<path d="M21.4,38H42.6" stroke="#e0ffc8" stroke-width="1.4"/>')
    for x, y, r in ((26, 47, 2.6), (35, 50, 1.8), (31, 43, 1.4), (40, 45, 1.2), (31, 31, 1.8), (34, 20, 1.4)):
        ic.path(circle(x, y, r), "#ffffff", "#2a8a20", .6, ' fill-opacity=".8"')
    ic.add('<path d="M30,12V25L18,46" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round"/>')
    ic.path(flask, "none", INK, LW)


def education(ic):
    """Education: KDE 3's black mortarboard with a red tassel, resting on a book."""
    book = "M8,40L32,50L56,40V48L32,58L8,48Z"
    ic.shadow(book, 2.6, 2.2)
    ic.path("M8,40L32,50V58L8,48Z", ic.lg([(0, "#ffffff"), (1, "#c9ccd1")]), INK, 1.2)
    ic.path("M32,50L56,40V48L32,58Z", ic.lg([(0, "#e4e6e9"), (1, "#9aa0a8")]), INK, 1.2)
    ic.path("M8,40L32,31L56,40L32,50Z", ic.lg([(0, "#ff8a7a"), (1, "#a8180c")]), INK, 1.2)
    for k in range(3):
        ic.add(f'<path d="M10,{43 + k * 1.8}L32,{52 + k * 1.8}" stroke="#9aa0a8" stroke-width=".6"/>')
    # cap: skull-cap under a square board seen at an angle
    ic.path("M20,22V30Q32,37 44,30V22Z", ic.lg([(0, "#4c5158"), (1, "#0a0c10")], 0, 0, 1, 0), INK, 1.2)
    board = "M32,6L58,17L32,28L6,17Z"
    ic.shadow(board, 2, 1.8)
    ic.path(board, ic.lg([(0, "#5c6168"), (.5, "#202328"), (1, "#0a0c10")], 0, 0, 1, 1), INK, 1.4)
    ic.add('<path d="M10,17L32,8L54,17" fill="none" stroke="#fff" stroke-opacity=".3" stroke-width="1"/>')
    ic.add(f'<path d="M32,17L50,22V34" fill="none" stroke="{INK}" stroke-width="2.4"/>')
    ic.add('<path d="M32,17L50,22V34" fill="none" stroke="#e0281a" stroke-width="1.2"/>')
    ic.path("M48,33H52L53,40H47Z", ic.lg([(0, "#ff8a7a"), (1, "#a8180c")]), INK, .9)
    ic.path(circle(32, 17, 1.8), "#e0281a", INK, .6)


def mathematics(ic):
    """Mathematics: a green chalkboard in a wooden frame with a sum chalked on it."""
    ic.shadow("M4,8H60V50H4Z", 2.6, 2.2)
    ic.path("M4,8H60V50H4Z", ic.lg([(0, WOOD[0]), (.5, WOOD[1]), (1, WOOD[2])], 0, 0, 1, 1), INK, LW)
    ic.path("M8,12H56V46H8Z", ic.lg([(0, "#3a7a4a"), (1, "#14402a")], 0, 0, 1, 1), INK, 1)
    chalk = "M13,22H21M17,18V26M26,22H33M26,28L33,16M38,20H46M38,24H46M13,38Q15,32 19,36T25,36M30,34H50"
    ic.add(f'<path d="{chalk}" fill="none" stroke="#f4f4ec" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')
    ic.add('<path d="M4,50H60L58,56H6Z" fill="#8a4c14" stroke="#141414" stroke-width="1.2"/>')
    ic.path(rrect(40, 51, 9, 3, 1.2), "#ffffff", INK, .7)


def _open_box(ic, inside=None):
    """The open cardboard box for Games, in the archive icons' colours. `inside(ic)`, if given, is drawn
    after the far walls and before the front walls, so whatever it draws sits in the box."""
    P = lambda *pts: "M" + "L".join(f"{a:.2f},{b:.2f}" for a, b in pts) + "Z"
    T, R, F, L, h = (27, 13), (47, 23), (27, 33), (7, 23), 21
    dn = lambda p: (p[0], p[1] + h)
    ic.shadow(P(T, R, dn(R), dn(F), dn(L), L), 2.8, 2.4)
    # back flaps opened up and outwards
    ic.path(P(L, T, (T[0] - 4, T[1] - 5.6), (L[0] - 4, L[1] - 5.6)), ic.lg([(0, "#fffbe4"), (1, "#d8c070")], 0, 0, 1, 1), INK, 1.2)
    ic.path(P(T, R, (R[0] + 4.4, R[1] - 5.4), (T[0] + 4.4, T[1] - 5.4)), ic.lg([(0, "#e8d690"), (1, "#a89040")], 0, 0, 1, 1), INK, 1.2)
    # inside: the two far walls in shadow, darker toward the bottom
    ic.path(P(L, T, R, F), ic.lg([(0, "#8a7430"), (.6, "#5a4a1a"), (1, "#3a2e0e")]), INK, 1.2)
    ic.path(P((L[0] + 3, L[1] + 1.5), (T[0], T[1] + 3), (T[0], F[1] - 3)), "#b8a050", None, ' fill-opacity=".55"')
    if inside:
        inside(ic)
    # front walls
    ic.path(P(L, F, dn(F), dn(L)), ic.lg([(0, "#fbf2c4"), (1, "#cdb468")]), INK, 1.3)
    ic.path(P(F, R, dn(R), dn(F)), ic.lg([(0, "#d8c070"), (1, "#8a7430")]), INK, 1.3)
    # front flaps folded down and outwards
    ic.path(P(L, F, (F[0] - 3, F[1] + 7), (L[0] - 4.5, L[1] + 5)), ic.lg([(0, "#fffbe4"), (1, "#e8d690")]), INK, 1.1)
    ic.path(P(F, R, (R[0] + 5, R[1] + 5), (F[0] + 3, F[1] + 7)), ic.lg([(0, "#e8d690"), (1, "#a89040")]), INK, 1.1)


def _iso_base(ic, cx, cy, w, h, cols):
    P = lambda *pts: "M" + "L".join(f"{a:.2f},{b:.2f}" for a, b in pts) + "Z"
    T, R, F, L = (cx, cy - w / 2), (cx + w, cy), (cx, cy + w / 2), (cx - w, cy)
    dn = lambda p: (p[0], p[1] + h)
    ic.shadow(P(T, R, dn(R), dn(F), dn(L), L), 2.4, 2)
    ic.path(P(L, F, dn(F), dn(L)), ic.lg([(0, cols[1]), (1, cols[2])]), INK, 1.2)
    ic.path(P(F, R, dn(R), dn(F)), ic.lg([(0, cols[2]), (1, cols[3])]), INK, 1.2)
    ic.path(P(T, R, F, L), ic.lg([(0, cols[0]), (1, cols[1])], 0, 0, 1, 1), INK, 1.2)


def _button(ic, x, y, rx=2.6, col=("#ffb0a0", "#a8180c")):
    ic.path(f"M{x - rx},{y}A{rx},{rx * .5} 0 1 0 {x + rx},{y}A{rx},{rx * .5} 0 1 0 {x - rx},{y}Z", ic.lg([(0, col[0]), (1, col[1])]), INK, .8)


def _rod(ic, x0, y0, x1, y1, w, cols):
    ic.add(f'<path d="M{x0},{y0}L{x1},{y1}" stroke="{INK}" stroke-width="{w + 2.2}" stroke-linecap="round"/>')
    gid = ic.gid("rod")
    ic.defs.append(f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{x0 - w}" y1="0" x2="{x0 + w}" y2="0">'
                   f'<stop offset="0" stop-color="{cols[0]}"/><stop offset=".4" stop-color="{cols[1]}"/><stop offset="1" stop-color="{cols[2]}"/></linearGradient>')
    ic.add(f'<path d="M{x0},{y0}L{x1},{y1}" stroke="url(#{gid})" stroke-width="{w}" stroke-linecap="round"/>')


GREY_BASE = ("#ffffff", "#c9ccd1", "#9aa0a8", "#4c5158")
BLACK_BASE = ("#8a9098", "#3c4148", "#2c3036", "#0a0c10")


def joy_pc(ic):
    """A: the original's 90s PC joystick - wide grey base, short chunky light-grey grip, red top button."""
    _iso_base(ic, 46, 48, 16, 6, GREY_BASE)
    _button(ic, 35, 49); _button(ic, 56, 46)
    ic.path("M42,48A4,2 0 1 0 50,48V46A4,2 0 1 0 42,46Z", "#2c3036", INK, .9)
    grip = "M42.4,46.5L41.6,30Q41.4,25.5 46,25.5Q50.6,25.5 50.4,30L49.6,46.5Z"
    ic.shadow(grip, 1.6, 1.4)
    ic.path(grip, ic.lg([(0, "#6c727a"), (.35, "#f4f5f6"), (.7, "#b4b9c0"), (1, "#5c6168")], 0, 0, 1, 0), INK, 1.3)
    for y in (33, 36.4, 39.8):
        ic.add(f'<path d="M42.4,{y}H49.6" stroke="#6c727a" stroke-width=".8"/>')
    ic.path("M41.8,27.4Q41.8,22 46,22Q50.2,22 50.2,27.4Z", ic.lg([(0, "#ffb0a0"), (.5, "#e0281a"), (1, "#6a0804")], 0, 0, 1, 0), INK, 1.2)


def joy_atari(ic):
    """B: the 80s home-computer joystick - square black base, thin black stick, one red fire button."""
    _iso_base(ic, 46, 47, 15, 7, BLACK_BASE)
    _button(ic, 35, 47.4, 3.2)
    ic.path("M42.6,47A3.4,1.7 0 1 0 49.4,47A3.4,1.7 0 1 0 42.6,47Z", "#14171c", INK, .8)
    _rod(ic, 46, 46, 47, 26, 4, ("#14171c", "#6c727a", "#0a0c10"))
    ic.path("M43.4,27V24Q43.4,21 47,21Q50.6,21 50.6,24V27Q47,29 43.4,27Z", ic.lg([(0, "#3c4148"), (.4, "#8a9098"), (1, "#0a0c10")], 0, 0, 1, 0), INK, 1.1)


def joy_arcade(ic):
    """C: an arcade stick - silver shaft with a big red ball top, on a black base with coloured buttons."""
    _iso_base(ic, 46, 48, 16, 6, BLACK_BASE)
    # three buttons in a neat row on the right-hand side, running along the base
    for k, c in enumerate((("#b8dcff", "#1a4a9a"), ("#fff0a0", "#a87a04"), ("#c8f8a8", "#145a0c"))):
        _button(ic, 51.6 + k * 3.5, 50.4 - k * 1.75, 1.9, c)
    ic.path("M42,48A4,2 0 1 0 50,48A4,2 0 1 0 42,48Z", "#14171c", INK, .8)
    _rod(ic, 46, 47, 46, 30, 2.8, ("#5c6168", "#ffffff", "#5c6168"))
    ic.shadow(circle(46, 26, 7), 1.6, 1.4)
    ic.path(circle(46, 26, 7), ic.rg([(0, "#ffd0c8"), (.5, "#e0281a"), (1, "#6a0804")], .38, .3, .8), INK, 1.3)


GAMES_JOYSTICK = joy_arcade


def games(ic, joystick=None):
    """Games: as KDE 3 - an open cardboard box with a joystick standing in front of its lower right corner."""
    _open_box(ic)
    (joystick or GAMES_JOYSTICK)(ic)


def _games_option(fn):
    return lambda ic: games(ic, fn)


games_a, games_b, games_c = _games_option(joy_pc), _games_option(joy_atari), _games_option(joy_arcade)


def arcade(ic):
    """Arcade: a little platform-game screen - sky, green ledges, a jumping hero and a coin."""
    ic.shadow("M6,6H58V58H6Z", 2.6, 2.2)
    ic.path("M6,6H58V58H6Z", ic.lg([(0, "#bfe8ff"), (1, "#4aa2e0")]), INK, LW * 1.4)
    ic.path("M14,16Q14,12 19,12Q21,9 25,11Q29,10 29,14Q32,15 30,17H14Z", "#ffffff", None)
    for x0, x1, y in ((8, 26, 44), (34, 56, 32), (20, 40, 20)):
        ic.path(f"M{x0},{y}H{x1}V{y + 5}H{x0}Z", ic.lg([(0, "#9ee070"), (.3, "#3fae2a"), (.35, "#a86a2a"), (1, "#6a3a10")]), INK, 1)
    ic.path("M6,52H58V58H6Z", ic.lg([(0, "#a86a2a"), (1, "#6a3a10")]), INK, 1)
    ic.path(rrect(16, 33, 6, 8, 1.4), "#e0281a", INK, .8)                   # hero
    ic.path(circle(19, 30.5, 2.6), "#ffd8b0", INK, .7)
    ic.add(f'<path d="M17,41V44M21,41V44" stroke="{INK}" stroke-width="1.6"/>')
    ic.path(circle(45, 24, 3.4), ic.rg([(0, "#fffbe0"), (1, "#e8a010")]), INK, .9)
    ic.path(circle(30, 12.5, 3.4), ic.rg([(0, "#fffbe0"), (1, "#e8a010")]), INK, .9)


def board(ic):
    """Board games: KDE 3's checkerboard seen from above, peach and dark brown squares, red and blue marbles."""
    ic.shadow("M3,3H61V61H3Z", 2.6, 2.2)
    ic.path("M3,3H61V61H3Z", ic.lg([(0, "#5a3410"), (1, "#2a1404")], 0, 0, 1, 1), INK, LW)
    x0, n, c = 6, 8, 6.5
    ic.path(f"M{x0},{x0}H{x0 + n * c}V{x0 + n * c}H{x0}Z", ic.lg([(0, "#fff4e0"), (.5, "#fcd8a8"), (1, "#f0a860")], 0, 0, 1, 1), None)
    d = ""
    for i in range(n):
        for j in range(n):
            if (i + j) % 2:
                d += f"M{x0 + i * c:.1f},{x0 + j * c:.1f}h{c}v{c}h-{c}Z"
    ic.path(d, ic.lg([(0, "#5a3410"), (1, "#2a1404")], 0, 0, 1, 1), None)
    ic.path(circle(19, 19, 13), ic.rg([(0, "#ffffff", .85), (.5, "#ffffff", .35), (1, "#ffffff", 0)], .5, .5, .5), None)
    red = ((6, 1), (3, 2), (5, 3), (2, 4), (5, 5), (6, 7))
    blue = ((4, 2), (3, 4), (1, 5), (6, 5), (3, 6))
    for cells, col in ((red, ("#ffc8c0", "#e0281a", "#6a0804")), (blue, ("#c8e0ff", "#2a5ac8", "#0c2060"))):
        for i, j in cells:
            x, y = x0 + (i + .5) * c, x0 + (j + .5) * c
            ic.path(circle(x + 1.2, y + 1.2, 2.7), "#000", None, ' fill-opacity=".35"')
            ic.path(circle(x, y, 2.7), ic.rg([(0, col[0]), (.55, col[1]), (1, col[2])], .35, .3, .8), INK, .6)


def cards(ic):
    """Card games: KDE 3's four aces stepped over one another - spades, clubs, diamonds, hearts -
    white fading to peach as in the original."""
    W, H = 22.5, 35
    def heart(x, y, k, c):
        ic.path(f"M{x},{y + 7 * k}C{x - 9 * k},{y} {x - 6 * k},{y - 7 * k} {x},{y - 3 * k}C{x + 6 * k},{y - 7 * k} {x + 9 * k},{y} {x},{y + 7 * k}Z", c, None)
    def diamond(x, y, k, c):
        ic.path(f"M{x},{y - 7 * k}L{x + 5.5 * k},{y}L{x},{y + 7 * k}L{x - 5.5 * k},{y}Z", c, None)
    def spade(x, y, k, c):
        ic.path(f"M{x},{y - 7 * k}C{x + 9 * k},{y} {x + 6 * k},{y + 6 * k} {x + 1 * k},{y + 3 * k}L{x + 2.4 * k},{y + 7 * k}H{x - 2.4 * k}"
                f"L{x - 1 * k},{y + 3 * k}C{x - 6 * k},{y + 6 * k} {x - 9 * k},{y} {x},{y - 7 * k}Z", c, None)
    def club(x, y, k, c):
        for dx, dy in ((0, -3.6), (-3.6, 1), (3.6, 1)):
            ic.path(circle(x + dx * k, y + dy * k, 3.2 * k), c, None)
        ic.path(f"M{x - 1 * k},{y}L{x - 2.6 * k},{y + 7 * k}H{x + 2.6 * k}L{x + 1 * k},{y}Z", c, None)
    def ace(x, y):
        d = f"M{x},{y + 5.4}L{x + 2},{y}L{x + 4},{y + 5.4}M{x + .7},{y + 3.6}H{x + 3.3}"
        ic.add(f'<path d="{d}" fill="none" stroke="#141414" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/>')
    for x, y, suit, col in ((1.5, 22, spade, "#141414"), (13, 11.5, club, "#141414"), (24.5, 2, diamond, "#e01a10"), (39.5, 20, heart, "#e01a10")):
        d = rrect(x, y, W, H, 2.4)
        ic.shadow(d, 2, 1.8)
        ic.path(d, ic.lg([(0, "#ffffff"), (.45, "#fff4e4"), (1, "#f4cc98")], 0, 0, .6, 1), INK, 1.4)
        suit(x + 4.4, y + 5.2, .4, col)              # small pip top left, A top right
        ace(x + W - 6.6, y + 2.4)
        suit(x + W / 2, y + H / 2, .95, col)
        ace(x + 2.6, y + H - 8)                       # A bottom left, small pip bottom right
        suit(x + W - 4.4, y + H - 5.2, .4, col)


def strategy(ic):
    """Strategy: KDE 3's green tank, now in isometric view with its gun pointing up and to the right,
    a red move arrow and a blue target cross above it."""
    ox, oy, k = 6, 50, 1.05
    def pt(u, v, z):
        return ox + .87 * (u + v) * k, oy + (-.5 * u + .5 * v - z) * k
    def poly(*q):
        return "M" + "L".join("{:.2f},{:.2f}".format(*pt(*p)) for p in q) + "Z"
    def block(u0, u1, v0, v1, z0, z1, top, side, end, w=1.2):
        ic.path(poly((u0, v0, z0), (u0, v1, z0), (u0, v1, z1), (u0, v0, z1)), end, INK, w)        # rear end (-u)
        ic.path(poly((u0, v1, z0), (u1, v1, z0), (u1, v1, z1), (u0, v1, z1)), side, INK, w)       # near side (+v)
        ic.path(poly((u0, v0, z1), (u1, v0, z1), (u1, v1, z1), (u0, v1, z1)), top, INK, w)        # top
    olive = lambda a, b: ic.lg([(0, a), (1, b)], 0, 0, 1, 1)
    # move arrow and target cross in the sky, as in the original
    ic.add('<path d="M8,30V12M3.5,17L8,10L12.5,17" fill="none" stroke="#e0281a" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>')
    ic.add('<path d="M17,5L25,13M25,5L17,13" stroke="#2a3ae8" stroke-width="2.6" stroke-linecap="round"/>')
    hull = poly((0, -1, 0), (32, -1, 0), (32, 17, 0), (32, 17, 7), (0, 17, 7), (0, -1, 7))
    ic.shadow(poly((0, -1, 0), (32, -1, 0), (32, 17, 0), (0, 17, 0)) + hull, 2.6, 2.2)
    # tracks and running gear
    block(0, 32, -1, 17, 0, 6.5, olive("#5c6168", "#2c3036"), olive("#3c4148", "#14171c"), olive("#4c5158", "#1a1d22"))
    for u in range(4, 31, 6):
        x, y = pt(u, 17, 3.2)
        ic.path(f"M{x - 2.4:.2f},{y:.2f}A2.4,2.8 0 1 0 {x + 2.4:.2f},{y:.2f}A2.4,2.8 0 1 0 {x - 2.4:.2f},{y:.2f}Z",
                ic.rg([(0, "#c3c7cd"), (1, "#3c4148")]), INK, .7)
    # upper hull, turret and gun
    block(2, 29, 1, 15, 6.5, 11, olive("#d8f080", "#7a9a28"), olive("#7a9a28", "#3a4a10"), olive("#9ab838", "#4a6014"))
    # curved turn arrow on the right, behind the gun
    arc, head = "M57,24Q53,13 42.5,15", "M46,11.4L42,15.1L46.2,18.6"
    for col, w in (("#fff", 4.2), ("#e0281a", 2.2)):
        ic.add(f'<path d="{arc}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>'
               f'<path d="{head}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')
    gx0, gy0 = pt(19, 8, 14)
    gx1, gy1 = pt(38, 8, 14)
    ic.add(f'<path d="M{gx0:.2f},{gy0:.2f}L{gx1:.2f},{gy1:.2f}" stroke="{INK}" stroke-width="4.4" stroke-linecap="round"/>')
    ic.add(f'<path d="M{gx0:.2f},{gy0:.2f}L{gx1:.2f},{gy1:.2f}" stroke="#7a9a28" stroke-width="2.4" stroke-linecap="round"/>')
    block(8, 20, 3, 13, 11, 16, olive("#e0f490", "#8aaa30"), olive("#7a9a28", "#3a4a10"), olive("#9ab838", "#4a6014"))
    hx, hy = pt(12, 7, 16)
    ic.path(f"M{hx - 3:.2f},{hy:.2f}A3,1.6 0 1 0 {hx + 3:.2f},{hy:.2f}A3,1.6 0 1 0 {hx - 3:.2f},{hy:.2f}Z", "#3a4a10", INK, .8)


def internet(ic):
    """Internet: the KDE globe with silver 'www' arched over it."""
    from filetypes import GLYPHS
    e_globe(ic, 9, 15, 22)
    g, w = GLYPHS["w"]
    for k, x in enumerate((6, 23, 40)):
        t = f"translate({x},14) scale(2.3)"
        ic.add(f'<g transform="{t}"><path d="{g}" fill="none" stroke="{INK}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
               f'<path d="{g}" fill="none" stroke="#eceef1" stroke-width="1.1" stroke-linecap="round" stroke-linejoin="round"/></g>')


def office(ic):
    """Office: KDE 3's traditional black typewriter - cream paper, brass platen knobs, gold and ivory keys."""
    brass = ic.lg([(0, "#5a4a10"), (.3, "#e8d070"), (.55, "#fff4b0"), (1, "#6a5410")], 0, 0, 1, 0)
    black = ic.lg([(0, "#6c727a"), (.35, "#2c3036"), (1, "#0a0c10")], 0, 0, .4, 1)
    # paper rolled into the platen
    paper = "M17,8H47V28H17Z"
    ic.shadow(paper, 2, 1.8)
    ic.path(paper, ic.lg([(0, "#ffffff"), (.6, "#fdf6e8"), (1, "#e8d8b8")]), INK, 1.3)
    for k in range(3):
        ic.add(f'<path d="M21,{13 + k * 4}H{43 - k * 5}" stroke="#b8a888" stroke-width="1.1"/>')
    # body: rounded, narrowing toward the bottom
    body = "M14,30Q14,27 17,27H47Q50,27 50,30L52,50Q52,56 46,56H18Q12,56 12,50Z"
    ic.shadow(body + "M8,20H56V33H8Z", 2.8, 2.4)
    ic.path(rrect(13, 20, 38, 9, 4), black, INK, 1.4)                                   # platen
    ic.add('<path d="M17,22.5H47" stroke="#fff" stroke-opacity=".35" stroke-width="1.2" stroke-linecap="round"/>')
    for x in (8, 50.5):                                                                  # brass knobs
        ic.path(rrect(x, 18.5, 5.5, 13, 2.6), brass, INK, 1.2)
        ic.add(f'<path d="M{x + 1.4},22V28" stroke="#fffbe0" stroke-opacity=".7" stroke-width="1.2" stroke-linecap="round"/>')
    ic.path(body, black, INK, LW)
    ic.path(rrect(27, 29, 10, 2.6, 1.2), ic.lg([(0, "#e4e6e9"), (1, "#7b818a")]), INK, .7)     # type guide
    # three rows of round keys, gold and ivory alternating as in the original
    for r, (y, n, x0) in enumerate(((34.5, 7, 16.8), (40, 7, 17.8), (45.5, 6, 20.6))):
        for k in range(n):
            col = ("#fff8d0", "#d8b840", "#6a5410") if (k + r) % 2 == 0 else ("#ffffff", "#e4e6e9", "#7b818a")
            ic.path(rrect(x0 + k * 4.4, y, 3.6, 3.6, 1.2), ic.rg([(0, col[0]), (.6, col[1]), (1, col[2])], .4, .35, .8), INK, .55)
    ic.path(rrect(23, 51, 18, 2.6, 1.2), ic.lg([(0, "#8a9098"), (1, "#3c4148")]), INK, .6)   # space bar


def utilities(ic):
    """Utilities: KDE 3's claw hammer with a wooden handle crossed over a pale blue spanner."""
    blue = ("#d8f8ff", "#7ad0dc", "#2a8aa0", "#0e4a58")
    # spanner: handle from lower left, open jaw at upper right
    sp = ("M0,-3.6H36L38,-7.4A9.4,9.4 0 0 1 52.6,-5.2L46.4,-3.2V3.2L52.6,5.2A9.4,9.4 0 0 1 38,7.4L36,3.6H0"
          "A3.6,3.6 0 0 1 0,-3.6Z")
    t = "translate(19.5,51.5) rotate(-40) scale(.9)"
    ic.shadow(sp, 2.4, 2, transform=t)
    ic.add(f'<g transform="{t}">')
    ic.path(sp, ic.lg([(0, blue[0]), (.35, blue[1]), (.75, blue[2]), (1, blue[3])], 0, 0, 0, 1), INK, LW * 1.2)
    ic.add('<path d="M1,-2H35" stroke="#fff" stroke-opacity=".75" stroke-width="1.2" stroke-linecap="round"/>')
    ic.add("</g>")
    # claw hammer, drawn upright (handle down, striking face right, claw left curling down) then turned
    # so the handle runs to the lower right
    t = "translate(23.5,26) rotate(-45) scale(1.06)"
    handle = "M-3.3,2H3.3V34Q3.3,37.6 0,37.6Q-3.3,37.6 -3.3,34Z"
    head = ("M-5,-6.5H5L6.2,-5H12.6L13.8,-6.4H16V5.4H13.8L12.6,4H6.2L5,5.6H-5V-1"
            "C-10,-.8 -14.6,2.2 -17.4,7.4L-16.4,4L-19.8,3.6C-16.8,-2.6 -11,-6.4 -5,-6.5Z")
    ic.shadow(handle, 2.4, 2, transform=t)
    ic.shadow(head, 2.4, 2, transform=t + " translate(0,1) scale(-.8,.8)")
    ic.add(f'<g transform="{t}">')
    ic.path(handle, ic.lg([(0, "#5a2806"), (.35, "#e0a060"), (.6, "#c07a38"), (1, "#5a2806")], 0, 0, 1, 0), INK, LW * 1.1)
    ic.add('<path d="M-1.4,8V33" stroke="#ffe0b0" stroke-opacity=".6" stroke-width="1" stroke-linecap="round"/>')
    ic.add('<g transform="translate(0,1) scale(-.8,.8)">')       # head smaller and turned round: claw up and to the right
    ic.path(head, ic.lg([(0, "#d9dce0"), (.4, "#8a9098"), (.75, "#4c5158"), (1, "#1e2024")], 0, 0, 0, 1), INK, LW * 1.3)   # dark steel head
    ic.add('<path d="M-4,-4.6H4.6M6.6,-3.2H12.4M-6,-5C-11,-4.6 -15,-1.6 -17.6,2.4" fill="none" stroke="#fff" stroke-opacity=".8" stroke-width="1.3" stroke-linecap="round"/>')
    ic.path("M14,-5.6H15.2V4.6H14Z", "#6c727a", None)
    ic.add("</g>")
    ic.add("</g>")


def headphones(ic):
    """Audio: a pair of headphones, grey band and black cushioned cups."""
    band = "M10,38V30A22,22 0 0 1 54,30V38"
    ic.add(f'<path d="{band}" fill="none" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>')
    ic.add(f'<path d="{band}" fill="none" stroke="#a8adb4" stroke-width="5" stroke-linecap="round"/>')
    ic.add('<path d="M13,30A19,19 0 0 1 32,11" fill="none" stroke="#fff" stroke-width="1.4" stroke-linecap="round"/>')
    for x, s in ((6, 1), (46, -1)):
        cup = rrect(x, 32, 12, 24, 5)
        ic.shadow(cup, 2.2, 1.8)
        ic.path(cup, ic.lg([(0, "#5c6168"), (1, "#0a0c10")], 0, 0, 1, 0), INK, LW)
        ic.path(rrect(x + 3 if s > 0 else x + 3, 36, 6, 16, 3), ic.lg([(0, "#e0281a"), (1, "#6a0804")]), INK, .8)


def mail_client(ic):
    """Mail client: KDE 3's KMail - an envelope standing in front of an orange letter tray."""
    for k in range(3):
        y = 20 + k * 10
        ic.path(f"M34,{y}L58,{y - 6}V{y + 4}L34,{y + 10}Z", ic.lg([(0, "#ffd890"), (.5, "#ec8a1a"), (1, "#8a4004")]), INK, 1.2)
    env = "M4,22L36,12L44,44L12,54Z"
    ic.shadow(env, 2.6, 2.2)
    ic.path(env, ic.lg([(0, "#ffffff"), (1, "#d9dce0")], 0, 0, 1, 1), INK, LW)
    ic.add(f'<path d="M4,22L26,36L36,12M12,54L22,34M44,44L28,32" fill="none" stroke="{INK}" stroke-width="1.1" stroke-linejoin="round"/>')


def mail_letterbox(ic):
    """Mail client (option A): a classic letterbox on a wooden post, red flag up, a letter in the door."""
    ic.path(rrect(27, 36, 8, 26, 1.4), ic.lg([(0, WOOD[2]), (.4, WOOD[0]), (1, WOOD[2])], 0, 0, 1, 0), INK, 1.2)
    body = "M6,22Q6,8 20,8H44Q58,8 58,22V40H6Z"
    ic.shadow(body, 2.6, 2.2)
    ic.path(body, ic.lg([(0, "#bfe0ff"), (.45, "#3a7ad0"), (1, "#123a7a")], 0, 0, .3, 1), INK, LW)
    ic.path("M6,22Q6,12 14,10Q22,12 22,22V40H6Z", ic.lg([(0, "#9fc8f0"), (1, "#1a4a8a")], 0, 0, 1, 0), INK, 1.2)   # door
    ic.add('<path d="M26,13H52" stroke="#fff" stroke-opacity=".5" stroke-width="2" stroke-linecap="round"/>')
    ic.path("M2,20L16,16V30L2,34Z", ic.lg([(0, "#ffffff"), (1, "#d9dce0")]), INK, 1.1)                 # letter
    ic.add(f'<path d="M2,20L9,26L16,16" fill="none" stroke="{INK}" stroke-width=".9"/>')
    ic.add(f'<path d="M50,30V6" stroke="{INK}" stroke-width="3.6" stroke-linecap="round"/>')
    ic.path("M50,4H62V13H50Z", ic.lg([(0, "#ffb0a0"), (.5, "#e0281a"), (1, "#6a0804")]), INK, 1.2)


def mail_at(ic):
    """Mail client (option B): an envelope with a blue @ stamped on it."""
    env = "M4,16H60V52H4Z"
    ic.shadow(env, 2.6, 2.2)
    ic.path(env, ic.lg([(0, "#ffffff"), (1, "#d9dce0")]), INK, LW * 1.2)
    ic.add(f'<path d="M4,16L32,36L60,16M4,52L24,31M60,52L40,31" fill="none" stroke="{INK}" stroke-width="1.2" stroke-linejoin="round"/>')
    at = ("M47,44A9,9 0 1 0 47.5,32.5M45.6,36.8A3.2,3.2 0 1 0 45.61,36.8ZM48.8,34V40.4Q48.8,42.6 51,42.6Q54,42.6 54,37"
          "A8,8 0 0 0 46,29")
    ic.path(circle(44, 38, 13), ic.rg([(0, "#ffffff"), (1, "#c8e0f8")]), INK, 1.4)
    ic.add('<path d="M48.6,34.6V40Q48.6,42.4 50.8,42.4Q53.6,42.4 53.6,37.6A9.6,9.6 0 1 0 49,46" fill="none" stroke="#1a4a9a" stroke-width="2.6" stroke-linecap="round"/>')
    ic.add('<circle cx="44.4" cy="37.6" r="4.2" fill="none" stroke="#1a4a9a" stroke-width="2.6"/>')


def web_browser(ic):
    """Web browser: KDE 3's Konqueror - the globe inside a silver gear."""
    pts = []
    for k in range(12):
        a = 2 * math.pi * k / 12
        for da, rad in ((-.14, 24), (-.08, 29), (.08, 29), (.14, 24)):
            pts.append((32 + rad * math.cos(a + da), 32 + rad * math.sin(a + da)))
    d = "M" + "L".join(f"{x:.2f},{y:.2f}" for x, y in pts) + "Z"
    ic.shadow(d, 2.6, 2.2)
    ic.path(d, ic.lg([(0, "#ffffff"), (.5, "#b4b9c0"), (1, "#5c6168")], 0, 0, 1, 1), INK, LW)
    e_globe(ic, 13, 13, 19)


def document_viewer(ic):
    """Document viewer: KDE 3's KGhostview - a page under a magnifying glass."""
    page = "M8,4H36L46,14V58H8Z"
    ic.shadow(page, 2.4, 2)
    ic.path(page, ic.lg([(0, "#ffffff"), (1, "#e2e4e8")]), INK, LW)
    ic.path("M36,4V14H46", "#d9dce0", INK, 1)
    for k in range(8):
        ic.add(f'<path d="M12,{18 + k * 4.4}H{40 - (k % 3) * 6}" stroke="#7b818a" stroke-width="1.2"/>')
    cx, cy, r = 38, 40, 10
    ic.add(f'<path d="M{cx + 7},{cy + 7}L{cx + 18},{cy + 18}" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>')
    ic.add(f'<path d="M{cx + 7},{cy + 7}L{cx + 18},{cy + 18}" stroke="#3c4148" stroke-width="5" stroke-linecap="round"/>')
    ic.path(circle(cx, cy, r + 2.6), ic.lg([(0, "#ffffff"), (1, "#7b818a")], 0, 0, 1, 1), INK, LW)
    ic.path(circle(cx, cy, r), ic.rg([(0, "#ffffff"), (1, "#bfe0f8")], .35, .3, .8), INK, 1, ' fill-opacity=".85"')
    ic.add(f'<path d="M{cx - 6},{cy - 2}H{cx + 6}M{cx - 6},{cy + 3}H{cx + 3}" stroke="#3c4148" stroke-width="1.8"/>')


def k_gear(ic):
    """The KDE 2/3 logo used for the K menu: white K over the cream gear with its golden centre.
    Shapes and colours are taken from KDE_2_logo.svg (Wikimedia Commons, LGPL) at 500 units, scaled to 64;
    its blur filter is replaced by the theme's stepped shadow and a dark outline is added to match the set."""
    gear = "m200 144-100-71-35 35 65 95-118 25v50l120 22-72 101 36 38 100-73 20 125h52l20-126 101 74 35-39-44-60v-48l89-14v-52l-100-17z"
    k = "m197 19v345l84-10v-147l115 160 83-26-112-158 115-145-90-23-111 150v-152z"
    t = "scale(.126) translate(4,8)"
    uid = ic.gid("kde")
    ic.defs.append(
        f'<radialGradient id="{uid}a" cx="170" cy="160" gradientUnits="userSpaceOnUse" r="220">'
        '<stop offset="0" stop-color="#fefef2"/><stop offset=".1" stop-color="#fefef2"/><stop offset=".3" stop-color="#fcfccd"/>'
        '<stop offset=".5" stop-color="#fcd99a"/><stop offset=".6" stop-color="#e4b573"/><stop offset=".75" stop-color="#cb9e60"/>'
        '<stop offset="1" stop-color="#c19553"/></radialGradient>'
        f'<linearGradient id="{uid}b" gradientUnits="userSpaceOnUse" x1="10" x2="300" y1="10" y2="400">'
        '<stop offset="0" stop-color="#fffff2"/><stop offset=".4" stop-color="#fffff2"/><stop offset="1" stop-color="#b1b3b2"/></linearGradient>'
        f'<linearGradient id="{uid}c" gradientUnits="userSpaceOnUse" x1="100" x2="300" y1="100" y2="400">'
        '<stop offset="0" stop-color="#6e6e6e"/><stop offset="1" stop-color="#373731"/></linearGradient>'
        f'<linearGradient id="{uid}d" gradientUnits="userSpaceOnUse" x1="200" x2="250" y1="200" y2="350">'
        '<stop offset="0" stop-color="#545450"/><stop offset="1" stop-color="#d9dade"/></linearGradient>'
        f'<linearGradient id="{uid}e" gradientUnits="userSpaceOnUse" x1="100" x2="250" y1="400" y2="350">'
        '<stop offset="0" stop-color="#c5b7aa"/><stop offset="1" stop-color="#fefdf9"/></linearGradient>')
    ring = "M78,254A165,165 0 1 0 408,254A165,165 0 1 0 78,254Z"
    ic.shadow(gear + ring, 22, 18, transform=t)
    ic.add(f'<g transform="{t}">')
    ic.add(f'<path d="{gear}" fill="url(#{uid}b)" stroke="{INK}" stroke-width="10" stroke-linejoin="round"/>')
    ic.add(f'<circle cx="243" cy="254" r="165" fill="url(#{uid}c)" stroke="{INK}" stroke-width="8"/>')
    ic.add(f'<circle cx="243" cy="254" r="158" fill="url(#{uid}b)"/>')
    ic.add(f'<circle cx="243" cy="254" r="135" fill="url(#{uid}d)"/>')
    ic.add(f'<circle cx="247" cy="269" r="120" fill="url(#{uid}e)"/>')
    ic.add(f'<circle cx="243" cy="254" r="123" fill="url(#{uid}a)"/>')
    ic.add("</g>")
    ic.shadow(k, 18, 15, transform=t)
    ic.add(f'<path transform="{t}" d="{k}" fill="#fff" stroke="{INK}" stroke-width="11" stroke-linejoin="round"/>')


def ladybird(ic):
    """Report a bug: KDE 3's red ladybird."""
    for s in (-1, 1):
        for k, y in enumerate((30, 40, 50)):
            ic.add(f'<path d="M{32 + s * 12},{y}L{32 + s * 24},{y - 4 + k * 4}" stroke="{INK}" stroke-width="2.4" stroke-linecap="round"/>')
        ic.add(f'<path d="M{32 + s * 4},12Q{32 + s * 8},4 {32 + s * 14},4" fill="none" stroke="{INK}" stroke-width="2.2" stroke-linecap="round"/>')
    ic.path("M22,20Q22,10 32,10Q42,10 42,20Z", ic.lg([(0, "#5c6168"), (1, "#0a0c10")]), INK, 1.2)
    body = "M32,18C46,18 52,30 50,42C48,54 40,58 32,58C24,58 16,54 14,42C12,30 18,18 32,18Z"
    ic.shadow(body, 2.6, 2.2)
    ic.path(body, ic.rg([(0, "#ffb0a0"), (.5, "#e0281a"), (1, "#6a0804")], .38, .3, .8), INK, LW)
    ic.add(f'<path d="M32,19V58" stroke="{INK}" stroke-width="1.8"/>')
    for x, y, r in ((23, 30, 3.4), (41, 30, 3.4), (21, 44, 3.6), (43, 44, 3.6), (28, 52, 2.6), (36, 52, 2.6)):
        ic.path(circle(x, y, r), INK, None)
    ic.add('<path d="M20,28Q22,22 28,21" fill="none" stroke="#fff" stroke-opacity=".7" stroke-width="2" stroke-linecap="round"/>')


# ------------------------------------------------------------------ sub-categories
def export(ic):
    """Export: a page with a green arrow leaving it."""
    page = "M6,4H32L42,14V58H6Z"
    ic.shadow(page, 2.4, 2)
    ic.path(page, ic.lg([(0, "#ffffff"), (1, "#e2e4e8")]), INK, LW)
    ic.path("M32,4V14H42", "#d9dce0", INK, 1)
    for k in range(7):
        ic.add(f'<path d="M10,{20 + k * 4.4}H{34 - (k % 3) * 5}" stroke="#7b818a" stroke-width="1.2"/>')
    a = "M26,36H44V28L60,42L44,56V48H26Z"
    ic.shadow(a, 2, 1.8)
    ic.path(a, ic.lg([(0, "#b8f0a0"), (.5, "#3fae2a"), (1, "#145a0c")]), INK, LW)


def brush(ic):
    """Painting: a paintbrush with a wooden handle, the bristles dipped in red."""
    ic.add('<g transform="rotate(40 32 32)">')
    ic.shadow("M28,4H36V40H28Z", 2.2, 1.8)
    ic.path("M28.5,4Q32,1 35.5,4V36H28.5Z", ic.lg([(0, WOOD[2]), (.4, WOOD[0]), (1, WOOD[2])], 0, 0, 1, 0), INK, 1.2)
    ic.path("M27,36H37V44H27Z", ic.lg([(0, METAL[2]), (.4, METAL[0]), (1, METAL[2])], 0, 0, 1, 0), INK, 1.2)
    ic.path("M27,44H37Q38,54 32,62Q26,54 27,44Z", ic.lg([(0, "#ffb0a0"), (.5, "#e0281a"), (1, "#6a0804")], 0, 0, 1, 0), INK, 1.2)
    ic.add("</g>")
    ic.add('<path d="M6,56Q14,50 20,54" fill="none" stroke="#e0281a" stroke-width="3.4" stroke-linecap="round"/>')


def freehand(ic):
    """Drawing: the orange pencil and the squiggle it has drawn."""
    ic.add('<path d="M6,54C12,40 20,58 26,46S36,30 42,42" fill="none" stroke="#2a6ac8" stroke-width="3.4" stroke-linecap="round"/>')
    ic.add('<g transform="rotate(40 40 30)">')
    ic.path("M34,2H46V40L40,50L34,40Z", ic.lg([(0, "#ffd08a"), (.5, "#f08a1a"), (1, "#a84c04")], 0, 0, 1, 0), INK, 1.3)
    ic.path("M34,40L40,50L46,40Z", "#f4d8b0", INK, 1)
    ic.path("M38.4,46.4L40,50L41.6,46.4Z", "#2a6ac8", None)
    ic.add("</g>")


def cuboid(ic):
    """3D graphics: a shaded cube with its hidden edges dashed."""
    T, R, F, L = (32, 6), (56, 18), (32, 30), (8, 18)
    dn = lambda p: (p[0], p[1] + 28)
    P = lambda *pts: "M" + "L".join(f"{a},{b}" for a, b in pts) + "Z"
    ic.shadow(P(T, R, dn(R), dn(F), dn(L), L), 2.6, 2.2)
    ic.add(f'<path d="M{L[0]},{L[1] + 28}L{T[0]},{T[1] + 28}L{R[0]},{R[1] + 28}M{T[0]},{T[1]}V{T[1] + 28}" fill="none" stroke="#7b818a" stroke-width="1" stroke-dasharray="2.4 2"/>')
    ic.path(P(L, F, dn(F), dn(L)), ic.lg([(0, "#9fd4ff"), (1, "#2a6ac8")], 0, 0, 1, 1), INK, 1.2, ' fill-opacity=".9"')
    ic.path(P(F, R, dn(R), dn(F)), ic.lg([(0, "#5a9ae0"), (1, "#0c2a6a")], 0, 0, 1, 1), INK, 1.2, ' fill-opacity=".9"')
    ic.path(P(T, R, F, L), ic.lg([(0, "#e8f6ff"), (1, "#8ac0f0")], 0, 0, 1, 1), INK, 1.2, ' fill-opacity=".9"')
    for p in (T, R, F, L, dn(R), dn(F), dn(L)):
        ic.path(rrect(p[0] - 2, p[1] - 2, 4, 4, .6), "#ffffff", INK, .9)


def interface(ic):
    """Interface (widgets): a small dialog with a checkbox, a slider and a button."""
    ic.shadow("M4,8H60V56H4Z", 2.6, 2.2)
    ic.path("M4,8H60V56H4Z", ic.lg([(0, "#f4f5f6"), (1, "#d9dce0")]), INK, LW)
    ic.path("M4,8H60V16H4Z", ic.lg([(0, "#9fc8f0"), (1, "#3a6ac0")]), INK, LW)
    ic.path("M10,21H18V29H10Z", "#ffffff", INK, 1.2)
    ic.add('<path d="M11.5,25L14,27.5L19.5,20" fill="none" stroke="#3fae2a" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>')
    ic.add('<path d="M23,25H50" stroke="#7b818a" stroke-width="2"/>')
    ic.add('<path d="M10,37H54" stroke="#5c6168" stroke-width="2.6" stroke-linecap="round"/>')
    ic.path(rrect(30, 32, 6, 10, 1.4), ic.lg([(0, "#ffffff"), (1, "#8a9098")], 0, 0, 1, 0), INK, 1)
    ic.path(rrect(32, 45, 22, 7, 2), ic.lg([(0, "#ffffff"), (1, "#a8adb4")]), INK, 1.1)
    ic.add('<path d="M37,48.5H49" stroke="#3c4148" stroke-width="1.4"/>')


def chat(ic):
    """Chat: two speech bubbles, yellow and blue."""
    a = "M6,8H38Q42,8 42,12V28Q42,32 38,32H18L10,40V32H6Q2,32 2,28V12Q2,8 6,8Z"
    b = "M26,26H58Q62,26 62,30V46Q62,50 58,50H54V58L46,50H26Q22,50 22,46V30Q22,26 26,26Z"
    for d, c in ((a, ("#fff8c0", "#e8c43a", "#8a6a06")), (b, ("#c8e8ff", "#5a9ae0", "#1a4a8a"))):
        ic.shadow(d, 2.2, 1.8)
        ic.path(d, ic.lg([(0, c[0]), (.6, c[1]), (1, c[2])], 0, 0, 0, 1), INK, LW)
    for x in (32, 42, 52):
        ic.path(circle(x, 38, 2.6), "#ffffff", INK, .7)


def astronomy(ic):
    """Astronomy: a night-sky disc with a crescent moon and yellow stars."""
    ic.shadow(circle(32, 32, 28), 2.6, 2.2)
    ic.path(circle(32, 32, 28), ic.rg([(0, "#3a4aa8"), (.7, "#141a50"), (1, "#060820")], .4, .35, .8), INK, LW)
    ic.path("M22,12A14,14 0 1 0 38,34A11,11 0 1 1 22,12Z", ic.lg([(0, "#fffbe0"), (1, "#e8c43a")]), INK, 1)
    for x, y, r in ((44, 18, 6), (48, 40, 4.4), (30, 48, 3.6), (40, 28, 2.6)):
        ic.path(_star(x, y, r, r * .42), ic.rg([(0, "#ffffff"), (1, "#ffd21a")]), INK, .8)


CATEGORIES = {
    "applications-development": development, "applications-engineering": engineering, "applications-science": science, "applications-education-science": physics,
    "applications-education": education, "applications-education-mathematics": mathematics,
    "applications-games": games, "applications-games-arcade": arcade, "applications-games-board": board,
    "applications-games-card": cards, "applications-games-strategy": strategy, "applications-internet": internet,
    "applications-office": office, "applications-utilities": utilities, "audio-headphones": headphones,
    "internet-mail": mail_letterbox, "internet-web-browser": web_browser, "graphics-viewer-document": document_viewer,
    "plasma": k_gear, "tools-report-bug": ladybird, "document-export": export, "draw-brush": brush,
    "draw-freehand": freehand, "draw-cuboid": cuboid, "interface": interface, "kopete": chat, "kstars_stars": astronomy,
}
CATEGORY_ALIASES = {
    "applications-education-language": "applications-education",
    "applications-education-miscellaneous": "applications-education", "applications-games-logic": "applications-games-board",
    "applications-games-puzzle": "applications-games-board", "applications-system": "applications-utilities",
    "start-here-kde": "plasma", "start-here-kde-plasma": "plasma", "kde": "plasma", "start-here": "plasma",
    "start-here-kde-symbolic": "plasma", "start-here-kde-plasma-symbolic": "plasma", "start-here-symbolic": "plasma",
    "kmenu": "plasma", "plasmashell": "plasma", "kde-symbolic": "plasma", "bug": "tools-report-bug",
    "internet-chat": "kopete", "im-user": "kopete", "kstars": "kstars_stars", "konqueror": "internet-web-browser",
    "kmail": "internet-mail", "okular": "graphics-viewer-document", "draw-cube": "draw-cuboid",
}
# names that point at drawings in another folder of the theme
CROSS = {"preferences-devices-scanner": "../devices/scanner.svg",  # document-share: own drawing in apps2 (2026-10-27)
         "globe": "../places/globe.svg"}


# ------------------------------------------------------------------ app page, sources and updates
GOLD = ("#fffbe0", "#ffd21a", "#c87a04")
GREY = ("#ffffff", "#c3c7cd", "#6c727a")


def _rating(ic, part):
    """Rating stars, drawn bold for the 16 px row on an app page: full, half (either way) or empty."""
    d = _star(32, 34, 29, 12.5)
    if part == "none":
        ic.path(d, ic.rg([(0, GREY[0]), (.5, GREY[1]), (1, GREY[2])], .45, .4, .7), INK, 2.4)
        return
    if part == "full":
        ic.path(d, ic.rg([(0, GOLD[0]), (.45, GOLD[1]), (1, GOLD[2])], .45, .4, .7), INK, 2.4)
        return
    # the star is symmetric about x = 32 (top tip and bottom inner corner), so each half is exact, no clipping
    pts = d[1:-1].split("L")
    left = [pts[0]] + pts[5:10][::-1] if False else pts[5:10] + [pts[0]]
    right = pts[0:6]
    ic.path(d, ic.rg([(0, GREY[0]), (.5, GREY[1]), (1, GREY[2])], .45, .4, .7), None)
    gold = left if part == "half" else right
    ic.path("M" + "L".join(gold) + "Z", ic.rg([(0, GOLD[0]), (.45, GOLD[1]), (1, GOLD[2])], .45, .4, .7), None)
    ic.add(f'<path d="M32,5V46.5" stroke="{INK}" stroke-width="1"/>')
    ic.path(d, "none", INK, 2.4)


def rating(ic): _rating(ic, "full")
def rating_half(ic): _rating(ic, "half")
def rating_half_rtl(ic): _rating(ic, "half-rtl")
def rating_unrated(ic): _rating(ic, "none")


UPD = {"high": ("#ffb0a0", "#e0281a", "#6a0804"), "medium": ("#ffe8a0", "#ec9a1a", "#7a4404"),
       "low": ("#b8dcff", "#2a6ac8", "#0c2a6a"), "none": ("#c8f8a8", "#3fae2a", "#145a0c")}


def _update(ic, level):
    """Update priority, as KDE Classic: a glossy round disc with a white down arrow (red, orange, blue),
    or a green tick when up to date."""
    from dolphin import badge
    colour = {"high": "red", "medium": "amber", "low": "blue", "none": "green"}[level]
    badge(ic, colour, "M19,33L28,42L45,23" if level == "none" else "M32,16V45M21,35L32,46L43,35")


def update_high(ic): _update(ic, "high")
def update_medium(ic): _update(ic, "medium")
def update_low(ic): _update(ic, "low")
def update_none(ic): _update(ic, "none")


def _up_badge(ic, x=47, y=47, r=12):
    ic.shadow(circle(x, y, r), 2, 1.8)
    ic.path(circle(x, y, r), ic.rg([(0, "#ffe8a0"), (.55, "#ec9a1a"), (1, "#7a4404")], .4, .32, .8), INK, 1.6)
    g = f"M{x},{y - 6.5}V{y + 6}M{x - 5.5},{y + .5}L{x},{y + 6.5}L{x + 5.5},{y + .5}"     # down arrow
    ic.add(f'<path d="{g}" fill="none" stroke="#000" stroke-opacity=".3" stroke-width="5.4" stroke-linecap="round" stroke-linejoin="round"/>')
    ic.add(f'<path d="{g}" fill="none" stroke="#fff" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"/>')


def parcel(ic):
    """Package: KDE 3's kpackage parcel - a tall cardboard box tied with string both ways, a bow on top."""
    P = lambda *pts: "M" + "L".join(f"{a:.2f},{b:.2f}" for a, b in pts) + "Z"
    w, h = 20, 28
    T, R, F, L = (32, 6), (32 + w, 6 + w / 2), (32, 6 + w), (32 - w, 6 + w / 2)
    dn = lambda p: (p[0], p[1] + h)
    mid = lambda a, b, t=.5: (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
    ic.shadow(P(T, R, dn(R), dn(F), dn(L), L), 2.8, 2.4)
    ic.path(P(L, F, dn(F), dn(L)), ic.lg([(0, "#fbf2c4"), (1, "#cdb468")]), INK, 1.3)
    ic.path(P(F, R, dn(R), dn(F)), ic.lg([(0, "#d8c070"), (1, "#8a7430")]), INK, 1.3)
    ic.path(P(T, R, F, L), ic.lg([(0, "#fffbe4"), (1, "#e8d690")], 0, 0, 1, 1), INK, 1.3)
    # string: round the middle of each face and across the top both ways
    a, b = mid(L, T), mid(F, R)
    c, d = mid(T, R), mid(L, F)
    lines = [(a, b), (c, d),                                                   # across the top
             (d, dn(d)), (b, dn(b)),                                             # down the two near faces
             (mid(L, dn(L)), mid(F, dn(F))), (mid(F, dn(F)), mid(R, dn(R)))]    # round the middle
    for p0, p1 in lines:
        ic.add(f'<path d="M{p0[0]:.2f},{p0[1]:.2f}L{p1[0]:.2f},{p1[1]:.2f}" stroke="#5a3a10" stroke-width="2.4" stroke-linecap="round"/>')
        ic.add(f'<path d="M{p0[0]:.2f},{p0[1]:.2f}L{p1[0]:.2f},{p1[1]:.2f}" stroke="#c89a50" stroke-width="1" stroke-linecap="round"/>')
    # bow on top
    cx, cy = mid(T, F)
    for sx in (-1, 1):
        loop = f"M{cx},{cy}C{cx + sx * 4},{cy - 8} {cx + sx * 10},{cy - 6} {cx + sx * 7},{cy - 1}C{cx + sx * 5},{cy + 1} {cx + sx * 2},{cy} {cx},{cy}Z"
        ic.path(loop, ic.lg([(0, "#ffd890"), (1, "#a86a1a")]), "#5a3a10", 1.1)
    for sx in (-1, 1):
        ic.add(f'<path d="M{cx},{cy}L{cx + sx * 4},{cy + 6}" stroke="#5a3a10" stroke-width="2.2" stroke-linecap="round"/>'
               f'<path d="M{cx},{cy}L{cx + sx * 4},{cy + 6}" stroke="#e0a860" stroke-width=".9" stroke-linecap="round"/>')
    ic.path(circle(cx, cy, 1.8), "#c89a50", "#5a3a10", .9)


def system_upgrade(ic):
    """System upgrade: the cardboard package with an amber up-arrow badge."""
    from filetypes import box
    ic.add('<g transform="translate(-4,2)">')
    box(ic, 6, 10, 20, 24)
    ic.add("</g>")
    _up_badge(ic)


def reboot_update(ic):
    """Restart to update: the green restart tile from the Leave screen with the update badge."""
    import session
    ic.add('<g transform="translate(-2,-2) scale(.86)">')
    session.reboot(ic, False)
    ic.add("</g>")
    _up_badge(ic)


def shutdown_update(ic):
    """Shut down after updating: the red power tile with the update badge."""
    import session
    ic.add('<g transform="translate(-2,-2) scale(.86)">')
    session.power(ic, False)
    ic.add("</g>")
    _up_badge(ic)


def download(ic):
    """Download: a fat green arrow dropping into a grey tray."""
    tray = "M4,42H18L22,48H42L46,42H60V58H4Z"
    ic.shadow(tray, 2.4, 2)
    ic.path(tray, ic.lg([(0, "#e4e6e9"), (1, "#7b818a")]), INK, LW * 1.3)
    a = "M24,4H40V24H50L32,44L14,24H24Z"
    ic.shadow(a, 2.4, 2)
    ic.path(a, ic.lg([(0, "#c8f8a8"), (.5, "#3fae2a"), (1, "#145a0c")]), INK, LW * 1.3)
    ic.add('<path d="M26,7H38" stroke="#fff" stroke-opacity=".6" stroke-width="1.6"/>')


def jigsaw(ic):
    """Extensions / add-ons: a green jigsaw piece."""
    d = ("M10,18H24A6,6 0 1 1 36,18H50V30A6,6 0 1 0 50,42V54H36A6,6 0 1 1 24,54H10V42A6,6 0 1 0 10,30Z")
    ic.shadow(d, 2.6, 2.2)
    ic.path(d, ic.lg([(0, "#c8f8a8"), (.5, "#3fae2a"), (1, "#145a0c")], 0, 0, 1, 1), INK, LW * 1.3)
    ic.add('<path d="M13,21H22M13,24V30" stroke="#fff" stroke-opacity=".55" stroke-width="1.6" stroke-linecap="round"/>')


def handbook(ic):
    """Documentation: an open blue handbook."""
    l, r = "M32,14Q20,6 4,10V54Q20,50 32,58Z", "M32,14Q44,6 60,10V54Q44,50 32,58Z"
    ic.shadow(l + r, 2.6, 2.2)
    for d in (l, r):
        ic.path(d, ic.lg([(0, "#ffffff"), (1, "#e2e4e8")]), INK, LW)
    for k in range(6):
        y = 18 + k * 6
        ic.add(f'<path d="M9,{y - 1}Q19,{y - 4} 28,{y + 2}M36,{y + 2}Q45,{y - 4} 55,{y - 1}" fill="none" stroke="#7b818a" stroke-width="1.1"/>')
    ic.path("M30,12Q32,10 34,12V58Q32,60 30,58Z", ic.lg([(0, "#5a9ae0"), (1, "#1a4a8a")], 0, 0, 1, 0), INK, 1)
    ic.add('<path d="M4,54Q20,50 32,58Q44,50 60,54V58Q44,54 32,62Q20,54 4,58Z" fill="#2a6ac8" stroke="#141414" stroke-width="1.2"/>')


def donate(ic):
    """Donate: a gold coin with a red heart on it."""
    ic.shadow(circle(32, 32, 27), 2.6, 2.2)
    ic.path(circle(32, 32, 27), ic.rg([(0, "#fffbe0"), (.5, "#f0c020"), (1, "#a86404")], .4, .35, .8), INK, LW * 1.3)
    ic.path(circle(32, 32, 21.5), "none", "#a86404", 1.4)
    h = "M32,46C18,37 18,22 26,22C29,22 31,24 32,27C33,24 35,22 38,22C46,22 46,37 32,46Z"
    ic.path(h, ic.rg([(0, "#ffb0a0"), (.55, "#e0281a"), (1, "#6a0804")], .4, .3, .8), INK, 1.4)


def paper_plane(ic):
    """Send: a white paper plane in flight."""
    ic.add('<path d="M4,52Q14,48 18,40" fill="none" stroke="#7b818a" stroke-width="1.6" stroke-dasharray="3 2.4"/>')
    top = "M60,6L4,30L22,36Z"
    ic.shadow("M60,6L4,30L22,36L28,56L36,42L48,50Z", 2.4, 2)
    ic.path("M60,6L22,36L28,56L32,40Z", ic.lg([(0, "#c9ccd1"), (1, "#7b818a")]), INK, 1.3)
    ic.path(top, ic.lg([(0, "#ffffff"), (1, "#e4e6e9")]), INK, 1.3)
    ic.path("M60,6L32,40L48,50Z", ic.lg([(0, "#ffffff"), (1, "#c9ccd1")]), INK, 1.3)


def file_search(ic):
    """Find a file: a big magnifier over a small dog-eared page."""
    page = "M26,4H44L52,12V40H26Z"
    ic.shadow(page, 2, 1.8)
    ic.path(page, ic.lg([(0, "#ffffff"), (1, "#e2e4e8")]), INK, 1.2)
    ic.path("M44,4V12H52", "#d9dce0", INK, .9)
    for k in range(4):
        ic.add(f'<path d="M30,{17 + k * 5}H{46 - (k % 2) * 6}" stroke="#7b818a" stroke-width="1.1"/>')
    cx, cy, r = 24, 36, 13
    ic.add(f'<path d="M{cx - 9},{cy + 9}L{cx - 19},{cy + 19}" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>')
    ic.add(f'<path d="M{cx - 9},{cy + 9}L{cx - 19},{cy + 19}" stroke="#8a5a2a" stroke-width="6" stroke-linecap="round"/>')
    ic.path(circle(cx, cy, r + 3), ic.lg([(0, "#ffffff"), (1, "#7b818a")], 0, 0, 1, 1), INK, LW)
    ic.path(circle(cx, cy, r), ic.rg([(0, "#e8f6ff"), (1, "#9ad0f0")], .35, .3, .8), INK, 1, ' fill-opacity=".85"')
    ic.add(f'<path d="M{cx - 7},{cy - 2}Q{cx - 6},{cy - 7} {cx - 1},{cy - 8}" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round"/>')


def sort_name(ic):
    """Sort by name: A to Z with a right arrow underneath."""
    for d, col in (("M6,30L14,8L22,30M9.4,22H18.6", "#2a3ae8"), ("M42,8H58L42,30H58", "#e0281a")):
        ic.add(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>')
        ic.add(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>')
    ic.add(f'<path d="M8,48H54M46,40L56,48L46,56" fill="none" stroke="{INK}" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"/>')


def text_unflow(ic):
    """Show less: lines of text drawing together under an up chevron."""
    ic.shadow("M6,30H58V58H6Z", 2.4, 2)
    ic.path("M6,30H58V58H6Z", ic.lg([(0, "#ffffff"), (1, "#eceef1")]), INK, LW)
    for k in range(3):
        ic.add(f'<path d="M12,{38 + k * 7}H{52 - (k == 2) * 16}" stroke="#5c6168" stroke-width="2.2" stroke-linecap="round"/>')
    g = "M18,22L32,8L46,22"
    ic.add(f'<path d="{g}" fill="none" stroke="{INK}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>')
    ic.add(f'<path d="{g}" fill="none" stroke="#2a6ac8" stroke-width="4.6" stroke-linecap="round" stroke-linejoin="round"/>')


def _classic_window(ic):
    ic.shadow("M4,8H60V58H4Z", 2.6, 2.2)
    ic.path("M4,8H60V58H4Z", ic.lg([(0, "#fffef4"), (1, "#fff4c4")], 0, 0, 1, 1), INK, LW * 1.3)
    ic.path("M4,8H60V18H4Z", ic.lg([(0, "#e4e6e9"), (1, "#8a9098")]), INK, LW * 1.3)


def _corner_arrows(ic, out):
    for sx, sy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        cx, cy = 32 + sx * 13, 38 + sy * 11
        if out:
            tip, b1, b2 = (cx + sx * 6, cy + sy * 6), (cx + sx * 6, cy - sy * 2), (cx - sx * 2, cy + sy * 6)
            tail = (cx - sx * 5, cy - sy * 5)
        else:
            tip, b1, b2 = (cx - sx * 5, cy - sy * 5), (cx - sx * 5, cy + sy * 3), (cx + sx * 3, cy - sy * 5)
            tail = (cx + sx * 6, cy + sy * 6)
        ic.add(f'<path d="M{tail[0]},{tail[1]}L{(tip[0] + tail[0]) / 2},{(tip[1] + tail[1]) / 2}" stroke="#8a1404" stroke-width="3.2" stroke-linecap="round"/>')
        ic.path(f"M{tip[0]},{tip[1]}L{b1[0]},{b1[1]}L{b2[0]},{b2[1]}Z", "#8a1404", None)


def maximize(ic):
    """Maximise: KDE Classic's window with dark red arrows pointing out to the corners."""
    _classic_window(ic)
    _corner_arrows(ic, True)


def restore(ic):
    """Restore: the same window with the arrows pointing back in."""
    _classic_window(ic)
    _corner_arrows(ic, False)


def offline(ic):
    """Offline: a grey globe with a red cross badge."""
    ic.add("<g>")
    cx, cy, r = 28, 28, 24
    ic.shadow(circle(cx, cy, r), 2.6, 2.2)
    ic.path(circle(cx, cy, r), ic.rg([(0, "#ffffff"), (.5, "#a8adb4"), (1, "#4c5158")], .35, .3, .8), INK, LW)
    ic.add(f'<path d="M{cx - r},{cy}H{cx + r}M{cx},{cy - r}V{cy + r}M{cx - r * .86},{cy - r * .5}Q{cx},{cy - r * .2} {cx + r * .86},{cy - r * .5}'
           f'M{cx - r * .86},{cy + r * .5}Q{cx},{cy + r * .2} {cx + r * .86},{cy + r * .5}" fill="none" stroke="#5c6168" stroke-width="1.1"/>')
    ic.add(f'<path d="M{cx},{cy - r}Q{cx - r * .7},{cy} {cx},{cy + r}M{cx},{cy - r}Q{cx + r * .7},{cy} {cx},{cy + r}" fill="none" stroke="#5c6168" stroke-width="1.1"/>')
    ic.add("</g>")
    ic.shadow(circle(47, 47, 13), 2, 1.8)
    ic.path(circle(47, 47, 13), ic.rg([(0, "#ffb0a0"), (.55, "#e0281a"), (1, "#6a0804")], .4, .32, .8), INK, 1.6)
    ic.add('<path d="M41.5,41.5L52.5,52.5M52.5,41.5L41.5,52.5" stroke="#fff" stroke-width="3.6" stroke-linecap="round"/>')


def emblem_error(ic):
    """Error: a red round badge with a white cross, in the version-control badge style."""
    from dolphin import badge
    badge(ic, "red", "M21,21L43,43M43,21L21,43")


def broom(ic):
    """Remove unused packages: a broom sweeping."""
    ic.add('<g transform="translate(2,-1) scale(.84) rotate(-35 32 32)">')       # kept inside the canvas
    ic.path(rrect(29.5, 0, 5, 38, 2.4), ic.lg([(0, WOOD[2]), (.4, WOOD[0]), (1, WOOD[2])], 0, 0, 1, 0), INK, 1.2)
    ic.path("M24,36H40L44,40H20Z", ic.lg([(0, "#e0281a"), (1, "#6a0804")]), INK, 1.1)
    b = "M20,40H44L50,62H14Z"
    ic.shadow(b, 2.2, 1.8)
    ic.path(b, ic.lg([(0, "#fff0a0"), (.5, "#e8c43a"), (1, "#a8840e")]), INK, LW)
    for x in (22, 27, 32, 37, 42):
        ic.add(f'<path d="M{x},43L{x + (x - 32) * .3},60" stroke="#a8840e" stroke-width="1"/>')
    ic.add("</g>")
    for x, y in ((48, 52), (54, 49), (53, 56)):
        ic.path(circle(x, y, 1.6), "#9aa0a8", None)


def sim_card(ic):
    """Smart card / SIM access: a white SIM card with its gold contact chip."""
    card = "M14,4H42L52,14V58H14Z"
    ic.shadow(card, 2.6, 2.2)
    ic.path(card, ic.lg([(0, "#ffffff"), (1, "#c9ccd1")], 0, 0, 1, 1), INK, LW * 1.3)
    ic.path(rrect(21, 24, 24, 26, 3), ic.lg([(0, "#fff3a6"), (.5, "#e8c43a"), (1, "#8a6a06")], 0, 0, 1, 1), INK, 1.2)
    ic.add(f'<path d="M21,33H30V24M45,33H36V24M21,41H30V50M45,41H36V50M30,33H36V41H30Z" fill="none" stroke="#7a5a04" stroke-width="1"/>')


def virtualisation(ic):
    """Virtual machines: a monitor showing a smaller monitor inside it."""
    ic.shadow(rrect(4, 4, 56, 42, 3) + "M24,44H40L43,56H21Z", 3, 2.6)
    ic.path("M18,52Q18,50 20,50H44Q46,50 46,52V58H18Z", ic.lg([(0, "#e8e4d8"), (1, "#8a877c")]), INK, LW)
    ic.path("M26,45H38L40,50.5H24Z", ic.lg([(0, "#d9d5c8"), (1, "#8a877c")]), INK, LW)
    ic.path(rrect(4, 4, 56, 42, 3), ic.lg([(0, "#fbf9f2"), (1, "#b4b0a3")], 0, 0, .3, 1), INK, LW)
    ic.path(rrect(9, 9, 46, 32, 1.6), ic.lg([(0, "#3a6fd8"), (.6, "#1a3ea8"), (1, "#0c2470")]), INK, 1)
    ic.path(rrect(20, 13, 24, 18, 1.4), ic.lg([(0, "#fbf9f2"), (1, "#b4b0a3")]), INK, 1)
    ic.path("M23,16H41V28H23Z", ic.lg([(0, "#b4f0a0"), (1, "#2f8a2e")]), INK, .7)
    ic.path("M27,31H37L38,35H26Z", "#d9d5c8", INK, .8)


PAGE = {"rating": rating, "rating-half": rating_half, "rating-half-rtl": rating_half_rtl, "rating-unrated": rating_unrated,
        "update-high": update_high, "update-medium": update_medium, "update-low": update_low, "update-none": update_none,
        "system-upgrade": system_upgrade, "system-reboot-update": reboot_update, "system-shutdown-update": shutdown_update,
        "download": download, "extension-symbolic": jigsaw, "documentation-symbolic": handbook,
        "help-donate-symbolic": donate, "document-send": paper_plane, "file-search-symbolic": file_search,
        "sort-name": sort_name, "text-unflow": text_unflow, "window-maximize": maximize, "window-restore": restore,
        "offline": offline, "run-build-prune-symbolic": broom, "auth-sim-symbolic": sim_card,
        "virt-manager-symbolic": virtualisation, "package": parcel}
PAGE_ALIASES = {"rating-symbolic": "rating", "state-download": "download", "download-symbolic": "download",
                "system-upgrade-symbolic": "system-upgrade", "plugins-symbolic": "extension-symbolic",
                "plugins": "extension-symbolic", "extension": "extension-symbolic", "documentation": "documentation-symbolic",
                "help-donate": "help-donate-symbolic", "network-offline": "offline", "update-medium-symbolic": "update-medium",
                "virt-manager": "virt-manager-symbolic", "auth-sim": "auth-sim-symbolic", "document-send-symbolic": "document-send",
                "snap": "package", "kpackage": "package", "package-symbolic": "package"}
PAGE_CROSS = {"favorite": "../emblems/starred.svg",
              "drive-harddisk-root-symbolic": "../devices/drive-harddisk.svg", "x-shape-connection-symbolic": "../apps/xorg.svg",
}
EMBLEMS = {"emblem-error": emblem_error}


def write(out):
    d = f"{out}/scalable/apps"
    os.makedirs(d, exist_ok=True)
    for name, fn in CATEGORIES.items():
        open(f"{d}/{name}.svg", "w").write(_ic(fn)().svg(64))
    for a, t in CATEGORY_ALIASES.items():
        if not os.path.exists(f"{d}/{a}.svg"):
            os.symlink(f"{t}.svg", f"{d}/{a}.svg")
    for a, t in CROSS.items():
        if not os.path.exists(f"{d}/{a}.svg"):
            os.symlink(t, f"{d}/{a}.svg")
    d = f"{out}/scalable/actions"
    for name, fn in PAGE.items():
        open(f"{d}/{name}.svg", "w").write(_ic(fn)().svg(64))
    for a, t in PAGE_ALIASES.items():
        if not os.path.exists(f"{d}/{a}.svg"):
            os.symlink(f"{t}.svg", f"{d}/{a}.svg")
    for a, t in PAGE_CROSS.items():
        if not os.path.exists(f"{d}/{a}.svg"):
            os.symlink(t, f"{d}/{a}.svg")
    d = f"{out}/scalable/emblems"
    for name, fn in EMBLEMS.items():
        open(f"{d}/{name}.svg", "w").write(_ic(fn)().svg(64))
    return len(CATEGORIES) + len(PAGE) + len(EMBLEMS)
