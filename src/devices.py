"""KDE Classic Vector: devices (drawn from the KDE Classic originals, see STYLE.md)."""
import math
from gen import Icon, INK, LW, circle, rrect


def iso(cx, cy, w, h, ang=-30):
    """Transform string: rotate a flat w x h object about its centre (isometric-ish lean)."""
    return f"rotate({ang} {cx} {cy})"


# ------------------------------------------------------------------ helpers for rotated frames
def frame(ox, oy, ang):
    """Map flat-frame points to screen: rotate by ang degrees (clockwise) and move the origin to (ox, oy)."""
    a = math.radians(ang)
    ca, sa = math.cos(a), math.sin(a)
    return lambda x, y: (ox + x * ca - y * sa, oy + x * sa + y * ca)


def poly(f, pts, close=True):
    s = "M" + "L".join(f"{x:.2f},{y:.2f}" for x, y in (f(*p) for p in pts))
    return s + ("Z" if close else "")


def rpoly(f, pts, r=2.5):
    """Closed polygon in a flat frame with rounded corners (quadratic corners)."""
    out, n = [], len(pts)
    for i in range(n):
        p0, p1, p2 = pts[i - 1], pts[i], pts[(i + 1) % n]
        def toward(a, b, d):
            dx, dy = b[0] - a[0], b[1] - a[1]
            L = math.hypot(dx, dy)
            k = min(d, L / 2) / L
            return (a[0] + dx * k, a[1] + dy * k)
        a, b = toward(p1, p0, r), toward(p1, p2, r)
        A, P, B = f(*a), f(*p1), f(*b)
        out.append((A, P, B))
    s = f"M{out[0][0][0]:.2f},{out[0][0][1]:.2f}"
    for i, (A, P, B) in enumerate(out):
        if i:
            s += f"L{A[0]:.2f},{A[1]:.2f}"
        s += f"Q{P[0]:.2f},{P[1]:.2f} {B[0]:.2f},{B[1]:.2f}"
    return s + "Z"


def extrude(top, dy):
    """Side faces under a convex screen-space outline: the outline repeated dy lower."""
    return top


def rounded(verts, ctrls, r=2.6):
    """Closed path through verts with every corner rounded. ctrls[i] is None for a straight edge from
    verts[i] to verts[i+1], or the control point of a quadratic edge (a curved edge)."""
    n = len(verts)
    def B(i, t):
        a, b, cc = verts[i], verts[(i + 1) % n], ctrls[i]
        if cc is None:
            return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
        u = 1 - t
        return (u * u * a[0] + 2 * u * t * cc[0] + t * t * b[0], u * u * a[1] + 2 * u * t * cc[1] + t * t * b[1])
    def span(i):
        a, b = verts[i], verts[(i + 1) % n]
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        k = min(r, L / 2.2) / L
        return k, 1 - k
    f = lambda p: f"{p[0]:.2f},{p[1]:.2f}"
    s = "M" + f(B(0, span(0)[0]))
    for i in range(n):
        t0, t1 = span(i)
        a, b, cc = verts[i], verts[(i + 1) % n], ctrls[i]
        if cc is None:
            s += "L" + f(B(i, t1))
        else:
            sub = tuple((1 - t0) * (1 - t1) * a[j] + ((1 - t0) * t1 + t0 * (1 - t1)) * cc[j] + t0 * t1 * b[j] for j in (0, 1))
            s += "Q" + f(sub) + " " + f(B(i, t1))
        j = (i + 1) % n
        s += "Q" + f(verts[j]) + " " + f(B(j, span(j)[0]))
    return s + "Z"


# ------------------------------------------------------------------ hard disk
def harddisk(ic=None):
    """Open hard disk, traced from the original: an oblong case turned 45 degrees, copper platter at the
    far end, black electronics bay at the near end, silver side visible along the lower left."""
    ic = ic or Icon()
    W, H, D = 36.5, 45, 4
    f = frame(36.5, 1.5, 45)
    g = lambda x, y: (f(x, y)[0], f(x, y)[1] + D)
    corners = [(0, 0), (W, 0), (W, H), (0, H)]
    top = rpoly(f, corners, 4)
    base = rpoly(g, corners, 4)
    ic.shadow(base, 3, 2.4)
    # sides: lower-left (silver) and lower-right (dark), drawn as the dropped outline
    ic.path(base, ic.lg([(0, "#ffffff"), (.45, "#a4aab2"), (1, "#3c4148")], 0, 0, 1, 0), INK, LW * 1.3)
    L, B, R = f(0, H), f(W, H), f(W, 0)
    ic.add(f'<path d="M{B[0]:.2f},{B[1]:.2f}V{B[1] + D:.2f}" stroke="{INK}" stroke-width="1"/>')
    # top face
    ic.path(top, ic.lg([(0, "#c3c7cd"), (.5, "#8a9098"), (1, "#5c6168")], 0, 0, 1, 1), INK, LW * 1.3)
    ic.add(f'<path d="{rpoly(f, [(2.2, 2.2), (W - 2.2, 2.2), (W - 2.2, H - 2.2), (2.2, H - 2.2)], 3)}" fill="none" stroke="#fff" stroke-opacity=".25" stroke-width="1"/>')
    # electronics bay (black) at the near end
    ic.path(rpoly(f, [(2.6, 22), (W - 2.6, 22), (W - 2.6, H - 2.6), (2.6, H - 2.6)], 2.5),
            ic.lg([(0, "#2a2d32"), (1, "#060708")]), INK, .8)
    # platter
    pc = f(W / 2, 18.2)
    ic.path(circle(round(pc[0], 2), round(pc[1], 2), 17.4),
            ic.rg([(0, "#fff4dc"), (.35, "#f0c48c"), (.75, "#c27a36"), (1, "#7a4416")], .55, .3, .8), INK, 1)
    for r in (13.5, 9.5):
        ic.add(f'<path d="{circle(round(pc[0], 2), round(pc[1], 2), r)}" fill="none" stroke="#8a4c1a" stroke-opacity=".35" stroke-width=".9"/>')
    ic.add(f'<path d="M{pc[0] - 4:.1f},{pc[1] - 12.5:.1f}Q{pc[0] + 8:.1f},{pc[1] - 12:.1f} {pc[0] + 12:.1f},{pc[1] - 4:.1f}" fill="none" stroke="#fff" stroke-opacity=".8" stroke-width="2" stroke-linecap="round"/>')
    ic.path(circle(round(pc[0], 2), round(pc[1], 2), 4.2), ic.lg([(0, "#3c4148"), (1, "#0a0c10")]), INK, .9)
    ic.path(circle(round(pc[0], 2), round(pc[1], 2), 1.6), "#9aa0a8", None)
    # head arm: pivot at the near-left, head over the platter
    piv = f(5.5, H - 7)
    arm = poly(f, [(3.2, H - 9), (W / 2 - 2.2, 22), (W / 2 + 1.2, 23.5), (7.8, H - 5)])
    ic.path(arm, ic.lg([(0, "#ffffff"), (1, "#9aa0a8")], 0, 0, 1, 1), INK, .9)
    ic.path(circle(round(piv[0], 2), round(piv[1], 2), 3.8), ic.rg([(0, "#ffffff"), (1, "#7b818a")]), INK, .9)
    return ic


