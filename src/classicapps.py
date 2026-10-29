"""KDE Classic Vector: current KDE apps redrawn from their KDE Classic (KDE 3) originals, or a KDE 3
predecessor's icon (docs/kde-apps-redraw-list.md lists the sources). Imported by apps2, which adds the names.
"""
import math
from gen import Icon, INK, LW, circle, rrect
from uitrace import _pencil
WOOD = ("#f0b070", "#b8662a", "#5a2806")
CHALK = "#f4f4ec"


def okteta(ic, hs=.76, depth=1.3):
    """Okteta (after KDE 3's KHexEdit): a clipboard of ruled paper with a chrome H tilted to match the
    orange pencil beside it."""
    sheet = "M3,9H51V61H3Z"
    ic.shadow(sheet, 2.4, 2)
    ic.path(sheet, ic.lg([(0, "#ffffff"), (.6, "#fffdf0"), (1, "#ece4c4")], 0, 0, 1, 1), INK, LW)
    for k in range(7):
        ic.add(f'<path d="M7,{19 + k * 6}H47" stroke="#9aa2ec" stroke-width="1.2"/>')
    # the clip
    ic.path("M18,10V6Q18,3 21,3H33Q36,3 36,6V10Q36,13 33,13H21Q18,13 18,10Z",
            ic.lg([(0, "#f0f0ff"), (.5, "#b8bce8"), (1, "#5a5e98")]), INK, 1.3)
    ic.add('<path d="M23,7H31" stroke="#5a5e98" stroke-width="1.6" stroke-linecap="round"/>')
    # chrome block H, leaning at the pencil's angle, with a shallow edge for depth
    H = "M0,0H6V8H14V0H20V22H14V13H6V22H0Z"
    ic.add(f'<g transform="translate(19,32) rotate(-43) scale({hs}) translate(-10,-11)">')
    ic.add(f'<path d="{H}" fill="#3c4148" stroke="{INK}" stroke-width="1.1" stroke-linejoin="round" '
           f'transform="translate({depth},{depth})"/>')
    ic.path(H, ic.lg([(0, "#ffffff"), (.45, "#c3c7cd"), (.55, "#7b818a"), (1, "#e4e6e9")], 0, 0, .3, 1), INK, 1.3 / hs)
    ic.add("</g>")
    _pencil(ic, "translate(59,21) rotate(47) scale(.85) translate(-6,0)")


def _board(ic):
    """KMathTool's square chalkboard: bright green slate in a wooden frame."""
    f = "M5,5H59V59H5Z"
    ic.shadow(f, 2.6, 2.2)
    ic.path(f, ic.lg([(0, WOOD[0]), (.5, WOOD[1]), (1, WOOD[2])], 0, 0, 1, 1), INK, LW)
    ic.path("M10,10H54V54H10Z", ic.lg([(0, "#5ad05a"), (.5, "#2aa83a"), (1, "#127a22")], 0, 0, 1, 1), INK, 1.1)
    ic.add('<path d="M11,11H53" stroke="#ffffff" stroke-opacity=".25" stroke-width="1.2"/>')


def _chalk(ic, d, w=2.3):
    ic.add(f'<path d="{d}" fill="none" stroke="{CHALK}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" stroke-opacity=".95"/>')


# x² + y, chalked across the top of the board
ALGEBRA = ("M14,16L21,26M21,16L14,26"                       # x
           "M23,13.4Q25,11 27,12.6Q28,14.4 23.4,18H28"      # ²
           "M31,21H38M34.5,17.5V24.5"                        # +
           "M41,16L45,23M49,16L42,30")                       # y


def _wrench(ic, s=.92):
    """KMathTool's spanner: handle to the lower left, open jaw to the upper right."""
    ic.add(f'<g transform="translate(35,41) rotate(45) scale({s}) translate(-36,-38)">')
    d = ("M32.8,11.06V20H39.2V11.06A9.5,9.5 0 0 1 40,28.62V56Q36,61 32,56V28.62A9.5,9.5 0 0 1 32.8,11.06Z")
    ic.shadow(d, 2, 1.7)
    ic.path(d, ic.lg([(0, "#ffffff"), (.45, "#c3c7cd"), (1, "#4c5158")], 0, 0, 1, 0), INK, 1.3 / s)
    ic.add('<path d="M34.6,31V54" stroke="#ffffff" stroke-opacity=".6" stroke-width="1.2"/>')
    ic.add("</g>")


def kalgebra(ic):
    """KAlgebra: KMathTool's chalkboard and spanner, with x² + y chalked on it in place of 2 + 3."""
    _board(ic)
    ic.add('<g transform="translate(1,0) scale(.86)">'); _chalk(ic, ALGEBRA, 2.6); ic.add("</g>")
    _wrench(ic)


