"""KDE Classic Vector: file types (drawn from the KDE Classic 64 px originals, see STYLE.md).

Every file type is the classic page (cream gradient, folded top-right corner) with an emblem that
overlaps it on the left, as in the originals. Brand logos in the originals (Acrobat, Debian, RPM)
are replaced by generic emblems.
"""
import math
from gen import Icon, INK, LW, circle, rrect, e_globe, e_speaker
from devices import frame, poly, rpoly, rounded, disc, strokes

PAGE = "M16.5,1H44L58,15V58H16.5Z"
FOLD = "M44,1V13.2Q44,15 45.8,15H58Z"
TEXT = "#6c6458"


def page(ic, x0=None):
    ic.shadow(PAGE, 2.8, 2.4)
    ic.path(PAGE, ic.lg([(0, "#ffffff"), (.42, "#fcf8f0"), (1, "#d9b688")], 0, 0, 1, 1), INK, 1.2)
    ic.add('<path d="M18.2,56.4V2.7H43.3" fill="none" stroke="#fff" stroke-width="1.1"/>')
    ic.path(FOLD, ic.lg([(0, "#ffffff"), (.6, "#eeeae4"), (1, "#bdb5a8")], 0, 0, 1, 1), INK, 1)


def lines(ic, x0, x1, y0, n, gap=3.2, col=TEXT, w=1.1, pattern=(1, .92, 1, .8, .96, .6), breaks=()):
    y, out = y0, []
    for k in range(n):
        if k in breaks:
            y += gap * .7
        L = (x1 - x0) * pattern[k % len(pattern)]
        out.append(f"M{x0},{y:.1f}H{x0 + L:.1f}")
        y += gap
    ic.add(f'<path d="{"".join(out)}" stroke="{col}" stroke-width="{w}"/>')


def ticks(ic):
    """The dashed edge the originals draw down the right of info and message pages."""
    ic.add('<path d="M54.5,19V55" stroke="#b4a890" stroke-width="1.4" stroke-dasharray="2.4 1.6"/>')


def mime(*emblems):
    def f():
        ic = Icon()
        page(ic)
        for e in emblems:
            e(ic)
        return ic
    return f


# ------------------------------------------------------------------ page contents
def m_lines(ic):
    lines(ic, 21, 52, 20, 11, breaks=(5,))


def m_document(ic):
    ic.add(f'<path d="M21,8.5H38" stroke="{TEXT}" stroke-width="1.8"/>')
    lines(ic, 21, 53, 19, 11, gap=3.1, breaks=(4, 8))
    ic.add(f'<path d="M36,54.5H39" stroke="{TEXT}" stroke-width="1.2"/>')


def m_binary(ic):
    """Columns of 0 and 1, as in the original binary page."""
    rows = [("0",), ("1",), ("0", "1", "0"), ("1", "0", "1"), ("", "1", "1")]
    out = []
    for r, row in enumerate(rows):
        y = 11 + r * 9.6
        for c, ch in enumerate(row):
            x = 25 + c * 10 + (r == 4 and c == 2) * 4
            if ch == "0":
                out.append(f"M{x},{y - 3.6}A2.6,3.6 0 1 0 {x},{y + 3.6}A2.6,3.6 0 1 0 {x},{y - 3.6}Z")
            elif ch == "1":
                out.append(f"M{x - 2},{y - 2.2}L{x},{y - 3.6}V{y + 3.6}M{x - 2.2},{y + 3.6}H{x + 2.2}")
    ic.add(f'<path d="{"".join(out)}" fill="none" stroke="{TEXT}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>')


def m_source(ic):
    """Hollow dots in indented rows: the original's picture of source code."""
    rows = [(0, 1), (0, 1), (1, 2, 3), (0, 1, 3), (0, 1, 2), (0, 2, 3)]
    for r, row in enumerate(rows):
        for c in row:
            x, y = 25.6 + c * 8, 9 + r * 7.6
            if y < 16 and x > 40:
                continue
            ic.path(circle(x, y, 2.3), ic.rg([(0, "#ffffff"), (1, "#e4ddd0")]), TEXT, 1.1)


# ------------------------------------------------------------------ emblems
def e_pencil(ic):
    """The original's big orange pencil, lying from the upper left with its point toward the page centre."""
    f = frame(5.5, 6, 47)
    w, L, b, c = 5, 54, 42, 50.5          # half width, length, where the wood starts, where the lead starts
    outline = [(0, -w), (b, -w), (c, -1.4), (L, 0), (c, 1.4), (b, w), (0, w)]
    ic.shadow(poly(f, outline), 2.6, 2.2)
    ic.path(poly(f, [(0, -w), (6, -w), (6, w), (0, w)]), ic.lg([(0, "#ffc4c8"), (1, "#d86a78")]), INK, 1)
    ic.path(poly(f, [(6, -w), (11.5, -w), (11.5, w), (6, w)]), ic.lg([(0, "#ffffff"), (.5, "#b4b9c0"), (1, "#6c727a")], 0, 0, 1, 0), INK, 1)
    for x in (7.8, 9.7):
        ic.add(f'<path d="{poly(f, [(x, -w), (x, w)], False)}" stroke="#6c727a" stroke-width=".7"/>')
    ic.path(poly(f, [(11.5, -w), (b, -w), (b, -1.6), (11.5, -1.6)]), "#ffc070", None)
    ic.path(poly(f, [(11.5, -1.6), (b, -1.6), (b, 1.6), (11.5, 1.6)]), "#f28a1c", None)
    ic.path(poly(f, [(11.5, 1.6), (b, 1.6), (b, w), (11.5, w)]), "#b85a0c", None)
    ic.add(f'<path d="{poly(f, [(11.5, -1.6), (b, -1.6)], False)}{poly(f, [(11.5, 1.6), (b, 1.6)], False)}" stroke="#8a4008" stroke-opacity=".5" stroke-width=".6"/>')
    ic.path(poly(f, [(b, -w), (c, -1.4), (c, 1.4), (b, w)]), ic.lg([(0, "#fbe2b8"), (1, "#c8965c")]), INK, 1)
    ic.path(poly(f, [(c, -1.4), (L, 0), (c, 1.4)]), "#2c3036", INK, .8)
    ic.path(poly(f, outline), "none", INK, LW)


def e_paint(ic):
    """Three paint drops (red, blue, green) above a white block with a paint run: image files."""
    blk = "M1.5,33Q1.5,30.5 4,30.5H35.5Q38,30.5 38,33V43Q38,45.5 35.5,45.5H4Q1.5,45.5 1.5,43Z"
    ic.shadow(blk, 2.6, 2.2)
    ic.path(blk, ic.lg([(0, "#ffffff"), (.55, "#dfe2e6"), (1, "#8a9098")]), INK, LW)
    ic.path("M3.5,31.5H11V40Q11,44 8,44Q5.5,44 5,40Q4.5,37 3.5,36Z", ic.lg([(0, "#ff7060"), (1, "#b8180c")]), None)
    for cx, col in ((8, ("#ff9a8a", "#e02414", "#8a0c04")), (20, ("#9ad0ff", "#1a6ae0", "#0a3478")), (31.5, ("#b4f0a0", "#2f9a2e", "#14561a"))):
        d = f"M{cx},33C{cx + 6.5},28 {cx + 6.8},20 {cx + 3.6},15.5Q{cx},11 {cx - 3.6},15.5C{cx - 6.8},20 {cx - 6.5},28 {cx},33Z"
        ic.path(d, ic.rg([(0, col[0]), (.55, col[1]), (1, col[2])], .38, .3, .8), INK, LW)
        ic.add(f'<path d="M{cx - 3},{18}Q{cx - 3.4},{22} {cx - 2.2},{25}" fill="none" stroke="#fff" stroke-opacity=".75" stroke-width="1.4" stroke-linecap="round"/>')


def e_audio(ic):
    e_speaker(ic, cx=25, cy=30, ry=19.5)


def e_film_strip(ic):
    f = frame(30, 33, 45)
    strip = [(-46, -9), (46, -9), (46, 9), (-46, 9)]
    ic.shadow(poly(f, strip), 2.6, 2.2)
    ic.path(poly(f, strip), ic.lg([(0, "#3a3f46"), (1, "#0a0c0e")], 0, 0, 1, 1), INK, LW)
    for k in range(-11, 12):
        x = k * 4
        for y in (-7.6, 5.4):
            ic.add(f'<path d="{poly(f, [(x - 1.1, y), (x + 1.1, y), (x + 1.1, y + 2.2), (x - 1.1, y + 2.2)])}" fill="#f4f4f4"/>')
    for k in (-2, -1, 0, 1, 2):
        x = k * 15
        ic.path(poly(f, [(x - 6.6, -4.4), (x + 6.6, -4.4), (x + 6.6, 4.4), (x - 6.6, 4.4)]),
                ic.lg([(0, "#fff0b0"), (.4, "#e0b440"), (.7, "#a8780c"), (1, "#f0d070")], 0, 0, 1, 1), "#000", .6)


def e_html(ic):
    e_globe(ic, 2, 11, 19)


def e_terminal(ic):
    ic.shadow(rrect(3, 14, 37, 31, 2.5), 2.6, 2.2)
    ic.path(rrect(3, 14, 37, 31, 2.5), ic.lg([(0, "#f4f5f7"), (.5, "#c3c7cd"), (1, "#7b818a")], 0, 0, 1, 1), INK, LW)
    ic.path("M6.5,17.5H36.5V41.5H6.5Z", ic.lg([(0, "#3a3f46"), (1, "#060708")], 0, 0, 1, 1), INK, .9)
    ic.add('<path d="M10,22L14,25L10,28M16,28.5H21" fill="none" stroke="#e4e6e9" stroke-width="1.5" stroke-linecap="square"/>')
    ic.add('<path d="M7.5,18.5H35.5" stroke="#fff" stroke-opacity=".15" stroke-width="1"/>')


def e_gear(ic):
    cx, cy, R, r, n = 23, 30, 18, 13.5, 8
    pts = []
    for k in range(n):
        a = 2 * math.pi * k / n
        for da, rad in ((-.2, r), (-.13, R), (.13, R), (.2, r)):
            pts.append((cx + rad * math.cos(a + da), cy + rad * math.sin(a + da)))
    d = "M" + "L".join(f"{x:.2f},{y:.2f}" for x, y in pts) + "Z"
    ic.shadow(d, 2.6, 2.2)
    ic.path(d, ic.rg([(0, "#ffffff"), (.6, "#c3c7cd"), (1, "#6c727a")], .35, .3, .8), INK, LW)
    ic.path(circle(cx, cy, 9.5), ic.rg([(0, "#ffe2b0"), (.55, "#e89a3a"), (1, "#8a4c10")], .4, .35, .75), INK, 1)
    ic.path(circle(cx, cy, 2.6), "#2c2016", None)
    ic.add(f'<path d="M{cx - 6},{cy - 4}Q{cx - 4},{cy - 7.5} {cx},{cy - 7.6}" fill="none" stroke="#fff" stroke-opacity=".8" stroke-width="1.4" stroke-linecap="round"/>')


def e_question(ic):
    q = "M14.5,19Q14.5,9.5 24.5,9.5Q34.5,9.5 34.5,18.5Q34.5,25 28,28Q24.5,30 24.5,35V37.5"
    ic.add(f'<path d="{q}" fill="none" stroke="#000" stroke-opacity=".25" stroke-width="8.5" stroke-linecap="round" transform="translate(2,2)"/>')
    ic.add(f'<path d="{q}" fill="none" stroke="{INK}" stroke-width="8.5" stroke-linecap="round" stroke-linejoin="round"/>')
    ic.add(f'<path d="{q}" fill="none" stroke="#2f9a2e" stroke-width="5.6" stroke-linecap="round" stroke-linejoin="round"/>')
    ic.add('<path d="M16.6,17.6Q17.4,12 24.4,11.8Q30,11.8 31.6,15.4" fill="none" stroke="#b4f0a0" stroke-width="1.6" stroke-linecap="round"/>')
    dot = "M24.5,41.5L29,46L24.5,50.5L20,46Z"
    ic.shadow(dot, 2, 2)
    ic.path(dot, ic.lg([(0, "#9ee070"), (1, "#1e6a10")], 0, 0, 1, 1), INK, LW)


def box(ic, x=8, y=14, w=18, h=22):
    """Isometric cardboard box (the original tar icon)."""
    T, R, F, L = (x + w, y), (x + 2 * w, y + w / 2), (x + w, y + w), (x, y + w / 2)
    dn = lambda p: (p[0], p[1] + h)
    P = lambda *pts: "M" + "L".join(f"{a:.2f},{b:.2f}" for a, b in pts) + "Z"
    ic.shadow(P(T, R, dn(R), dn(F), dn(L), L), 2.6, 2.2)
    ic.path(P(L, F, dn(F), dn(L)), ic.lg([(0, "#fbf2c4"), (1, "#cdb468")]), INK, 1)
    ic.path(P(F, R, dn(R), dn(F)), ic.lg([(0, "#d8c070"), (1, "#8a7430")]), INK, 1)
    ic.path(P(T, R, F, L), ic.lg([(0, "#fffbe4"), (1, "#e8d690")], 0, 0, 1, 1), INK, 1)
    m1, m2 = ((L[0] + T[0]) / 2, (L[1] + T[1]) / 2), ((F[0] + R[0]) / 2, (F[1] + R[1]) / 2)
    ic.add(f'<path d="M{m1[0]:.1f},{m1[1]:.1f}L{m2[0]:.1f},{m2[1]:.1f}" stroke="#a89040" stroke-width="1"/>')
    # label on the left face, a tab mark on the right
    lb = [(x + 4, y + w / 2 + 9), (x + 13, y + w / 2 + 13.5), (x + 13, y + w / 2 + 19), (x + 4, y + w / 2 + 14.5)]
    ic.path(P(*lb), "#ffffff", "#a89040", .7)
    ic.add(f'<path d="M{x + 5.5},{y + w / 2 + 12.4}L{x + 11.5},{y + w / 2 + 15.4}" stroke="#c87ae8" stroke-width="1.4"/>')
    ic.path(P((x + w + 6, y + w + 14), (x + w + 12, y + w + 11), (x + w + 12, y + w + 17)), "#8a7430", None)
    ic.add(f'<path d="{P(T, R, dn(R), dn(F), dn(L), L)}" fill="none" stroke="{INK}" stroke-width="{LW}" stroke-linejoin="round"/>')


def e_box(ic):
    box(ic)


def e_squeeze(ic):
    """The magenta corner marks the originals put on compressed files."""
    g = lambda: ic.lg([(0, "#fbd0ff"), (.5, "#d050e8"), (1, "#7a1090")], 0, 0, 1, 1)
    ic.path("M1.5,13L13,1.5V13Z", g(), INK, 1)
    ic.path("M50,50H62.5L50,62.5Z", g(), INK, 1)


def e_info(ic):
    ticks(ic)
    ic.shadow(circle(21, 30, 18), 2.6, 2.2)
    ic.path(circle(21, 30, 18), ic.rg([(0, "#8ab8f0"), (.45, "#2a5ab0"), (1, "#081c50")], .35, .28, .85), INK, LW)
    ic.add('<path d="M9,24C10,15 20,10 29,14C24,13 15,15 9,24Z" fill="#fff" fill-opacity=".5"/>')
    ic.path(circle(21, 20.5, 3), "#ffffff", None)
    ic.path("M16.5,26H23.5V37.5H26V41H16V37.5H18.5V29.5H16.5Z", "#ffffff", None)


def e_envelope(ic):
    ticks(ic)
    env = "M2,26H38V54H2Z"
    ic.shadow(env, 2.6, 2.2)
    ic.path(env, ic.lg([(0, "#fffdf6"), (1, "#e8dcc4")], 0, 0, 1, 1), INK, LW)
    ic.add(f'<path d="M2.6,26.6L20,42L37.4,26.6M2.6,53.4L15,38.5M37.4,53.4L25,38.5" fill="none" stroke="#8a7a5c" stroke-width="1.1" stroke-linejoin="round"/>')