# ------------------------------------------------------------------ optical discs
DCX, DCY, DR = 31.5, 30.5, 27.5


def disc(ic, cx=DCX, cy=DCY, r=DR, blue=False):
    """The original disc fills the canvas: silver face, rainbow sheen top right and bottom left, black hub ring."""
    ic.shadow(circle(cx, cy, r), 2.6, 2.4)
    face = [(0, "#ffffff"), (.55, "#dde2ee"), (1, "#a4acc4")] if blue else [(0, "#ffffff"), (.55, "#e4e6e9"), (1, "#b4b8be")]
    ic.path(circle(cx, cy, r), ic.rg(face, .3, .25, .85), INK, LW)
    if blue:   # the blue-violet sheen of a high-definition disc
        sheen = ic.lg([(0, "#8c7cff", 0), (.3, "#8c7cff", .75), (.55, "#5aa8ff", .85), (.8, "#b4d8ff", .5), (1, "#c8b4ff", 0)], 0, 0, 1, 1)
    else:
        sheen = ic.lg([(0, "#ffb4c8", 0), (.3, "#ffb4c8", .8), (.55, "#b8f4b0", .85), (.8, "#c8e8c0", .5), (1, "#b4d8ff", 0)], 0, 0, 1, 1)
    ic.add(f'<path d="M{cx},{cy}L{cx + r * .05:.1f},{cy - r:.1f}A{r},{r} 0 0 1 {cx + r:.1f},{cy + r * .05:.1f}Z" fill="{sheen}"/>')
    sheen2 = (ic.lg([(0, "#5aa8ff", 0), (.5, "#5aa8ff", .6), (.75, "#a890ff", .5), (1, "#8c7cff", 0)], 0, 0, 1, 1) if blue else
              ic.lg([(0, "#b8f4b0", 0), (.5, "#b8f4b0", .7), (.75, "#ffc8b4", .5), (1, "#ffb4c8", 0)], 0, 0, 1, 1))
    ic.add(f'<path d="M{cx},{cy}L{cx - r:.1f},{cy + r * .2:.1f}A{r},{r} 0 0 0 {cx - r * .2:.1f},{cy + r:.1f}Z" fill="{sheen2}"/>')
    ic.add(f'<path d="{circle(cx, cy, r * .66)}" fill="none" stroke="#fff" stroke-opacity=".7" stroke-width="1"/>')
    ic.path(circle(cx, cy, r * .34), ic.lg([(0, "#3c4148"), (1, "#060708")], 0, 0, 1, 1), INK, 1)
    ic.path(circle(cx, cy, r * .22), ic.rg([(0, "#ffffff"), (1, "#b4b8be")]), INK, .8)
    ic.path(circle(cx, cy, r * .07), "#5c6168", None)


def strokes(ic, d, fill_black="", w_in=2.1, w_out=4.1, transform="scale(1.3333)"):
    """Lettering traced from the originals as centre lines (in 48 px units): a thick black stroke under
    a thinner white one, so neighbouring letters share a black outline as they do in the original."""
    ic.add(f'<g transform="{transform}">' if transform else "<g>")
    ic.add(f'<path d="{fill_black}{d}" fill="none" stroke="#000" stroke-opacity=".3" stroke-width="{w_out}" stroke-linecap="round" stroke-linejoin="round" transform="translate(.8,.9)"/>')
    if fill_black:
        ic.add(f'<path d="{fill_black}" fill="{INK}"/>')
    ic.add(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w_out}" stroke-linecap="round" stroke-linejoin="round"/>')
    ic.add(f'<path d="{d}" fill="none" stroke="#ffffff" stroke-width="{w_in}" stroke-linecap="round" stroke-linejoin="round"/>')
    ic.add("</g>")


