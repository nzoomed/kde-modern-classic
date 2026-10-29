"""KDE Classic Vector: the panel and system tray icons that still came from KDE Classic bitmaps - battery
levels, volume and microphone levels, wireless and wired network states, notifications, playback states and
controls, text formatting, brightness and night colour - redrawn as vectors in parametric families, plus
aliases where the meaning matches an icon already drawn.

State badges are the shell's round badges; arrows follow STYLE.md (teal); signal strength uses the
glossy blue of the Bluetooth icon for lit bars and grey for unlit ones.
"""
import math, os
from gen import Icon, INK, LW, circle, rrect
from actions import _mpath
from settingstrace import _battery, _teal, _arrow_pts, _double_arrow, _badge, _ok, _no, _poly, _page, _speaker

def _ic(fn, *a, **kw):
    def f():
        ic = Icon()
        fn(ic, *a, **kw)
        return ic
    return f


def _dots(ic, x=48, y=48, r=11, colour="blue"):
    _badge(ic, x, y, r, colour, "")
    for dx in (-r * .42, 0, r * .42):
        ic.path(circle(x + dx, y, r * .14), "#ffffff", None)


def _bang(ic, x=48, y=48, r=11, colour="amber"):
    from shell import _bang_badge
    _bang_badge(ic, x, y, r, colour)


def _lock(ic, x=47, y=46, k=.42):
    from dolphin import _padlock
    ic.add(f'<g transform="translate({x - 32 * k:.2f},{y - 32 * k:.2f}) scale({k})">')
    _padlock(ic, False)
    ic.add("</g>")


# ------------------------------------------------------------------ battery
LEVELS = list(range(0, 101, 10))


def _battery_level(ic, pct, charging=False):
    lvl = pct / 100
    colour = "red" if pct <= 10 else ("yellow" if pct <= 30 else "green")
    _battery(ic, lvl if pct else 0, colour, bolt=charging)


def battery_missing(ic):
    _battery(ic, 0, "green")
    _no(ic, 47, 48, 12)


def battery_full_charged(ic):
    _battery(ic, 1, "green")
    _ok(ic, 47, 48, 12)


# ------------------------------------------------------------------ sound and microphone
def _waves(ic, n, colour, x0=30, cy=32, radii=(14.5, 24.5, 34.5)):
    """Sound waves: slices of circles centred just right of the speaker, 45 degrees either side of its axis, as
    in most icon themes (2026-10-27: were half circles). The first `n` are lit, the rest grey. x0 is the old
    anchor; the arcs' centre sits at x0 - 5, which leaves a gap after the default speaker's rim. The outer arc
    reaches x ~62 so the volume icons fill the canvas as the old half circles did (they looked small in the tray)."""
    import math
    cols = {"teal": "#0aa0b8", "amber": "#ec9a1a", "red": "#e0281a", "grey": "#b4b9c0"}
    ccx, a = x0 - 5, math.radians(45)
    for k, r in enumerate(radii):
        lit = k < n
        x, dy = ccx + r * math.cos(a), r * math.sin(a)
        d = f"M{x:.2f},{cy - dy:.2f}A{r},{r} 0 0 1 {x:.2f},{cy + dy:.2f}"
        ic.add(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="4.4" stroke-linecap="round"/>'
               f'<path d="{d}" fill="none" stroke="{cols[colour] if lit else cols["grey"]}" stroke-width="2.4" stroke-linecap="round"/>')


# Panel volume icons (and Speakers, Muted): the speaker 25% larger than the shared emblem so it reads at 22 px
# beside its waves, the waves fitted to the space left (2026-10-27).
VOL_SPEAKER = (1.0, -23.0, 1.25)          # _speaker(dx, dy, k): box left ~1.5, axis at y=32
VOL_WAVES = dict(x0=36, radii=(13, 21, 28.8))


def volume(ic, n, colour="teal"):
    _speaker(ic, *VOL_SPEAKER)
    _waves(ic, n, colour, **VOL_WAVES)


def mic_level(ic, level, muted=False):
    """Microphone sensitivity: the silver stage mic, filled green up to the level."""
    from systray import _mic
    _mic(ic, False)
    if level:
        top = 6 + 30 * (1 - level)
        ic.path(rrect(24.6, top, 14.8, 36 - top, min(7.4, (36 - top) / 2)), ic.lg([(0, "#0e6a08"), (.4, "#7ae060"), (1, "#0a4a06")], 0, 0, 1, 0), None, ' fill-opacity=".9"')
    if muted:
        _no(ic, 48, 48, 12)


# ------------------------------------------------------------------ wireless and wired network
BLUE = [(0, "#b8dcff"), (.45, "#2a6ac8"), (1, "#0c2a6a")]
GREEN = [(0, "#c8f8a8"), (.45, "#3fae2a"), (1, "#145a0c")]
GREYS = [(0, "#ffffff"), (.5, "#c3c7cd"), (1, "#7b818a")]


def wifi(ic, lit, colour=BLUE, badge=None, off=False):
    """Wireless: KDE's fan of signal arcs over a dot, `lit` of the five parts (dot + four arcs) coloured."""
    cx, cy = 30, 50
    for k in range(4, 0, -1):
        r = 9 + k * 9
        a0, a1 = math.radians(-135), math.radians(-45)
        ro, ri = r, r - 5.4
        d = (f"M{cx + ro * math.cos(a0):.2f},{cy + ro * math.sin(a0):.2f}A{ro},{ro} 0 0 1 {cx + ro * math.cos(a1):.2f},{cy + ro * math.sin(a1):.2f}"
             f"L{cx + ri * math.cos(a1):.2f},{cy + ri * math.sin(a1):.2f}A{ri},{ri} 0 0 0 {cx + ri * math.cos(a0):.2f},{cy + ri * math.sin(a0):.2f}Z")
        ic.shadow(d, 1.8, 1.5)
        ic.path(d, ic.lg(colour if k < lit else GREYS, 0, 0, 0, 1), INK, 1.2)
    ic.shadow(circle(cx, cy, 5), 1.6, 1.4)
    ic.path(circle(cx, cy, 5), ic.rg(colour if lit else GREYS, .4, .35, .8), INK, 1.2)
    if off:
        ic.add('<path d="M8,10L52,56" stroke="#5a0402" stroke-width="6" stroke-linecap="round"/><path d="M8,10L52,56" stroke="#f02a1a" stroke-width="3.6" stroke-linecap="round"/>')
    if badge:
        badge(ic)