def e_vcard(ic):
    ic.add('<g transform="rotate(-14 22 36)">')
    ic.shadow("M14,22H44V44H14Z", 2.4, 2)
    ic.path("M14,22H44V44H14Z", ic.lg([(0, "#d8d4ff"), (1, "#7a72d8")]), INK, 1)
    ic.shadow("M2,30H34V52H2Z", 2.4, 2)
    ic.path("M2,30H34V52H2Z", ic.lg([(0, "#ffffff"), (1, "#e4e6e9")]), INK, LW)
    ic.add(f'<path d="M7,35L11,46L15,35M18.5,39H27.5M18.5,43H27.5" fill="none" stroke="{INK}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>')
    ic.add("</g>")


def e_calendar(ic):
    ic.add('<g transform="rotate(14 24 40)">')
    body = "M6,24H42V54H6Z"
    ic.shadow(body, 2.4, 2)
    ic.path(body, ic.lg([(0, "#ffffff"), (1, "#dfe2e6")]), INK, LW)
    ic.path("M6,24H42V30.5H6Z", ic.lg([(0, "#c4a8ff"), (1, "#6a3ac0")]), INK, 1)
    grid = "".join(f"M{6 + k * 6},30.5V54" for k in range(1, 6)) + "".join(f"M6,{30.5 + k * 5.9}H42" for k in range(1, 4))
    ic.add(f'<path d="{grid}" stroke="#9aa0a8" stroke-width=".7"/>')
    ic.path("M24.4,42.6H29.6V47.9H24.4Z", ic.lg([(0, "#ff9a6a"), (1, "#c02a0c")]), "#7a1a0a", .6)
    for k in range(6):
        ic.path(circle(9 + k * 6, 24, 1.3), "#f4f5f7", INK, .6)
    ic.add("</g>")


def e_book(ic):
    l = "M23,18C18,14 11,14 5,17V45C11,42 18,42 23,46Z"
    r = "M23,18C28,14 35,14 41,17V45C35,42 28,42 23,46Z"
    ic.shadow(l + r, 2.6, 2.2)
    ic.path(l, ic.lg([(0, "#ffffff"), (1, "#b4b9c0")], 1, 0, 0, 1), INK, LW)
    ic.path(r, ic.lg([(0, "#9aa0a8"), (.6, "#d4d7dc"), (1, "#7b818a")], 0, 0, 1, 1), INK, LW)
    ic.add('<path d="M8,21Q14,18.5 20,20.5M8,25Q14,22.5 20,24.5M26,20.5Q32,18.5 38,21" fill="none" stroke="#9aa0a8" stroke-width=".9"/>')


def e_midi(ic):
    keys = "M1,4H24V54H1Z"
    ic.shadow(keys, 2.6, 2.2)
    ic.path(keys, "#ffffff", INK, LW)
    ic.add(f'<path d="{"".join(f"M1,{4 + k * 7.14:.1f}H24" for k in range(1, 7))}" stroke="#9aa0a8" stroke-width=".8"/>')
    for k in (1, 2, 4, 5, 6):
        y = 4 + k * 7.14
        ic.path(f"M1,{y - 2.4:.1f}H14Q15,{y - 2.4:.1f} 15,{y - 1.4:.1f}V{y + 1.4:.1f}Q15,{y + 2.4:.1f} 14,{y + 2.4:.1f}H1Z", ic.lg([(0, "#5c6168"), (1, "#060708")], 0, 0, 1, 0), None)
    staff = "".join(f"M28,{20 + k * 2.6:.1f}H53" for k in range(5)) + "".join(f"M28,{38 + k * 2.6:.1f}H53" for k in range(5))
    ic.add(f'<path d="{staff}" stroke="#9a8e74" stroke-width=".7"/>')
    for x, y in ((34, 27.8), (44, 25.2), (36, 45.8), (47, 43.2)):
        ic.path(f"M{x - 2},{y}a2,1.5 -20 1 0 4,0a2,1.5 -20 1 0 -4,0Z", "#6c6458", None)
        ic.add(f'<path d="M{x + 1.9},{y - .3}V{y - 8}Q{x + 4},{y - 6} {x + 4.5},{y - 3.5}" fill="none" stroke="#6c6458" stroke-width=".9"/>')


def e_padlock(ic):
    ic.add(f'<path d="M12,30V21A11,11 0 0 1 34,21V30" fill="none" stroke="{INK}" stroke-width="7.4"/>')
    ic.add(f'<path d="M12,30V21A11,11 0 0 1 34,21V30" fill="none" stroke="#c3c7cd" stroke-width="4.4"/>')
    ic.add('<path d="M12.6,26V21A10.4,10.4 0 0 1 23,10.6" fill="none" stroke="#fff" stroke-width="1.2" stroke-opacity=".8"/>')
    body = rrect(5, 29, 36, 26, 4)
    ic.shadow(body, 2.6, 2.2)
    ic.path(body, ic.lg([(0, "#fff3a6"), (.45, "#d8b030"), (1, "#7a5a04")], 0, 0, 1, 1), INK, LW)
    ic.path("M5.7,37H40.3V45H5.7Z", ic.lg([(0, "#ffffff"), (.5, "#c3c7cd"), (1, "#7b818a")]), None)
    ic.add(f'<path d="M5.7,37H40.3M5.7,45H40.3" stroke="{INK}" stroke-width=".9"/>')


def e_vector(ic):
    # set square: smaller and over the page, angled band a little thinner than the straight sides (2026-10-27)
    sq = "M8,6L25,48H8Z M12.5,26.98V43.5H19.19Z"
    ic.shadow(sq, 2.4, 2)
    ic.path(sq, ic.lg([(0, "#c4f4f4"), (.5, "#3ab0b8"), (1, "#0a5a64")], 0, 0, 1, 1), INK, LW, ' fill-rule="evenodd"')
    ic.add('<path d="M28,22Q31,34 38,36Q46,38 50,52" fill="none" stroke="#6c6458" stroke-width="1.2"/>')
    ic.add('<path d="M28,22L38,36L48,46" fill="none" stroke="#6c6458" stroke-width=".7"/>')
    for x, y in ((28, 22), (48, 46)):
        ic.path(f"M{x - 2.4},{y - 2.4}H{x + 2.4}V{y + 2.4}H{x - 2.4}Z", "#ffffff", INK, 1)
    ic.path(circle(38, 36, 2.4), ic.rg([(0, "#fff3a6"), (1, "#a87a10")]), INK, .9)


def e_log(ic):
    ic.shadow("M2,15H40V47H2Z", 2.6, 2.2)
    ic.path("M2,15H40V47H2Z", ic.lg([(0, "#2c8a6a"), (1, "#063a2a")], 0, 0, 1, 1), INK, LW)
    ic.add(f'<path d="{"".join(f"M3,{19 + k * 4}H39" for k in range(7))}" stroke="#6ad0a8" stroke-opacity=".45" stroke-width=".7"/>')
    ic.add('<path d="M3,39L9,35L13,37L18,27L22,33L26,21L30,30L34,25L39,29" fill="none" stroke="#fff060" stroke-width="1.8" stroke-linejoin="round"/>')


def e_disc(ic):
    disc(ic, 23, 31, 20.5)


def e_bomb(ic):
    ic.add(f'<path d="M30,15Q33,8 39,9" fill="none" stroke="{INK}" stroke-width="3.6" stroke-linecap="round"/>')
    ic.add('<path d="M30,15Q33,8 39,9" fill="none" stroke="#c8a878" stroke-width="1.8" stroke-linecap="round"/>')
    ic.add(f'<path d="M26,16L32,12L35,17L29,21Z" fill="#5c6168" stroke="{INK}" stroke-width="1"/>')
    ic.shadow(circle(21, 34, 16), 2.6, 2.2)
    ic.path(circle(21, 34, 16), ic.rg([(0, "#9aa0a8"), (.35, "#3c4148"), (1, "#060708")], .35, .3, .8), INK, LW)
    ic.add('<path d="M11,29Q13,22 20,20" fill="none" stroke="#fff" stroke-opacity=".6" stroke-width="2" stroke-linecap="round"/>')
    for a in range(0, 360, 45):
        r1, r2 = 2, 5.5 if a % 90 == 0 else 4
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        ic.add(f'<path d="M{39 + r1 * ca:.1f},{9 + r1 * sa:.1f}L{39 + r2 * ca:.1f},{9 + r2 * sa:.1f}" stroke="#ff9a10" stroke-width="1.3" stroke-linecap="round"/>')
    ic.path(circle(39, 9, 1.8), "#fff3a6", None)


def e_calc_sheet(ic):
    # spreadsheet grid on the page
    ic.path("M30,24H54V52H30Z", "#ffffff", "#9aa0a8", .8)
    ic.path("M30,24H54V28.5H30Z", "#b4b4ec", "#9aa0a8", .8)
    grid = "".join(f"M{30 + k * 6},24V52" for k in range(1, 4)) + "".join(f"M30,{28.5 + k * 4.7:.1f}H54" for k in range(1, 5))
    ic.add(f'<path d="{grid}" stroke="#9aa0a8" stroke-width=".7"/>')
    # calculator
    body = rrect(3, 12, 27, 38, 2.5)
    ic.shadow(body, 2.6, 2.2)
    ic.path(body, ic.lg([(0, "#f4f5f7"), (.5, "#c9ccd1"), (1, "#7b818a")], 0, 0, 1, 1), INK, LW)
    ic.path("M7,16H26V23H7Z", ic.lg([(0, "#b4f0a0"), (1, "#3a9a3a")]), INK, .9)
    for r in range(4):
        for c in range(3):
            ic.path(rrect(7 + c * 6.6, 26.5 + r * 5.6, 5, 4.2, .8), ic.lg([(0, "#ffffff"), (1, "#b4b9c0")]), INK, .7)


def e_slide(ic):
    ic.shadow("M3,18H41V46H3Z", 2.6, 2.2)
    ic.path("M3,18H41V46H3Z", ic.lg([(0, "#ffffff"), (1, "#dfe2e6")]), INK, LW)
    ic.path("M3,18H41V24H3Z", ic.lg([(0, "#9fd4ff"), (1, "#1a5c9e")]), INK, 1)
    for k, (h, col) in enumerate(((10, ("#ff9a8a", "#c0281a")), (15, ("#ffe080", "#c89a10")), (7, ("#9ee070", "#2f8a1e")), (12, ("#9fd4ff", "#1a5c9e")))):
        x = 8 + k * 7.5
        ic.path(f"M{x},{42 - h}H{x + 5}V42H{x}Z", ic.lg([(0, col[0]), (1, col[1])], 0, 0, 1, 0), INK, .7)
    ic.add(f'<path d="M6,42.4H38" stroke="{INK}" stroke-width=".8"/>')


def e_badge(text_d, colour=("#ff8a7a", "#c41a0c", "#6a0a04")):
    """A coloured label with white block lettering (used for PDF and PostScript, instead of logos)."""
    def f(ic):
        b = rrect(2, 27, 36, 20, 3)
        ic.shadow(b, 2.6, 2.2)
        ic.path(b, ic.lg([(0, colour[0]), (.5, colour[1]), (1, colour[2])]), INK, LW)
        ic.add('<path d="M5,29.6H35" stroke="#fff" stroke-opacity=".4" stroke-width="1.2"/>')
        strokes(ic, text_d, w_in=2.2, w_out=4.2, transform="")
    return f


PDF = ("M7.5,42.5V31.5H11.5Q14.8,31.5 14.8,34.6Q14.8,37.6 11.5,37.6H7.5 "
       "M18.2,42.5V31.5H21Q25.6,31.5 25.6,37Q25.6,42.5 21,42.5Z "
       "M29.2,42.5V31.5H34.2M29.2,36.8H33")
PS = ("M10.5,42.5V31.5H14.5Q17.8,31.5 17.8,34.6Q17.8,37.6 14.5,37.6H10.5 "
      "M29.5,32.6Q28.2,31.4 25.8,31.4Q22.4,31.4 22.4,34.2Q22.4,36.6 25.9,37Q29.6,37.4 29.6,39.8Q29.6,42.6 25.9,42.6Q23.4,42.6 22,41.2")


def exe():
    """Programs: the original shows the gear on its own, no page."""
    ic = Icon()
    ic.add('<g transform="translate(32,32) scale(1.5) translate(-23,-30)">')
    e_gear(ic)
    ic.add("</g>")
    return ic


MIMES = {
    "application-x-zerosize": mime(),
    "text-plain": mime(m_lines),
    "text-x-generic": mime(e_pencil),
    "x-office-document": mime(m_document),
    "x-office-spreadsheet": mime(e_calc_sheet),
    "x-office-presentation": mime(e_slide),
    "image-x-generic": mime(lambda ic: e_scene(ic)),
    "audio-x-generic": mime(e_audio),
    "video-x-generic": mime(e_film_strip),
    "text-html": mime(e_html),
    "application-x-shellscript": mime(e_terminal),
    "application-x-object": mime(m_binary),
    "application-x-executable": exe,
    "text-x-source": mime(m_source),
    "text-x-makefile": mime(e_gear),
    "unknown": mime(e_question),
    "package-x-generic": mime(e_box),
    "application-x-compressed-tar": mime(e_box, e_squeeze),
    "text-x-readme": mime(e_info),
    "message-rfc822": mime(e_envelope),
    "text-vcard": mime(e_vcard),
    "text-calendar": mime(e_calendar),
    "application-x-troff-man": mime(e_book),
    "audio-midi": mime(e_midi),
    "application-pgp-encrypted": mime(e_padlock),
    "image-svg+xml": mime(e_vector),
    "text-x-log": mime(e_log),
    "application-x-cd-image": mime(e_disc),
    "application-x-core": mime(e_bomb),
    "application-pdf": mime(lambda ic: lines(ic, 21, 53, 19, 11, breaks=(5,)), e_badge(PDF)),
    "application-postscript": mime(lambda ic: lines(ic, 21, 53, 19, 11, breaks=(5,)), e_badge(PS, ("#8a9098", "#2c3036", "#060708"))),
}

