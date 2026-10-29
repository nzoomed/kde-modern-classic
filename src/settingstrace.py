"""KDE Classic Vector: icons System Settings still took from the KDE Classic bitmaps, redrawn as vectors
(batteries, playback stop, input and network states, fingerprint, rotate/flip/move, table resizing,
help, TV, system monitor ...), plus aliases where the meaning matches an icon already drawn.

Arrows follow STYLE.md (teal #0087AE, pale #C5E4EF highlight, mitred corners); state badges reuse the
round badges from the shell icons. Lighting from the top-left, Qt-SVG safe.
"""
import math, os
from gen import Icon, INK, LW, circle, rrect
from actions import _mpath, TEAL, _curl_points

def _ic(fn):
    def f():
        ic = Icon()
        fn(ic)
        return ic
    return f


def _poly(pts):
    return "M" + "L".join(f"{x:.2f},{y:.2f}" for x, y in pts) + "Z"


def _badge(ic, x, y, r, colour, glyph):
    from shell import _badge as b
    b(ic, x, y, r, colour, glyph)


def _ok(ic, x=48, y=48, r=11):
    _badge(ic, x, y, r, "green", f"M{x - r * .45:.2f},{y + r * .02:.2f}L{x - r * .1:.2f},{y + r * .38:.2f}L{x + r * .48:.2f},{y - r * .36:.2f}")


def _no(ic, x=48, y=48, r=11):
    k = r * .38
    _badge(ic, x, y, r, "red", f"M{x - k:.2f},{y - k:.2f}L{x + k:.2f},{y + k:.2f}M{x + k:.2f},{y - k:.2f}L{x - k:.2f},{y + k:.2f}")


def _teal(ic, d, w=LW * 1.2, shadow=True):
    if shadow:
        ic.shadow(d, 2, 1.7)
    _mpath(ic, d, ic.lg([(0, TEAL[0]), (.35, TEAL[1]), (.7, TEAL[2]), (1, TEAL[3])], 0, 0, .35, 1), w)


def _arrow_pts(x0, y0, x1, y1, shaft, head_w, head_len):
    """A straight block arrow from (x0,y0) to the tip at (x1,y1)."""
    L = math.hypot(x1 - x0, y1 - y0)
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    nx, ny = -uy, ux
    bx, by = x1 - ux * head_len, y1 - uy * head_len
    return [(x0 + nx * shaft, y0 + ny * shaft), (bx + nx * shaft, by + ny * shaft), (bx + nx * head_w, by + ny * head_w),
            (x1, y1), (bx - nx * head_w, by - ny * head_w), (bx - nx * shaft, by - ny * shaft), (x0 - nx * shaft, y0 - ny * shaft)]


def _double_arrow(x0, y0, x1, y1, shaft=2.6, head_w=7, head_len=8):
    L = math.hypot(x1 - x0, y1 - y0)
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    nx, ny = -uy, ux
    a = (x0 + ux * head_len, y0 + uy * head_len)
    b = (x1 - ux * head_len, y1 - uy * head_len)
    return _poly([(x0, y0), (a[0] + nx * head_w, a[1] + ny * head_w), (a[0] + nx * shaft, a[1] + ny * shaft),
                  (b[0] + nx * shaft, b[1] + ny * shaft), (b[0] + nx * head_w, b[1] + ny * head_w), (x1, y1),
                  (b[0] - nx * head_w, b[1] - ny * head_w), (b[0] - nx * shaft, b[1] - ny * shaft),
                  (a[0] - nx * shaft, a[1] - ny * shaft), (a[0] - nx * head_w, a[1] - ny * head_w)])


def _page(ic, x=10, y=4, w=38, h=54):
    d = f"M{x},{y}H{x + w - 11}L{x + w},{y + 11}V{y + h}H{x}Z"
    ic.shadow(d, 2.4, 2)
    ic.path(d, ic.lg([(0, "#ffffff"), (.5, "#fcf8f0"), (1, "#d9c8a8")], 0, 0, 1, 1), INK, LW)
    ic.path(f"M{x + w - 11},{y}V{y + 11}H{x + w}", ic.lg([(0, "#ffffff"), (1, "#bdb5a8")], 0, 0, 1, 1), INK, 1)


def _lines(ic, x, y, w, n, gap=5):
    for k in range(n):
        ic.add(f'<path d="M{x},{y + k * gap}H{x + w - (k % 3) * 5}" stroke="#7b818a" stroke-width="1.6" stroke-dasharray="3.4 1.2"/>')


# ------------------------------------------------------------------ battery
def _battery(ic, level, colour, bolt=False):
    """KDE Classic's upright battery: a glossy grey cell with a cap, its charge shown as a coloured fill."""
    ic.path(rrect(25, 3, 14, 6, 1.5), ic.lg([(0, "#ffffff"), (.5, "#9aa0a8"), (1, "#4c5158")], 0, 0, 1, 0), INK, 1.1)
    cell = rrect(15, 7, 34, 54, 5)
    ic.shadow(cell, 2.6, 2.2)
    ic.path(cell, ic.lg([(0, "#8a9098"), (.3, "#f4f5f7"), (.6, "#c3c7cd"), (1, "#5c6168")], 0, 0, 1, 0), INK, LW * 1.2)
    ic.path(rrect(19, 11, 26, 46, 3), ic.lg([(0, "#d9dce0"), (1, "#a8adb4")], 0, 0, 1, 0), "#4c5158", .9)
    if level:
        top = 57 - 46 * level
        cols = {"green": ("#b4f8a0", "#1ec81a", "#0a6a08"), "yellow": ("#fffbb0", "#f0e010", "#8a7a04"),
                "red": ("#ffb0a0", "#f02a1a", "#7a0804")}[colour]
        ic.path(rrect(19, top, 26, 57 - top, 3 if level > .15 else 2.2), ic.lg([(0, cols[2]), (.35, cols[0]), (.6, cols[1]), (1, cols[2])], 0, 0, 1, 0), "#14371a" if colour == "green" else INK, .9)
    ic.add('<path d="M22,14V52" stroke="#fff" stroke-opacity=".6" stroke-width="2" stroke-linecap="round"/>')
    if bolt:
        d = "M36,14L23,37H31L27,54L42,29H34L38,14Z"
        ic.path(d, ic.lg([(0, "#fffbb0"), (.5, "#ffe010"), (1, "#c88a04")]), INK, 1.2)


