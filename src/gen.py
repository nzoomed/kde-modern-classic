#!/usr/bin/env python3
"""KDE Classic Vector: a modern SVG take on the KDE 2/3 "KDE Classic" icons.

Style rules (measured from the original PNGs; see STYLE.md):
  * 3/4 view: folders and devices lean back, the right side drops (skew ~0.16)
  * near-black outline on every shape (1.4 units on a 64 grid = ~1 px at 48)
  * white/grey bodies with one saturated colour band, gradients top-left light
  * hard-edged hatching in the shadowed bottom-right corner of folders
  * cast shadow to the lower right, built from stacked translucent copies
  * emblems overlap the lower-left corner and break out of the folder
Only Qt-SVG-safe features: paths, linear/radial gradients, opacity, transforms.
No filters, masks, clip paths or patterns.
"""
import math, os, shutil, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "KDE-Classic-Vector"
INK = "#141414"
LW = 1.4

# folder band colours (light, mid, dark)
BAND = {
    "blue": ("#c4ecff", "#3d9ad8", "#1a5c9e"), "red": ("#ffd0c4", "#d8573d", "#9e2a1a"),
    "green": ("#d0f5c8", "#4fae5a", "#22703a"), "yellow": ("#fff6c0", "#e8c43a", "#a8840e"),
    "orange": ("#ffe2c0", "#ec9a3a", "#ae5e10"), "violet": ("#ead4ff", "#9a62d8", "#5e2c9e"),
    "grey": ("#f2f2f2", "#a8adb4", "#6c727a"), "cyan": ("#c8fbff", "#3cc4d4", "#13808e"),
    "brown": ("#f4dcc0", "#a8723a", "#6a4018"),
}


class Icon:
    def __init__(self):
        self.defs, self.body, self.n = [], [], 0

    def gid(self, p="g"):
        self.n += 1
        return f"{p}{self.n}"

    def lg(self, stops, x1=0, y1=0, x2=0, y2=1):
        i = self.gid("l")
        s = "".join(f'<stop offset="{o}" stop-color="{c}"' + (f' stop-opacity="{a}"' if a != 1 else "") + "/>"
                    for o, c, a in [(t + (1,))[:3] for t in stops])
        self.defs.append(f'<linearGradient id="{i}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">{s}</linearGradient>')
        return f"url(#{i})"

    def rg(self, stops, cx=.38, cy=.32, r=.75):
        i = self.gid("r")
        s = "".join(f'<stop offset="{o}" stop-color="{c}"' + (f' stop-opacity="{a}"' if a != 1 else "") + "/>"
                    for o, c, a in [(t + (1,))[:3] for t in stops])
        self.defs.append(f'<radialGradient id="{i}" cx="{cx}" cy="{cy}" r="{r}" fx="{cx}" fy="{cy}">{s}</radialGradient>')
        return f"url(#{i})"

    def add(self, s):
        self.body.append(s)

    def path(self, d, fill, stroke=INK, w=LW, extra=""):
        st = f' stroke="{stroke}" stroke-width="{w}" stroke-linejoin="round"' if stroke else ""
        self.add(f'<path d="{d}" fill="{fill}"{st}{extra}/>')

    def shadow(self, d, dx=3.2, dy=2.6, steps=3, a=.16, transform=""):
        """Soft-ish cast shadow to the lower right from stacked offset copies."""
        tf = f' transform="{transform}"' if transform else ""
        g = "".join(f'<path d="{d}" fill="#000" fill-opacity="{a:.3f}" transform="translate({dx * (k + 1) / steps:.2f},{dy * (k + 1) / steps:.2f})"/>'
                    for k in range(steps))
        self.add(f"<g{tf}>{g}</g>")

    def svg(self, size=64):
        return ('<?xml version="1.0" encoding="UTF-8"?>\n'
                f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 64 64">'
                f'<defs>{"".join(self.defs)}</defs>{"".join(self.body)}</svg>\n')


def circle(cx, cy, r):
    return f"M{cx + r},{cy}A{r},{r} 0 1 0 {cx - r},{cy}A{r},{r} 0 1 0 {cx + r},{cy}Z"


def rrect(x, y, w, h, r):
    return (f"M{x + r},{y}H{x + w - r}A{r},{r} 0 0 1 {x + w},{y + r}V{y + h - r}A{r},{r} 0 0 1 {x + w - r},{y + h}"
            f"H{x + r}A{r},{r} 0 0 1 {x},{y + h - r}V{y + r}A{r},{r} 0 0 1 {x + r},{y}Z")


# =========================================================== folders
SKEW = "matrix(1,0.14,0,1,0,-2.5)"   # the classic lean: right side drops
BACK = "M4,9Q4,6 7,6H21L24.6,9.8H53Q56,9.8 56,12.8V50H4Z"
FRONT = "M4,17H56V51.5Q56,54 53.5,54H6.5Q4,54 4,51.5Z"
FRONT_OPEN = "M8.5,22H60L56,53Q55.6,55 53.5,55H6Q3.9,55 4.3,53Z"
SMALL = False       # set while drawing the 16/22 px versions


