"""KDE Classic Vector: panel and system tray icons - widgets, devices, media, status indicators.

Note: a Plasma Style may ship its own copies of some tray icons (Breeze does); with a style that doesn't,
such as Nova7, these icon-theme drawings are what the panel shows.
"""
import math, os
from gen import Icon, INK, LW, circle, rrect, e_globe
from shell import _arrow, _badge, _win, _mini, _bang_badge


def _ic(fn):
    def f():
        ic = Icon()
        fn(ic)
        return ic
    return f


def _star(cx, cy, r1, r2, n=5):
    return "M" + "L".join(f"{cx + (r1 if k % 2 == 0 else r2) * math.cos(math.radians(-90 + 180 * k / n)):.2f},"
                          f"{cy + (r1 if k % 2 == 0 else r2) * math.sin(math.radians(-90 + 180 * k / n)):.2f}" for k in range(2 * n)) + "Z"


# ------------------------------------------------------------------ power profiles and disk quota
def perf_profile(ic):
    """Performance power profile: the dial with its needle swung right round into the red."""
    from shell import speedometer
    speedometer(ic)
    ic.path(circle(48, 18, 9), ic.rg([(0, "#ffb0a0"), (.55, "#e0281a"), (1, "#6a0804")], .4, .32, .8), INK, 1.2)
    ic.path("M49,12L45,19H48.5L46.5,24L52,16.5H48.6L50.6,12Z", "#fff", None)


def powersave_profile(ic):
    """Power saver profile: a green leaf."""
    d = "M10,54C8,30 24,10 56,8C58,38 40,56 10,54Z"
    ic.shadow(d, 2.6, 2.2)
    ic.path(d, ic.lg([(0, "#c8f8a8"), (.5, "#3fae2a"), (1, "#145a0c")], 0, 0, 1, 1), INK, LW)
    ic.add('<path d="M10,54Q28,34 50,14M24,40L22,28M32,32L36,22M36,28L46,28M26,38L36,40" fill="none" stroke="#e0ffd0" stroke-width="1.6" stroke-linecap="round"/>')


def _quota(ic, level):
    """Disk quota: a disc showing how full it is - green, amber or red."""
    cx, cy, r = 32, 32, 26
    ic.shadow(circle(cx, cy, r), 2.6, 2.2)
    ic.path(circle(cx, cy, r), ic.rg([(0, "#ffffff"), (1, "#c3c7cd")], .4, .35, .8), INK, LW)
    frac, col = {"low": (.3, ("#c8f8a8", "#2f8a1e")), "": (.55, ("#c8f8a8", "#2f8a1e")), "high": (.78, ("#ffe8a0", "#c87a04")),
                 "critical": (.95, ("#ffb0a0", "#c8180c"))}[level]
    a = -math.pi / 2 + 2 * math.pi * frac
    x, y = cx + (r - 4) * math.cos(a), cy + (r - 4) * math.sin(a)
    big = 1 if frac > .5 else 0
    ic.path(f"M{cx},{cy}V{cy - r + 4}A{r - 4},{r - 4} 0 {big} 1 {x:.2f},{y:.2f}Z", ic.lg([(0, col[0]), (1, col[1])], 0, 0, 1, 1), INK, 1)
    ic.path(circle(cx, cy, 6), ic.rg([(0, "#ffffff"), (1, "#8a9098")]), INK, 1)


def quota(ic): _quota(ic, "")
def quota_low(ic): _quota(ic, "low")
def quota_high(ic): _quota(ic, "high")
def quota_critical(ic): _quota(ic, "critical")


# ------------------------------------------------------------------ camera, microphone, audio devices
def _webcam(ic, state):
    """Camera indicator: a round webcam on its stand - red light when in use, struck through when off."""
    ic.path("M24,52H40L44,58H20Z", ic.lg([(0, "#8a9098"), (1, "#2c3036")]), INK, 1.2)
    ic.path("M30,42H34V52H30Z", "#3c4148", INK, 1)
    ic.shadow(circle(32, 26, 20), 2.6, 2.2)
    ic.path(circle(32, 26, 20), ic.lg([(0, "#ffffff"), (1, "#a8adb4")], 0, 0, 1, 1), INK, LW)
    ic.path(circle(32, 26, 11), ic.rg([(0, "#9fd4ff"), (.5, "#1a3ea8"), (1, "#060a20")], .35, .3, .8), INK, 1.2)
    ic.path(circle(28, 22, 3), "#ffffff", None, ' fill-opacity=".8"')
    led = {"on": "#ff3020", "ready": "#9aa0a8", "off": "#9aa0a8"}[state]
    ic.path(circle(46, 12, 3), led, INK, .8)
    if state == "off":
        _arrow(ic, "M10,50L54,6", "#e0281a", 3.6)