_A = {
    "application-x-zerosize": ["empty"],
    "text-plain": ["text-x-nfo", "text-x-changelog", "text-x-authors", "text-x-copying", "text-x-install", "text-markdown", "text-x-markdown"],
    "text-x-generic": ["text-x-generic-template", "text-richtext", "application-rtf"],
    "x-office-document": ["application-vnd.oasis.opendocument.text", "application-msword", "application-vnd.ms-word",
                          "application-vnd.openxmlformats-officedocument.wordprocessingml.document", "x-office-document-template",
                          "application-vnd.oasis.opendocument.text-template", "application-x-abiword", "application-epub+zip"],
    "x-office-spreadsheet": ["application-vnd.oasis.opendocument.spreadsheet", "application-vnd.ms-excel", "text-csv",
                             "application-vnd.openxmlformats-officedocument.spreadsheetml.sheet", "x-office-spreadsheet-template",
                             "text-tab-separated-values", "application-x-gnumeric"],
    "x-office-presentation": ["application-vnd.oasis.opendocument.presentation", "application-vnd.ms-powerpoint",
                              "application-vnd.openxmlformats-officedocument.presentationml.presentation", "x-office-presentation-template"],
    "image-x-generic": ["image-png", "image-jpeg", "image-gif", "image-bmp", "image-tiff", "image-webp", "image-x-xcf", "image-x-portable-bitmap",
                        "image-x-portable-pixmap", "image-x-xpixmap", "image-x-icon", "image-vnd.microsoft.icon", "image-heif", "image-avif", "image-jxl",
                        "application-x-krita", "image-openraster", "image-x-generic-template"],
    "audio-x-generic": ["audio-mpeg", "audio-x-mp3", "audio-x-wav", "audio-x-flac", "audio-flac", "audio-ogg", "audio-x-vorbis+ogg", "audio-mp4",
                        "audio-x-m4a", "audio-aac", "audio-x-ms-wma", "audio-x-mpegurl", "audio-x-scpls", "audio-webm", "audio-x-opus+ogg", "audio-x-aiff"],
    "video-x-generic": ["video-mp4", "video-x-matroska", "video-webm", "video-mpeg", "video-x-msvideo", "video-quicktime", "video-x-flv",
                        "video-x-ms-wmv", "video-ogg", "video-x-theora+ogg", "video-3gpp", "video-mp2t"],
    "text-html": ["application-xhtml+xml", "text-x-html", "html", "application-x-mswinurl", "text-uri-list"],
    "application-x-shellscript": ["text-x-script", "application-x-perl", "text-x-perl", "application-x-ruby", "text-x-ruby", "application-x-csh",
                                  "text-x-sh", "application-x-desktop", "shellscript"],
    "application-x-object": ["application-x-sharedlib", "binary"],
    "application-x-executable": [ "application-octet-stream-binary", "application-x-ms-dos-executable",
                                 "application-x-msdownload", "application-x-elf", "application-x-appimage", "exec"],
    "text-x-source": ["text-x-c", "text-x-csrc", "text-x-chdr", "text-x-c++src", "text-x-c++hdr", "text-x-c++", "text-x-java", "text-x-python",
                      "text-x-python3", "application-x-python", "application-x-python-bytecode", "application-javascript", "text-javascript",
                      "application-json", "application-xml", "text-xml", "text-css", "text-x-csharp", "text-x-go", "text-rust", "text-x-rust",
                      "text-x-php", "application-x-php", "text-x-qml", "text-x-lua", "text-x-patch", "text-x-diff", "text-x-sql",
                      "application-x-yaml", "text-x-yaml", "application-toml", "text-x-kotlin", "text-x-pascal", "text-x-fortran",
                      "text-x-haskell", "text-x-tex", "text-x-csharp", "source", "text-x-hex"],
    "text-x-makefile": ["text-x-cmake", "application-x-ninja", "text-x-meson", "make"],
    "unknown": ["application-octet-stream", "application-x-generic"],
    "package-x-generic": ["application-x-tar", "application-x-archive", "application-x-deb", "application-vnd.debian.binary-package",
                          "application-x-rpm", "application-x-source-rpm", "application-x-java-archive", "application-x-cpio", "tar"],
    "application-x-compressed-tar": ["application-zip", "application-x-zip", "application-x-7z-compressed", "application-x-rar",
                                     "application-vnd.rar", "application-x-bzip", "application-x-bzip-compressed-tar", "application-x-xz",
                                     "application-x-xz-compressed-tar", "application-gzip", "application-x-gzip", "application-zstd",
                                     "application-x-zstd-compressed-tar", "application-x-lzma", "application-x-arj", "application-x-lha",
                                     "application-x-ace", "application-x-cab", "tgz"],
    "text-x-readme": ["text-x-info", "readme", "info"],
    "message-rfc822": ["message", "application-mbox", "message-news", "message-partial"],
    "text-vcard": ["text-x-vcard", "text-directory", "vcard"],
    "text-calendar": ["text-x-vcalendar", "vcalendar", "application-ics"],
    "application-x-troff-man": ["text-troff", "text-x-troff-man", "man"],
    "audio-midi": ["audio-x-midi", "midi"],
    "application-pgp-encrypted": ["application-pgp", "application-pgp-keys", "application-pgp-signature", "application-x-pkcs12",
                                  "application-pkcs7-signature", "application-x-x509-ca-cert", "application-pkcs8", "encrypted"],
    "image-svg+xml": ["image-svg+xml-compressed", "image-x-eps", "application-illustrator", "image-x-wmf", "image-x-emf",
                      "application-vnd.oasis.opendocument.graphics", "x-office-drawing", "vectorgfx"],
    "text-x-log": ["log"],
    "application-x-cd-image": ["application-x-iso9660-image", "application-x-raw-disk-image", "application-x-iso", "cdimage", "cdtrack"],
    "application-x-core": ["core"],
    "application-pdf": ["application-x-pdf", "pdf"],
    "application-postscript": ["image-x-eps-postscript", "application-x-dvi", "postscript"],
}
MIME_ALIASES = {a: t for t, al in _A.items() for a in al if a not in MIMES}


# ------------------------------------------------------------------ small corner labels (py, c++, ...)
def _bowl(cx):
    return f"M{cx},-4A1.5,2 0 1 0 {cx},0A1.5,2 0 1 0 {cx},-4"


# a tiny stroked lowercase alphabet (x-height 4, ascenders 6.5): no fonts, so it renders anywhere
GLYPHS = {
    "a": (_bowl(1.5) + "M3,-4V0", 3), "b": ("M0,-6.5V0" + _bowl(1.5), 3),
    "c": ("M3,-3.6Q2.5,-4 1.5,-4Q0,-4 0,-2Q0,0 1.5,0Q2.5,0 3,-.4", 3), "d": (_bowl(1.5) + "M3,-6.5V0", 3),
    "e": ("M0,-2H3Q3,-4 1.5,-4Q0,-4 0,-2Q0,0 1.5,0Q2.5,0 3,-.5", 3), "f": ("M2.5,-6.3Q1,-6.8 1,-5V0M0,-4H2.4", 2.5),
    "g": (_bowl(1.5) + "M3,-4V1Q3,2.5 1.5,2.5Q.6,2.5 .2,2", 3), "h": ("M0,-6.5V0M0,-2.5Q.5,-4 1.6,-4Q3,-4 3,-2.5V0", 3),
    "i": ("M.5,-4V0M.5,-6V-5.9", 1), "j": ("M1,-4V1.2Q1,2.5 -.2,2.4M1,-6V-5.9", 1.5),
    "k": ("M0,-6.5V0M3,-4L.3,-1.6M1.2,-2.4L3,0", 3), "l": ("M.5,-6.5V0", 1),
    "m": ("M0,-4V0M0,-2.8Q.4,-4 1.3,-4Q2.3,-4 2.3,-2.8V0M2.3,-2.8Q2.7,-4 3.6,-4Q4.6,-4 4.6,-2.8V0", 4.6),
    "n": ("M0,-4V0M0,-2.5Q.5,-4 1.6,-4Q3,-4 3,-2.5V0", 3), "o": (_bowl(1.5), 3),
    "p": ("M0,-4V2.5" + _bowl(1.5), 3), "q": (_bowl(1.5) + "M3,-4V2.5", 3),
    "r": ("M0,-4V0M0,-2.4Q.6,-4 2.4,-3.9", 2.4),
    "s": ("M2.8,-3.6Q2.2,-4 1.4,-4Q.2,-4 .2,-3Q.2,-2.1 1.5,-2Q2.9,-1.9 2.9,-1Q2.9,0 1.5,0Q.6,0 0,-.5", 2.9),
    "t": ("M1,-5.6V-1Q1,0 2.2,0M0,-4H2.2", 2.2), "u": ("M0,-4V-1.5Q0,0 1.4,0Q3,0 3,-1.5M3,-4V0", 3),
    "v": ("M0,-4L1.5,0L3,-4", 3), "w": ("M0,-4L1.1,0L2.3,-3L3.5,0L4.6,-4", 4.6), "x": ("M0,-4L3,0M3,-4L0,0", 3),
    "y": ("M0,-4L1.5,0M3,-4L1,2.5", 3), "z": ("M0,-4H3L0,0H3", 3),
    "+": ("M0,-2H3M1.5,-3.5V-.5", 3),
    "2": ("M.2,-5.5Q.8,-6.5 1.8,-6.5Q3,-6.5 3,-5Q3,-3.8 0,0H3.2", 3.2),
    "3": ("M.3,-6.5H3L1.4,-3.8Q3.2,-3.8 3.2,-1.9Q3.2,0 1.5,0Q.6,0 0,-.6", 3.2),
    "4": ("M2.4,0V-6.5L0,-2H3.2", 3.2),
    "7": ("M0,-6.5H3.2L1.2,0", 3.2),
    "1": ("M.3,-5.2L1.7,-6.5V0M.2,0H3.2", 3.2),
    "0": ("M1.6,-6.5Q0,-6.5 0,-3.25Q0,0 1.6,0Q3.2,0 3.2,-3.25Q3.2,-6.5 1.6,-6.5Z", 3.2),
    "5": ("M3,-6.5H.4L.2,-3.6Q.8,-4.1 1.6,-4.1Q3.2,-4.1 3.2,-2Q3.2,0 1.5,0Q.6,0 0,-.6", 3.2),
    "6": ("M2.8,-6.3Q2.3,-6.5 1.8,-6.5Q0,-6.5 0,-3Q0,0 1.6,0Q3.2,0 3.2,-2Q3.2,-4 1.6,-4Q.6,-4 0,-3", 3.2),
    "8": ("M1.6,-3.6Q.2,-3.8 .2,-5Q.2,-6.5 1.6,-6.5Q3,-6.5 3,-5Q3,-3.8 1.6,-3.6Q0,-3.4 0,-1.8Q0,0 1.6,0Q3.2,0 3.2,-1.8Q3.2,-3.4 1.6,-3.6Z", 3.2),
    "9": ("M3.2,-3.4Q2.6,-2.5 1.6,-2.5Q0,-2.5 0,-4.5Q0,-6.5 1.6,-6.5Q3.2,-6.5 3.2,-3.5Q3.2,0 1.4,0Q.9,0 .4,-.2", 3.2), "#": ("M1,-4.6L.6,.4M2.6,-4.6L2.2,.4M0,-3H3.2M-.2,-1H3", 3.2),
}
LABEL_COLOURS = {
    "blue": ("#8ab8f0", "#2a5ab0", "#0e2a6a"), "teal": ("#8ae0e0", "#1a8a96", "#064048"),
    "violet": ("#d4b4ff", "#7a3ac8", "#3a1070"), "orange": ("#ffd0a0", "#d8701a", "#7a3404"),
    "amber": ("#ffe8a0", "#c08a10", "#6a4404"), "red": ("#ffb4a8", "#c42a1a", "#6a0a04"),
    "green": ("#b4f0a0", "#2f8a2e", "#10481a"), "grey": ("#d4d7dc", "#5c6168", "#26292e"),
    "brown": ("#e8c8a0", "#8a5a2a", "#4a2a0a"), "pink": ("#ffc4e0", "#c8327a", "#6a0a3a"),
    "navy": ("#a8b8e8", "#22357a", "#0a1238"), "crimson": ("#ffa8b8", "#a8102e", "#500414"),
    "cyan": ("#b0f0ff", "#1aa0c8", "#06485a"), "lime": ("#e0f8a0", "#6aa810", "#2e4a04"),
    "magenta": ("#ffb0f4", "#b01aa0", "#500448"), "slate": ("#c8d0dc", "#4a5868", "#1e2630"),
    "gold": ("#fff0a0", "#b89410", "#5a4404"), "indigo": ("#c4b8ff", "#4a2ab8", "#1e0a5a"),
    "olive": ("#e8e8b0", "#7a7a24", "#38380a"),
}


def e_label(text, colour="blue", k=1.25, x1=56.5, y1=56.5, transform="", shadow=True):
    """A coloured tag (by default in the page's lower-right corner) with the file's usual extension in white.
    x1, y1 place the tag's lower-right corner; transform lets it sit on a slanted face."""
    def f(ic):
        gap, xs, d = 1.3, [], ""
        x = 0.0
        for ch in text:
            g, w = GLYPHS[ch]
            d += f'<path d="{g}" transform="translate({x:.2f},0)"/>'
            x += w + gap
        W = (x - gap) * k
        desc = any(ch in "gjpqy" for ch in text)
        h = (6.5 + (2.5 if desc else 0)) * k + 4
        x0, y0 = x1 - W - 4.4, y1 - h
        c = LABEL_COLOURS[colour]
        tag = rrect(round(x0, 2), round(y0, 2), round(W + 4.4, 2), round(h, 2), 1.8)
        ic.add(f'<g transform="{transform}">' if transform else "<g>")
        if shadow:
            ic.shadow(tag, 1.4, 1.2)
        ic.path(tag, ic.lg([(0, c[0]), (.5, c[1]), (1, c[2])]), INK, 1)
        base = y0 + 2 + 6.5 * k
        ic.add(f'<g transform="translate({x0 + 2.2:.2f},{base:.2f}) scale({k})" fill="none" stroke="#fff" '
               f'stroke-width="{1.15 / k * 1.25:.2f}" stroke-linecap="round" stroke-linejoin="round">{d}</g>')
        ic.add("</g>")
    return f


# ------------------------------------------------------------------ lion's head (TeX / DVI files)
def e_lion(ic):
    """A friendly, generic lion's head: shaggy mane, tan face, dark nose."""
    cx, cy = 22, 31
    mane = []
    n = 14
    for k in range(n * 2):
        a = math.pi * k / n
        r = 19 if k % 2 == 0 else 14.5
        mane.append((cx + r * math.cos(a), cy + r * math.sin(a) * .95))
    d = "M" + "L".join(f"{x:.2f},{y:.2f}" for x, y in mane) + "Z"
    from traceart import catmull
    d = catmull(mane, .7)
    ic.shadow(d, 2.6, 2.2)
    ic.path(d, ic.rg([(0, "#ffd890"), (.5, "#d8781c"), (1, "#7a3404")], .45, .4, .75), INK, LW)
    for ex in (-8.5, 8.5):
        ic.path(circle(cx + ex, cy - 9, 3.6), ic.rg([(0, "#f4d4a0"), (1, "#b07a3a")]), INK, 1)
    face = (f"M{cx},{cy - 11}C{cx + 8},{cy - 11} {cx + 10.5},{cy - 5} {cx + 10},{cy + 1}C{cx + 9.5},{cy + 8} {cx + 5},{cy + 12} {cx},{cy + 12}"
            f"C{cx - 5},{cy + 12} {cx - 9.5},{cy + 8} {cx - 10},{cy + 1}C{cx - 10.5},{cy - 5} {cx - 8},{cy - 11} {cx},{cy - 11}Z")
    ic.path(face, ic.rg([(0, "#fff0cc"), (.6, "#f0c47c"), (1, "#c08440")], .45, .3, .8), INK, 1.1)
    ic.path(f"M{cx - 6.5},{cy + 5}Q{cx - 6.5},{cy + .5} {cx},{cy + .5}Q{cx + 6.5},{cy + .5} {cx + 6.5},{cy + 5}Q{cx + 6},{cy + 10.5} {cx},{cy + 10.5}Q{cx - 6},{cy + 10.5} {cx - 6.5},{cy + 5}Z",
            "#fff8e8", None)
    for ex in (-4.2, 4.2):
        ic.path(circle(cx + ex, cy - 3.5, 1.6), INK, None)
        ic.path(circle(cx + ex + .5, cy - 4, .5), "#ffffff", None)
    ic.path(f"M{cx - 2.6},{cy + 1.8}H{cx + 2.6}L{cx},{cy + 4.6}Z", "#3a2010", INK, .6)
    ic.add(f'<path d="M{cx},{cy + 4.6}V{cy + 6.4}M{cx - 3.4},{cy + 6.2}Q{cx - 1.6},{cy + 8.2} {cx},{cy + 6.4}Q{cx + 1.6},{cy + 8.2} {cx + 3.4},{cy + 6.2}" '
           f'fill="none" stroke="#3a2010" stroke-width=".9" stroke-linecap="round"/>')