# KDE Classic's folder, redrawn over lines traced from the original: seen in 3/4 view, the front pocket leaning
# back to the right (its edges fall about 0.32 per unit across), the back panel standing behind it with the tab
# on the right, and the folder's thickness showing as a grey side strip down the right-hand edge.
FOLDER_X = 6                     # the traced folder is 48 units wide; this centres it on the canvas
ISO_BACK = ("M6.6,4.2L27.4,11.6Q28.8,12 29.6,11L31.6,8.2Q32.6,6.8 34.2,7.2L44,10.2Q45.4,10.6 46.4,11.8L47.6,13.4"
            "Q48.6,14.6 48.6,16.4V57L44,60.8L4.8,47V6.2Q4.8,4.2 6.6,4.2Z")   # lower corner joined to the pocket's; the top stays open
ISO_TOP = "M2.6,8.2Q1,7.8 1,9.6V{y_l}L44,{y_r}V22.6L30,18.4C28.2,17.8 28.2,15.7 25.8,15.3Z"   # one smooth step down
ISO_FRONT = ISO_TOP.replace("V{y_l}L44,{y_r}", "V46.4Q1,47.6 2.2,48L42,60.6Q44,61.2 44,59.2")


def folder(ic, colour="blue", open_=False):
    l, m, d = BAND[colour]
    w = LW * (1.9 if SMALL else 1)
    ic.shadow(ISO_BACK, 3.6, 3, transform=f"translate({FOLDER_X},0)")
    ic.add(f'<g transform="translate({FOLDER_X},0)">')
    # back panel, tab on the right, and the folder's thickness down the right side
    ic.path(ISO_BACK, ic.lg([(0, "#ffffff"), (.5, "#e4e6e9"), (1, "#b4b9c0")], 0, 0, .4, 1), INK, w)
    if not SMALL:
        ic.add('<path d="M6.8,5.6L27.2,13M33.4,8.6L44,11.8" fill="none" stroke="#fff" stroke-width="1.1"/>')
        ic.add('<path d="M30.4,10.6L31.8,8.8" stroke="#5c6168" stroke-opacity=".5" stroke-width="1.2" stroke-linecap="round"/>')   # tab shoulder
    if open_:          # sheets standing up out of the folder, the pocket swung forward a little
        ic.path("M7,9.4L41,20.4V34L7,23Z", "#fdfdfd", "#8a8f96", .8)
        ic.path("M10,13L44,24V36L10,25Z", "#ffffff", "#8a8f96", .8)
        ic.add('<g transform="translate(0,61) scale(1,.86) translate(0,-61)">')
    front = ISO_FRONT
    band = ISO_TOP.format(y_l=30, y_r=44)
    ic.path(front, ic.lg([(0, "#ffffff"), (.55, "#eceef1"), (1, "#b4b9c0")], 0, 0, .3, 1))
    ic.path(band, ic.lg([(0, l), (.35, m), (.7, d), (1, m)], 0, 0, .25, 1))
    if not SMALL:
        ic.add('<path d="M2.6,11.4L25.4,18.4M2.6,16.6L43,29.4" fill="none" stroke="#fff" stroke-opacity=".7" stroke-width="1.6"/>')
        ic.add('<path d="M2.6,21.6L43,34.4" fill="none" stroke="#fff" stroke-opacity=".25" stroke-width="1"/>')
        ic.add(f'<path d="M1,30L44,44" stroke="{INK}" stroke-opacity=".35" stroke-width=".8"/>')
        if not open_:      # hatched shadow corner, lower right, as in the dithered original
            for k in range(4):
                xb = 30 + k * 3.3
                yb = 48 + (xb - 2.2) * .316 - 1.4
                ic.add(f'<path d="M{xb:.2f},{yb:.2f}L43,{yb - (43 - xb):.2f}" stroke="#7b818a" stroke-width=".9"/>')
        ic.add('<path d="M2.4,10V45.6" stroke="#fff" stroke-opacity=".6" stroke-width="1"/>')
    else:
        ic.add('<path d="M2.6,13L25.4,20" stroke="#fff" stroke-opacity=".7" stroke-width="2.4"/>')
    ic.path(front, "none", INK, w)
    if open_:
        ic.add("</g>")
    ic.add("</g>")


def make_folder(colour="blue", emblem=None, open_=False):
    def f():
        ic = Icon()
        folder(ic, colour, open_)
        if emblem:
            k = 1.5 if SMALL else 1.2
            ax = EMBLEM_ANCHOR_X.get(emblem, 0)   # scale from the corner the emblem sits in
            ic.add(f'<g transform="translate({ax},64) scale({k}) translate({-ax},-64)">')
            EMBLEM[emblem](ic)
            ic.add("</g>")
        return ic
    return f


# =========================================================== emblems (drawn upright, lower-left)
def e_house(ic, x=2, y=27, s=1.0):
    t = f"translate({x},{y}) scale({s})"
    ic.shadow("M2,14L15,2L28,14V30H2Z", 2.4, 2, transform=t)
    ic.add(f'<g transform="{t}">')
    ic.path("M4,13V30H26V13L15,4Z", ic.lg([(0, "#ffffff"), (1, "#d9d4c8")]))
    ic.path("M1,15L15,2L29,15L26.4,17.4L15,7L3.6,17.4Z", ic.lg([(0, "#8a8f96"), (1, "#3c4148")]))
    ic.path("M11,30V20.5Q11,17.5 15,17.5Q19,17.5 19,20.5V30Z", ic.lg([(0, "#d2722c"), (1, "#7c3a10")], 0, 0, 1, 0))
    ic.add('<path d="M5.5,14.5L15,5.8" stroke="#fff" stroke-opacity=".5" stroke-width="1"/>')
    ic.add("</g>")