def battery_full(ic): _battery(ic, 1, "green")
def battery_charging(ic): _battery(ic, 1, "green", bolt=True)
def battery_low(ic): _battery(ic, .2, "yellow")
def battery_caution(ic): _battery(ic, .1, "red")


def battery_ups(ic):
    """UPS: the full battery with a green plus - a battery kept charged from the mains."""
    _battery(ic, 1, "green")
    _badge(ic, 48, 48, 12, "green", "M48,42V54M42,48H54")


# ------------------------------------------------------------------ sound
def _speaker(ic, dx=0, dy=-12, k=1.0):
    from gen import e_speaker
    ic.add(f'<g transform="translate({dx},{dy}) scale({k})">')
    e_speaker(ic)
    ic.add("</g>")


# Kept for reference: a grey-speaker / blue-wave redraw traced from KDE Classic's audio-volume icons was tried
# on 2026-10-20 and rejected; the teal speaker stays. See ROADMAP (speaker and printer).


def audio_volume_muted(ic):
    from traytrace import VOL_SPEAKER
    _speaker(ic, *VOL_SPEAKER)
    _no(ic, 47, 47, 12)


def audio_speakers(ic):
    """Speakers: the KDE Classic loudspeaker with sound waves coming out."""
    from traytrace import _waves, VOL_SPEAKER, VOL_WAVES
    _speaker(ic, *VOL_SPEAKER)
    _waves(ic, 3, "teal", **VOL_WAVES)


# ------------------------------------------------------------------ dialogs and states
def _tick_shape():
    return "M5,33L16,22L27,33L50,8L60,18L27,56Z"


def dialog_ok(ic):
    """OK: KDE Classic's bold green tick."""
    d = _tick_shape()
    ic.shadow(d, 2.6, 2.2)
    _mpath(ic, d, ic.lg([(0, "#c8ffa8"), (.35, "#3cd02a"), (.75, "#14920a"), (1, "#0a4a06")], 0, 0, .4, 1), LW * 1.3)
    ic.add('<path d="M9,33L16,26L27,37L50,12.5" fill="none" stroke="#fff" stroke-opacity=".6" stroke-width="1.6" stroke-linejoin="miter"/>')


def help_browser(ic):
    """Help: KDE Classic's glossy blue question mark."""
    d = ("M18,20C18,9 26,4 34,4C44,4 50,10 50,18C50,26 44,29 40,32C37,34 36,36 36,40V43H26V38C26,32 29,29 33,26"
         "C37,23 39,21.6 39,18.4C39,15 36.6,13 33.6,13C30,13 28.6,15.6 28.6,20Z")
    ic.shadow(d, 2.6, 2.2)
    ic.path(d, ic.lg([(0, "#c8e4ff"), (.35, "#3a8ae0"), (.75, "#1a4aa0"), (1, "#0a2050")], 0, 0, 1, 1), INK, LW * 1.2)
    ic.add('<path d="M21,19C21,12 27,7.4 34,7.4" fill="none" stroke="#fff" stroke-opacity=".7" stroke-width="2" stroke-linecap="round"/>')
    ic.shadow(circle(31, 53, 6), 2.2, 1.8)
    ic.path(circle(31, 53, 6), ic.rg([(0, "#c8e4ff"), (.5, "#3a8ae0"), (1, "#0a2050")], .4, .35, .8), INK, LW * 1.2)


def system_help(ic):
    """Help centre: KDE Classic's red and white lifebuoy round a blue question mark."""
    o, i = 28, 15
    ring = (f"M{32 - o},32A{o},{o} 0 1 0 {32 + o},32A{o},{o} 0 1 0 {32 - o},32Z"
            f"M{32 - i},32A{i},{i} 0 1 1 {32 + i},32A{i},{i} 0 1 1 {32 - i},32Z")
    ic.shadow(ring, 2.6, 2.2)
    ic.add(f'<path d="{ring}" fill="{ic.lg([(0, "#ffffff"), (.6, "#e4e6e9"), (1, "#a8adb4")], 0, 0, 1, 1)}" fill-rule="evenodd" stroke="{INK}" stroke-width="{LW * 1.2}"/>')
    for k in range(4):
        a0, a1 = math.radians(k * 90 + 20), math.radians(k * 90 + 70)
        seg = (f"M{32 + o * math.cos(a0):.2f},{32 + o * math.sin(a0):.2f}A{o},{o} 0 0 1 {32 + o * math.cos(a1):.2f},{32 + o * math.sin(a1):.2f}"
               f"L{32 + i * math.cos(a1):.2f},{32 + i * math.sin(a1):.2f}A{i},{i} 0 0 0 {32 + i * math.cos(a0):.2f},{32 + i * math.sin(a0):.2f}Z")
        ic.path(seg, ic.lg([(0, "#ff8a7a"), (.5, "#e0200a"), (1, "#7a0804")], 0, 0, 1, 1), INK, 1)
    ic.add(f'<path d="M{32 - o + 3},26A{o - 3},{o - 3} 0 0 1 26,{32 - o + 3}" fill="none" stroke="#fff" stroke-opacity=".7" stroke-width="1.6" stroke-linecap="round"/>')
    ic.add('<path d="M27,28.4Q27,24 32,24Q37,24 37,28Q37,31 33,32.6V35" fill="none" stroke="#1a4aa0" stroke-width="3" stroke-linecap="round"/>')
    ic.path(circle(33, 39, 1.8), "#1a4aa0", None)