def cd():
    """CD with the original's lowercase "disc": blocky letters, narrow black counters."""
    ic = Icon()
    disc(ic)
    d = ("M11,35H6.6Q5,35 5,36.6V41.2Q5,42.8 6.6,42.8H11 M10.8,29.4V42.8 "          # d: bowl and stem
         "M15.2,35V42.8 "                                                         # i (no dot, as drawn)
         "M25.4,34.9H20.9Q19.5,34.9 19.5,36.3V37.1Q19.5,38.5 20.9,38.5H24.1Q25.5,38.5 25.5,39.9V41.4Q25.5,42.8 24.1,42.8H19.5 "  # s
         "M33.9,37.3V36.3Q33.9,34.9 32.5,34.9H29.7Q28.3,34.9 28.3,36.3V41.4Q28.3,42.8 29.7,42.8H32.5Q33.9,42.8 33.9,41.4V40.5")   # c
    black = "M5,35H11V42.8H5Z M28.3,34.9H33.9V42.8H28.3Z "
    strokes(ic, d, black, w_in=2.3, w_out=4.5)
    return ic


def dvd():
    """DVD with the original's italic lettering: the first D's top stroke runs on into the V and up into
    the second D, and each D's upright stops short of the top bar."""
    ic = Icon()
    disc(ic)
    d = ("M6,33.9H18.2Q19.6,33.9 20.1,35.4L22.4,42.6L28.8,35.2Q29.8,33.9 31.4,33.9H38.4"
         "Q41.6,33.9 41.3,37.4Q40.8,42.9 36.4,42.9H30.6L32.9,36.4 "                 # swoosh, V and second D
         "M14.8,33.9Q16.2,35 15.8,38.2Q15.2,42.9 10.6,42.9H4.6L6.8,36.4")            # first D: bowl, base, upright
    strokes(ic, d, w_in=2.2, w_out=4.2)
    return ic


def hd_disc():
    """High-definition (Blu-ray class) disc: the same disc with a blue-violet sheen and generic "HD"
    block lettering in the style of the CD and DVD icons (no format logo)."""
    ic = Icon()
    disc(ic, blue=True)
    d = ("M5,31.6V42.8 M11.8,31.6V42.8 M5,37.2H11.8 "
         "M16,31.6V42.8H19.4Q24.4,42.8 24.4,37.2Q24.4,31.6 19.4,31.6H16")
    strokes(ic, d, w_in=2.4, w_out=4.6)
    return ic


# ------------------------------------------------------------------ floppy
def floppy(ic=None):
    """3.5-inch floppy traced from the original: turned 45 degrees, label at the far (top right) end,
    metal shutter at the near (lower left) end, the cut corner on the left."""
    ic = ic or Icon()
    W, H = 38, 41
    f0 = frame(32, .8, 44)
    f = lambda x, y: f0(x * 42 / 38, y * 44 / 41)     # drawn at 38 x 41, scaled to fill the canvas
    body = [(0, 0), (W, 0), (W, H), (6, H), (0, H - 6)]          # chamfer at the left corner
    d = poly(f, body)
    ic.shadow(d, 1.6, 1.4)
    ic.path(rpoly(f, body, 1.6), ic.lg([(0, "#9aa0a8"), (.5, "#6c727a"), (1, "#3c4148")], 0, 0, 1, 1), INK, LW * 1.2)
    # light bevel along the far right edges
    ic.add(f'<path d="{poly(f, [(W - 2, 2), (W - 2, H - 2), (7, H - 2)], False)}" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width="1.1"/>')
    # label
    ic.path(poly(f, [(5, 1.5), (W - 4, 1.5), (W - 4, 21), (5, 21)]), ic.lg([(0, "#ffffff"), (1, "#e4e8ec")], 0, 0, 1, 1), INK, .9)
    for k in range(5):
        ic.add(f'<path d="{poly(f, [(9, 6 + k * 3.2), (W - 7, 6 + k * 3.2)], False)}" stroke="#2a9aa8" stroke-width="1.2"/>')
    # metal shutter with its window, and the recess beside it
    ic.path(poly(f, [(7, 26), (27, 26), (27, H), (7, H)]), ic.lg([(0, "#ffffff"), (.5, "#d0d4d9"), (1, "#8a9098")], 0, 0, 1, 1), INK, .9)
    ic.path(poly(f, [(11, 29), (18, 29), (18, 37.5), (11, 37.5)]), ic.lg([(0, "#5c6168"), (1, "#1a1d22")]), INK, .8)
    ic.path(poly(f, [(27, 30), (W - 3, 30), (W - 3, H), (27, H)]), ic.lg([(0, "#4c5158"), (1, "#26292e")]), INK, .8)
    return ic


# ------------------------------------------------------------------ USB
def usb(ic=None):
    """The USB trident on its own, outlined in black like the rest of the theme, brushed silver inside."""
    ic = ic or Icon()
    trunk, up, down = "M9,34H50", "M18,34Q23,34 27,22H38", "M27,34Q32,34 36,45H43"
    strokes = f"{trunk} {up} {down}"
    ic.add(f'<path d="{strokes}" fill="none" stroke="#000" stroke-opacity=".25" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" transform="translate(2,2)"/>')
    ic.add(f'<path d="{strokes}" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>')
    ic.add(f'<path d="{strokes}" fill="none" stroke="#9aa0a8" stroke-width="4.2" stroke-linecap="round" stroke-linejoin="round"/>')
    ic.add(f'<path d="M9,33H49M19,32.6Q22.6,32 26.2,21.2H37" fill="none" stroke="#f4f5f7" stroke-width="1.1" stroke-linecap="round"/>')
    blue = lambda: ic.rg([(0, "#ffffff"), (.5, "#b4b9c0"), (1, "#5c6168")], .35, .3, .8)
    for shape in ("M48,26.5L60,34L48,41.5Z", circle(8.5, 34, 5.5), circle(39.5, 22, 4.6), "M40.5,41H48.5V49H40.5Z"):
        ic.add(f'<path d="{shape}" fill="#000" fill-opacity=".25" transform="translate(2,2)"/>')
        ic.path(shape, blue(), INK, LW * 1.1)
    return ic