def e_globe(ic, x=1, y=26, r=15):
    """Classic KDE globe: Africa/Europe view, yellow-green land on a cyan-to-deep-blue sea."""
    cx, cy = x + r, y + r
    ic.shadow(circle(cx, cy, r), 2.6, 2.4)
    ic.path(circle(cx, cy, r), ic.rg([(0, "#c8f4ff"), (.35, "#3cb8ee"), (.75, "#1468c0"), (1, "#0a3478")], .34, .28, .8), INK, LW * .9)
    k = r / 15
    # land drawn on a 30x30 frame, enlarged 14% about its centre and nudged left like the original
    tf = (f"translate({cx - 15 * k:.2f},{cy - 15 * k:.2f}) scale({k:.4f}) "
          f"translate(15,15) scale(1.14) translate(-16,-15.4)")
    land = ic.rg([(0, "#fbf68a"), (.3, "#c4e64a"), (.62, "#5cb82e"), (1, "#1a6a1e")], .3, .2, .95)
    ic.add(f'<path transform="{tf}" fill="{land}" stroke="#0e4a14" stroke-width=".7" stroke-linejoin="round" d="'
           'M9.5,4.2C11.4,3.2 13.8,3.4 15.6,4.4C16.6,5 16.1,6.2 17.2,6.6C18.6,7 19.6,5.8 21,6.4C22.6,7.2 23.8,8.6 24.2,10'
           'C22.8,10.4 21.6,10 20.6,10.8C19.6,11.6 19.8,12.8 18.6,13C17.4,13.2 16.4,12.2 15.2,12.4C14,12.6 13.4,11.6 12.2,11.8'
           'C11,12 10.2,13 9,12.6C8.2,11.4 8.8,10 8,9C7.4,7.6 8.2,5.2 9.5,4.2Z '
           'M10.6,13.6C12.6,13 14.6,13.4 16.4,14.2C17.6,14.8 19,14.4 20.2,15C21.4,15.8 21.6,17.4 22.6,18.2'
           'C23.2,19.4 22,20.4 21.4,21.6C20.4,23.4 19.8,25.4 18.4,26.8C17.2,27.8 16,26.8 15.6,25.6C15,23.6 15.4,21.4 14.2,19.8'
           'C13,18.6 11.2,18.8 10,17.8C9.2,16.6 9.4,14.4 10.6,13.6Z '
           'M21.6,12.4C23,12 24.6,12.8 25.6,14C26.2,15.2 25.4,16.4 24.4,16.8C23.2,16.4 22.6,15.2 21.8,14.4C21.2,13.8 21,12.8 21.6,12.4Z '
           'M2.6,15.4C3.6,15 4.6,15.8 5,17C5.6,19 5.2,21.4 4.4,23.2C3.8,22.2 3,20.6 2.6,19C2.3,17.8 2.2,16.4 2.6,15.4Z"/>')
    ic.add(f'<path d="M{cx - r * .74:.2f},{cy - r * .2:.2f}C{cx - r * .66:.2f},{cy - r * .86:.2f} {cx + r * .46:.2f},{cy - r * .98:.2f} {cx + r * .7:.2f},{cy - r * .4:.2f}'
           f'C{cx + r * .28:.2f},{cy - r * .56:.2f} {cx - r * .3:.2f},{cy - r * .46:.2f} {cx - r * .74:.2f},{cy - r * .2:.2f}Z" fill="#fff" fill-opacity=".62"/>')
    ic.add(f'<path d="{circle(cx, cy, r - .6)}" fill="none" stroke="#082a60" stroke-opacity=".35" stroke-width="1.2"/>')


def speaker_parts(cx=21.0, cy=44.0, ry=18.0):
    """Speaker geometry (KDE Classic audio icon), level axis at cy: a small box at the back, a long teal flare
    running from it to the rim at the top and bottom of the opening, and the opening seen almost edge-on.
    Redrawn 2026-10-27: smaller box set further back so the flare shows, as on the original. The rim (cx, rx)
    is where it was, so the volume icons' sound waves still line up."""
    rx = ry * .37
    bx0, bx1, bh = cx - 20.6, cx - 14.4, ry * .36       # back box
    top, bot = cy - ry, cy + ry
    return dict(
        rx=rx,
        sil=f"M{bx0},{cy - bh}H{bx1}L{cx},{top}A{rx},{ry} 0 0 1 {cx},{bot}L{bx1},{cy + bh}H{bx0}Z",
        box=f"M{bx0},{cy - bh}H{bx1}V{cy + bh}H{bx0}Z",
        shell=f"M{bx1},{cy - bh}L{cx},{top}A{rx},{ry} 0 0 0 {cx},{bot}L{bx1},{cy + bh}Z",
        hl=f"M{bx1 + .9},{cy - bh - .4}L{cx - .8},{top + 1.8}",
        box_hl=f"M{bx0 + 1},{cy - bh + 1.1}H{bx1 - 1}",
        rim=f"M{cx},{top}A{rx},{ry} 0 0 1 {cx},{bot}A{rx},{ry} 0 0 1 {cx},{top}Z",
        inner=(f"M{cx + .5},{top + 1.8}A{rx - 1.2},{ry - 1.8} 0 0 1 {cx + .5},{bot - 1.8}"
               f"A{rx - 1.2},{ry - 1.8} 0 0 1 {cx + .5},{top + 1.8}Z"),
    )