def discover_app(ic):
    """Discover (the app): the ribboned parcel, enlarged to fill the canvas so it reads at full size on the taskbar."""
    from discover import parcel
    ic.add('<g transform="translate(32,31.4) scale(1.17) translate(-32.8,-30.8)">')
    parcel(ic)
    ic.add("</g>")


def security_medium(ic):
    """Security medium: KDE Classic's half-encrypted padlock, the shackle lifted with one leg out."""
    from dolphin import _padlock
    ic.add('<g transform="translate(0,4)">')
    _padlock(ic, "half")
    ic.add("</g>")


def notifications_disabled(ic):
    from settings import notifications, BELL_GREY
    notifications(ic, BELL_GREY)
    ic.add('<path d="M8,6L56,58" stroke="#5a0402" stroke-width="7" stroke-linecap="round"/><path d="M8,6L56,58" stroke="#f02a1a" stroke-width="4.4" stroke-linecap="round"/>')


def network_bluetooth_activated(ic):
    from settings import bluetooth_kcm
    ic.add('<g transform="translate(-4,-2)">')
    bluetooth_kcm(ic)
    ic.add("</g>")
    _ok(ic, 48, 49, 12)


def _plugs(ic, gap):
    """Two plug halves, one coming in from each side, with sparks in the gap between them."""
    for sgn in (1, -1):
        cx, cy = 32 + sgn * (gap + 10), 32 - sgn * (gap + 10)
        ic.add(f'<g transform="translate({cx},{cy}) rotate({45 if sgn == 1 else 225})">')
        body = "M-6,-7H6V8H-6Z"
        ic.shadow(body, 2, 1.6)
        ic.path(body, ic.lg([(0, "#5c6168"), (.4, "#f4f5f7"), (1, "#6c727a")], 0, 0, 1, 0), INK, LW)
        ic.add(f'<path d="M0,8V22" stroke="{INK}" stroke-width="5"/><path d="M0,8V22" stroke="#8a9098" stroke-width="3"/>')
        if sgn == 1:
            ic.add(f'<path d="M-3,-7V-13M3,-7V-13" stroke="{INK}" stroke-width="2.8" stroke-linecap="square"/><path d="M-3,-7.6V-12.6M3,-7.6V-12.6" stroke="#e8c43a" stroke-width="1.2"/>')
        else:
            ic.path("M-4,-7H4V-9H-4Z", "#2c3036", None)
        ic.add("</g>")


def network_connect(ic):
    _plugs(ic, 3)
    _ok(ic, 48, 48, 12)


def network_disconnect(ic):
    _plugs(ic, 9)
    for x, y in ((24, 26), (30, 32), (36, 38)):
        ic.add(f'<path d="M{x - 2},{y - 3}L{x + 2},{y + 3}" stroke="{INK}" stroke-width="3" stroke-linecap="round"/><path d="M{x - 2},{y - 3}L{x + 2},{y + 3}" stroke="#ffe010" stroke-width="1.6" stroke-linecap="round"/>')
    _no(ic, 48, 48, 12)


def input_caps_on(ic):
    """Caps Lock on: a grey key with an outlined up arrow, its green light lit."""
    k = rrect(6, 6, 52, 52, 7)
    ic.shadow(k, 2.6, 2.2)
    ic.path(k, ic.lg([(0, "#ffffff"), (.5, "#d9dce0"), (1, "#8a9098")], 0, 0, 1, 1), INK, LW * 1.2)
    ic.path(rrect(11, 11, 42, 42, 5), ic.lg([(0, "#c3c7cd"), (1, "#f4f5f7")], 0, 0, 1, 1), "#7b818a", .9)
    ic.path("M32,16L47,32H39V40H25V32H17Z", INK, None)
    ic.path("M25,44H39V48H25Z", INK, None)
    ic.path(circle(48, 15, 4), ic.rg([(0, "#d8ffc8"), (.5, "#3fd02a"), (1, "#0e6a08")], .4, .35, .8), INK, 1)


def input_keyboard_virtual_off(ic):
    from settings import virtual_keyboard
    virtual_keyboard(ic)
    _no(ic, 48, 48, 12)


def fingerprint(ic, badge=None):
    """Fingerprint: purple ridges of a print on a silver reader pad."""
    pad = rrect(5, 5, 54, 54, 12)
    ic.shadow(pad, 2.6, 2.2)
    ic.path(pad, ic.lg([(0, "#ffffff"), (.5, "#c3c7cd"), (1, "#7b818a")], 0, 0, 1, 1), INK, LW * 1.2)
    for k, r in enumerate((4, 8.5, 13, 17.5, 22)):
        d = f"M{32 - r:.2f},{44 if k else 40}V{36 - r * .2:.2f}A{r},{r * 1.1} 0 0 1 {32 + r:.2f},{36 - r * .2:.2f}V{44 - k * 1.5:.2f}"
        ic.add(f'<path d="{d}" fill="none" stroke="#3a0a4a" stroke-width="3.8" stroke-linecap="round"/>'
               f'<path d="{d}" fill="none" stroke="#a020b0" stroke-width="2.2" stroke-linecap="round"/>')
    ic.add('<path d="M32,40V52" stroke="#3a0a4a" stroke-width="3.8" stroke-linecap="round"/><path d="M32,40V52" stroke="#a020b0" stroke-width="2.2" stroke-linecap="round"/>')
    if badge:
        badge(ic)


def fingerprint_gui(ic):
    from settings import _gear
    def gear(ic):
        _gear(ic, 49, 49, 12)
    fingerprint(ic, gear)


def font_enable(ic):
    from filetypes import _tt
    _tt(ic)
    _ok(ic, 48, 49, 12)


def font_disable(ic):
    from filetypes import _tt
    _tt(ic)
    _no(ic, 48, 49, 12)


# ------------------------------------------------------------------ arrows and transforms
def go_top(ic):
    """To the top: the teal arrow pointing up to a bar."""
    _teal(ic, _poly(_arrow_pts(32, 60, 32, 16, 8, 20, 20)))
    ic.add('<path d="M28,52V36" stroke="#fff" stroke-opacity=".7" stroke-width="1.6"/>')
    _teal(ic, "M8,5H56V12H8Z")
    ic.add('<path d="M10,7H54" stroke="#fff" stroke-opacity=".75" stroke-width="1.4"/>')