WIFI_LEVELS = {0: 0, 20: 1, 40: 2, 60: 3, 80: 4, 100: 5}


def _plug(ic):
    """Wired network: an RJ45 plug on its grey cable."""
    ic.add(f'<path d="M26,44V62M34,44V62" stroke="{INK}" stroke-width="1.2"/>')
    ic.path("M24,44H36V62H24Z", ic.lg([(0, "#5c6168"), (.4, "#c3c7cd"), (1, "#4c5158")], 0, 0, 1, 0), INK, LW)
    ic.path("M20,38H40V46H20Z", ic.lg([(0, "#8a9098"), (.4, "#e4e6e9"), (1, "#5c6168")], 0, 0, 1, 0), INK, LW)
    body = "M12,6H48V40H12Z"
    ic.shadow(body, 2.4, 2)
    ic.path(body, ic.lg([(0, "#ffffff"), (.5, "#d9dce0"), (1, "#8a9098")], 0, 0, 1, 1), INK, LW * 1.2)
    ic.path("M17,10H43V20H17Z", "#3c4148", INK, 1)
    for k in range(6):
        ic.path(f"M{19.4 + k * 4},11.5H{21.4 + k * 4}V18H{19.4 + k * 4}Z", ic.lg([(0, "#fff8b0"), (1, "#c8940a")], 0, 0, 1, 0), None)
    ic.path("M24,40V46H36V40", "none", INK, 1)


def wired(ic, badge=None, dim=False):
    _plug(ic)
    if dim:
        ic.add('<path d="M12,6H48V40H12ZM20,38H40V62H20Z" fill="#ffffff" fill-opacity=".5"/>')
    if badge:
        badge(ic)


def _bt(ic, grey=False):
    oval = "M32,6C44,6 49,14 49,32C49,50 44,58 32,58C20,58 15,50 15,32C15,14 20,6 32,6Z"
    ic.shadow(oval, 2.6, 2.2)
    cols = [(0, "#ffffff"), (.45, "#9aa0a8"), (1, "#3c4148")] if grey else [(0, "#9fd0ff"), (.45, "#2a6ac8"), (1, "#0e2e6a")]
    ic.path(oval, ic.lg(cols, 0, 0, .3, 1), INK, LW)
    ic.add('<path d="M20,18Q22,10 32,9.5Q42,10 44,18Q32,24 20,18Z" fill="#fff" fill-opacity=".3"/>')
    rune = "M24,23L40,39L32,47V17L40,25L24,41"
    ic.add(f'<path d="{rune}" fill="none" stroke="#000" stroke-opacity=".3" stroke-width="5.4" stroke-linecap="round" stroke-linejoin="round"/>')
    ic.add(f'<path d="{rune}" fill="none" stroke="#fff" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/>')


def bluetooth_inactive(ic):
    _bt(ic, grey=True)


def vpn(ic):
    """VPN: a blue shield with a white padlock."""
    s = "M32,4Q44,10 56,10Q56,40 32,60Q8,40 8,10Q20,10 32,4Z"
    ic.shadow(s, 2.6, 2.2)
    ic.path(s, ic.lg([(0, "#b8dcff"), (.45, "#2a6ac8"), (1, "#0c2a6a")], 0, 0, 1, 1), INK, LW * 1.2)
    ic.add('<path d="M12,13Q22,12.6 32,8V30Q14,30 12,13Z" fill="#fff" fill-opacity=".25"/>')
    ic.add('<path d="M25,30V25A7,7 0 0 1 39,25V30" fill="none" stroke="#fff" stroke-width="3.4"/>')
    ic.path(rrect(22, 29, 20, 16, 2), "#ffffff", None)
    ic.path("M32,34A2,2 0 0 1 33.2,37.4V40.4H30.8V37.4A2,2 0 0 1 32,34Z", "#2a6ac8", None)


def plane(ic, on=True):
    """Flight mode: an aeroplane seen from above - orange when on, grey with a red slash when off."""
    d = ("M32,3Q35,3 35,10V25L58,38V44L35,37V50L42,55V59L32,56L22,59V55L29,50V37L6,44V38L29,25V10Q29,3 32,3Z")
    ic.shadow(d, 2.4, 2)
    ic.path(d, ic.lg([(0, "#ffd8a0"), (.45, "#f88a14"), (1, "#a84a04")] if on else GREYS, 0, 0, 1, 1), INK, LW)
    ic.add('<path d="M31,8V24" stroke="#fff" stroke-opacity=".6" stroke-width="1.4" stroke-linecap="round"/>')
    if not on:
        ic.add('<path d="M8,8L56,56" stroke="#5a0402" stroke-width="6" stroke-linecap="round"/><path d="M8,8L56,56" stroke="#f02a1a" stroke-width="3.6" stroke-linecap="round"/>')


def modem(ic):
    """Modem (KDE 3's KPPP): a grey modem box with its lights, and the globe behind."""
    from gen import e_globe
    e_globe(ic, 18, 4, 16)
    box = "M4,40L18,30H60L46,40Z"
    ic.shadow(box + "M4,40H46V54H4Z", 2.4, 2)
    ic.path("M46,40L60,30V44L46,54Z", ic.lg([(0, "#8a9098"), (1, "#3c4148")]), INK, LW)
    ic.path("M4,40H46V54H4Z", ic.lg([(0, "#e4e6e9"), (1, "#7b818a")]), INK, LW)
    ic.path(box, ic.lg([(0, "#ffffff"), (1, "#c3c7cd")]), INK, LW)
    for k, col in enumerate(("#e0281a", "#e0281a", "#3fd02a", "#e8c43a")):
        ic.path(circle(10 + k * 6, 47, 1.8), col, INK, .6)


# ------------------------------------------------------------------ notifications
def bell(ic, badge=None, grey=False):
    """The KDE 3 hand bell drawn for Notifications, brass when active, grey when quiet, empty or off."""
    from settings import notifications, BELL_BRASS, BELL_GREY
    ic.add('<g transform="translate(-2,0)">')
    notifications(ic, BELL_GREY if grey else BELL_BRASS)
    ic.add("</g>")
    if badge:
        badge(ic)


