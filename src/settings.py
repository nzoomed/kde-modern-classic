"""KDE Classic Vector: System Settings module icons.

Drawn in the KDE Classic style (full colour, black outline, top-left light, soft shadow), one distinct
design per module so no two sidebar entries share a picture. Built in batches; see ROADMAP.md.
"""
import math
from gen import Icon, INK, LW, circle, rrect, e_globe

SX, SY, SW, SH = 10.5, 9.5, 43, 30      # screen area of the standard monitor


def monitor(ic, screen=None, bezel=("#fbf9f2", "#b4b0a3"), glass=("#3a6fd8", "#1a3ea8", "#0c2470")):
    """The classic beige monitor on a short stand; screen(ic) draws the screen contents."""
    ic.shadow(rrect(5, 5, 54, 40, 3) + "M22,44H42L45,56H19Z", 3, 2.6)
    ic.path("M18,52Q18,50 20,50H44Q46,50 46,52V56H18Z", ic.lg([(0, "#e8e4d8"), (1, "#8a877c")]), INK, LW)
    ic.path("M25,43H39L41,50.5H23Z", ic.lg([(0, "#d9d5c8"), (1, "#8a877c")]), INK, LW)
    ic.path(rrect(5, 5, 54, 40, 3), ic.lg([(0, bezel[0]), (1, bezel[1])], 0, 0, .3, 1), INK, LW)
    ic.path(rrect(SX, SY, SW, SH, 1.6), ic.lg([(0, glass[0]), (.6, glass[1]), (1, glass[2])]), INK, 1)
    if screen:
        screen(ic)
    ic.add(f'<path d="M{SX + 1.5},{SY + 1.5}H{SX + SW - 1.5}V{SY + 11}C{SX + 28},{SY + 15} {SX + 14},{SY + 15.5} {SX + 1.5},{SY + 15}Z" fill="#fff" fill-opacity=".16"/>')
    ic.path(circle(52, 41.5, 1.1), "#4fae5a", None)


def window(ic, x, y, w, h, title=("#9fd4ff", "#1a5c9e"), body=("#ffffff", "#dfe2e6"), buttons=True, shadow=True):
    """A KDE 3-style window: coloured title bar, three buttons, light body."""
    if shadow:
        ic.shadow(rrect(x, y, w, h, 2), 2.6, 2.2)
    ic.path(rrect(x, y, w, h, 2), ic.lg([(0, body[0]), (1, body[1])]), INK, LW)
    ic.path(f"M{x + 2},{y}H{x + w - 2}Q{x + w},{y} {x + w},{y + 2}V{y + 7}H{x}V{y + 2}Q{x},{y} {x + 2},{y}Z",
            ic.lg([(0, title[0]), (1, title[1])]), INK, 1)
    if buttons:
        for k, col in enumerate(("#d8302a", "#e8c43a", "#4fae5a")):
            ic.path(circle(x + w - 4.2 - k * 4.6, y + 3.5, 1.6), col, INK, .5)


# ------------------------------------------------------------------ appearance & style
def global_theme(ic):
    """Global Theme: a monitor whose screen holds a sweep of every part of the look (colours, window, icons)."""
    def scr(ic):
        for i, col in enumerate(("#ff6a5a", "#ffb03a", "#ffe23a", "#6ad04a", "#3aa8ff", "#8a5ae8")):
            ic.add(f'<path d="M{SX + 2 + i * 6.8},{SY + SH - 1}L{SX + 9 + i * 6.8},{SY + 1}H{SX + 15.8 + i * 6.8}L{SX + 8.8 + i * 6.8},{SY + SH - 1}Z" fill="{col}" fill-opacity=".85"/>')
        window(ic, 17, 15, 22, 15, shadow=False)
        ic.add('<path d="M20,27H34" stroke="#9aa0a8" stroke-width="1.2"/>')
    monitor(ic, scr)
    # a paintbrush resting across the corner: "apply a look to everything"
    ic.add('<g transform="rotate(-38 48 46)">')
    ic.path("M38,44H52V48H38Z", ic.lg([(0, "#e8b878"), (1, "#8a5a2a")]), INK, 1)
    ic.path("M52,43.6H56V48.4H52Z", ic.lg([(0, "#ffffff"), (1, "#8a9098")]), INK, 1)
    ic.path("M56,43.8Q62,43 64,46Q62,49 56,48.2Z", ic.lg([(0, "#ff7a5a"), (1, "#a8180a")]), INK, 1)
    ic.add("</g>")


def plasma_style(ic):
    """Plasma Style: the desktop's panel and a widget, glowing blue on a dark screen."""
    def scr(ic):
        ic.add(f'<path d="M{SX + .6},{SY + SH - 6}H{SX + SW - .6}V{SY + SH - .6}H{SX + .6}Z" fill="#1a1e26"/>')
        ic.add(f'<path d="M{SX + .6},{SY + SH - 6}H{SX + SW - .6}" stroke="#5ab8ff" stroke-width=".9"/>')
        for k in range(4):
            ic.path(rrect(SX + 3 + k * 5.5, SY + SH - 4.6, 3.6, 3.2, .8), ["#3aa8ff", "#ffb03a", "#6ad04a", "#e8e8e8"][k], None)
        ic.path(rrect(31, 13, 19, 14, 2.2), "#262c38", "#5ab8ff", .9, ' fill-opacity=".9"')
        ic.add('<path d="M34,22L37,18L40,21L43,16L47,19" fill="none" stroke="#5ab8ff" stroke-width="1.3" stroke-linejoin="round"/>')
        ic.path(circle(20, 20, 5.5), "none", "#5ab8ff", 1.6)
        ic.add('<path d="M20,14.5A5.5,5.5 0 0 1 25.5,20" fill="none" stroke="#bfe4ff" stroke-width="1.6"/>')
    monitor(ic, scr, glass=("#3a4a6a", "#1a2238", "#0a0e18"))


def app_style(ic):
    """Application Style: a window showing widgets (a button, a check box, a slider)."""
    window(ic, 4, 7, 54, 46)
    ic.path(rrect(9, 18, 20, 8, 2), ic.lg([(0, "#ffffff"), (1, "#c3c7cd")]), INK, 1)
    ic.add('<path d="M13,22H25" stroke="#5c6168" stroke-width="1.4"/>')
    ic.path(rrect(34, 18, 7.5, 7.5, 1.2), "#ffffff", INK, 1)
    ic.add(f'<path d="M35.5,21.8L37.6,24L40.6,19.4" fill="none" stroke="#2f9a2e" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>')
    ic.add('<path d="M44.5,22H53" stroke="#5c6168" stroke-width="1.4"/>')
    ic.add(f'<path d="M10,36H52" stroke="{INK}" stroke-width="3.4" stroke-linecap="round"/><path d="M10,36H52" stroke="#c3c7cd" stroke-width="1.8" stroke-linecap="round"/>')
    ic.add('<path d="M10,36H31" stroke="#3a8ee0" stroke-width="1.8" stroke-linecap="round"/>')
    ic.path(circle(31, 36, 3.6), ic.rg([(0, "#ffffff"), (1, "#9aa0a8")]), INK, 1)
    ic.path(circle(12, 46, 3), "#ffffff", INK, 1)
    ic.path(circle(12, 46, 1.4), "#3a8ee0", None)
    ic.add('<path d="M18,46H30" stroke="#5c6168" stroke-width="1.4"/>')


def window_decorations(ic):
    """Window Decorations: a big close-up of a title bar with its buttons, over a window's corner."""
    ic.shadow(rrect(3, 14, 58, 40, 3), 2.6, 2.2)
    ic.path(rrect(3, 14, 58, 40, 3), ic.lg([(0, "#ffffff"), (1, "#dfe2e6")]), INK, LW)
    ic.path("M6,14H58Q61,14 61,17V30H3V17Q3,14 6,14Z", ic.lg([(0, "#bfe4ff"), (.5, "#3a8ee0"), (1, "#14468e")]), INK, LW)
    ic.add('<path d="M6,16.5H58" stroke="#fff" stroke-opacity=".5" stroke-width="1.2"/>')
    ic.add('<path d="M9,22H27" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/>')
    for k, (col, g) in enumerate((("#d8302a", "M-2.4,-2.4L2.4,2.4M2.4,-2.4L-2.4,2.4"), ("#e8c43a", "M-2.6,-2.6H2.6V2.6H-2.6Z"), ("#4fae5a", "M-2.6,1.8H2.6"))):
        cx = 54 - k * 9
        ic.path(circle(cx, 22, 3.8), ic.rg([(0, "#ffffff"), (.5, col), (1, col)], .35, .3, .8), INK, 1)
        ic.add(f'<path d="{g}" transform="translate({cx},22)" fill="none" stroke="#fff" stroke-width="1.3" stroke-linecap="round"/>')
    ic.add('<path d="M9,37H44M9,42H38M9,47H41" stroke="#9aa0a8" stroke-width="1.4"/>')