def transform_move(ic):
    """Move: a four-way teal arrow."""
    s, hw, hl = 3.6, 9, 11
    d = (f"M32,3L{32 + hw},{3 + hl}H{32 + s}V{32 - s}H{61 - hl}V{32 - hw}L61,32L{61 - hl},{32 + hw}V{32 + s}H{32 + s}"
         f"V{61 - hl}H{32 + hw}L32,61L{32 - hw},{61 - hl}H{32 - s}V{32 + s}H{3 + hl}V{32 + hw}L3,32L{3 + hl},{32 - hw}V{32 - s}"
         f"H{32 - s}V{3 + hl}H{32 - hw}Z")
    _teal(ic, d)
    ic.add(f'<path d="M{32 - s + 1.4},{3 + hl + 2}V{32 - s - 1}M{3 + hl + 2},{32 - s + 1.4}H{32 - s - 1}" stroke="#fff" stroke-opacity=".7" stroke-width="1.4"/>')


def _arc_arrow(ic, clockwise):
    """A teal arrow curling round the top of a dial, for rotating."""
    pts = _curl_points(32, 34, 21, 5, 200 if not clockwise else 200, 150, 13, 11, taper=40, N=40)
    if clockwise:
        pts = [(64 - x, y) for x, y in pts]
    _teal(ic, _poly(pts))


def _dial(ic):
    ic.path(circle(32, 36, 15), ic.lg([(0, "#ffffff"), (1, "#d9dce0")], 0, 0, 1, 1), INK, LW)
    ic.add(f'<path d="M32,26V46M22,36H42" stroke="{INK}" stroke-width="1.8"/>')


def rotate_left(ic):
    _dial(ic)
    _arc_arrow(ic, False)


def rotate_right(ic):
    _dial(ic)
    _arc_arrow(ic, True)


def flip_vertical(ic):
    """Flip vertically: a solid teal triangle above the mirror line and its outline reflected below."""
    up = "M10,27L32,6L54,27Z"
    _teal(ic, up)
    ic.add(f'<path d="M4,32H60" stroke="{INK}" stroke-width="1.6" stroke-dasharray="4 2.4"/>')
    ic.path("M10,37L32,58L54,37Z", "#ffffff", INK, LW)
    ic.add('<path d="M15,40L32,56" stroke="#c5e4ef" stroke-width="1.4"/>')


def distribute_horizontal(ic):
    """Distribute horizontally: three blocks spaced evenly between two guides."""
    ic.add(f'<path d="M4,6V58M60,6V58" stroke="{INK}" stroke-width="2" stroke-dasharray="4 2"/>')
    for x, w in ((8, 10), (27, 10), (46, 10)):
        d = f"M{x},14H{x + w}V50H{x}Z"
        ic.shadow(d, 1.8, 1.5)
        ic.path(d, ic.lg([(0, "#ffffff"), (.5, "#c3c7cd"), (1, "#7b818a")], 0, 0, 1, 0), INK, LW)
    for x0 in (18, 37):
        _teal(ic, _double_arrow(x0 + .6, 32, x0 + 8.4, 32, 1.2, 3.6, 3.4), 1, shadow=False)


def _table(ic):
    t = "M4,8H60V56H4Z"
    ic.shadow(t, 2.4, 2)
    ic.path(t, ic.lg([(0, "#ffffff"), (1, "#e4e6e9")], 0, 0, 1, 1), INK, LW)
    ic.path("M4,8H60V17H4Z", ic.lg([(0, "#e4e6e9"), (1, "#9aa0a8")]), INK, 1)
    ic.add('<path d="M4,30H60M4,43H60M22,8V56M42,8V56" stroke="#9aa0a8" stroke-width="1.2"/>')


def resize_column(ic):
    _table(ic)
    ic.add(f'<path d="M42,8V56" stroke="{INK}" stroke-width="2.6"/>')
    _teal(ic, _double_arrow(26, 36, 58, 36, 3, 8, 9))


def resize_row(ic):
    _table(ic)
    ic.add(f'<path d="M4,30H60" stroke="{INK}" stroke-width="2.6"/>')
    _teal(ic, _double_arrow(32, 14, 32, 54, 3, 8, 9))


# ------------------------------------------------------------------ documents
def document_export(ic):
    """Export: a page with the teal arrow leaving it to the right."""
    _page(ic, 4, 4, 36, 54)
    _lines(ic, 9, 22, 24, 6)
    _teal(ic, _poly(_arrow_pts(26, 40, 61, 40, 6, 14, 14)))


def document_import(ic):
    """Import: the teal arrow coming in from the left into a page."""
    _page(ic, 24, 4, 36, 54)
    _lines(ic, 29, 22, 24, 6)
    _teal(ic, _poly(_arrow_pts(2, 40, 38, 40, 6, 14, 14)))


def print_preview(ic):
    """Print preview: the printer with the magnifier held over its page."""
    from devices import printer
    from actions import _magnifier
    ic.add('<g transform="translate(-2,8) scale(.86)">')
    printer(ic)
    ic.add("</g>")
    _magnifier(ic, 38, 22, 13, 13)


def edit_comment(ic):
    """Comment: a yellow note with a turned-up corner and writing."""
    d = "M6,8H58V44L46,56H6Z"
    ic.shadow(d, 2.4, 2)
    ic.path(d, ic.lg([(0, "#fffbd0"), (.6, "#fff36a"), (1, "#e0c020")], 0, 0, 1, 1), INK, LW)
    ic.path("M46,56V44H58Z", ic.lg([(0, "#fff8b0"), (1, "#c8a810")], 0, 0, 1, 1), INK, 1)
    for k in range(4):
        ic.add(f'<path d="M12,{18 + k * 7}H{50 - (k % 2) * 8 - (k == 3) * 10}" stroke="#7a6a10" stroke-width="2" stroke-linecap="round"/>')