# ------------------------------------------------------------------ labelled variants
SRC = lambda t, c: mime(m_source, e_label(t, c))
SCRIPT = lambda t, c: mime(e_terminal, e_label(t, c))
LABELLED = {
    # source code
    "text-x-python": SRC("py", "blue"), "text-x-csrc": SRC("c", "grey"), "text-x-chdr": SRC("h", "grey"),
    "text-x-c++src": SRC("c++", "violet"), "text-x-c++hdr": SRC("h++", "violet"), "text-x-java": SRC("java", "orange"),
    "application-javascript": SRC("js", "amber"), "application-json": SRC("json", "amber"), "application-xml": SRC("xml", "teal"),
    "text-css": SRC("css", "blue"), "text-x-csharp": SRC("c#", "green"), "text-x-go": SRC("go", "teal"),
    "text-rust": SRC("rs", "brown"), "text-x-php": SRC("php", "violet"), "text-x-qml": SRC("qml", "green"),
    "text-x-lua": SRC("lua", "blue"), "text-x-patch": SRC("diff", "red"), "text-x-sql": SRC("sql", "orange"),
    "application-x-yaml": SRC("yml", "red"), "application-toml": SRC("toml", "brown"), "text-x-kotlin": SRC("kt", "violet"),
    "text-x-pascal": SRC("pas", "teal"), "text-x-fortran": SRC("for", "brown"), "text-x-haskell": SRC("hs", "violet"),
    "text-x-hex": SRC("hex", "grey"),
    # scripts
    "application-x-shellscript": SCRIPT("sh", "green"), "application-x-perl": SCRIPT("pl", "blue"),
    "application-x-ruby": SCRIPT("rb", "red"), "application-x-csh": SCRIPT("csh", "green"),
    # text
    "text-markdown": mime(m_lines, e_label("md", "grey")),
    # TeX family
    "text-x-tex": mime(lambda ic: lines(ic, 30, 53, 19, 11, breaks=(5,)), e_lion, e_label("tex", "brown")),
    "application-x-dvi": mime(lambda ic: lines(ic, 30, 53, 19, 11, breaks=(5,)), e_lion, e_label("dvi", "brown")),
}
LABEL_ALIASES = {
    "text-x-python": ["text-x-python3", "application-x-python", "application-x-python-bytecode"],
    "text-x-csrc": ["text-x-c"], "text-x-c++src": ["text-x-c++", "text-x-cpp"], "text-x-c++hdr": ["text-x-hpp"],
    "application-javascript": ["text-javascript", "application-x-javascript"], "application-xml": ["text-xml"],
    "text-rust": ["text-x-rust"], "text-x-php": ["application-x-php"], "text-x-patch": ["text-x-diff"],
    "application-x-yaml": ["text-x-yaml", "application-yaml"], "application-x-perl": ["text-x-perl"],
    "application-x-ruby": ["text-x-ruby"], "text-markdown": ["text-x-markdown"],
    "text-x-tex": ["text-x-latex", "application-x-tex", "text-x-bibtex"], "application-x-dvi": ["dvi"],
}
MIMES.update(LABELLED)
for t, al in LABEL_ALIASES.items():
    for a in al:
        MIME_ALIASES[a] = t
for n in LABELLED:
    MIME_ALIASES.pop(n, None)


# ------------------------------------------------------------------ 16 and 22 px versions of the tagged types
# At these sizes the emblem and the small tag can't be read, so the page carries just the abbreviation
# in a pixel font, white on a band of the tag's colour, laid on the pixel grid so it stays sharp.
PIXEL_FONT = {
    "A": [".#.", "#.#", "###", "#.#", "#.#"], "B": ["##.", "#.#", "##.", "#.#", "##."],
    "C": [".##", "#..", "#..", "#..", ".##"], "D": ["##.", "#.#", "#.#", "#.#", "##."],
    "E": ["###", "#..", "##.", "#..", "###"], "F": ["###", "#..", "##.", "#..", "#.."],
    "G": [".##", "#..", "#.#", "#.#", ".##"], "H": ["#.#", "#.#", "###", "#.#", "#.#"],
    "I": ["#", "#", "#", "#", "#"], "J": ["..#", "..#", "..#", "#.#", ".#."],
    "K": ["#.#", "#.#", "##.", "#.#", "#.#"], "L": ["#..", "#..", "#..", "#..", "###"],
    "M": ["#...#", "##.##", "#.#.#", "#...#", "#...#"], "N": ["#..#", "##.#", "#.##", "#..#", "#..#"],
    "O": [".#.", "#.#", "#.#", "#.#", ".#."], "P": ["##.", "#.#", "##.", "#..", "#.."],
    "Q": [".#.", "#.#", "#.#", "#.#", ".##"], "R": ["##.", "#.#", "##.", "#.#", "#.#"],
    "S": [".##", "#..", ".#.", "..#", "##."], "T": ["###", ".#.", ".#.", ".#.", ".#."],
    "U": ["#.#", "#.#", "#.#", "#.#", "###"], "V": ["#.#", "#.#", "#.#", ".#.", ".#."],
    "X": ["#.#", "#.#", ".#.", "#.#", "#.#"], "Y": ["#.#", "#.#", ".#.", ".#.", ".#."],
    "+": ["...", ".#.", "###", ".#.", "..."], "W": ["#...#", "#...#", "#.#.#", "##.##", "#...#"],
    "2": ["##.", "..#", ".#.", "#..", "###"], "3": ["##.", "..#", ".#.", "..#", "##."], "4": ["#.#", "#.#", "###", "..#", "..#"], "7": ["###", "..#", ".#.", ".#.", ".#."], "1": [".#.", "##.", ".#.", ".#.", "###"], "0": ["###", "#.#", "#.#", "#.#", "###"], "5": ["###", "#..", "##.", "..#", "##."],
    "6": [".##", "#..", "###", "#.#", "###"], "8": ["###", "#.#", "###", "#.#", "###"], "9": ["###", "#.#", "###", "..#", "##."],
    "Z": ["###", "..#", ".#.", "#..", "###"], "#": [".#.#.", "#####", ".#.#.", "#####", ".#.#."],
}


def pixel_text(text):
    """Pixel runs for text in the 3x5 font: list of (x, y, w) with 1 px gaps between letters."""
    runs, x = [], 0
    for ch in text.upper():
        g = PIXEL_FONT[ch]
        for y, row in enumerate(g):
            for cx, v in enumerate(row):
                if v == "#":
                    runs.append((x + cx, y))
        x += len(g[0]) + 1
    return runs, x - 1


def small_tagged(text, colour, S):
    """Page with the abbreviation as large as the pixel grid allows (S = 16 or 22)."""
    c = LABEL_COLOURS[colour]
    if S == 22:
        page_d, fold_d = "M3.5,1.5H13.5L18.5,6.5V20.5H3.5Z", "M13.5,1.5V6.5H18.5"
        band_top, band_bot = 10, 18          # band outline rows; text sits on rows 12..16
    else:
        page_d, fold_d = "M2.5,.5H9.5L13.5,4.5V15.5H2.5Z", "M9.5,.5V4.5H13.5"
        band_top, band_bot = 7, 15
    runs, w = pixel_text(text)
    inner = S - 2
    sides = w <= inner - 2                    # keep side outlines only when the text leaves room
    x0 = (S - w) // 2
    ty = band_top + 2
    g = ('<linearGradient id="p" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffffff"/>'
         '<stop offset=".45" stop-color="#fcf8f0"/><stop offset="1" stop-color="#d9b688"/></linearGradient>'
         f'<linearGradient id="b" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c[0]}"/>'
         f'<stop offset=".45" stop-color="{c[1]}"/><stop offset="1" stop-color="{c[2]}"/></linearGradient>')
    bx0, bx1 = (.5, S - .5) if sides else (-1, S + 1)
    band = f'M{bx0},{band_top + .5}H{bx1}V{band_bot + .5}H{bx0}Z'
    px = "".join(f"M{x0 + x},{ty + y}h1v1h-1z" for x, y in runs)
    body = (f'<path d="{page_d}" fill="url(#p)" stroke="{INK}" stroke-width="1"/>'
            f'<path d="{fold_d}" fill="#eeeae4" stroke="{INK}" stroke-width="1"/>'
            f'<path d="{band}" fill="url(#b)" stroke="{INK}" stroke-width="1" shape-rendering="crispEdges"/>'
            f'<path d="{px}" fill="#ffffff" shape-rendering="crispEdges"/>')
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}" viewBox="0 0 {S} {S}">'
            f'<defs>{g}</defs>{body}</svg>\n')


TAGS = {}   # name -> (text, colour), filled from the labelled table below
SMALL_TEXT = {}   # name -> shorter text for the 16/22 px band, when the full tag is too long


def _tags():
    src = {
        "text-x-python": ("py", "blue"), "text-x-csrc": ("c", "grey"), "text-x-chdr": ("h", "grey"),
        "text-x-c++src": ("c++", "violet"), "text-x-c++hdr": ("h++", "violet"), "text-x-java": ("java", "orange"),
        "application-javascript": ("js", "amber"), "application-json": ("json", "amber"), "application-xml": ("xml", "teal"),
        "text-css": ("css", "blue"), "text-x-csharp": ("c#", "green"), "text-x-go": ("go", "teal"),
        "text-rust": ("rs", "brown"), "text-x-php": ("php", "violet"), "text-x-qml": ("qml", "green"),
        "text-x-lua": ("lua", "blue"), "text-x-patch": ("diff", "red"), "text-x-sql": ("sql", "orange"),
        "application-x-yaml": ("yml", "red"), "application-toml": ("toml", "brown"), "text-x-kotlin": ("kt", "violet"),
        "text-x-pascal": ("pas", "teal"), "text-x-fortran": ("for", "brown"), "text-x-haskell": ("hs", "violet"),
        "text-x-hex": ("hex", "grey"), "application-x-shellscript": ("sh", "green"), "application-x-perl": ("pl", "blue"),
        "application-x-ruby": ("rb", "red"), "application-x-csh": ("csh", "green"), "text-markdown": ("md", "grey"),
        "text-x-tex": ("tex", "brown"), "application-x-dvi": ("dvi", "brown"),
    }
    TAGS.update(src)


_tags()


def write_small(out):
    """Write 16x16/mimetypes and 22x22/mimetypes for the tagged types, with their aliases."""
    import os
    for S in (16, 22):
        d = f"{out}/{S}x{S}/mimetypes"
        os.makedirs(d, exist_ok=True)
        short = lambda n: SMALL_TEXT.get(n, TAGS[n][0])
        fits = {n for n in TAGS if pixel_text(short(n))[1] <= S}   # e.g. WEBM is too wide for 16 px
        for name in fits:
            text, colour = short(name), TAGS[name][1]
            open(f"{d}/{name}.svg", "w").write(small_tagged(text, colour, S))
        for a, t in MIME_ALIASES.items():
            if t in fits and not os.path.exists(f"{d}/{a}.svg"):
                os.symlink(f"{t}.svg", f"{d}/{a}.svg")
    return len(TAGS)


# ------------------------------------------------------------------ audio and video formats, tagged the same way
MEDIA = {
    # audio
    "audio-mpeg": ("mp3", "blue", "a"), "audio-x-wav": ("wav", "teal", "a"), "audio-flac": ("flac", "violet", "a"),
    "audio-ogg": ("ogg", "green", "a"), "audio-x-opus+ogg": ("opus", "green", "a"), "audio-mp4": ("m4a", "orange", "a"),
    "audio-aac": ("aac", "orange", "a"), "audio-x-ms-wma": ("wma", "grey", "a"), "audio-x-aiff": ("aiff", "brown", "a"),
    "audio-x-mpegurl": ("m3u", "pink", "a"), "audio-x-scpls": ("pls", "pink", "a"),
    # video
    "video-mp4": ("mp4", "blue", "v"), "video-x-matroska": ("mkv", "violet", "v"), "video-webm": ("webm", "green", "v"),
    "video-mpeg": ("mpg", "teal", "v"), "video-x-msvideo": ("avi", "orange", "v"), "video-quicktime": ("mov", "grey", "v"),
    "video-x-flv": ("flv", "red", "v"), "video-x-ms-wmv": ("wmv", "grey", "v"), "video-ogg": ("ogv", "green", "v"),
    "video-3gpp": ("3gp", "brown", "v"), "video-mp2t": ("ts", "amber", "v"),
}
MEDIA_ALIASES = {
    "audio-mpeg": ["audio-x-mp3", "audio-mp3", "audio-x-mpeg"], "audio-x-wav": ["audio-wav", "audio-vnd.wave", "audio-x-pn-wav"],
    "audio-flac": ["audio-x-flac", "audio-x-flac+ogg"], "audio-ogg": ["audio-x-vorbis+ogg", "audio-vorbis", "audio-x-ogg"],
    "audio-x-opus+ogg": ["audio-opus"], "audio-mp4": ["audio-x-m4a", "audio-m4a", "audio-x-m4b"], "audio-aac": ["audio-x-aac"],
    "audio-x-aiff": ["audio-aiff", "audio-x-aifc"], "audio-x-mpegurl": ["audio-mpegurl", "application-vnd.apple.mpegurl"],
    "video-x-matroska": ["video-matroska", "video-x-matroska-3d"], "video-mpeg": ["video-x-mpeg", "video-x-mpeg2"],
    "video-x-msvideo": ["video-avi", "video-msvideo", "video-x-avi"], "video-x-flv": ["video-flv", "video-x-flash-video"],
    "video-ogg": ["video-x-theora+ogg", "video-x-ogm+ogg", "video-x-theora"], "video-3gpp": ["video-3gpp2", "audio-3gpp"],
    "video-mp4": ["video-x-m4v", "video-mp4v-es"],
}
for name, (text, colour, kind) in MEDIA.items():
    MIMES[name] = mime(e_audio if kind == "a" else e_film_strip, e_label(text, colour))
    TAGS[name] = (text, colour)
for t, al in MEDIA_ALIASES.items():
    for a in al:
        if a not in MIMES:
            MIME_ALIASES[a] = t
for n in MEDIA:
    MIME_ALIASES.pop(n, None)


# ------------------------------------------------------------------ optional: official logos supplied by the builder
# Logos are not drawn by this generator. If a freely licensed official logo file is placed in
# src/brand/, it is laid onto the page as-is. Currently supported:
#   brand/debian-openlogo-nd.svg  - Debian Open Use Logo without the label ("openlogo-nd.svg" from
#                                   https://www.debian.org/logos/, LGPL-3+ or CC BY-SA 3.0). Used for .deb packages.
import os as _os
import re as _re

BRAND_DIR = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "brand")


def _embed_svg(path, x, y, w, h, prefix):
    """Inline an SVG file's content into a box (x, y, w, h), keeping its aspect ratio, ids prefixed."""
    src = open(path, encoding="utf-8").read()
    src = _re.sub(r"<\?xml.*?\?>|<!DOCTYPE.*?>|<!--.*?-->", "", src, flags=_re.S)
    m = _re.search(r"<svg\b([^>]*)>(.*)</svg>", src, flags=_re.S)
    attrs, inner = m.group(1), m.group(2)
    vb = _re.search(r'viewBox="([^"]+)"', attrs)
    if vb:
        vx, vy, vw, vh = map(float, _re.split(r"[ ,]+", vb.group(1).strip()))
    else:
        num = lambda k: float(_re.search(k + r'="([\d.]+)', attrs).group(1))
        vx, vy, vw, vh = 0, 0, num("width"), num("height")
    inner = _re.sub(r'<metadata\b.*?</metadata>', "", inner, flags=_re.S)
    inner = _re.sub(r'\bid="([^"]+)"', lambda q: f'id="{prefix}{q.group(1)}"', inner)
    inner = _re.sub(r'url\(#([^)]+)\)', lambda q: f'url(#{prefix}{q.group(1)})', inner)
    inner = _re.sub(r'href="#([^"]+)"', lambda q: f'href="#{prefix}{q.group(1)}"', inner)
    k = min(w / vw, h / vh)
    ox, oy = x + (w - vw * k) / 2, y + (h - vh * k) / 2
    return f'<g transform="translate({ox:.2f},{oy:.2f}) scale({k:.5f}) translate({-vx},{-vy})">{inner}</g>'


def _brand_icon(file, box):
    def f():
        ic = Icon()
        page(ic)
        ic.add(_embed_svg(_os.path.join(BRAND_DIR, file), *box, prefix="brand-"))
        return ic
    return f