# ------------------------------------------------------------------ KDE Edu (2026-10-30)
def _ball(ic, x, y, r, stops):
    ic.shadow(circle(x, y, r), 2.2, 1.8)
    ic.path(circle(x, y, r), ic.rg(stops, .36, .3, .85), INK, LW)


def _bond(ic, x0, y0, x1, y1):
    ic.add(f'<path d="M{x0},{y0}L{x1},{y1}" stroke="{INK}" stroke-width="7.4" stroke-linecap="round"/>'
           f'<path d="M{x0},{y0}L{x1},{y1}" stroke="#7b818a" stroke-width="4.6" stroke-linecap="round"/>'
           f'<path d="M{x0},{y0}L{x1},{y1}" stroke="#d8dce0" stroke-width="1.4" stroke-linecap="round" transform="translate(-.8,-.8)"/>')


def kalzium(ic):
    """Kalzium: a molecule - black, blue and red atoms joined by grey bonds."""
    B, K, R = (42, 18), (18, 37), (43, 45)
    _bond(ic, *K, *B); _bond(ic, *B, *R); _bond(ic, *K, *R)
    _ball(ic, *B, 11, [(0, "#c8d8ff"), (.35, "#2a4ae0"), (1, "#060a50")])
    _ball(ic, *R, 11, [(0, "#ffc8c0"), (.35, "#d8201a"), (1, "#500604")])
    _ball(ic, *K, 12, [(0, "#c8ccd0"), (.3, "#3c4148"), (1, "#020304")])


def khangman(ic):
    """KHangMan: KDE 3's rope noose - the rope coming down from the top left into a coiled knot and a loop."""
    rope = "M6,3L22,20M30,30Q20,42 26,54Q35,63 48,57Q59,49 53,36Q46,27 32,30"
    for w, c in ((6.6, INK), (4.4, "#b07a28")):
        ic.add(f'<path d="{rope}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')
    ic.add(f'<path d="{rope}" fill="none" stroke="#f0c878" stroke-width="1.2" stroke-linecap="round" stroke-dasharray="3 3" transform="translate(-.7,-.7)"/>')
    # the coiled knot
    ic.add('<g transform="rotate(-42 27 25)">')
    for e in ("M24.5,16L21,8", "M29.5,16L32,7.5"):
        for w, c in ((5.4, INK), (3.4, "#b07a28")):
            ic.add(f'<path d="{e}" stroke="{c}" stroke-width="{w}" stroke-linecap="round"/>')
    ic.shadow(rrect(21.5, 14, 11, 22, 4), 2, 1.7)
    ic.path(rrect(21.5, 14, 11, 22, 4), ic.lg([(0, "#f0c878"), (.5, "#b07a28"), (1, "#5a3406")], 0, 0, 1, 0), INK, 1.4)
    for k in range(5):
        y = 16.5 + k * 4.2
        ic.add(f'<path d="M22,{y}Q27,{y + 2.2} 32,{y}" fill="none" stroke="{INK}" stroke-width="1"/>')
    ic.add("</g>")


def _digit(ic, d, x, y, col):
    p = {"2": "M{0},{4}Q{0},{0} {7},{0}Q{14},{0} {14},{5}Q{14},{9} {0},{18}H{14}",
         "7": "M{0},{0}H{14}L{5},{18}",
         "5": "M{13},{0}H{2}L{1},{8}Q{12},{5} {13},{12}Q{13},{18} {6},{18}Q{1},{18} {0},{15}",
         "3": "M{1},{2}Q{7},{-1} {12},{3}Q{14},{8} {6},{9}Q{15},{10} {13},{15}Q{8},{20} {0},{16}"}[d]
    import re
    # numbers in the template are offsets from (x, y): they alternate x, y, except that H takes only an x
    vals = [int(v) for v in re.findall(r"\{(-?\d+)\}", p)]
    out, k = p, 0
    for v in vals:
        out = out.replace("{%d}" % v, "\x00", 1)
    parts = out.split("\x00"); s = parts[0]
    # rebuild alternating x/y, except after H which takes one x and after V one y
    xs = True
    toks = []
    for i, v in enumerate(vals):
        pre = parts[i]
        if pre.endswith("H"): xs = True
        val = x + v if xs else y + v
        toks.append(pre + ("%g" % val)); xs = not xs
        if pre.endswith("H"): xs = True
    s = "".join(toks) + parts[-1]
    for w, c in ((7, INK), (4.6, col)):
        ic.add(f'<path d="{s}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')


