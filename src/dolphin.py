"""KDE Classic Vector: Dolphin file manager icons (app icons, folder variants, view controls,
selection actions, version-control and status emblems)."""
import json, math, os
from gen import Icon, INK, LW, circle, rrect

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, "traced", "dolphin.json")))["dolphin"]


# ------------------------------------------------------------------ app icons
def dolphin(ic):
    """Dolphin: the leaping blue dolphin of KDE Classic, traced from the original."""
    t="translate(32,33) scale(.9) translate(-32,-32)"
    ic.shadow(D,2.6,2.2,transform=t)
    ic.add(f'<g transform="{t}">')
    ic.path(D, ic.lg([(0,"#c8e8ff"),(.3,"#5aa6ea"),(.7,"#2a72c8"),(1,"#123e86")],0,0,.4,1), INK, 1.5)
    ic.add('<path d="M47.5,38.6Q54,42 60.5,47.2" fill="none" stroke="#0c3070" stroke-width="1.1" stroke-linecap="round"/>')
    ic.add('<path d="M14,34Q22,22 36,20" fill="none" stroke="#fff" stroke-opacity=".75" stroke-width="2" stroke-linecap="round"/>')
    ic.add('<path d="M44,25.5Q50,30 52,36" fill="none" stroke="#fff" stroke-opacity=".45" stroke-width="1.4" stroke-linecap="round"/>')
    ic.add('</g>')

def cabinet(ic):
    """File manager: KDE Classic's grey filing cabinet, top drawer pulled out with coloured folders."""
    metal_side = ic.lg([(0, "#f4f5f6"), (1, "#9aa0a8")], 0, 0, 0, 1)
    ic.shadow("M5,6H34L45,12V60H16L5,54Z", 3, 2.6)
    ic.path("M5,6L16,12V60L5,54Z", metal_side, INK, 1.4)                      # left side
    ic.path("M5,6H34L45,12H16Z", ic.lg([(0, "#ffffff"), (1, "#c9ccd1")]), INK, 1.4)   # top
    ic.path("M16,12H45V60H16Z", ic.lg([(0, "#d9dce0"), (1, "#8a9098")], 0, 0, 1, 1), INK, 1.4)  # front
    ic.add('<path d="M6.5,8.4L15,13" stroke="#fff" stroke-width="1"/>')
    def handle(x, y, w=8):
        ic.add(f'<path d="M{x},{y - 1.2}V{y}H{x + w}V{y - 1.2}" fill="none" stroke="{INK}" stroke-width="1.6" stroke-linejoin="round"/>')
    for y0 in (31, 46):
        ic.path(f"M19,{y0}H42V{y0 + 12}H19Z", ic.lg([(0, "#eceef1"), (1, "#a8adb4")]), "#4c5158", 1.2)
        handle(26.5, y0 + 6.5)
    # top drawer, pulled straight out along the cabinet's depth line (back-left to front-right)
    ox, oy = 12, 6.55                                   # how far it is pulled out
    x0, x1, y0, y1 = 19, 42, 15, 29                     # the drawer slot in the cabinet front
    fx0, fx1, fy0, fy1 = x0 + ox, x1 + ox, y0 + oy, y1 + oy
    ic.path(f"M{x0},{y0}H{x1}V{y1}H{x0}Z", "#202328", "#4c5158", 1.2)                # dark slot behind
    # open top of the drawer: inner floor and back wall seen from above
    ic.path(f"M{x0},{y0}H{x1}L{fx1},{fy0}H{fx0}Z", ic.lg([(0, "#2c3036"), (1, "#5c6168")]), INK, 1)
    # hanging folders standing across the drawer, back to front; tops rise above the rim
    for col, f, h in (("#3ad03a", .2, 7.5), ("#e0281a", .45, 6.5), ("#ffc89a", .72, 5)):
        bx, by = x0 + ox * f, y0 + oy * f
        ic.path(f"M{bx + 1:.2f},{by:.2f}V{by - h:.2f}H{bx + 22:.2f}V{by:.2f}Z",
                ic.lg([(0, "#ffffff"), (.25, col), (1, col)], 0, 0, 0, 1), INK, .9)
    bx, by = x0 + ox * .45, y0 + oy * .45
    ic.path(f"M{bx + 15:.2f},{by - 6.5:.2f}Q{bx + 15:.2f},{by - 9.6:.2f} {bx + 18:.2f},{by - 9.6:.2f}Q{bx + 21:.2f},{by - 9.6:.2f} {bx + 21:.2f},{by - 6.5:.2f}Z",
            ic.lg([(0, "#b0ffb0"), (1, "#1aa01a")]), INK, .9)
    # left side wall of the drawer, running from the slot out to the drawer front
    ic.path(f"M{x0},{y0}L{fx0},{fy0}V{fy1}L{x0},{y1}Z", ic.lg([(0, "#eceef1"), (1, "#8a9098")]), INK, 1.2)
    ic.add(f'<path d="M{x0 + 1},{y0 + 1.6}L{fx0 - .6},{fy0 + 1}" stroke="#fff" stroke-width=".9"/>')
    # drawer front
    ic.path(f"M{fx0},{fy0}H{fx1}V{fy1}H{fx0}Z", ic.lg([(0, "#f4f5f6"), (1, "#a8adb4")]), INK, 1.4)
    handle(fx0 + 7.5, fy0 + 8)


# ------------------------------------------------------------------ folder emblems (lower left, as in gen.py)
def e_star(ic):
    """'New' starburst, yellow with a red edge, as on KDE Classic's folder_new."""
    pts = []
    for k in range(16):
        a = 2 * math.pi * k / 16 - math.pi / 2
        r = 14 if k % 2 == 0 else 6.5
        pts.append(f"{17 + r * math.cos(a):.2f},{43 + r * math.sin(a):.2f}")
    d = "M" + "L".join(pts) + "Z"
    ic.shadow(d, 2.2, 1.8)
    ic.path(d, ic.rg([(0, "#ffffff"), (.35, "#fff36a"), (1, "#e8a010")], .45, .45, .7), "#7a4404", 1.1)


def e_bookmark(ic):
    """KDE Classic bookmark: a grey ribbed strip with a notched tail, lying on the diagonal."""
    d = "M4,34L12,28L36,52L36,60L29,54L22,58Z"
    ic.shadow(d, 2.2, 1.8)
    ic.path(d, ic.lg([(0, "#ffffff"), (.5, "#a8adb4"), (1, "#5c6168")], 0, 0, 1, 0), INK, LW)
    for k in range(4):
        ic.add(f'<path d="M{12 + k * 4},{36 + k * 4}L{17 + k * 4},{32 + k * 4}" stroke="#5c6168" stroke-width="1.1"/>')


def e_cloud(ic):
    d = "M8,54A7,7 0 0 1 7,40A9,9 0 0 1 23,34A8,8 0 0 1 36,42A6,6 0 0 1 34,54Z"
    ic.shadow(d, 2.2, 1.8)
    ic.path(d, ic.lg([(0, "#ffffff"), (.6, "#e4f2ff"), (1, "#8ab8e8")]), INK, LW)
    ic.add('<path d="M10,41A7,7 0 0 1 22,37" fill="none" stroke="#fff" stroke-width="1.6" stroke-linecap="round"/>')


def e_gamepad(ic):
    d = "M10,38H30Q38,38 38,48Q38,58 32,58Q28,58 26,53H14Q12,58 8,58Q2,58 2,48Q2,38 10,38Z"
    ic.shadow(d, 2.2, 1.8)
    ic.path(d, ic.lg([(0, "#8a9098"), (1, "#2c3036")]), INK, LW)
    ic.add('<path d="M10,43V51M6,47H14" stroke="#e4e6e9" stroke-width="2.4" stroke-linecap="round"/>')
    for x, y, c in ((29, 44, "#e0281a"), (33, 48, "#3aa83a"), (25, 48, "#2a6ae0"), (29, 52, "#e8c43a")):
        ic.path(circle(x, y, 1.8), c, INK, .5)