if _os.path.exists(_os.path.join(BRAND_DIR, "debian-openlogo-nd.svg")):
    MIMES["application-vnd.debian.binary-package"] = _brand_icon("debian-openlogo-nd.svg", (3, 10, 34, 42))
    for _a in ("application-x-deb", "application-x-debian-package"):
        MIME_ALIASES[_a] = "application-vnd.debian.binary-package"
    MIME_ALIASES.pop("application-vnd.debian.binary-package", None)


# ------------------------------------------------------------------ package formats, tagged
PACKAGES = {"application-x-rpm": ("rpm", "red"), "application-vnd.debian.binary-package": ("deb", "red")}
PACKAGE_ALIASES = {"application-x-rpm": ["application-x-source-rpm", "application-x-redhat-package-manager"],
                   "application-vnd.debian.binary-package": ["application-x-deb", "application-x-debian-package"]}
for name, (text, colour) in PACKAGES.items():
    if name in MIMES:          # an official logo from brand/ takes priority
        continue
    MIMES[name] = mime(e_box, e_label(text, colour))
    TAGS[name] = (text, colour)
    for a in PACKAGE_ALIASES[name]:
        MIME_ALIASES[a] = name
    MIME_ALIASES.pop(name, None)


# ------------------------------------------------------------------ app bundles
BUNDLES = {"application-vnd.flatpak": ("flatpak", "blue", "fpak"), "application-vnd.snap": ("snap", "orange", "snap")}
BUNDLE_ALIASES = {"application-vnd.flatpak": ["application-vnd.flatpak.ref", "application-vnd.flatpak.repo", "application-x-flatpak"],
                  "application-vnd.snap": ["application-x-snap"]}
for name, (text, colour, small) in BUNDLES.items():
    MIMES[name] = mime(e_box, e_label(text, colour))
    TAGS[name] = (text, colour)
    SMALL_TEXT[name] = small
    for a in BUNDLE_ALIASES[name]:
        MIME_ALIASES[a] = name
    MIME_ALIASES.pop(name, None)



# ------------------------------------------------------------------ more tagged formats
def m_formula(ic):
    """Formula page: a sum sign and a fraction among a few lines."""
    ic.add(f'<path d="M22,12H30L25.5,17.5L30,23H22M33,15H41M33,20H41M37,13V17M33,30H52M36,26H49M38,34.5H47" fill="none" stroke="{TEXT}" stroke-width="1.5" stroke-linejoin="round"/>')
    lines(ic, 21, 53, 40, 4, breaks=())


def e_pixels(ic):
    """Bitmap: a framed picture made of chunky pixels (sky, sun, hills)."""
    frame_d = "M2,18H38V48H2Z"
    ic.shadow(frame_d, 2.6, 2.2)
    ic.path(frame_d, ic.lg([(0, "#ffffff"), (1, "#c3c7cd")], 0, 0, 1, 1), INK, LW)
    rows = ["SSSSSSSYY", "SSSSSSYYY", "SSSSSSSYS", "SSGGSSSSS", "SGGGGSSGG", "GGGGGGGGG", "GGgGGGgGG"]
    col = {"S": "#7cc4f4", "Y": "#ffd23a", "G": "#4fae3a", "g": "#2e7a22"}
    for r, row in enumerate(rows):
        for c, ch in enumerate(row):
            ic.add(f'<rect x="{5 + c * 3.3:.1f}" y="{21 + r * 3.43:.2f}" width="3.3" height="3.43" fill="{col[ch]}"/>')
    ic.add(f'<path d="M5,21H34.7V45H5Z" fill="none" stroke="{INK}" stroke-width=".9"/>')


def _reg(name, emblems, text, colour, aliases=(), small=None, **label):
    MIMES[name] = mime(*emblems, e_label(text, colour, **label))
    TAGS[name] = (text, colour)
    if small:
        SMALL_TEXT[name] = small
    for a in aliases:
        if a not in MIMES:
            MIME_ALIASES[a] = name
    MIME_ALIASES.pop(name, None)


# images: the paint page, tagged
for name, text, colour, al in [
    ("image-png", "png", "blue", []), ("image-jpeg", "jpg", "orange", ["image-jpg", "image-pjpeg"]),
    ("image-gif", "gif", "green", []), ("image-tiff", "tif", "brown", ["image-x-tiff"]),
    ("image-webp", "webp", "teal", []), ("image-x-psd", "psd", "navy", ["image-vnd.adobe.photoshop", "image-psd", "application-photoshop"]),
    ("image-vnd.microsoft.icon", "ico", "amber", ["image-x-icon", "image-ico", "image-x-ico"]),
    ("image-x-tga", "tga", "violet", ["image-tga", "image-x-targa"]),
    ("image-x-xcf", "xcf", "slate", ["image-x-compressed-xcf"]), ("application-x-krita", "kra", "pink", ["image-x-krita"]),
    ("image-heif", "heic", "red", ["image-heic"]), ("image-avif", "avif", "cyan", []), ("image-jxl", "jxl", "lime", []),
    ("image-x-portable-pixmap", "ppm", "olive", ["image-x-portable-bitmap", "image-x-portable-graymap", "image-x-portable-anymap"]),
]:
    _reg(name, (lambda ic: e_scene(ic),), text, colour, al)
# bitmap gets its own picture
_reg("image-bmp", (e_pixels,), "bmp", "indigo", ["image-x-bmp", "image-x-win-bitmap", "image-x-win-bmp", "image-x-ms-bmp"])

# office: OpenDocument (our own, so the theme is complete without LibreOffice) and Microsoft formats
TEXT_PAGE, SHEET, SLIDE = (m_document,), (e_calc_sheet,), (e_slide,)
for name, base, text, colour, al in [
    ("application-vnd.oasis.opendocument.text", TEXT_PAGE, "odt", "blue", ["libreoffice-oasis-text", "libreoffice-text", "application-vnd.sun.xml.writer", "application-vnd.stardivision.writer"]),
    ("application-vnd.oasis.opendocument.text-template", TEXT_PAGE, "ott", "blue", ["libreoffice-oasis-text-template", "libreoffice-text-template", "application-vnd.sun.xml.writer.template"]),
    ("application-vnd.oasis.opendocument.spreadsheet", SHEET, "ods", "green", ["libreoffice-oasis-spreadsheet", "libreoffice-spreadsheet", "application-vnd.sun.xml.calc", "application-vnd.stardivision.calc"]),
    ("application-vnd.oasis.opendocument.spreadsheet-template", SHEET, "ots", "green", ["libreoffice-oasis-spreadsheet-template", "libreoffice-spreadsheet-template", "application-vnd.sun.xml.calc.template"]),
    ("application-vnd.oasis.opendocument.presentation", SLIDE, "odp", "orange", ["libreoffice-oasis-presentation", "libreoffice-presentation", "application-vnd.sun.xml.impress", "application-vnd.stardivision.impress"]),
    ("application-vnd.oasis.opendocument.presentation-template", SLIDE, "otp", "orange", ["libreoffice-oasis-presentation-template", "libreoffice-presentation-template", "application-vnd.sun.xml.impress.template"]),
    ("application-vnd.oasis.opendocument.graphics", (e_vector,), "odg", "gold", ["application-vnd.oasis.opendocument.drawing", "libreoffice-oasis-drawing", "libreoffice-drawing", "application-vnd.sun.xml.draw", "application-vnd.stardivision.draw"]),
    ("application-vnd.oasis.opendocument.graphics-template", (e_vector,), "otg", "gold", ["application-vnd.oasis.opendocument.drawing.template", "application-vnd.oasis.opendocument.draw.template", "application-vnd.oasis.opendocument.drawing-template", "libreoffice-oasis-drawing-template", "libreoffice-drawing-template", "application-vnd.sun.xml.draw.template"]),
    ("application-vnd.oasis.opendocument.formula", (m_formula,), "odf", "violet", ["application-vnd.oasis.opendocument.formula-template", "libreoffice-oasis-formula", "libreoffice-formula", "application-vnd.sun.xml.math", "application-vnd.stardivision.math", "application-x-kformula"]),
    ("application-vnd.oasis.opendocument.web-template", TEXT_PAGE, "oth", "teal", ["libreoffice-oasis-web-template"]),
    ("application-msword", TEXT_PAGE, "doc", "navy", ["application-vnd.ms-word", "application-msword-template", "application-wps-office.doc", "application-wps-office.dot"]),
    ("application-vnd.openxmlformats-officedocument.wordprocessingml.document", TEXT_PAGE, "docx", "navy",
     ["application-vnd.ms-word.document.macroenabled.12", "application-vnd.ms-word.template.macroenabled.12", "application-wps-office.docx", "application-wps-office.dotx",
      "application-vnd.openxmlformats-officedocument.wordprocessingml.template"]),
    ("application-vnd.ms-excel", SHEET, "xls", "lime", ["application-wps-office.xls", "application-wps-office.xlt"]),
    ("application-vnd.openxmlformats-officedocument.spreadsheetml.sheet", SHEET, "xlsx", "lime",
     ["application-vnd.ms-excel.sheet.macroenabled.12", "application-vnd.ms-excel.sheet.binary.macroenabled.12", "application-vnd.ms-excel.template.macroenabled.12",
      "application-vnd.ms-excel.addin.macroenabled.12", "application-wps-office.xlsx", "application-wps-office.xltx", "application-vnd.openxmlformats-officedocument.spreadsheetml.template"]),
    ("application-vnd.ms-powerpoint", SLIDE, "ppt", "crimson", ["application-wps-office.ppt", "application-wps-office.pot"]),
    ("application-vnd.openxmlformats-officedocument.presentationml.presentation", SLIDE, "pptx", "crimson",
     ["application-vnd.ms-powerpoint.presentation.macroenabled.12", "application-vnd.ms-powerpoint.slideshow.macroenabled.12", "application-vnd.ms-powerpoint.template.macroenabled.12",
      "application-vnd.ms-powerpoint.slide.macroenabled.12", "application-vnd.ms-powerpoint.addin.macroenabled.12", "application-wps-office.pptx", "application-wps-office.potx",
      "application-vnd.openxmlformats-officedocument.presentationml.slideshow", "application-vnd.openxmlformats-officedocument.presentationml.template"]),
    ("application-rtf", TEXT_PAGE, "rtf", "slate", ["text-rtf", "text-richtext", "text-enriched"]),
    ("text-csv", SHEET, "csv", "olive", ["text-tab-separated-values", "text-x-csv"]),
]:
    _reg(name, base, text, colour, al)

# archives: the compressed box (or the plain box for uncompressed tar), each with its own colour.
# The tag sits where the lower magenta mark would go, so tagged archives keep just the top one.
def e_squeeze_top(ic):
    ic.path("M1.5,13L13,1.5V13Z", ic.lg([(0, "#fbd0ff"), (.5, "#d050e8"), (1, "#7a1090")], 0, 0, 1, 1), INK, 1)


COMP = (e_box, e_squeeze)          # both magenta marks; the tag sits above the lower one
for name, base, text, colour, al in [
    ("application-zip", COMP, "zip", "blue", ["application-x-zip", "application-x-zip-compressed"]),
    ("application-x-7z-compressed", COMP, "7z", "green", []),
    ("application-vnd.rar", COMP, "rar", "violet", ["application-x-rar", "application-x-rar-compressed"]),
    ("application-x-compressed-tar", COMP, "tgz", "orange", []),
    ("application-x-bzip-compressed-tar", COMP, "tbz", "crimson", ["application-x-bzip2-compressed-tar"]),
    ("application-x-xz-compressed-tar", COMP, "txz", "teal", []),
    ("application-x-zstd-compressed-tar", COMP, "tzst", "brown", []),
    ("application-x-lzma-compressed-tar", COMP, "tlz", "indigo", ["application-x-lzip-compressed-tar"]),
    ("application-x-tarz", COMP, "taz", "slate", []),
    ("application-gzip", COMP, "gz", "amber", ["application-x-gzip"]),
    ("application-x-bzip", COMP, "bz2", "red", ["application-x-bzip2"]),
    ("application-x-xz", COMP, "xz", "cyan", []),
    ("application-zstd", COMP, "zst", "gold", ["application-x-zstd"]),
    ("application-x-lzma", COMP, "lzma", "magenta", ["application-x-lzip", "application-x-lzop", "application-x-tzo"]),
    ("application-x-compress", COMP, "z", "slate", []),
    ("application-vnd.ms-cab-compressed", COMP, "cab", "olive", ["application-x-cab"]),
    ("application-x-arj", COMP, "arj", "pink", ["application-arj", "application-x-arc"]),
    ("application-x-lha", COMP, "lha", "lime", ["application-x-lzh-compressed", "application-x-lharc"]),
    ("application-x-ms-wim", COMP, "wim", "navy", []),
    ("application-x-tar", (e_box,), "tar", "brown", ["application-x-gtar"]),
    ("application-x-cpio", (e_box,), "cpio", "grey", ["application-x-ar", "application-x-archive"]),
    ("application-x-java-archive", (e_box,), "jar", "orange", ["application-x-jar", "application-java-archive", "application-x-java", "application-x-java-applet"]),
]:
    if base is COMP:
        _reg(name, base, text, colour, al, x1=57, y1=47.5)
    else:
        _reg(name, base, text, colour, al)

# plain renames that point at icons we already have
for a, t in {
    "text-x-plain": "text-plain", "text-x-javascript": "application-javascript", "text-x-java-source": "text-x-java",
    "text-csharp": "text-x-csharp", "text-fortran": "text-x-fortran", "application-sql": "text-x-sql",
    "text-x-dtd": "application-xml", "application-xsd": "application-xml", "application-xslt+xml": "application-xml",
    "text-x-xslfo": "application-xml", "application-x-designer": "application-xml", "text-rdf": "application-xml",
    "text-rdf+xml": "application-xml", "application-mathml+xml": "application-xml", "application-x-xliff": "application-xml",
    "text-x-opml": "application-xml", "text-x-opml+xml": "application-xml", "text-sgml": "application-xml",
    "application-x-m4": "text-x-source", "text-x-gettext-translation": "text-x-source", "text-x-po": "text-x-source",
    "application-x-gettext-translation": "text-x-source", "text-x-ldif": "text-plain", "text-x-credits": "text-plain",
    "image-x-svg+xml": "image-svg+xml", "image-x-wmf": "image-svg+xml", "application-x-wmf": "image-svg+xml",
    "application-ogg": "audio-ogg", "audio-mp2": "audio-mpeg", "audio-x-mp2": "audio-mpeg", "audio-x-speex+ogg": "audio-ogg",
    "video-x-wmv": "video-x-ms-wmv", "video-x-ms-wmp": "video-x-ms-wmv", "application-x-flash-video": "video-x-flv",
    "application-x-compressed-iso": "application-x-cd-image", "application-vnd.efi.iso": "application-x-cd-image",
    "application-x-apple-diskimage": "application-x-cd-image", "application-x-cue": "application-x-cd-image",
    "application-certificate": "application-pgp-encrypted", "application-pkcs12": "application-pgp-encrypted",
    "application-pkcs7-mime": "application-pgp-encrypted", "application-pkix-cert": "application-pgp-encrypted",
    "application-pkix-cerl": "application-pgp-encrypted", "application-x-pem-key": "application-pgp-encrypted",
    "application-x-x509-user-cert": "application-pgp-encrypted", "application-x-pkcs7-certificates": "application-pgp-encrypted",
    "application-x-bzdvi": "application-x-dvi", "application-x-gzdvi": "application-x-dvi", "application-x-gzpostscript": "application-postscript",
    "message-x-gnu-rmail": "message-rfc822", "x-mail-distribution-list": "text-vcard", "x-office-contact": "text-vcard",
    "application-vnd.ms-publisher": "x-office-document", "vnd.ms-publisher": "x-office-document",
    "application-vnd.scribus": "x-office-document", "application-x-lyx": "text-x-tex",
}.items():
    if a not in MIMES:
        MIME_ALIASES[a] = t