def shred(ic):
    """Shred: a page fed through the shredder, coming out as strips."""
    _page(ic, 12, 2, 40, 36)
    _lines(ic, 17, 18, 26, 4)
    for k in range(8):
        x = 12 + k * 5
        y1 = 52 + (k % 3) * 3
        d = f"M{x},38H{x + 4}V{y1}L{x + 2},{y1 + 3}L{x},{y1}Z"
        ic.path(d, ic.lg([(0, "#ffffff"), (1, "#d9c8a8")]), INK, .9)
    ic.path(rrect(6, 34, 52, 8, 2), ic.lg([(0, "#8a9098"), (.4, "#f4f5f7"), (1, "#4c5158")]), INK, LW)
    ic.path("M12,37H52V39H12Z", "#14171c", None)


def restore_defaults(ic):
    """Restore defaults: a page with the green undo arrow turning back over it."""
    from actions import _curved_arrow, CURL_GREEN, GREEN_LIT_TOP, UNDO_GEO
    _page(ic, 4, 10, 36, 50)
    _lines(ic, 9, 28, 24, 6)
    ic.add('<g transform="translate(26,-2) scale(.6)">')
    _curved_arrow(ic, CURL_GREEN, grad=GREEN_LIT_TOP, **UNDO_GEO)
    ic.add("</g>")


def draw_path(ic):
    """Draw path: a blue pen trailing a yellow path with its nodes."""
    path = "M6,54C14,40 22,58 30,46S44,36 48,28"
    ic.add(f'<path d="{path}" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/><path d="{path}" fill="none" stroke="#ffe010" stroke-width="3" stroke-linecap="round"/>')
    for x, y in ((6, 54), (30, 46)):
        ic.path(f"M{x - 3},{y - 3}H{x + 3}V{y + 3}H{x - 3}Z", "#ffffff", INK, 1.1)
    ic.add('<g transform="translate(48,28) rotate(40)">')
    body = "M-4.4,-30H4.4V-6L0,0L-4.4,-6Z"
    ic.shadow(body, 2, 1.6)
    ic.path(body, ic.lg([(0, "#8ab0ff"), (.5, "#1a4ae0"), (1, "#0a1a70")], 0, 0, 1, 0), INK, 1.2)
    ic.path("M-4.4,-6L0,0L4.4,-6Z", ic.lg([(0, "#ffffff"), (1, "#8a9098")], 0, 0, 1, 0), INK, 1)
    ic.path("M-4.4,-30H4.4V-25H-4.4Z", ic.lg([(0, "#ffffff"), (1, "#7b818a")], 0, 0, 1, 0), INK, 1)
    ic.add("</g>")


def color_picker(ic):
    """Colour picker: a glass eyedropper with its green bulb, the tip down at the lower left."""
    ic.add('<g transform="translate(32,32) rotate(45)">')
    bulb = "M-6,-30Q-6,-36 0,-36Q6,-36 6,-30V-18H-6Z"
    ic.shadow(bulb + "M-3.6,-18H3.6V20L0,28L-3.6,20Z", 2, 1.6)
    ic.path("M-3.6,-18H3.6V20L0,28L-3.6,20Z", ic.lg([(0, "#c8dce8"), (.4, "#ffffff"), (1, "#8aa8b8")], 0, 0, 1, 0), INK, 1.2)
    ic.path("M-2.2,6H2.2V20L0,25L-2.2,20Z", ic.lg([(0, "#3fd02a"), (1, "#0e6a08")], 0, 0, 1, 0), None)
    ic.path("M-7,-20H7V-15H-7Z", ic.lg([(0, "#8a9098"), (.4, "#ffffff"), (1, "#4c5158")], 0, 0, 1, 0), INK, 1.1)
    ic.path(bulb, ic.lg([(0, "#0e6a08"), (.4, "#7ae060"), (1, "#0a4a06")], 0, 0, 1, 0), INK, 1.2)
    ic.add("</g>")


def mark_location(ic):
    """Mark location: a red pennant on a pole."""
    ic.path(rrect(13, 4, 4, 56, 2), ic.lg([(0, "#5c6168"), (.4, "#f4f5f7"), (1, "#3c4148")], 0, 0, 1, 0), INK, 1.1)
    f = "M17,7Q30,3 40,9Q50,14 58,10V34Q50,38 40,33Q30,28 17,32Z"
    ic.shadow(f, 2.4, 2)
    ic.path(f, ic.lg([(0, "#ff9a8a"), (.5, "#e0200a"), (1, "#7a0804")], 0, 0, 1, 1), INK, LW)
    ic.path(circle(15, 5, 3), ic.rg([(0, "#fff8b0"), (1, "#c8940a")]), INK, 1)


# ------------------------------------------------------------------ media, windows, apps
def media_stop(ic):
    """Stop: a glossy grey square, matching play and pause."""
    o = rrect(8, 8, 48, 48, 7)
    ic.shadow(o, 2.6, 2.2)
    ic.path(o, ic.lg([(0, "#8a9098"), (.5, "#4c5158"), (1, "#141414")], 0, 0, 1, 1), INK, LW * 1.2)
    ic.path(rrect(14, 14, 36, 36, 4), ic.lg([(0, "#ffffff"), (.45, "#c3c7cd"), (1, "#6c727a")], 0, 0, .6, 1), "#2c3036", .9)


def window_minimize(ic):
    """Minimise: the KDE Classic window with a dark red arrow pointing down to the taskbar line."""
    from discover import _classic_window
    _classic_window(ic)
    ic.path("M27,22H37V36H44L32,48L20,36H27Z", "#8a1404", INK, 1)
    ic.add('<path d="M16,53H48" stroke="#8a1404" stroke-width="3.4" stroke-linecap="round"/>')