def e_important(ic):
    ic.shadow(circle(17, 44, 13), 2.2, 1.8)
    ic.path(circle(17, 44, 13), ic.rg([(0, "#ffb0a0"), (.55, "#e0281a"), (1, "#7a0a04")], .4, .35, .75), INK, LW)
    ic.add('<path d="M17,36V46" stroke="#fff" stroke-width="3.6" stroke-linecap="round"/>')
    ic.path(circle(17, 51.5, 2), "#fff", None)


def e_mail(ic):
    ic.shadow("M2,36H34V56H2Z", 2.2, 1.8)
    ic.path("M2,36H34V56H2Z", ic.lg([(0, "#ffffff"), (1, "#d9dce0")]), INK, LW)
    ic.add(f'<path d="M2,36L18,48L34,36M2,56L14,45M34,56L22,45" fill="none" stroke="{INK}" stroke-width="1.1" stroke-linejoin="round"/>')
    ic.add('<path d="M26,39H31V44H26Z" fill="#e0281a" stroke="#7a0a04" stroke-width=".5"/>')


def e_cube(ic):
    """Stash: the isometric cardboard box of the archive file icons."""
    from filetypes import box
    box(ic)


def e_box(ic):
    """(unused) Stash: a taped cardboard box, as in KDE Classic's folder_tar."""
    front, side, top = "M2,38H24V58H2Z", "M24,38L34,32V52L24,58Z", "M2,38L12,32H34L24,38Z"
    ic.shadow(front + side + top, 2.2, 1.8)
    ic.path(side, ic.lg([(0, "#c8965c"), (1, "#7a4c1a")], 0, 0, 1, 0), INK, 1.1)
    ic.path(top, ic.lg([(0, "#fbe2b8"), (1, "#d8a868")]), INK, 1.1)
    ic.path(front, ic.lg([(0, "#f0cc94"), (1, "#b8803e")]), INK, 1.1)
    ic.add('<path d="M7,35L17,35M13,38V45" stroke="#e8d8a8" stroke-width="3"/>')
    ic.add('<path d="M5,49H14M5,52H11" stroke="#c84a4a" stroke-width="1"/>')


def e_clock(ic):
    """Temporary: a stopwatch."""
    ic.add(f'<path d="M15,30H21M18,30V33" stroke="{INK}" stroke-width="2.6" stroke-linecap="round"/>')
    ic.shadow(circle(18, 46, 13), 2.2, 1.8)
    ic.path(circle(18, 46, 13), ic.lg([(0, "#e4e6e9"), (1, "#6c727a")], 0, 0, 1, 1), INK, LW)
    ic.path(circle(18, 46, 10.4), ic.rg([(0, "#ffffff"), (1, "#e4e6e9")]), INK, .8)
    for k in range(12):
        a = 2 * math.pi * k / 12
        ic.add(f'<path d="M{18 + 8 * math.sin(a):.2f},{46 - 8 * math.cos(a):.2f}L{18 + 9.6 * math.sin(a):.2f},{46 - 9.6 * math.cos(a):.2f}" stroke="{INK}" stroke-width=".8"/>')
    ic.add(f'<path d="M18,46V39M18,46L23,49" stroke="{INK}" stroke-width="1.8" stroke-linecap="round"/>')
    ic.add('<path d="M18,46L13.5,41.5" stroke="#e0281a" stroke-width="1" stroke-linecap="round"/>')


def e_search(ic):
    a = math.radians(45)
    cx, cy, r = 15, 42, 9
    ic.add(f'<path d="M{cx + r * .8},{cy + r * .8}L{cx + r * .8 + 11},{cy + r * .8 + 11}" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>')
    ic.add(f'<path d="M{cx + r * .8},{cy + r * .8}L{cx + r * .8 + 11},{cy + r * .8 + 11}" stroke="#8a5a2a" stroke-width="4.6" stroke-linecap="round"/>')
    ic.shadow(circle(cx, cy, r + 2.4), 2, 1.6)
    ic.path(circle(cx, cy, r + 2.4), ic.lg([(0, "#ffffff"), (1, "#7b818a")], 0, 0, 1, 1), INK, LW)
    ic.path(circle(cx, cy, r), ic.rg([(0, "#e8f6ff"), (1, "#9ad0f0")], .35, .3, .8), INK, .9)
    ic.add(f'<path d="M{cx - 5},{cy - 1}Q{cx - 4.6},{cy - 5} {cx - 1},{cy - 5.4}" fill="none" stroke="#fff" stroke-width="1.6" stroke-linecap="round"/>')


def e_plus(ic):
    """Add: a glossy green badge with a white plus, in the lower right corner."""
    ic.shadow(circle(47, 47, 11), 2, 1.8)
    ic.path(circle(47, 47, 11), ic.rg([(0, "#c8f8a8"), (.55, "#3fae2a"), (1, "#145a0c")], .4, .32, .8), INK, 1.4)
    ic.add('<path d="M39,43Q40,37 47,36.5Q54,37 55,43Q47,46 39,43Z" fill="#fff" fill-opacity=".32"/>')
    ic.add('<path d="M47,41V53M41,47H53" stroke="#000" stroke-opacity=".3" stroke-width="5.2" stroke-linecap="round"/>')
    ic.add('<path d="M47,41V53M41,47H53" stroke="#fff" stroke-width="3.4" stroke-linecap="round"/>')


def e_recent(ic):
    """Recent: a small clock with a green arrow curling back round it."""
    ic.add(f'<path d="M5,44A13,13 0 1 0 9,34" fill="none" stroke="{INK}" stroke-width="5.4" stroke-linecap="round"/>')
    ic.add('<path d="M5,44A13,13 0 1 0 9,34" fill="none" stroke="#3fae2a" stroke-width="3.2" stroke-linecap="round"/>')
    ic.path("M3,30L12,31L7,38Z", ic.lg([(0, "#c8f8a8"), (1, "#1e7a10")]), INK, 1)
    ic.path(circle(18, 44, 9), ic.rg([(0, "#ffffff"), (1, "#e4e6e9")]), INK, 1.2)
    ic.add(f'<path d="M18,44V38.5M18,44L22,46" stroke="{INK}" stroke-width="1.8" stroke-linecap="round"/>')


def e_drive(ic):
    """Root folder: a small hard disk drive."""
    ic.shadow(rrect(2, 36, 32, 18, 2), 2, 1.8)
    ic.path(rrect(2, 36, 32, 18, 2), ic.lg([(0, "#e4e6e9"), (1, "#6c727a")]), INK, 1.3)
    ic.path("M5,40H31V46H5Z", ic.lg([(0, "#5c6168"), (1, "#14171c")]), INK, .8)
    ic.path(circle(28, 50, 1.6), "#3ae03a", INK, .5)
    ic.add('<path d="M6,50H20" stroke="#5c6168" stroke-width="1.2"/>')


def e_ribbon(ic):
    """Bookmark: a red ribbon tucked into the folder, sticking up out of the top.
    Drawn in the folder's own frame (undoing the emblem scale) so it ends at the front panel's top edge."""
    import __main__
    k = 1.5 if getattr(__main__, "SMALL", False) else 1.2
    ic.add(f'<g transform="translate(0,64) scale({1 / k:.4f}) translate(0,-64)"><g transform="translate(6,0)">')
    x0, x1 = 31.4, 37.6               # over the pocket's top edge just right of its step
    y0, y1 = 18.4 + (x0 - 30) * .3, 18.4 + (x1 - 30) * .3
    d = f"M{x0},{y0:.2f}V1.5L{(x0 + x1) / 2},5.5L{x1},1.5V{y1:.2f}Z"     # V snipped into the end
    ic.add(f'<path d="{d}" fill="#000" fill-opacity=".18" transform="translate(1.8,0)"/>')
    ic.path(d, ic.lg([(0, "#ff8a8a"), (.45, "#d81a2a"), (1, "#7a0410")], 0, 0, 1, 0), INK, 1.3)
    ic.add(f'<path d="M{x0 + 2},4V{y0 - 1:.2f}" stroke="#fff" stroke-opacity=".55" stroke-width="1.4"/>')
    ic.add(f'<path d="M{x0},{y0:.2f}L{x1},{y1:.2f}" stroke="#000" stroke-opacity=".35" stroke-width="1.2"/>')
    ic.add("</g></g>")