# ------------------------------------------------------------------ picture emblem (replaces the paint drops)
def e_scene(ic):
    """A small framed photo: sky, sun and a cloud over green hills, with a tree in the foreground."""
    t = "translate(2,15) rotate(-5 18 15)"
    outer = "M0,0H37V31H0Z"
    ic.shadow(outer, 2.6, 2.2, transform=t)
    ic.add(f'<g transform="{t}">')
    ic.path(outer, ic.lg([(0, "#ffffff"), (.6, "#eef0f2"), (1, "#b4b9c0")], 0, 0, 1, 1), INK, LW)
    # sky
    ic.path("M3,3H34V27H3Z", ic.lg([(0, "#3a8ee0"), (.55, "#9ad0f8"), (1, "#e4f6ff")]), None)
    ic.path(circle(27, 9.5, 3.6), ic.rg([(0, "#fffbe0"), (.5, "#ffd23a"), (1, "#e88a10")], .4, .35, .7), "#a05a08", .6)
    ic.add('<path d="M6.5,11.5Q6.5,8.6 9.4,8.8Q10.4,6.4 13.2,7Q15.6,7.2 16,9.4Q18.4,9.4 18.4,11.5Z" fill="#ffffff" stroke="#9ab0c4" stroke-width=".5"/>')
    # hills: a darker far one, then bright near grass
    ic.path("M3,20Q10,15 17,18.5Q24,14 34,17.5V27H3Z", ic.lg([(0, "#6ab84a"), (1, "#2e7a26")]), None)
    ic.path("M3,23Q13,19.5 22,22.5Q28,21 34,22V27H3Z", ic.lg([(0, "#a8e060"), (1, "#4a9a28")]), None)
    # tree
    ic.path("M9.2,24V17.5H11.4V24Z", ic.lg([(0, "#a8682a"), (1, "#5a3010")], 0, 0, 1, 0), "#3a2008", .5)
    ic.path("M10.3,8.8C13.8,8.8 15.6,11.2 15.2,13.8C15,16.4 12.8,18.4 10.3,18.4C7.8,18.4 5.6,16.4 5.4,13.8C5,11.2 6.8,8.8 10.3,8.8Z",
            ic.rg([(0, "#a8e870"), (.55, "#3a9a2a"), (1, "#14561a")], .4, .3, .8), "#0e3a12", .7)
    ic.add('<path d="M7.4,12.2Q8.2,10.2 10.4,10" fill="none" stroke="#e4ffc0" stroke-opacity=".8" stroke-width=".9" stroke-linecap="round"/>')
    ic.add(f'<path d="M3,3H34V27H3Z" fill="none" stroke="{INK}" stroke-width=".8"/>')
    ic.add("</g>")


# ------------------------------------------------------------------ the rest of the archive formats shared-mime-info knows
for name, base, text, colour, al in [
    ("application-x-ace", COMP, "ace", "crimson", []),
    ("application-x-arc", COMP, "arc", "teal", []),
    ("application-x-lzip", COMP, "lz", "indigo", []),
    ("application-x-lzop", COMP, "lzo", "magenta", []),
    ("application-x-tzo", COMP, "tzo", "pink", []),
    ("application-x-lz4", COMP, "lz4", "cyan", []),
    ("application-x-lz4-compressed-tar", COMP, "tlz4", "cyan", []),
    ("application-x-bzip3", COMP, "bz3", "red", []),
    ("application-x-bzip3-compressed-tar", COMP, "tbz3", "crimson", []),
    ("application-x-lrzip", COMP, "lrz", "olive", []),
    ("application-x-lrzip-compressed-tar", COMP, "tlrz", "olive", []),
    ("application-x-cpio-compressed", COMP, "cpio", "grey", []),
    ("application-x-xar", COMP, "xar", "navy", []),
    ("application-x-alz", COMP, "alz", "lime", []),
    ("application-x-zoo", COMP, "zoo", "gold", []),
    ("application-x-zpaq", COMP, "zpaq", "violet", []),
    ("application-x-stuffit", COMP, "sit", "orange", []),
    ("application-x-stuffitx", COMP, "sitx", "orange", []),
    ("application-x-dar", COMP, "dar", "brown", []),
    ("application-x-pak", COMP, "pak", "amber", []),
    ("application-vnd.squashfs", COMP, "sqfs", "teal", []),
    ("application-x-archive", (e_box,), "ar", "slate", ["application-x-ar"]),
    ("application-x-shar", (e_box,), "shar", "green", []),
    ("application-x-asar", (e_box,), "asar", "blue", []),
    ("application-x-msi", (e_box,), "msi", "navy", ["application-msix", "application-msixbundle"]),
]:
    if base is COMP:
        _reg(name, base, text, colour, al, x1=57, y1=47.5)
    else:
        _reg(name, base, text, colour, al)
for a, t in {"application-x-bzip1": "application-x-bzip", "application-x-bzip1-compressed-tar": "application-x-bzip-compressed-tar",
             "application-x-ustar": "application-x-tar", "application-x-bcpio": "application-x-cpio", "application-x-sv4cpio": "application-x-cpio",
             "application-x-sv4crc": "application-x-cpio"}.items():
    if a not in MIMES:
        MIME_ALIASES[a] = t



# ------------------------------------------------------------------ executables: the original's gear, seen at an angle
def exe3d():
    """The KDE Classic program gear in 3/4 view: a thick silver gear lying tilted back, with the
    orange dish and its centre hole, side walls showing below the teeth."""
    ic = Icon()
    cx, cy, R, r, n, sq, depth = 32, 28, 28.5, 22, 8, .8, 6
    pts = []
    for k in range(n):
        a = 2 * math.pi * k / n + math.pi / n
        for da, rad in ((-.24, r), (-.15, R), (.15, R), (.24, r)):
            pts.append((rad * math.cos(a + da), rad * math.sin(a + da)))
    def ring(dy=0.0):
        return "M" + "L".join(f"{cx + x:.2f},{cy + y * sq + dy:.2f}" for x, y in pts) + "Z"
    ic.shadow(ring(depth), 3, 2.6)
    # side walls: the outline repeated downward, darkest at the bottom
    steps = 12
    for i in range(steps, 0, -1):
        dy = depth * i / steps
        shade = int(0x5c + (0x9a - 0x5c) * (1 - i / steps))
        ic.add(f'<path d="{ring(dy)}" fill="#{shade:02x}{shade + 4:02x}{shade + 10:02x}"/>')
    ic.path(ring(depth), "none", INK, LW * 1.2)
    # top face
    ic.path(ring(), ic.rg([(0, "#ffffff"), (.55, "#dfe2e6"), (1, "#8a9098")], .4, .3, .8), INK, LW * 1.1)
    # orange dish (concave: darker at the top, lit at the bottom), with a silver rim
    rx, ry = 15, 15 * sq
    ic.path(f"M{cx - rx - 2},{cy}A{rx + 2},{ry + 1.6} 0 1 0 {cx + rx + 2},{cy}A{rx + 2},{ry + 1.6} 0 1 0 {cx - rx - 2},{cy}Z",
            ic.lg([(0, "#8a9098"), (1, "#ffffff")]), INK, 1)
    ic.path(f"M{cx - rx},{cy}A{rx},{ry} 0 1 0 {cx + rx},{cy}A{rx},{ry} 0 1 0 {cx - rx},{cy}Z",
            ic.lg([(0, "#b8600c"), (.35, "#f0a040"), (1, "#ffe8c0")]), INK, .9)
    ic.add(f'<path d="M{cx - rx + 2.5},{cy + 2}Q{cx},{cy + ry + 2.5} {cx + rx - 2.5},{cy + 2}" fill="none" stroke="#fff1d8" stroke-opacity=".8" stroke-width="1.2"/>')
    ic.path(f"M{cx - 3},{cy + .6}A3,{3 * sq} 0 1 0 {cx + 3},{cy + .6}A3,{3 * sq} 0 1 0 {cx - 3},{cy + .6}Z", "#2c1a0c", None)
    ic.add(f'<path d="M{cx - 2.6},{cy + 1.4}Q{cx},{cy + 3.4} {cx + 2.6},{cy + 1.4}" fill="none" stroke="#ffd8a0" stroke-width=".7"/>')
    # a glint along the near teeth
    ic.add(f'<path d="M{cx - 20},{cy - 8}Q{cx - 10},{cy - 15} {cx + 2},{cy - 15}" fill="none" stroke="#fff" stroke-opacity=".7" stroke-width="1.6" stroke-linecap="round"/>')
    return ic



def exe_tilt(sq=.86, depth=2.6):
    """The flat program gear, tilted back a little: same teeth and orange centre, slightly foreshortened,
    with a thin edge showing below."""
    ic = Icon()
    cx, cy, R, r, n = 32, 30, 27, 20.25, 8
    pts = []
    for k in range(n):
        a = 2 * math.pi * k / n
        for da, rad in ((-.2, r), (-.13, R), (.13, R), (.2, r)):
            pts.append((rad * math.cos(a + da), rad * math.sin(a + da)))
    ring = lambda dy=0.0: "M" + "L".join(f"{cx + x:.2f},{cy + y * sq + dy:.2f}" for x, y in pts) + "Z"
    ell = lambda rr, dy=0.0: (f"M{cx - rr},{cy + dy}A{rr},{rr * sq} 0 1 0 {cx + rr},{cy + dy}"
                              f"A{rr},{rr * sq} 0 1 0 {cx - rr},{cy + dy}Z")
    ic.shadow(ring(depth), 3, 2.6)
    if depth:
        for i in range(8, 0, -1):
            v = int(0x6c + (0x9a - 0x6c) * (1 - i / 8))
            ic.add(f'<path d="{ring(depth * i / 8)}" fill="#{v:02x}{v + 4:02x}{v + 10:02x}"/>')
        ic.path(ring(depth), "none", INK, LW * 1.4)
    ic.path(ring(), ic.rg([(0, "#ffffff"), (.6, "#c3c7cd"), (1, "#6c727a")], .35, .3, .8), INK, LW * 1.4)
    ic.path(ell(14.25), ic.rg([(0, "#ffe2b0"), (.55, "#e89a3a"), (1, "#8a4c10")], .4, .35, .75), INK, 1.4)
    ic.path(ell(3.9), "#2c2016", None)
    ic.add(f'<path d="M{cx - 9},{cy - 6 * sq}Q{cx - 6},{cy - 11.2 * sq} {cx},{cy - 11.4 * sq}" fill="none" stroke="#fff" stroke-opacity=".8" stroke-width="2" stroke-linecap="round"/>')
    return ic



def gear_tilted(ic, cx, cy, R, sq=.8, depth=3.4, axis="y", lw=LW * 1.4):
    """The program gear tilted back. axis="y": leans back (foreshortened top to bottom, edge below);
    axis="x": turned to the right (foreshortened side to side, edge on the right), as on the makefile icon."""
    r, n = R * .75, 8
    pts = []
    for k in range(n):
        a = 2 * math.pi * k / n
        for da, rad in ((-.2, r), (-.13, R), (.13, R), (.2, r)):
            pts.append((rad * math.cos(a + da), rad * math.sin(a + da)))
    if axis == "y":
        P = lambda x, y, d=0.0: (cx + x, cy + y * sq + d)
    else:
        P = lambda x, y, d=0.0: (cx + x * sq + d, cy + y)
    ring = lambda d=0.0: "M" + "L".join(f"{a:.2f},{b:.2f}" for a, b in (P(x, y, d) for x, y in pts)) + "Z"
    def ell(rr, d=0.0):
        rx, ry = (rr, rr * sq) if axis == "y" else (rr * sq, rr)
        x0, y0 = P(0, 0, d)
        return f"M{x0 - rx:.2f},{y0:.2f}A{rx:.2f},{ry:.2f} 0 1 0 {x0 + rx:.2f},{y0:.2f}A{rx:.2f},{ry:.2f} 0 1 0 {x0 - rx:.2f},{y0:.2f}Z"
    ic.shadow(ring(depth), 3, 2.6)
    for i in range(8, 0, -1):
        v = int(0x6c + (0x9a - 0x6c) * (1 - i / 8))
        ic.add(f'<path d="{ring(depth * i / 8)}" fill="#{v:02x}{v + 4:02x}{v + 10:02x}"/>')
    ic.path(ring(depth), "none", INK, lw)
    ic.path(ring(), ic.rg([(0, "#ffffff"), (.6, "#c3c7cd"), (1, "#6c727a")], .35, .3, .8), INK, lw)
    ic.path(ell(R * .528), ic.rg([(0, "#ffe2b0"), (.55, "#e89a3a"), (1, "#8a4c10")], .4, .35, .75), INK, lw * .72)
    ic.path(ell(R * .145), "#2c2016", None)
    g = lambda x, y: "{:.2f},{:.2f}".format(*P(x, y))
    ic.add(f'<path d="M{g(-R * .33, -R * .26)}Q{g(-R * .22, -R * .44)} {g(0, -R * .45)}" fill="none" stroke="#fff" stroke-opacity=".8" stroke-width="{lw * 1.05:.2f}" stroke-linecap="round"/>')


GEAR_STYLE = "tilt"     # "tilt" (current) or "flat" (the first redraw, kept so it can be switched back)


def exe_icon():
    if GEAR_STYLE == "flat":
        return exe()
    ic = Icon()
    gear_tilted(ic, 32, 30, 27, .8, 3.4, "y")
    return ic


def e_gear_doc(ic):
    """Makefile gear: turned to the right over the page, its edge and a soft shadow falling on the page."""
    if GEAR_STYLE == "flat":
        return e_gear(ic)
    # soft shadow on the page to the right of the gear
    for rx, op in ((17, .08), (15, .1), (13, .12), (11, .12)):
        ic.add(f'<path d="M{26 - rx * .62:.1f},{33.5}A{rx * .62:.1f},{rx:.1f} 0 1 0 {26 + rx * .62:.1f},{33.5}A{rx * .62:.1f},{rx:.1f} 0 1 0 {26 - rx * .62:.1f},{33.5}Z" fill="#3a2a10" fill-opacity="{op}"/>')
    gear_tilted(ic, 17, 30, 18.5, .8, 3.2, "x", lw=LW)      # centred on the page's left edge, as in the original


MIMES["application-x-executable"] = exe_icon
MIMES["text-x-makefile"] = mime(e_gear_doc)



# ------------------------------------------------------------------ Windows programs and scripts
def exe_tagged(text, colour):
    """The tilted program gear with a tag, for Windows and DOS programs."""
    def f():
        ic = exe_icon()
        e_label(text, colour)(ic)
        return ic
    return f


# One MIME type covers .exe, .dll, .sys, .cpl, .scr and .ocx (they are all "portable executables"),
# so these files share an icon; it is tagged "win" (Windows) rather than naming one extension.
for name, text, colour, al in [
    ("application-vnd.microsoft.portable-executable", "win", "blue", ["application-x-msdownload", "application-x-ms-ne-executable",
                                                                      "application-x-ms-dos-executable", "application-x-msdos-program", "application-x-dosexec"]),
]:
    MIMES[name] = exe_tagged(text, colour)
    TAGS[name] = (text, colour)
    for a in al:
        MIME_ALIASES[a] = name
    MIME_ALIASES.pop(name, None)
for name, base, text, colour, al in [
    ("application-x-bat", (e_terminal,), "bat", "slate", ["application-bat", "application-x-cmd"]),
    ("application-x-powershell", (e_terminal,), "ps1", "navy", []),
    ("text-vbscript", (e_terminal,), "vbs", "violet", ["text-x-vbscript"]),
    ("text-x-ms-regedit", (m_source,), "reg", "teal", []),
    ("application-x-ms-shortcut", (lambda ic: lines(ic, 21, 53, 19, 11, breaks=(5,)),), "lnk", "grey", []),
]:
    _reg(name, base, text, colour, al)