# ------------------------------------------------------------------ keyboard (single keycap, isometric)
def keycap(ic=None):
    """The KDE Classic keyboard icon: one beige keycap in isometric view, rounded edges, a K engraved on the top."""
    ic = ic or Icon()
    BR = "#5a4a30"                                                   # the original's brown outline
    Lt, Bk, Rt, Fr = (10, 20), (31, 12), (54, 20), (33, 28.5)        # top face
    Lb, Fb, Rb = (3.5, 43), (33.5, 54), (60.5, 43)                  # base corners
    SAG = 2.6                                                        # how far the scooped edges dip
    q = lambda a, b: (f"{(a[0] + b[0]) / 2:.2f},{(a[1] + b[1]) / 2 + 2 * SAG:.2f}")
    c = lambda p: f"{p[0]:.2f},{p[1]:.2f}"
    # the edges above and below the K (back and front) curve down into the scoop
    cq = lambda a, b: ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + 2 * SAG)
    out = rounded([Bk, Rt, Rb, Fb, Lb, Lt], [cq(Bk, Rt), None, None, None, None, None], 3)
    ic.shadow(out, 3, 2.4)
    ic.path(out, ic.lg([(0, "#ece6cc"), (1, "#a49a7a")], 0, 0, 0, 1), BR, LW)
    right = rounded([Fr, Rt, Rb, Fb], [None] * 4, 2.4)
    ic.path(right, ic.lg([(0, "#b8ae8c"), (1, "#7e7252")], 0, 0, .3, 1), None)
    left = rounded([Lt, Fr, Fb, Lb], [cq(Lt, Fr), None, None, None], 2.4)
    ic.path(left, ic.lg([(0, "#f4f0e0"), (1, "#c4bc9e")], 0, 0, .3, 1), None)
    top = rounded([Bk, Rt, Fr, Lt], [cq(Bk, Rt), None, cq(Fr, Lt), None], 3)
    # concave top: shaded under the back edge, brightest just in front of the middle, a lit front lip
    ic.path(top, ic.lg([(0, "#c8be9a"), (.25, "#e6dfc6"), (.62, "#fffef8"), (.86, "#f7f3e6"), (1, "#e2dbc0")]), None)
    k1, k2 = (Bk[0] + 1.2, Bk[1] + 1.6), (Rt[0] - 2.4, Rt[1] + .8)
    ic.add(f'<path d="M{Lt[0] + 2.4:.1f},{Lt[1]:.1f}L{c(k1)}Q{(k1[0] + k2[0]) / 2:.2f},{(k1[1] + k2[1]) / 2 + 2 * SAG:.2f} {c(k2)}" fill="none" stroke="#a89c78" stroke-opacity=".45" stroke-width="1.8" stroke-linejoin="round"/>')
    f1, f2 = (Lt[0] + 2.2, Lt[1] + 2.2), (Fr[0] - .6, Fr[1] + 1.6)
    ic.add(f'<path d="M{c(f1)}Q{(f1[0] + f2[0]) / 2:.2f},{(f1[1] + f2[1]) / 2 + 2 * SAG:.2f} {c(f2)}" fill="none" stroke="#fff" stroke-opacity=".9" stroke-width="1.4"/>')
    ic.path(top, "none", BR, .9)
    ic.add(f'<path d="M{Fr[0]},{Fr[1] + 2}L{Fb[0]},{Fb[1] - 2.5}" stroke="#fff" stroke-opacity=".5" stroke-width="1.2"/>')
    ic.path(out, "none", BR, LW * 1.1)
    # K on the top face: letter-up runs toward the back edge, letter-right toward the front-left edge
    o = Bk
    ux, uy = (Fr[0] - Lt[0]), (Fr[1] - Lt[1])
    vx, vy = (Lt[0] - Bk[0]), (Lt[1] - Bk[1])
    P = lambda u, v: (o[0] + u * ux + v * vx, o[1] + u * uy + v * vy)
    def seg(a, b):
        (x1, y1), (x2, y2) = P(*a), P(*b)
        return f"M{x1:.2f},{y1:.2f}L{x2:.2f},{y2:.2f}"
    k = seg((.36, .28), (.36, .72)) + seg((.66, .28), (.39, .53)) + seg((.48, .45), (.68, .72))
    ic.add(f'<path d="{k}" stroke="#fff" stroke-width="2.4" stroke-linecap="round" transform="translate(.4,.7)"/>')
    ic.add(f'<path d="{k}" stroke="#bfb48e" stroke-width="2.1" stroke-linecap="round"/>')
    return ic