def e_speaker(ic, **kw):
    """Loudspeaker emblem (KDE Classic folder_sound / audio icon): teal box and long flare, the inside of the
    cone shadowed at the top and bright below, and a pointed silver dome growing out of the cone's left edge.
    A lighter outline than the theme's usual LW, as the original speaker was finely drawn."""
    import math
    cx, cy, ry = kw.get("cx", 21.0), kw.get("cy", 44.0), kw.get("ry", 18.0)
    p = speaker_parts(cx, cy, ry)
    ow = .9
    teal = ic.lg([(0, "#b8f6f8"), (.32, "#22c0d0"), (.7, "#0a7486"), (1, "#063e48")], 0, 0, 0, 1)
    ic.shadow(p["sil"], 2.6, 2.2)
    ic.path(p["shell"], teal, INK, ow)
    ic.add(f'<path d="{p["hl"]}" stroke="#fff" stroke-opacity=".8" stroke-width="1.1" stroke-linecap="round"/>')
    ic.path(p["box"], teal, INK, ow)
    ic.add(f'<path d="{p["box_hl"]}" stroke="#fff" stroke-opacity=".7" stroke-width="1"/>')
    ic.path(p["rim"], ic.lg([(0, "#3aa6b4"), (1, "#0a4a54")], 0, 0, 1, 0), INK, ow)
    ic.path(p["inner"], ic.lg([(0, "#4c5158"), (.3, "#8a9098"), (.58, "#eceef1"), (1, "#c3c7cd")], .2, 0, .5, 1), None)
    cxi, rxi, ryi = cx + .5, p["rx"] - 1.2, ry - 1.8
    d, w = ryi * .32, rxi * 1.0
    xe = cxi - rxi * math.sqrt(1 - (d / ryi) ** 2)
    dome = (f"M{xe:.2f},{cy - d:.2f}C{xe + w * .5:.2f},{cy - d * .92:.2f} {xe + w * .88:.2f},{cy - d * .34:.2f} {xe + w:.2f},{cy:.2f}"
            f"C{xe + w * .88:.2f},{cy + d * .34:.2f} {xe + w * .5:.2f},{cy + d * .92:.2f} {xe:.2f},{cy + d:.2f}"
            f"A{rxi:.2f},{ryi:.2f} 0 0 1 {xe:.2f},{cy - d:.2f}Z")
    ic.path(dome, ic.lg([(0, "#ffffff"), (.45, "#d9dce0"), (1, "#5c6168")], 0, 0, .4, 1), "#202428", .6)
    ic.add(f'<path d="M{xe + w * .18:.2f},{cy - d * .62:.2f}Q{xe + w * .55:.2f},{cy - d * .5:.2f} {xe + w * .78:.2f},{cy - d * .14:.2f}" '
           f'fill="none" stroke="#fff" stroke-width=".9" stroke-linecap="round"/>')
    ic.path(p["rim"], "none", INK, ow)


def e_note(ic):
    ic.shadow("M14,30L36,25V48A5,4 0 1 1 32,44V33L18,36V52A5,4 0 1 1 14,48Z", 2.4, 2)
    ic.path("M14,30L36,25V48A5,4 0 1 1 32,44V33L18,36V52A5,4 0 1 1 14,48Z", ic.lg([(0, "#5a5f68"), (1, "#141414")], 0, 0, 1, 1))
    ic.add('<path d="M15,31L35,26.5" stroke="#fff" stroke-opacity=".5" stroke-width="1"/>')


def e_picture(ic):
    ic.shadow(rrect(3, 30, 30, 25, 1.5), 2.4, 2)
    ic.path(rrect(3, 30, 30, 25, 1.5), ic.lg([(0, "#ffffff"), (1, "#d9dce0")]))
    ic.path("M6,33H30V48H6Z", ic.lg([(0, "#bfe8ff"), (1, "#4aa2e0")]), INK, .9)
    ic.path("M6,48V43L13,36L19,42L23,38L30,45V48Z", ic.lg([(0, "#9ee070"), (1, "#2f8a1e")]), INK, .8)
    ic.path(circle(24, 37.5, 2.6), ic.rg([(0, "#fff8c0"), (1, "#f0a810")]), INK, .7)


def e_film(ic):
    ic.add('<g transform="rotate(-24 18 44)">')
    ic.shadow("M-2,36H38V52H-2Z", 2.4, 2)
    ic.path("M-2,36H38V52H-2Z", ic.lg([(0, "#3a3f46"), (1, "#101214")]))
    for i in range(9):
        x = -0.5 + i * 4.4
        ic.add(f'<rect x="{x}" y="37.4" width="2.4" height="2" rx=".4" fill="#f4f4f4"/><rect x="{x}" y="48.6" width="2.4" height="2" rx=".4" fill="#f4f4f4"/>')
    for i in range(3):
        ic.path(f"M{1 + i * 12},40.6H{11 + i * 12}V47.4H{1 + i * 12}Z", ic.lg([(0, "#ffe9a8"), (1, "#d89a20")]), "#000", .5)
    ic.add("</g>")


def e_docs(ic):
    for i, dx in enumerate((0, 6)):
        x, y = 3 + dx, 28 + dx
        ic.shadow(f"M{x},{y}H{x + 17}L{x + 23},{y + 6}V{y + 26}H{x}Z", 2, 1.6)
        ic.path(f"M{x},{y}H{x + 17}L{x + 23},{y + 6}V{y + 26}H{x}Z", ic.lg([(0, "#ffffff"), (1, "#e2e4e8")]))
        ic.path(f"M{x + 17},{y}V{y + 6}H{x + 23}", "#d9dce0", INK, 1)
        for k in range(5):
            ic.add(f'<path d="M{x + 3.5},{y + 9 + k * 3.3}H{x + 19 - (k % 3) * 3}" stroke="#5a6470" stroke-width="1.1"/>')