def _red_dot(ic):
    ic.shadow(circle(48, 46, 9), 1.6, 1.4)
    ic.path(circle(48, 46, 9), ic.rg([(0, "#ffb0a0"), (.55, "#f02a1a"), (1, "#6a0804")], .4, .32, .8), INK, 1.4)


def _empty_ring(ic):
    ic.path(circle(48, 46, 9), "#ffffff", INK, 1.4)
    ic.path(circle(48, 46, 5.4), "none", "#9aa0a8", 2)


# ------------------------------------------------------------------ playback
def _disc_badge(ic, colour, shape):
    _badge(ic, 32, 32, 27, colour, "")
    ic.add('<path d="M12,26Q14,9 32,8Q50,9 52,26Q32,33 12,26Z" fill="#fff" fill-opacity=".3"/>')
    ic.path(shape, "#000000", None, ' fill-opacity=".3" transform="translate(1.2,1.2)"')
    ic.path(shape, "#ffffff", None)


def playing(ic): _disc_badge(ic, "green", "M25,18L46,32L25,46Z")
def paused(ic): _disc_badge(ic, "amber", "M21,19H29V45H21ZM35,19H43V45H35Z")
def stopped(ic): _disc_badge(ic, "red", "M20,20H44V44H20Z")


def _bevel(ic, d, inner):
    """A media control shape in the theme's bevelled grey: dark outer body, light glossy inner face."""
    ic.shadow(d, 2.4, 2)
    _mpath(ic, d, ic.lg([(0, "#8a9098"), (.5, "#4c5158"), (1, "#141414")], 0, 0, 1, 1), LW * 1.2)
    ic.path(inner, ic.lg([(0, "#ffffff"), (.45, "#c3c7cd"), (1, "#6c727a")], 0, 0, .6, 1), "#2c3036", .8)


def _tri(x, y0, y1, tip, inset=0):
    my = (y0 + y1) / 2
    if inset:
        k = inset
        sgn = 1 if tip > x else -1
        return f"M{x + sgn * k * 1.4},{y0 + k * 2}L{tip - sgn * k * 2},{my}L{x + sgn * k * 1.4},{y1 - k * 2}Z"
    return f"M{x},{y0}L{tip},{my}L{x},{y1}Z"


def _mirror(fn):
    def f(ic):
        ic.add('<g transform="translate(64,0) scale(-1,1)">')
        fn(ic)
        ic.add("</g>")
    return f


def seek_forward(ic):
    for x in (4, 31):
        _bevel(ic, _tri(x, 12, 52, x + 29), _tri(x, 12, 52, x + 29, 3))


def skip_forward(ic):
    _bevel(ic, _tri(6, 10, 54, 42), _tri(6, 10, 54, 42, 3.4))
    _bevel(ic, "M44,10H56V54H44Z", "M47.4,14H52.6V50H47.4Z")


seek_backward = _mirror(seek_forward)
skip_backward = _mirror(skip_forward)


def eject(ic):
    _bevel(ic, "M32,6L60,36H4Z", "M32,12.4L51.6,32.6H12.4Z")
    _bevel(ic, rrect(6, 42, 52, 12, 2), rrect(10, 45.4, 44, 5.2, 1.4))


def _loop(ic, k=0):
    """A teal arrow looping round once (repeat)."""
    from actions import _curl_points
    pts = _curl_points(32, 32, 19, 4.4, 300, 300, 13, 10, taper=40, N=60)
    _teal(ic, _poly(pts))


def repeat(ic):
    _loop(ic)


def repeat_one(ic):
    _loop(ic)
    ic.add(f'<path d="M28,28L33,24V42M28,42H38" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="square" stroke-linejoin="miter"/>')


def shuffle(ic):
    """Shuffle: two teal arrows crossing over each other."""
    _teal(ic, _poly([(4, 16), (22, 16), (40, 42), (46, 42), (46, 34), (60, 46), (46, 58), (46, 50), (36, 50), (18, 24), (4, 24)]))
    # the second arrow is one unbroken band, crossing over the first
    _teal(ic, _poly([(4, 42), (18, 42), (36, 18), (46, 18), (46, 10), (60, 22), (46, 34), (46, 26), (40, 26), (22, 50), (4, 50)]))


# ------------------------------------------------------------------ text formatting
def _textlines(ic, rows):
    for y, x0, x1 in rows:
        ic.path(f"M{x0},{y}H{x1}V{y + 4.6}H{x0}Z", ic.lg([(0, "#4c5158"), (1, "#000000")]), None)


def justify(ic, mode):
    rows = []
    widths = (52, 40, 48, 34, 52, 30)
    for k, w in enumerate(widths):
        y = 7 + k * 8.8
        if mode == "left":
            rows.append((y, 6, 6 + w))
        elif mode == "right":
            rows.append((y, 58 - w, 58))
        elif mode == "center":
            rows.append((y, 32 - w / 2, 32 + w / 2))
        else:
            rows.append((y, 6, 58 if k < 5 else 36))
    _textlines(ic, rows)


def indent(ic, more):
    rows = [(6, 6, 58), (54, 6, 58)] + [(15 + k * 9.6, 30, 58) for k in range(4)]
    _textlines(ic, rows)
    if more:
        _teal(ic, _poly(_arrow_pts(4, 32, 26, 32, 4, 11, 11)))
    else:
        _teal(ic, _poly(_arrow_pts(26, 32, 4, 32, 4, 11, 11)))


def italic(ic):
    d = "M24,6H48V10H42L30,54H36V58H12V54H18L30,10H24Z"
    ic.shadow(d, 2.2, 1.8)
    ic.path(d, ic.lg([(0, "#4c5158"), (1, "#000000")]), INK, .8)


def underline(ic):
    d = ("M8,4H26V8H22V34Q22,44 32,44Q42,44 42,34V8H38V4H56V8H50V34Q50,51 32,51Q14,51 14,34V8H8Z")
    ic.shadow(d, 2.2, 1.8)
    ic.path(d, ic.lg([(0, "#4c5158"), (1, "#000000")]), INK, .8)
    ic.path("M6,55H58V60H6Z", "#000000", None)


def strikethrough(ic):
    s = "M46,14Q42,8 32,8Q20,8 20,18Q20,26 32,29Q44,32 44,42Q44,54 30,54Q20,54 16,46"
    ic.add(f'<path d="{s}" fill="none" stroke="{INK}" stroke-width="7.4" stroke-linecap="square"/>')
    ic.add(f'<path d="{s}" fill="none" stroke="#2c3036" stroke-width="5"/>')
    ic.path("M4,30H60V35H4Z", ic.lg([(0, "#ff8a7a"), (1, "#a8180a")]), INK, 1)