# ------------------------------------------------------------------ mouse
def mouse(ic=None):
    """Mouse traced from the original's outline: a long, even oval (not pear shaped), nose to the
    upper left, side showing along the lower left. Two buttons and a scroll wheel, cable off the nose."""
    ic = ic or Icon()
    from traceart import catmull
    C, ANG = (36.6, 35.2), 34.2
    f = frame(C[0], C[1], ANG)

    def oval(a, b, ox=0, oy=0, n=2.35, steps=48):
        pts = []
        for k in range(steps):
            t = 2 * math.pi * k / steps
            c_, s_ = math.cos(t), math.sin(t)
            pts.append((ox + a * math.copysign(abs(c_) ** (2 / n), c_), oy + b * math.copysign(abs(s_) ** (2 / n), s_)))
        return pts

    def half(a, b, x, n=2.35):
        return b * max(0.0, 1 - abs(x / a) ** n) ** (1 / n)

    A, B = 27.2, 16.4                      # whole silhouette (half length, half width)
    TA, TB, TY = 26.2, 13.6, -2.4          # top face, shifted toward the upper right
    sil = catmull([f(*p) for p in oval(A, B)])
    top = catmull([f(*p) for p in oval(TA, TB, 0, TY)])
    nose = f(-A + .6, -1.2)
    ic.add(f'<path d="M{nose[0]:.1f},{nose[1]:.1f}Q9.5,16.5 6,12Q2.6,7.2 7.4,5Q11.4,3.4 16.4,5.2" fill="none" stroke="{INK}" stroke-width="1.8" stroke-linecap="round"/>')
    ic.shadow(sil, 3, 2.4)
    ic.path(sil, ic.lg([(0, "#d9dce0"), (1, "#5c6168")], 1, 0, 0, 1), INK, LW)
    ic.path(top, ic.rg([(0, "#ffffff"), (.6, "#f2f3f5"), (1, "#c3c7cd")], .5, .4, .7), INK, 1)
    # buttons: a line across the front third, bowed toward the back, and the split down the middle
    X = -8.5
    h = half(TA, TB, X) - .2
    p1, pm, p2 = f(X, TY - h), f(X + 3.2, TY), f(X, TY + h)
    ic.add(f'<path d="M{p1[0]:.2f},{p1[1]:.2f}Q{pm[0]:.2f},{pm[1]:.2f} {p2[0]:.2f},{p2[1]:.2f}" fill="none" stroke="{INK}" stroke-width="1"/>')
    a1, a2 = f(-TA + .4, TY), f(X + 1.6, TY)
    ic.add(f'<path d="M{a1[0]:.2f},{a1[1]:.2f}L{a2[0]:.2f},{a2[1]:.2f}" stroke="{INK}" stroke-width="1"/>')
    # scroll wheel sitting in the split
    wheel = rpoly(f, [(-19.5, TY - 1.9), (-12.5, TY - 1.9), (-12.5, TY + 1.9), (-19.5, TY + 1.9)], 1.8)
    ic.path(wheel, ic.lg([(0, "#8a9098"), (.5, "#2c3036"), (1, "#14171c")], 0, 0, 0, 1), INK, .8)
    for x in (-17.6, -16, -14.4):
        q1, q2 = f(x, TY - 1.3), f(x, TY + 1.3)
        ic.add(f'<path d="M{q1[0]:.2f},{q1[1]:.2f}L{q2[0]:.2f},{q2[1]:.2f}" stroke="#9aa0a8" stroke-width=".55"/>')
    h1, h2 = f(-21, TY - 7.5), f(-10.5, TY - 11)
    ic.add(f'<path d="M{h1[0]:.2f},{h1[1]:.2f}L{h2[0]:.2f},{h2[1]:.2f}" stroke="#fff" stroke-width="1.6" stroke-linecap="round"/>')
    # the original's colourful marks on the palm
    r1 = f(-2.5, TY - 4); g1 = f(-2.5, TY + 1.5); b1, b2, b3 = f(1.5, TY + 5.5), f(9.5, TY - 3.5), f(8.5, TY + 7)
    ic.path(circle(round(r1[0], 2), round(r1[1], 2), 1.5), "#d8302a", None)
    ic.add(f'<path d="M{g1[0] - 1.5:.2f},{g1[1] - 1.5:.2f}L{g1[0]:.2f},{g1[1] + 1:.2f}L{g1[0] + 2.5:.2f},{g1[1] - .5:.2f}" fill="none" stroke="#2f9a2e" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>')
    ic.add(f'<path d="M{b1[0]:.2f},{b1[1]:.2f}L{b2[0]:.2f},{b2[1]:.2f}M{b1[0]:.2f},{b1[1]:.2f}L{b3[0]:.2f},{b3[1]:.2f}" stroke="#1a3ec8" stroke-width="1.6" stroke-linecap="round"/>')
    return ic