def cam_on(ic): _webcam(ic, "on")
def cam_ready(ic): _webcam(ic, "ready")
def cam_off(ic): _webcam(ic, "off")


def _mic(ic, live):
    """Microphone: a silver stage mic - a green light when it is live."""
    ic.add(f'<path d="M16,30Q16,46 32,46Q48,46 48,30" fill="none" stroke="{INK}" stroke-width="5"/><path d="M16,30Q16,46 32,46Q48,46 48,30" fill="none" stroke="#a8adb4" stroke-width="2.8"/>')
    ic.path("M30,46H34V56H30ZM20,56H44V60H20Z", "#5c6168", INK, 1)
    head = rrect(22, 4, 20, 34, 10)
    ic.shadow(head, 2.4, 2)
    ic.path(head, ic.lg([(0, "#5c6168"), (.4, "#e4e6e9"), (1, "#3c4148")], 0, 0, 1, 0), INK, LW)
    for y in (12, 17, 22, 27):
        ic.add(f'<path d="M24,{y}H40" stroke="#3c4148" stroke-width="1" stroke-opacity=".6"/>')
    if live:
        ic.path(circle(48, 12, 5), ic.rg([(0, "#c8f8a8"), (1, "#1e7a10")]), INK, 1)


def mic_on(ic): _mic(ic, True)
def mic_ready(ic): _mic(ic, False)


def headset(ic):
    """Headset: headphones with a boom microphone."""
    from discover import headphones
    headphones(ic)
    ic.add(f'<path d="M12,52Q16,60 30,58" fill="none" stroke="{INK}" stroke-width="4.4" stroke-linecap="round"/><path d="M12,52Q16,60 30,58" fill="none" stroke="#6c727a" stroke-width="2.4" stroke-linecap="round"/>')
    ic.path(rrect(28, 54.5, 8, 7, 3), ic.lg([(0, "#5c6168"), (1, "#0a0c10")]), INK, 1)


def hands_free(ic):
    """Hands-free: a phone with sound waves coming from it."""
    ph = rrect(10, 6, 26, 52, 5)
    ic.shadow(ph, 2.4, 2)
    ic.path(ph, ic.lg([(0, "#5c6168"), (1, "#14171c")], 0, 0, 1, 0), INK, LW)
    ic.path("M14,12H32V46H14Z", ic.lg([(0, "#e8f6ff"), (1, "#9ac8e8")]), INK, .8)
    for k, r in enumerate((10, 17)):
        ic.add(f'<path d="M{42 + k * 3},{32 - r}Q{50 + r},32 {42 + k * 3},{32 + r}" fill="none" stroke="{INK}" stroke-width="3.6" stroke-linecap="round"/>'
               f'<path d="M{42 + k * 3},{32 - r}Q{50 + r},32 {42 + k * 3},{32 + r}" fill="none" stroke="#3ab8d8" stroke-width="2" stroke-linecap="round"/>')


def hifi(ic):
    """Hi-fi: the speaker cabinet on its own."""
    from settings import system_sounds
    system_sounds(ic, "")


# ------------------------------------------------------------------ keyboard indicator, timer, little widgets
def _lock_key(ic, label):
    """Caps / Num Lock: a keycap with its letter and a lit green lock light."""
    from filetypes import PIXEL_FONT
    cap = rrect(8, 10, 48, 46, 8)
    ic.shadow(cap, 2.6, 2.2)
    ic.path(cap, ic.lg([(0, "#ffffff"), (1, "#c9c5b8")], 0, 0, .4, 1), INK, LW)
    ic.path(rrect(14, 14, 36, 34, 6), ic.lg([(0, "#fbf9f2"), (1, "#e4e0d4")]), "#a8a497", 1)
    if label == "A":
        _arrow(ic, "M20,42L28,20L36,42M23,35H33", "#2c3036", 3.4)
    else:
        _arrow(ic, "M22,26L28,20V42M22,42H34", "#2c3036", 3.4)
    ic.path(circle(44, 22, 4.4), ic.rg([(0, "#d8ffc0"), (1, "#1e9a10")]), INK, 1)