# folder name -> (band colour, emblem key); emblems are added to gen.EMBLEM at build time
# Every folder emblem is fitted into the same 28 x 28 box in the lower right corner (the size of the
# house on user-home, placed where the padlock sits on folder-locked), so the overlays match across folders. Boxes are each drawing's own extent.
EMBLEM_BOX = (28, 29, 56, 57)       # lower right, scaled from the right edge like the padlock
_EXTENT = {"plus": (35.3, 35.3, 58.6, 58.6), "cloud": (0, 29.9, 41.7, 54.7), "games": (1.3, 37.3, 38.6, 58.6),
           "important": (3.3, 30.3, 30.6, 57.6), "mail": (1.3, 35.3, 34.6, 56.6), "stash": (8, 14, 44, 54), "sync": (0.4, 28.3, 33.5, 59.6), "recent": (2.3, 27.7, 33.6, 59.0), "root": (1.3, 35.3, 34.6, 54.6),
           "temp": (4.3, 28.7, 31.6, 59.6), "search": (2.9, 29.9, 36.6, 63.6),
           "print": (5.3, 3.0, 60.5, 52.8), "development": (2.3, 13.3, 42.6, 47.2)}


def _fit(fn, key, grow=1.0, dy=0.0):
    x0, y0, x1, y1 = _EXTENT[key]
    bx0, by0, bx1, by1 = EMBLEM_BOX
    k = min((bx1 - bx0) / (x1 - x0), (by1 - by0) / (y1 - y0)) * grow
    cx = (bx0 + bx1) / 2          # centred across the box, sitting on its bottom edge
    def f(ic):
        ic.add(f'<g transform="translate({cx:.2f},{by1 + dy}) scale({k:.4f}) translate({-(x0 + x1) / 2:.2f},{-y1:.2f})">')
        fn(ic)
        ic.add("</g>")
    return f


FOLDER_EMBLEM_ANCHORS = {k: 60 for k in ("new", "cloud", "games", "important", "mail", "stash", "temp", "search", "sync", "recent", "root",
                                          "print", "development")}


def e_printer(ic):
    from devices import printer
    printer(ic)


def e_console(ic):
    from filetypes import e_terminal
    e_terminal(ic)
FOLDER_EMBLEMS = {"new": _fit(e_plus, "plus", .9), "bookmark": e_ribbon, "cloud": _fit(e_cloud, "cloud"),
                  "games": _fit(e_gamepad, "games"), "important": _fit(e_important, "important", .9),
                  "mail": _fit(e_mail, "mail"), "stash": _fit(e_cube, "stash"), "temp": _fit(e_clock, "temp"),
                  "search": _fit(e_search, "search", .82, 2.5), "sync": _fit(lambda ic: e_sync(ic), "sync"),
                  "recent": _fit(e_recent, "recent"), "root": _fit(e_drive, "root"),
                  "print": _fit(e_printer, "print", 1.08), "development": _fit(e_console, "development")}
FOLDERS = {"folder-add": ("blue", "new"), "folder-bookmark": ("blue", "bookmark"), "folder-cloud": ("blue", "cloud"),
           "folder-games": ("blue", "games"), "folder-important": ("blue", "important"), "folder-mail": ("blue", "mail"),
           "folder-stash": ("blue", "stash"), "folder-temp": ("blue", "temp"), "folder-saved-search": ("blue", "search"),
           "folder-sync": ("blue", "sync"), "folder-recent": ("blue", "recent"), "folder-print": ("blue", "print"),
           "folder-development": ("blue", "development")}
# folder-root: KDE has long shown the root folder (/) as a plain red folder
FOLDER_ALIASES = {"folder-new": "folder-add", "folder-bookmarks": "folder-bookmark", "folder-favorites": "folder-bookmark",
                  "folder-tar": "folder-stash", "folder-tmp": "folder-temp", "folder-saved-search-symbolic": "folder-saved-search",
                  "folder-gdrive": "folder-cloud", "folder-dropbox": "folder-cloud", "folder-onedrive": "folder-cloud",
                  "folder-nextcloud": "folder-cloud", "folder-sync-symbolic": "folder-sync",
                  "folder-recent-symbolic": "folder-recent", "folder-root": "folder-red", "folder-root-symbolic": "folder-red",
                  "document-open-recent-folder": "folder-recent", "folder-owncloud": "folder-cloud", "folder-game": "folder-games"}


# ------------------------------------------------------------------ view controls (KDE Classic "view" pane:
# cream panel with a navy border; window-type views add the grey title bar of view-restore)
NAVY = "#0a1a80"
CREAM = ("#fffef4", "#fff4c4")


def pane(ic, x=7, y=9, w=50, h=46, shadow=True):
    d = f"M{x},{y}H{x + w}V{y + h}H{x}Z"
    if shadow:
        ic.shadow(d, 2.6, 2.2)
    ic.path(d, ic.lg([(0, CREAM[0]), (1, CREAM[1])], 0, 0, 1, 1), NAVY, 2.2)


def _mini_icon(ic, x, y, s, col):
    """A tiny folder-like tile used inside view panes."""
    ic.path(f"M{x},{y + s * .2}H{x + s * .4}L{x + s * .5},{y}H{x + s}V{y + s * .85}H{x}Z", ic.lg([(0, "#ffffff"), (.45, col), (1, col)]), INK, .8)


def view_icons(ic):
    pane(ic)
    cols = ("#3d9ad8", "#e8c43a", "#4fae5a", "#d8573d", "#9a62d8", "#3cc4d4", "#ec9a3a", "#3d9ad8", "#4fae5a")
    for k, c in enumerate(cols):
        r, q = divmod(k, 3)
        _mini_icon(ic, 12 + q * 15, 14 + r * 13.5, 10, c)


def view_details(ic):
    pane(ic)
    ic.path("M9,11H55V18H9Z", ic.lg([(0, "#e4e6e9"), (1, "#a8adb4")]), None)
    ic.add(f'<path d="M30,11V18M44,11V18" stroke="#6c727a" stroke-width=".8"/>')
    for k, c in enumerate(("#3d9ad8", "#e8c43a", "#4fae5a", "#d8573d", "#3d9ad8")):
        y = 21 + k * 6.6
        _mini_icon(ic, 11, y, 5.4, c)
        ic.add(f'<path d="M19,{y + 2.6}H{27 + (k % 2) * 2}M32,{y + 2.6}H41M46,{y + 2.6}H52" stroke="#3c4148" stroke-width="1.4"/>')


def view_tree(ic):
    pane(ic)
    rows = ((0, 13, "#3d9ad8"), (1, 21, "#3d9ad8"), (2, 29, "#e8c43a"), (2, 37, "#4fae5a"), (1, 45, "#3d9ad8"))
    ic.add(f'<path d="M14,19.5V48H18M14,24H18M23,27.5V40H27M23,32H27" fill="none" stroke="#6c727a" stroke-width="1.1"/>')
    for lvl, y, c in rows:
        x = 11 + lvl * 9
        _mini_icon(ic, x, y, 6.4, c)
        ic.add(f'<path d="M{x + 9},{y + 3}H{x + 24 - lvl * 2}" stroke="#3c4148" stroke-width="1.3"/>')


def view_split(ic):
    pane(ic)
    ic.path("M30.5,10H33.5V54H30.5Z", NAVY, None)
    for x0 in (11, 37):
        for k in range(4):
            ic.add(f'<path d="M{x0},{17 + k * 8}H{x0 + 14 - (k % 2) * 4}" stroke="#6c727a" stroke-width="1.4"/>')


