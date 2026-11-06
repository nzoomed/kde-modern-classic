"""Perl clam (KDE 3 shellscript2.png), work in progress (2026-10-30): not built. Traced over the original and
redrawn; the shape lines up but it does not look right yet. Revisit. The theme keeps its script icon with the
blue "pl" label for Perl (application-x-perl, text-x-perl).
"""
import math
from gen import Icon, INK, LW, circle
from filetypes import page, e_label

GOLD = [(0, "#fff4b0"), (.45, "#e8b428"), (1, "#7a4c04")]


def _ribs(ic, cx, cy, r0, r1, a0, a1, n, w=.9):
    d = ""
    for k in range(n):
        a = math.radians(a0 + (a1 - a0) * (k + .5) / n)
        d += f"M{cx + r0 * math.cos(a):.2f},{cy + r0 * math.sin(a):.2f}L{cx + r1 * math.cos(a):.2f},{cy + r1 * math.sin(a):.2f}"
    ic.add(f'<path d="{d}" stroke="#7a4c04" stroke-width="{w}" stroke-linecap="round"/>')


def _valve(ic, cx, cy, rx, ry, a0, a1, n, lip, hub):
    """One half of the scallop: an elliptical fan from angle a0 to a1 with a scalloped rim of n lobes, closed
    by a gentle curve through `lip` (the edge that opens), ribs running from `hub` to each scallop."""
    P = lambda a, k=1.0: (cx + rx * k * math.cos(math.radians(a)), cy + ry * k * math.sin(math.radians(a)))
    angs = [a0 + (a1 - a0) * i / n for i in range(n + 1)]
    x, y = P(angs[0]); d = f"M{x:.2f},{y:.2f}"
    for i in range(n):
        mx, my = P((angs[i] + angs[i + 1]) / 2, 1.14)
        x, y = P(angs[i + 1]); d += f"Q{mx:.2f},{my:.2f} {x:.2f},{y:.2f}"
    x0, y0 = P(angs[0]); d += f"Q{lip[0]},{lip[1]} {x0:.2f},{y0:.2f}Z"
    ic.shadow(d, 2.4, 2)
    ic.path(d, ic.lg(GOLD, 0, 0, 1, 1), INK, LW)
    rib = ""
    for i in range(1, n):
        x, y = P(angs[i], .96); hx, hy = hub
        rib += f"M{hx + (x - hx) * .3:.2f},{hy + (y - hy) * .3:.2f}L{x:.2f},{y:.2f}"
    ic.add(f'<path d="{rib}" stroke="#7a4c04" stroke-width="1" stroke-linecap="round"/>')


def e_clam(ic):
    """KDE 3's open clam, traced from the original (shellscript2.png) and redrawn: the bowl seen from above with a
    big pearl filling its opening, and the lid standing open behind, hinged on the right."""
    from traceart import catmull
    rib = lambda hub, pts, k0=.25: "".join(f"M{hub[0] + (x - hub[0]) * k0:.2f},{hub[1] + (y - hub[1]) * k0:.2f}L{x:.2f},{y:.2f}" for x, y in pts)
    # lid
    lid = [(10.2, 15.8), (12.6, 13.6), (21, 13.4), (30, 13.8), (36.6, 15.6), (41.6, 19.6), (44, 24.2), (42.6, 26.2),
           (32, 26.4), (22, 26), (16.4, 22.6), (11.6, 19.8)]
    d = catmull(lid, .6)
    ic.shadow(d, 2.4, 2)
    ic.path(d, ic.lg(GOLD, 0, 0, .6, 1), INK, LW)
    ic.add(f'<path d="{rib((43, 25.6), [(12.4, 15.2), (17.4, 13.8), (23.4, 13.6), (29.4, 14.2), (34.6, 15.4), (39, 18), (16, 21.6)])}" '
           'stroke="#7a4c04" stroke-width="1" stroke-linecap="round"/>')
    # bowl
    bowl = [(10.5, 26.6), (4.6, 31.6), (2.4, 38.4), (4.2, 45.2), (10.2, 51.2), (18.6, 55.2), (29.2, 55.4), (37.4, 53.2),
            (41, 48.4), (45, 43.4), (47, 37.4), (47.4, 32.4), (45.2, 28.2), (40, 26.6), (26, 25.6)]
    d = catmull(bowl, .6)
    ic.shadow(d, 2.4, 2)
    ic.path(d, ic.lg(GOLD, 0, 0, .5, 1), INK, LW)
    ic.add(f'<path d="{rib((46, 31), [(4, 33.6), (3, 40.6), (6.4, 47.6), (12.6, 52.6), (20.4, 55.2), (28.6, 55.4), (36, 53.6), (41.4, 48.6)], .2)}" '
           'stroke="#7a4c04" stroke-width="1" stroke-linecap="round"/>')
    # the lining and the pearl in the bowl's opening
    ic.path("M13.4,34Q13.4,25.2 25,25.2Q36.6,25.2 36.6,34Q36.6,43 25,43Q13.4,43 13.4,34Z",
            ic.rg([(0, "#fff8f0"), (.6, "#f4d0c0"), (1, "#b87858")]), INK, 1)
    ic.shadow(circle(25, 33.4, 7.8), 1.4, 1.2)
    ic.path(circle(25, 33.4, 7.8), ic.rg([(0, "#ffffff"), (.45, "#fde4ec"), (.8, "#e8a8c0"), (1, "#a86888")], .36, .3, .8), INK, 1.1)
    ic.path(circle(22.4, 30.6, 2.2), "#ffffff", None, ' fill-opacity=".9"')


def perl(ic):
    page(ic); e_clam(ic); e_label("pl", "blue")(ic)


def perl_nolabel(ic):
    page(ic); e_clam(ic)