# ------------------------------------------------------------------ go to end arrows
def go_bottom(ic):
    _teal(ic, _poly(_arrow_pts(32, 4, 32, 48, 8, 20, 20)))
    _teal(ic, "M8,52H56V59H8Z")


def go_first(ic):
    _teal(ic, _poly(_arrow_pts(60, 32, 16, 32, 8, 20, 20)))
    _teal(ic, "M5,8H12V56H5Z")


def go_last(ic):
    _teal(ic, _poly(_arrow_pts(4, 32, 48, 32, 8, 20, 20)))
    _teal(ic, "M52,8H59V56H52Z")


# ------------------------------------------------------------------ light, sun and moon
def sun_icon(ic, r, rays=True, warm=False):
    from weather import sun
    if warm:
        from weather import SUN
    sun(ic, 32, 32, r, rays)


def brightness(ic, high):
    from weather import sun
    sun(ic, 32, 32, 15 if high else 10)


def display_brightness(ic):
    from shell import _monitor
    _monitor(ic, 4, 8, 56, 42)
    from weather import sun
    sun(ic, 32, 28, 8)


def redshift_day(ic):
    from weather import sun, moon
    sun(ic, 28, 28, 13)
    moon(ic, 48, 48, 10)


def redshift_off(ic):
    d = "M38,6A26,26 0 1 0 58,44A21,21 0 1 1 38,6Z"
    ic.shadow(d, 2.4, 2)
    ic.path(d, ic.lg(GREYS, 0, 0, 1, 1), INK, LW)


# ------------------------------------------------------------------ input and power
def touchpad_state(ic, on):
    from settings import touchpad
    touchpad(ic)
    (_ok if on else _no)(ic, 48, 48, 12)


def vkbd_on(ic):
    from settings import virtual_keyboard
    virtual_keyboard(ic)
    _ok(ic, 48, 48, 12)