def swap_panels(ic):
    view_split(ic)
    for sgn, y in ((1, 25), (-1, 39)):
        x0, x1 = (16, 48) if sgn > 0 else (48, 16)
        d = f"M{x0},{y}H{x1}M{x1 - sgn * 6},{y - 5}L{x1},{y}L{x1 - sgn * 6},{y + 5}"
        ic.add(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="5.6" stroke-linecap="round" stroke-linejoin="round"/>')
        ic.add(f'<path d="{d}" fill="none" stroke="{"#3fae2a" if sgn > 0 else "#3d9ad8"}" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>')


def _red_x(ic, cx, cy, r):
    d = f"M{cx - r},{cy - r}L{cx + r},{cy + r}M{cx + r},{cy - r}L{cx - r},{cy + r}"
    ic.add(f'<path d="{d}" stroke="#7a0a04" stroke-width="{r * .62:.2f}" stroke-linecap="round"/>')
    ic.add(f'<path d="{d}" stroke="#ec2a1a" stroke-width="{r * .38:.2f}" stroke-linecap="round"/>')


def view_left_close(ic):
    view_split(ic)
    ic.add('<path d="M8.5,10.5H30.5V53.5H8.5Z" fill="#000" fill-opacity=".08"/>')
    _red_x(ic, 19.5, 32, 8)


def view_right_close(ic):
    view_split(ic)
    ic.add('<path d="M33.5,10.5H55.5V53.5H33.5Z" fill="#000" fill-opacity=".08"/>')
    _red_x(ic, 44.5, 32, 8)


def view_sidetree(ic):
    pane(ic)
    ic.path("M8.5,10.5H24V53.5H8.5Z", ic.lg([(0, "#e8f0ff"), (1, "#b8ccf0")]), None)
    ic.path("M24,10V54", "none", NAVY, 2)
    ic.add(f'<path d="M12,18V38H15M12,25H15M12,31H15" fill="none" stroke="#5c6890" stroke-width="1"/>')
    for y in (14, 22, 28, 34):
        _mini_icon(ic, 12 if y == 14 else 16, y, 5, "#3d9ad8")
    for k, c in enumerate(("#3d9ad8", "#e8c43a", "#4fae5a", "#d8573d")):
        _mini_icon(ic, 29 + (k % 2) * 13, 15 + (k // 2) * 15, 9, c)


def view_sort(ic):
    """Sort: a blue A over a red Z with a black arrow, as in KDE Classic's sort icons."""
    for d, col in (("M10,28L18,8L26,28M13.2,20.4H22.8", "#2a3ae8"), ("M10,34H26L10,54H26", "#e0281a")):
        ic.add(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>')
        ic.add(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>')
    ic.add(f'<path d="M44,8V52M36,44L44,54L52,44" fill="none" stroke="{INK}" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/>')


def view_group(ic):
    pane(ic)
    for y0, c in ((12, "#3d9ad8"), (33, "#4fae5a")):
        ic.path(f"M10,{y0}H54V{y0 + 6}H10Z", ic.lg([(0, "#9fc8f0"), (1, "#3a6ac0")]), None)
        ic.add(f'<path d="M13,{y0 + 3}H28" stroke="#fff" stroke-width="1.6"/>')
        for k in range(2):
            y = y0 + 9 + k * 6
            _mini_icon(ic, 12, y, 5, c)
            ic.add(f'<path d="M20,{y + 2.4}H{40 - k * 6}" stroke="#3c4148" stroke-width="1.3"/>')


def view_choose(ic):
    """Choose view mode: the icon, details, tree and split panes as four small tiles."""
    for fn, (tx, ty) in ((view_icons, (0, 0)), (view_details, (31, 0)), (view_tree, (0, 31)), (view_split, (31, 31))):
        ic.add(f'<g transform="translate({tx},{ty}) scale(.5)">')
        fn(ic)
        ic.add("</g>")


def _eye(ic, open_=True):
    eye = "M4,32Q32,6 60,32Q32,58 4,32Z"
    ic.shadow(eye, 2.4, 2)
    ic.path(eye, ic.lg([(0, "#ffffff"), (1, "#d9dce0")]), INK, LW * 1.4)
    ic.path(circle(32, 32, 11), ic.rg([(0, "#9fd4ff"), (.6, "#2a6ac8"), (1, "#0e2e6a")], .4, .35, .8), INK, 1.2)
    ic.path(circle(32, 32, 5), INK, None)
    ic.path(circle(28.5, 28.5, 2.4), "#fff", None)
    if not open_:
        ic.add(f'<path d="M10,54L54,10" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>')
        ic.add('<path d="M10,54L54,10" stroke="#e0281a" stroke-width="4" stroke-linecap="round"/>')


def view_visible(ic):
    _eye(ic, True)


def view_hidden(ic):
    _eye(ic, False)


def view_presentation(ic):
    """Presentation: a projector screen on a tripod showing a little chart."""
    ic.add(f'<path d="M32,46V60M32,46L20,60M32,46L44,60" stroke="{INK}" stroke-width="2.4" stroke-linecap="round"/>')
    ic.shadow("M6,8H58V46H6Z", 2.6, 2.2)
    ic.path("M6,10H58V46H6Z", ic.lg([(0, "#ffffff"), (1, "#e4e6e9")]), INK, LW)
    ic.path(rrect(4, 5, 56, 6, 3), ic.lg([(0, "#c3c7cd"), (1, "#5c6168")]), INK, 1.2)
    for k, (h, c) in enumerate(((14, "#3d9ad8"), (22, "#4fae5a"), (10, "#e8c43a"), (26, "#d8573d"))):
        ic.path(f"M{14 + k * 10},{40 - h}H{21 + k * 10}V40H{14 + k * 10}Z", ic.lg([(0, "#ffffff"), (.4, c), (1, c)], 0, 0, 1, 0), INK, .9)
    ic.add(f'<path d="M11,40.5H53" stroke="{INK}" stroke-width="1.2"/>')


def view_more(ic):
    for x in (14, 32, 50):
        ic.shadow(circle(x, 32, 6), 1.8, 1.6)
        ic.path(circle(x, 32, 6), ic.rg([(0, "#ffffff"), (.5, "#8a9098"), (1, "#2c3036")], .4, .35, .8), INK, 1.2)


VIEW = {"view-list-icons": view_icons, "view-list-details": view_details, "view-list-tree": view_tree,
        "view-split-left-right": view_split, "swap-panels": swap_panels, "view-left-close": view_left_close,
        "view-right-close": view_right_close, "view-sidetree": view_sidetree, "view-sort": view_sort,
        "view-group": view_group, "view-choose": view_choose, "view-visible": view_visible, "view-hidden": view_hidden,
        "view-presentation": view_presentation, "view-more": view_more}
VIEW_ALIASES = {"view-more-symbolic": "view-more", "view-more-horizontal": "view-more", "view-list-icons-symbolic": "view-list-icons",
                "view-list-details-symbolic": "view-list-details", "view-list-tree-symbolic": "view-list-tree",
                "view-split-left-right-symbolic": "view-split-left-right", "hint": "view-visible", "visibility": "view-visible",
                "view-sort-symbolic": "view-sort", "view-group-symbolic": "view-group", "view-file-columns": "view-list-details",
                "view-list-text": "view-list-details", "view-list-compact": "view-list-icons", "show-hidden": "view-visible"}


# ------------------------------------------------------------------ selection and edit actions
SEL = ("#bcd4ff", "#3a6ac8")


def _marquee(ic, x, y, w, h):
    d = f"M{x},{y}H{x + w}V{y + h}H{x}Z"
    ic.add(f'<path d="{d}" fill="none" stroke="#fff" stroke-width="1.6"/>')
    ic.add(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="1.6" stroke-dasharray="3 2.4"/>')


def _sel_grid(ic, picked):
    pane(ic)
    cols = ("#3d9ad8", "#e8c43a", "#4fae5a", "#d8573d")
    for k, c in enumerate(cols):
        r, q = divmod(k, 2)
        x, y = 13 + q * 21, 14 + r * 20
        if k in picked:
            ic.path(rrect(x - 3, y - 3, 19, 18, 2), ic.lg([(0, SEL[0]), (1, SEL[1])]), "#1a3a8a", .9, ' fill-opacity=".85"')
        _mini_icon(ic, x, y, 13, c)


def select_all(ic):
    _sel_grid(ic, {0, 1, 2, 3})
    _marquee(ic, 7.5, 8.5, 49, 47)


def select_invert(ic):
    _sel_grid(ic, {1, 2})
    for x, y in ((10, 11), (31, 31)):
        ic.add(f'<path d="M{x},{y}H{x + 19}V{y + 18}H{x}Z" fill="none" stroke="#7b818a" stroke-width="1" stroke-dasharray="2 2"/>')


def select_text(ic):
    from filetypes import GLYPHS
    ic.shadow("M4,18H60V46H4Z", 2.4, 2)
    ic.path("M4,18H60V46H4Z", ic.lg([(0, "#ffffff"), (1, "#eceef1")]), INK, LW)
    ic.path("M18,23H42V41H18Z", ic.lg([(0, SEL[0]), (1, SEL[1])]), None)
    x = 9
    for ch in "text":
        g, w = GLYPHS[ch]
        col = "#ffffff" if 18 < x + 1 < 42 else "#2c3036"
        ic.add(f'<g transform="translate({x:.2f},37) scale(1.7)"><path d="{g}" fill="none" stroke="{col}" stroke-width="1.1" stroke-linecap="round" stroke-linejoin="round"/></g>')
        x += (w + 1.6) * 1.7
    ic.add(f'<path d="M50,14V50M46.5,14H53.5M46.5,50H53.5" stroke="{INK}" stroke-width="2.2" stroke-linecap="round"/>')


def _clear_field(ic, rtl=False):
    ic.add('<g transform="translate(64,0) scale(-1,1)">' if rtl else "<g>")
    ic.shadow("M4,16H60V48H4Z", 2.4, 2)
    ic.path("M4,16H60V48H4Z", ic.lg([(0, "#ffffff"), (1, "#eceef1")]), INK, LW * 1.4)
    ic.add(f'<path d="M10,24V40" stroke="{INK}" stroke-width="3"/>')
    key = "M24,32L34,22H56V42H34Z"
    ic.path(key, ic.lg([(0, "#ffb0a0"), (.5, "#e0281a"), (1, "#7a0a04")]), INK, 1.4)
    ic.add('<path d="M40,27L49,37M49,27L40,37" stroke="#fff" stroke-width="3" stroke-linecap="round"/>')
    ic.add("</g>")


def clear_ltr(ic):
    _clear_field(ic)


def clear_rtl(ic):
    _clear_field(ic, True)


def edit_reset(ic):
    """Reset to defaults: an amber arrow curling back round to the dot it started from."""
    d = "M44,44A17,17 0 1 0 20,44"
    ic.add(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>')
    ic.add(f'<path d="{d}" fill="none" stroke="#e8a010" stroke-width="5.6" stroke-linecap="round"/>')
    ic.path("M27,51L23.6,37.6L13.4,47.8Z", ic.lg([(0, "#ffd890"), (1, "#a86404")]), INK, 1.4)
    ic.path(circle(44, 44, 5), ic.rg([(0, "#ffffff"), (1, "#c8301a")], .4, .35, .8), INK, 1.2)


def list_add(ic):
    """Add (list-add, add, value-increase): the green plus badge, as on emblem-added (2026-10-27). The old dark
    plus read poorly on dark colour schemes; it is kept as list_add_dark() and alt/list-add-dark.svg in case
    users prefer it."""
    vcs_added(ic)


def list_add_dark(ic):
    """The previous Add icon: a black plus (kept on record, not built)."""
    d = "M26,8H38V26H56V38H38V56H26V38H8V26H26Z"
    ic.shadow(d, 2.4, 2)
    ic.path(d, ic.lg([(0, "#4c5158"), (1, "#0a0c10")], 0, 0, 1, 1), INK, LW)
    ic.add('<path d="M28,11V27M11,28H27" stroke="#fff" stroke-opacity=".45" stroke-width="1.4"/>')


def edit_rename(ic):
    """Rename: a name label with an I-beam cursor, and the classic orange pencil."""
    ic.shadow("M3,22H50V44H3Z", 2.4, 2)
    ic.path("M3,22H50V44H3Z", ic.lg([(0, "#ffffff"), (1, "#eceef1")]), INK, LW)
    ic.path("M7,27H30V39H7Z", ic.lg([(0, SEL[0]), (1, SEL[1])]), None)
    ic.add('<path d="M10,35H27M10,31H22" stroke="#fff" stroke-width="2"/>')
    ic.add(f'<path d="M33,25V41" stroke="{INK}" stroke-width="1.8"/>')
    ic.add('<g transform="rotate(45 44 32)">')
    ic.path("M38,6H50V48L44,58L38,48Z", ic.lg([(0, "#ffd08a"), (.5, "#f08a1a"), (1, "#a84c04")], 0, 0, 1, 0), INK, 1.3)
    ic.path("M38,48L44,58L50,48Z", "#f4d8b0", INK, 1)
    ic.path("M42.4,54.4L44,58L45.6,54.4Z", INK, None)
    ic.path("M38,4Q38,1 41,1H47Q50,1 50,4V8H38Z", "#ff8aa0", INK, 1)
    ic.add("</g>")


def window_close(ic):
    """Close window: a small window, KDE Classic grey title bar, red cross on cream."""
    ic.shadow("M6,8H58V56H6Z", 2.6, 2.2)
    ic.path("M6,8H58V56H6Z", ic.lg([(0, CREAM[0]), (1, CREAM[1])], 0, 0, 1, 1), INK, LW * 1.3)
    ic.path("M6,8H58V18H6Z", ic.lg([(0, "#e4e6e9"), (1, "#8a9098")]), INK, LW * 1.3)
    ic.path(rrect(47, 10, 8, 6, 1), "#e0281a", INK, .8)
    _red_x(ic, 32, 37, 11)


def copy_path(ic):
    """Copy location: the copy pages with a blue path bar across them."""
    for x, y in ((6, 6), (20, 14)):
        d = f"M{x},{y}H{x + 26}L{x + 34},{y + 8}V{y + 42}H{x}Z"
        ic.shadow(d, 2.2, 1.8)
        ic.path(d, ic.lg([(0, "#ffffff"), (1, "#e2e4e8")]), INK, LW)
        ic.path(f"M{x + 26},{y}V{y + 8}H{x + 34}", "#d9dce0", INK, 1)
        for k in range(6):
            ic.add(f'<path d="M{x + 4},{y + 14 + k * 4.4}H{x + 28 - (k % 3) * 5}" stroke="#7b818a" stroke-width="1.1"/>')
    ic.shadow(rrect(4, 40, 56, 14, 3), 2, 1.6)
    ic.path(rrect(4, 40, 56, 14, 3), ic.lg([(0, "#9fd4ff"), (1, "#1a5c9e")]), INK, 1.3)
    ic.add('<path d="M10,51L14,43M22,51L26,43M34,51L38,43" stroke="#fff" stroke-width="2.2" stroke-linecap="round"/>')
    ic.add('<path d="M15.5,47H20M27.5,47H32M39.5,47H54" stroke="#fff" stroke-width="2.2" stroke-linecap="round"/>')


EDIT = {"edit-select-all": select_all, "edit-select-invert": select_invert, "edit-select-text": select_text,
        "edit-clear-locationbar-ltr": clear_ltr, "edit-clear-locationbar-rtl": clear_rtl, "edit-reset": edit_reset,
        "list-add": list_add, "edit-rename": edit_rename, "window-close": window_close, "edit-copy-path": copy_path}
EDIT_ALIASES = {"edit-select-all-symbolic": "edit-select-all", "edit-select-invert-symbolic": "edit-select-invert",
                "edit-select-none": "edit-select-invert", "edit-clear-locationbar": "edit-clear-locationbar-ltr",
                "edit-undo-history": "edit-reset", "list-add-symbolic": "list-add", "add": "list-add",
                "edit-rename-symbolic": "edit-rename",
                "edit-copy-path-symbolic": "edit-copy-path"}


# ------------------------------------------------------------------ version-control and status emblems
# Glossy round badges in the classic emblem style; Dolphin draws them over a corner of the file icon,
# so the symbol is bold and the edge dark enough to hold up at 8-12 px.
BADGE = {"green": ("#c8f8a8", "#3fae2a", "#145a0c"), "red": ("#ffb0a0", "#e0281a", "#6a0804"),
         "amber": ("#ffe8a0", "#ec9a1a", "#7a4404"), "blue": ("#b8dcff", "#2a6ac8", "#0c2a6a"),
         "grey": ("#ffffff", "#9aa0a8", "#3c4148")}


def badge(ic, colour, glyph, filled=True, w=7):
    c = BADGE[colour]
    o = circle(32, 32, 27)
    ic.shadow(o, 2, 1.8)
    if filled:
        ic.path(o, ic.rg([(0, c[0]), (.55, c[1]), (1, c[2])], .4, .32, .8), INK, 2.6)
        ic.add('<path d="M12,26Q14,9 32,8Q50,9 52,26Q32,33 12,26Z" fill="#fff" fill-opacity=".32"/>')
        stroke = "#fff"
    else:
        ic.path(o, "#ffffff", INK, 2.6)
        ic.path(circle(32, 32, 23.5), "none", c[1], 4.4)
        stroke = c[2]
    ic.add(f'<path d="{glyph}" fill="none" stroke="#000" stroke-opacity=".3" stroke-width="{w + 2.4}" stroke-linecap="round" stroke-linejoin="round"/>')
    ic.add(f'<path d="{glyph}" fill="none" stroke="{stroke}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')


TICK, PLUS, MINUS = "M19,33L28,42L45,23", "M32,17V47M17,32H47", "M17,32H47"
DOWN, BANG = "M32,16V45M21,35L32,46L43,35", "M32,15V34M32,46V46.5"
PENCIL = "M21,43L41,23M37,19L45,27M21,43L19,45"


def vcs_normal(ic): badge(ic, "green", TICK)
def vcs_added(ic): badge(ic, "green", PLUS)
def vcs_removed(ic): badge(ic, "red", MINUS)
def _pencil_badge(ic, filled):
    badge(ic, "amber", "", filled)
    col = "#ffffff" if filled else BADGE["amber"][2]
    d = "M28.5,12H35.5V39L32,48L28.5,39Z"
    ic.add(f'<g transform="rotate(45 32 31)"><path d="{d}" fill="{col}" stroke="#000" stroke-opacity=".3" stroke-width="2.4" stroke-linejoin="round"/>'
           f'<path d="{d}" fill="{col}"/><path d="M28.5,18H35.5" stroke="{BADGE["amber"][1] if filled else "#fff"}" stroke-width="1.6"/></g>')


def vcs_modified(ic): _pencil_badge(ic, True)
def vcs_unstaged(ic): _pencil_badge(ic, False)
def vcs_update(ic): badge(ic, "blue", DOWN)
def emblem_important(ic): badge(ic, "red", BANG)


def vcs_conflict(ic):
    """Conflicting: a red warning triangle, two changes colliding."""
    t = "M32,4L61,56H3Z"
    ic.shadow(t, 2, 1.8)
    ic.path(t, ic.lg([(0, "#ffb0a0"), (.5, "#e0281a"), (1, "#6a0804")]), INK, 2.6)
    ic.add('<path d="M32,21V36M32,47V47.5" fill="none" stroke="#000" stroke-opacity=".3" stroke-width="9.4" stroke-linecap="round"/>')
    ic.add('<path d="M32,21V36M32,47V47.5" fill="none" stroke="#fff" stroke-width="7" stroke-linecap="round"/>')


def _padlock(ic, open_):
    """KDE Classic's encrypted / decrypted padlock: brass body, silver band, steel shackle."""
    shackle = {False: "M20,30V20A12,12 0 0 1 44,20V30", True: "M40,30V16A12,12 0 0 1 64,16V22",
               "half": "M20,23V12A12,12 0 0 1 44,12V30"}[open_]       # "half": lifted, one leg out (security-medium)
    if open_ is True:
        ic.add('<g transform="translate(-6,0)">')
    ic.add(f'<path d="{shackle}" fill="none" stroke="{INK}" stroke-width="9"/>')
    ic.add(f'<path d="{shackle}" fill="none" stroke="url(#steel)" stroke-width="5.6"/>')
    ic.defs.append('<linearGradient id="steel" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#6c727a"/>'
                   '<stop offset=".35" stop-color="#ffffff"/><stop offset=".7" stop-color="#a8adb4"/><stop offset="1" stop-color="#4c5158"/></linearGradient>')
    body = rrect(12, 28, 40, 32, 4)
    ic.shadow(body, 2.4, 2)
    ic.path(body, ic.lg([(0, "#5a5430"), (.25, "#c8bc78"), (.45, "#f0e8b0"), (.75, "#9a9050"), (1, "#3e3a1c")], 0, 0, 1, 0), INK, LW * 1.4)
    ic.path("M12,38H52V48H12Z", ic.lg([(0, "#8a9098"), (.4, "#ffffff"), (1, "#7b818a")]), INK, 1)
    ic.path("M32,40.4A2.6,2.6 0 0 1 33.6,45V47.6H30.4V45A2.6,2.6 0 0 1 32,40.4Z", INK, None)
    if open_ is True:
        ic.add("</g>")


def locked(ic): _padlock(ic, False)
def unlocked(ic): _padlock(ic, True)


def starred(ic):
    pts = []
    for k in range(10):
        a = 2 * math.pi * k / 10 - math.pi / 2
        r = 28 if k % 2 == 0 else 12
        pts.append(f"{32 + r * math.cos(a):.2f},{34 + r * math.sin(a):.2f}")
    d = "M" + "L".join(pts) + "Z"
    ic.shadow(d, 2.2, 1.8)
    ic.path(d, ic.rg([(0, "#fffbe0"), (.45, "#ffd21a"), (1, "#c87a04")], .45, .4, .7), INK, 2)


def change_date(ic):
    """Change date: a calendar page with the red header, one day circled."""
    ic.shadow(rrect(6, 8, 52, 50, 3), 2.4, 2)
    ic.path(rrect(6, 8, 52, 50, 3), ic.lg([(0, "#ffffff"), (1, "#dfe2e6")]), INK, LW * 1.4)
    ic.path("M9,8H55Q58,8 58,11V20H6V11Q6,8 9,8Z", ic.lg([(0, "#ff8a7a"), (1, "#b8180c")]), INK, 1.4)
    for x in (18, 46):
        ic.path(rrect(x - 2, 3, 4, 10, 2), ic.lg([(0, "#e4e6e9"), (1, "#7b818a")], 0, 0, 1, 0), INK, 1)
    for r in range(4):
        for q in range(5):
            ic.path(f"M{11 + q * 9.4:.1f},{24 + r * 8.2:.1f}h5.4v4.6h-5.4Z", "#b4b9c0", None)
    ic.add(f'<path d="{circle(32.5, 34.5, 6.4)}" fill="none" stroke="#e0281a" stroke-width="2.4"/>')


def character_set(ic):
    """Character set: a Latin A and a Greek omega on two type tiles."""
    for x, y, col in ((4, 6, ("#ffffff", "#c9ccd1")), (26, 24, ("#fff8d0", "#e8c43a"))):
        ic.shadow(rrect(x, y, 34, 34, 4), 2.2, 1.8)
        ic.path(rrect(x, y, 34, 34, 4), ic.lg([(0, col[0]), (1, col[1])], 0, 0, 1, 1), INK, LW * 1.3)
    a = "M11,34L21,12L31,34M14.6,26.4H27.4"
    om = "M33,51H39.5V48C34,46 32.5,41.5 32.5,38.5C32.5,32.5 37,28.5 43,28.5C49,28.5 53.5,32.5 53.5,38.5C53.5,41.5 52,46 46.5,48V51H53"
    for d, c in ((a, "#2a3ae8"), (om, "#e0281a")):
        ic.add(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="5.4" stroke-linecap="round" stroke-linejoin="round"/>')
        ic.add(f'<path d="{d}" fill="none" stroke="{c}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')


EMBLEMS = {"vcs-normal": vcs_normal, "vcs-added": vcs_added, "vcs-removed": vcs_removed,
           "vcs-locally-modified": vcs_modified, "vcs-locally-modified-unstaged": vcs_unstaged,
           "vcs-update-required": vcs_update, "vcs-conflicting": vcs_conflict, "emblem-important": emblem_important,
           "object-locked": locked, "object-unlocked": unlocked, "starred": starred}
EMBLEM_ALIASES = {"emblem-added": "vcs-added", "emblem-remove": "vcs-removed", "emblem-checked": "vcs-normal",
                  "emblem-ok-symbolic": "vcs-normal", "vcs-locally-modified-small": "vcs-locally-modified",
                  "vcs-locally-modified-unstaged-small": "vcs-locally-modified-unstaged", "vcs-normal-small": "vcs-normal",
                  "vcs-added-small": "vcs-added", "vcs-removed-small": "vcs-removed", "vcs-conflicting-small": "vcs-conflicting",
                  "vcs-update-required-small": "vcs-update-required", "emblem-important-symbolic": "emblem-important",
                  "emblem-favorite": "starred", "starred-symbolic": "starred", "object-locked-symbolic": "object-locked",
                  "object-unlocked-symbolic": "object-unlocked", "emblem-locked": "object-locked", "emblem-unlocked": "object-unlocked"}
MORE = {"change-date": change_date, "character-set": character_set}
MORE_ALIASES = {"change-date-symbolic": "change-date", "view-calendar-day": "change-date"}


# ------------------------------------------------------------------ network servers, remote drives, share and mount emblems
def _tower(ic, x=20):
    """A beige server tower seen from the front left corner: drive bays, LEDs, vents."""
    beige = ("#fbf9f2", "#d9d5c8", "#8a877c")
    front, side, top = f"M{x},8H{x + 24}V60H{x}Z", f"M{x + 24},8L{x + 32},3V55L{x + 24},60Z", f"M{x},8L{x + 8},3H{x + 32}L{x + 24},8Z"
    ic.shadow(front + side + top, 3, 2.6)
    ic.path(side, ic.lg([(0, beige[1]), (1, beige[2])], 0, 0, 1, 0), INK, LW)
    ic.path(top, ic.lg([(0, "#ffffff"), (1, beige[1])]), INK, LW)
    ic.path(front, ic.lg([(0, beige[0]), (1, "#b4b0a3")], 0, 0, .4, 1), INK, LW)
    for k in range(2):                                   # 5.25" bays
        y = 12 + k * 8
        ic.path(f"M{x + 3},{y}H{x + 21}V{y + 6}H{x + 3}Z", ic.lg([(0, "#eceae2"), (1, "#bcb8ab")]), "#6c6a60", .8)
        ic.add(f'<path d="M{x + 5},{y + 3}H{x + 19}" stroke="#3c3a34" stroke-width="1.2"/>')
    ic.path(f"M{x + 8},29H{x + 21}V33H{x + 8}Z", ic.lg([(0, "#eceae2"), (1, "#bcb8ab")]), "#6c6a60", .8)   # floppy
    ic.add(f'<path d="M{x + 10},31H{x + 19}" stroke="#3c3a34" stroke-width="1"/>')
    ic.path(circle(x + 5, 31, 1.4), "#3ae03a", INK, .5)
    ic.path(circle(x + 5, 36, 1.4), "#ffb020", INK, .5)
    for k in range(5):
        ic.add(f'<path d="M{x + 4},{43 + k * 3}H{x + 20}" stroke="#8a877c" stroke-width="1.1"/>')


def network_server(ic):
    """Network server: the server tower with the KDE globe in front of it."""
    from gen import e_globe
    _tower(ic, 24)
    e_globe(ic, 3, 34, 13)


def _cylinder(ic, cx, top, bot, rx, ry):
    body = f"M{cx - rx},{top}V{bot}A{rx},{ry} 0 0 0 {cx + rx},{bot}V{top}Z"
    lid = f"M{cx - rx},{top}A{rx},{ry} 0 1 0 {cx + rx},{top}A{rx},{ry} 0 1 0 {cx - rx},{top}Z"
    ic.shadow(body + lid, 2.4, 2)
    ic.path(body, ic.lg([(0, "#1a5a7a"), (.35, "#5ab8d8"), (.6, "#2a88b0"), (1, "#0a3448")], 0, 0, 1, 0), INK, LW)
    mid = (top + bot) / 2
    ic.add(f'<path d="M{cx - rx},{mid}A{rx},{ry} 0 0 0 {cx + rx},{mid}" fill="none" stroke="{INK}" stroke-width="1"/>')
    ic.path(lid, ic.rg([(0, "#e8fbff"), (.6, "#8ad4ec"), (1, "#3a98c0")], .4, .35, .8), INK, LW)


def database_server(ic):
    """Database server: the server tower with the teal database cylinder in front."""
    _tower(ic, 24)
    _cylinder(ic, 16, 36, 54, 12, 4.2)


def drive_remote(ic):
    """Remote (network) drive: the hard disk with KDE Classic's crossed-cable junction in front."""
    from devices import harddisk
    ic.add('<g transform="translate(1,0) scale(.82)">')
    harddisk(ic)
    ic.add("</g>")
    cx, cy = 44, 46
    for a in (35, -35):
        r = math.radians(a)
        dx, dy = 15 * math.cos(r), 15 * math.sin(r)
        d = f"M{cx - dx:.2f},{cy - dy:.2f}L{cx + dx:.2f},{cy + dy:.2f}"
        ic.add(f'<path d="{d}" stroke="#000" stroke-opacity=".18" stroke-width="5" stroke-linecap="round" transform="translate(1.6,1.6)"/>')
        ic.add(f'<path d="{d}" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>')
        ic.add(f'<path d="{d}" stroke="#d9dce0" stroke-width="2.8" stroke-linecap="round"/>')
        ic.add(f'<path d="{d}" stroke="#fff" stroke-width=".9" stroke-linecap="round" transform="translate(0,-.6)"/>')
    ic.path(circle(cx, cy, 5), ic.rg([(0, "#fffbe0"), (.5, "#b8a860"), (1, "#5a5020")], .4, .35, .8), INK, 1.2)


def emblem_shared(ic):
    """Shared: KDE Classic's plug, blue-grey with brass pins and an orange cable."""
    cable = "M30,34C30,42 22,42 24,48C26,54 38,50 40,56C41,59 38,61 36,62"
    ic.add(f'<path d="{cable}" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>')
    ic.add(f'<path d="{cable}" fill="none" stroke="#f0a020" stroke-width="3.6" stroke-linecap="round"/>')
    ic.add(f'<path d="{cable}" fill="none" stroke="#ffe0a0" stroke-width="1" stroke-linecap="round" transform="translate(-.6,-.6)"/>')
    for x in (23, 33):
        ic.path(rrect(x, 3, 4.4, 15, 1.2), ic.lg([(0, "#fff0a0"), (.5, "#e8b830"), (1, "#8a5a04")], 0, 0, 1, 0), INK, 1.1)
    body = "M14,16H46V24Q46,34 36,36H24Q14,34 14,24Z"
    ic.shadow(body, 2.2, 1.8)
    ic.path(body, ic.lg([(0, "#e4e8f8"), (.45, "#8a98d0"), (1, "#3a4680")], 0, 0, 1, 1), INK, LW)
    ic.add('<path d="M17,19H43" stroke="#fff" stroke-opacity=".7" stroke-width="1.6" stroke-linecap="round"/>')


def _wedge(ic, cols):
    """KDE Classic's mount wedge: a right-angled triangle in the lower right, with a light stripe."""
    t = "M6,58L58,6V58Z"
    ic.shadow(t, 2, 1.8)
    ic.path(t, ic.lg([(0, cols[0]), (.5, cols[1]), (1, cols[2])], 0, 0, 1, 1), INK, 3)
    ic.add(f'<path d="M20,50L50,20" stroke="#fff" stroke-opacity=".7" stroke-width="4" stroke-linecap="round"/>')
    ic.add(f'<path d="M33,51L51,33" stroke="#fff" stroke-opacity=".35" stroke-width="3" stroke-linecap="round"/>')


def emblem_mounted(ic): _wedge(ic, ("#b0ff90", "#2fbf2a", "#0e5a10"))
def emblem_unmounted(ic): _wedge(ic, ("#f4f5f6", "#9aa0a8", "#3c4148"))


def e_sync(ic):
    """Synced folder: two green arrows chasing each other round."""
    for a0, a1 in ((200, 340), (20, 160)):
        r = 12
        p0 = (17 + r * math.cos(math.radians(a0)), 44 + r * math.sin(math.radians(a0)))
        p1 = (17 + r * math.cos(math.radians(a1)), 44 + r * math.sin(math.radians(a1)))
        d = f"M{p0[0]:.2f},{p0[1]:.2f}A{r},{r} 0 0 1 {p1[0]:.2f},{p1[1]:.2f}"
        ic.add(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="7.4" stroke-linecap="round"/>')
        ic.add(f'<path d="{d}" fill="none" stroke="#3fae2a" stroke-width="4.4" stroke-linecap="round"/>')
        t = math.radians(a1)
        tx, ty = -math.sin(t), math.cos(t)                  # direction of travel (clockwise)
        nx, ny = math.cos(t), math.sin(t)
        tip = (p1[0] + tx * 6, p1[1] + ty * 6)
        b1 = (p1[0] + nx * 5.4 - tx * 1, p1[1] + ny * 5.4 - ty * 1)
        b2 = (p1[0] - nx * 5.4 - tx * 1, p1[1] - ny * 5.4 - ty * 1)
        ic.path(f"M{tip[0]:.2f},{tip[1]:.2f}L{b1[0]:.2f},{b1[1]:.2f}L{b2[0]:.2f},{b2[1]:.2f}Z", ic.lg([(0, "#c8f8a8"), (1, "#1e7a10")]), INK, 1.2)


NETWORK = {"network-server": network_server, "network-server-database": database_server}
NETWORK_ALIASES = {"network-server-symbolic": "network-server", "server-database": "network-server-database",
                   "network-server-database-symbolic": "network-server-database"}
NET_DEVICES = {"drive-remote": drive_remote}
NET_DEVICE_ALIASES = {"drive-harddisk-network": "drive-remote", "network-drive": "drive-remote"}
EMBLEMS_NET = {"emblem-shared": emblem_shared, "emblem-mounted": emblem_mounted, "emblem-unmounted": emblem_unmounted}
EMBLEMS_NET_ALIASES = {"emblem-shared-symbolic": "emblem-shared", "emblem-mounted-symbolic": "emblem-mounted",
                       "emblem-unmounted-symbolic": "emblem-unmounted", "emblem-share": "emblem-shared"}


def _ic(fn):
    def f():
        ic = Icon()
        fn(ic)
        return ic
    return f


# system-file-manager is also the Locations page in System Settings, "Open with File Manager" and the Locations runner
# Dolphin's own app icon is the KDE Classic filing cabinet by default (Dolphin came after KDE 3). The traced
# dolphin is kept for the optional "KDE Modern Classic Dolphin" add-on theme (DOLPHIN_ADDON below).
APPS = {"system-file-manager": _ic(cabinet)}
DOLPHIN_ADDON = {"org.kde.dolphin": _ic(dolphin)}
DOLPHIN_ADDON_ALIASES = {"dolphin": "org.kde.dolphin", "system-file-manager-dolphin": "org.kde.dolphin"}
APP_ALIASES = {"org.kde.dolphin": "system-file-manager", "system-file-manager-dolphin": "system-file-manager", "dolphin": "system-file-manager",
               "file-manager": "system-file-manager", "kfm": "system-file-manager", "system-file-manager-symbolic": "system-file-manager"}


# ---------------------------------------------------------------- 16 / 22 px view modes
# At toolbar sizes the pane frame left only white boxes, so the small versions drop the frame and draw bold,
# pixel-aligned tiles and rows on their own grid.
SMALL_COLS = ("#3d9ad8", "#e8c43a", "#4fae5a", "#d8573d")


def _tile(x, y, w, h, col):
    hl = f'<path d="M{x + 1},{y + 1.5}H{x + w - 1}" stroke="#fff" stroke-opacity=".7" stroke-width="1"/>' if w >= 4 else ""
    return (f'<rect x="{x + .5}" y="{y + .5}" width="{w - 1}" height="{h - 1}" fill="{col}" stroke="{INK}" stroke-width="1"/>' + hl)


def small_view(kind, S):
    out = []
    if kind == "icons":
        t = 6 if S == 16 else 8
        g = 2 if S == 16 else 3
        o = (S - 2 * t - g) // 2
        for k in range(4):
            r, q = divmod(k, 2)
            out.append(_tile(o + q * (t + g), o + r * (t + g), t, t, SMALL_COLS[k]))
    else:
        n = 3 if S == 16 else 4
        step = 5 if S == 16 else 5
        t = 4 if S == 16 else 4
        y0 = (S - (n * step - (step - t))) // 2
        for k in range(n):
            y = y0 + k * step
            if kind == "details":
                x = 1
                w = S - 8 - (k % 2) * 2
            else:               # tree: the second and third rows are children
                x = 1 + (0 if k in (0, n - 1) else 3 if S == 16 else 4)
                w = S - x - 6 - (k % 2)
            out.append(_tile(x, y, t, t, SMALL_COLS[k % 4]))
            # white bar with a black edge: reads on light and dark toolbars alike
            out.append(f'<rect x="{x + t + 1.5}" y="{y + .5}" width="{w - 1}" height="3" fill="#f2f2f2" stroke="{INK}" stroke-width="1"/>')
        if kind == "tree":
            xs = 1 + t // 2
            last_child = y0 + (n - 2) * step + t // 2
            out.insert(0, f'<path d="M{xs + .5},{y0 + t}V{last_child + .5}H{xs + (3 if S == 16 else 4)}" fill="none" stroke="#9aa0a8" stroke-width="1"/>')
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}" '
            f'viewBox="0 0 {S} {S}" shape-rendering="crispEdges">{"".join(out)}</svg>\n')


SMALL_VIEW = {"view-list-icons": "icons", "view-list-details": "details", "view-list-tree": "tree"}


def write(out):
    for S in (16, 22):
        d = f"{out}/{S}x{S}/actions"
        os.makedirs(d, exist_ok=True)
        for name, kind in SMALL_VIEW.items():
            open(f"{d}/{name}.svg", "w").write(small_view(kind, S))
        for a, t in VIEW_ALIASES.items():
            if t in SMALL_VIEW and not os.path.lexists(f"{d}/{a}.svg"):
                os.symlink(f"{t}.svg", f"{d}/{a}.svg")
    d = f"{out}/scalable/actions"
    os.makedirs(d, exist_ok=True)
    for name, fn in {**VIEW, **EDIT, **MORE}.items():
        open(f"{d}/{name}.svg", "w").write(_ic(fn)().svg(64))
    if not os.path.exists(f"{d}/document-open-folder.svg"):
        os.symlink("../places/folder-open.svg", f"{d}/document-open-folder.svg")
    for a, t in {**VIEW_ALIASES, **EDIT_ALIASES, **MORE_ALIASES}.items():
        if not os.path.exists(f"{d}/{a}.svg"):
            os.symlink(f"{t}.svg", f"{d}/{a}.svg")
    for sub, icons, aliases in (("places", NETWORK, NETWORK_ALIASES), ("devices", NET_DEVICES, NET_DEVICE_ALIASES)):
        d = f"{out}/scalable/{sub}"
        os.makedirs(d, exist_ok=True)
        for name, fn in icons.items():
            open(f"{d}/{name}.svg", "w").write(_ic(fn)().svg(64))
        for a, t in aliases.items():
            if not os.path.exists(f"{d}/{a}.svg"):
                os.symlink(f"{t}.svg", f"{d}/{a}.svg")
    d = f"{out}/scalable/emblems"
    os.makedirs(d, exist_ok=True)
    for name, fn in {**EMBLEMS, **EMBLEMS_NET}.items():
        open(f"{d}/{name}.svg", "w").write(_ic(fn)().svg(64))
    for a, t in {**EMBLEM_ALIASES, **EMBLEMS_NET_ALIASES}.items():
        if not os.path.exists(f"{d}/{a}.svg"):
            os.symlink(f"{t}.svg", f"{d}/{a}.svg")
    d = f"{out}/scalable/apps"
    os.makedirs(d, exist_ok=True)
    for name, fn in APPS.items():
        open(f"{d}/{name}.svg", "w").write(fn().svg(64))
    for a, t in APP_ALIASES.items():
        if not os.path.exists(f"{d}/{a}.svg"):
            os.symlink(f"{t}.svg", f"{d}/{a}.svg")
    return len(APPS)