def e_bomb2(ic):
    """Crash-dump bomb, as in the original: the fuse end points up and to the left, set into the
    sphere through a short metal collar, with a burst of sparks at the tip."""
    cx, cy, R = 26, 35, 17.5
    L = 5.2                                   # how far the collar stands out from the sphere
    g = f'<g transform="translate({cx},{cy}) rotate(-135)">'
    # collar and fuse in the bomb's own frame (x points out along the fuse); drawn before the sphere
    # so the sphere covers the collar's base and it sits into the bomb
    ic.add(g)
    ic.path(f"M{R - 4},-3.6H{R + L}V3.6H{R - 4}Z", ic.lg([(0, "#4c5158"), (.45, "#d4d7dc"), (1, "#4c5158")], 0, 0, 0, 1), INK, 1)
    ic.path(f"M{R + L - 1.3},0A1.3,3.6 0 1 0 {R + L + 1.3},0A1.3,3.6 0 1 0 {R + L - 1.3},0Z", ic.lg([(0, "#c3c7cd"), (1, "#5c6168")]), INK, .9)
    ic.add(f'<path d="M{R + L},0Q{R + L + 4},-.4 {R + L + 7},-2.6" fill="none" stroke="{INK}" stroke-width="2.8" stroke-linecap="round"/>')
    ic.add(f'<path d="M{R + L},0Q{R + L + 4},-.4 {R + L + 7},-2.6" fill="none" stroke="#b89060" stroke-width="1.4" stroke-linecap="round"/>')
    ic.add("</g>")
    f = frame(cx, cy, -135)
    tx, ty = f(R + L + 7, -2.6)
    bx, by = f(R + L + 7.6, -2.6)          # the burst is centred a little beyond the tip, away from the bomb
    # bomb
    ic.shadow(circle(cx, cy, R), 2.6, 2.2)
    ic.path(circle(cx, cy, R), ic.rg([(0, "#a8aeb6"), (.3, "#4c5158"), (.75, "#16181c"), (1, "#060708")], .32, .3, .8), INK, LW)
    # sparks: a speckled burst of yellow, orange and red around the tip, like the original
    import random
    rnd = random.Random(7)
    for k in range(130):
        ang = rnd.uniform(0, 2 * math.pi)
        d = abs(rnd.gauss(0, 4.4))
        x, y = bx + d * math.cos(ang), by + d * math.sin(ang) * .9
        col = rnd.choice(["#ffe23a", "#ffb020", "#ff7a10", "#e8301a", "#fff6a0", "#ff9a20"])
        sz = rnd.uniform(.8, 1.6)
        ic.add(f'<rect x="{x - sz / 2:.2f}" y="{y - sz / 2:.2f}" width="{sz:.2f}" height="{sz:.2f}" fill="{col}"/>')
    ic.path(circle(round(tx, 2), round(ty, 2), 1.8), "#fffbe0", None)


MIMES["application-x-core"] = mime(e_bomb2)
MIME_ALIASES["text-vnd.kde.kcrash-report"] = "application-x-core"


# ================================================================== group 2: formats that are new since KDE 3
def e_font(ic):
    """Fonts: a big serif capital A and a small a, in deep blue."""
    A = ("M3,50L15.5,13H22L34.5,50H27.5L24.6,41H12.9L10,50Z M14.8,35H22.7L18.8,22.6Z")
    ic.shadow(A, 2.6, 2.2)
    ic.path(A, ic.lg([(0, "#6a8ae8"), (.5, "#1a3a9a"), (1, "#0a1a50")], 0, 0, 1, 1), INK, LW, ' fill-rule="evenodd"')
    ic.add(f'<path d="M1,50.5H11.5M24,50.5H36.5" stroke="{INK}" stroke-width="2.4" stroke-linecap="round"/>')   # serifs
    a = ("M41.8,50V47.8Q40,50.5 36.8,50.5Q32.2,50.5 32.2,46.2Q32.2,41.6 39,41.2L41.6,41V40.2Q41.6,37.6 38.6,37.6Q36.2,37.6 34.4,39L33.4,36.4"
         "Q35.8,34.8 39.2,34.8Q45,34.8 45,40.4V50Z M41.6,43.4L39.6,43.6Q35.8,43.8 35.8,46Q35.8,48 38,48Q41.6,48 41.6,44.6Z")
    ic.path(a, ic.lg([(0, "#6a8ae8"), (1, "#0a1a50")]), INK, 1, ' fill-rule="evenodd"')
    ic.add('<path d="M16.6,16L7.6,44" stroke="#fff" stroke-opacity=".35" stroke-width="1.4" stroke-linecap="round"/>')


def e_subtitles(ic):
    """Subtitles: a dark film frame with two white caption lines across the bottom."""
    fr = "M2,17H40V45H2Z"
    ic.shadow(fr, 2.6, 2.2)
    ic.path(fr, ic.lg([(0, "#4c5868"), (.6, "#1a2028"), (1, "#060809")], 0, 0, 1, 1), INK, LW)
    ic.add('<path d="M3,18H39V28Q21,33 3,28Z" fill="#fff" fill-opacity=".08"/>')
    for y, x0, x1 in ((35, 8, 34), (40.5, 12, 30)):
        ic.add(f'<path d="M{x0},{y}H{x1}" stroke="#000" stroke-opacity=".5" stroke-width="4.2" stroke-linecap="round"/>')
        ic.add(f'<path d="M{x0},{y}H{x1}" stroke="#ffffff" stroke-width="2.6" stroke-linecap="round"/>')


def e_database(ic):
    """Databases: the classic stacked cylinder, three bands, teal-blue."""
    cx, rx, ry, top, bot = 20, 16, 5.5, 16, 50
    body = f"M{cx - rx},{top}V{bot}A{rx},{ry} 0 0 0 {cx + rx},{bot}V{top}Z"
    ic.shadow(body + f"M{cx - rx},{top}A{rx},{ry} 0 1 0 {cx + rx},{top}A{rx},{ry} 0 1 0 {cx - rx},{top}Z", 2.4, 2)
    side = ic.lg([(0, "#1a5a7a"), (.35, "#5ab8d8"), (.6, "#2a88b0"), (1, "#0a3448")], 0, 0, 1, 0)
    ic.path(body, side, INK, LW)
    for y in (27.3, 38.6):
        ic.add(f'<path d="M{cx - rx},{y}A{rx},{ry} 0 0 0 {cx + rx},{y}" fill="none" stroke="{INK}" stroke-width="1"/>')
        ic.add(f'<path d="M{cx - rx + 1},{y + 1.8}A{rx - 1},{ry - .6} 0 0 0 {cx + rx - 1},{y + 1.8}" fill="none" stroke="#bff0ff" stroke-opacity=".5" stroke-width=".9"/>')
    ic.path(f"M{cx - rx},{top}A{rx},{ry} 0 1 0 {cx + rx},{top}A{rx},{ry} 0 1 0 {cx - rx},{top}Z",
            ic.rg([(0, "#e8fbff"), (.6, "#8ad4ec"), (1, "#3a98c0")], .4, .35, .8), INK, LW)


def e_ebook(ic):
    """E-books: a closed hardback book seen at an angle, coloured cover, page edges along the side."""
    cover = "M6,14L30,10V48L6,52Z"
    pages = "M30,10L36,13V51L30,48Z"
    ic.shadow(cover + pages, 2.6, 2.2)
    ic.path(pages, ic.lg([(0, "#ffffff"), (1, "#d8d0c0")], 0, 0, 1, 0), INK, 1)
    ic.add('<path d="M31.5,12.5V48.6M33,13.4V49.4M34.5,14.2V50.2" stroke="#b8ae98" stroke-width=".6"/>')
    ic.path("M6,52L30,48L36,51L12,55Z", ic.lg([(0, "#f4f0e8"), (1, "#c8bea8")]), INK, 1)
    ic.path(cover, ic.lg([(0, "#ff9a7a"), (.5, "#c8301a"), (1, "#6a0a04")], 0, 0, 1, 1), INK, LW)
    ic.add('<path d="M9.5,14.6V50.4" stroke="#4a0804" stroke-width="1.2"/>')                     # spine edge
    ic.add('<path d="M13,22L26,20M13,26L23,24.4" stroke="#ffd890" stroke-width="1.4" stroke-linecap="round"/>')   # title
    ic.add('<path d="M11.5,16.5L27.5,13.7" stroke="#fff" stroke-opacity=".4" stroke-width="1.2"/>')


def e_vmdisk(ic):
    """Virtual machine disks: the redrawn hard disk, smaller, on the page."""
    from devices import harddisk
    ic.add('<g transform="translate(-1,10) scale(.68)">')
    harddisk(ic)
    ic.add("</g>")


def e_torrent(ic):
    """Torrents and partial downloads: a green arrow coming down onto the page."""
    d = "M13,14H25V30H33L19,46L5,30H13Z"
    ic.shadow(d, 2.6, 2.2)
    ic.path(d, ic.lg([(0, "#b4f0a0"), (.5, "#3fae2a"), (1, "#1e6a10")]), INK, LW)
    ic.add('<path d="M14.6,16H23.4" stroke="#fff" stroke-opacity=".6" stroke-width="1.3"/>')
    ic.add(f'<path d="M5,50.5H24" stroke="{INK}" stroke-width="3.6" stroke-linecap="round"/>')
    ic.add('<path d="M5,50.5H24" stroke="#9aa0a8" stroke-width="1.8" stroke-linecap="round"/>')


GROUP2 = [
    # fonts
    ("font-ttf", (e_font,), "ttf", "blue", ["application-x-font-ttf", "application-x-font-ttx", "font-collection", "application-x-font-truetype"]),
    ("font-otf", (e_font,), "otf", "violet", ["application-x-font-otf", "application-vnd.ms-opentype", "font-opentype"]),
    ("font-woff", (e_font,), "woff", "teal", []), ("font-woff2", (e_font,), "woff2", "teal", []),
    ("application-x-font-type1", (e_font,), "pfb", "brown", ["application-x-font-afm", "application-x-font-speedo", "application-font-tdpfr"]),
    ("application-x-font-pcf", (e_font,), "pcf", "slate", ["application-x-font-bdf", "application-x-font-snf", "application-x-font-linux-psf", "application-x-gz-font-linux-psf"]),
    # subtitles
    ("application-x-subrip", (e_subtitles,), "srt", "blue", ["application-x-srt", "text-x-srt", "application-x-srtrip"]),
    ("text-vtt", (e_subtitles,), "vtt", "green", []), ("text-x-ssa", (e_subtitles,), "ass", "violet", []),
    ("text-x-microdvd", (e_subtitles,), "sub", "orange", ["text-x-subviewer", "text-x-mpsub", "text-x-mpl2"]),
    ("application-x-sami", (e_subtitles,), "smi", "teal", ["application-ttml+xml"]),
    # databases
    ("application-vnd.sqlite3", (e_database,), "db", "teal", ["application-x-sqlite3", "application-x-sqlite2", "application-sql-database"]),
    ("application-vnd.oasis.opendocument.database", (e_database,), "odb", "blue", ["libreoffice-oasis-database", "libreoffice-database"]),
    ("application-vnd.ms-access", (e_database,), "mdb", "crimson", ["application-x-msaccess", "application-msaccess"]),
    ("application-vnd.dbf", (e_database,), "dbf", "olive", ["application-x-dbf", "application-dbf"]),
    ("application-x-kexiproject-sqlite3", (e_database,), "kexi", "green", ["application-x-kexiproject-sqlite2", "application-x-kexiproject-sqlite",
                                                                             "application-x-kexiproject-shortcut", "application-x-kexi-connectiondata"]),
    # e-books and comics
    ("application-epub+zip", (e_ebook,), "epub", "green", []),
    ("application-x-fictionbook+xml", (e_ebook,), "fb2", "orange", ["application-x-zip-compressed-fb2"]),
    ("application-x-mobipocket-ebook", (e_ebook,), "mobi", "amber", ["application-vnd.amazon.mobi8-ebook"]),
    ("image-vnd.djvu", (e_ebook,), "djvu", "slate", ["image-vnd.djvu+multipage", "image-x-djvu"]),
    ("application-vnd.ms-htmlhelp", (e_ebook,), "chm", "blue", ["application-x-chm"]),
    ("application-vnd.comicbook+zip", (e_ebook,), "cbz", "pink", ["application-x-cbz"]),
    ("application-vnd.comicbook-rar", (e_ebook,), "cbr", "violet", ["application-x-cbr"]),
    ("application-x-cb7", (e_ebook,), "cb7", "teal", []), ("application-x-cbt", (e_ebook,), "cbt", "brown", []),
    # virtual machine and raw disk images
    ("application-x-qemu-disk", (e_vmdisk,), "qcow2", "orange", []),
    ("application-x-vdi-disk", (e_vmdisk,), "vdi", "blue", ["application-x-virtualbox-vdi", "virtualbox-vdi", "virtualbox-hdd"]),
    ("application-x-vmdk-disk", (e_vmdisk,), "vmdk", "slate", ["application-x-virtualbox-vmdk", "virtualbox-vmdk"]),
    ("application-x-vhd-disk", (e_vmdisk,), "vhd", "navy", ["application-x-virtualbox-vhd", "virtualbox-vhd"]),
    ("application-x-vhdx-disk", (e_vmdisk,), "vhdx", "navy", []),
    ("application-ovf", (e_vmdisk,), "ova", "teal", ["application-x-virtualbox-ova", "virtualbox-ova", "application-x-virtualbox-ovf", "virtualbox-ovf"]),
    ("application-x-raw-disk-image", (e_vmdisk,), "img", "grey", ["application-x-raw-disk-image-xz-compressed"]),
    # downloads
    ("application-x-bittorrent", (e_torrent,), "torrent", "green", []),
    ("application-x-partial-download", (e_torrent,), "part", "amber", []),
]
G2_SMALL = {"application-x-qemu-disk": "qcow", "application-x-bittorrent": "tor"}
for name, base, text, colour, al in GROUP2:
    if base == (e_font,):       # fonts: tag up on the right so it doesn't cover the letters
        _reg(name, base, text, colour, al, small=G2_SMALL.get(name), x1=57, y1=31)
    else:
        _reg(name, base, text, colour, al, small=G2_SMALL.get(name))



# ------------------------------------------------------------------ generic font file, and the System Settings font icons
MIMES["font-x-generic"] = mime(e_font)
for _a in ("fonts-package", "application-x-font", "font-generic"):
    MIME_ALIASES[_a] = "font-x-generic"
MIME_ALIASES.pop("font-x-generic", None)