def caps_lock(ic): _lock_key(ic, "A")
def num_lock(ic): _lock_key(ic, "1")


def _stopwatch(ic, playing):
    from dolphin import e_clock
    ic.add('<g transform="translate(-3,-31) scale(1.42)">')
    e_clock(ic)
    ic.add("</g>")
    if playing:
        _badge(ic, 48, 48, 12, "green", "M45,42.5L53,48L45,53.5Z")
    else:
        _badge(ic, 48, 48, 12, "amber", "")
        for x in (42.6, 49.4):                     # two bars with a clear gap
            ic.path(rrect(x, 42, 4, 12, 1), "#ffffff", INK, .5)


def timer_start(ic): _stopwatch(ic, True)
def timer_pause(ic): _stopwatch(ic, False)


def compass(ic):
    """Compass: a brass compass with its red and white needle."""
    ic.shadow(circle(32, 32, 27), 2.6, 2.2)
    ic.path(circle(32, 32, 27), ic.lg([(0, "#fff4b0"), (.5, "#d8b040"), (1, "#6a5410")], 0, 0, 1, 1), INK, LW)
    ic.path(circle(32, 32, 22), ic.rg([(0, "#ffffff"), (1, "#e4e6e9")]), INK, 1)
    for k in range(8):
        a = math.radians(45 * k)
        r1 = 16 if k % 2 == 0 else 18
        ic.add(f'<path d="M{32 + r1 * math.sin(a):.2f},{32 - r1 * math.cos(a):.2f}L{32 + 21 * math.sin(a):.2f},{32 - 21 * math.cos(a):.2f}" stroke="{INK}" stroke-width="{1.4 if k % 2 == 0 else .8}"/>')
    ic.path("M32,12L37,32H27Z", "#e0281a", INK, 1)
    ic.path("M32,52L37,32H27Z", "#ffffff", INK, 1)
    ic.path(circle(32, 32, 2.4), "#3c4148", None)


def black_flag(ic):
    ic.add(f'<path d="M14,6V60" stroke="{INK}" stroke-width="4.4" stroke-linecap="round"/><path d="M14,6V60" stroke="#8a9098" stroke-width="2.4" stroke-linecap="round"/>')
    d = "M16,8Q26,4 36,9Q46,14 56,9V34Q46,39 36,34Q26,29 16,33Z"
    ic.shadow(d, 2.4, 2)
    ic.path(d, ic.lg([(0, "#5c6168"), (1, "#0a0c10")], 0, 0, 1, 1), INK, LW)


def pie_chart(ic):
    """Pie chart: four coloured slices, one pulled out."""
    cx, cy, r = 30, 34, 24
    slices = ((0, .35, "#3d9ad8"), (.35, .6, "#4fae5a"), (.6, .82, "#e8c43a"), (.82, 1, "#d8573d"))
    for k, (a0, a1, c) in enumerate(slices):
        t0, t1 = -math.pi / 2 + 2 * math.pi * a0, -math.pi / 2 + 2 * math.pi * a1
        off = 5 if k == 3 else 0
        mx, my = math.cos((t0 + t1) / 2) * off, math.sin((t0 + t1) / 2) * off
        p0 = (cx + mx + r * math.cos(t0), cy + my + r * math.sin(t0))
        p1 = (cx + mx + r * math.cos(t1), cy + my + r * math.sin(t1))
        d = f"M{cx + mx:.2f},{cy + my:.2f}L{p0[0]:.2f},{p0[1]:.2f}A{r},{r} 0 {1 if a1 - a0 > .5 else 0} 1 {p1[0]:.2f},{p1[1]:.2f}Z"
        ic.shadow(d, 2, 1.8)
        ic.path(d, ic.lg([(0, "#ffffff"), (.35, c), (1, c)], 0, 0, 1, 1), INK, 1.2)