def e_download(ic):
    d = "M12,28H24V40H31L18,54L5,40H12Z"
    ic.shadow(d, 2.4, 2)
    ic.path(d, ic.lg([(0, "#9ee070"), (.5, "#3fae2a"), (1, "#1e6a10")]))
    ic.add('<path d="M13.5,30H22.5" stroke="#fff" stroke-opacity=".6" stroke-width="1.3"/>')


def e_template(ic):
    ic.shadow("M3,30H24L30,36V56H3Z", 2, 1.6)
    ic.path("M3,30H24L30,36V56H3Z", ic.lg([(0, "#ffffff"), (1, "#e2e4e8")]))
    ic.path("M24,30V36H30", "#d9dce0", INK, 1)
    ic.add(f'<path d="M7,36H19M7,42H26M7,48H22" stroke="#3d9ad8" stroke-width="1.6" stroke-dasharray="2.2 1.4"/>')


def e_people(ic):
    for cx, col, dy in ((10, ("#9ee070", "#2f8a1e"), 0), (22, ("#9fd4ff", "#1a5c9e"), 3)):
        body = f"M{cx - 8},{55 + dy}C{cx - 8},{46 + dy} {cx - 4},{43 + dy} {cx},{43 + dy}C{cx + 4},{43 + dy} {cx + 8},{46 + dy} {cx + 8},{55 + dy}Z"
        ic.shadow(body + circle(cx, 37 + dy, 5), 2, 1.6)
        ic.path(body, ic.lg([(0, col[0]), (1, col[1])]))
        ic.path(circle(cx, 37 + dy, 5), ic.rg([(0, "#fff1e2"), (1, "#d89a6a")]))


def e_lock(ic):
    ic.add(f'<path d="M37,42V36.5A7,7 0 0 1 51,36.5V42" fill="none" stroke="{INK}" stroke-width="5"/>')
    ic.add(f'<path d="M37,42V36.5A7,7 0 0 1 51,36.5V42" fill="none" stroke="#c9ccd1" stroke-width="2.6"/>')
    ic.shadow(rrect(33, 41, 22, 17, 2), 2.4, 2)
    ic.path(rrect(33, 41, 22, 17, 2), ic.lg([(0, "#fff3a6"), (.5, "#e8c43a"), (1, "#8a6a06")], 0, 0, 1, 1))
    ic.path("M44,46A2.4,2.4 0 0 1 45.4,50.4V54H42.6V50.4A2.4,2.4 0 0 1 44,46Z", INK, None)


def e_desktop(ic):
    ic.shadow(rrect(2, 29, 32, 22, 2), 2.4, 2)
    ic.path(rrect(2, 29, 32, 22, 2), ic.lg([(0, "#eceef1"), (1, "#9aa0a8")]))
    ic.path("M5,32H31V46H5Z", ic.lg([(0, "#9fd4ff"), (1, "#1a5c9e")]), INK, .9)
    ic.path("M13,51H23L25,56H11Z", ic.lg([(0, "#c9ccd1"), (1, "#7b818a")]))
    for i, c in enumerate(("#e8c43a", "#d8573d", "#4fae5a")):
        ic.add(f'<rect x="{7 + i * 5}" y="35" width="3.4" height="3.4" fill="{c}" stroke="#000" stroke-width=".5"/>')


def e_share(ic):
    e_globe(ic, 1, 27, 14)
    # small "shared" badge on the globe
    ic.path(circle(29, 52, 6.2), ic.rg([(0, "#ffe2c0"), (.6, "#ec9a3a"), (1, "#ae5e10")]), INK, 1)
    ic.add('<path d="M25.6,52H32.2M30,49.6L32.6,52L30,54.4" fill="none" stroke="#fff" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>')


EMBLEM_ANCHOR_X = {"lock": 60}
EMBLEM = {"home": e_house, "globe": lambda ic: e_globe(ic), "music": e_speaker, "pictures": e_picture,
          "videos": e_film, "documents": e_docs, "download": e_download, "templates": e_template,
          "people": e_people, "lock": e_lock, "desktop": e_desktop, "share": e_share}


# =========================================================== other places
TRASH_STRAIGHT = True      # True: KDE Classic's straight-sided can (current); False: the earlier tapered can, kept on record