def _tt(ic, badge=None):
    """KDE 3's fonts icon, redrawn over lines traced from the original: two serif T's in isometric view,
    a black one behind and a red one in front. Each letter stands in a plane running back to the right
    (x along 30 degrees), extruded back and up so its lit top faces show white and its right sides grey."""
    T = [(0, 0), (25, 0), (25, 9.5), (23.2, 7.4), (20, 6), (15, 6), (15, 30.5), (16.8, 32.4), (20.5, 33.4), (20.5, 35),
         (3, 35), (3, 33.4), (6.7, 32.4), (8.5, 30.5), (8.5, 6), (5, 6), (1.8, 7.4), (0, 9.5)]
    ux, uy = .866, .5                 # the letter's x axis on screen
    wx, wy = 4.6, -2.65               # extrusion (depth) on screen
    def inside(px, py, poly):
        c = False
        for i in range(len(poly)):
            (x0, y0), (x1, y1) = poly[i], poly[i - 1]
            if (y0 > py) != (y1 > py) and px < x0 + (py - y0) * (x1 - x0) / (y1 - y0):
                c = not c
        return c
    P = lambda pts: "M" + "L".join(f"{x:.2f},{y:.2f}" for x, y in pts) + "Z"
    top = ic.lg([(0, "#ffffff"), (.6, "#f0f1f3"), (1, "#c3c7cd")], 0, 0, 1, 1)
    right = ic.lg([(0, "#e4e6e9"), (.5, "#c3c7cd"), (1, "#8a9098")], 0, 0, 0, 1)
    faces = (((26.5, 9.5), ic.lg([(0, "#3c4148"), (.2, "#141618"), (1, "#000000")], 0, 0, 1, 1)),
             ((10, 16), ic.lg([(0, "#ff8a7a"), (.3, "#f01a0a"), (1, "#8a0402")], 0, 0, 1, 1)))
    for (ox, oy), face in faces:
        f = [(ox + U * ux, oy + U * uy + V) for U, V in T]
        back = [(x + wx, y + wy) for x, y in f]
        ic.shadow(P(f) + P(back), 2.4, 2)
        ic.path(P(back), right, INK, LW)
        for i in range(len(f)):
            a, b = f[i - 1], f[i]
            ex, ey = b[0] - a[0], b[1] - a[1]
            L = math.hypot(ex, ey) or 1
            nx, ny = ey / L, -ex / L
            mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
            if inside(mx + nx * .3, my + ny * .3, f):
                nx, ny = -nx, -ny
            if nx * wx + ny * wy <= 0:
                continue                      # this side faces away from us
            quad = [a, b, (b[0] + wx, b[1] + wy), (a[0] + wx, a[1] + wy)]
            ic.add(f'<path d="{P(quad)}" fill="{top if ny < -abs(nx) * .6 else right}" stroke="{INK}" stroke-width="1" stroke-linejoin="round"/>')
        ic.add(f'<path d="{P(f)}" fill="{face}" stroke="{INK}" stroke-width="{LW}" stroke-linejoin="round"/>')
        hl = [(ox + U * ux, oy + U * uy + V) for U, V in ((1.6, 1.4), (23.4, 1.4))]
        ic.add(f'<path d="{P(hl)[:-1]}" stroke="#fff" stroke-opacity=".5" stroke-width="1.2" stroke-linecap="round"/>')
    if badge == "install":
        ic.shadow(circle(51, 51, 10), 1.6, 1.4)
        ic.path(circle(51, 51, 10), ic.rg([(0, "#d4f8c0"), (.55, "#3fae2a"), (1, "#14561a")], .4, .35, .75), INK, LW)
        ic.add('<path d="M51,45V57M45,51H57" stroke="#000" stroke-opacity=".3" stroke-width="5" stroke-linecap="round"/>')
        ic.add('<path d="M51,45V57M45,51H57" stroke="#fff" stroke-width="3.2" stroke-linecap="round"/>')


def _aa(ic, badge=None):
    """The "Aa" on its own (no page), larger: System Settings' Fonts and Font Management."""
    ic.add('<g transform="translate(31,30) scale(1.28) translate(-23,-32)">')
    e_font(ic)
    ic.add("</g>")
    if badge == "install":      # a green plus in a disc, lower right
        ic.shadow(circle(51, 51, 10), 1.6, 1.4)
        ic.path(circle(51, 51, 10), ic.rg([(0, "#d4f8c0"), (.55, "#3fae2a"), (1, "#14561a")], .4, .35, .75), INK, LW)
        ic.add('<path d="M51,45V57M45,51H57" stroke="#000" stroke-opacity=".3" stroke-width="5" stroke-linecap="round"/>')
        ic.add('<path d="M51,45V57M45,51H57" stroke="#fff" stroke-width="3.2" stroke-linecap="round"/>')


def _app(fn, **kw):
    def f():
        ic = Icon()
        fn(ic, **kw)
        return ic
    return f


APPS = {"preferences-desktop-font": _app(_tt), "preferences-desktop-font-installer": _app(_tt, badge="install")}
APP_ALIASES = {"font": "preferences-desktop-font", "fonts": "preferences-desktop-font", "kfontview": "preferences-desktop-font",
               "org.kde.kfontview": "preferences-desktop-font", "kcmfontinst": "preferences-desktop-font-installer",
               "kfontinst": "preferences-desktop-font-installer"}


def write_apps(out):
    import os
    d = f"{out}/scalable/apps"
    os.makedirs(d, exist_ok=True)
    for name, fn in APPS.items():
        open(f"{d}/{name}.svg", "w").write(fn().svg(64))
    for a, t in APP_ALIASES.items():
        if not os.path.exists(f"{d}/{a}.svg"):
            os.symlink(f"{t}.svg", f"{d}/{a}.svg")


# ================================================================== small groups: ROMs, feeds, VPN, apps, colour, GPS, Arduino
def e_cartridge(ic):
    """Game ROMs: a generic grey game cartridge with a coloured label, grip ridges and gold contacts."""
    body = "M4,16Q4,13 7,13H33Q36,13 36,16V46H31V50H9V46H4Z"
    ic.shadow(body, 2.6, 2.2)
    ic.path(body, ic.lg([(0, "#e4e6e9"), (.5, "#b4b9c0"), (1, "#6c727a")], 0, 0, 1, 1), INK, LW)
    ic.path("M8.5,17H31.5V36H8.5Z", ic.lg([(0, "#ff9a7a"), (.5, "#c8301a"), (1, "#6a0a04")], 0, 0, 1, 1), INK, .9)
    ic.add('<path d="M11.5,21.5H24M11.5,25H20" stroke="#ffe0a0" stroke-width="1.6" stroke-linecap="round"/>')
    ic.add('<path d="M9,17.5H31L9,33Z" fill="#fff" fill-opacity=".18"/>')
    ic.add(f'<path d="M8,39.5H32M8,42.2H32" stroke="#7b818a" stroke-width="1"/>')
    for k in range(6):
        ic.add(f'<rect x="{10.4 + k * 3.3:.1f}" y="46.6" width="2" height="3" fill="#e8c43a" stroke="#7a5a04" stroke-width=".4"/>')


def e_feed(ic):
    """Web feeds: the orange feed square with its dot and two waves."""
    sq = rrect(4, 18, 30, 30, 5)
    ic.shadow(sq, 2.6, 2.2)
    ic.path(sq, ic.lg([(0, "#ffc070"), (.5, "#f07a10"), (1, "#a83c04")], 0, 0, 1, 1), INK, LW)
    ic.add('<path d="M8,22H30V30Q19,34 8,30Z" fill="#fff" fill-opacity=".22"/>')
    ic.path(circle(12, 40, 3.2), "#ffffff", None)
    ic.add('<path d="M10,30A10,10 0 0 1 22,42M10,22.5A17.5,17.5 0 0 1 29.5,42" fill="none" stroke="#fff" stroke-width="3.6" stroke-linecap="round"/>')


def e_vpn(ic):
    """VPN profiles: the globe with a padlock badge."""
    e_globe(ic, 2, 14, 16)
    ic.add(f'<path d="M27,44V40.5A4.5,4.5 0 0 1 36,40.5V44" fill="none" stroke="{INK}" stroke-width="3.6"/>')
    ic.add('<path d="M27,44V40.5A4.5,4.5 0 0 1 36,40.5V44" fill="none" stroke="#c9ccd1" stroke-width="1.8"/>')
    ic.path(rrect(24.5, 43.5, 14, 11, 1.5), ic.lg([(0, "#fff3a6"), (.5, "#d8b030"), (1, "#7a5a04")], 0, 0, 1, 1), INK, 1.1)
    ic.path("M31.5,46.5A1.5,1.5 0 0 1 32.4,49.2V51.5H30.6V49.2A1.5,1.5 0 0 1 31.5,46.5Z", INK, None)


def e_colour(ic):
    """Colour profiles: three overlapping red, green and blue discs."""
    ic.shadow(circle(14, 27, 10.5) + circle(27, 27, 10.5) + circle(20.5, 38, 10.5), 2.4, 2)
    for (x, y), col in (((14, 27), "#ff3a2a"), ((27, 27), "#3ac83a"), ((20.5, 38), "#2a6aff")):
        ic.path(circle(x, y, 10.5), col, INK, 1.1, ' fill-opacity=".72"')
    ic.add('<path d="M8,22Q10,18.5 14,18M21,22Q23,18.5 27,18" fill="none" stroke="#fff" stroke-opacity=".7" stroke-width="1.4" stroke-linecap="round"/>')


def e_map(ic):
    """GPS and map data: a folded map with a dotted red route and a pin."""
    xs, top, bot = (3, 14, 25, 36), (20, 16, 20, 16), (50, 46, 50, 46)
    outline = "M" + "L".join(f"{x},{y}" for x, y in zip(xs, top)) + "L" + "L".join(f"{x},{y}" for x, y in zip(xs[::-1], bot[::-1])) + "Z"
    ic.shadow(outline, 2.6, 2.2)
    for i in range(3):
        panel = f"M{xs[i]},{top[i]}L{xs[i + 1]},{top[i + 1]}L{xs[i + 1]},{bot[i + 1]}L{xs[i]},{bot[i]}Z"
        light = ("#e8f4c8", "#a8d080") if i % 2 == 0 else ("#fff6dc", "#d8c8a0")
        ic.path(panel, ic.lg([(0, light[0]), (1, light[1])], 0, 0, 1, 1), INK, 1)
    ic.add('<path d="M6,24Q12,22 14,28T25,30T33,24" fill="none" stroke="#3a8ee0" stroke-width="1.6"/>')    # a river
    ic.add('<path d="M6,44L12,38L18,40L23,33L28,30" fill="none" stroke="#d8302a" stroke-width="1.8" stroke-dasharray="2.4 1.6" stroke-linecap="round"/>')
    pin = "M28,30C24,24 23.5,22 23.5,20.5A4.5,4.5 0 0 1 32.5,20.5C32.5,22 32,24 28,30Z"
    ic.shadow(pin, 1.4, 1.2)
    ic.path(pin, ic.rg([(0, "#ff9a8a"), (.55, "#e02414"), (1, "#7a0a04")], .4, .3, .8), INK, 1)
    ic.path(circle(28, 20.6, 1.6), "#ffffff", None)


GROUP3 = [
    # cartridge consoles
    ("application-x-nes-rom", (e_cartridge,), "nes", "red", []), ("application-vnd.nintendo.snes.rom", (e_cartridge,), "sfc", "violet", ["application-x-snes-rom"]),
    ("application-x-gameboy-rom", (e_cartridge,), "gb", "olive", []), ("application-x-gameboy-color-rom", (e_cartridge,), "gbc", "lime", []),
    ("application-x-gba-rom", (e_cartridge,), "gba", "indigo", []), ("application-x-n64-rom", (e_cartridge,), "n64", "green", []),
    ("application-x-nintendo-ds-rom", (e_cartridge,), "nds", "slate", []), ("application-x-nintendo-3ds-rom", (e_cartridge,), "3ds", "red", ["application-x-nintendo-3ds-executable"]),
    ("application-x-virtual-boy-rom", (e_cartridge,), "vb", "crimson", []),
    ("application-x-genesis-rom", (e_cartridge,), "smd", "navy", []),   # one type covers .gen, .smd and .sgd ("application-x-genesis-32x-rom", (e_cartridge,), "32x", "navy", []),
    ("application-x-sms-rom", (e_cartridge,), "sms", "blue", []), ("application-x-sg1000-rom", (e_cartridge,), "sg", "slate", []), ("application-x-gamegear-rom", (e_cartridge,), "gg", "teal", []),
    ("application-x-pc-engine-rom", (e_cartridge,), "pce", "orange", []), ("application-x-msx-rom", (e_cartridge,), "msx", "amber", []),
    ("application-x-atari-2600-rom", (e_cartridge,), "a26", "brown", []), ("application-x-atari-7800-rom", (e_cartridge,), "a78", "brown", []),
    ("application-x-atari-lynx-rom", (e_cartridge,), "lnx", "gold", []),
    ("application-x-neo-geo-pocket-rom", (e_cartridge,), "ngp", "grey", []), ("application-x-neo-geo-pocket-color-rom", (e_cartridge,), "ngc", "cyan", []),
    ("application-x-wonderswan-rom", (e_cartridge,), "ws", "grey", []), ("application-x-wonderswan-color-rom", (e_cartridge,), "wsc", "magenta", []),
    ("application-x-thomson-cartridge-memo7", (e_cartridge,), "m7", "olive", []),
    # disc consoles
    ("application-x-gamecube-rom", (e_disc,), "gc", "indigo", []), ("application-x-wii-rom", (e_disc,), "wii", "cyan", []),
    ("application-x-saturn-rom", (e_disc,), "sat", "slate", []), ("application-x-dreamcast-rom", (e_disc,), "dc", "orange", ["application-x-gd-rom-cue"]),
    ("application-x-sega-cd-rom", (e_disc,), "scd", "navy", []), ("application-x-sega-pico-rom", (e_cartridge,), "pico", "pink", []),
    # feeds
    ("application-rss+xml", (e_feed,), "rss", "orange", ["application-x-rss+xml", "text-rss"]), ("application-atom+xml", (e_feed,), "atom", "amber", []),
    ("text-x-opml+xml", (e_feed,), "opml", "brown", ["text-x-opml"]),
    # VPN
    ("application-x-openvpn-profile", (e_vpn,), "ovpn", "green", []), ("application-x-cisco-vpn-settings", (e_vpn,), "pcf", "blue", []),
    # apps
    ("application-vnd.android.package-archive", (e_box,), "apk", "lime", ["android-package-archive"]),
    # colour
    ("application-vnd.iccprofile", (e_colour,), "icc", "slate", ["application-x-icc-profile"]),
    # GPS and maps
    ("application-gpx+xml", (e_map,), "gpx", "red", ["application-x-gpx+xml", "application-x-gpx"]),
    ("application-vnd.google-earth.kml+xml", (e_map,), "kml", "blue", []),
    ("application-vnd.google-earth.kmz", (e_map,), "kmz", "navy", []),
    ("application-geo+json", (e_map,), "geo", "teal", []),
    # Arduino (the Arduino IDE registers this type; without it .ino files show as plain text)
    ("text-x-arduino", (m_source,), "ino", "teal", ["text-x-arduino-sketch"]),
]
for name, base, text, colour, al in GROUP3:
    _reg(name, base, text, colour, al)


def appimage_icon():
    """AppImage: a self-contained program, so the program gear with a small "appimage" tag."""
    ic = exe_icon()
    e_label("appimage", "violet", k=.92)(ic)
    return ic


MIMES["application-vnd.appimage"] = appimage_icon
TAGS["application-vnd.appimage"] = ("appimage", "violet")
SMALL_TEXT["application-vnd.appimage"] = "aimg"
for _a in ("application-x-iso9660-appimage", "application-x-appimage"):
    MIME_ALIASES[_a] = "application-vnd.appimage"
MIME_ALIASES.pop("application-vnd.appimage", None)



# ------------------------------------------------------------------ disc images used by emulators, PlayStation music, Amiga disks
def e_floppy_small(ic):
    from devices import floppy
    ic.add('<g transform="translate(0,10) scale(.66)">')
    floppy(ic)
    ic.add("</g>")


for name, base, text, colour, al in [
    ("application-x-mame-chd", (e_disc,), "chd", "red", []),
    ("application-x-compressed-iso", (e_disc,), "cso", "teal", []),
    ("application-x-cue", (e_disc,), "cue", "slate", []),
    ("application-x-cdrdao-toc", (e_disc,), "toc", "grey", []),
    ("application-vnd.efi.img", (e_vmdisk,), "img", "grey", []),
    ("audio-x-psf", (e_audio,), "psf", "indigo", ["audio-x-minipsf"]),
    ("application-x-amiga-disk-format", (e_floppy_small,), "adf", "orange", []),
]:
    _reg(name, base, text, colour, al)
_reg("application-x-cd-image", (e_disc,), "iso", "blue", ["application-x-iso9660-image", "application-x-iso", "application-vnd.efi.iso", "cdimage"])

# unknown *binary* files (.bin and anything else the system can't identify but knows is binary) get the
# 0/1 page; "unknown" (type can't be determined at all) keeps the green question mark
MIME_ALIASES["application-octet-stream"] = "application-x-object"