def tv(ic):
    """TV: an old wooden television set with rabbit-ear aerials."""
    ic.add(f'<path d="M32,16L18,3M32,16L46,4" stroke="{INK}" stroke-width="3.2" stroke-linecap="round"/><path d="M32,16L18,3M32,16L46,4" stroke="#c3c7cd" stroke-width="1.4" stroke-linecap="round"/>')
    ic.path(circle(32, 16, 3), "#3c4148", INK, 1)
    cab = rrect(3, 16, 58, 42, 5)
    ic.shadow(cab, 2.6, 2.2)
    ic.path(cab, ic.lg([(0, "#e0a060"), (.5, "#a85a22"), (1, "#4a2006")], 0, 0, 1, 1), INK, LW * 1.2)
    scr = "M9,22Q8,21 10,21H42Q44,21 43,22Q45,36 43,50Q44,51 42,51H10Q8,51 9,50Q7,36 9,22Z"
    ic.path(scr, ic.rg([(0, "#8ad0f0"), (.6, "#2a6aa0"), (1, "#0a1a30")], .35, .3, .9), INK, 1.2)
    ic.add('<path d="M12,26Q24,23 34,25" fill="none" stroke="#fff" stroke-opacity=".6" stroke-width="1.6" stroke-linecap="round"/>')
    for y in (27, 37):
        ic.path(circle(52, y, 3.4), ic.rg([(0, "#ffffff"), (1, "#5c6168")], .4, .35, .8), INK, 1)
    for k in range(3):
        ic.add(f'<path d="M47,{45 + k * 3}H57" stroke="#3a1a04" stroke-width="1.2"/>')


def system_monitor(ic):
    """System monitor: KDE 3's KSysGuard gauge - a round dial with a red needle swinging into the red."""
    o = circle(32, 34, 27)
    ic.shadow(o, 2.6, 2.2)
    ic.path(o, ic.lg([(0, "#ffffff"), (.5, "#c3c7cd"), (1, "#5c6168")], 0, 0, 1, 1), INK, LW * 1.2)
    ic.path(circle(32, 34, 22), ic.rg([(0, "#ffffff"), (.7, "#eef2f6"), (1, "#c8d0d8")], .45, .4, .7), INK, 1)
    ic.add(f'<path d="M{32 + 18 * math.cos(math.radians(-60)):.2f},{34 + 18 * math.sin(math.radians(-60)):.2f}A18,18 0 0 1 {32 + 18 * math.cos(math.radians(-10)):.2f},{34 + 18 * math.sin(math.radians(-10)):.2f}" fill="none" stroke="#e0200a" stroke-width="4"/>')
    for k in range(9):
        a = math.radians(-210 + k * 30)
        ic.add(f'<path d="M{32 + 15 * math.cos(a):.2f},{34 + 15 * math.sin(a):.2f}L{32 + 19.5 * math.cos(a):.2f},{34 + 19.5 * math.sin(a):.2f}" stroke="{INK}" stroke-width="1.4"/>')
    a = math.radians(-40)
    ic.add(f'<path d="M32,34L{32 + 18 * math.cos(a):.2f},{34 + 18 * math.sin(a):.2f}" stroke="#7a0804" stroke-width="3.4" stroke-linecap="round"/>'
           f'<path d="M32,34L{32 + 18 * math.cos(a):.2f},{34 + 18 * math.sin(a):.2f}" stroke="#f02a1a" stroke-width="1.8" stroke-linecap="round"/>')
    ic.path(circle(32, 34, 3.4), ic.rg([(0, "#ffffff"), (1, "#3c4148")]), INK, 1)
    ic.add('<path d="M14,22A22,22 0 0 1 28,13" fill="none" stroke="#fff" stroke-width="1.6" stroke-linecap="round"/>')


def launch_feedback(ic):
    """Launch feedback: a little red rocket taking off with its flame."""
    ic.add('<g transform="translate(34,30) rotate(45)">')
    flame = "M-6,16Q0,40 6,16Z"
    ic.path(flame, ic.lg([(0, "#fffbb0"), (.4, "#ffc010"), (1, "#e0200a")], 0, 0, 0, 1), "#7a2004", 1)
    for s in (1, -1):
        ic.path(f"M{s * 6},4L{s * 15},18L{s * 6},14Z", ic.lg([(0, "#ff8a7a"), (1, "#7a0804")]), INK, 1.1)
    body = "M0,-26Q10,-14 7,16H-7Q-10,-14 0,-26Z"
    ic.shadow(body, 2.2, 1.8)
    ic.path(body, ic.lg([(0, "#7a0804"), (.35, "#ff6a4a"), (.6, "#e0200a"), (1, "#5a0402")], 0, 0, 1, 0), INK, LW)
    ic.path(circle(0, -6, 4), ic.rg([(0, "#e8f6ff"), (1, "#3a7ab0")], .4, .35, .8), INK, 1.1)
    ic.path("M-7,12H7V16H-7Z", ic.lg([(0, "#8a9098"), (.4, "#ffffff"), (1, "#4c5158")], 0, 0, 1, 0), INK, .9)
    ic.add("</g>")


