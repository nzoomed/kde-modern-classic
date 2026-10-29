"""KDE Classic Vector: desktop shell icons - panel and desktop edit mode, widgets, lock/login screen,
on-screen displays, notifications from the shell, Spectacle's annotation tools and System Monitor."""
import math, os
from gen import Icon, INK, LW, circle, rrect, e_globe


def _ic(fn):
    def f():
        ic = Icon()
        fn(ic)
        return ic
    return f


METAL = ("#ffffff", "#b4b9c0", "#5c6168")
SCREEN = ("#3a6fd8", "#1a3ea8", "#0c2470")


def _screen(ic, x=4, y=6, w=56, h=42):
    """A plain monitor face used as the backdrop for panel and desktop icons."""
    ic.shadow(rrect(x, y, w, h, 3), 2.6, 2.2)
    ic.path(rrect(x, y, w, h, 3), ic.lg([(0, "#fbf9f2"), (1, "#b4b0a3")], 0, 0, .3, 1), INK, LW)
    ic.path(rrect(x + 4, y + 4, w - 8, h - 8, 1.4), ic.lg([(0, SCREEN[0]), (.6, SCREEN[1]), (1, SCREEN[2])]), INK, 1)


def _arrow(ic, d, col="#3fae2a", w=3.4):
    ic.add(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w + 2.4}" stroke-linecap="round" stroke-linejoin="round"/>')
    ic.add(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')


def _panel_bar(ic, x, y, w, h):
    ic.path(f"M{x},{y}H{x + w}V{y + h}H{x}Z", ic.lg([(0, "#e4e6e9"), (1, "#8a9098")]), INK, 1)
    ic.path(rrect(x + 1.5, y + 1.5, h - 3, h - 3, 1), "#ffffff", INK, .6)


# ------------------------------------------------------------------ panel and desktop edit mode
def panel_fit_width(ic):
    """Panel width: fill the screen - a panel along the bottom with arrows out to both sides."""
    _screen(ic)
    _panel_bar(ic, 8, 36, 48, 8)
    _arrow(ic, "M16,24H48M22,18L16,24L22,30M42,18L48,24L42,30", "#ffffff", 3)


def panel_fit_height(ic):
    """Panel height: fill the screen - a panel down the left with arrows up and down."""
    _screen(ic)
    ic.path("M8,10H16V44H8Z", ic.lg([(0, "#e4e6e9"), (1, "#8a9098")], 0, 0, 1, 0), INK, 1)
    ic.path(rrect(9.5, 11.5, 5, 5, 1), "#ffffff", INK, .6)
    _arrow(ic, "M36,14V40M30,20L36,14L42,20M30,34L36,40L42,34", "#ffffff", 3)


def panel_custom(ic):
    """Panel size: custom - a short panel with a ruler and a slider handle."""
    _screen(ic)
    _panel_bar(ic, 18, 36, 28, 8)
    ic.path("M10,18H54V26H10Z", ic.lg([(0, "#fff8c0"), (1, "#e8c43a")]), INK, 1)
    for k in range(12):
        x = 12 + k * 3.6
        ic.add(f'<path d="M{x:.1f},18V{21 if k % 3 else 23}" stroke="{INK}" stroke-width=".8"/>')
    ic.path("M44,14L48,14L48,28L46,31L44,28Z", ic.lg([(0, "#ffffff"), (1, "#8a9098")], 0, 0, 1, 0), INK, 1)


def overflow_menu(ic):
    """More options (vertical): three glossy dots stacked."""
    for y in (14, 32, 50):
        ic.shadow(circle(32, y, 6), 1.8, 1.6)
        ic.path(circle(32, y, 6), ic.rg([(0, "#ffffff"), (.5, "#8a9098"), (1, "#2c3036")], .4, .35, .8), INK, 1.2)


def hamburger(ic):
    """Open menu: three bars."""
    for y in (14, 30, 46):
        ic.shadow(rrect(8, y, 48, 7, 3.4), 1.8, 1.6)
        ic.path(rrect(8, y, 48, 7, 3.4), ic.lg([(0, "#8a9098"), (1, "#2c3036")]), INK, 1.2)
        ic.add(f'<path d="M12,{y + 2}H52" stroke="#fff" stroke-opacity=".45" stroke-width="1.2" stroke-linecap="round"/>')


def show_background(ic):
    """Widget background: a widget panel half translucent over the desktop."""
    _screen(ic)
    ic.path(rrect(16, 14, 32, 24, 3), "#ffffff", INK, 1.2, ' fill-opacity=".85"')
    ic.add('<path d="M16,26H48" stroke="#5c6168" stroke-width=".8" stroke-dasharray="2 2"/>')
    ic.path(rrect(16, 26, 32, 12, 3), "#ffffff", None, ' fill-opacity=".35"')
    ic.add('<path d="M20,19H38M20,22H32" stroke="#5c6168" stroke-width="1.4"/>')


def funnel(ic):
    """Filter: KDE Classic's grey funnel."""
    d = "M6,10Q6,4 32,4Q58,4 58,10Q58,14 38,30V52Q38,58 32,58Q26,58 26,52V30Q6,14 6,10Z"
    ic.shadow(d, 2.6, 2.2)
    ic.path(d, ic.lg([(0, "#6c727a"), (.3, "#ffffff"), (.6, "#b4b9c0"), (1, "#4c5158")], 0, 0, 1, 0), INK, LW * 1.2)
    ic.path("M8,10Q8,7 32,7Q56,7 56,10Q56,13 32,13Q8,13 8,10Z", ic.lg([(0, "#5c6168"), (1, "#c3c7cd")]), INK, 1)
    ic.add('<path d="M30,32V52" stroke="#fff" stroke-opacity=".7" stroke-width="1.6" stroke-linecap="round"/>')


def _mini(ic, x, y, s, col):
    ic.path(f"M{x},{y + s * .2}H{x + s * .4}L{x + s * .5},{y}H{x + s}V{y + s * .85}H{x}Z",
            ic.lg([(0, "#ffffff"), (.45, col), (1, col)]), INK, .8)


def arrange_rows(ic):
    """Arrange icons in rows: three rows of small folders with arrows along them."""
    cols = ("#3d9ad8", "#e8c43a", "#4fae5a", "#d8573d", "#9a62d8", "#3cc4d4")
    for r in range(3):
        for c in range(3):
            _mini(ic, 6 + c * 16, 8 + r * 17, 11, cols[(r * 3 + c) % 6])
    for r in range(3):
        _arrow(ic, f"M54,{13 + r * 17}H60", "#2a6ac8", 2)


def dashboard(ic):
    """Show the desktop / dashboard: the screen with a clock, a note and a chart widget on it."""
    _screen(ic)
    ic.path(circle(18, 20, 6.6), "#ffffff", INK, 1)
    ic.add(f'<path d="M18,20V16M18,20L21,22" stroke="{INK}" stroke-width="1.2" stroke-linecap="round"/>')
    ic.path(rrect(30, 13, 20, 14, 1.4), "#fff8c0", INK, 1)
    ic.add('<path d="M33,17H47M33,20H44M33,23H46" stroke="#a8840e" stroke-width="1"/>')
    ic.path(rrect(12, 30, 38, 12, 1.4), "#ffffff", INK, 1)
    for k, h in enumerate((4, 7, 5, 9, 6, 8)):
        ic.path(f"M{15 + k * 5.6},{40 - h}h3.6v{h}h-3.6Z", "#4fae5a", None)


def widget_folder(ic):
    """Folder View widget: a classic folder framed as a window on the desktop."""
    ic.shadow("M4,8H60V56H4Z", 2.6, 2.2)
    ic.path("M4,8H60V56H4Z", ic.lg([(0, "#fffef4"), (1, "#fff4c4")], 0, 0, 1, 1), "#0a1a80", 2.2)
    ic.path("M5,9H59V16H5Z", ic.lg([(0, "#9fc8f0"), (1, "#3a6ac0")]), None)
    for k, c in enumerate(("#3d9ad8", "#e8c43a", "#4fae5a", "#d8573d", "#3d9ad8", "#9a62d8")):
        _mini(ic, 10 + (k % 3) * 16, 21 + (k // 3) * 16, 11, c)


def widget_tray(ic):
    """System tray widget: a strip of tiny tray icons with the up arrow for hidden ones."""
    ic.shadow("M2,22H62V44H2Z", 2.6, 2.2)
    ic.path(rrect(2, 22, 60, 22, 3), ic.lg([(0, "#e4e6e9"), (1, "#8a9098")]), INK, LW)
    _arrow(ic, "M8,37L12,29L16,37", "#3c4148", 2)
    for k, c in enumerate(("#3fae2a", "#2a6ac8", "#e8c43a", "#d8573d")):
        ic.path(rrect(21 + k * 10, 28, 8, 10, 1.6), ic.lg([(0, "#ffffff"), (.5, c), (1, c)]), INK, .8)


def clipboard(ic):
    """Clipboard: KDE 3's Klipper - a wooden clipboard with a sheet, the K on it and an orange pencil."""
    ic.shadow(rrect(8, 6, 40, 54, 3), 2.6, 2.2)
    ic.path(rrect(8, 6, 40, 54, 3), ic.lg([(0, "#d89050"), (.5, "#a8642a"), (1, "#5a2806")], 0, 0, 1, 1), INK, LW)
    ic.path("M12,13H44V56H12Z", ic.lg([(0, "#ffffff"), (1, "#e4e6e9")]), INK, 1)
    for k in range(4):
        ic.add(f'<path d="M16,{19 + k * 4}H{38 - (k % 2) * 6}" stroke="#7b818a" stroke-width="1.1"/>')
    ic.path("M17,36H22V42L27,36H33L26,44L33,52H27L22,46V52H17Z", ic.lg([(0, "#5c6168"), (1, "#0a0c10")]), INK, .8)
    ic.path(rrect(20, 2, 16, 8, 2.4), ic.lg([(0, "#e4e6e9"), (1, "#6c727a")]), INK, 1.2)
    ic.add('<g transform="rotate(40 48 36)">')
    ic.path("M43,10H53V46L48,54L43,46Z", ic.lg([(0, "#ffd08a"), (.5, "#f08a1a"), (1, "#a84c04")], 0, 0, 1, 0), INK, 1.2)
    ic.path("M43,46L48,54L53,46Z", "#f4d8b0", INK, .9)
    ic.path("M46.6,51L48,54L49.4,51Z", INK, None)
    ic.add("</g>")


def analog_clock(ic):
    """Analog clock widget: a round wall clock."""
    cx, cy, r = 32, 32, 27
    ic.shadow(circle(cx, cy, r), 2.6, 2.2)
    ic.path(circle(cx, cy, r), ic.lg([(0, "#e4e6e9"), (1, "#7b818a")], 0, 0, 1, 1), INK, LW)
    ic.path(circle(cx, cy, r - 4), ic.rg([(0, "#ffffff"), (1, "#e4e6e9")]), INK, 1)
    for k in range(12):
        a = 2 * math.pi * k / 12
        r1 = r - 9 if k % 3 == 0 else r - 7.6
        ic.add(f'<path d="M{cx + r1 * math.sin(a):.2f},{cy - r1 * math.cos(a):.2f}L{cx + (r - 5.6) * math.sin(a):.2f},{cy - (r - 5.6) * math.cos(a):.2f}" '
               f'stroke="{INK}" stroke-width="{2 if k % 3 == 0 else 1}"/>')
    ic.add(f'<path d="M{cx},{cy}L{cx - 6},{cy - 12}M{cx},{cy}L{cx + 14},{cy + 3}" stroke="{INK}" stroke-width="2.8" stroke-linecap="round"/>')
    ic.add(f'<path d="M{cx},{cy + 4}L{cx + 4},{cy - 17}" stroke="#d8302a" stroke-width="1.2" stroke-linecap="round"/>')
    ic.path(circle(cx, cy, 2), INK, None)


# ------------------------------------------------------------------ login, OSD and shell notices
def user_list(ic):
    """Other users (login screen): the KDE Classic cartoon faces in profile beside a short list of users."""
    from settings import _profile
    for k in range(3):
        ic.path(rrect(34, 12 + k * 13, 26, 9, 2), ic.lg([(0, "#ffffff"), (1, "#c9ccd1")]), INK, 1)
        ic.path(circle(39, 16.5 + k * 13, 2.6), ("#3fae2a", "#2a6ac8", "#e8a010")[k], INK, .6)
        ic.add(f'<path d="M44,{16.5 + k * 13}H56" stroke="#5c6168" stroke-width="1.4"/>')
    _profile(ic, 2, 8, .95, ("#ffb070", "#a8400a"))          # ginger hair, behind
    _profile(ic, 9, 26, 1.12, ("#5a5048", "#14100c"))        # dark hair, in front


def keyboard_layout(ic):
    """Keyboard layout (on-screen display): a keyboard with the KDE globe for languages."""
    ic.shadow("M4,26H54V54H4Z", 2.6, 2.2)
    ic.path(rrect(4, 26, 50, 28, 3), ic.lg([(0, "#f4f1e8"), (1, "#a8a497")]), INK, LW)
    for r, (y, n, x0) in enumerate(((30, 7, 8), (37, 7, 10), (44, 6, 12))):
        for k in range(n):
            ic.path(rrect(x0 + k * 6, y, 5, 5, 1), ic.lg([(0, "#ffffff"), (1, "#c9c5b8")]), INK, .6)
    ic.path(rrect(16, 50.6, 24, 2.6, 1), "#ffffff", INK, .6)
    e_globe(ic, 36, 4, 13)


def speedometer(ic):
    """Performance (power profile on-screen display): a dial from green to red with its needle."""
    cx, cy, r = 32, 40, 27
    ic.shadow(f"M{cx - r},{cy}A{r},{r} 0 0 1 {cx + r},{cy}V{cy + 10}H{cx - r}Z", 2.6, 2.2)
    ic.path(f"M{cx - r},{cy + 8}V{cy}A{r},{r} 0 0 1 {cx + r},{cy}V{cy + 8}Q{cx + r},{cy + 12} {cx + r - 4},{cy + 12}H{cx - r + 4}Q{cx - r},{cy + 12} {cx - r},{cy + 8}Z",
            ic.lg([(0, "#5c6168"), (1, "#14171c")]), INK, LW)
    for a0, a1, col in ((180, 240, "#3fae2a"), (240, 300, "#e8c43a"), (300, 360, "#e0281a")):
        p0 = (cx + (r - 6) * math.cos(math.radians(a0)), cy + (r - 6) * math.sin(math.radians(a0)))
        p1 = (cx + (r - 6) * math.cos(math.radians(a1)), cy + (r - 6) * math.sin(math.radians(a1)))
        ic.add(f'<path d="M{p0[0]:.2f},{p0[1]:.2f}A{r - 6},{r - 6} 0 0 1 {p1[0]:.2f},{p1[1]:.2f}" fill="none" stroke="{col}" stroke-width="5"/>')
    a = math.radians(305)
    ic.add(f'<path d="M{cx},{cy}L{cx + 19 * math.cos(a):.2f},{cy + 19 * math.sin(a):.2f}" stroke="#fff" stroke-width="2.6" stroke-linecap="round"/>')
    ic.path(circle(cx, cy, 3.4), ic.rg([(0, "#ffffff"), (1, "#8a9098")]), INK, 1)


def phone_battery(ic):
    """Phone battery: a phone with a green battery gauge on its screen."""
    ph = rrect(16, 4, 32, 56, 5)
    ic.shadow(ph, 2.4, 2)
    ic.path(ph, ic.lg([(0, "#5c6168"), (1, "#14171c")], 0, 0, 1, 0), INK, LW)
    ic.path("M20,11H44V50H20Z", ic.lg([(0, "#e8f6ff"), (1, "#9ac8e8")]), INK, .8)
    ic.path(rrect(26, 18, 12, 26, 2), "#ffffff", INK, 1.2)
    ic.path("M29,15.6H35V18H29Z", "#ffffff", INK, 1)
    ic.path("M28,29H36V42H28Z", ic.lg([(0, "#c8f8a8"), (1, "#2f8a1e")]), None)
    ic.path(circle(32, 55, 2), "#4c5158", None)


def software_rendering(ic):
    """Software rendering (graphics card not used): the green graphics card, greyed, with a red cross."""
    ic.add('<g opacity=".55">')
    ic.shadow("M4,12H52V44H4Z", 2.6, 2.2)
    ic.path("M4,12H52V44H4Z", ic.lg([(0, "#d9dce0"), (1, "#7b818a")], 0, 0, 1, 1), INK, LW)
    ic.path("M14,20H30V36H14Z", "#3c4148", INK, .8)
    for k in range(12):
        ic.add(f'<rect x="{7 + k * 3.6:.1f}" y="44" width="2" height="4.5" fill="#c9ccd1" stroke="#5c6168" stroke-width=".3"/>')
    ic.add("</g>")
    ic.shadow(circle(46, 46, 13), 2, 1.8)
    ic.path(circle(46, 46, 13), ic.rg([(0, "#ffb0a0"), (.55, "#e0281a"), (1, "#6a0804")], .4, .32, .8), INK, 1.6)
    ic.add('<path d="M40.5,40.5L51.5,51.5M51.5,40.5L40.5,51.5" stroke="#fff" stroke-width="3.6" stroke-linecap="round"/>')


def bomb(ic):
    """Out of memory (an app was stopped): the crash-dump bomb on its own."""
    from filetypes import e_bomb2
    ic.add('<g transform="translate(32,32) scale(1.32) translate(-27,-31)">')
    e_bomb2(ic)
    ic.add("</g>")


def mask(ic):
    """Private browsing: a purple masquerade mask."""
    d = ("M4,22Q4,16 12,16H52Q60,16 60,22Q60,38 48,42Q40,44 36,36Q32,32 28,36Q24,44 16,42Q4,38 4,22Z")
    ic.shadow(d, 2.6, 2.2)
    ic.path(d, ic.lg([(0, "#d8b0ff"), (.5, "#7a3ad0"), (1, "#3a0e6a")], 0, 0, 0, 1), INK, LW)
    for x in (18, 46):
        ic.path(f"M{x - 8},27Q{x},20 {x + 8},27Q{x},33 {x - 8},27Z", "#1a1a1a", INK, 1)
    ic.add('<path d="M8,22Q10,19 16,19" fill="none" stroke="#fff" stroke-opacity=".6" stroke-width="1.6" stroke-linecap="round"/>')
    ic.add(f'<path d="M4,22L1,30M60,22L63,30" stroke="{INK}" stroke-width="1.6" stroke-linecap="round"/>')


def in_love(ic):
    """Welcome screen: a yellow smiley with heart eyes."""
    ic.shadow(circle(32, 32, 27), 2.6, 2.2)
    ic.path(circle(32, 32, 27), ic.rg([(0, "#fffbe0"), (.6, "#ffd21a"), (1, "#c87a04")], .4, .35, .8), INK, LW)
    for x in (22, 42):
        ic.path(f"M{x},34C{x - 9},28 {x - 7},20 {x - 3},20C{x - 1},20 {x},22 {x},23C{x},22 {x + 1},20 {x + 3},20C{x + 7},20 {x + 9},28 {x},34Z",
                ic.rg([(0, "#ffb0a0"), (1, "#c8180c")], .4, .3, .8), INK, 1)
    ic.add(f'<path d="M18,40Q32,52 46,40" fill="none" stroke="{INK}" stroke-width="2.6" stroke-linecap="round"/>')


def split_top_bottom(ic):
    """Split top / bottom: KDE Classic's cream view pane divided across the middle."""
    from dolphin import pane, NAVY
    pane(ic)
    ic.path("M8,30.5H56V33.5H8Z", NAVY, None)
    for y0 in (14, 38):
        for k in range(2):
            ic.add(f'<path d="M12,{y0 + k * 6}H{44 - k * 10}" stroke="#6c727a" stroke-width="1.4"/>')


# ------------------------------------------------------------------ Spectacle annotation tools
# One family: each tool shown by the mark it makes, bold enough for a 22 px toolbar.
def pointer(ic):
    """Browse (no tool): a white mouse pointer."""
    d = "M18,6V50L28,40L36,58L44,54L36,37H50Z"
    ic.shadow(d, 2.4, 2)
    ic.path(d, ic.lg([(0, "#ffffff"), (1, "#c9ccd1")]), INK, LW * 1.4)


def crop(ic):
    """Crop: two dark crop brackets with a dashed frame between them."""
    ic.add('<path d="M18,18H46V46H18Z" fill="#9fd4ff" fill-opacity=".35" stroke="#2a6ac8" stroke-width="1.4" stroke-dasharray="3 2"/>')
    _arrow(ic, "M14,4V50H60", "#5c6168", 4.4)
    _arrow(ic, "M4,14H50V60", "#a8adb4", 4.4)


def select_area(ic):
    """Select: a dashed selection box with the pointer at its corner."""
    ic.add('<path d="M6,6H44V40H6Z" fill="#9fd4ff" fill-opacity=".4"/>')
    ic.add('<path d="M6,6H44V40H6Z" fill="none" stroke="#fff" stroke-width="2"/>')
    ic.add(f'<path d="M6,6H44V40H6Z" fill="none" stroke="{INK}" stroke-width="2" stroke-dasharray="4 3"/>')
    d = "M38,30V60L45,53L50,63L55,60L50,51H60Z"
    ic.shadow(d, 1.8, 1.6)
    ic.path(d, ic.lg([(0, "#ffffff"), (1, "#c9ccd1")]), INK, 1.4)


def highlighter(ic):
    """Highlight: a yellow highlighter pen and the bright stroke it has laid down."""
    ic.add('<path d="M4,54H40" stroke="#fff36a" stroke-width="9" stroke-linecap="square" stroke-opacity=".9"/>')
    ic.add('<g transform="rotate(45 40 26)">')
    ic.path(rrect(33, 2, 14, 30, 3), ic.lg([(0, "#fff8c0"), (.5, "#ffe020"), (1, "#a88a04")], 0, 0, 1, 0), INK, 1.3)
    ic.path("M34,32H46V38H34Z", ic.lg([(0, "#e4e6e9"), (1, "#6c727a")], 0, 0, 1, 0), INK, 1.1)
    ic.path("M36,38H44L42,46H38Z", "#ffe020", INK, 1.1)
    ic.add("</g>")


def draw_line(ic):
    _arrow(ic, "M10,54L54,10", "#2a6ac8", 4)
    for x, y in ((10, 54), (54, 10)):
        ic.path(rrect(x - 4, y - 4, 8, 8, 1.4), "#ffffff", INK, 1.2)


def draw_arrow(ic):
    _arrow(ic, "M10,54L50,14M28,12H52V36", "#e0281a", 5)


def draw_rect(ic):
    ic.shadow("M8,14H56V50H8Z", 2.4, 2)
    ic.path("M8,14H56V50H8Z", "#9fd4ff", "#2a6ac8", 4, ' fill-opacity=".45"')


def draw_ellipse(ic):
    ic.shadow("M4,32A28,20 0 1 0 60,32A28,20 0 1 0 4,32Z", 2.4, 2)
    ic.path("M4,32A28,20 0 1 0 60,32A28,20 0 1 0 4,32Z", "#b8f0a0", "#2f8a1e", 4, ' fill-opacity=".5"')


def pixelate(ic):
    """Pixelate: a block of chunky coloured squares, like a mosaic."""
    cols = ["#3d9ad8", "#5aaee8", "#e8c43a", "#f0d870", "#4fae5a", "#7ac884", "#d8573d", "#e88a6a", "#9a62d8"]
    ic.shadow("M6,6H58V58H6Z", 2.4, 2)
    for i in range(4):
        for j in range(4):
            ic.path(f"M{6 + i * 13},{6 + j * 13}h13v13h-13Z", cols[(i * 3 + j * 5) % 9], None)
    ic.path("M6,6H58V58H6Z", "none", INK, LW * 1.2)


def blur(ic):
    """Blur: a blue disc whose edge fades away in soft rings."""
    for k in range(7):
        ic.path(circle(32, 32, 28 - k * 2.4), "#2a6ac8", None, f' fill-opacity="{.12 + k * .04:.2f}"')
    ic.path(circle(32, 32, 11), ic.rg([(0, "#bfe0ff"), (1, "#2a6ac8")], .4, .35, .8), None)


def draw_text(ic):
    """Text: a bold serif capital T."""
    d = "M8,6H56V20H50L48,14H38V50L44,52V58H20V52L26,50V14H16L14,20H8Z"
    ic.shadow(d, 2.4, 2)
    ic.path(d, ic.lg([(0, "#5c6168"), (1, "#0a0c10")], 0, 0, 1, 1), INK, 1.2)


def draw_number(ic):
    """Number: a red counter badge with a white 1."""
    ic.shadow(circle(32, 32, 26), 2.4, 2)
    ic.path(circle(32, 32, 26), ic.rg([(0, "#ffb0a0"), (.55, "#e0281a"), (1, "#6a0804")], .4, .32, .8), INK, LW * 1.4)
    _arrow(ic, "M26,22L34,16V48M26,48H42", "#ffffff", 4.6)


def video_camera(ic):
    """Record: a video camera with its lens and a red recording light."""
    body = rrect(4, 18, 40, 30, 4)
    ic.shadow(body + "M44,26L60,18V48L44,40Z", 2.4, 2)
    ic.path("M44,26L60,18V48L44,40Z", ic.lg([(0, "#8a9098"), (1, "#2c3036")]), INK, LW)
    ic.path(body, ic.lg([(0, "#6c727a"), (1, "#14171c")]), INK, LW)
    ic.path(circle(18, 33, 9), ic.rg([(0, "#bfe0ff"), (.5, "#2a5ac8"), (1, "#0a1a40")], .35, .3, .8), INK, 1.2)
    ic.path(circle(38, 24, 2.6), ic.rg([(0, "#ffb0a0"), (1, "#c8180c")]), INK, .8)


# ------------------------------------------------------------------ System Monitor
def _table(ic, x=4, y=8, w=56, h=46, cols=(22, 40)):
    ic.shadow(f"M{x},{y}H{x + w}V{y + h}H{x}Z", 2.4, 2)
    ic.path(f"M{x},{y}H{x + w}V{y + h}H{x}Z", ic.lg([(0, "#ffffff"), (1, "#eceef1")]), INK, LW)
    ic.path(f"M{x},{y}H{x + w}V{y + 8}H{x}Z", ic.lg([(0, "#e4e6e9"), (1, "#a8adb4")]), INK, LW)
    for r in range(1, 5):
        ic.add(f'<path d="M{x},{y + 8 + r * 8}H{x + w}" stroke="#c9ccd1" stroke-width=".8"/>')
    for cx in cols:
        ic.add(f'<path d="M{cx},{y}V{y + h}" stroke="#9aa0a8" stroke-width=".8"/>')


def sort_handle(ic):
    """Sort: a drag handle with arrows up and down."""
    for y in (26, 32, 38):
        ic.add(f'<path d="M8,{y}H36" stroke="#5c6168" stroke-width="3" stroke-linecap="round"/>')
    _arrow(ic, "M50,6V58M42,14L50,6L58,14M42,50L50,58L58,50", "#2a6ac8", 3.4)


def hide_column(ic):
    """Hide column: a table with its middle column greyed and struck through."""
    _table(ic)
    ic.add('<path d="M22,8H40V54H22Z" fill="#000" fill-opacity=".14"/>')
    _arrow(ic, "M18,58L44,4", "#e0281a", 3.4)


def send_signal(ic):
    """Send signal: a yellow lightning bolt striking a process window."""
    ic.shadow("M4,20H44V58H4Z", 2.4, 2)
    ic.path("M4,20H44V58H4Z", ic.lg([(0, "#ffffff"), (1, "#e4e6e9")]), INK, LW)
    ic.path("M4,20H44V27H4Z", ic.lg([(0, "#9fc8f0"), (1, "#3a6ac0")]), INK, LW)
    for k in range(3):
        ic.add(f'<path d="M9,{34 + k * 6}H{36 - k * 6}" stroke="#7b818a" stroke-width="1.6"/>')
    bolt = "M42,2L28,30H38L32,54L58,20H46L54,2Z"
    ic.shadow(bolt, 2, 1.8)
    ic.path(bolt, ic.lg([(0, "#fffbe0"), (.5, "#ffd21a"), (1, "#c87a04")]), INK, LW)


def _proc_badge(ic, kind):
    _table(ic, 4, 4, 48, 40, (20, 36))
    cx, cy = 46, 46
    ic.shadow(circle(cx, cy, 14), 2, 1.8)
    ic.path(circle(cx, cy, 14), ic.rg([(0, "#ffffff"), (1, "#c9ccd1")], .4, .35, .8), INK, 1.6)
    from settings import _profile
    if kind == "own":
        _profile(ic, cx - 10.6, cy - 12.6, .82, ("#fff0a0", "#c89a20"))
    elif kind == "users":
        _profile(ic, cx - 13, cy - 12.6, .66, ("#ffb070", "#a8400a"))
        _profile(ic, cx - 6, cy - 9, .7, ("#5a5048", "#14100c"))
    else:
        for k in range(4):
            a = math.radians(45 * k)
            ic.add(f'<path d="M{cx - 8 * math.cos(a):.2f},{cy - 8 * math.sin(a):.2f}L{cx + 8 * math.cos(a):.2f},{cy + 8 * math.sin(a):.2f}" stroke="#e8a010" stroke-width="3.2" stroke-linecap="round"/>')


def proc_own(ic): _proc_badge(ic, "own")
def proc_users(ic): _proc_badge(ic, "users")
def proc_all(ic): _proc_badge(ic, "all")


def trim_margins(ic):
    """Margins: a page with arrows pressing in from each side."""
    ic.shadow("M14,10H50V54H14Z", 2.4, 2)
    ic.path("M14,10H50V54H14Z", ic.lg([(0, "#ffffff"), (1, "#e4e6e9")]), INK, LW)
    ic.add('<path d="M20,16H44V48H20Z" fill="none" stroke="#2a6ac8" stroke-width="1.2" stroke-dasharray="3 2"/>')
    _arrow(ic, "M2,32H12M8,28L12,32L8,36M62,32H52M56,28L52,32L56,36", "#3fae2a", 2.6)


def insert_row(ic):
    """Add row: a table with a green plus on a new row underneath."""
    _table(ic, 4, 4, 56, 38, (22, 40))
    ic.add('<path d="M4,46H60" stroke="#3fae2a" stroke-width="2" stroke-dasharray="3 2"/>')
    ic.shadow(circle(32, 52, 10), 2, 1.8)
    ic.path(circle(32, 52, 10), ic.rg([(0, "#c8f8a8"), (.55, "#3fae2a"), (1, "#145a0c")], .4, .32, .8), INK, 1.4)
    ic.add('<path d="M32,46.5V57.5M26.5,52H37.5" stroke="#fff" stroke-width="3" stroke-linecap="round"/>')


# ------------------------------------------------------------------ icons inside System Settings pages
CREAM = ("#fffef4", "#fff4c4")


def _win(ic, x, y, w, h, title=("#e4e6e9", "#8a9098"), body=CREAM, shadow=True, op=None):
    d = f"M{x},{y}H{x + w}V{y + h}H{x}Z"
    if shadow:
        ic.shadow(d, 2.4, 2)
    extra = f' fill-opacity="{op}"' if op else ""
    ic.path(d, ic.lg([(0, body[0]), (1, body[1])], 0, 0, 1, 1), INK, LW * 1.2, extra)
    ic.path(f"M{x},{y}H{x + w}V{y + 8}H{x}Z", ic.lg([(0, title[0]), (1, title[1])]), INK, LW * 1.2, extra)
    ic.path(rrect(x + w - 7, y + 2, 5, 4, .8), "#e0281a", INK, .6)


def _badge(ic, x, y, r, colour, glyph):
    cols = {"green": ("#c8f8a8", "#3fae2a", "#145a0c"), "red": ("#ffb0a0", "#e0281a", "#6a0804"),
            "blue": ("#b8dcff", "#2a6ac8", "#0c2a6a"), "amber": ("#ffe8a0", "#ec9a1a", "#7a4404"),
            "grey": ("#ffffff", "#9aa0a8", "#3c4148")}[colour]
    ic.shadow(circle(x, y, r), 1.8, 1.6)
    ic.path(circle(x, y, r), ic.rg([(0, cols[0]), (.55, cols[1]), (1, cols[2])], .4, .32, .8), INK, 1.4)
    ic.add(f'<path d="{glyph}" fill="none" stroke="#000" stroke-opacity=".3" stroke-width="{r * .5 + 1.6:.2f}" stroke-linecap="round" stroke-linejoin="round"/>')
    ic.add(f'<path d="{glyph}" fill="none" stroke="#fff" stroke-width="{r * .5:.2f}" stroke-linecap="round" stroke-linejoin="round"/>')


def _bang_badge(ic, x, y, r, colour):
    """A badge with an exclamation mark drawn as a separate bar and dot, with a clear gap."""
    _badge(ic, x, y, r, colour, "")
    w, top, bot, dr = r * .28, y - r * .62, y + r * .14, r * .17
    for dx, col, op in ((.7, "#000", ' fill-opacity=".3"'), (0, "#ffffff", "")):
        ic.path(rrect(x - w / 2 + dx, top + dx, w, bot - top, w / 2), col, None, op)
        ic.path(circle(x + dx, y + r * .48 + dx, dr), col, None, op)


def keep_above(ic):
    """Keep above others: a window raised over another, with a green up-arrow badge."""
    _win(ic, 4, 20, 36, 30, body=("#e4e6e9", "#b4b9c0"))
    _win(ic, 16, 6, 36, 30)
    _badge(ic, 48, 48, 11, "green", "M48,54V42M42.5,47L48,41.5L53.5,47")


def keep_below(ic):
    """Keep below others: a window sunk beneath another, with a blue down-arrow badge."""
    _win(ic, 16, 6, 36, 30, body=("#e4e6e9", "#b4b9c0"))
    _win(ic, 4, 20, 36, 30, op=".55")
    _win(ic, 4, 20, 36, 30, shadow=False, op=".0")
    _badge(ic, 48, 48, 11, "blue", "M48,41.5V53.5M42.5,48.5L48,54L53.5,48.5")


def shade(ic):
    """Shade: a window rolled up into just its title bar, with an up arrow."""
    ic.shadow("M4,22H60V32H4Z", 2.4, 2)
    ic.path("M4,22H60V32H4Z", ic.lg([(0, "#e4e6e9"), (1, "#8a9098")]), INK, LW * 1.3)
    ic.path(rrect(52, 24.5, 6, 5, .8), "#e0281a", INK, .6)
    ic.add('<path d="M4,34H60" stroke="#8a9098" stroke-width="1.4" stroke-dasharray="3 3"/>')
    _arrow(ic, "M32,58V40M24,47L32,39L40,47", "#2a6ac8", 3.6)


def duplicate(ic):
    """Dialog / duplicate window: two windows offset over one another."""
    _win(ic, 4, 6, 40, 32)
    _win(ic, 20, 24, 40, 32)


def pushpin(ic):
    """Pin: a red map pin pushed in at an angle."""
    ic.add('<g transform="rotate(35 32 32)">')
    ic.add(f'<path d="M32,40V62" stroke="{INK}" stroke-width="3.6" stroke-linecap="round"/><path d="M32,40V61" stroke="#c3c7cd" stroke-width="1.8" stroke-linecap="round"/>')
    ic.path("M22,8H42L38,18V28L46,36V40H18V36L26,28V18Z", ic.lg([(0, "#ffb0a0"), (.5, "#e0281a"), (1, "#6a0804")], 0, 0, 1, 0), INK, LW)
    ic.add('<path d="M26,12H30" stroke="#fff" stroke-opacity=".7" stroke-width="2" stroke-linecap="round"/>')
    ic.add("</g>")


def skip_taskbar(ic):
    """Skip taskbar: a window above a panel, its taskbar button crossed out."""
    _win(ic, 10, 4, 44, 32)
    ic.shadow("M2,44H62V58H2Z", 2.4, 2)
    ic.path("M2,44H62V58H2Z", ic.lg([(0, "#e4e6e9"), (1, "#8a9098")]), INK, LW)
    ic.path(rrect(18, 47, 26, 8, 1.4), ic.lg([(0, "#ffffff"), (1, "#c9ccd1")]), INK, .9)
    _arrow(ic, "M20,58L42,44", "#e0281a", 2.6)


def pager(ic):
    """Virtual desktop: KDE 3's pager - four small desktops, the current one highlighted."""
    for i in range(2):
        for j in range(2):
            x, y = 4 + i * 29, 8 + j * 25
            d = f"M{x},{y}H{x + 27}V{y + 23}H{x}Z"
            ic.shadow(d, 2, 1.8)
            on = (i, j) == (0, 0)
            ic.path(d, ic.lg([(0, "#5a9ae0" if on else "#c9ccd1"), (1, "#1a4a8a" if on else "#7b818a")]), INK, 1.4)
            ic.path(f"M{x + 4},{y + 5}H{x + 17}V{y + 15}H{x + 4}Z", "#ffffff" if on else "#e4e6e9", INK, .8)


def ignore_geometry(ic):
    """Ignore requested geometry: a window with a dashed size frame struck through."""
    ic.add('<path d="M4,4H60V60H4Z" fill="none" stroke="#2a6ac8" stroke-width="1.6" stroke-dasharray="4 3"/>')
    _win(ic, 14, 16, 36, 30)
    _badge(ic, 48, 48, 11, "red", "M42.5,48H53.5")


def opacity(ic):
    """Opacity: a checkerboard showing through a half-transparent blue square."""
    for i in range(4):
        for j in range(4):
            ic.path(f"M{6 + i * 13},{6 + j * 13}h13v13h-13Z", "#ffffff" if (i + j) % 2 else "#a8adb4", None)
    ic.path("M6,6H58V58H6Z", "none", INK, LW)
    ic.path("M18,18H58V58H18Z", "#2a6ac8", INK, LW, ' fill-opacity=".55"')


def block_compositing(ic):
    """Block compositing: two see-through layers stopped by a red badge."""
    for k, c in enumerate(("#9fd4ff", "#b8f0a0")):
        x, y = 4 + k * 12, 6 + k * 10
        ic.shadow(f"M{x},{y}H{x + 36}V{y + 30}H{x}Z", 2, 1.8)
        ic.path(f"M{x},{y}H{x + 36}V{y + 30}H{x}Z", c, INK, LW, ' fill-opacity=".75"')
    _badge(ic, 48, 48, 12, "red", "M42,48H54")


def torn_menu(ic):
    """Torn-off menu: a menu whose top edge is torn along a dashed line."""
    d = "M10,14L16,10L22,14L28,10L34,14L40,10L46,14L52,10V58H10Z"
    ic.shadow(d, 2.4, 2)
    ic.path(d, ic.lg([(0, "#ffffff"), (1, "#e4e6e9")]), INK, LW)
    for k in range(5):
        y = 22 + k * 7
        ic.add(f'<path d="M16,{y}H{44 - (k % 2) * 8}" stroke="#5c6168" stroke-width="2"/>')
    ic.path("M12,34H50V40H12Z", "#3a6ac0", None, ' fill-opacity=".35"')


def splash(ic):
    """Splash screen: a rounded blue panel with a glowing star rising in its middle."""
    d = rrect(4, 10, 56, 44, 6)
    ic.shadow(d, 2.6, 2.2)
    ic.path(d, ic.lg([(0, "#5a9ae0"), (1, "#0c2a6a")], 0, 0, .3, 1), INK, LW)
    ic.path(circle(32, 30, 12), ic.rg([(0, "#ffffff", .9), (1, "#ffffff", 0)], .5, .5, .5), None)
    pts = []
    for k in range(10):
        a = math.radians(-90 + 36 * k)
        r = 9 if k % 2 == 0 else 3.8
        pts.append(f"{32 + r * math.cos(a):.2f},{30 + r * math.sin(a):.2f}")
    ic.path("M" + "L".join(pts) + "Z", ic.rg([(0, "#ffffff"), (1, "#ffd21a")]), INK, .8)
    ic.path(rrect(18, 45, 28, 3.4, 1.6), "#0a1a40", "#9fd4ff", .6)
    ic.path(rrect(18, 45, 16, 3.4, 1.6), "#9fd4ff", None)


def _monitor(ic, x, y, w, h, on=True, content=None):
    ic.path(f"M{x + w / 2 - 4},{y + h}H{x + w / 2 + 4}L{x + w / 2 + 6},{y + h + 5}H{x + w / 2 - 6}Z", "#b4b0a3", INK, .9)
    ic.path(rrect(x, y, w, h, 2), ic.lg([(0, "#fbf9f2"), (1, "#b4b0a3")], 0, 0, .3, 1), INK, LW)
    scr = ic.lg([(0, SCREEN[0]), (1, SCREEN[2])]) if on else ic.lg([(0, "#3c4148"), (1, "#0a0c10")])
    ic.path(rrect(x + 3, y + 3, w - 6, h - 6, 1), scr, INK, .8)
    if content and on:
        content(x + 3, y + 3, w - 6, h - 6)


def _laptop(ic, x, y, w, h, on=True):
    ic.path(f"M{x - 4},{y + h}H{x + w + 4}L{x + w + 6},{y + h + 5}H{x - 6}Z", ic.lg([(0, "#c3c7cd"), (1, "#6c727a")]), INK, LW)
    ic.path(rrect(x, y, w, h, 2), ic.lg([(0, "#5c6168"), (1, "#14171c")]), INK, LW)
    scr = ic.lg([(0, SCREEN[0]), (1, SCREEN[2])]) if on else ic.lg([(0, "#3c4148"), (1, "#0a0c10")])
    ic.path(f"M{x + 3},{y + 3}H{x + w - 3}V{y + h - 3}H{x + 3}Z", scr, INK, .7)


def osd_duplicate(ic):
    """Screens: mirror - two monitors showing the same picture, with an equals sign between."""
    star = lambda x, y, w, h: ic.path(circle(x + w / 2, y + h / 2, h / 3.4), "#ffd21a", INK, .6)
    _monitor(ic, 2, 14, 26, 22, content=star)
    _monitor(ic, 36, 14, 26, 22, content=star)
    ic.add(f'<path d="M29,22H35M29,28H35" stroke="{INK}" stroke-width="2.2" stroke-linecap="round"/>')


def _extend(ic, left):
    a, b = (2, 24) if left else (24, 2)
    _monitor(ic, 24 if left else 2, 12, 38, 28)
    _monitor(ic, 2 if left else 40, 22, 22, 18)
    _arrow(ic, "M42,52H10M18,46L10,52L18,58" if left else "M10,52H54M46,46L54,52L46,58", "#3fae2a", 3.2)


def osd_left(ic):
    """Screens: extend to the left."""
    _extend(ic, True)


def osd_right(ic):
    """Screens: extend to the right."""
    _extend(ic, False)


def osd_laptop_off(ic):
    """Screens: laptop screen off - the laptop dark, the external monitor on."""
    _monitor(ic, 26, 6, 36, 28)
    _laptop(ic, 6, 30, 26, 20, on=False)


def osd_screen_off(ic):
    """Screens: external screen off - the monitor dark, the laptop on."""
    _monitor(ic, 26, 6, 36, 28, on=False)
    _laptop(ic, 6, 30, 26, 20)


def unavailable(ic):
    """Unavailable: a grey no-entry circle with a red bar across."""
    ic.shadow(circle(32, 32, 27), 2.4, 2)
    ic.path(circle(32, 32, 27), ic.rg([(0, "#ffffff"), (1, "#a8adb4")], .4, .35, .8), INK, LW)
    ic.add(f'<path d="M14,14L50,50" stroke="{INK}" stroke-width="10" stroke-linecap="round"/><path d="M14,14L50,50" stroke="#e0281a" stroke-width="7" stroke-linecap="round"/>')
    ic.add(f'<path d="{circle(32, 32, 20.5)}" fill="none" stroke="#e0281a" stroke-width="5"/>')


def crosshairs(ic):
    """Crosshairs: a red target circle with crossing lines."""
    for r, w in ((24, 3.4), (12, 2.4)):
        ic.add(f'<path d="{circle(32, 32, r)}" fill="none" stroke="{INK}" stroke-width="{w + 2}"/><path d="{circle(32, 32, r)}" fill="none" stroke="#e0281a" stroke-width="{w}"/>')
    ic.add(f'<path d="M32,2V22M32,42V62M2,32H22M42,32H62" stroke="{INK}" stroke-width="2.6" stroke-linecap="round"/>')
    ic.path(circle(32, 32, 2.4), INK, None)


def marker(ic):
    """A small downward pointer, used to mark a position on a scale."""
    ic.shadow("M10,14H54L32,52Z", 2.4, 2)
    ic.path("M10,14H54L32,52Z", ic.lg([(0, "#ffd890"), (.5, "#ec9a1a"), (1, "#7a4404")]), INK, LW * 1.3)


def clear_all(ic):
    """Clear all: a pink eraser rubbing out lines of text."""
    for k in range(4):
        ic.add(f'<path d="M6,{12 + k * 9}H{44 - k * 6}" stroke="#5c6168" stroke-width="2.6" stroke-linecap="round" stroke-opacity="{1 - k * .22:.2f}"/>')
    ic.add('<g transform="rotate(-35 42 46)">')
    ic.shadow("M24,38H60V54H24Z", 2.2, 1.8)
    ic.path("M24,38H44V54H24Z", ic.lg([(0, "#ffc8d8"), (1, "#d86088")]), INK, LW)
    ic.path("M44,38H60V54H44Z", ic.lg([(0, "#9fd4ff"), (1, "#2a6ac8")]), INK, LW)
    ic.add("</g>")


def pause_badge(ic):
    """Paused: an amber badge with two white bars, a clear gap between them."""
    _badge(ic, 32, 32, 27, "amber", "")
    for x in (21.5, 35.5):
        ic.path(rrect(x + .8, 19.8, 7, 25.6, 1.6), "#000", None, ' fill-opacity=".3"')
        ic.path(rrect(x, 19, 7, 25.6, 1.6), "#ffffff", None)


def get_new_stuff(ic):
    """Get New Stuff: the tied parcel with a gold sparkle bursting from it."""
    from discover import parcel
    ic.add('<g transform="translate(-2,6) scale(.86)">')
    parcel(ic)
    ic.add("</g>")
    pts = []
    for k in range(16):
        a = math.radians(-90 + 22.5 * k)
        r = 12 if k % 2 == 0 else 5
        pts.append(f"{48 + r * math.cos(a):.2f},{16 + r * math.sin(a):.2f}")
    d = "M" + "L".join(pts) + "Z"
    ic.shadow(d, 1.8, 1.6)
    ic.path(d, ic.rg([(0, "#ffffff"), (.35, "#fff36a"), (1, "#e8a010")], .45, .45, .7), "#7a4404", 1.1)


def mouse_left_click(ic):
    """Left click: a mouse with its left button lit up in blue."""
    body = "M18,10Q32,4 46,10Q54,14 54,30V44Q54,60 32,60Q10,60 10,44V30Q10,14 18,10Z"
    ic.shadow(body, 2.6, 2.2)
    ic.path(body, ic.lg([(0, "#ffffff"), (1, "#b4b9c0")], 0, 0, 1, 1), INK, LW)
    ic.path("M32,6.6V30H10Q10,14 18,10Q24,7 32,6.6Z", ic.lg([(0, "#9fd4ff"), (1, "#1a5ac8")]), INK, LW)
    ic.add(f'<path d="M10,30H54M32,30V6.6" stroke="{INK}" stroke-width="1.4"/>')
    ic.path(rrect(29.5, 13, 5, 10, 2.4), "#3c4148", INK, .8)


def new_message(ic):
    """New message (sound): an envelope with a gold star on its corner."""
    ic.shadow("M4,16H54V52H4Z", 2.4, 2)
    ic.path("M4,16H54V52H4Z", ic.lg([(0, "#ffffff"), (1, "#d9dce0")]), INK, LW)
    ic.add(f'<path d="M4,16L29,36L54,16M4,52L22,32M54,52L36,32" fill="none" stroke="{INK}" stroke-width="1.2" stroke-linejoin="round"/>')
    pts = []
    for k in range(10):
        a = math.radians(-90 + 36 * k)
        r = 11 if k % 2 == 0 else 4.6
        pts.append(f"{50 + r * math.cos(a):.2f},{14 + r * math.sin(a):.2f}")
    ic.path("M" + "L".join(pts) + "Z", ic.rg([(0, "#fffbe0"), (.45, "#ffd21a"), (1, "#c87a04")]), INK, 1.1)


def locked_package(ic):
    """Not available: the tied parcel with a padlock."""
    from discover import parcel
    from dolphin import locked
    parcel(ic)
    ic.add('<g transform="translate(34,34) scale(.46)">')
    locked(ic)
    ic.add("</g>")


def unknown(ic):
    """Unknown: a grey tile with a white question mark."""
    t = rrect(6, 6, 52, 52, 10)
    ic.shadow(t, 2.4, 2)
    ic.path(t, ic.lg([(0, "#c3c7cd"), (1, "#5c6168")]), INK, LW)
    _arrow(ic, "M23,24Q23,14 32,14Q41,14 41,23Q41,29 34,32Q32,33 32,38", "#ffffff", 5)
    ic.path(circle(32, 47, 3.6), "#ffffff", INK, 1)


def energy_monitor(ic):
    """Energy information: a graph screen with a yellow lightning bolt."""
    ic.shadow("M4,8H60V52H4Z", 2.4, 2)
    ic.path("M4,8H60V52H4Z", ic.lg([(0, "#3c4148"), (1, "#0a0c10")]), INK, LW)
    grid = "".join(f"M4,{8 + k * 11}H60" for k in range(1, 4)) + "".join(f"M{4 + k * 14},8V52" for k in range(1, 4))
    ic.add(f'<path d="{grid}" stroke="#3aa83a" stroke-opacity=".4" stroke-width=".8"/>')
    ic.add('<path d="M6,44L16,40L24,42L32,28L40,32L48,18L58,22" fill="none" stroke="#7ae07a" stroke-width="2.4" stroke-linejoin="round"/>')
    bolt = "M36,26L24,48H32L28,62L46,36H36L42,26Z"
    ic.shadow(bolt, 1.8, 1.6)
    ic.path(bolt, ic.lg([(0, "#fffbe0"), (.5, "#ffd21a"), (1, "#c87a04")]), INK, 1.3)


def reconnect(ic):
    """Repeat / reconnect: two blue arrows chasing each other round."""
    for a0, a1 in ((200, 340), (20, 160)):
        r = 20
        p0 = (32 + r * math.cos(math.radians(a0)), 32 + r * math.sin(math.radians(a0)))
        p1 = (32 + r * math.cos(math.radians(a1)), 32 + r * math.sin(math.radians(a1)))
        _arrow(ic, f"M{p0[0]:.2f},{p0[1]:.2f}A{r},{r} 0 0 1 {p1[0]:.2f},{p1[1]:.2f}", "#2a6ac8", 5)
        t = math.radians(a1)
        tx, ty, nx, ny = -math.sin(t), math.cos(t), math.cos(t), math.sin(t)
        tip = (p1[0] + tx * 9, p1[1] + ty * 9)
        b1, b2 = (p1[0] + nx * 8, p1[1] + ny * 8), (p1[0] - nx * 8, p1[1] - ny * 8)
        ic.path(f"M{tip[0]:.2f},{tip[1]:.2f}L{b1[0]:.2f},{b1[1]:.2f}L{b2[0]:.2f},{b2[1]:.2f}Z", ic.lg([(0, "#b8dcff"), (1, "#0c2a6a")]), INK, 1.3)


def new_script(ic):
    """New command or script: a script page with a green plus badge."""
    page = "M6,4H34L44,14V58H6Z"
    ic.shadow(page, 2.4, 2)
    ic.path(page, ic.lg([(0, "#ffffff"), (1, "#e2e4e8")]), INK, LW)
    ic.path("M34,4V14H44", "#d9dce0", INK, 1)
    ic.add('<path d="M11,20L16,24L11,28M19,28H30" fill="none" stroke="#2f8a1e" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>')
    for k in range(3):
        ic.add(f'<path d="M11,{36 + k * 5}H{36 - k * 7}" stroke="#7b818a" stroke-width="1.4"/>')
    _badge(ic, 48, 48, 12, "green", "M48,41.5V54.5M41.5,48H54.5")


def magnifier(ic):
    """Search: a magnifying glass with a wooden handle."""
    cx, cy, r = 26, 26, 16
    ic.add(f'<path d="M{cx + 11},{cy + 11}L56,56" stroke="{INK}" stroke-width="11" stroke-linecap="round"/>')
    ic.add(f'<path d="M{cx + 11},{cy + 11}L56,56" stroke="#8a5a2a" stroke-width="7.6" stroke-linecap="round"/>')
    ic.shadow(circle(cx, cy, r + 4), 2.2, 1.8)
    ic.path(circle(cx, cy, r + 4), ic.lg([(0, "#ffffff"), (1, "#7b818a")], 0, 0, 1, 1), INK, LW)
    ic.path(circle(cx, cy, r), ic.rg([(0, "#e8f6ff"), (1, "#9ad0f0")], .35, .3, .8), INK, 1, ' fill-opacity=".85"')
    ic.add(f'<path d="M{cx - 9},{cy - 2}Q{cx - 8},{cy - 9} {cx - 1},{cy - 10}" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round"/>')


def connector(ic):
    """Direct connection: a grey cable plug."""
    ic.add(f'<path d="M32,40V52Q32,60 24,60H8" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>')
    ic.add('<path d="M32,40V52Q32,60 24,60H8" fill="none" stroke="#5c6168" stroke-width="3.6" stroke-linecap="round"/>')
    for x in (24, 36):
        ic.path(rrect(x, 4, 4, 14, 1), ic.lg([(0, "#fff0a0"), (.5, "#e8b830"), (1, "#8a5a04")], 0, 0, 1, 0), INK, 1)
    body = "M16,16H48V30Q48,42 32,42Q16,42 16,30Z"
    ic.shadow(body, 2.2, 1.8)
    ic.path(body, ic.lg([(0, "#e4e6e9"), (.5, "#a8adb4"), (1, "#4c5158")], 0, 0, 1, 1), INK, LW)
    ic.add('<path d="M20,20H44" stroke="#fff" stroke-width="1.6" stroke-linecap="round"/>')


def minus(ic):
    """Remove / decrease (list-remove, remove, value-decrease): the red minus badge, as on emblem-remove
    (2026-10-27). The old black bar is kept as minus_dark() and alt/list-remove-dark.svg."""
    from dolphin import vcs_removed
    vcs_removed(ic)


def minus_dark(ic):
    """The previous Remove icon: a black minus bar (kept on record, not built)."""
    d = "M8,26H56V38H8Z"
    ic.shadow(d, 2.4, 2)
    ic.path(d, ic.lg([(0, "#4c5158"), (1, "#0a0c10")], 0, 0, 1, 1), INK, LW)
    ic.add('<path d="M11,28.4H53" stroke="#fff" stroke-opacity=".45" stroke-width="1.4"/>')


def video_clip(ic):
    """Video preview: a strip of film with a white play triangle on it."""
    ic.shadow("M4,12H60V52H4Z", 2.4, 2)
    ic.path("M4,12H60V52H4Z", ic.lg([(0, "#3a3f46"), (1, "#101214")]), INK, LW)
    for k in range(8):
        x = 7 + k * 6.8
        ic.add(f'<rect x="{x:.1f}" y="14.5" width="3.6" height="3.4" rx=".6" fill="#f4f4f4"/><rect x="{x:.1f}" y="46" width="3.6" height="3.4" rx=".6" fill="#f4f4f4"/>')
    ic.path("M8,21H56V43H8Z", ic.lg([(0, "#bfe8ff"), (1, "#4aa2e0")]), INK, 1)
    ic.path("M26,24L42,32L26,40Z", "#ffffff", INK, 1.2)


def equalizer(ic):
    """Equaliser: five sliders set to a curve."""
    ic.shadow("M4,6H60V58H4Z", 2.4, 2)
    ic.path(rrect(4, 6, 56, 52, 3), ic.lg([(0, "#5c6168"), (1, "#14171c")]), INK, LW)
    for k, v in enumerate((34, 22, 16, 26, 38)):
        x = 13 + k * 9.5
        ic.add(f'<path d="M{x},12V52" stroke="#0a0c10" stroke-width="3" stroke-linecap="round"/>')
        ic.path(rrect(x - 4, v - 3, 8, 6, 1.4), ic.lg([(0, "#ffffff"), (1, "#8a9098")]), INK, .9)
        ic.add(f'<path d="M{x},{v + 3}V52" stroke="#3fae2a" stroke-width="2" stroke-linecap="round"/>')


def tasks(ic):
    """Tasks / jobs: a checklist with green ticks."""
    ic.shadow("M10,4H54V60H10Z", 2.4, 2)
    ic.path("M10,4H54V60H10Z", ic.lg([(0, "#ffffff"), (1, "#e4e6e9")]), INK, LW)
    for k in range(4):
        y = 12 + k * 12
        ic.path(f"M15,{y}H23V{y + 8}H15Z", "#ffffff", INK, 1.1)
        if k < 3:
            ic.add(f'<path d="M16.5,{y + 4}L19,{y + 6.5}L24,{y - 1}" fill="none" stroke="#2f8a1e" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>')
        ic.add(f'<path d="M28,{y + 4}H{48 - (k % 2) * 6}" stroke="#5c6168" stroke-width="1.6"/>')


def log_viewer(ic):
    """Logs: a ruled page of timestamped lines under a small clock."""
    ic.shadow("M8,8H52V60H8Z", 2.4, 2)
    ic.path("M8,8H52V60H8Z", ic.lg([(0, "#fffef4"), (1, "#fff0c0")]), INK, LW)
    for k in range(6):
        y = 22 + k * 6
        ic.add(f'<path d="M12,{y}H19" stroke="#2a6ac8" stroke-width="1.6"/><path d="M22,{y}H{46 - (k % 3) * 6}" stroke="#5c6168" stroke-width="1.4"/>')
    ic.shadow(circle(46, 12, 9), 1.8, 1.6)
    ic.path(circle(46, 12, 9), ic.rg([(0, "#ffffff"), (1, "#c9ccd1")]), INK, 1.2)
    ic.add(f'<path d="M46,12V7M46,12L49.5,13.6" stroke="{INK}" stroke-width="1.6" stroke-linecap="round"/>')


def _map_zoom(ic, plus):
    ic.shadow("M4,10L22,4L40,10L58,4V50L40,56L22,50L4,56Z", 2.4, 2)
    ic.path("M4,10L22,4V50L4,56Z", ic.lg([(0, "#c8f0a0"), (1, "#6aa83a")]), INK, 1.2)
    ic.path("M22,4L40,10V56L22,50Z", ic.lg([(0, "#bfe8ff"), (1, "#4aa2e0")]), INK, 1.2)
    ic.path("M40,10L58,4V50L40,56Z", ic.lg([(0, "#fff0b0"), (1, "#d8b448")]), INK, 1.2)
    _badge(ic, 46, 46, 13, "blue", "M40,46H52" + ("M46,40V52" if plus else ""))


def map_zoom_in(ic): _map_zoom(ic, True)
def map_zoom_out(ic): _map_zoom(ic, False)


SHELL = {
    "panel-fit-width": panel_fit_width, "panel-fit-height": panel_fit_height, "kdenlive-custom-effect": panel_custom,
    "overflow-menu": overflow_menu, "open-menu": hamburger, "show-background": show_background,
    "view-filter": funnel, "object-rows": arrange_rows, "dashboard-show": dashboard,
    "org.kde.plasma.folder": widget_folder, "org.kde.plasma.systemtray": widget_tray,
    "org.kde.plasma.clipboard": clipboard, "org.kde.plasma.analogclock": analog_clock,
    "system-user-list": user_list, "keyboard-layout": keyboard_layout, "speedometer": speedometer,
    "phone-battery": phone_battery, "video-card-inactive": software_rendering, "edit-bomb": bomb,
    "view-private": mask, "face-in-love": in_love, "view-split-top-bottom": split_top_bottom,
    "transform-browse": pointer, "transform-crop": crop, "edit-select": select_area, "draw-highlight": highlighter,
    "draw-line": draw_line, "draw-arrow": draw_arrow, "draw-rectangle": draw_rect, "draw-ellipse": draw_ellipse,
    "pixelate": pixelate, "blur": blur, "draw-text": draw_text, "draw-number": draw_number, "camera-video": video_camera,
    "handle-sort": sort_handle, "hide_table_column": hide_column, "send_signal": send_signal,
    "view-process-own": proc_own, "view-process-users": proc_users, "view-process-all": proc_all,
    "trim-margins": trim_margins, "edit-table-insert-row-under": insert_row,
    "window-keep-above": keep_above, "window-keep-below": keep_below, "window-shade": shade, "window-duplicate": duplicate,
    "window-pin": pushpin, "kt-show-statusbar": skip_taskbar, "org.kde.plasma.pager": pager,
    "view-time-schedule-baselined-remove": ignore_geometry, "edit-opacity": opacity, "composite-track-on": block_compositing,
    "overflow-menu-left": torn_menu, "embosstool": splash, "osd-duplicate": osd_duplicate, "osd-sbs-left": osd_left,
    "osd-sbs-sright": osd_right, "osd-shutd-laptop": osd_laptop_off, "osd-shutd-screen": osd_screen_off,
    "action-unavailable": unavailable, "crosshairs": crosshairs, "draw-triangle4": marker, "edit-clear-all": clear_all,
    "emblem-pause": pause_badge, "get-hot-new-stuff": get_new_stuff, "input-mouse-click-left": mouse_left_click,
    "message-new": new_message, "package-available-locked": locked_package, "paint-unknown": unknown,
    "utilities-energy-monitor": energy_monitor, "repeat": reconnect, "scriptnew": new_script, "search": magnifier,
    "standard-connector": connector, "value-decrease": minus, "videoclip-amarok": video_clip,
    "view-media-equalizer": equalizer, "view-pim-tasks": tasks, "viewlog": log_viewer,
    "zoom-in-map": map_zoom_in, "zoom-out-map": map_zoom_out,
}
SHELL_ALIASES = {
    "open-menu-symbolic": "open-menu", "application-menu": "open-menu", "overflow-menu-symbolic": "overflow-menu",
    "preferences-desktop-filter": "view-filter", "view-filter-symbolic": "view-filter", "edit-bomb-symbolic": "edit-bomb",
    "klipper": "org.kde.plasma.clipboard", "org.kde.klipper": "org.kde.plasma.clipboard", "edit-paste-in-place": "org.kde.plasma.clipboard",
    "preferences-system-time-analog": "org.kde.plasma.analogclock", "dashboard": "dashboard-show",
    "view-split-top-bottom-symbolic": "view-split-top-bottom", "speedometer-symbolic": "speedometer",
    "input-keyboard-layout": "keyboard-layout", "private-browsing": "view-private", "phone-battery-symbolic": "phone-battery",
    "send_signal-symbolic": "send_signal", "process-stop-signal": "send_signal", "camera-video-symbolic": "camera-video",
    "media-record-video": "camera-video", "draw-square": "draw-rectangle", "draw-circle": "draw-ellipse", "draw-arrow-forward": "draw-arrow",
    "edit-select-symbolic": "edit-select", "transform-crop-and-resize": "transform-crop", "insert-text": "draw-text",
    "action-unavailable-symbolic": "action-unavailable", "emblem-unavailable": "action-unavailable", "edit-none": "action-unavailable",
    "draw-triangle4-symbolic": "draw-triangle4", "edit-clear-all-symbolic": "edit-clear-all", "emblem-paused": "emblem-pause",
    "knewstuff": "get-hot-new-stuff", "input-mouse-click-left-symbolic": "input-mouse-click-left", "mail-message-new-sound": "message-new",
    "scriptnew-symbolic": "scriptnew", "search-symbolic": "search", "standard-connector-symbolic": "standard-connector",
    "value-decrease-symbolic": "value-decrease", "zoom-in-map-symbolic": "zoom-in-map", "zoom-out-map-symbolic": "zoom-out-map",
    "window-pin-symbolic": "window-pin", "pin": "window-pin", "window-unpin": "window-pin", "view-refresh-symbolic": "repeat",
    "window-keep-above-symbolic": "window-keep-above", "window-keep-below-symbolic": "window-keep-below",
}
# names that are the same picture as one drawn elsewhere in the theme
SHELL_CROSS = {
    "view-hidden-symbolic": "../actions/view-hidden.svg", "password-show-off": "../actions/view-hidden.svg",
    "password-show-on": "../actions/view-visible.svg", "value-increase": "../actions/list-add.svg",
    "favorite-symbolic": "../emblems/starred.svg", "knetattach": "../places/folder-remote.svg",
    "homerun": "../apps/applications-all.svg",
    "cursor-arrow": "../actions/transform-browse.svg", "font-select-symbolic": "../apps/preferences-desktop-font.svg",
    "edit-delete-remove": "../emblems/vcs-removed.svg", "edit-delete-remove-symbolic": "../emblems/vcs-removed.svg",
    "messagebox_warning": "../emblems/vcs-conflicting.svg",
}


# -symbolic names Plasma asks for whose full-colour icon we already have. Without these, the inherited
# Breeze theme answers the exact -symbolic name first and our drawing is never used.
SYMBOLIC = {
    "edit-clear-locationbar-ltr-symbolic": "actions/edit-clear-locationbar-ltr", "edit-clear-locationbar-rtl-symbolic": "actions/edit-clear-locationbar-rtl",
    "edit-reset-symbolic": "actions/edit-reset", "view-visible-symbolic": "actions/view-visible",
    "document-open-folder-symbolic": "places/folder-open", "folder-open-symbolic": "places/folder-open",
    "trash-empty-symbolic": "places/user-trash", "lock-symbolic": "actions/system-lock-screen",
    "non-starred-symbolic": "actions/rating-unrated", "home": "places/user-home", "image-missing": "mimetypes/image-x-generic",
    "network-wireless-bluetooth-symbolic": "apps/preferences-system-bluetooth", "emblem-information": "apps/dialog-information",
}


def write(out):
    d = f"{out}/scalable/actions"
    os.makedirs(d, exist_ok=True)
    for name, fn in SHELL.items():
        open(f"{d}/{name}.svg", "w").write(_ic(fn)().svg(64))
    for a, t in SHELL_ALIASES.items():
        if not os.path.exists(f"{d}/{a}.svg"):
            os.symlink(f"{t}.svg", f"{d}/{a}.svg")
    for a, t in SHELL_CROSS.items():
        if not os.path.exists(f"{d}/{a}.svg"):
            os.symlink(t, f"{d}/{a}.svg")
    for a, t in SYMBOLIC.items():
        if os.path.exists(f"{out}/scalable/{t}.svg") and not os.path.exists(f"{d}/{a}.svg"):
            os.symlink(f"../{t}.svg", f"{d}/{a}.svg")
    return len(SHELL)