def alternatives(ic):
    """Widget alternatives: two widget tiles with arrows swapping them."""
    for x, y, c in ((4, 6, "#9fd4ff"), (34, 30, "#b8f0a0")):
        d = rrect(x, y, 26, 26, 4)
        ic.shadow(d, 2, 1.8)
        ic.path(d, ic.lg([(0, "#ffffff"), (1, c)], 0, 0, 1, 1), INK, LW)
    _arrow(ic, "M38,10Q54,10 54,24M50,20L54,25L58,20", "#3fae2a", 2.6)
    _arrow(ic, "M26,54Q10,54 10,40M6,44L10,39L14,44", "#2a6ac8", 2.6)


def global_menu(ic):
    """Global menu: a menu bar with a menu dropped down from it."""
    ic.shadow("M2,8H62V18H2Z", 2.4, 2)
    ic.path("M2,8H62V18H2Z", ic.lg([(0, "#e4e6e9"), (1, "#a8adb4")]), INK, LW)
    for x0, x1 in ((6, 14), (20, 30), (36, 44)):
        ic.add(f'<path d="M{x0},13H{x1}" stroke="#2c3036" stroke-width="2"/>')
    ic.path("M18,18H40V18H18Z", "#3a6ac0", None)
    ic.path("M17,17H33V19H17Z", "#3a6ac0", None)
    ic.shadow("M17,19H46V56H17Z", 2.4, 2)
    ic.path("M17,19H46V56H17Z", ic.lg([(0, "#ffffff"), (1, "#e4e6e9")]), INK, LW)
    for k in range(4):
        ic.add(f'<path d="M22,{27 + k * 8}H{40 - (k % 2) * 6}" stroke="#5c6168" stroke-width="1.8"/>')
    ic.path("M18,33H45V39H18Z", "#3a6ac0", None, ' fill-opacity=".4"')


def plasmoid(ic):
    """A Plasma widget: a rounded panel holding three little widgets."""
    t = rrect(4, 6, 56, 52, 8)
    ic.shadow(t, 2.6, 2.2)
    ic.path(t, ic.lg([(0, "#f4f5f6"), (1, "#b4b9c0")], 0, 0, .3, 1), INK, LW)
    ic.path(circle(20, 22, 8), "#ffffff", INK, 1)
    ic.add(f'<path d="M20,22V16.5M20,22L24,24" stroke="{INK}" stroke-width="1.4" stroke-linecap="round"/>')
    ic.path(rrect(32, 14, 22, 16, 2), "#fff8c0", INK, 1)
    ic.path(rrect(10, 36, 44, 16, 2), "#ffffff", INK, 1)
    for k, h in enumerate((5, 9, 7, 11, 8, 6)):
        ic.path(f"M{14 + k * 6.5},{49 - h}h4v{h}h-4Z", "#4fae5a", None)


def record(ic):
    """Record: a glossy red recording dot."""
    ic.shadow(circle(32, 32, 24), 2.6, 2.2)
    ic.path(circle(32, 32, 24), ic.rg([(0, "#ffc8c0"), (.5, "#e0281a"), (1, "#6a0804")], .38, .32, .8), INK, LW * 1.3)
    ic.add('<path d="M18,26Q20,14 32,12" fill="none" stroke="#fff" stroke-opacity=".7" stroke-width="3" stroke-linecap="round"/>')


def qr_code(ic):
    """QR code: three square finder marks and a scatter of modules."""
    ic.shadow("M4,4H60V60H4Z", 2.4, 2)
    ic.path("M4,4H60V60H4Z", "#ffffff", INK, LW)
    for x, y in ((8, 8), (40, 8), (8, 40)):
        ic.path(f"M{x},{y}h16v16h-16Z M{x + 3},{y + 3}v10h10v-10Z", INK, None, ' fill-rule="evenodd"')
        ic.path(f"M{x + 5},{y + 5}h6v6h-6Z", INK, None)
    import random
    rnd = random.Random(3)
    d = ""
    for i in range(10):
        for j in range(10):
            x, y = 8 + i * 4.8, 8 + j * 4.8
            if (x < 26 and y < 26) or (x > 36 and y < 26) or (x < 26 and y > 36):
                continue
            if rnd.random() < .45:
                d += f"M{x:.1f},{y:.1f}h4v4h-4Z"
    ic.path(d, INK, None)