def trash(full=False, straight=None):
    """Isometric metal can as in KDE Classic: elliptical lid and rim seen from above,
    body tapered or straight-sided, ribs that wrap the cylinder (closer together toward the edges)."""
    straight = TRASH_STRAIGHT if straight is None else straight
    def f():
        ic = Icon()
        cx, top, bot = 32, 20.5, 58
        rt, rb, et, eb = 18.5, 14.6, 5.2, 4         # radii and ellipse heights, top and bottom
        if straight:
            rt, rb, et, eb = 17, 17, 5, 5
        body = (f"M{cx - rt},{top}L{cx - rb},{bot}A{rb},{eb} 0 0 0 {cx + rb},{bot}"
                f"L{cx + rt},{top}A{rt},{et} 0 0 1 {cx - rt},{top}Z")
        ic.shadow(body, 3.8, 3)
        metal = ic.lg([(0, "#6c727a"), (.14, "#d9dce0"), (.3, "#ffffff"), (.55, "#c9ccd1"), (.82, "#8a8f96"), (1, "#5c6168")], 0, 0, 1, 0)
        ic.path(body, metal)
        # ribs: positions follow the curve of the can
        n, span, gw = (5, 1.5, 3.4) if straight else (7, 1.64, 2.1)   # the straight can has KDE Classic's wider grooves
        for i in range(n):
            a = -span / 2 + i * (span / (n - 1))       # angle across the visible half
            u = math.sin(a)
            xt, xb = cx + u * (rt - 2.6), cx + u * (rb - 2.2)
            yt, yb = top + et * math.cos(a) + 2.4, bot + eb * math.cos(a) - 3
            w = gw * (.55 + .45 * math.cos(a))          # narrower toward the edges, where the can turns away
            ic.add(f'<path d="M{xt:.1f},{yt:.1f}L{xb:.1f},{yb:.1f}" stroke="#4c5158" stroke-opacity=".7" stroke-width="{w:.2f}" stroke-linecap="round"/>')
            ic.add(f'<path d="M{xt + w * .55:.1f},{yt:.1f}L{xb + w * .5:.1f},{yb:.1f}" stroke="#fff" stroke-opacity=".75" stroke-width=".8" stroke-linecap="round"/>')
        lid_side = ic.lg([(0, "#7b818a"), (.3, "#f2f3f5"), (.6, "#c3c7cd"), (1, "#6c727a")], 0, 0, 1, 0)
        lid_top = ic.rg([(0, "#ffffff"), (.6, "#dfe2e6"), (1, "#9aa0a8")], .4, .3, .8)

        def lid(y, rx=20, ry=5.8, thick=2.6):
            ic.path(f"M{cx - rx},{y}V{y + thick}A{rx},{ry} 0 0 0 {cx + rx},{y + thick}V{y}Z", lid_side)
            ic.path(f"M{cx - rx},{y}A{rx},{ry} 0 0 1 {cx + rx},{y}A{rx},{ry} 0 0 1 {cx - rx},{y}Z", lid_top)
            ic.add(f'<path d="M{cx - rx + 3},{y - .6}A{rx - 3},{ry - 1.8} 0 0 1 {cx + rx - 6},{y - 3.6}" fill="none" stroke="#fff" stroke-width="1.1" stroke-opacity=".9"/>')
            # loop handle standing on the lid
            h = f"M{cx - 4.4},{y + .6}V{y - 3.4}Q{cx - 4.4},{y - 6.8} {cx},{y - 6.8}Q{cx + 4.4},{y - 6.8} {cx + 4.4},{y - 3.4}V{y + .6}"
            ic.add(f'<path d="{h}" fill="none" stroke="{INK}" stroke-width="4.2" stroke-linecap="round"/>')
            ic.add(f'<path d="{h}" fill="none" stroke="#e8eaed" stroke-width="1.8" stroke-linecap="round"/>')

        if full:
            # rim and dark opening, papers spilling out, lid tipped back
            ic.path(f"M{cx - rt},{top}A{rt},{et} 0 0 1 {cx + rt},{top}A{rt},{et} 0 0 1 {cx - rt},{top}Z", "#3c4148")
            for px, py, r, c, rot in ((23, 19, 7, "#ffffff", 0), (40.5, 18.5, 7.4, "#fff6d8", 40), (31.5, 13.5, 7, "#e8f4ff", 75)):
                pts = []
                for k in range(9):
                    a_ = math.radians(rot + k * 40)
                    rr = r * (1 if k % 2 == 0 else .78)
                    pts.append(f"{px + rr * math.cos(a_):.1f},{py + rr * math.sin(a_):.1f}")
                ic.path("M" + " L".join(pts) + "Z", ic.lg([(0, "#ffffff"), (1, c)], 0, 0, 1, 1), INK, 1)
                ic.add(f'<path d="M{px - r * .6:.1f},{py - r * .2:.1f}L{px:.1f},{py + r * .15:.1f}L{px + r * .5:.1f},{py - r * .45:.1f}" fill="none" stroke="#9aa0a8" stroke-width=".8"/>')
            ic.add(f'<g transform="rotate(-20 {cx - 20} 17) translate(1,3)">')
            lid(14.5)
            ic.add("</g>")
        else:
            lid(top - 1.6)
        return ic
    return f