# ------------------------------------------------------------------ printer
def printer(ic=None):
    """Printer in isometric view, after KDE Classic's: an oblong grey body with a rounded lid (a half cylinder on
    top), the sheet standing in the feed slot at the back, the printed sheet sliding out onto the tray in front."""
    ic = ic or Icon()
    W, D, H = 40, 19, 9                        # length, depth (front to back), height of the box below the lid
    R = D / 2                                  # the lid is a half cylinder along the length
    c, sn = .9, .36                            # a lower camera than true isometric: more front, less lid
    raw = lambda x, y, z: ((y - x) * c, (x + y) * sn - z)     # facing right: the tray comes out to the lower right

    def arc(x, n=14):                          # cross-section of the lid at length x, back to front
        return [(x, R - R * math.cos(math.pi * k / n), H + R * math.sin(math.pi * k / n)) for k in range(n + 1)]

    def hull(pts):
        pts = sorted(set(pts))
        cross = lambda o, a, b: (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
        lo, up = [], []
        for p in pts:
            while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
                lo.pop()
            lo.append(p)
        for p in reversed(pts):
            while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0:
                up.pop()
            up.append(p)
        return lo[:-1] + up[:-1]

    xa, xb = 8, W - 8                          # both sheets are the same width: real, rectangular paper
    yslot = R * 1.25                           # the feed slot is in the top of the lid, just in front of its crown
    zb = H + math.sqrt(R * R - (yslot - R) ** 2)

    def sheet_at(t):                           # the waiting sheet stands up out of the slot and curls back at the top
        return (yslot - 1.2 * t - 6 * t ** 4, zb - .4 + 17 * t - 2 * t ** 4)
    ts = [k / 10 for k in range(11)]
    sheet3 = [(xa,) + sheet_at(t) for t in ts] + [(xb,) + sheet_at(t) for t in reversed(ts)]

    def tray_at(u):                            # the printed sheet slides out and droops a little
        return (D + 12 * u, 3.6 - 1.2 * u - 1.2 * u ** 2)
    tray3 = [(xa,) + tray_at(u) for u in ts] + [(xb,) + tray_at(u) for u in reversed(ts)]
    box3 = [(x, y, z) for x in (0, W) for y in (0, D) for z in (0, H)]
    allp = [raw(*p) for p in box3 + arc(0) + arc(W) + sheet3 + tray3]
    xs, ys = [p[0] for p in allp], [p[1] for p in allp]
    ox, oy = 31 - (min(xs) + max(xs)) / 2, 31.5 - (min(ys) + max(ys)) / 2

    def iso(x, y, z):
        u, v = raw(x, y, z)
        return (ox + u, oy + v)
    D2 = lambda pts: "M" + "L".join("%.2f,%.2f" % p for p in pts) + "Z"
    P = lambda *pts: D2([iso(*p) for p in pts])

    body2 = hull([iso(*p) for p in box3 + arc(0) + arc(W)])
    ic.shadow(D2(body2), 3.2, 2.6)
    # rounded lid, lit from the front left
    lid = hull([iso(*p) for p in arc(0) + arc(W)])
    ic.path(D2(lid), ic.lg([(0, "#ececec"), (.4, "#d2d3d5"), (.75, "#bdc1c3"), (1, "#a4aaad")], 1, .2, 0, .8), None)
    crown = [iso(x, R * .6, H + R * .97) for x in (2, W - 2)]
    ic.add('<path d="M%.2f,%.2fL%.2f,%.2f" stroke="#ffffff" stroke-width="2.2" stroke-linecap="round" stroke-opacity=".8"/>' % (crown[0] + crown[1]))
    # feed slot in the top of the lid: a dark opening with a lit lip in front
    y0, y1 = yslot - 2.4, yslot + 2.2
    z0, z1 = H + math.sqrt(R * R - (y0 - R) ** 2), H + math.sqrt(R * R - (y1 - R) ** 2)
    ic.path(P((xa - 4, y0, z0), (xb + 4, y0, z0), (xb + 4, y1, z1), (xa - 4, y1, z1)), "#2c3036", INK, .9)
    # front face (lower right, a little in shade) and the lit left-hand end with the lid's half-round cap
    ic.path(P((0, D, H), (W, D, H), (W, D, 0), (0, D, 0)), ic.lg([(0, "#d1d4d6"), (.5, "#bbbfc1"), (1, "#959b9e")], 0, 0, 1, 1), None)
    ic.path(D2([iso(W, 0, 0), iso(W, 0, H)] + [iso(*p) for p in arc(W)] + [iso(W, D, 0)]),
            ic.lg([(0, "#efefef"), (.5, "#dddee0"), (1, "#c3c6c8")], 0, 0, 1, 1), None)
    # seam between lid and body, along the front and down the left-hand end, and the front corner
    ic.add('<path d="M%.2f,%.2fL%.2f,%.2fL%.2f,%.2f" fill="none" stroke="#808080" stroke-width="1" stroke-linejoin="round"/>'
           % (iso(0, D, H) + iso(W, D, H) + iso(W, 0, H)))
    ic.add('<path d="M%.2f,%.2fL%.2f,%.2f" stroke="#808080" stroke-width="1"/>' % (iso(W, D, H) + iso(W, D, 0)))
    ic.add('<path d="%s" fill="none" stroke="#808080" stroke-width="1"/>' % ("M" + "L".join("%.2f,%.2f" % iso(*p) for p in arc(W))))
    # output slot, buttons and the power light on the front
    ic.path(P((8, D, 5), (W - 8, D, 5), (W - 8, D, 3.4), (8, D, 3.4)), "#3c4148", INK, .8)
    x, y = iso(W - 4, D, 7)
    ic.path("M%.2f,%.2fA1.5,1.5 0 1 0 %.2f,%.2fA1.5,1.5 0 1 0 %.2f,%.2fZ" % (x + 1.5, y, x - 1.5, y, x + 1.5, y), "#4fae5a", INK, .6)
    ic.path(D2(body2), "none", INK, LW)
    # the sheet goes down into the slot (drawn after the outline, so no edge shows through it)
    ic.path(P(*sheet3), ic.lg([(0, "#e7d7c2"), (.4, "#f2eae0"), (1, "#f7f2ee")], 0, 1, 0, 0), "#664b2a", 1.1)
    bend = [iso(x, *sheet_at(.78)) for x in (xa + 1, xb - 1)]
    ic.add('<path d="M%.2f,%.2fL%.2f,%.2f" stroke="#c8b48c" stroke-width=".8"/>' % (bend[0] + bend[1]))
    lip = P((xa - 4, yslot + .9, zb), (xb + 4, yslot + .9, zb), (xb + 4, y1, z1), (xa - 4, y1, z1))
    ic.path(lip, ic.lg([(0, "#dfe0e2"), (1, "#c4c7c9")], 0, 0, 0, 1), None)
    ic.add('<path d="M%.2f,%.2fL%.2f,%.2f" stroke="%s" stroke-width="1"/>' % (iso(xa - 4, yslot + .9, zb) + iso(xb + 4, yslot + .9, zb) + (INK,)))
    ic.add('<path d="M%.2f,%.2fL%.2f,%.2f" stroke="#ffffff" stroke-width=".9" stroke-opacity=".9"/>' % (iso(xa - 3, y1 - .4, z1 + .1) + iso(xb + 3, y1 - .4, z1 + .1)))
    # printed sheet on the tray
    ic.shadow(P(*tray3), 1.4, 1.2)
    ic.path(P(*tray3), ic.lg([(0, "#f7f2ee"), (.5, "#ede1d2"), (1, "#e7d7c2")], 0, 0, 1, 1), "#664b2a", 1.1)
    for u in (.25, .45, .65):
        y, z = tray_at(u)
        ic.add('<path d="M%.2f,%.2fL%.2f,%.2f" stroke="#b8a888" stroke-width=".8"/>' % (iso(xa + 3, y, z) + iso(xb - 3, y, z)))
    return ic


# ------------------------------------------------------------------ scanner
def scanner():
    """Flatbed scanner traced from the original: base turned 45 degrees, glass on the near-left half,
    lid raised over the far-right half, cable curling up behind it, green power light at the front."""
    ic = Icon()
    D = 4                                                            # base thickness
    T, R, B, L = (32.5, 5.5), (59.5, 30.5), (30.5, 57.5), (3.5, 32)  # base top face
    dn = lambda p: (p[0], p[1] + D)
    P = lambda *pts: "M" + "L".join(f"{x:.2f},{y:.2f}" for x, y in pts) + "Z"
    ident = lambda x, y: (x, y)
    base = rpoly(ident, [T, R, dn(R), dn(B), dn(L), L], 2)
    ic.shadow(base, 3.2, 2.6)
    ic.path(P(L, B, dn(B), dn(L)), ic.lg([(0, "#f4f5f7"), (1, "#b4b9c0")]), None)
    ic.path(P(B, R, dn(R), dn(B)), ic.lg([(0, "#8a9098"), (1, "#3c4148")]), None)
    ic.path(rpoly(ident, [T, R, B, L], 2), ic.lg([(0, "#ffffff"), (.6, "#eceef1"), (1, "#c3c7cd")], 0, 0, 1, 1), INK, 1)
    ic.add(f'<path d="M{B[0]:.2f},{B[1]:.2f}V{B[1] + D:.2f}" stroke="{INK}" stroke-width=".8"/>')
    ic.path(base, "none", INK, LW * 1.1)
    # glass in a white frame
    Tg, Rg, Bg, Lg = (25, 19.5), (41.5, 35.5), (29, 48.5), (11.5, 33)
    ic.path(P(Tg, Rg, Bg, Lg), ic.lg([(0, "#e8f8ff"), (.45, "#8fd0f4"), (1, "#3d9ad8")], 0, 0, 1, 1), INK, .9)
    ic.add(f'<path d="{P(Tg, (34, 28.2), (16, 30.5))}" fill="#fff" fill-opacity=".4"/>')
    ic.path(circle(26.2, 56.4, 1.2), "#4fae5a", "#1a5c2a", .4)
    # cable from behind the lid
    ic.add(f'<path d="M50.5,19Q55.5,16.5 53.8,12.2Q52.2,8.4 56.2,4.6" fill="none" stroke="{INK}" stroke-width="1.6" stroke-linecap="round"/>')
    # lid, raised and leaning back over the far half; its near edge runs along the glass
    A, Bl, Cl, Dl = (16, 9.5), (35, 3.8), (56.4, 25.6), (41.2, 34.6)
    ic.path(P(Dl, Cl, (Cl[0], Cl[1] + 2.4), (Dl[0], Dl[1] + 2.4)), "#7b818a", INK, .9)
    ic.path(P(A, Bl, Cl, Dl), ic.lg([(0, "#ffffff"), (.5, "#e2e5e9"), (1, "#a4aab2")], 0, 0, 1, 1), INK, LW)
    ic.add(f'<path d="M{A[0] + 2:.1f},{A[1] + .8:.1f}L{Bl[0] - 1:.1f},{Bl[1] + 1.4:.1f}" stroke="#fff" stroke-width="1.2"/>')
    return ic


# ------------------------------------------------------------------ camera
def camera(ic=None):
    """Compact camera in 3/4 view: white body, big black lens, viewfinder and flash."""
    ic = ic or Icon()
    t = "matrix(1,0.18,0,1,0,-5)"
    body = "M5,18Q5,15 8,15H50Q53,15 53,18V44Q53,47 50,47H8Q5,47 5,44Z"
    side = "M53,18L59,15V41L53,44Z"
    ic.shadow(body + side, 3.4, 2.8, transform=t)
    ic.add(f'<g transform="{t}">')
    ic.path(side, ic.lg([(0, "#d4d7dc"), (1, "#7b818a")]), INK, LW)
    ic.path("M8,15L14,11H56L59,15H53Z", "#f4f5f7", INK, 1)
    ic.path(body, ic.lg([(0, "#ffffff"), (.5, "#eceef1"), (1, "#b4b9c0")]), INK, LW)
    ic.path("M10,11V9H17V11Z", "#4c5158", INK, .8)
    ic.path(rrect(40, 19, 9, 6, 1), ic.lg([(0, "#4a5a6a"), (1, "#141820")]), INK, .8)    # viewfinder
    ic.path(rrect(8, 19, 8, 5, 1), ic.lg([(0, "#ffffff"), (1, "#c9ccd1")]), INK, .8)      # flash
    ic.add("</g>")
    # lens (upright, not skewed)
    ic.path(circle(27, 33.5, 13.5), ic.rg([(0, "#ffffff"), (.6, "#c3c7cd"), (1, "#6c727a")]), INK, LW)
    ic.path(circle(27, 33.5, 10), ic.rg([(0, "#5c6878"), (.5, "#20262e"), (1, "#060809")]), INK, 1)
    ic.path(circle(27, 33.5, 5.5), ic.rg([(0, "#8aa4c0"), (.6, "#2a3a50"), (1, "#0a1018")]), None)
    ic.add('<path d="M21.5,28.5Q24,26 27.5,26.4" fill="none" stroke="#fff" stroke-opacity=".85" stroke-width="1.4" stroke-linecap="round"/>')
    return ic


# ------------------------------------------------------------------ PDA / phone
def pda():
    ic = Icon()
    t = "translate(32,32) rotate(-28) translate(-32,-32)"
    body = rrect(16, 6, 32, 52, 4)
    ic.shadow(body, 3, 2.6, transform=t)
    ic.add(f'<g transform="{t}">')
    ic.path(body, ic.lg([(0, "#b4b9c0"), (.5, "#6c727a"), (1, "#3c4148")], 0, 0, 1, 0), INK, LW)
    ic.path(rrect(20, 10, 24, 30, 1.2), ic.lg([(0, "#d8f2ff"), (.6, "#7cc4ec"), (1, "#2a7ab8")], 0, 0, 1, 1), INK, .9)
    ic.add('<path d="M22,12L36,12L22,26Z" fill="#fff" fill-opacity=".4"/>')
    for i, x in enumerate((22, 28, 36, 42)):
        ic.path(circle(x, 47, 2), ic.rg([(0, "#d9dce0"), (1, "#3c4148")]), INK, .6)
    ic.path(rrect(29, 51, 6, 3, 1.2), "#2c3036", None)
    ic.add("</g>")
    return ic


def external_drive(ic=None, usb_mark=False):
    """External drive: a small silver drive case in 3/4 view with its activity light, in the hard disk's
    colours. With usb_mark, the USB trident on its front (generic USB storage: external disks, card readers)."""
    ic = ic or Icon()
    front = "M5,26H48V56H5Z"
    top = "M5,26L17,15H60L48,26Z"
    side = "M48,26L60,15V45L48,56Z"
    ic.shadow(front + side, 3, 2.4)
    ic.path(side, ic.lg([(0, "#9aa0a8"), (1, "#4c5158")], 0, 0, 0, 1), INK, LW)
    ic.path(top, ic.lg([(0, "#ffffff"), (1, "#c3c7cd")], 0, 0, 1, 1), INK, LW)
    ic.path(front, ic.lg([(0, "#f4f5f7"), (.5, "#c3c7cd"), (1, "#7b818a")], 0, 0, .3, 1), INK, LW)
    ic.add('<path d="M7,28.4H46" stroke="#fff" stroke-width="1.2"/>')
    for k in range(4):
        ic.add(f'<path d="M51,{30 + k * 4}L57,{25 + k * 4}" stroke="#2c3036" stroke-opacity=".5" stroke-width="1.2"/>')
    ic.path(circle(42, 51, 1.9), ic.rg([(0, "#d8f8ff"), (.5, "#2aa0f0"), (1, "#0a4a8a")]), INK, .6)
    if usb_mark:
        ic.add('<g transform="translate(6.7,20.2) scale(.62)">')
        usb(ic)
        ic.add("</g>")
    else:
        ic.add('<path d="M10,47H34M10,51H28" stroke="#5c6168" stroke-width="1.4"/>')
    return ic


def external_drive_usb(ic=None):
    return external_drive(ic, True)


def memory_card(ic=None):
    """Memory card: a blue SD card with its notched corner, gold contacts and a white label."""
    ic = ic or Icon()
    card = "M12,4H44L52,12V60H12Z"
    ic.shadow(card, 2.6, 2.2)
    ic.path(card, ic.lg([(0, "#8ab8f0"), (.45, "#2a5ab0"), (1, "#0a1e5a")], 0, 0, 1, 1), INK, LW * 1.2)
    for k in range(5):
        x = 16 + k * 6
        ic.path(f"M{x},7H{x + 4}V17H{x}Z", ic.lg([(0, "#fff4b0"), (.5, "#e8b830"), (1, "#a87a10")], 0, 0, 1, 0), INK, .7)
    ic.path("M17,26H47V52H17Z", ic.lg([(0, "#ffffff"), (1, "#d9dce0")], 0, 0, 1, 1), INK, 1)
    ic.add('<path d="M21,33H43M21,39H38" stroke="#2a5ab0" stroke-width="2"/>')
    ic.add('<path d="M14.6,7V57" stroke="#fff" stroke-opacity=".45" stroke-width="1.4"/>')
    ic.path("M8,30H12V36H8Z", ic.lg([(0, "#e4e6e9"), (1, "#7b818a")]), INK, .8)
    return ic


DEVICES = {
    "drive-harddisk": harddisk, "media-optical": cd, "media-optical-dvd": dvd, "media-optical-blu-ray": hd_disc, "media-floppy": floppy,
    "drive-removable-media": external_drive, "drive-removable-media-usb": external_drive_usb,
    "media-flash": memory_card, "printer": printer, "scanner": scanner, "camera-photo": camera,
    "input-keyboard": keycap, "input-mouse": mouse, "pda": pda,
}
DEVICE_ALIASES = {
    "drive-harddisk-solidstate": "drive-harddisk", "media-optical-cd": "media-optical", "drive-optical": "media-optical",
    "media-optical-recordable": "media-optical", "media-optical-cd-recordable": "media-optical", "media-optical-audio": "media-optical",
    "media-optical-dvd-video": "media-optical-dvd", "media-optical-bd": "media-optical-blu-ray",
    "media-floppy-350": "media-floppy", "printer-network": "printer", "camera-web": "camera-photo",
    "phone": "pda", "smartphone": "pda", "multimedia-player": "pda",
}