def _bar(ic, x0, x1, y, col):
    for w, c in ((6, INK), (3.6, col)):
        ic.add(f'<path d="M{x0},{y}H{x1}" stroke="{c}" stroke-width="{w}" stroke-linecap="round"/>')


def kbruch(ic):
    """KBruch: two fractions being added, 2/7 + 5/3, each figure in its own bright colour."""
    _digit(ic, "2", 6, 7, "#e8201a"); _bar(ic, 5, 21, 32, "#7a3ae0"); _digit(ic, "7", 6, 39, "#2ad02a")
    for w, c in ((6, INK), (3.6, "#a040c8")):
        ic.add(f'<path d="M26,32H35M30.5,27.5V36.5" stroke="{c}" stroke-width="{w}" stroke-linecap="round"/>')
    _digit(ic, "5", 43, 7, "#f020e0"); _bar(ic, 41, 58, 32, "#20c8f0"); _digit(ic, "3", 43, 39, "#f09010")


def kmplot(ic):
    """KmPlot: a yellow plotting sheet with ticked axes and a red curve."""
    sq = "M6,6H58V58H6Z"
    ic.shadow(sq, 2.6, 2.2)
    ic.path(sq, ic.lg([(0, "#ffffa0"), (.5, "#fff020"), (1, "#e0c000")], 0, 0, 1, 1), INK, LW)
    ticks = "".join(f"M{x},30.5V33.5M30.5,{x}H33.5" for x in range(8, 58, 6) if x != 32)
    ic.add(f'<path d="M7,32H57M32,7V57{ticks}" stroke="#3c4148" stroke-width="1.4"/>')
    def f(x):           # a sine with broad, rounded crests, like the original's
        s = math.sin(2 * math.pi * (x - 32) / 32)
        return 32 + 22 * math.copysign(abs(s) ** .55, s)
    pts = [(x / 4, f(x / 4)) for x in range(40, 214)]
    curve = "M" + "L".join(f"{x:.2f},{y:.2f}" for x, y in pts)
    ic.add(f'<path d="{curve}" fill="none" stroke="#e0201a" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>')


def kig(ic):
    """Kig: a sheet with a circle above a right-angled triangle, the red-to-yellow set square and the orange
    pencil."""
    ic.add('<g transform="rotate(-26 30 36)">')
    sheet = "M12,14H48V60H12Z"
    ic.shadow(sheet, 2.4, 2)
    ic.path(sheet, ic.lg([(0, "#fffbe8"), (.45, "#f6e2b4"), (1, "#c8965a")], 0, 0, 1, 1), INK, LW)
    for shape in (circle(30, 32.5, 11), "M20,55H42V41Z"):      # shaded like the paper, a little lighter
        ic.path(shape, ic.lg([(0, "#ffffff"), (.5, "#fbedd0"), (1, "#dcb47c")], 0, 0, 1, 1), "#6c6458", 1.3)
    ic.add("</g>")
    ic.add('<g transform="translate(0,6)">')
    sq = "M16,6H60V26Z M37.6,9.6H55.2V17.6Z"
    ic.add("<g>" + "".join(f'<path d="{sq}" fill="#000" fill-opacity=".16" fill-rule="evenodd" '
                           f'transform="translate({.73 * (k + 1):.2f},{.6 * (k + 1):.2f})"/>' for k in range(3)) + "</g>")
    ic.path(sq, ic.lg([(0, "#c00a00"), (.2, "#ff1a00"), (.55, "#ff7a00"), (1, "#fff000")], 0, 0, 1, 0), INK, 1.4, ' fill-rule="evenodd"')
    ic.add('<path d="M20.5,7.4H58.6V23" fill="none" stroke="#ffffff" stroke-opacity=".6" stroke-width="1.1"/>')
    ic.add('<path d="' + "".join(f"M{16 + k * 3.67:.1f},{6 + k * 1.67:.1f}l.8,-1.8" for k in range(1, 12)) + '" stroke="#5a1004" stroke-width=".8"/>')
    ic.add("</g>")
    _pencil(ic, "translate(15.5,55.4) rotate(210) scale(.45) translate(-6,0)")


CLASSIC_APPS = {"okteta": okteta, "kalgebra": kalgebra, "kalzium": kalzium, "khangman": khangman, "kbruch": kbruch,
                "kmplot": kmplot, "kig": kig}
CLASSIC_ALIASES = {"org.kde." + a: "apps/" + a for a in CLASSIC_APPS}
CLASSIC_ALIASES.update({
    # Kamoso (webcam): KDE 3's camera is the theme's camera, as for camera-web
    "kamoso": "camera-photo", "org.kde.kamoso": "camera-photo"})