def desktop():
    """Drafting desk in perspective with a desk lamp and a pencil (KDE Classic 'desktop')."""
    ic = Icon()
    frame = "M4,40L30,25L60,40L34,56Z"
    ic.shadow(frame + "M4,40V44L34,60V56Z", 3, 2.4)
    ic.path("M4,40V44L34,60V56Z", ic.lg([(0, "#9aa0a8"), (1, "#4c5158")]))
    ic.path("M34,56V60L60,44V40Z", ic.lg([(0, "#c3c7cd"), (1, "#6c727a")]))
    ic.path(frame, ic.lg([(0, "#eceef1"), (1, "#9aa0a8")], 0, 0, 1, 1))
    ic.path("M10,40L30,28.6L54,40L34,51.6Z", ic.lg([(0, "#ffffff"), (.55, "#fbf3ea"), (1, "#f0b47c")], 0, 0, 1, 1), INK, .9)
    # desk lamp: round base, two-part jointed arm, bell shade aimed down at the desk
    ic.path("M21.5,29.6A6.5,3 0 0 1 34.5,29.6A6.5,3 0 0 1 21.5,29.6Z", ic.lg([(0, "#d9dce0"), (1, "#5c6168")]), INK, .9)
    arm = "M28,29V24L22.5,13.5L33,7.5"
    ic.add(f'<path d="{arm}" fill="none" stroke="{INK}" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/>')
    ic.add(f'<path d="{arm}" fill="none" stroke="#b4b9c0" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>')
    ic.path(circle(22.5, 13.5, 1.8), "#8a8f96", INK, .8)
    # light falling on the desk
    ic.add('<path d="M34.5,11.5L44,15.5L48,34L35.5,34Z" fill="#fff6c0" fill-opacity=".35"/>')
    ic.add('<g transform="translate(36,9.5) rotate(-38)">')
    ic.path("M-2.6,-3.4H2.6L7,7A7,2.4 0 0 1 -7,7Z", ic.lg([(0, "#ffffff"), (.35, "#aab0b8"), (1, "#4c5158")], 0, 0, 1, 0))
    ic.path("M-7,7A7,2.4 0 0 1 7,7A7,2.4 0 0 1 -7,7Z", ic.rg([(0, "#ffffe8"), (.6, "#fff0a0"), (1, "#d8b440")], .5, .5, .6), INK, .9)
    ic.path("M-2.6,-3.4A2.6,1 0 0 1 2.6,-3.4", "none", INK, 1)
    ic.add("</g>")
    ic.add('<g transform="rotate(-8 42 42)">')
    ic.path("M40,30H44V46H40Z", ic.lg([(0, "#ffb070"), (.5, "#f07a1a"), (1, "#a84a08")], 0, 0, 1, 0), INK, .9)
    ic.path("M40,46L42,50.5L44,46Z", "#f3d3a2", INK, .8)
    ic.add("</g>")
    ic.path(circle(52, 36.5, 2.6), ic.rg([(0, "#fff6a0"), (1, "#a8840e")]), INK, .8)
    return ic


def plain_globe():
    """The KDE Classic globe on its own: the web and online services."""
    ic = Icon()
    e_globe(ic, 6, 6, 24)
    return ic