def coffee(ic, steam=True):
    """Suspend inhibited: KDE's coffee cup keeping the machine awake - steaming hot; cold and grey when not."""
    cup = "M10,26H46V40Q46,56 28,56Q10,56 10,40Z"
    if steam:
        for x in (22, 32):
            d = f"M{x},20Q{x - 4},15 {x},10Q{x + 4},5 {x},2"
            ic.add(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="3.4" stroke-linecap="round"/><path d="{d}" fill="none" stroke="#e4e6e9" stroke-width="1.8" stroke-linecap="round"/>')
    ic.add(f'<path d="M45,32Q56,30 56,39Q56,48 44,47" fill="none" stroke="{INK}" stroke-width="6"/>')
    ic.add(f'<path d="M45,32Q56,30 56,39Q56,48 44,47" fill="none" stroke="{"#c86a20" if steam else "#9aa0a8"}" stroke-width="3.4"/>')
    ic.shadow(cup, 2.4, 2)
    ic.path(cup, ic.lg([(0, "#ffb070"), (.4, "#c85a10"), (1, "#5a2404")] if steam else GREYS, 0, 0, 1, 0), INK, LW)
    ic.path("M10,26A18,4 0 0 0 46,26A18,4 0 0 0 10,26Z", "#5a2a08" if steam else "#e4e6e9", INK, 1)


# ------------------------------------------------------------------ apps and odds
def calculator(ic):
    """Calculator (KDE 3's KCalc): a teal calculator with a green display, in front of squared paper."""
    p = "M24,4H58V58H24Z"
    ic.path(p, "#ffffff", INK, 1)
    for k in range(1, 9):
        ic.add(f'<path d="M{24 + k * 3.8:.1f},4V58M24,{4 + k * 6:.1f}H58" stroke="#a8b8e8" stroke-width=".6"/>')
    body = rrect(4, 10, 34, 50, 4)
    ic.shadow(body, 2.6, 2.2)
    ic.path(body, ic.lg([(0, "#8ae0e0"), (.45, "#1a9098"), (1, "#0a4048")], 0, 0, 1, 1), INK, LW)
    ic.path("M9,15H33V25H9Z", ic.lg([(0, "#c8f0b0"), (1, "#5a9a40")]), INK, 1)
    ic.add('<path d="M22,18V22M26,18H29V20H26V22H29" fill="none" stroke="#14371a" stroke-width="1.4"/>')
    for r in range(4):
        for c in range(4):
            col = "#e0281a" if (r == 3 and c == 3) else ("#2c3036" if c < 3 else "#e4e6e9")
            ic.path(rrect(9 + c * 6.2, 29 + r * 7.2, 4.8, 5.2, 1), col, INK, .6)


def charselect(ic):
    """Character map (KDE 3's KCharSelect): a white keycap tilted on its corner, with a glyph on it."""
    d = "M32,3L61,32L32,61L3,32Z"
    ic.shadow(d, 2.6, 2.2)
    ic.path(d, ic.lg([(0, "#ffffff"), (.5, "#d9dce0"), (1, "#8a9098")], 0, 0, 1, 1), INK, LW * 1.2)
    ic.path("M32,10L54,32L32,54L10,32Z", ic.lg([(0, "#c3c7cd"), (1, "#ffffff")], 0, 0, 1, 1), "#7b818a", .9)
    ic.add(f'<path d="M24,40V26Q24,20 30,20H38M30,32H36M30,26V44" fill="none" stroke="{INK}" stroke-width="2.6" stroke-linecap="round"/>')


def planner(ic):
    """Calendar (KDE 3's KOrganizer): a green ring-bound planner with the orange pencil across it."""
    from uitrace import _pencil
    b = "M8,4H56V60H8Z"
    ic.shadow(b, 2.6, 2.2)
    ic.path(b, ic.lg([(0, "#8ae08a"), (.5, "#1a8a2a"), (1, "#0a4012")], 0, 0, 1, 1), INK, LW)
    ic.path("M12,7H31V57H12Z", ic.lg([(0, "#ffffff"), (1, "#e4e6e9")]), INK, .9)
    ic.path("M33,7H53V57H33Z", ic.lg([(0, "#ffffff"), (1, "#e4e6e9")]), INK, .9)
    for k in range(7):
        y = 12 + k * 6.6
        ic.add(f'<path d="M15,{y}H28M36,{y}H50" stroke="#a8b8e8" stroke-width="1"/>')
    for y in (12, 22, 32, 42, 52):
        ic.path(rrect(29.5, y - 2, 5, 4, 2), ic.lg([(0, "#ffffff"), (1, "#7b818a")]), INK, .7)
    _pencil(ic, "translate(52,6) rotate(36) translate(-6,0) scale(.9)")


def colour_management(ic):
    """Colour management: a window showing red, green and blue bands."""
    w = "M6,6H58V58H6Z"
    ic.shadow(w, 2.4, 2)
    ic.path(w, ic.lg([(0, "#ffffff"), (1, "#e4e6e9")], 0, 0, 1, 1), INK, LW)
    ic.path("M6,6H58V15H6Z", ic.lg([(0, "#8ab0ff"), (.5, "#1a3ae0"), (1, "#0a1a80")]), INK, LW)
    for k, cols in enumerate(((("#ffb0a0"), "#e0200a"), ("#c8f8a8", "#1e9a14"), ("#b8dcff", "#1a4ae0"))):
        ic.path(f"M11,{20 + k * 12}H53V{29 + k * 12}H11Z", ic.lg([(0, "#ffffff"), (.3, cols[0]), (1, cols[1])], 0, 0, 1, 0), INK, .9)


def dice(ic):
    """Roll: two ivory dice tumbling."""
    def die(x, y, a, pips):
        ic.add(f'<g transform="translate({x},{y}) rotate({a})">')
        b = rrect(-12, -12, 24, 24, 5)
        ic.shadow(b, 2.2, 1.8)
        ic.path(b, ic.lg([(0, "#ffffff"), (.6, "#e4e6e9"), (1, "#9aa0a8")], 0, 0, 1, 1), INK, LW)
        for px, py in pips:
            ic.path(circle(px, py, 2.4), "#14171c", None)
        ic.add("</g>")
    die(21, 21, -12, ((-6, -6), (6, -6), (0, 0), (-6, 6), (6, 6)))
    die(43, 43, 14, ((-6, -6), (0, 0), (6, 6)))


def group(ic):
    """Group: a square and a circle overlapping, sharing one set of selection handles."""
    sq = "M8,22H34V48H8Z"
    ic.shadow(sq, 2, 1.7)
    ic.path(sq, ic.lg([(0, "#ffffff"), (1, "#c3c7cd")], 0, 0, 1, 1), INK, LW)
    ic.shadow(circle(38, 26, 13), 2, 1.7)
    ic.path(circle(38, 26, 13), ic.rg([(0, "#ffffff"), (1, "#c3c7cd")], .4, .35, .8), INK, LW)
    ic.add(f'<path d="M6,11H53V50H6Z" fill="none" stroke="{INK}" stroke-width="1" stroke-dasharray="3 2"/>')
    for x, y in ((6, 11), (53, 11), (6, 50), (53, 50)):
        ic.path(f"M{x - 2.8},{y - 2.8}H{x + 2.8}V{y + 2.8}H{x - 2.8}Z", "#2a5ae0", INK, .8)


def services(ic):
    """Services: KDE 3's gold star."""
    from discover import _star
    d = _star(32, 34, 28, 12)
    ic.shadow(d, 2.6, 2.2)
    _mpath(ic, d, ic.rg([(0, "#fffbc0"), (.5, "#f0c020"), (1, "#a8700a")], .4, .35, .8), LW * 1.1)


def zoom_fit(ic):
    from actions import _magnifier
    _magnifier(ic, 30, 28, 15, 16)
    for x, y, sx, sy in ((4, 4, 1, 1), (60, 4, -1, 1), (4, 60, 1, -1), (60, 60, -1, -1)):
        d = f"M{x},{y + sy * 10}V{y}H{x + sx * 10}"
        ic.add(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="4.4"/><path d="{d}" fill="none" stroke="#0087ae" stroke-width="2.4"/>')


def kate(ic):
    """Text editor (Kate): a gold fountain pen nib writing on a sheet."""
    _page(ic, 4, 8, 44, 52)
    ic.add('<g transform="translate(40,28) rotate(40)">')
    nib = "M-7,-4H7L4,20L0,30L-4,20Z"
    ic.shadow(nib, 2.2, 1.8)
    ic.path(nib, ic.lg([(0, "#fffbc0"), (.45, "#e8b020"), (1, "#8a5a04")], 0, 0, 1, 0), INK, LW)
    ic.add(f'<path d="M0,6V26" stroke="{INK}" stroke-width="1.2"/>')
    ic.path(circle(0, 6, 2), INK, None)
    ic.path("M-8,-26H8V-4H-8Z", ic.lg([(0, "#5c6168"), (.4, "#2c3036"), (1, "#000000")], 0, 0, 1, 0), INK, LW)
    ic.add("</g>")


def cd_audio(ic):
    from devices import disc
    from gen import e_note
    disc(ic)
    ic.add('<g transform="translate(-2,-24)">')
    e_note(ic)
    ic.add("</g>")


def printer_badge(ic, kind):
    from devices import printer
    printer(ic)
    if kind == "error":
        _no(ic, 48, 48, 12)
    else:
        _badge(ic, 48, 48, 12, "green", "")
        ic.path("M44,42L54,48L44,54Z", "#ffffff", None)


def checkbox(ic):
    b = rrect(8, 8, 48, 48, 4)
    ic.shadow(b, 2.4, 2)
    ic.path(b, ic.lg([(0, "#ffffff"), (1, "#d9dce0")], 0, 0, 1, 1), INK, LW * 1.3)
    from settingstrace import _tick_shape
    ic.add('<g transform="translate(13,12) scale(.62)">')
    _mpath(ic, _tick_shape(), ic.lg([(0, "#c8ffa8"), (.35, "#3cd02a"), (.75, "#14920a"), (1, "#0a4a06")], 0, 0, .4, 1), LW * 1.6)
    ic.add("</g>")


# ------------------------------------------------------------------ registry
TT = {"status": {}, "actions": {}, "apps": {}, "devices": {}}
S, A, P, D = TT["status"], TT["actions"], TT["apps"], TT["devices"]
for pct in LEVELS:
    S[f"battery-{pct:03d}"] = _ic(_battery_level, pct)
    S[f"battery-{pct:03d}-charging"] = _ic(_battery_level, pct, True)
S["battery-missing"] = _ic(battery_missing)
S["battery-full-charged"] = _ic(battery_full_charged)
for name, n, c in (("low", 1, "teal"), ("medium", 2, "teal"), ("high", 3, "teal"), ("high-warning", 3, "amber"), ("high-danger", 3, "red")):
    S[f"audio-volume-{name}"] = _ic(volume, n, c)
for name, lvl in (("low", .3), ("medium", .6), ("high", 1.0)):
    S[f"microphone-sensitivity-{name}"] = _ic(mic_level, lvl)
S["microphone-sensitivity-muted"] = _ic(mic_level, 0, True)
for pct, lit in WIFI_LEVELS.items():
    S[f"network-wireless-{pct}"] = _ic(wifi, lit)
    S[f"network-wireless-{pct}-limited"] = _ic(wifi, lit, badge=_bang)
    S[f"network-wireless-{pct}-locked"] = _ic(wifi, lit, badge=_lock)
S["network-wireless-acquiring"] = _ic(wifi, 0, badge=_dots)
S["network-wireless-available"] = _ic(wifi, 5, badge=lambda ic: _dots(ic, colour="green"))
S["network-wireless-disconnected"] = _ic(wifi, 0, badge=_no)
S["network-wireless-off"] = _ic(wifi, 0, off=True)
S["network-wireless-on"] = _ic(wifi, 5, GREEN, badge=_ok)
S["network-wireless-hotspot"] = _ic(wifi, 5, GREEN)
S["network-wired"] = _ic(wired)
S["network-wired-activated"] = _ic(wired, _ok)
S["network-wired-activated-limited"] = _ic(wired, _bang)
S["network-wired-activated-locked"] = _ic(wired, _lock)
S["network-wired-available"] = _ic(wired, _dots)
S["network-wired-disconnected"] = _ic(wired, _no)
S["network-wired-unavailable"] = _ic(wired, None, True)
S["network-bluetooth-inactive"] = _ic(bluetooth_inactive)
S["network-vpn"] = _ic(vpn)
S["network-flightmode-on"] = _ic(plane, True)
S["network-flightmode-off"] = _ic(plane, False)
S["notification-active"] = _ic(bell, _red_dot)
S["notification-empty"] = _ic(bell, _empty_ring, True)
S["notification-inactive"] = _ic(bell, None, True)
S["notification-progress-active"] = _ic(bell, _dots)
S["notification-progress-inactive"] = _ic(bell, lambda ic: _dots(ic, colour="grey"), True)
S["media-playback-playing"] = _ic(playing)
S["media-playback-paused"] = _ic(paused)
S["media-playback-stopped"] = _ic(stopped)
S["brightness-high"] = _ic(brightness, True)
S["brightness-low"] = _ic(brightness, False)
S["video-display-brightness"] = _ic(display_brightness)
S["redshift-status-day"] = _ic(redshift_day)
S["redshift-status-off"] = _ic(redshift_off)
S["input-touchpad-on"] = _ic(touchpad_state, True)
S["input-touchpad-off"] = _ic(touchpad_state, False)
S["input-keyboard-virtual-on"] = _ic(vkbd_on)
S["system-suspend-inhibited"] = _ic(coffee, True)
S["system-suspend-uninhibited"] = _ic(coffee, False)
A.update({"media-seek-forward": _ic(seek_forward), "media-seek-backward": _ic(seek_backward),
          "media-skip-forward": _ic(skip_forward), "media-skip-backward": _ic(skip_backward), "media-eject": _ic(eject),
          "media-playlist-repeat": _ic(repeat), "media-playlist-repeat-song": _ic(repeat_one),
          "media-playlist-shuffle": _ic(shuffle), "format-justify-left": _ic(justify, "left"),
          "format-justify-right": _ic(justify, "right"), "format-justify-center": _ic(justify, "center"),
          "format-justify-fill": _ic(justify, "fill"), "format-indent-more": _ic(indent, True),
          "format-indent-less": _ic(indent, False), "format-text-italic": _ic(italic),
          "format-text-underline": _ic(underline), "format-text-strikethrough": _ic(strikethrough),
          "go-bottom": _ic(go_bottom), "go-first": _ic(go_first), "go-last": _ic(go_last),
          "color-management": _ic(colour_management), "roll": _ic(dice), "object-group": _ic(group),
          "zoom-fit-best": _ic(zoom_fit), "checkbox": _ic(checkbox)})
P.update({"accessories-calculator": _ic(calculator), "accessories-character-map": _ic(charselect),
          "office-calendar": _ic(planner), "network-modem": _ic(modem), "services": _ic(services),
          "kate": _ic(kate)})
D.update({"media-optical-cd-audio": _ic(cd_audio), "printer-error": _ic(printer_badge, "error"),
          "printer-printing": _ic(printer_badge, "printing")})


PROFILES = ("profile-balanced", "profile-performance", "profile-powersave", "symbolic")
TT_ALIASES = {}
for pct in LEVELS:
    for c in ("", "-charging"):
        for p in PROFILES:
            TT_ALIASES[f"battery-{pct:03d}{c}-{p}"] = f"status/battery-{pct:03d}{c}"
TT_ALIASES.update({
    "battery-empty": "status/battery-000", "battery-empty-symbolic": "status/battery-000",
    "battery-empty-charging": "status/battery-000-charging", "battery-empty-charging-symbolic": "status/battery-000-charging",
    "battery-good": "status/battery-070", "battery-good-symbolic": "status/battery-070",
    "battery-good-charging": "status/battery-070-charging", "battery-good-charging-symbolic": "status/battery-070-charging",
    "battery-low-charging": "status/battery-020-charging", "battery-low-charging-symbolic": "status/battery-020-charging",
    "battery-caution-charging": "status/battery-010-charging", "battery-caution-charging-symbolic": "status/battery-010-charging",
    "battery-missing-symbolic": "status/battery-missing", "battery-full-charged-symbolic": "status/battery-full-charged",
    "battery-caution-symbolic": "status/battery-caution", "battery-full-charging-symbolic": "status/battery-full-charging",
    "battery-full-symbolic": "status/battery-full", "battery-low-symbolic": "status/battery-low",
    "battery-ups-symbolic": "status/battery-ups",
    "brightness-high-symbolic": "status/brightness-high", "brightness-low-symbolic": "status/brightness-low",
    "video-display-brightness-symbolic": "status/video-display-brightness",
    "redshift-status-day-symbolic": "status/redshift-status-day", "redshift-status-off-symbolic": "status/redshift-status-off",
    "redshift-status-on-symbolic": "apps/redshift-status-on",
    "input-touchpad-on-symbolic": "status/input-touchpad-on", "input-touchpad-off-symbolic": "status/input-touchpad-off",
    "network-vpn-symbolic": "status/network-vpn", "network-bluetooth": "apps/preferences-system-bluetooth",
    "network-bluetooth-inactive-symbolic": "status/network-bluetooth-inactive",
    "network-bluetooth-activated-symbolic": "status/network-bluetooth-activated",
    "network-wireless-bluetooth": "apps/preferences-system-bluetooth", "network-wireless": "status/network-wireless-100",
    "network-wired-symbolic": "status/network-wired", "network-wired-activated-symbolic": "status/network-wired-activated",
    "network-wired-disconnected-symbolic": "status/network-wired-disconnected",
    "network-wired-unavailable-symbolic": "status/network-wired-unavailable",
    "network-wireless-acquiring-symbolic": "status/network-wireless-acquiring",
    "network-wireless-disconnected-symbolic": "status/network-wireless-disconnected",
    "network-wireless-hotspot-symbolic": "status/network-wireless-hotspot",
    "notification-disabled": "status/notifications-disabled", "notification-disabled-symbolic": "status/notifications-disabled",
    "notifications-disabled-symbolic": "status/notifications-disabled",
    "notification-inactive-symbolic": "status/notification-inactive", "notification-active-symbolic": "status/notification-active",
    "notification-empty-symbolic": "status/notification-empty",
    "preferences-desktop-notification-symbolic": "apps/preferences-desktop-notification",
    "media-playback-playing-symbolic": "status/media-playback-playing", "media-playback-paused-symbolic": "status/media-playback-paused",
    "media-playback-stopped-symbolic": "status/media-playback-stopped",
    "media-seek-forward-symbolic": "actions/media-seek-forward", "media-seek-backward-symbolic": "actions/media-seek-backward",
    "media-skip-forward-symbolic": "actions/media-skip-forward", "media-skip-backward-symbolic": "actions/media-skip-backward",
    "media-eject-symbolic": "actions/media-eject", "media-playlist-repeat-symbolic": "actions/media-playlist-repeat",
    "media-playlist-repeat-amarok": "actions/media-playlist-repeat", "media-repeat-single": "actions/media-playlist-repeat-song",
    "media-repeat-single-symbolic": "actions/media-playlist-repeat-song", "media-repeat-track-amarok": "actions/media-playlist-repeat-song",
    "media-playlist-shuffle-symbolic": "actions/media-playlist-shuffle",
    "microphone-sensitivity-low-symbolic": "status/microphone-sensitivity-low",
    "microphone-sensitivity-medium-symbolic": "status/microphone-sensitivity-medium",
    "microphone-sensitivity-high-symbolic": "status/microphone-sensitivity-high",
    "microphone-sensitivity-muted-symbolic": "status/microphone-sensitivity-muted", "microphone": "status/mic-ready",
    "audio-volume-low-symbolic": "status/audio-volume-low", "audio-volume-medium-symbolic": "status/audio-volume-medium",
    "audio-volume-high-symbolic": "status/audio-volume-high", "audio-volume-high-warning-symbolic": "status/audio-volume-high-warning",
    "audio-volume-high-danger-symbolic": "status/audio-volume-high-danger", "speaker": "apps/audio-speakers",
    "kmix": "apps/audio-speakers", "audio-card-symbolic": "apps/audio-card", "internal": "apps/audio-card",
    "audio-headphones-symbolic": "apps/audio-headphones", "headphone": "apps/audio-headphones",
    "arrow-left": "actions/go-previous", "camera-web-symbolic": "status/camera-ready", "webcam": "status/camera-ready",
    "computer-symbolic": "devices/computer", "desktop-symbolic": "places/user-desktop",
    "dialog-align-and-distribute": "actions/align-horizontal-left", "dialog-filters": "actions/view-filter",
    "dialog-question": "actions/help-browser", "dialog-scripts-symbolic": "mimetypes/application-x-shellscript",
    "drive-harddisk-encrypted": "devices/drive-harddisk", "drive-harddisk-root": "devices/drive-harddisk",
    "drive-harddisk-symbolic": "devices/drive-harddisk", "drive-symbolic": "devices/drive-harddisk",
    "folder-decrypted": "places/folder", "folder-encrypted": "places/folder-locked", "folder-symbolic": "places/folder",
    "fork": "apps/preferences-desktop-launch-feedback", "gtk-bold": "actions/format-text-bold",
    "gtk-clear": "actions/edit-clear-locationbar-ltr", "gtk-execute": "apps/system-run", "gtk-floppy": "actions/document-save",
    "system-save-session": "actions/document-save", "gtk-preferences": "actions/configure",
    "gtk-properties": "actions/document-properties", "media-track-edit-amarok": "actions/document-properties",
    "gtk-quit": "actions/application-exit", "system-log-out-symbolic": "actions/system-log-out",
    "system-shutdown-symbolic": "actions/system-shutdown", "handset": "devices/smartphone", "kdeconnect": "devices/smartphone",
    "kdeconnect-symbolic": "devices/smartphone", "phone-symbolic": "devices/smartphone", "kdeconnect-tray": "devices/smartphone",
    "kdeconnect-tray-symbolic": "devices/smartphone", "input-touchpad-symbolic": "apps/preferences-desktop-touchpad",
    "internet-web-browser-symbolic": "apps/internet-web-browser", "kate-symbolic": "apps/kate",
    "accessories-text-editor": "apps/kate", "org.kde.kate": "apps/kate", "klipper-symbolic": "actions/klipper",
    "kmenuedit": "apps/preferences-desktop-menu-edit", "knotes": "actions/edit-comment", "knotes-symbolic": "actions/edit-comment",
    "org.kde.plasma.notes": "actions/edit-comment", "ksysguardd": "apps/utilities-system-monitor",
    "mail-unread-new": "status/mail-unread", "mail-unread-new-symbolic": "status/mail-unread",
    "media-floppy-symbolic": "devices/media-floppy", "media-import-audio-cd": "actions/document-import",
    "media-optical-audio-symbolic": "devices/media-optical-cd-audio", "media-optical-cd-audio-symbolic": "devices/media-optical-cd-audio",
    "media-optical-data": "devices/media-optical-cd", "media-optical-mixed-cd": "devices/media-optical-cd",
    "media-optical-symbolic": "devices/media-optical", "media-optical-video": "devices/media-optical-dvd",
    "media-optical-dvd-symbolic": "devices/media-optical-dvd", "media-optical-recordable-symbolic": "devices/media-optical-recordable",
    "media-standard-track-progression-amarok": "actions/format-list-ordered", "media-track-remove-amarok": "actions/list-remove",
    "remove": "actions/list-remove", "office-calendar-symbolic": "apps/office-calendar", "x-office-calendar": "apps/office-calendar",
    "org.kde.korganizer": "apps/office-calendar", "korganizer": "apps/office-calendar",
    "accessories-calculator-symbolic": "apps/accessories-calculator", "kcalc": "apps/accessories-calculator",
    "org.kde.kcalc": "apps/accessories-calculator", "accessories-character-map-symbolic": "apps/accessories-character-map",
    "kcharselect": "apps/accessories-character-map", "preferences-desktop-plasma": "apps/kmenu",
    "preferences-system-bluetooth-symbolic": "apps/preferences-system-bluetooth",
    "preferences-system-windows-effect-coverswitch": "apps/preferences-system-tabbox",
    "printer-error-symbolic": "devices/printer-error", "printer-network-symbolic": "devices/printer-network",
    "printer-printing-symbolic": "devices/printer-printing", "system-hibernate-symbolic": "actions/system-hibernate",
    "system-lock-screen-symbolic": "actions/system-lock-screen", "system-log-out-rtl-symbolic": "actions/system-log-out",
    "system-reboot-symbolic": "actions/system-reboot", "system-reboot-update-symbolic": "actions/system-reboot-update",
    "system-shutdown-update-symbolic": "actions/system-shutdown-update",
    "system-software-update-symbolic": "apps/system-software-update", "system-suspend-hibernate-symbolic": "actions/system-hibernate",
    "system-suspend-symbolic": "actions/system-suspend", "system-switch-user-symbolic": "actions/system-switch-user",
    "unlock-symbolic": "emblems/object-unlocked", "update-high-symbolic": "actions/update-high",
    "update-low-symbolic": "actions/update-low", "update-none-symbolic": "actions/update-none",
    "video-television-symbolic": "apps/tv", "view-history": "actions/document-open-recent",
    "window-symbolic": "apps/preferences-system-tabbox", "drive-removable-media-symbolic": "devices/drive-removable-media",
    "drive-removable-media-usb-pendrive-symbolic": "apps/drive-removable-media-usb-pendrive",
    "drive-removable-media-usb-symbolic": "devices/drive-removable-media-usb", "media-flash-memory-stick": "devices/media-flash",
    "media-flash-sd-mmc": "devices/media-flash", "media-flash-smart-media": "devices/media-flash",
    "media-flash-symbolic": "devices/media-flash", "media-removable-symbolic": "devices/drive-removable-media",
    "services-symbolic": "apps/services", "roll-symbolic": "actions/roll", "object-group-symbolic": "actions/object-group",
    "zoom-fit-best-symbolic": "actions/zoom-fit-best", "checkbox-symbolic": "actions/checkbox",
    "format-justify-left-symbolic": "actions/format-justify-left", "format-justify-right-symbolic": "actions/format-justify-right",
    "format-justify-center-symbolic": "actions/format-justify-center", "format-justify-fill-symbolic": "actions/format-justify-fill",
    "format-indent-more-symbolic": "actions/format-indent-more", "format-indent-less-symbolic": "actions/format-indent-less",
    "format-text-italic-symbolic": "actions/format-text-italic", "format-text-underline-symbolic": "actions/format-text-underline",
    "format-text-strikethrough-symbolic": "actions/format-text-strikethrough", "gtk-italic": "actions/format-text-italic",
    "gtk-underline": "actions/format-text-underline", "gtk-strikethrough": "actions/format-text-strikethrough",
    "go-bottom-symbolic": "actions/go-bottom", "go-first-symbolic": "actions/go-first", "go-last-symbolic": "actions/go-last",
    "network-modem-symbolic": "apps/network-modem", "kppp": "apps/network-modem",
    "help-contextual": "actions/help-whatsthis", "network-wireless-symbolic": "status/network-wireless-100",
})
# connection strength names map onto the 0-100 signal set
for n, p in (("00", 0), ("20", 20), ("25", 20), ("40", 40), ("50", 40), ("60", 60), ("75", 80), ("80", 80), ("100", 100)):
    TT_ALIASES[f"network-wireless-connected-{n}"] = f"status/network-wireless-{p}"
    TT_ALIASES[f"network-wireless-connected-{n}-symbolic"] = f"status/network-wireless-{p}"
for n, p in (("none", 0), ("weak", 20), ("ok", 40), ("good", 60), ("excellent", 100)):
    TT_ALIASES[f"network-wireless-signal-{n}"] = f"status/network-wireless-{p}"
    TT_ALIASES[f"network-wireless-signal-{n}-symbolic"] = f"status/network-wireless-{p}"
for p in WIFI_LEVELS:
    for suf in ("", "-limited", "-locked"):
        TT_ALIASES[f"network-wireless-{p}{suf}-symbolic"] = f"status/network-wireless-{p}{suf}"


def write(out):
    n = 0
    for ctx, icons in TT.items():
        d = f"{out}/scalable/{ctx}"
        os.makedirs(d, exist_ok=True)
        for name, fn in icons.items():
            open(f"{d}/{name}.svg", "w").write(fn().svg(64))
            n += 1
    missing = []
    ctxs = os.listdir(f"{out}/scalable")
    for a, t in TT_ALIASES.items():
        ctx, name = t.split("/")
        d = f"{out}/scalable/{ctx}"
        if not os.path.exists(f"{d}/{name}.svg"):
            missing.append(t)
            continue
        if not any(os.path.lexists(f"{out}/scalable/{c}/{a}.svg") for c in ctxs):
            os.symlink(f"{name}.svg", f"{d}/{a}.svg")
    if missing:
        print("traytrace: alias targets missing:", sorted(set(missing)))
    return n