def colours(ic):
    """Colours: the classic colour wheel, glossy."""
    cx, cy, r = 30, 30, 23
    ic.shadow(circle(cx, cy, r), 2.6, 2.2)
    cols = ["#ff2a2a", "#ff8a1a", "#ffe21a", "#8ad81a", "#1ab84a", "#1ac8c8", "#1a7aff", "#5a3aff", "#b82aff", "#ff2ab8"]
    n = len(cols)
    for k, col in enumerate(cols):
        a0, a1 = 2 * math.pi * k / n - math.pi / 2, 2 * math.pi * (k + 1) / n - math.pi / 2
        ic.add(f'<path d="M{cx},{cy}L{cx + r * math.cos(a0):.2f},{cy + r * math.sin(a0):.2f}A{r},{r} 0 0 1 {cx + r * math.cos(a1):.2f},{cy + r * math.sin(a1):.2f}Z" fill="{col}"/>')
    ic.path(circle(cx, cy, r), ic.rg([(0, "#ffffff", .85), (.55, "#ffffff", 0)], .5, .5, .5), INK, LW)
    ic.add(f'<path d="M{cx - 16},{cy - 8}Q{cx - 12},{cy - 18} {cx - 1},{cy - 20}" fill="none" stroke="#fff" stroke-opacity=".7" stroke-width="2.4" stroke-linecap="round"/>')
    # a small swatch card in front
    ic.shadow(rrect(38, 38, 22, 20, 2), 1.8, 1.6)
    ic.path(rrect(38, 38, 22, 20, 2), "#ffffff", INK, 1.2)
    for k, col in enumerate(("#d8302a", "#3a8ee0", "#4fae5a", "#e8c43a")):
        ic.path(rrect(41 + (k % 2) * 9, 41 + (k // 2) * 8, 7, 6, 1), col, INK, .6)


def gamma(ic):
    """Gamma / display colour: a monitor showing a grey ramp with a red, green and blue curve over it."""
    def scr(ic):
        for k in range(8):
            v = int(20 + k * 33)
            ic.add(f'<rect x="{SX + 1 + k * 5.1:.1f}" y="{SY + 1}" width="5.2" height="{SH - 2}" fill="rgb({v},{v},{v})"/>')
        for col, b in (("#ff4a3a", 0), ("#4ae04a", 2.5), ("#4a8aff", 5)):
            ic.add(f'<path d="M{SX + 2},{SY + SH - 3 - b / 2}Q{SX + 14 + b},{SY + 8 + b} {SX + SW - 2},{SY + 3}" fill="none" stroke="{col}" stroke-width="1.6"/>')
    monitor(ic, scr)


def _perf(x, y, w, h, r):
    """A postage-stamp outline: a rectangle whose edges are bitten by evenly spaced half-circle perforations."""
    def edge(n_len):
        n = max(2, round(n_len / (r * 3.2)))        # number of notches along this edge
        gap = (n_len - n * 2 * r) / (n + 1)
        return n, gap
    d = [f"M{x:.2f},{y:.2f}"]
    # top: left -> right, notches bite downward
    n, g = edge(w)
    cx = x
    for _ in range(n):
        cx += g
        d.append(f"H{cx:.2f}A{r},{r} 0 0 0 {cx + 2 * r:.2f},{y:.2f}")
        cx += 2 * r
    d.append(f"H{x + w:.2f}")
    # right: top -> bottom, notches bite leftward
    n, g = edge(h)
    cy = y
    for _ in range(n):
        cy += g
        d.append(f"V{cy:.2f}A{r},{r} 0 0 0 {x + w:.2f},{cy + 2 * r:.2f}")
        cy += 2 * r
    d.append(f"V{y + h:.2f}")
    # bottom: right -> left, notches bite upward
    n, g = edge(w)
    cx = x + w
    for _ in range(n):
        cx -= g
        d.append(f"H{cx:.2f}A{r},{r} 0 0 0 {cx - 2 * r:.2f},{y + h:.2f}")
        cx -= 2 * r
    d.append(f"H{x:.2f}")
    # left: bottom -> top, notches bite rightward
    n, g = edge(h)
    cy = y + h
    for _ in range(n):
        cy -= g
        d.append(f"V{cy:.2f}A{r},{r} 0 0 0 {x:.2f},{cy - 2 * r:.2f}")
        cy -= 2 * r
    d.append("Z")
    return "".join(d)


# The queen in profile, traced from Shaun Belcher's own drawing (89 points), in a
# QUEEN_W x QUEEN_H box with its top-left corner at 0,0.
QUEEN = "M6.31,0.04L6.02,0.25L5.73,0.94L5.32,1.43L5.24,2.09L4.67,3.60L4.46,3.77L3.52,3.85L3.15,4.05L2.66,4.59L2.46,5.16L2.54,6.18L1.60,8.48L1.56,9.66L1.43,10.07L1.11,10.60L0.12,11.59L0.00,11.91L0.08,12.28L0.70,12.69L0.98,13.02L0.90,13.55L1.02,14.13L0.98,14.70L1.35,15.27L1.43,16.17L1.64,16.66L2.33,17.07L3.89,17.24L4.42,17.44L4.79,18.02L5.20,19.49L5.28,20.10L5.24,21.66L4.91,22.15L4.18,22.60L3.97,23.42L2.25,25.63L2.25,25.96L14.58,25.96L14.54,25.39L13.84,23.38L12.12,19.49L12.00,18.59L11.51,18.02L11.30,16.46L11.51,16.26L12.86,16.17L13.43,15.48L13.92,15.31L14.13,15.11L14.29,14.33L14.74,13.63L14.74,13.14L14.13,11.34L14.09,10.97L15.35,9.66L16.34,8.97L17.32,7.86L17.36,7.66L17.11,7.49L16.46,7.33L16.26,7.17L16.30,6.31L16.09,5.98L15.80,5.94L14.86,6.26L14.29,5.86L13.80,5.81L13.59,5.53L13.55,5.20L13.88,4.63L13.84,4.46L11.18,2.46L10.89,2.42L10.56,2.70L10.32,2.74L9.87,2.50L9.83,2.17L9.70,2.05L8.84,2.05L8.60,1.72L8.64,0.82L8.43,0.53L7.62,0.86L6.84,0.90L6.76,0.53L6.88,0.12L6.71,0.00Z"
QUEEN_W, QUEEN_H = 17.4, 26.0


def _stamp(ic, x, y, w, h, inset, panel, cameo, maxw):
    """One perforated stamp with the queen centred on its picture; maxw caps her width in icon units."""
    ic.shadow(rrect(x, y, w, h, 1), 2.4, 2.2)
    ic.path(_perf(x, y, w, h, 1.55), ic.lg([(0, "#ffffff"), (1, "#dcdcd6")], 0, 0, 1, 1), INK, 1)
    px, py, pw, ph = x + inset, y + inset, w - 2 * inset, h - 2 * inset
    ic.path(f"M{px},{py}H{px + pw}V{py + ph}H{px}Z", ic.lg([(0, panel[0]), (1, panel[1])]), INK, .8)
    s = min(maxw / QUEEN_W, ph * .78 / QUEEN_H)       # centred on the picture both ways
    tx = px + (pw - QUEEN_W * s) / 2
    ty = py + (ph - QUEEN_H * s) / 2
    ic.add(f'<g transform="translate({tx:.2f},{ty:.2f}) scale({s:.3f})">'
           f'<path d="{QUEEN}" fill="url(#{_grad(ic, cameo)})"/></g>')
    # a soft gloss across the top of the picture
    ic.add(f'<path d="M{px + .6},{py + .6}H{px + pw - .6}V{py + ph * .3}Q{px + pw / 2},{py + ph * .42} {px + .6},{py + ph * .36}Z" '
           f'fill="#fff" fill-opacity=".14"/>')


def _grad(ic, stops):
    u = ic.lg([(0, stops[0]), (1, stops[1])])
    return u[5:-1] if u.startswith("url(#") else u


def icons_kcm(ic):
    """Icons: two postage stamps, after KDE Classic's icons.png (plum stamp behind, green stamp in front)."""
    _stamp(ic, 4, 4, 38, 46, 5, ("#5a2450", "#e4127e"), ("#fbe4f2", "#e6a8cc"), 17)
    _stamp(ic, 33, 28, 27, 33, 4.5, ("#2f5a26", "#d8e418"), ("#f4f8e2", "#d2e6a0"), 16)


def emoji_selector(ic):
    """Emoji Selector: a winking smiley in front of a little picker card of symbols."""
    ic.shadow(rrect(27, 4, 33, 33, 4), 2.4, 2.2)
    ic.path(rrect(27, 4, 33, 33, 4), ic.lg([(0, "#ffffff"), (1, "#c9ccd1")], 0, 0, 1, 1), INK, LW)
    # a heart, a star and a water drop on the card
    ic.path("M37,19C31,15 32,9.5 34.5,9.5C36,9.5 37,10.6 37,11.6C37,10.6 38,9.5 39.5,9.5C42,9.5 43,15 37,19Z",
            ic.rg([(0, "#ffb0a0"), (1, "#c8180c")], .4, .3, .8), INK, .9)
    star = []
    for k in range(10):
        a = -math.pi / 2 + k * math.pi / 5
        rad = 5.4 if k % 2 == 0 else 2.3
        star.append((51 + rad * math.cos(a), 14.4 + rad * math.sin(a)))
    ic.path("M" + "L".join(f"{px:.2f},{py:.2f}" for px, py in star) + "Z",
            ic.rg([(0, "#fff6c0"), (1, "#e09a08")]), INK, .9)
    ic.path("M51,21.5C51,21.5 46.6,26.8 46.6,29A4.4,4.4 0 0 0 55.4,29C55.4,26.8 51,21.5 51,21.5Z",
            ic.rg([(0, "#c8ecff"), (1, "#1a6ac8")], .4, .5, .8), INK, .9)
    # the winking face, large, lower left
    cx, cy, r = 23, 41, 18
    ic.shadow(circle(cx, cy, r), 2.6, 2.2)
    ic.path(circle(cx, cy, r), ic.rg([(0, "#fffbe0"), (.6, "#ffd21a"), (1, "#c87a04")], .4, .35, .8), INK, LW)
    ic.path(f"M{cx - 10.5},{cy - 6}A2.4,3.1 0 1 0 {cx - 5.7},{cy - 6}A2.4,3.1 0 1 0 {cx - 10.5},{cy - 6}Z", INK, None)
    ic.add(f'<path d="M{cx + 3.6},{cy - 5}Q{cx + 7.2},{cy - 8.6} {cx + 10.8},{cy - 5}" fill="none" stroke="{INK}" '
           f'stroke-width="2.4" stroke-linecap="round"/>')
    ic.add(f'<path d="M{cx - 10.5},{cy + 3.5}Q{cx},{cy + 14.5} {cx + 10.5},{cy + 3.5}" fill="none" stroke="{INK}" '
           f'stroke-width="2.6" stroke-linecap="round"/>')


def cursors(ic):
    """Cursors: the white arrow pointer in front of a busy hourglass."""
    hg = "M30,8H52V12Q52,20 43,25Q52,30 52,38V42H30V38Q30,30 39,25Q30,20 30,12Z"
    ic.shadow(hg, 2.4, 2)
    ic.path(hg, ic.lg([(0, "#ffffff", .9), (1, "#c3d4e4", .9)]), INK, LW)
    ic.add('<path d="M33,12Q33,18 41,22.5H41.6Q49,18 49,12Z" fill="#e8c43a"/><path d="M34,39.5Q37,33 41,31Q45,33 48,39.5Z" fill="#e8c43a"/>')
    ic.path("M28,6H54V10H28Z M28,40H54V44H28Z", ic.lg([(0, "#c8965c"), (1, "#6a4418")]), INK, 1)
    arrow = "M8,20V54L16,46.5L21.5,58L27,55.5L21.5,44.5H32Z"
    ic.shadow(arrow, 2.6, 2.4)
    ic.path(arrow, "#ffffff", INK, LW * 1.2)
    ic.add('<path d="M10.5,26V47.5" stroke="#d4d7dc" stroke-width="1.2"/>')


def wallpaper(ic):
    """Wallpaper: a monitor showing a landscape (sky, sun, hills) edge to edge."""
    def scr(ic):
        ic.path(f"M{SX + .6},{SY + .6}H{SX + SW - .6}V{SY + SH - .6}H{SX + .6}Z", ic.lg([(0, "#3a8ee0"), (.6, "#9ad0f8"), (1, "#e4f6ff")]), None)
        ic.path(circle(43, 17, 3.6), ic.rg([(0, "#fffbe0"), (1, "#ffb21a")]), None)
        ic.add('<path d="M15,17.5Q15,15 17.6,15.2Q18.6,13 21.2,13.6Q23.4,13.8 23.8,15.8Q26,15.8 26,17.5Z" fill="#fff"/>')
        ic.path(f"M{SX + .6},{SY + 21}Q{SX + 12},{SY + 15} {SX + 22},{SY + 19}Q{SX + 32},{SY + 13} {SX + SW - .6},{SY + 18}V{SY + SH - .6}H{SX + .6}Z", ic.lg([(0, "#6ab84a"), (1, "#2e7a26")]), None)
        ic.path(f"M{SX + .6},{SY + 25}Q{SX + 18},{SY + 21} {SX + SW - .6},{SY + 24}V{SY + SH - .6}H{SX + .6}Z", ic.lg([(0, "#a8e060"), (1, "#4a9a28")]), None)
    monitor(ic, scr)


def splash(ic):
    """Splash Screen: a monitor showing a star burst over a progress bar, as Plasma starts."""
    def scr(ic):
        cx, cy = SX + SW / 2, SY + 12
        d = ""
        for k in range(10):
            a = 2 * math.pi * k / 10 - math.pi / 2
            r = 7.5 if k % 2 == 0 else 3.2
            d += ("M" if k == 0 else "L") + f"{cx + r * math.cos(a):.2f},{cy + r * math.sin(a):.2f}"
        ic.path(d + "Z", ic.rg([(0, "#ffffff"), (.5, "#ffe23a"), (1, "#e88a10")]), "#7a4404", .8)
        ic.path(rrect(SX + 7, SY + 23, SW - 14, 3.4, 1.7), "#0a1a40", "#9fd4ff", .7)
        ic.path(rrect(SX + 7.6, SY + 23.6, (SW - 15.2) * .62, 2.2, 1.1), "#9fd4ff", None)
    monitor(ic, scr)


def boot_splash(ic):
    """Boot Splash: a black screen with a spinner, as the machine starts up."""
    def scr(ic):
        cx, cy = SX + SW / 2, SY + SH / 2
        for k in range(8):
            a = 2 * math.pi * k / 8
            op = .25 + .75 * k / 7
            ic.path(circle(round(cx + 7 * math.cos(a), 2), round(cy + 7 * math.sin(a), 2), 1.9), "#ffffff", None, f' fill-opacity="{op:.2f}"')
    monitor(ic, scr, glass=("#2a2e36", "#0e1014", "#000000"))


def login_screen(ic):
    """Login Screen: a monitor showing a user picture above a password box."""
    def scr(ic):
        cx = SX + SW / 2
        ic.path(circle(cx, SY + 9, 5.5), ic.rg([(0, "#fff1e2"), (1, "#c88a5a")]), "#ffffff", 1)
        ic.path(f"M{cx - 7},{SY + 19.5}Q{cx - 7},{SY + 14.5} {cx},{SY + 14.5}Q{cx + 7},{SY + 14.5} {cx + 7},{SY + 19.5}Z", "#9fd4ff", None)
        ic.path(rrect(cx - 12, SY + 21.5, 24, 5.4, 1.4), "#ffffff", "#0a1a40", .7)
        for k in range(5):
            ic.path(circle(cx - 8 + k * 3.4, SY + 24.2, .9), "#1a1e26", None)
    monitor(ic, scr)


def effects(ic):
    """Desktop Effects: a window wobbling as it moves, with a sparkle trail."""
    ic.add('<g transform="translate(8,8) rotate(-12 22 22) skewX(-6)">')
    window(ic, 0, 0, 40, 32)
    ic.add('<path d="M5,14H30M5,19H26M5,24H28" stroke="#9aa0a8" stroke-width="1.3"/>')
    ic.add("</g>")
    for x, y, r in ((50, 12, 4.5), (55, 26, 3), (46, 46, 3.6), (12, 52, 2.6)):
        d = ""
        for k in range(8):
            a = math.pi * k / 4
            rr = r if k % 2 == 0 else r * .35
            d += ("M" if k == 0 else "L") + f"{x + rr * math.cos(a):.2f},{y + rr * math.sin(a):.2f}"
        ic.path(d + "Z", ic.rg([(0, "#ffffff"), (.5, "#ffe23a"), (1, "#e8a010")]), "#8a5a04", .6)


# ------------------------------------------------------------------ input devices
def _keys_rows(ic, x0, y0, rows, kw=5.2, kh=4.6, gap=.9, skew=0.0):
    for r, n in enumerate(rows):
        for k in range(n):
            x = x0 + r * skew + k * (kw + gap)
            y = y0 + r * (kh + gap)
            ic.path(rrect(round(x, 2), round(y, 2), kw, kh, .9), ic.lg([(0, "#ffffff"), (1, "#cfc8b0")]), "#6a6050", .6)


def keyboard(ic):
    """Keyboard: a whole beige keyboard seen from the front at a slight angle, rows of keys and a space bar."""
    body = "M3,24Q3,20 7,20H57Q61,20 61,24V48Q61,52 57,52H7Q3,52 3,48Z"
    ic.shadow(body, 2.6, 2.2)
    ic.path("M3,46H61V48Q61,52 57,52H7Q3,52 3,48Z", "#8a8064", INK, LW)
    ic.path("M3,24Q3,20 7,20H57Q61,20 61,24V46H3Z", ic.lg([(0, "#f4f0e0"), (1, "#c4bc9e")]), INK, LW)
    _keys_rows(ic, 6.5, 23, (8, 8, 8), skew=1.6)
    ic.path(rrect(18, 40.5, 26, 4, .9), ic.lg([(0, "#ffffff"), (1, "#cfc8b0")]), "#6a6050", .6)
    ic.path(circle(55.5, 42.5, .9), "#4fae5a", None)


def shortcuts(ic):
    """Shortcuts: two keycaps, ctrl + K, with a blue plus between them."""
    from devices import keycap
    ic.add('<g transform="translate(-2,14) scale(.55)">')
    keycap(ic)
    ic.add("</g>")
    ic.add('<g transform="translate(29,14) scale(.55)">')
    keycap(ic)
    ic.add("</g>")
    ic.add(f'<path d="M30.5,22V30M26.5,26H34.5" stroke="{INK}" stroke-width="4.4" stroke-linecap="round"/><path d="M30.5,22V30M26.5,26H34.5" stroke="#3a8ee0" stroke-width="2.4" stroke-linecap="round"/>')


def mouse_kcm(ic):
    from devices import mouse
    mouse(ic)


def touchpad(ic):
    """Touchpad: a laptop's palm rest with its pad and buttons, a fingertip sliding across it."""
    rest = rrect(3, 10, 58, 46, 5)
    ic.shadow(rest, 2.6, 2.2)
    ic.path(rest, ic.lg([(0, "#e4e6e9"), (1, "#8a9098")], 0, 0, .3, 1), INK, LW)
    ic.path(rrect(13, 15, 38, 26, 3), ic.lg([(0, "#5c6168"), (1, "#2c3036")]), INK, 1)
    ic.add('<path d="M14.5,17H49.5" stroke="#fff" stroke-opacity=".18" stroke-width="1.2"/>')
    ic.path("M13,44H31.5V50.5H15Q13,50.5 13,48.5Z", ic.lg([(0, "#c3c7cd"), (1, "#7b818a")]), INK, 1)
    ic.path("M32.5,44H51V48.5Q51,50.5 49,50.5H32.5Z", ic.lg([(0, "#c3c7cd"), (1, "#7b818a")]), INK, 1)
    ic.add('<path d="M20,32Q26,26 35,28" fill="none" stroke="#9fd4ff" stroke-width="1.6" stroke-dasharray="2 1.6" stroke-linecap="round"/>')
    ic.path(circle(38, 28.5, 4.4), ic.rg([(0, "#fff1e2"), (1, "#d89a6a")]), INK, 1)


def tablet(ic):
    """Drawing Tablet: a dark tablet with its active area, a stylus drawing a curve."""
    slab = rrect(3, 14, 52, 40, 4)
    ic.shadow(slab, 2.6, 2.2)
    ic.path(slab, ic.lg([(0, "#5c6168"), (1, "#1a1d22")], 0, 0, .3, 1), INK, LW)
    ic.path("M12,19H50V49H12Z", ic.lg([(0, "#3a3f46"), (1, "#26292e")]), "#7b818a", .8)
    for k in range(4):
        ic.path(rrect(5.5, 20 + k * 7, 4, 4.4, .8), "#4c5158", "#7b818a", .5)
    ic.add('<path d="M16,43Q22,28 31,36T46,26" fill="none" stroke="#5ab8ff" stroke-width="1.8" stroke-linecap="round"/>')
    ic.add('<g transform="rotate(40 46 26)">')
    ic.path("M44,-6H48V24L46,28L44,24Z", ic.lg([(0, "#e4e6e9"), (.5, "#9aa0a8"), (1, "#4c5158")], 0, 0, 1, 0), INK, 1)
    ic.path("M44,10H48V13H44Z", "#3a8ee0", None)
    ic.add("</g>")


def touchscreen(ic):
    """Touchscreen: a screen being touched by a fingertip, with ripples where it lands."""
    scr = rrect(4, 6, 46, 36, 3)
    ic.shadow(scr, 2.6, 2.2)
    ic.path(scr, ic.lg([(0, "#4c5158"), (1, "#14171c")], 0, 0, .3, 1), INK, LW)
    ic.path("M8,10H46V38H8Z", ic.lg([(0, "#9fd4ff"), (1, "#1a5c9e")]), INK, .8)
    for r, op in ((9, .35), (6, .6)):
        ic.add(f'<path d="{circle(31, 25, r)}" fill="none" stroke="#fff" stroke-opacity="{op}" stroke-width="1.3"/>')
    hand = "M28,24.5Q28,21.5 31,21.5Q34,21.5 34,24.5V38L40,36Q44,35 45,38L46,46Q46.5,52 41,56H29Q25,53 23,47L20,40Q19,37 21.5,36.5Q24,36 25.5,39L28,43Z"
    ic.shadow(hand, 2, 1.8)
    ic.path(hand, ic.rg([(0, "#fff1e2"), (.7, "#f0c8a0"), (1, "#c88a5a")], .4, .3, .8), INK, LW)
    ic.add('<path d="M34,38V44M40,36.6V43" stroke="#a87048" stroke-width=".9"/>')


def gamepad(ic):
    """Game Controller: a grey game pad with a cross pad and four coloured buttons."""
    pad = "M14,18H50Q60,18 61,32L62,44Q62.5,52 55,52Q50,52 46,44H18Q14,52 9,52Q1.5,52 2,44L3,32Q4,18 14,18Z"
    ic.shadow(pad, 2.6, 2.2)
    ic.path(pad, ic.lg([(0, "#e4e6e9"), (.55, "#a4aab2"), (1, "#5c6168")], 0, 0, .3, 1), INK, LW)
    ic.path("M13,27H17V31H21V35H17V39H13V35H9V31H13Z", "#2c3036", INK, .8)
    for (x, y), col in (((47, 27), "#3aa8ff"), ((52, 32), "#d8302a"), ((42, 32), "#e8c43a"), ((47, 37), "#4fae5a")):
        ic.path(circle(x, y, 2.6), ic.rg([(0, "#ffffff"), (.5, col), (1, col)], .35, .3, .8), INK, .8)
    ic.path(circle(24, 41, 3.6), "#4c5158", INK, .8)
    ic.path(circle(36, 41, 3.6), "#4c5158", INK, .8)
    ic.add('<path d="M10,21H54" stroke="#fff" stroke-opacity=".5" stroke-width="1.2"/>')


def screen_edges(ic):
    """Screen Edges: a monitor whose top-left corner and edges glow, with arrows pointing into them."""
    def scr(ic):
        ic.add(f'<path d="M{SX + .6},{SY + 10}V{SY + .6}H{SX + 14}" fill="none" stroke="#ffe23a" stroke-width="3" stroke-linecap="round"/>')
        ic.add(f'<path d="M{SX + SW - .6},{SY + 9}V{SY + SH - 9}" fill="none" stroke="#ffe23a" stroke-width="3" stroke-linecap="round"/>')
        ic.add(f'<path d="M{SX + 16},{SY + 14}L{SX + 6},{SY + 5}M{SX + 6},{SY + 10}V{SY + 5}H{SX + 11}" fill="none" stroke="#fff" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>')
        ic.add(f'<path d="M{SX + 28},{SY + 15}H{SX + 39}M{SX + 35},{SY + 11}L{SX + 39},{SY + 15}L{SX + 35},{SY + 19}" fill="none" stroke="#fff" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>')
    monitor(ic, scr)


def touch_gestures(ic):
    """Touchscreen Gestures: two fingertips swiping across a surface, with motion arrows."""
    surf = rrect(3, 12, 58, 40, 5)
    ic.shadow(surf, 2.6, 2.2)
    ic.path(surf, ic.lg([(0, "#9fd4ff"), (1, "#1a5c9e")], 0, 0, .3, 1), INK, LW)
    for y in (26, 38):
        ic.add(f'<path d="M12,{y}H38" stroke="#fff" stroke-opacity=".6" stroke-width="2" stroke-dasharray="3 2" stroke-linecap="round"/>')
        ic.path(circle(44, y, 5), ic.rg([(0, "#fff1e2"), (1, "#d89a6a")]), INK, 1)
    ic.add('<path d="M50,32H58M54.5,28.5L58,32L54.5,35.5" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>')


def virtual_keyboard(ic):
    """Virtual Keyboard: a tablet screen with a keyboard drawn on its lower half."""
    t = rrect(4, 8, 56, 46, 4)
    ic.shadow(t, 2.6, 2.2)
    ic.path(t, ic.lg([(0, "#4c5158"), (1, "#14171c")], 0, 0, .3, 1), INK, LW)
    ic.path("M8,12H56V50H8Z", ic.lg([(0, "#e8f4ff"), (1, "#b4d0ec")]), INK, .8)
    ic.add('<path d="M12,17H40M12,21H34" stroke="#5a7aa0" stroke-width="1.2"/>')
    ic.path("M8,28H56V50H8Z", "#2c3440", None)
    for r, n in enumerate((9, 9, 7)):
        for k in range(n):
            ic.path(rrect(10 + r * 1.5 + k * 5.1, 30 + r * 5.2, 4.3, 4.2, .7), "#5c6878", None)
    ic.path(rrect(20, 45.6, 24, 3.4, .7), "#5c6878", None)


# ------------------------------------------------------------------ hardware
def _sub(ic, fn, tx, ty, k):
    ic.add(f'<g transform="translate({tx},{ty}) scale({k})">')
    fn(ic)
    ic.add("</g>")


def _badge(ic, x, y, r, colour, glyph):
    c = {"green": ("#d4f8c0", "#3fae2a", "#14561a"), "red": ("#ffd0c4", "#d8302a", "#6a0a04"), "blue": ("#c4e2ff", "#2a6ac8", "#0e2e6a"),
         "amber": ("#fff0b0", "#e8a010", "#6a4404")}[colour]
    ic.shadow(circle(x, y, r), 1.4, 1.2)
    ic.path(circle(x, y, r), ic.rg([(0, c[0]), (.55, c[1]), (1, c[2])], .4, .35, .75), INK, 1.1)
    ic.add(f'<path d="{glyph}" fill="none" stroke="#fff" stroke-width="{r * .32:.2f}" stroke-linecap="round" stroke-linejoin="round"/>')


def displays(ic):
    """Display Configuration: two monitors side by side, numbered by colour, one larger."""
    for x, y, w, h, glass in ((26, 6, 35, 27, ("#3a6fd8", "#0c2470")), (3, 18, 27, 21, ("#4fae5a", "#14561a"))):
        ic.shadow(rrect(x, y, w, h, 2.4), 2.4, 2)
        ic.path(f"M{x + w / 2 - 4},{y + h - 1}H{x + w / 2 + 4}L{x + w / 2 + 6},{y + h + 7}H{x + w / 2 - 6}Z", ic.lg([(0, "#d9d5c8"), (1, "#8a877c")]), INK, 1)
        ic.path(rrect(x, y, w, h, 2.4), ic.lg([(0, "#fbf9f2"), (1, "#b4b0a3")]), INK, LW)
        ic.path(rrect(x + 3, y + 3, w - 6, h - 6, 1.2), ic.lg([(0, glass[0]), (1, glass[1])]), INK, .9)
        ic.add(f'<path d="M{x + 4},{y + 4}H{x + w - 4}V{y + h / 2 - 1}Q{x + w / 2},{y + h / 2 + 1} {x + 4},{y + h / 2}Z" fill="#fff" fill-opacity=".18"/>')
    ic.path(rrect(13, 51, 50, 6, 2), ic.lg([(0, "#e8e4d8"), (1, "#8a877c")]), INK, 1)


def opengl(ic):
    """OpenGL / graphics information: a monitor showing a shaded 3D cube."""
    def scr(ic):
        cx, cy, s_ = SX + SW / 2, SY + SH / 2 + 1, 9
        top = f"M{cx},{cy - s_}L{cx + s_},{cy - s_ / 2}L{cx},{cy}L{cx - s_},{cy - s_ / 2}Z"
        left = f"M{cx - s_},{cy - s_ / 2}L{cx},{cy}V{cy + s_}L{cx - s_},{cy + s_ / 2}Z"
        right = f"M{cx + s_},{cy - s_ / 2}L{cx},{cy}V{cy + s_}L{cx + s_},{cy + s_ / 2}Z"
        ic.path(top, "#ff8a5a", "#fff", .8)
        ic.path(left, "#c8301a", "#fff", .8)
        ic.path(right, "#e85a2a", "#fff", .8)
    monitor(ic, scr, glass=("#2a2e36", "#14171c", "#060708"))


def audio_card(ic):
    """Audio information: a green sound card with chips and three coloured jacks on its bracket."""
    ic.add('<g transform="rotate(-8 32 32)">')
    ic.shadow("M4,16H54V44H4Z", 2.6, 2.2)
    ic.path("M4,16H54V44H4Z", ic.lg([(0, "#5ac85a"), (1, "#1a6a24")], 0, 0, 1, 1), INK, LW)
    ic.path("M54,12H59V48H54Z", ic.lg([(0, "#e4e6e9"), (1, "#8a9098")], 0, 0, 1, 0), INK, 1)
    for k, col in enumerate(("#3ac8ff", "#6ad04a", "#ff7ab0")):
        ic.path(circle(56.5, 20 + k * 9, 2.4), col, INK, .7)
    ic.path("M12,22H28V34H12Z", ic.lg([(0, "#3c4148"), (1, "#14171c")]), INK, .8)
    ic.path("M33,24H43V31H33Z", ic.lg([(0, "#3c4148"), (1, "#14171c")]), INK, .8)
    for k in range(14):
        ic.add(f'<rect x="{7 + k * 3.2:.1f}" y="44" width="2" height="4" fill="#e8c43a" stroke="#7a5a04" stroke-width=".3"/>')
    ic.add("</g>")


def sound(ic):
    """Sound: the classic loudspeaker with sound waves coming from it."""
    from gen import e_speaker
    from traytrace import _waves
    e_speaker(ic, cx=26, cy=32, ry=20)
    _waves(ic, 2, "teal", x0=34, cy=32, radii=(13.5, 21.5))


def bluetooth_kcm(ic):
    """Bluetooth: the Bluetooth symbol in white on a glossy blue oval, as in the tray icons."""
    oval = "M32,6C44,6 49,14 49,32C49,50 44,58 32,58C20,58 15,50 15,32C15,14 20,6 32,6Z"
    ic.shadow(oval, 2.6, 2.2)
    ic.path(oval, ic.lg([(0, "#9fd0ff"), (.45, "#2a6ac8"), (1, "#0e2e6a")], 0, 0, .3, 1), INK, LW)
    ic.add('<path d="M20,18Q22,10 32,9.5Q42,10 44,18Q32,24 20,18Z" fill="#fff" fill-opacity=".3"/>')
    rune = "M24,23L40,39L32,47V17L40,25L24,41"
    ic.add(f'<path d="{rune}" fill="none" stroke="#000" stroke-opacity=".3" stroke-width="5.4" stroke-linecap="round" stroke-linejoin="round"/>')
    ic.add(f'<path d="{rune}" fill="none" stroke="#fff" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/>')


def printers(ic):
    from devices import printer
    printer(ic)
    _badge(ic, 51, 50, 9, "blue", "M47,50H55M51,46V54")


def power_management(ic):
    """Power Management: a battery with a green charge level and a mains plug."""
    bat = rrect(4, 18, 40, 22, 3)
    ic.shadow(bat, 2.4, 2)
    ic.path("M44,24H48V34H44Z", "#8a9098", INK, 1)
    ic.path(bat, ic.lg([(0, "#f4f5f7"), (1, "#9aa0a8")]), INK, LW)
    ic.path("M7,21H30V37H7Z", ic.lg([(0, "#b4f0a0"), (.5, "#3fae2a"), (1, "#1e6a10")]), INK, .8)
    ic.add('<path d="M9,23H28" stroke="#fff" stroke-opacity=".5" stroke-width="1.2"/>')
    ic.add(f'<path d="M30,48Q30,56 40,56H52" fill="none" stroke="{INK}" stroke-width="3.4"/><path d="M30,48Q30,56 40,56H52" fill="none" stroke="#5c6168" stroke-width="1.8"/>')
    ic.path(rrect(24, 40, 12, 9, 2), ic.lg([(0, "#ffffff"), (1, "#9aa0a8")]), INK, 1.1)
    ic.add(f'<path d="M27.5,40V35M32.5,40V35" stroke="{INK}" stroke-width="2.6" stroke-linecap="round"/><path d="M27.5,40V35.5M32.5,40V35.5" stroke="#e8c43a" stroke-width="1.2" stroke-linecap="round"/>')


def energy_info(ic):
    """Energy information: a battery beside a little chart of its charge over time."""
    ic.shadow(rrect(18, 8, 42, 34, 3), 2.4, 2)
    ic.path(rrect(18, 8, 42, 34, 3), ic.lg([(0, "#ffffff"), (1, "#dfe2e6")]), INK, LW)
    ic.add('<path d="M23,36H55M23,13V36" stroke="#9aa0a8" stroke-width="1"/>')
    ic.add('<path d="M23,16L30,20L36,19L42,26L48,30L55,34" fill="none" stroke="#2f9a2e" stroke-width="2" stroke-linejoin="round"/>')
    bat = rrect(4, 30, 18, 28, 2.5)
    ic.shadow(bat, 2, 1.8)
    ic.path("M9,27H17V30H9Z", "#8a9098", INK, .9)
    ic.path(bat, ic.lg([(0, "#f4f5f7"), (1, "#9aa0a8")], 0, 0, 1, 0), INK, LW)
    ic.path("M7,42H19V55H7Z", ic.lg([(0, "#ffe080"), (1, "#c89a10")], 0, 0, 1, 0), INK, .8)


def disks_cameras(ic):
    """Disks & Cameras (category): the hard disk with the camera in front."""
    from devices import harddisk, camera
    _sub(ic, harddisk, 0, 0, .75)
    _sub(ic, camera, 22, 26, .6)


def smart_status(ic):
    """SMART Status: the hard disk with a heartbeat line, health being watched."""
    from devices import harddisk
    _sub(ic, harddisk, 0, 0, .8)
    _badge(ic, 48, 47, 12, "green", "M38,47H42.5L45,41L49,53L51.5,47H58")


def thunderbolt(ic):
    """Thunderbolt: a USB-C style plug and cable with a yellow spark (generic, not the logo)."""
    ic.add(f'<path d="M14,58Q14,44 24,40" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round"/><path d="M14,58Q14,44 24,40" fill="none" stroke="#5c6168" stroke-width="4" stroke-linecap="round"/>')
    ic.add('<g transform="rotate(-45 32 32)">')
    ic.path(rrect(20, 26, 22, 12, 3), ic.lg([(0, "#5c6168"), (1, "#14171c")]), INK, LW)
    ic.path(rrect(42, 28.5, 12, 7, 3.5), ic.lg([(0, "#ffffff"), (.5, "#b4b9c0"), (1, "#6c727a")]), INK, 1)
    ic.path(rrect(44, 30.6, 8, 2.8, 1.4), "#2c3036", None)
    ic.add("</g>")
    bolt = "M42,4L30,24H38L32,40L48,18H40L46,4Z"
    ic.shadow(bolt, 2, 1.8)
    ic.path(bolt, ic.lg([(0, "#fff6a0"), (.5, "#ffd21a"), (1, "#c88a04")], 0, 0, 1, 1), INK, LW)


def usb_devices(ic):
    """USB Devices / USB thumb drive (drive-removable-media-usb-pendrive): a USB stick with its silver plug and a
    blue body. 2026-10-27: enlarged to fill the icon, and the plug's two holes set side by side across its width
    near the tip, as on a real USB plug. The grey box (drive-removable-media-usb) stays for other USB drives."""
    ic.add('<g transform="translate(32,33) scale(1.55) translate(-33,-34)">')
    ic.add('<g transform="rotate(-35 32 34)">')
    ic.shadow(rrect(14, 26, 30, 16, 3), 2.4, 2)
    ic.path(rrect(42, 28.5, 12, 11, 1), ic.lg([(0, "#ffffff"), (.5, "#c3c7cd"), (1, "#6c727a")]), INK, 1)
    ic.path("M48.4,30.4H51.6V32.8H48.4Z M48.4,35.2H51.6V37.6H48.4Z", "#2c3036", None)
    ic.path(rrect(14, 26, 30, 16, 3), ic.lg([(0, "#9fd4ff"), (.5, "#2a6ac8"), (1, "#0e2e6a")]), INK, LW)
    ic.path(circle(19, 34, 2), "#fff", INK, .7)
    ic.add('<path d="M16,28.5H41" stroke="#fff" stroke-opacity=".45" stroke-width="1.2"/>')
    ic.add("</g></g>")


def block_devices(ic):
    """Block Devices: the original's three coloured blocks stacked together (green, blue, yellow)."""
    def cube(cx, cy, a, cols):
        h = a * .5
        top = f"M{cx},{cy - h}L{cx + a},{cy}L{cx},{cy + h}L{cx - a},{cy}Z"
        left = f"M{cx - a},{cy}L{cx},{cy + h}V{cy + h + a * 1.05}L{cx - a},{cy + a * 1.05}Z"
        right = f"M{cx + a},{cy}L{cx},{cy + h}V{cy + h + a * 1.05}L{cx + a},{cy + a * 1.05}Z"
        ic.shadow(top + left + right, 2.2, 1.8)
        ic.path(left, ic.lg([(0, cols[1]), (1, cols[2])]), INK, 1.1)
        ic.path(right, ic.lg([(0, cols[2]), (1, cols[3])]), INK, 1.1)
        ic.path(top, ic.lg([(0, cols[0]), (1, cols[1])], 0, 0, 1, 1), INK, 1.1)
    cube(25, 13, 13, ("#d4f8b0", "#6ad04a", "#2e8a22", "#14561a"))      # green, at the back
    cube(43, 24, 13, ("#d4e0ff", "#7a9aff", "#3a5ad8", "#1a2a8a"))      # blue, to the right
    cube(22, 34, 13, ("#fff6c0", "#f0d060", "#c8a020", "#7a5a04"))      # yellow, in front


def memory(ic):
    """Memory: a stick of RAM, green board, black chips, gold contacts."""
    ic.add('<g transform="rotate(-20 32 32)">')
    ic.shadow("M2,20H62V40H2Z", 2.4, 2)
    ic.path("M2,20H62V40H33V43H31V40H2Z", ic.lg([(0, "#5ac85a"), (1, "#1a6a24")], 0, 0, 0, 1), INK, LW)
    for k in range(4):
        ic.path(rrect(5 + k * 14.5, 23, 11, 10, .8), ic.lg([(0, "#3c4148"), (1, "#0a0c10")]), INK, .7)
    for k in range(26):
        if 13 <= k <= 14:
            continue
        ic.add(f'<rect x="{3.4 + k * 2.2:.1f}" y="35.5" width="1.3" height="4" fill="#e8c43a"/>')
    ic.add("</g>")


def _chip(ic, cx, cy, s_, lid=True):
    for k in range(5):
        o = -s_ / 2 + (k + .5) * s_ / 5
        for (x1, y1, x2, y2) in ((cx + o, cy - s_ / 2 - 4, cx + o, cy - s_ / 2), (cx + o, cy + s_ / 2, cx + o, cy + s_ / 2 + 4),
                                 (cx - s_ / 2 - 4, cy + o, cx - s_ / 2, cy + o), (cx + s_ / 2, cy + o, cx + s_ / 2 + 4, cy + o)):
            ic.add(f'<path d="M{x1:.1f},{y1:.1f}L{x2:.1f},{y2:.1f}" stroke="{INK}" stroke-width="3" stroke-linecap="round"/><path d="M{x1:.1f},{y1:.1f}L{x2:.1f},{y2:.1f}" stroke="#e8c43a" stroke-width="1.4" stroke-linecap="round"/>')
    ic.path(rrect(cx - s_ / 2, cy - s_ / 2, s_, s_, 2.4), ic.lg([(0, "#4c5158"), (1, "#14171c")], 0, 0, 1, 1), INK, LW)
    if lid:
        ic.path(rrect(cx - s_ / 3, cy - s_ / 3, s_ * 2 / 3, s_ * 2 / 3, 1.6), ic.lg([(0, "#ffffff"), (.5, "#c3c7cd"), (1, "#7b818a")], 0, 0, 1, 1), INK, 1)


def cpu_info(ic):
    """CPU: a processor chip with gold pins and a silver lid."""
    ic.shadow(rrect(14, 14, 36, 36, 3), 2.4, 2)
    _chip(ic, 32, 32, 34)


def interrupts(ic):
    """Interrupts: the processor chip with a red signal flash badge."""
    ic.shadow(rrect(10, 10, 32, 32, 3), 2.4, 2)
    _chip(ic, 26, 26, 30, lid=False)
    _badge(ic, 47, 47, 12, "red", "M49,39L43.5,48H50L45,55")


def network_card(ic):
    """Network Interfaces: the original's green network card, chips, traces, coloured LEDs, bracket and contacts."""
    ic.shadow("M10,10H60V46H10Z", 2.6, 2.2)
    ic.path("M4,5H9V58H4Z", ic.lg([(0, "#ffffff"), (.5, "#b4b9c0"), (1, "#5c6168")], 0, 0, 1, 0), INK, 1)          # bracket
    ic.path("M5.5,24H8.5V34H5.5Z", "#2c3036", None)
    ic.path("M9,10H60V44H9Z", ic.lg([(0, "#7ae07a"), (.55, "#3aa83a"), (1, "#1a6a24")], 0, 0, 1, 1), INK, LW)          # board
    traces = "M18,20H30L34,24H46M20,30H26L30,26M36,30H44L48,34M14,38H24L28,34M40,38H52"
    ic.add(f'<path d="{traces}" fill="none" stroke="#c8f4a0" stroke-opacity=".8" stroke-width=".9"/>')
    for x, y, w, h in ((14, 14, 10, 9), (36, 26, 9, 8), (47, 16, 8, 7)):
        ic.path(f"M{x},{y}H{x + w}V{y + h}H{x}Z", ic.lg([(0, "#4c5158"), (1, "#0a0c10")]), INK, .7)
    for k, col in enumerate(("#ff3a2a", "#3a6aff", "#3a6aff", "#ff3a2a")):
        ic.path(rrect(28 + k * 4, 13, 2.6, 2.6, .6), col, INK, .4)
    ic.path("M14,44H52V51H14Z", "#ffffff", INK, 1)                                                                    # edge connector
    for k in range(12):
        ic.add(f'<rect x="{15.5 + k * 3:.1f}" y="45" width="1.8" height="5" fill="#e8c43a" stroke="#7a5a04" stroke-width=".3"/>')


def peripherals(ic):
    """Connected Devices (category): a laptop with a phone plugged into its side by a cable."""
    ic.shadow("M4,18H42V44H4Z", 2.4, 2)
    ic.path("M1,44H45L47,50H-1Z", ic.lg([(0, "#c3c7cd"), (1, "#7b818a")]), INK, LW)
    ic.path(rrect(5, 16, 36, 28, 2), ic.lg([(0, "#5c6168"), (1, "#14171c")]), INK, LW)
    ic.path("M8,19H38V41H8Z", ic.lg([(0, "#9fd4ff"), (1, "#1a5c9e")]), INK, .8)
    ic.add('<path d="M9,20H37V28Q23,31 9,28Z" fill="#fff" fill-opacity=".18"/>')
    # cable: from the phone's foot, down and round into a port on the laptop's right side
    cab = "M54,50V54Q54,58 50,58H44Q40.5,58 40.5,54V50.5"
    ic.add(f'<path d="{cab}" fill="none" stroke="{INK}" stroke-width="3.4" stroke-linecap="round"/><path d="{cab}" fill="none" stroke="#e8e8e8" stroke-width="1.8" stroke-linecap="round"/>')
    ic.path(rrect(38.6, 46.6, 3.8, 4.6, .8), "#8a9098", INK, .7)
    ph = rrect(47, 18, 14, 30, 3)
    ic.shadow(ph, 2, 1.8)
    ic.path(ph, ic.lg([(0, "#5c6168"), (1, "#14171c")], 0, 0, 1, 0), INK, LW)
    ic.path("M49.5,22H58.5V42H49.5Z", ic.lg([(0, "#b4f0a0"), (1, "#2f8a2e")]), INK, .7)
    ic.path(circle(54, 45, 1.3), "#4c5158", None)
    ic.path(rrect(52, 47.5, 4, 3, .6), "#8a9098", INK, .6)


def night_light(ic):
    """Night Light: a monitor glowing warm orange, a crescent moon on the screen."""
    def scr(ic):
        ic.path(f"M{SX + 15},{SY + 7}A9,9 0 1 0 {SX + 26},{SY + 21}A7,7 0 1 1 {SX + 15},{SY + 7}Z", "#fff6c8", None)
        for x, y in ((SX + 32, SY + 7), (SX + 37, SY + 15), (SX + 30, SY + 20)):
            ic.path(circle(x, y, 1.1), "#fff6c8", None)
    monitor(ic, scr, glass=("#ffb05a", "#e86a1a", "#8a3404"))


# ------------------------------------------------------------------ personal, region, network, security, search
def _person(ic, cx, top, s_=1.0, shirt=("#9fd4ff", "#1a5c9e")):
    head = circle(cx, top + 7 * s_, 7 * s_)
    body = (f"M{cx - 12 * s_},{top + 34 * s_}C{cx - 12 * s_},{top + 21 * s_} {cx - 7 * s_},{top + 16 * s_} {cx},{top + 16 * s_}"
            f"C{cx + 7 * s_},{top + 16 * s_} {cx + 12 * s_},{top + 21 * s_} {cx + 12 * s_},{top + 34 * s_}Z")
    ic.shadow(head + body, 2.2, 1.8)
    ic.path(body, ic.lg([(0, shirt[0]), (1, shirt[1])]), INK, LW)
    ic.path(head, ic.rg([(0, "#fff1e2"), (.7, "#f0c8a0"), (1, "#c88a5a")], .4, .3, .8), INK, LW)


def _profile(ic, x, y, k, hair, skin=("#fff1e2", "#f0c8a0", "#c88a5a")):
    """A cartoon head in profile facing left (as on the original KDE user icons)."""
    t = f"translate({x},{y}) scale({k})"
    face = ("M16,1C9,1 4.5,4 4,9.5C3.8,11 3.2,12 2,13.6C1,15 1.6,16 3,16.2C2.8,17.4 3.4,18 3,19.2"
            "C2.8,21 4,23 7,23.6C9,24 11,24 12.4,23.6L13,29H22L22.6,20C24.6,17 24.6,6 16,1Z")
    hair_d = ("M3.6,9.6C3.4,3.6 9,0 16,0C24,0 26.4,8 24,16C23.4,18 22.6,19.6 21.6,20.4C21.4,17 20,14 17.6,12.4"
              "C15.4,11 13.4,9.8 12.4,7.6C10,9.8 6.6,10.4 3.6,9.6Z")
    ic.add(f'<g transform="{t}">')
    ic.shadow(face, 1.6, 1.4)
    ic.path(face, ic.lg([(0, skin[0]), (.6, skin[1]), (1, skin[2])], 0, 0, 1, 1), INK, 1.2)
    ic.path(hair_d, ic.lg([(0, hair[0]), (1, hair[1])], 0, 0, 1, 1), INK, 1.1)
    ic.path("M15.4,13.2A2.2,3 0 1 1 15.41,13.2Z", skin[2], INK, .8)                    # ear
    ic.path(circle(6.6, 11.6, 1), INK, None)                                          # eye
    ic.add(f'<path d="M3.8,20.2Q5.4,20.6 6.6,20" fill="none" stroke="#8a4a2a" stroke-width=".8" stroke-linecap="round"/>')
    ic.add("</g>")


def _terminal_monitor(ic, prompt=True, glass=("#3a3f46", "#14171c", "#000000")):
    def scr(ic):
        if prompt:
            ic.add(f'<path d="M{SX + 4},{SY + 5}L{SX + 8},{SY + 8.5}L{SX + 4},{SY + 12}M{SX + 10},{SY + 12}H{SX + 15}" fill="none" stroke="#5aff6a" stroke-width="1.6" stroke-linecap="square"/>')
    monitor(ic, scr, bezel=("#f4f5f7", "#9aa0a8"), glass=glass)


def users(ic):
    """Users: as in the original, a terminal monitor with two faces in profile looking at it."""
    _terminal_monitor(ic)
    _profile(ic, 26.5, 11, 1.05, ("#ffb070", "#a8400a"))       # ginger hair, behind
    _profile(ic, 35, 22, 1.1, ("#5a5048", "#14100c"))        # dark hair, in front


def personalisation(ic):
    """Personalisation (category): the monitor with one face in profile and a gold star: your own settings."""
    _terminal_monitor(ic, prompt=False, glass=("#3a6fd8", "#1a3ea8", "#0c2470"))
    _profile(ic, 31.5, 16, 1.2, ("#fff0a0", "#c89a20"))        # fair hair
    d = ""
    for k in range(10):
        a = 2 * math.pi * k / 10 - math.pi / 2
        r = 7.5 if k % 2 == 0 else 3.3
        d += ("M" if k == 0 else "L") + f"{20 + r * math.cos(a):.2f},{23 + r * math.sin(a):.2f}"
    ic.path(d + "Z", ic.rg([(0, "#fffbe0"), (.5, "#ffd21a"), (1, "#c88a04")]), INK, 1)


def _wave_flag(ic, x0, y0, w, h, stripes, amp=3.2, waves=1.25, disc=None):
    """A flag on a pole, waving: horizontal stripes follow a sine wave, with light and shadow folds."""
    N = 24
    def yat(x, f):
        return y0 + f * h + amp * math.sin(2 * math.pi * waves * (x - x0) / w) * (1 - .25 * f) + .12 * (x - x0) * f * 0
    def pts(f, rev=False):
        xs = [x0 + w * i / N for i in range(N + 1)]
        if rev:
            xs = xs[::-1]
        return [(x, yat(x, f)) for x in xs]
    def poly(p):
        return "M" + "L".join(f"{x:.2f},{y:.2f}" for x, y in p) + "Z"
    outline = poly(pts(0) + pts(1, True))
    # pole
    ic.shadow(outline, 1.8, 1.6)
    pole = rrect(x0 - 3.2, y0 - 3, 3.2, 64 - y0 - 2, 1.4)
    ic.path(pole, ic.lg([(0, "#c8a070"), (.5, "#8a5a2a"), (1, "#4a2a10")], 0, 0, 1, 0), INK, 1)
    ic.path(circle(x0 - 1.6, y0 - 3.4, 2.2), ic.rg([(0, "#fff4c0"), (1, "#c89a20")]), INK, .9)
    n = len(stripes)
    for i, col in enumerate(stripes):
        ic.path(poly(pts(i / n) + pts((i + 1) / n, True)), col, None)
    if disc:
        cx, cy, r, col = disc
        d = "M" + "L".join(f"{cx + r * math.cos(t):.2f},{cy + r * math.sin(t) + amp * math.sin(2 * math.pi * waves * (cx + r * math.cos(t) - x0) / w):.2f}"
                           for t in [2 * math.pi * k / 32 for k in range(32)]) + "Z"
        ic.path(d, col, None)
    # folds: light crests and dark troughs running down the cloth
    stops, k = [], 0
    for j in range(9):
        ph = j / 8
        v = math.cos(2 * math.pi * waves * ph)
        stops.append((ph, "#ffffff" if v > 0 else "#000000", abs(v) * (.32 if v > 0 else .3)))
    gid = ic.gid("fold")
    st = "".join(f'<stop offset="{o:.3f}" stop-color="{c}" stop-opacity="{a:.2f}"/>' for o, c, a in stops)
    ic.defs.append(f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{x0 + w * .2:.2f}" y1="0" x2="{x0 + w * 1.0:.2f}" y2="0">{st}</linearGradient>')
    ic.add(f'<path d="{outline}" fill="url(#{gid})"/>')
    ic.path(outline, "none", INK, 1.4)


def region(ic):
    """Region & Language: two waving flags on poles, as in KDE 3's locale icon."""
    _wave_flag(ic, 8, 7, 44, 27, ["#ffffff"], amp=3, disc=(28, 20.5, 6.4, "#d8141c"))
    _wave_flag(ic, 16.5, 25, 44.5, 30, ["#1a1a1a", "#dd1a10", "#ffcc00"], amp=3.4)


def date_time(ic):
    """Date & Time: a round wall clock in front of a calendar page."""
    ic.shadow(rrect(28, 6, 32, 34, 3), 2, 1.8)
    ic.path(rrect(28, 6, 32, 34, 3), ic.lg([(0, "#ffffff"), (1, "#dfe2e6")]), INK, LW)
    ic.path("M31,6H57Q60,6 60,9V14H28V9Q28,6 31,6Z", ic.lg([(0, "#ff8a7a"), (1, "#b8180c")]), INK, 1)
    grid = "".join(f"M{28 + k * 6.4:.1f},14V40" for k in range(1, 5)) + "".join(f"M28,{14 + k * 6.5:.1f}H60" for k in range(1, 4))
    ic.add(f'<path d="{grid}" stroke="#b4b9c0" stroke-width=".7"/>')
    cx, cy, r = 24, 38, 19
    ic.shadow(circle(cx, cy, r), 2.6, 2.2)
    ic.path(circle(cx, cy, r), ic.lg([(0, "#e4e6e9"), (1, "#7b818a")], 0, 0, 1, 1), INK, LW)
    ic.path(circle(cx, cy, r - 3.2), ic.rg([(0, "#ffffff"), (1, "#e4e6e9")]), INK, 1)
    for k in range(12):
        a = 2 * math.pi * k / 12
        r1 = r - 5.2 if k % 3 == 0 else r - 4.4
        ic.add(f'<path d="M{cx + r1 * math.sin(a):.2f},{cy - r1 * math.cos(a):.2f}L{cx + (r - 3.8) * math.sin(a):.2f},{cy - (r - 3.8) * math.cos(a):.2f}" stroke="{INK}" stroke-width="{1.4 if k % 3 == 0 else .8}"/>')
    ic.add(f'<path d="M{cx},{cy}L{cx},{cy - 10}M{cx},{cy}L{cx + 7},{cy + 3}" stroke="{INK}" stroke-width="2.2" stroke-linecap="round"/>')
    ic.add(f'<path d="M{cx},{cy}L{cx - 7},{cy + 9}" stroke="#d8302a" stroke-width="1" stroke-linecap="round"/>')
    ic.path(circle(cx, cy, 1.6), INK, None)


BELL_BRASS = ("#6a6a48", "#cfcfb0", "#f2f2e0", "#a8a882", "#4a4a30", "#5e5e3e")
BELL_GREY = ("#4c5158", "#c3c7cd", "#f4f5f7", "#9aa0a8", "#2c3036", "#5c6168")


def notifications(ic, metal=BELL_BRASS):
    """Notifications: KDE 3's hand bell, a pale brass bell with a turned wooden handle, seen from slightly above.
    `metal` recolours the bell for notification states (BELL_GREY when quiet or off)."""
    body = ("M10,54.5C10,52.4 12.6,51.6 14.5,49.6C17.2,46.4 17.6,41 18,34C18.4,28.6 23.5,26 32,26C40.5,26 45.6,28.6 46,34"
            "C46.4,41 46.8,46.4 49.5,49.6C51.4,51.6 54,52.4 54,54.5A22,5.6 0 0 1 10,54.5Z")
    ic.shadow(body, 2.6, 2.2)
    ic.path(body, ic.lg([(0, metal[0]), (.18, metal[1]), (.34, metal[2]), (.62, metal[3]), (1, metal[4])], 0, 0, 1, 0), INK, LW)
    # crown seen from above, rim band and lip following the ellipse
    ic.add(f'<path d="M19.6,31.4A12.6,3.4 0 0 0 44.4,31.4" fill="none" stroke="{metal[5]}" stroke-width=".9" stroke-opacity=".6"/>')
    ic.add(f'<path d="M12.2,52.2A20,4.6 0 0 0 51.8,52.2" fill="none" stroke="{metal[5]}" stroke-width="1" stroke-opacity=".7"/>')
    ic.add('<path d="M11.6,55.4A20.6,4.8 0 0 0 52.4,55.4" fill="none" stroke="#fff" stroke-width=".9" stroke-opacity=".55"/>')
    ic.add('<path d="M23,33.6Q22.2,43 20.4,49" fill="none" stroke="#fff" stroke-opacity=".75" stroke-width="2.4" stroke-linecap="round"/>')
    # handle: a slim oval of turned wood on a bead, set in a narrow collar (2026-10-27: was a straight shaft)
    w = 6.4
    wood = ic.lg([(0, "#5a2806"), (.28, "#b8622a"), (.45, "#d88a50"), (.72, "#8e4414"), (1, "#3e1a04")], 0, 0, 1, 0)
    ic.path(f"M{32 - w},26.6V24.2A{w},2.2 0 0 1 {32 + w},24.2V26.6A{w},2.2 0 0 1 {32 - w},26.6Z", wood, INK, 1.1)
    ic.path(f"M{32 - w},24.2A{w},2.2 0 0 1 {32 + w},24.2A{w},2.2 0 0 1 {32 - w},24.2Z", "#c87a3e", INK, .8)
    ic.path("M32,25A3.6,2.2 0 1 1 32.01,25Z", ic.rg([(0, "#f0aa70"), (1, "#5a2806")], .4, .3, .9), INK, .9)
    ic.path("M32,21.6A5.6,10.35 0 1 1 32.01,21.6Z",
            ic.rg([(0, "#f4b880"), (.35, "#c8763a"), (.75, "#8a4012"), (1, "#3e1a04")], .36, .3, .78), INK, 1.1)
    ic.add('<path d="M28.6,6.6Q27.7,10.8 28.8,14.6" fill="none" stroke="#fff" stroke-opacity=".55" stroke-width="1.6" stroke-linecap="round"/>')


def accessibility(ic):
    """Accessibility: as in the original, the white wheelchair symbol on a glossy blue tile."""
    t = rrect(5, 5, 54, 54, 7)
    ic.shadow(t, 2.6, 2.2)
    ic.path(t, ic.lg([(0, "#8ac0ff"), (.45, "#2a6ac8"), (1, "#0e2e6a")], 0, 0, .35, 1), INK, LW)
    ic.add('<path d="M9,16Q9,9 16,9H48Q55,9 55,16V26Q32,33 9,26Z" fill="#fff" fill-opacity=".28"/>')
    # the International Symbol of Access (public domain), traced from the MUTCD D9-6 sign the user supplied
    import json, os
    d = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "traced", "isa.json")))["isa"]
    ic.add(f'<path d="{d}" fill="#ffffff" fill-rule="evenodd" transform="translate(32,33) scale(.8) translate(-31.9,-31.9)"/>')

def networking(ic):
    """Wi-Fi & Networking: the globe with Wi-Fi waves above a network cable plug."""
    e_globe(ic, 2, 14, 18)
    for k, r in enumerate((8, 14, 20)):
        ic.add(f'<path d="M{48 - r * .78:.1f},{34 - r * .62:.1f}A{r},{r} 0 0 1 {48 + r * .78:.1f},{34 - r * .62:.1f}" fill="none" stroke="{INK}" stroke-width="4.2" stroke-linecap="round"/>')
        ic.add(f'<path d="M{48 - r * .78:.1f},{34 - r * .62:.1f}A{r},{r} 0 0 1 {48 + r * .78:.1f},{34 - r * .62:.1f}" fill="none" stroke="#3a8ee0" stroke-width="2.4" stroke-linecap="round"/>')
    ic.path(circle(48, 34, 2.6), "#3a8ee0", INK, 1)
    ic.path(rrect(40, 44, 16, 12, 2), ic.lg([(0, "#ffffff"), (1, "#9aa0a8")]), INK, 1.2)
    ic.add('<path d="M43,44V47M46,44V47M49,44V47M52,44V47" stroke="#c89a10" stroke-width="1.2"/>')
    ic.add(f'<path d="M48,56V62" stroke="{INK}" stroke-width="4"/><path d="M48,56V62" stroke="#3a8ee0" stroke-width="2.2"/>')


def network_sharing(ic):
    """Samba / network sharing: a yellow folder with a network of three linked computers."""
    from gen import folder
    ic.add('<g transform="translate(-2,-4) scale(.85)">')
    folder(ic, "yellow")
    ic.add("</g>")
    pts = ((44, 36), (34, 54), (56, 54))
    ic.add(f'<path d="M44,40L34,52M44,40L56,52M34,54H56" stroke="{INK}" stroke-width="2.6"/><path d="M44,40L34,52M44,40L56,52M34,54H56" stroke="#3a8ee0" stroke-width="1.2"/>')
    for x, y in pts:
        ic.path(rrect(x - 5.5, y - 4.5, 11, 8.5, 1.4), ic.lg([(0, "#fbf9f2"), (1, "#b4b0a3")]), INK, 1.1)
        ic.path(rrect(x - 3.8, y - 3, 7.6, 5, .6), ic.lg([(0, "#3a6fd8"), (1, "#0c2470")]), None)


def firewall(ic):
    """Firewall: a red brick wall with a flame rising behind it."""
    flame = "M34,4C40,14 50,16 48,28C47,34 42,36 40,30C42,24 36,20 34,26C30,20 26,14 34,4Z M22,10C26,18 30,20 28,28C26,32 20,30 20,24C18,18 20,16 22,10Z"
    ic.path(flame, ic.lg([(0, "#ffe23a"), (.5, "#ff8a10"), (1, "#d8301a")]), "#7a2004", 1.2)
    wall = "M4,26H60V58H4Z"
    ic.shadow(wall, 2.6, 2.2)
    ic.path(wall, ic.lg([(0, "#f0805a"), (1, "#a0300c")]), INK, LW)
    mortar = "".join(f"M4,{26 + k * 8}H60" for k in range(1, 4))
    for r in range(4):
        off = 0 if r % 2 == 0 else 7
        for x in range(4 + off, 60, 14):
            mortar += f"M{x},{26 + r * 8}V{34 + r * 8}"
    ic.add(f'<path d="{mortar}" stroke="#f4e4d0" stroke-width="1.4"/>')
    ic.path(wall, "none", INK, LW)


def firmware_security(ic):
    """Firmware Security: a firmware chip (no lid, unlike CPU) with a gold padlock in the centre."""
    ic.shadow(rrect(14, 14, 36, 36, 3), 2.4, 2)
    _chip(ic, 32, 32, 36, lid=False)
    ic.add('<g transform="translate(32,34) scale(.82) translate(-32,-34)">')
    ic.add('<path d="M25,32V25.5A7,7 0 0 1 39,25.5V32" fill="none" stroke="#14171c" stroke-width="5.2"/>')
    ic.add('<path d="M25,32V25.5A7,7 0 0 1 39,25.5V32" fill="none" stroke="url(#shk)" stroke-width="3"/>')
    ic.defs.append('<linearGradient id="shk" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ffffff"/><stop offset=".5" stop-color="#c3c7cd"/><stop offset="1" stop-color="#7b818a"/></linearGradient>')
    body = rrect(21.5, 30.5, 21, 16, 2.4)
    ic.path(body, ic.lg([(0, "#fff3a6"), (.5, "#e8c43a"), (1, "#a87a10")], 0, 0, 0, 1), INK, 1.2)
    ic.add('<path d="M23.5,33.5H40.5" stroke="#fff" stroke-opacity=".6" stroke-width="1.2" stroke-linecap="round"/>')
    ic.path("M32,35.6A2.4,2.4 0 0 1 33.3,40V42.6H30.7V40A2.4,2.4 0 0 1 32,35.6Z", "#5a3a04", None)
    ic.add('</g>')


def _magnifier(ic, cx, cy, r, glass=("#e8f6ff", "#9ad0f0"), handle_len=16):
    a = math.radians(45)
    hx, hy = cx + r * math.cos(a), cy + r * math.sin(a)
    ex, ey = hx + handle_len * math.cos(a), hy + handle_len * math.sin(a)
    ic.add(f'<path d="M{hx:.1f},{hy:.1f}L{ex:.1f},{ey:.1f}" stroke="{INK}" stroke-width="8.4" stroke-linecap="round"/>')
    ic.add(f'<path d="M{hx:.1f},{hy:.1f}L{ex:.1f},{ey:.1f}" stroke="#8a5a2a" stroke-width="6" stroke-linecap="round"/>')
    ic.add(f'<path d="M{hx + 1:.1f},{hy:.1f}L{ex - 1:.1f},{ey - 2:.1f}" stroke="#c8965c" stroke-width="1.4" stroke-linecap="round"/>')
    ic.shadow(circle(cx, cy, r + 2.5), 2.2, 1.8)
    ic.path(circle(cx, cy, r + 2.5), ic.lg([(0, "#ffffff"), (1, "#7b818a")], 0, 0, 1, 1), INK, LW)
    ic.path(circle(cx, cy, r), ic.rg([(0, glass[0]), (1, glass[1])], .35, .3, .8), INK, 1, ' fill-opacity=".85"')
    ic.add(f'<path d="M{cx - r * .6:.1f},{cy - r * .2:.1f}Q{cx - r * .5:.1f},{cy - r * .6:.1f} {cx - r * .1:.1f},{cy - r * .65:.1f}" fill="none" stroke="#fff" stroke-width="1.8" stroke-linecap="round"/>')


def search_category(ic):
    """Search (category): a big magnifying glass."""
    _magnifier(ic, 26, 26, 16, handle_len=18)


def file_search(ic):
    """File Search: the magnifier over a page of text."""
    ic.shadow("M14,4H40L50,14V58H14Z", 2.4, 2)
    ic.path("M14,4H40L50,14V58H14Z", ic.lg([(0, "#ffffff"), (1, "#e2d4b8")], 0, 0, 1, 1), INK, LW)
    ic.path("M40,4V14H50", "#eeeae4", INK, 1)
    ic.add('<path d="M19,20H44M19,25H40M19,30H44M19,35H36" stroke="#9a8e74" stroke-width="1.3"/>')
    _magnifier(ic, 30, 40, 9.5, handle_len=10)


def plasma_search(ic):
    """Plasma Search: the magnifier over the launcher's search field, with a sparkle."""
    ic.shadow(rrect(4, 8, 56, 16, 8), 2, 1.8)
    ic.path(rrect(4, 8, 56, 16, 8), ic.lg([(0, "#ffffff"), (1, "#c3d4e4")]), INK, LW)
    ic.add('<path d="M14,16H40" stroke="#5a7aa0" stroke-width="1.6" stroke-dasharray="3 2"/>')
    _magnifier(ic, 26, 40, 11, handle_len=12)
    d = ""
    for k in range(8):
        a = math.pi * k / 4
        rr = 6 if k % 2 == 0 else 2
        d += ("M" if k == 0 else "L") + f"{52 + rr * math.cos(a):.2f},{38 + rr * math.sin(a):.2f}"
    ic.path(d + "Z", ic.rg([(0, "#ffffff"), (1, "#ffc21a")]), "#8a5a04", .7)


def krunner(ic):
    """KRunner: the dark run bar dropping from the top of the screen, a prompt and a magnifier."""
    ic.path("M4,6H60V10H4Z", "#5c6168", INK, 1)
    bar = rrect(6, 10, 52, 20, 3)
    ic.shadow(bar, 2.4, 2)
    ic.path(bar, ic.lg([(0, "#3c4148"), (1, "#14171c")]), INK, LW)
    ic.add('<path d="M12,16L16,20L12,24M19,24H27" fill="none" stroke="#9fd4ff" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>')
    ic.path(rrect(10, 34, 44, 22, 3), ic.lg([(0, "#ffffff"), (1, "#dfe2e6")]), INK, LW)
    for k, col in enumerate(("#3a8ee0", "#4fae5a", "#e8a010")):
        ic.path(rrect(14, 37 + k * 6, 5, 5, 1), col, INK, .5)
        ic.add(f'<path d="M22,{39.5 + k * 6}H{44 - k * 4}" stroke="#7b818a" stroke-width="1.3"/>')
    _magnifier(ic, 47, 20, 4.2, handle_len=4)


def default_apps(ic):
    """Default Applications: three app windows stacked, the front one with a green tick."""
    for k, title in enumerate((("#ffd0a0", "#c8601a"), ("#b4f0a0", "#2f8a2e"), ("#9fd4ff", "#1a5c9e"))):
        window(ic, 4 + k * 7, 6 + k * 8, 38, 28, title=title)
    ic.add('<path d="M23,36H44M23,41H40" stroke="#9aa0a8" stroke-width="1.3"/>')
    from settings import _badge
    _badge(ic, 49, 49, 10, "green", "M44,49L48,53L54.5,45")


def spelling(ic):
    """Spell Check: "abc" on a page with a red wavy underline and a green tick."""
    ic.shadow("M8,8H44L54,18V56H8Z", 2.4, 2)
    ic.path("M8,8H44L54,18V56H8Z", ic.lg([(0, "#ffffff"), (1, "#e2d4b8")], 0, 0, 1, 1), INK, LW)
    ic.path("M44,8V18H54", "#eeeae4", INK, 1)
    from filetypes import GLYPHS
    d, x = "", 0.0
    for ch in "abc":
        g, w = GLYPHS[ch]
        d += f'<path d="{g}" transform="translate({x:.2f},0)"/>'
        x += w + 1.3
    ic.add(f'<g transform="translate(13,34) scale(2.6)" fill="none" stroke="{INK}" stroke-width=".8" stroke-linecap="round" stroke-linejoin="round">{d}</g>')
    wave = "M13,40" + "".join(f"q1.5,{-2 if k % 2 == 0 else 2} 3,0" for k in range(9))
    ic.add(f'<path d="{wave}" fill="none" stroke="#d8302a" stroke-width="1.4"/>')
    _badge(ic, 48, 48, 9.5, "green", "M43.5,48L47,51.5L53,44.5")


def user_feedback(ic):
    """User Feedback: a speech bubble holding a small bar chart."""
    b = "M8,8H56Q60,8 60,12V40Q60,44 56,44H28L18,54V44H8Q4,44 4,40V12Q4,8 8,8Z"
    ic.shadow(b, 2.6, 2.2)
    ic.path(b, ic.lg([(0, "#ffffff"), (1, "#c3d4e4")]), INK, LW)
    for k, (h, col) in enumerate(((12, "#3a8ee0"), (20, "#4fae5a"), (8, "#e8a010"), (16, "#d8302a"))):
        x = 14 + k * 10
        ic.path(f"M{x},{38 - h}H{x + 7}V38H{x}Z", ic.lg([(0, "#ffffff"), (.3, col), (1, col)], 0, 0, 1, 0), INK, .8)
    ic.add(f'<path d="M11,38.5H53" stroke="{INK}" stroke-width="1"/>')


def software_update(ic):
    """Software Update: the cardboard package with green circling update arrows."""
    from filetypes import box
    box(ic, 6, 18, 16, 20)
    cx, cy, r = 44, 22, 13
    ic.add(f'<path d="M{cx - r},{cy}A{r},{r} 0 0 1 {cx + r * .7:.1f},{cy - r * .7:.1f}" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>')
    ic.add(f'<path d="M{cx + r},{cy}A{r},{r} 0 0 1 {cx - r * .7:.1f},{cy + r * .7:.1f}" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>')
    ic.add(f'<path d="M{cx - r},{cy}A{r},{r} 0 0 1 {cx + r * .7:.1f},{cy - r * .7:.1f}" fill="none" stroke="#3fae2a" stroke-width="4" stroke-linecap="round"/>')
    ic.add(f'<path d="M{cx + r},{cy}A{r},{r} 0 0 1 {cx - r * .7:.1f},{cy + r * .7:.1f}" fill="none" stroke="#3fae2a" stroke-width="4" stroke-linecap="round"/>')
    ic.path(f"M{cx + 4},{cy - 16}L{cx + 13},{cy - 10}L{cx + 4},{cy - 4}Z", "#3fae2a", INK, 1)
    ic.path(f"M{cx - 4},{cy + 16}L{cx - 13},{cy + 10}L{cx - 4},{cy + 4}Z", "#3fae2a", INK, 1)


LOCATIONS_COLOURS = ("green", "yellow", "blue")     # back, middle, front


def locations(ic, colours=None):
    """Locations / file manager: three classic folders fanned out, one place behind another."""
    from gen import folder
    back, mid, front = colours or LOCATIONS_COLOURS
    for col, tx, ty in ((back, 0, 0), (mid, 9, 10), (front, 18, 20)):
        ic.add(f'<g transform="translate({tx},{ty}) scale(.7)">')
        folder(ic, col)
        ic.add("</g>")


# ------------------------------------------------------------------ workspace, session, categories, info
def _gear(ic, cx, cy, R, n=8, colours=("#ffffff", "#c3c7cd", "#6c727a"), hub=True):
    """KDE Classic's system-run gear: broad teeth with rounded tips, polished steel lit from the top-left,
    a raised inner ring and a small hole right through the middle."""
    root, half = R * .68, math.pi / n
    d = ""
    for k in range(n):
        a = 2 * math.pi * k / n
        b0, t0, t1, b1 = a - half * .62, a - half * .44, a + half * .44, a + half * .62
        P = lambda ang, rad: f"{cx + rad * math.cos(ang):.2f},{cy + rad * math.sin(ang):.2f}"
        d += ("M" if k == 0 else "L") + P(b0, root) + "L" + P(t0, R * .97)
        d += "Q" + P(a, R * 1.06) + " " + P(t1, R * .97) + "L" + P(b1, root)
        d += f"A{root:.2f},{root:.2f} 0 0 1 " + P(a + 2 * half - half * .62, root)
    d += "Z"
    hole = R * .17
    hd = f"M{cx - hole:.2f},{cy:.2f}A{hole:.2f},{hole:.2f} 0 1 0 {cx + hole:.2f},{cy:.2f}A{hole:.2f},{hole:.2f} 0 1 0 {cx - hole:.2f},{cy:.2f}Z"
    ic.shadow(d, 2.2, 1.8)
    body = ic.lg([(0, colours[0]), (.45, colours[1]), (.85, colours[2]), (1, "#3c4148")], 0, 0, 1, 1)
    ic.add(f'<path d="{d}{hd if hub else ""}" fill="{body}" fill-rule="evenodd" stroke="{INK}" stroke-width="{LW * 1.2}" stroke-linejoin="round"/>')
    if hub:
        rr = R * .42
        ring = f"M{cx - rr:.2f},{cy:.2f}A{rr:.2f},{rr:.2f} 0 1 0 {cx + rr:.2f},{cy:.2f}A{rr:.2f},{rr:.2f} 0 1 0 {cx - rr:.2f},{cy:.2f}Z"
        ic.add(f'<path d="{ring}{hd}" fill="{ic.lg([(0, colours[1]), (.6, colours[0]), (1, colours[0])], 0, 0, 1, 1)}" fill-rule="evenodd" stroke="{INK}" stroke-opacity=".35" stroke-width="1"/>')
        ic.add(f'<path d="{hd}" fill="none" stroke="{INK}" stroke-width="1.2"/>')
    ic.add(f'<path d="M{cx - R * .62:.2f},{cy - R * .1:.2f}Q{cx - R * .55:.2f},{cy - R * .55:.2f} {cx - R * .1:.2f},{cy - R * .62:.2f}" fill="none" stroke="#fff" stroke-opacity=".75" stroke-width="1.4" stroke-linecap="round"/>')


def activities(ic):
    """Activities: three desktops fanned out like cards, blue, green and orange."""
    for k, col in enumerate((("#ffd0a0", "#c8601a"), ("#b4f0a0", "#2f8a2e"), ("#9fd4ff", "#1a5c9e"))):
        x, y = 4 + k * 8, 6 + k * 9
        ic.shadow(rrect(x, y, 40, 30, 3), 2.2, 1.8)
        ic.path(rrect(x, y, 40, 30, 3), ic.lg([(0, col[0]), (1, col[1])], 0, 0, 1, 1), INK, LW)
        ic.path(f"M{x},{y + 26}H{x + 40}V{y + 27}Q{x + 40},{y + 30} {x + 37},{y + 30}H{x + 3}Q{x},{y + 30} {x},{y + 27}Z", "#1a1e26", None, ' fill-opacity=".55"')
    ic.add('<path d="M25,32H48M25,37H42" stroke="#fff" stroke-opacity=".8" stroke-width="1.4"/>')


def virtual_desktops(ic):
    """Virtual Desktops: the pager, four desktops in a grid, the current one lit blue."""
    ic.shadow(rrect(4, 8, 56, 48, 4), 2.6, 2.2)
    ic.path(rrect(4, 8, 56, 48, 4), ic.lg([(0, "#e4e6e9"), (1, "#7b818a")], 0, 0, .3, 1), INK, LW)
    for r in range(2):
        for c in range(2):
            x, y = 8 + c * 25, 12 + r * 21
            lit = (r, c) == (0, 1)
            ic.path(rrect(x, y, 23, 19, 2), ic.lg([(0, "#9fd4ff"), (1, "#1a5c9e")]) if lit else ic.lg([(0, "#5c6878"), (1, "#2c3440")]), INK, 1)
            ic.path(rrect(x + 3, y + 3, 11, 8, 1), "#ffffff" if lit else "#8a96a8", None, ' fill-opacity=".85"')


def task_switcher(ic):
    """Task Switcher: a row of window thumbnails, the middle one picked, as with Alt+Tab."""
    ic.shadow(rrect(2, 12, 60, 36, 6), 2.6, 2.2)
    ic.path(rrect(2, 12, 60, 36, 6), ic.lg([(0, "#3c4148"), (1, "#14171c")], 0, 0, 0, 1), INK, LW, ' fill-opacity=".92"')
    for k, x in enumerate((6, 22.5, 39)):
        if k == 1:
            ic.path(rrect(x - 2, 16, 23, 24, 3), "none", "#5ab8ff", 2)
        window(ic, x, 19, 19, 15, title=(("#ffd0a0", "#c8601a"), ("#9fd4ff", "#1a5c9e"), ("#b4f0a0", "#2f8a2e"))[k], buttons=False, shadow=False)
    ic.add('<path d="M22,44H42" stroke="#9fd4ff" stroke-width="1.6" stroke-linecap="round"/>')


def window_behaviour(ic):
    """Window Behavior: a window being dragged by its title bar with the pointer."""
    window(ic, 4, 6, 46, 38)
    ic.add('<path d="M9,22H40M9,27H34M9,32H38" stroke="#9aa0a8" stroke-width="1.3"/>')
    ic.add('<path d="M50,10L58,10M54,6V14M50,58H58" stroke="none"/>')
    arrow = "M30,6V30L35.5,25L39.5,33.5L43.5,31.5L39.5,23H47Z"
    ic.add('<g transform="translate(6,16)">')
    ic.shadow(arrow, 2, 1.8)
    ic.path(arrow, "#ffffff", INK, LW)
    ic.add("</g>")
    ic.add(f'<path d="M52,30H60M56,26V34M52,30L54,28M52,30L54,32" stroke="none"/>')


def compositor(ic):
    """Compositor: as in KDE 3, a green graphics card standing in front of a monitor showing a colour palette."""
    import colorsys
    # monitor, set back to the right
    ic.shadow(rrect(19, 4, 42, 38, 3) + "M34,42H50L53,54H31Z", 3, 2.6)
    ic.path("M29,52Q29,50 31,50H53Q55,50 55,52V56H29Z", ic.lg([(0, "#e8e4d8"), (1, "#8a877c")]), INK, LW)
    ic.path("M35,41H49L51,50.5H33Z", ic.lg([(0, "#d9d5c8"), (1, "#8a877c")]), INK, LW)
    ic.path(rrect(19, 4, 42, 38, 3), ic.lg([(0, "#f4f4f4"), (1, "#a8adb4")], 0, 0, .3, 1), INK, LW)
    ic.path(rrect(26, 8, 31, 26, 1.4), "#101418", INK, 1)
    hues = (.5, .33, .16, .08, 0)
    for r, (lt, sat) in enumerate(((.32, .9), (.45, .95), (.55, 1), (.8, .7))):
        for c, h in enumerate(hues):
            R, G, B = colorsys.hls_to_rgb(h, lt, sat)
            ic.add(f'<rect x="{27.6 + c * 5.8:.1f}" y="{9.6 + r * 6:.1f}" width="4.6" height="4.8" fill="#{int(R * 255):02x}{int(G * 255):02x}{int(B * 255):02x}"/>')
    ic.add('<path d="M27,9H56V18Q41,21 27,18Z" fill="#fff" fill-opacity=".14"/>')
    ic.path(rrect(51, 36.4, 4.4, 2.4, .6), "#3ae03a", INK, .5)
    # graphics card, upright in front on the left, gold contacts down its left edge
    card = "M6,3H31V50H6Z"
    ic.shadow(card, 2.8, 2.4)
    ic.path(card, ic.lg([(0, "#8aea7a"), (.55, "#3aa83a"), (1, "#1a6a24")], 0, 0, 1, 1), INK, LW)
    ic.path("M2,8H6V30H2Z", "#ffffff", INK, .9)
    for k in range(6):
        ic.add(f'<rect x="2.6" y="{9.2 + k * 3.4:.1f}" width="3.2" height="2" fill="#e8c43a" stroke="#7a5a04" stroke-width=".3"/>')
    traces = ("M9,12H14L17,15V22M9,26H13L16,29V38M20,18V26L24,30M12,42H18L21,45M24,36V44M27,14V34M9,46H28"
              "M14,33H19M22,8V14H26")
    ic.add(f'<path d="{traces}" fill="none" stroke="#e0f8a0" stroke-opacity=".85" stroke-width=".9"/>')
    for x, y, w in ((16, 8, 9), (11, 26, 7), (11, 38, 6), (21, 38, 6)):
        ic.path(f"M{x},{y}H{x + w}V{y + w}H{x}Z", ic.lg([(0, "#5c6168"), (1, "#0a0c10")]), INK, .7)
    ic.path(rrect(10, 5.4, 5, 1.8, .4), "#e0281a", INK, .3)
    for k, col in enumerate(("#e0281a", "#2a5ae0", "#2a5ae0")):
        ic.path(rrect(27, 22 + k * 4.4, 1.8, 3.2, .4), col, INK, .3)


def autostart(ic):
    """Autostart: the program gear with a green play badge: starts on its own at login."""
    _gear(ic, 26, 28, 21)
    _badge(ic, 48, 48, 11, "green", "M45,42.5L53,48L45,53.5Z")


def background_services(ic):
    """Background Services: two meshing gears turning out of sight, one large, one small."""
    _gear(ic, 24, 26, 19, colours=("#ffffff", "#b4b9c0", "#5c6168"))
    _gear(ic, 45, 45, 13, n=7, colours=("#ffe2b0", "#e89a3a", "#8a4c10"))


def desktop_session(ic):
    """Desktop Session: a monitor showing the log-out door, for what happens at login and logout."""
    def scr(ic):
        ic.add(f'<path d="M{SX + 18},{SY + 5}H{SX + 9}V{SY + 25}H{SX + 18}" fill="none" stroke="#fff" stroke-width="2.4" stroke-linejoin="round"/>')
        ic.add(f'<path d="M{SX + 14},{SY + 15}H{SX + 32}M{SX + 26},{SY + 9}L{SX + 32},{SY + 15}L{SX + 26},{SY + 21}" fill="none" stroke="#ffd890" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>')
    monitor(ic, scr, glass=("#ffb05a", "#c8601a", "#5a2404"))


def multimedia(ic):
    """Multimedia (category): a film clapperboard with a music note."""
    ic.shadow("M4,24H44V54H4Z", 2.4, 2)
    ic.path("M4,24H44V54H4Z", ic.lg([(0, "#3c4148"), (1, "#0a0c10")]), INK, LW)
    ic.add('<path d="M8,32H40M8,38H34M8,44H38" stroke="#fff" stroke-opacity=".5" stroke-width="1.2"/>')
    ic.add('<g transform="rotate(-14 4 24)">')
    ic.path("M4,16H44V24H4Z", "#ffffff", INK, LW)
    for k in range(4):
        ic.path(f"M{8 + k * 10},16H{13 + k * 10}L{9 + k * 10},24H{4 + k * 10}Z", "#14171c", None)
    ic.add("</g>")
    note = "M44,14L60,10V40A5,4 0 1 1 56,36V20L48,22V46A5,4 0 1 1 44,42Z"
    ic.shadow(note, 2, 1.8)
    ic.path(note, ic.lg([(0, "#9fd4ff"), (1, "#1a5c9e")]), INK, LW)


def apps_windows(ic):
    """Apps & Windows (category): a window full of app tiles."""
    window(ic, 4, 6, 56, 50)
    cols = ("#3a8ee0", "#4fae5a", "#e8a010", "#d8302a", "#8a5ae8", "#1aa0a8")
    for r in range(2):
        for c in range(3):
            x, y = 10 + c * 16, 18 + r * 17
            ic.path(rrect(x, y, 12, 12, 2.5), ic.lg([(0, "#ffffff"), (.35, cols[r * 3 + c]), (1, cols[r * 3 + c])], 0, 0, 1, 1), INK, .9)


def graphics_category(ic):
    """Graphics (category): an artist's palette with paint and a brush."""
    pal = "M30,8C48,8 60,18 60,32C60,44 50,46 44,44C40,43 38,46 40,50C42,55 36,58 30,58C14,58 4,46 4,32C4,18 14,8 30,8Z"
    ic.shadow(pal, 2.6, 2.2)
    ic.path(pal, ic.lg([(0, "#f4d8a8"), (1, "#b07a3a")], 0, 0, 1, 1), INK, LW)
    for (x, y), col in (((18, 20), "#d8302a"), ((30, 16), "#e8c43a"), ((43, 21), "#4fae5a"), ((14, 34), "#3a8ee0"), ((20, 46), "#8a5ae8")):
        ic.path(circle(x, y, 4.4), ic.rg([(0, "#ffffff"), (.4, col), (1, col)], .35, .3, .8), INK, .8)
    ic.path(circle(31, 46, 3.4), "#ffffff", INK, 1)
    ic.add('<g transform="rotate(40 44 36)">')
    ic.path("M41,10H47V42H41Z", ic.lg([(0, "#e8b878"), (1, "#8a5a2a")], 0, 0, 1, 0), INK, 1)
    ic.path("M40.6,42H47.4V47H40.6Z", ic.lg([(0, "#ffffff"), (1, "#8a9098")], 0, 0, 1, 0), INK, 1)
    ic.path("M40.8,47Q44,58 44,60Q44,58 47.2,47Z", "#2a6ac8", INK, 1)
    ic.add("</g>")


def basic_info(ic):
    """Basic Information (category): the classic blue "i" sphere."""
    ic.shadow(circle(32, 32, 26), 2.6, 2.2)
    ic.path(circle(32, 32, 26), ic.rg([(0, "#8ab8f0"), (.45, "#2a5ab0"), (1, "#081c50")], .35, .28, .85), INK, LW)
    ic.add('<path d="M14,24C16,12 30,6 42,11C34,9 22,12 14,24Z" fill="#fff" fill-opacity=".5"/>')
    ic.path(circle(32, 18, 4.4), "#ffffff", None)
    ic.path("M25.5,26H35.5V43H39V48H25V43H28.5V31H25.5Z", "#ffffff", None)


def lost_found(ic):
    """Lost And Found (category): an open cardboard box with a question mark in it."""
    from filetypes import box
    box(ic, 8, 22, 16, 18)
    q = "M30,14Q30,6 38,6Q46,6 46,13Q46,18 41,20Q38,21.5 38,25V27"
    ic.add(f'<path d="{q}" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>')
    ic.add(f'<path d="{q}" fill="none" stroke="#2a6ac8" stroke-width="4.4" stroke-linecap="round" stroke-linejoin="round"/>')
    ic.path(circle(38, 34, 3), "#2a6ac8", INK, 1.2)


def about_system(ic):
    """About this System: the classic computer with a blue "i" badge."""
    from gen import computer
    c = computer()
    ic.defs += c.defs
    ic.add('<g transform="translate(0,2) scale(.88)">' + "".join(c.body) + "</g>")
    _badge(ic, 49, 49, 11, "blue", "M49,46V54M49,42.6V42.8")


def wayland_kcm(ic):
    """Wayland: three layers stacked in perspective, the way the compositor stacks surfaces."""
    for k, col in enumerate((("#9fd4ff", "#1a5c9e"), ("#b4f0a0", "#2f8a2e"), ("#ffd0a0", "#c8601a"))):
        y = 38 - k * 11
        d = f"M32,{y - 12}L58,{y}L32,{y + 12}L6,{y}Z"
        ic.shadow(d, 1.8, 1.6)
        ic.path(d, ic.lg([(0, col[0]), (1, col[1])], 0, 0, 1, 1), INK, LW, ' fill-opacity=".92"')


def xorg_kcm(ic):
    """Legacy X11 App Support: an old grey window showing a big X."""
    window(ic, 4, 6, 56, 50, title=("#c3c7cd", "#5c6168"), body=("#f4f5f7", "#c9ccd1"))
    ic.add(f'<path d="M18,20L46,48M46,20L18,48" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>')
    ic.add('<path d="M18,20L46,48" stroke="#5c6168" stroke-width="5.6" stroke-linecap="round"/><path d="M46,20L18,48" stroke="#9aa0a8" stroke-width="3" stroke-linecap="round"/>')


def _control_centre(ic):
    """KDE 2/3 Control Centre (monitor, colour chart and circuit board) - used for preferences-desktop and the
    System Settings app, as KDE Classic did."""
    from odds import control_centre
    control_centre(ic)


def _system_settings_app(ic):
    """System Settings (the app): the refined gear with the flathead screwdriver, as on configure.
    It already fills the canvas, so it reads at full size on the taskbar."""
    from uitrace import configure
    configure(ic)


def system_settings(ic):
    """System Settings: a spanner and screwdriver crossed in front of a gear."""
    _gear(ic, 32, 30, 22, colours=("#ffffff", "#b4b9c0", "#5c6168"))
    ic.add('<g transform="rotate(45 32 34)">')
    ic.path("M29.5,10H34.5V40H29.5Z", ic.lg([(0, "#ffffff"), (.5, "#9aa0a8"), (1, "#4c5158")], 0, 0, 1, 0), INK, 1.1)
    ic.path("M27,40H37V58Q37,61 34,61H30Q27,61 27,58Z", ic.lg([(0, "#ff9a7a"), (1, "#a8180a")], 0, 0, 1, 0), INK, 1.1)
    ic.add("</g>")
    ic.add('<g transform="rotate(-45 32 34)">')
    sp = "M29.5,16H34.5V54H29.5Z M26,6Q26,14 32,14Q38,14 38,6L35,6V10H29V6Z"
    ic.path(sp, ic.lg([(0, "#ffffff"), (.5, "#b4b9c0"), (1, "#5c6168")], 0, 0, 1, 0), INK, 1.1)
    ic.add("</g>")


SYSTEM_SOUNDS_BADGE = "note"     # "" for the plain cabinet


def _cone(ic, cx, cy, r):
    ic.path(circle(cx, cy, r), ic.lg([(0, "#e4e6e9"), (1, "#6c727a")], 0, 0, 1, 1), INK, 1.1)
    ic.path(circle(cx, cy, r * .78), ic.rg([(0, "#8a9098"), (.7, "#3c4148"), (1, "#1a1d22")], .5, .5, .6), INK, .8)
    ic.path(circle(cx, cy, r * .3), ic.rg([(0, "#ffffff"), (1, "#8a9098")], .4, .35, .8), INK, .7)


def system_sounds(ic, badge=None):
    """System Sounds: a hi-fi speaker cabinet seen from the front corner, a tweeter above the woofer."""
    badge = SYSTEM_SOUNDS_BADGE if badge is None else badge
    front = "M10,10H38V60H10Z"
    side = "M38,10L48,4V54L38,60Z"
    top = "M10,10L20,4H48L38,10Z"
    ic.shadow(front + side + top, 2.6, 2.2)
    ic.path(side, ic.lg([(0, "#5c6168"), (1, "#1a1d22")], 0, 0, 1, 0), INK, LW)
    ic.path(top, ic.lg([(0, "#a8adb4"), (1, "#6c727a")]), INK, LW)
    ic.path(front, ic.lg([(0, "#6c727a"), (.5, "#3c4148"), (1, "#202328")], 0, 0, 1, 1), INK, LW)
    ic.add('<path d="M12,12.5H36" stroke="#fff" stroke-opacity=".35" stroke-width="1"/>')
    _cone(ic, 24, 21, 6.5)
    _cone(ic, 24, 43, 11.5)
    ic.path(circle(14, 56.5, 1), "#3ae03a", None)
    for k, r in enumerate((7, 12)):
        ic.add(f'<path d="M{51 + k * 2},{32 - r}Q{55 + r},32 {51 + k * 2},{32 + r}" fill="none" stroke="{INK}" stroke-width="3.6" stroke-linecap="round"/>')
        ic.add(f'<path d="M{51 + k * 2},{32 - r}Q{55 + r},32 {51 + k * 2},{32 + r}" fill="none" stroke="#3ab8d8" stroke-width="2" stroke-linecap="round"/>')
    if badge == "note":
        note = "M44,40L60,36V52A3.6,3 0 1 1 57,49V41.6L47,44V56A3.6,3 0 1 1 44,53Z"
        ic.shadow(note, 1.6, 1.4)
        ic.path(note, ic.lg([(0, "#ffd890"), (.5, "#e8a010"), (1, "#7a4404")], 0, 0, 1, 1), INK, 1.1)


def _ic(fn):
    def f():
        ic = Icon()
        fn(ic)
        return ic
    return f


SETTINGS = {
    "preferences-desktop-theme-global": _ic(global_theme), "preferences-desktop-plasma-theme": _ic(plasma_style),
    "preferences-desktop-theme-applications": _ic(app_style), "preferences-desktop-theme-windowdecorations": _ic(window_decorations),
    "preferences-desktop-color": _ic(colours), "preferences-desktop-display-color": _ic(gamma), "preferences-desktop-icons": _ic(icons_kcm),
    "preferences-desktop-emoticons": _ic(emoji_selector),
    "preferences-desktop-cursors": _ic(cursors), "preferences-desktop-wallpaper": _ic(wallpaper), "preferences-system-splash": _ic(splash),
    "preferences-desktop-display": _ic(boot_splash), "preferences-system-login": _ic(login_screen), "preferences-desktop-effects": _ic(effects),
    # input devices
    "preferences-desktop-keyboard": _ic(keyboard), "preferences-desktop-keyboard-shortcut": _ic(shortcuts),
    "preferences-desktop-mouse": _ic(mouse_kcm), "preferences-desktop-touchpad": _ic(touchpad),
    "preferences-desktop-tablet": _ic(tablet), "preferences-desktop-touchscreen": _ic(touchscreen),
    "preferences-desktop-gaming": _ic(gamepad), "preferences-desktop-gestures-screenedges": _ic(screen_edges),
    "preferences-desktop-gestures-touch": _ic(touch_gestures), "input-keyboard-virtual": _ic(virtual_keyboard),
    # hardware
    "preferences-desktop-display-randr": _ic(displays), "audio-card": _ic(audio_card),
    "preferences-desktop-sound": _ic(sound), "preferences-system-bluetooth": _ic(bluetooth_kcm), "preferences-devices-printer": _ic(printers),
    "preferences-system-power-management": _ic(power_management), "battery": _ic(energy_info), "preferences-system-disks": _ic(disks_cameras),
    "preferences-smart-status": _ic(smart_status), "preferences-desktop-thunderbolt": _ic(thunderbolt),
    "drive-removable-media-usb-pendrive": _ic(usb_devices), "drive-multidisk": _ic(block_devices), "memory": _ic(memory),
    "preferences-devices-cpu": _ic(cpu_info), "cpu": _ic(interrupts), "network-card": _ic(network_card),
    "preferences-desktop-peripherals": _ic(peripherals), "redshift-status-on": _ic(night_light),
    # personal, region, network, security, search
    "preferences-system-users": _ic(users), "preferences-desktop-user": _ic(personalisation), "preferences-desktop-locale": _ic(region),
    "preferences-system-time": _ic(date_time), "preferences-desktop-notification-bell": _ic(notifications),
    "preferences-desktop-accessibility": _ic(accessibility), "preferences-system-network": _ic(networking),
    "preferences-system-network-sharing": _ic(network_sharing), "preferences-security-firewall": _ic(firewall),
    "preferences-security": _ic(firmware_security), "preferences-desktop-search": _ic(search_category),
    "preferences-desktop-baloo": _ic(file_search), "plasma-search": _ic(plasma_search), "krunner": _ic(krunner),
    "preferences-desktop-default-applications": _ic(default_apps), "tools-check-spelling": _ic(spelling),
    "preferences-desktop-feedback": _ic(user_feedback), "system-software-update": _ic(software_update),
    # "system-file-manager" (Locations) is drawn by dolphin.py as the KDE Classic filing cabinet;
    # the folder stack below is kept as locations() for a future use.
    # workspace, session, categories, info
    "preferences-desktop-activities": _ic(activities), "preferences-desktop-virtual": _ic(virtual_desktops),
    "preferences-system-tabbox": _ic(task_switcher), "preferences-system-windows-actions": _ic(window_behaviour),
    "preferences-desktop": _ic(_control_centre), "system-run": _ic(autostart), "preferences-system-session-services": _ic(background_services),
    "preferences-desktop-multimedia": _ic(multimedia), "applications-all": _ic(apps_windows),
    "applications-graphics": _ic(graphics_category), "dialog-information": _ic(basic_info), "hwinfo": _ic(lost_found),
    "ktip": _ic(about_system), "wayland": _ic(wayland_kcm), "xorg": _ic(xorg_kcm), "preferences-system": _ic(_control_centre),
    "preferences-desktop-sound-notification": _ic(system_sounds),
}
SETTINGS_ALIASES = {
    "preferences-system-windows": "preferences-desktop-theme-windowdecorations", "preferences-desktop-theme": "preferences-desktop-theme-global",
    "preferences-desktop-color-scheme": "preferences-desktop-color", "preferences-desktop-colors": "preferences-desktop-color",
    "preferences-desktop-splash": "preferences-system-splash",
    "preferences-system-plymouth": "preferences-desktop-display",
    "preferences-desktop-keyboard-shortcuts": "preferences-desktop-keyboard-shortcut", "input-gaming": "preferences-desktop-gaming",
    "preferences-desktop-gestures": "preferences-desktop-gestures-touch",
    "preferences-desktop-display-nightcolor": "redshift-status-on", "preferences-desktop-sound-system": "preferences-desktop-sound",
    "preferences-system-bluetooth-activated": "preferences-system-bluetooth", "preferences-desktop-printer": "preferences-devices-printer",
    "printer-settings": "preferences-devices-printer", "preferences-desktop-compositing": "preferences-desktop", "systemsettings": "preferences-desktop", "org.kde.systemsettings": "preferences-desktop",
    "kinfocenter": "ktip", "org.kde.kinfocenter": "ktip", 
    "preferences-system-windows-behavior": "preferences-system-windows-actions",
    "preferences-system-windows-effect": "preferences-desktop-effects", "applications-multimedia": "preferences-desktop-multimedia",
    "emblem-music-symbolic": "preferences-desktop-sound-notification", "preferences-system-sounds": "preferences-desktop-sound-notification", "preferences-desktop-notification": "preferences-desktop-notification-bell",
    "preferences-system-firewall": "preferences-security-firewall", "preferences-desktop-user-password": "preferences-system-users",
    "system-users": "preferences-system-users", "preferences-system-date-time": "preferences-system-time", "clock": "preferences-system-time",
    "preferences-desktop-locale-symbolic": "preferences-desktop-locale", "preferences-system-network-proxy": "preferences-system-network", "preferences-system-power": "preferences-system-power-management", "preferences-desktop-screen-edges": "preferences-desktop-gestures-screenedges", "preferences-desktop-theme-windowdecoration": "preferences-desktop-theme-windowdecorations",
}


def write(out):
    import os
    d = f"{out}/scalable/apps"
    os.makedirs(d, exist_ok=True)
    for name, fn in SETTINGS.items():
        open(f"{d}/{name}.svg", "w").write(fn().svg(64))
    for a, t in SETTINGS_ALIASES.items():
        if not os.path.exists(f"{d}/{a}.svg"):
            os.symlink(f"{t}.svg", f"{d}/{a}.svg")
    return len(SETTINGS)