def text_to_speech(ic):
    """Text to speech: a speech bubble with lines of text and blue sound waves."""
    b = "M4,8H46Q50,8 50,12V36Q50,40 46,40H22L12,50V40H8Q4,40 4,36V12Q4,8 8,8Z"
    ic.shadow(b, 2.4, 2)
    ic.path(b, ic.lg([(0, "#ffffff"), (1, "#e4e6e9")], 0, 0, 1, 1), INK, LW)
    for k, w in enumerate((32, 26, 18)):
        ic.add(f'<path d="M11,{17 + k * 7}H{11 + w}" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>')
    for r in (6, 11):
        d = f"M{48 + r * .3:.2f},{46 - r:.2f}A{r},{r} 0 0 1 {48 + r * .3:.2f},{46 + r:.2f}"
        ic.add(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="4.4" stroke-linecap="round"/><path d="{d}" fill="none" stroke="#2a6ae0" stroke-width="2.6" stroke-linecap="round"/>')


def process_working(ic):
    """Working: a ring of dots fading round, the busy spinner."""
    for k in range(8):
        a = 2 * math.pi * k / 8 - math.pi / 2
        x, y = 32 + 20 * math.cos(a), 32 + 20 * math.sin(a)
        v = int(0x2c + (0xe4 - 0x2c) * k / 8)
        ic.path(circle(x, y, 6.4 - k * .35), f"#{v:02x}{v + 2:02x}{min(v + 6, 255):02x}", INK, 1.1)


def partition_manager(ic):
    """Partition manager: a stack of coloured blocks - the disk split into parts, as KDE 3's partitions module."""
    from uitrace import _iso_cube
    _iso_cube(ic, 22, 6, 12, ("#c8ffb0", "#3fd02a", "#14920a", "#0a4a06"))
    _iso_cube(ic, 43, 14, 11, ("#c8dcff", "#3a6ae0", "#1a3aa0", "#0a1a60"))
    _iso_cube(ic, 22, 30, 12, ("#fffbc0", "#e8d020", "#a89004", "#5a4a02"))


def preferences_other(ic):
    """Other settings: an application window with a disc in front, as KDE 3's package_applications."""
    from discover import _classic_window
    ic.add('<g transform="translate(0,-2) scale(.82)">')
    _classic_window(ic)
    ic.add("</g>")
    ic.shadow(circle(42, 42, 18), 2.4, 2)
    ic.path(circle(42, 42, 18), ic.lg([(0, "#ffffff"), (.3, "#e8d8ff"), (.55, "#c8f0e0"), (.8, "#f0e0c8"), (1, "#a8adb4")], 0, 0, 1, 1), INK, LW)
    ic.path(circle(42, 42, 6), ic.lg([(0, "#d9dce0"), (1, "#8a9098")]), INK, 1)
    ic.path(circle(42, 42, 2.4), "#ffffff", INK, .8)
    ic.add('<path d="M29,36A14,14 0 0 1 36,29" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round"/>')


def applications_other(ic):
    """Other applications: the open cardboard box."""
    from discover import _open_box
    ic.add('<g transform="translate(-6,4) scale(1.3)">')
    _open_box(ic)
    ic.add("</g>")


def link_emblem(ic):
    """Link: KDE Classic's link emblem - a small white tile with a curved arrow."""
    t = rrect(6, 6, 52, 52, 4)
    ic.shadow(t, 2.4, 2)
    ic.path(t, ic.lg([(0, "#ffffff"), (1, "#d9dce0")], 0, 0, 1, 1), INK, LW * 1.6)
    from actions import _curl_points
    pts = _curl_points(32, 40, 15, 4.4, 270, 120, 12, 9.5, taper=30, N=30)
    pts = [(64 - x, y) for x, y in pts]
    _teal(ic, _poly(pts), LW)


# ------------------------------------------------------------------ registry
SS = {
    "status": {"battery-full": battery_full, "battery-full-charging": battery_charging, "battery-low": battery_low,
               "battery-caution": battery_caution, "battery-ups": battery_ups, "audio-volume-muted": audio_volume_muted,
               "network-bluetooth-activated": network_bluetooth_activated, "network-connect": network_connect,
               "network-disconnect": network_disconnect, "notifications-disabled": notifications_disabled,
               "input-caps-on": input_caps_on, "input-keyboard-virtual-off": input_keyboard_virtual_off,
               "fingerprint": fingerprint, "process-working": process_working, "security-medium": security_medium},
    "actions": {"dialog-ok": dialog_ok, "go-top": go_top, "transform-move": transform_move, "object-rotate-left": rotate_left,
                "object-rotate-right": rotate_right, "object-flip-vertical": flip_vertical,
                "distribute-horizontal": distribute_horizontal, "resizecol": resize_column, "resizerow": resize_row,
                "document-export": document_export, "document-import": document_import,
                "document-print-preview": print_preview, "edit-comment": edit_comment, "edit-delete-shred": shred,
                "kt-restore-defaults": restore_defaults, "draw-path": draw_path, "color-picker": color_picker,
                "mark-location": mark_location, "media-playback-stop": media_stop, "window-minimize": window_minimize,
                "help-browser": help_browser},
    "apps": {"audio-speakers": audio_speakers, "system-help": system_help, "fingerprint-gui": fingerprint_gui,
             "font-enable": font_enable, "font-disable": font_disable, "tv": tv, "utilities-system-monitor": system_monitor,
             "preferences-desktop-launch-feedback": launch_feedback, "preferences-desktop-text-to-speech": text_to_speech,
             "partitionmanager": partition_manager, "preferences-other": preferences_other,
             "applications-other": applications_other, "plasmadiscover": discover_app},
    "emblems": {"emblem-symbolic-link": link_emblem},
}

# same meaning as an icon already in the set: link to it ("context/name")
SS_ALIASES = {
    "activities": "apps/preferences-desktop-activities", "virtual-desktops": "apps/preferences-desktop-virtual",
    "application-x-executable-script": "mimetypes/application-x-shellscript", "applications-all-symbolic": "apps/kmenu",
    "delete": "actions/edit-delete", "entry-delete": "actions/edit-delete",
    "arrow-down": "actions/go-down", "arrow-down-symbolic": "actions/go-down", "arrow-right": "actions/go-next",
    "arrow-up": "actions/go-up", "arrow-up-symbolic": "actions/go-up", "go-next-use": "actions/go-next",
    "go-previous-use": "actions/go-previous", "go-top-symbolic": "actions/go-top",
    "audio-input-microphone": "status/mic-on", "audio-input-microphone-symbolic": "status/mic-on",
    "audio-speakers-symbolic": "apps/audio-speakers", "audio-volume-muted-symbolic": "status/audio-volume-muted",
    "configure-toolbars": "actions/configure", "settings-configure": "actions/configure",
    "settings-configure-symbolic": "actions/configure", "tools": "actions/configure",
    "cups": "devices/printer", "printer-symbolic": "devices/printer", "printer-laser": "devices/printer",
    "document-print": "devices/printer", "document-print-symbolic": "devices/printer",
    "data-information": "apps/dialog-information", "documentinfo": "mimetypes/text-x-readme",
    "documentinfo-symbolic": "mimetypes/text-x-readme", "desktop": "places/user-desktop",
    "device-notifier": "devices/drive-removable-media-usb",
    "dialog-object-properties": "actions/document-properties", "document-edit": "actions/document-properties",
    "document-edit-symbolic": "actions/document-properties", "edit-entry": "actions/document-properties",
    "entry-edit": "actions/document-properties",
    "dialog-password": "apps/preferences-desktop-user-password", "kwalletmanager": "apps/preferences-desktop-user-password",
    "system-user-prompt": "apps/preferences-desktop-user-password",
    "dialog-ok-symbolic": "actions/dialog-ok", "dialog-ok-apply": "actions/dialog-ok", "dialog-ok-apply-symbolic": "actions/dialog-ok",
    "dialog-positive": "actions/dialog-ok", "task-complete": "actions/dialog-ok",
    "document-export-symbolic": "actions/document-export", "document-import-symbolic": "actions/document-import",
    "document-print-preview-symbolic": "actions/document-print-preview", "document-multiple": "actions/edit-copy",
    "draw-path-symbolic": "actions/draw-path", "tool_pen-symbolic": "actions/draw-path",
    "edit-clear": "actions/edit-clear-locationbar-ltr", "edit-clear-symbolic": "actions/edit-clear-locationbar-ltr",
    "favorites-symbolic": "actions/bookmarks", "feed-subscribe": "mimetypes/application-rss+xml",
    "folder-network-symbolic": "places/folder-network", "internet-services": "places/globe",
    "folder-print-symbolic": "places/folder-print", "games-config-background": "actions/view-preview",
    "preview": "actions/view-preview", "gtkconfig": "apps/preferences-desktop-theme-applications",
    "help-browser-symbolic": "actions/help-browser",
    "input-keyboard-symbolic": "devices/input-keyboard", "input-mouse-symbolic": "devices/input-mouse",
    "input-tablet": "apps/preferences-desktop-tablet", "input-tablet-symbolic": "apps/preferences-desktop-tablet",
    "input-touchpad": "apps/preferences-desktop-touchpad", "input-touchscreen": "apps/preferences-desktop-touchscreen",
    "input-gamepad": "apps/preferences-desktop-gaming", "input-keyboard-virtual-symbolic": "apps/input-keyboard-virtual",
    "kaccess": "apps/preferences-desktop-accessibility", "kwin": "apps/preferences-system-windows",
    "link": "emblems/emblem-symbolic-link", "media-playback-stop-symbolic": "actions/media-playback-stop",
    "monitor": "devices/video-display", "monitor-symbolic": "devices/video-display",
    "network-bluetooth-symbolic": "apps/preferences-system-bluetooth", "network-connect-symbolic": "status/network-connect",
    "network-disconnect-symbolic": "status/network-disconnect",
    "notifications": "apps/preferences-desktop-notification-bell", "notifications-symbolic": "apps/preferences-desktop-notification-bell",
        "preferences-desktop-navigation": "status/compass",
    "preferences-system-windows-effect-flipswitch": "apps/preferences-system-tabbox", "window": "apps/preferences-system-tabbox",
    "preferences-system-windows-effect-glide": "apps/preferences-desktop-effects",
    "preferences-system-windows-effect-minimize": "apps/preferences-desktop-effects",
    "system-search": "actions/edit-find", "tools-report-bug-symbolic": "apps/tools-report-bug",
    "transform-move-symbolic": "actions/transform-move", "user": "apps/preferences-desktop-user",
    "user-identity": "apps/preferences-desktop-user", "view-fullscreen": "actions/window-maximize",
    "xterm": "apps/utilities-terminal", "color-profile": "apps/preferences-desktop-color",
    "chronometer": "status/chronometer-start", "system-help-symbolic": "apps/system-help",
    "org.kde.discover": "apps/plasmadiscover", "plasmadiscover-symbolic": "apps/plasmadiscover", "org.kde.discover-symbolic": "apps/plasmadiscover",
    # Discover leftovers
    "applications-development-symbolic": "apps/applications-development", "arrow-left-symbolic": "actions/go-previous",
    "arrow-right-symbolic": "actions/go-next", "checkmark": "actions/dialog-ok", "device-notifier-symbolic": "devices/drive-removable-media-usb",
    "document-edit-sign-encrypt": "actions/document-properties", "document-revert": "actions/kt-restore-defaults",
    "document-revert-symbolic": "actions/kt-restore-defaults",
    "help-feedback": "mimetypes/text-x-readme", "internet-services-symbolic": "places/globe",
    "kdevelop": "apps/applications-development",
    "process-working-symbolic": "status/process-working", "run-build": "mimetypes/text-x-makefile",
    "run-build-symbolic": "mimetypes/text-x-makefile", "security-medium-symbolic": "status/security-medium",
    "security-high": "emblems/object-locked", "security-high-symbolic": "emblems/object-locked",
    "user-home-symbolic": "places/user-home", "view-process-system": "apps/system-run",
}


def write(out):
    n = 0
    for ctx, icons in SS.items():
        d = f"{out}/scalable/{ctx}"
        os.makedirs(d, exist_ok=True)
        for name, fn in icons.items():
            open(f"{d}/{name}.svg", "w").write(_ic(fn)().svg(64))
            n += 1
    missing = []
    for a, t in SS_ALIASES.items():
        ctx, name = t.split("/")
        d = f"{out}/scalable/{ctx}"
        if not os.path.exists(f"{d}/{name}.svg"):
            missing.append(t)
            continue
        if not any(os.path.lexists(f"{out}/scalable/{c}/{a}.svg") for c in os.listdir(f"{out}/scalable")):
            os.symlink(f"{name}.svg", f"{d}/{a}.svg")
    if missing:
        print("settingstrace: alias targets missing:", missing)
    return n