def network():
    """Network (workgroups, shared folders): KDE Classic's globe on a network junction with two plugs, so it reads
    as a local network rather than the web."""
    ic = Icon()
    d = "M32,40V52M8,52H56"
    ic.add(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>')
    ic.add(f'<path d="{d}" fill="none" stroke="#f0a020" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/>')
    e_globe(ic, 12, 2, 20)
    for x in (8, 56):
        ic.path(rrect(x - 4, 48, 8, 8, 1.4), ic.lg([(0, "#ffffff"), (1, "#a8adb4")], 0, 0, 1, 1), INK, 1.1)
    ic.path(circle(32, 52, 4.5), ic.rg([(0, "#fffbe0"), (.5, "#b8a860"), (1, "#5a5020")], .4, .35, .8), INK, 1.2)
    return ic


def computer():
    ic = Icon()
    ic.add("<g>")
    ic.shadow("M6,6H54V44H6Z M10,46H50V58H10Z", 3.2, 2.6)
    ic.path(rrect(10, 46, 40, 11, 1.6), ic.lg([(0, "#f4f1e8"), (1, "#a8a497")]))
    ic.add(f'<path d="M14,52H30M38,50.5H44" stroke="#5c6168" stroke-width="1.6"/>')
    ic.path(circle(46, 53, 1.4), "#4fae5a", INK, .6)
    ic.path("M24,43H36L38,47H22Z", ic.lg([(0, "#d9d5c8"), (1, "#8a877c")]))
    ic.path(rrect(6, 5, 48, 39, 3), ic.lg([(0, "#fbf9f2"), (1, "#b4b0a3")]))
    ic.path(rrect(10.5, 9.5, 39, 29, 1.6), ic.lg([(0, "#3a6fd8"), (.6, "#1a3ea8"), (1, "#0c2470")]))
    ic.add('<path d="M12,11.5H48V22C36,26 24,27 12,26Z" fill="#fff" fill-opacity=".22"/>')
    ic.add("</g>")
    return ic


# =========================================================== registry
ICONS = {
    "places": {
        "folder": make_folder(), "folder-open": make_folder(open_=True),
        "user-home": make_folder(emblem="home"), "user-desktop": desktop,
        "folder-documents": make_folder(emblem="documents"), "folder-download": make_folder(emblem="download"),
        "folder-music": make_folder(emblem="music"), "folder-pictures": make_folder(emblem="pictures"),
        "folder-videos": make_folder(emblem="videos"), "folder-templates": make_folder(emblem="templates"),
        "folder-publicshare": make_folder(emblem="share"), "folder-remote": make_folder(emblem="globe"),
        "folder-locked": make_folder(emblem="lock"),
        **{f"folder-{c}": make_folder(c) for c in BAND if c != "blue"},
        "folder-blue": make_folder("blue"),
        "user-trash": trash(False), "user-trash-full": trash(True), "network-workgroup": network, "globe": plain_globe,
    },
    "devices": {"computer": computer},
}

ALIASES = {
    "places": {"inode-directory": "folder", "folder-home": "user-home", "folder-desktop": "user-desktop",
               "folder-downloads": "folder-download", "folder-image": "folder-pictures", "folder-picture": "folder-pictures",
               "folder-images": "folder-pictures", "folder-video": "folder-videos", "folder-sound": "folder-music",
               "folder-network": "folder-remote", "folder-public": "folder-publicshare", "folder-gray": "folder-grey",
               "folder-purple": "folder-violet", "trash-empty": "user-trash"},
    "devices": {"video-display": "computer", "computer-laptop": "computer"},
}

# icons that get a dedicated small-size drawing (others scale the 64 px one)
SMALL_DRAWN = {n for n in ICONS["places"] if n.startswith(("folder", "user-home"))}

INDEX = """[Icon Theme]
Name=KDE Modern Classic
Comment=A modern take on the KDE 2/3 Classic icons, drawn as SVG
Inherits=kdeclassic,breeze,hicolor
Example=folder
DisplayDepth=32
Directories=16x16/places,22x22/places,16x16/mimetypes,22x22/mimetypes,16x16/actions,22x22/actions,scalable/places,scalable/devices,scalable/mimetypes,scalable/actions,scalable/apps,scalable/emblems,scalable/status

[16x16/places]
Size=16
Context=Places
Type=Fixed

[22x22/places]
Size=22
Context=Places
Type=Fixed

[16x16/mimetypes]
Size=16
Context=MimeTypes
Type=Fixed

[22x22/mimetypes]
Size=22
Context=MimeTypes
Type=Fixed

[16x16/actions]
Size=16
Context=Actions
Type=Fixed

[22x22/actions]
Size=22
Context=Actions
Type=Fixed

[scalable/places]
Size=64
Context=Places
Type=Scalable
MinSize=8
MaxSize=512

[scalable/devices]
Size=64
Context=Devices
Type=Scalable
MinSize=8
MaxSize=512

[scalable/mimetypes]
Size=64
Context=MimeTypes
Type=Scalable
MinSize=8
MaxSize=512

[scalable/actions]
Size=64
Context=Actions
Type=Scalable
MinSize=8
MaxSize=512

[scalable/status]
Size=64
Context=Status
Type=Scalable
MinSize=8
MaxSize=512

[scalable/emblems]
Size=64
Context=Emblems
Type=Scalable
MinSize=8
MaxSize=512

[scalable/apps]
Size=64
Context=Applications
Type=Scalable
MinSize=8
MaxSize=512
"""


def main():
    global SMALL
    from devices import DEVICES, DEVICE_ALIASES
    from filetypes import MIMES, MIME_ALIASES
    ICONS["devices"].update(DEVICES)
    ALIASES["devices"].update(DEVICE_ALIASES)
    ICONS["mimetypes"] = MIMES
    ALIASES["mimetypes"] = MIME_ALIASES
    from dolphin import FOLDERS, FOLDER_EMBLEMS, FOLDER_ALIASES, FOLDER_EMBLEM_ANCHORS
    EMBLEM.update(FOLDER_EMBLEMS)
    EMBLEM_ANCHOR_X.update(FOLDER_EMBLEM_ANCHORS)
    for name, (colour, emblem) in FOLDERS.items():
        ICONS["places"][name] = make_folder(colour, emblem)
        SMALL_DRAWN.add(name)
    ALIASES["places"].update(FOLDER_ALIASES)
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    n = 0
    for ctx, d in ICONS.items():
        for sub, small in (("scalable", False), ("22x22", True), ("16x16", True)):
            os.makedirs(f"{OUT}/{sub}/{ctx}", exist_ok=True)
            SMALL = small
            for name, fn in d.items():
                if small and name not in SMALL_DRAWN:
                    continue
                open(f"{OUT}/{sub}/{ctx}/{name}.svg", "w").write(fn().svg(16 if sub == "16x16" else 22 if small else 64))
                n += sub == "scalable"
        SMALL = False
    for ctx, d in ALIASES.items():
        for sub in ("scalable", "22x22", "16x16"):
            for a, t in d.items():
                if os.path.exists(f"{OUT}/{sub}/{ctx}/{t}.svg"):
                    os.symlink(f"{t}.svg", f"{OUT}/{sub}/{ctx}/{a}.svg")
    from filetypes import write_small
    write_small(OUT)
    import session
    session.write(OUT)
    from filetypes import write_apps
    write_apps(OUT)
    import settings
    settings.write(OUT)
    import dolphin
    dolphin.write(OUT)
    import discover
    discover.write(OUT)
    import shell
    shell.write(OUT)
    import weather
    weather.write(OUT)
    import systray
    systray.write(OUT)
    import mobile
    mobile.write(OUT)
    import actions
    actions.write(OUT)
    import uitrace
    uitrace.write(OUT)
    import settingstrace
    settingstrace.write(OUT)
    import desktoptrace
    desktoptrace.write(OUT)
    import traytrace
    traytrace.write(OUT)
    import leftovers
    leftovers.write(OUT)
    import ark
    ark.write(OUT)
    import kdeapps
    kdeapps.write(OUT)
    import okular
    okular.write(OUT)
    import kate
    kate.write(OUT)
    import elisa
    elisa.write(OUT)
    import odds
    odds.write(OUT)
    import pim
    pim.write(OUT)
    import updates
    updates.write(OUT)
    import apps2
    apps2.write(OUT)
    import qbittorrent
    qbittorrent.write(OUT)
    broken = [os.path.join(dp, f) for dp, dn, fn in os.walk(OUT) for f in fn
              if os.path.islink(os.path.join(dp, f)) and not os.path.exists(os.path.join(dp, f))]
    if broken:
        print("BROKEN LINKS:", broken)
    open(f"{OUT}/index.theme", "w").write(INDEX)
    print(n, "icons")


if __name__ == "__main__":
    main()