def mount(ic):
    """Mount: a hard disk with a green arrow rising into it."""
    from devices import harddisk
    ic.add('<g transform="translate(0,-2) scale(.84)">')
    harddisk(ic)
    ic.add("</g>")
    _badge(ic, 47, 47, 12, "green", "M47,53.5V41M41.5,46.5L47,40.5L52.5,46.5")


def close_document(ic):
    """Close document: a page with a red cross badge."""
    page = "M8,4H34L44,14V58H8Z"
    ic.shadow(page, 2.4, 2)
    ic.path(page, ic.lg([(0, "#ffffff"), (1, "#e2e4e8")]), INK, LW)
    ic.path("M34,4V14H44", "#d9dce0", INK, 1)
    for k in range(6):
        ic.add(f'<path d="M13,{20 + k * 5}H{36 - (k % 3) * 6}" stroke="#7b818a" stroke-width="1.2"/>')
    _badge(ic, 46, 46, 13, "red", "M41,41L51,51M51,41L41,51")


def _chevrons(ic, d):
    """Double chevrons with crisp square corners, in the teal-blue of KDE Classic's arrows."""
    ic.add(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="8.6" stroke-linecap="square" stroke-linejoin="miter" stroke-miterlimit="8"/>')
    ic.add(f'<path d="{d}" fill="none" stroke="#0087ae" stroke-width="5" stroke-linecap="square" stroke-linejoin="miter" stroke-miterlimit="8"/>')   # picked from KDE Classic go-up/go-down
    ic.add(f'<path d="{d}" fill="none" stroke="#c5e4ef" stroke-opacity=".85" stroke-width="1.2" stroke-linejoin="miter" transform="translate(0,-1.2)"/>')


def collapse(ic): _chevrons(ic, "M13,28L32,12L51,28M13,54L32,38L51,54")
def expand(ic): _chevrons(ic, "M13,10L32,26L51,10M13,36L32,52L51,36")


def missed_appointment(ic):
    """Missed appointment: the calendar page with an amber warning badge."""
    from dolphin import change_date
    change_date(ic)
    _bang_badge(ic, 48, 48, 12, "amber")


def _smiley(ic, big):
    ic.shadow(circle(32, 32, 27), 2.6, 2.2)
    ic.path(circle(32, 32, 27), ic.rg([(0, "#fffbe0"), (.6, "#ffd21a"), (1, "#c87a04")], .4, .35, .8), INK, LW)
    if big:
        for x in (22, 42):
            ic.add(f'<path d="M{x - 5},28Q{x},22 {x + 5},28" fill="none" stroke="{INK}" stroke-width="2.6" stroke-linecap="round"/>')
        ic.path("M16,36H48Q48,52 32,52Q16,52 16,36Z", "#6a1a0a", INK, 1.6)
        ic.path("M20,36H44V40H20Z", "#ffffff", None)
        ic.path("M24,48Q32,44 40,48Q36,51 32,51Q28,51 24,48Z", "#e0503a", None)
    else:
        for x in (22, 42):
            ic.path(f"M{x - 3},24A3,4 0 1 0 {x + 3},24A3,4 0 1 0 {x - 3},24Z", INK, None)
        ic.add(f'<path d="M16,36Q32,54 48,36" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>')


def laughing(ic): _smiley(ic, True)
def smile_big(ic): _smiley(ic, False)


def task_icons(ic):
    """Icons-only task manager: a panel strip of square app buttons."""
    ic.shadow("M2,20H62V44H2Z", 2.4, 2)
    ic.path("M2,20H62V44H2Z", ic.lg([(0, "#e4e6e9"), (1, "#8a9098")]), INK, LW)
    for k, c in enumerate(("#3d9ad8", "#e8c43a", "#4fae5a", "#d8573d")):
        ic.path(rrect(6 + k * 14.5, 24, 12, 16, 2), ic.lg([(0, "#ffffff"), (.5, c), (1, c)]), INK, .9)
    ic.add('<path d="M7,41.5H17" stroke="#2a6ac8" stroke-width="2"/>')


def task_manager(ic):
    """Task manager: a panel strip with labelled window buttons."""
    ic.shadow("M2,20H62V44H2Z", 2.4, 2)
    ic.path("M2,20H62V44H2Z", ic.lg([(0, "#e4e6e9"), (1, "#8a9098")]), INK, LW)
    for k in range(2):
        x = 5 + k * 29
        ic.path(rrect(x, 24, 26, 16, 2), ic.lg([(0, "#ffffff"), (1, "#c9ccd1")] if k else [(0, "#bcd4ff"), (1, "#3a6ac8")]), INK, .9)
        ic.path(rrect(x + 2.5, 28, 8, 8, 1), ("#e8c43a", "#4fae5a")[k], INK, .6)
        ic.add(f'<path d="M{x + 13},32H{x + 23}" stroke="{"#fff" if not k else "#3c4148"}" stroke-width="1.6"/>')


def kicker(ic):
    """Application menu: the K gear above a menu list."""
    from discover import k_gear
    ic.shadow("M14,22H60V60H14Z", 2.4, 2)
    ic.path("M14,22H60V60H14Z", ic.lg([(0, "#ffffff"), (1, "#e4e6e9")]), INK, LW)
    for k in range(4):
        y = 30 + k * 7.5
        ic.path(rrect(30, y - 2.5, 5, 5, 1), ("#3d9ad8", "#e8c43a", "#4fae5a", "#d8573d")[k], INK, .5)
        ic.add(f'<path d="M38,{y}H{55 - (k % 2) * 6}" stroke="#5c6168" stroke-width="1.4"/>')
    ic.add('<g transform="translate(2,2) scale(.48)">')
    k_gear(ic)
    ic.add("</g>")


def vault(ic, error=False):
    """Plasma Vault: a steel safe with a combination dial and handle."""
    ic.shadow("M6,8H58V56H6Z", 2.6, 2.2)
    ic.path(rrect(6, 8, 52, 48, 4), ic.lg([(0, "#d9dce0"), (.5, "#8a9098"), (1, "#3c4148")], 0, 0, 1, 1), INK, LW)
    ic.path(rrect(11, 13, 42, 38, 2), ic.lg([(0, "#c3c7cd"), (1, "#5c6168")], 0, 0, 1, 1), INK, 1.2)
    ic.path(circle(30, 32, 11), ic.rg([(0, "#ffffff"), (.6, "#b4b9c0"), (1, "#4c5158")], .4, .35, .8), INK, 1.3)
    for k in range(12):
        a = 2 * math.pi * k / 12
        ic.add(f'<path d="M{30 + 8 * math.sin(a):.2f},{32 - 8 * math.cos(a):.2f}L{30 + 10 * math.sin(a):.2f},{32 - 10 * math.cos(a):.2f}" stroke="{INK}" stroke-width=".8"/>')
    ic.path(circle(30, 32, 3.4), "#3c4148", INK, .8)
    ic.path(rrect(46, 24, 4, 16, 1.6), ic.lg([(0, "#ffffff"), (1, "#6c727a")], 0, 0, 1, 0), INK, 1)
    for y in (8, 52):
        ic.path(rrect(10, y, 8, 4, 1), "#2c3036", INK, .6)
    if error:
        _bang_badge(ic, 48, 48, 12, "red")


def vault_error(ic): vault(ic, True)


def unread_mail(ic):
    """Unread mail: a closed envelope with a blue 'new' dot."""
    ic.shadow("M4,16H56V52H4Z", 2.4, 2)
    ic.path("M4,16H56V52H4Z", ic.lg([(0, "#ffffff"), (1, "#d9dce0")]), INK, LW)
    ic.add(f'<path d="M4,16L30,36L56,16M4,52L22,32M56,52L38,32" fill="none" stroke="{INK}" stroke-width="1.2" stroke-linejoin="round"/>')
    ic.path(circle(52, 16, 8), ic.rg([(0, "#bfe0ff"), (.55, "#2a6ac8"), (1, "#0c2a6a")], .4, .32, .8), INK, 1.2)


def _handset(ic, colour, down):
    t = "rotate(135 32 32)" if down else ""
    d = "M14,10Q8,12 8,20Q10,38 26,50Q40,58 46,56Q52,54 54,48L46,40Q42,38 38,42L34,44Q24,38 20,28L22,24Q26,20 24,16Z"
    ic.add(f'<g transform="{t}">')
    ic.shadow(d, 2.4, 2)
    c = {"green": ("#c8f8a8", "#3fae2a", "#145a0c"), "red": ("#ffb0a0", "#e0281a", "#6a0804")}[colour]
    ic.path(d, ic.lg([(0, c[0]), (.5, c[1]), (1, c[2])], 0, 0, 1, 1), INK, LW)
    ic.add("</g>")


def call_start(ic): _handset(ic, "green", False)
def call_stop(ic): _handset(ic, "red", True)


def printer_warning(ic):
    """Printer problem: the printer with an amber warning badge."""
    from devices import printer
    ic.add('<g transform="translate(-2,-2) scale(.86)">')
    printer(ic)
    ic.add("</g>")
    _bang_badge(ic, 48, 48, 12, "amber")


def computer_fail(ic):
    """Computer error: the beige computer with a red cross badge."""
    from gen import computer
    c = computer()
    ic.defs += c.defs
    ic.add('<g transform="translate(-2,-2) scale(.86)">' + "".join(c.body) + "</g>")
    _badge(ic, 48, 48, 12, "red", "M43,43L53,53M53,43L43,53")


def burn(ic, dvd=False):
    """Write CD / DVD / Blu-ray: the disc with a red burning flame."""
    from devices import cd, dvd as dvdf, hd_disc
    c = {False: cd, True: dvdf, "bd": hd_disc}[dvd]()
    ic.defs += c.defs
    ic.add('<g transform="translate(-2,-2) scale(.86)">' + "".join(c.body) + "</g>")
    flame = "M48,62C38,62 36,52 40,46C42,50 44,50 44,48C44,42 48,38 52,34C52,40 58,44 58,52C58,58 54,62 48,62Z"
    ic.shadow(flame, 1.8, 1.6)
    ic.path(flame, ic.lg([(0, "#fff36a"), (.5, "#ff8a1a"), (1, "#c8180c")]), INK, 1.2)


def burn_cd(ic): burn(ic, False)
def burn_dvd(ic): burn(ic, True)
def burn_bd(ic): burn(ic, "bd")


def album_cover(ic):
    """Album art placeholder: a record sleeve with the disc sliding out."""
    ic.path(circle(42, 32, 20), ic.rg([(0, "#5c6168"), (.3, "#14171c"), (.32, "#e8c43a"), (.4, "#e8c43a"), (.42, "#14171c"), (1, "#2c3036")], .5, .5, .5), INK, LW)
    ic.shadow("M4,10H44V54H4Z", 2.4, 2)
    ic.path("M4,10H44V54H4Z", ic.lg([(0, "#9fd4ff"), (1, "#1a4a8a")], 0, 0, 1, 1), INK, LW)
    ic.path(circle(24, 30, 9), "#ffffff", INK, 1, ' fill-opacity=".85"')
    ic.add('<path d="M22,26L28,30L22,34Z" fill="#1a4a8a"/>')


TRAY = {
    "battery-profile-performance": perf_profile, "battery-profile-powersave": powersave_profile,
    "disk-quota": quota, "disk-quota-low": quota_low, "disk-quota-high": quota_high, "disk-quota-critical": quota_critical,
    "camera-on": cam_on, "camera-ready": cam_ready, "camera-off": cam_off, "mic-on": mic_on, "mic-ready": mic_ready,
    "audio-headset": headset, "hands-free": hands_free, "hifi": hifi, "input-combo-on": caps_lock, "input-num-on": num_lock,
    "chronometer-start": timer_start, "chronometer-pause": timer_pause, "compass": compass, "flag-black": black_flag,
    "office-chart-pie": pie_chart, "widget-alternatives": alternatives, "show-menu": global_menu,
    "application-x-plasma": plasmoid, "media-record": record, "view-barcode-qr": qr_code, "media-mount": mount,
    "document-close": close_document, "collapse": collapse, "expand": expand, "appointment-missed": missed_appointment,
    "face-laughing": laughing, "face-smile-big": smile_big, "org.kde.plasma.icontasks": task_icons,
    "org.kde.plasma.taskmanager": task_manager, "org.kde.plasma.kicker": kicker, "plasmavault": vault,
    "plasmavault_error": vault_error, "mail-unread": unread_mail, "call-start": call_start, "call-stop": call_stop,
    "printer-warning": printer_warning, "computer-fail": computer_fail, "media-write-cd": burn_cd,
    "media-write-dvd": burn_dvd, "media-write-bd": burn_bd, "media-album-cover": album_cover,
}
TRAY_ALIASES = {
    "battery-profile-performance-symbolic": "battery-profile-performance", "battery-profile-powersave-symbolic": "battery-profile-powersave",
    "camera-on-symbolic": "camera-on", "camera-ready-symbolic": "camera-ready", "camera-off-symbolic": "camera-off",
    "audio-headset-symbolic": "audio-headset", "headset": "audio-headset", "media-record-symbolic": "media-record",
    "media-mount-symbolic": "media-mount", "document-close-symbolic": "document-close", "collapse-symbolic": "collapse",
    "expand-symbolic": "expand", "appointment-missed-symbolic": "appointment-missed", "plasmavault-symbolic": "plasmavault",
    "mail-unread-symbolic": "mail-unread", "printer-warning-symbolic": "printer-warning", "computer-fail-symbolic": "computer-fail",
    "media-write-cd-symbolic": "media-write-cd", "media-write-dvd-symbolic": "media-write-dvd",
    "media-write-bd-symbolic": "media-write-bd", "media-write-blu-ray": "media-write-bd", "media-write-bluray": "media-write-bd",
    "media-album-cover-symbolic": "media-album-cover", "media-default-album": "media-album-cover", "media-album-track": "media-album-cover",
    "media-album-track-symbolic": "media-album-cover", "org.kde.plasma.appmenu": "show-menu", "plasma": None,
}
TRAY_CROSS = {
    "application-menu-symbolic": "../actions/open-menu.svg", "network-unavailable": "../actions/offline.svg",
    "audio-on": "../apps/preferences-desktop-sound.svg", "audio-ready": "../apps/preferences-desktop-sound.svg",
    "org.kde.plasma.networkmanagement": "../apps/preferences-system-network.svg", "window-minimize-symbolic": None,
    "drive-harddisk-encrypted-symbolic": "../devices/drive-harddisk.svg", "drive-harddisk-usb-symbolic": "../devices/drive-removable-media-usb.svg",
    "drive-harddisk-system-symbolic": "../devices/drive-harddisk.svg", "drive-harddisk-ieee1394-symbolic": "../devices/drive-harddisk.svg",
    "drive-multidisk-symbolic": "../apps/drive-multidisk.svg", "drive-optical-symbolic": "../devices/drive-optical.svg",
    "media-optical-bd-symbolic": "../devices/media-optical-bd.svg", "media-optical-data-symbolic": "../devices/media-optical-cd.svg",
    "media-optical-mixed-cd-symbolic": "../devices/media-optical-audio.svg", "media-optical-video-symbolic": "../devices/media-optical-dvd-video.svg",
    "media-flash-sd-mmc-symbolic": "../devices/media-flash.svg", "media-flash-memory-stick-symbolic": "../devices/media-flash.svg",
    "media-import-audio-cd-symbolic": "../devices/media-optical-audio.svg", "media-default-track": "../mimetypes/audio-x-generic.svg",
    "media-view-subtitles-symbolic": "../mimetypes/text-x-subviewer.svg", "drive-partition": "../devices/drive-harddisk.svg",
}


def write(out):
    d = f"{out}/scalable/status"
    os.makedirs(d, exist_ok=True)
    for name, fn in TRAY.items():
        open(f"{d}/{name}.svg", "w").write(_ic(fn)().svg(64))
    for a, t in TRAY_ALIASES.items():
        if t and not os.path.exists(f"{d}/{a}.svg"):
            os.symlink(f"{t}.svg", f"{d}/{a}.svg")
    for a, t in TRAY_CROSS.items():
        if t and os.path.exists(os.path.join(d, t)) and not os.path.exists(f"{d}/{a}.svg"):
            os.symlink(t, f"{d}/{a}.svg")
    return len(TRAY)
