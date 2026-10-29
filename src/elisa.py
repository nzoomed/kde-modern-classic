"""KDE Classic Vector: Elisa, the music player - its app icon, its library views (artists, tracks, genres,
lyrics, playlists) and the queue actions. Runs after kate, so aliases can point anywhere.
"""
import math, os
from gen import Icon, INK, LW, circle, rrect
from settingstrace import _teal, _arrow_pts, _badge, _poly


def _ic(fn):
    def f():
        ic = Icon()
        fn(ic)
        return ic
    return f


NOTE = [(0, "#6c727a"), (.5, "#202428"), (1, "#000000")]


def _note(ic, x, y, s=1.0):
    """A single eighth note: head at (x, y), stem up, flag to the right."""
    ic.add(f'<g transform="translate({x},{y}) scale({s})">')
    head = "M-9,0C-9,-5 -2,-8 3,-7C8,-6 9,-2 7,2C5,6 -3,8 -7,5C-8.5,4 -9,2 -9,0Z"
    stem = "M4.5,-5V-40H9V-5Z"
    flag = "M9,-40Q11,-30 20,-24Q26,-19 22,-8Q22,-16 16,-20Q12,-23 9,-25Z"
    for d in (stem, flag, head):
        ic.path(d, ic.lg(NOTE, 0, 0, 1, 1), INK, 1 / s)
    ic.add('<path d="M-6,-1Q-4,-5 1,-5" fill="none" stroke="#fff" stroke-opacity=".6" stroke-width="1.6" stroke-linecap="round"/>')
    ic.add("</g>")


def _beamed(ic, x, y, s=1.0):
    """Two beamed eighth notes, left head at (x, y)."""
    ic.add(f'<g transform="translate({x},{y}) scale({s})">')
    for dx, dy in ((0, 0), (24, -6)):
        head = f"M{dx - 9},{dy}C{dx - 9},{dy - 5} {dx - 2},{dy - 8} {dx + 3},{dy - 7}C{dx + 8},{dy - 6} {dx + 9},{dy - 2} {dx + 7},{dy + 2}C{dx + 5},{dy + 6} {dx - 3},{dy + 8} {dx - 7},{dy + 5}Z"
        stem = f"M{dx + 4.5},{dy - 5}V{dy - 38}H{dx + 9}V{dy - 5}Z"
        ic.path(stem, ic.lg(NOTE, 0, 0, 1, 1), INK, 1 / s)
        ic.path(head, ic.lg(NOTE, 0, 0, 1, 1), INK, 1 / s)
        ic.add(f'<path d="M{dx - 6},{dy - 1}Q{dx - 4},{dy - 5} {dx + 1},{dy - 5}" fill="none" stroke="#fff" stroke-opacity=".6" stroke-width="1.6" stroke-linecap="round"/>')
    ic.path("M4.5,-38L33,-44V-36L4.5,-30Z", ic.lg(NOTE, 0, 0, 1, 1), INK, 1 / s)
    ic.add("</g>")


# ------------------------------------------------------------------ app icon
def elisa(ic):
    """Elisa: a silver audio CD with a pair of black beamed notes in front of it."""
    c = circle(40, 24, 22)
    ic.shadow(c, 2.4, 2)
    ic.path(c, ic.rg([(0, "#ffffff"), (.45, "#dfe2e6"), (.75, "#b8c8e0"), (.9, "#f0d8f0"), (1, "#a8adb4")], .45, .45, .7), INK, LW)
    ic.add('<path d="M24,10A20,20 0 0,1 44,4" fill="none" stroke="#9ad0f0" stroke-width="3" stroke-opacity=".7"/>'
           '<path d="M58,32A20,20 0 0,1 46,43" fill="none" stroke="#f0b0e0" stroke-width="3" stroke-opacity=".7"/>')
    ic.path(circle(40, 24, 7), ic.lg([(0, "#ffffff"), (1, "#a8adb4")], 0, 0, 1, 1), INK, 1)
    ic.path(circle(40, 24, 2.6), "#eff0f1", INK, 1)
    _beamed(ic, 11, 57, .9)


# ------------------------------------------------------------------ library views
def _vinyl(ic, cx, cy, r):
    c = circle(cx, cy, r)
    ic.shadow(c, 2.4, 2)
    ic.path(c, ic.rg([(0, "#3c4148"), (.6, "#1a1c20"), (1, "#050607")], .45, .4, .7), INK, LW)
    for k in (.86, .74, .62):
        ic.add(f'<path d="{circle(cx, cy, r * k)}" fill="none" stroke="#5c6168" stroke-width=".8"/>')
    ic.add(f'<path d="M{cx - r * .7:.1f},{cy - r * .35:.1f}A{r * .78:.1f},{r * .78:.1f} 0 0,1 {cx - r * .1:.1f},{cy - r * .77:.1f}" '
           'fill="none" stroke="#ffffff" stroke-opacity=".45" stroke-width="2.4" stroke-linecap="round"/>')
    ic.path(circle(cx, cy, r * .34), ic.rg([(0, "#ffb0a0"), (.5, "#e0281a"), (1, "#7a0804")], .4, .35, .8), INK, 1)
    ic.path(circle(cx, cy, r * .07), "#eff0f1", INK, .8)


def view_media_track(ic):
    """Track: a page (the track's details) with a black record over its lower right corner."""
    from okular import _pg
    _pg(ic, 4, 2, 40, 54)
    _vinyl(ic, 42, 42, 19)


def view_media_track_cd(ic):
    """Alternative: the same page with a silver CD instead of the record."""
    from okular import _pg
    _pg(ic, 4, 2, 40, 54)
    c = circle(42, 42, 19)
    ic.shadow(c, 2.4, 2)
    ic.path(c, ic.rg([(0, "#ffffff"), (.45, "#dfe2e6"), (.75, "#b8c8e0"), (.9, "#f0d8f0"), (1, "#a8adb4")], .45, .45, .7), INK, LW)
    ic.add('<path d="M28,34A16,16 0 0,1 42,25" fill="none" stroke="#9ad0f0" stroke-width="2.6" stroke-opacity=".7"/>'
           '<path d="M57,48A16,16 0 0,1 48,58" fill="none" stroke="#f0b0e0" stroke-width="2.6" stroke-opacity=".7"/>')
    ic.path(circle(42, 42, 6), ic.lg([(0, "#ffffff"), (1, "#a8adb4")], 0, 0, 1, 1), INK, 1)
    ic.path(circle(42, 42, 2.2), "#eff0f1", INK, 1)


def view_media_track_page(ic):
    """Alternative kept for comparison: a note on a page with a sound wave."""
    from okular import _pg
    _pg(ic, 6, 2, 44, 60, lines=False)
    w = "M10,20" + "".join(f"L{12 + k * 2},{20 + (6 if k % 2 else -6) * (1 - abs(k - 8) / 9)}" for k in range(17))
    ic.add(f'<path d="{w}" fill="none" stroke="#2a6ac8" stroke-width="1.8" stroke-linejoin="round"/>')
    _note(ic, 30, 56, 1.0)


def view_media_artist(ic):
    """Artist: a chrome stage microphone on its stand."""
    ic.add(f'<path d="M32,40V58M20,60H44" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
           '<path d="M32,40V58M20,60H44" fill="none" stroke="#8a9098" stroke-width="2.6" stroke-linecap="round"/>')
    ic.add(f'<path d="M18,22Q18,40 32,40Q46,40 46,22" fill="none" stroke="{INK}" stroke-width="4.4"/>'
           '<path d="M18,22Q18,40 32,40Q46,40 46,22" fill="none" stroke="#b4b9c0" stroke-width="2.2"/>')
    body = "M22,8Q22,2 32,2Q42,2 42,8V24Q42,32 32,32Q22,32 22,24Z"
    ic.shadow(body, 2.2, 1.8)
    ic.path(body, ic.lg([(0, "#5c6168"), (.3, "#ffffff"), (.6, "#a8adb4"), (1, "#3c4148")], 0, 0, 1, 0), INK, LW)
    for y in range(6, 22, 4):
        ic.add(f'<path d="M24,{y}H40" stroke="#3c4148" stroke-width="1.2" stroke-opacity=".7"/>')
    ic.path("M22,21H42V25H22Z", ic.lg([(0, "#ff8a7a"), (1, "#a8180a")], 0, 0, 0, 1), INK, 1)


def view_media_lyrics(ic):
    """Lyrics: a page of words with a note beside them."""
    from okular import _pg
    _pg(ic, 4, 4, 40, 56)
    _note(ic, 48, 56, .9)


def _rows(ic, n=5, x=4, w=40):
    for k in range(n):
        ic.path(rrect(x, 6 + k * 10, w, 7, 1.5), ic.lg([(0, "#ffffff"), (1, "#c3c7cd")], 0, 0, 0, 1), INK, 1.1)


def view_media_playlist(ic):
    """Playlist: a list of rows with a note over its corner."""
    _rows(ic)
    _note(ic, 47, 58, .9)


def playlist_append_next(ic):
    """Play next: a teal arrow slotting a new row in just under the one playing."""
    for k in range(5):
        hi = k == 1
        ic.path(rrect(22, 6 + k * 11, 38, 8, 1.5),
                ic.lg([(0, "#ffffff"), (1, "#bfe6f4" if hi else "#c3c7cd")], 0, 0, 0, 1), INK, 1.4 if hi else 1.1)
    ic.path("M26,7L31.5,10L26,13Z", "#3fae2a", INK, .8)
    _teal(ic, _poly(_arrow_pts(2, 21, 21, 21, 4, 9, 10)))


def radio(ic):
    """Radio: a classic transistor set - speaker grille on the left, tuning dial on the right, aerial up."""
    ic.add(f'<path d="M46,20L58,2" stroke="{INK}" stroke-width="3.4" stroke-linecap="round"/>'
           '<path d="M46,20L58,2" stroke="#c3c7cd" stroke-width="1.6" stroke-linecap="round"/>')
    body = rrect(3, 18, 58, 40, 6)
    ic.shadow(body, 2.6, 2.2)
    ic.path(body, ic.lg([(0, "#ffb0a0"), (.45, "#d8573d"), (1, "#7a1a0a")], 0, 0, 1, 1), INK, LW)
    grille = circle(20, 38, 12)
    ic.path(grille, ic.rg([(0, "#8a9098"), (1, "#2c3036")], .5, .5, .6), INK, 1.2)
    for k in range(-2, 3):
        ic.add(f'<path d="M{20 + k * 4.4},{29 + abs(k) * 1.4}V{47 - abs(k) * 1.4}" stroke="#d9dce0" stroke-width="1.4"/>')
    ic.path(rrect(37, 26, 20, 12, 2), ic.lg([(0, "#fff6c0"), (1, "#e8c43a")], 0, 0, 0, 1), INK, 1.2)
    for k in range(5):
        ic.add(f'<path d="M{40 + k * 3.6},28V{31 if k % 2 else 33}" stroke="{INK}" stroke-width=".9"/>')
    ic.add('<path d="M46,27V37" stroke="#e0281a" stroke-width="1.6"/>')
    for x in (42, 52):
        ic.path(circle(x, 47, 4.4), ic.rg([(0, "#ffffff"), (1, "#7b818a")], .4, .35, .8), INK, 1.1)


def no_shuffle(ic):
    """Play in order (no shuffle): two straight teal arrows running side by side - the shuffle arrows untangled."""
    for y in (20, 44):
        _teal(ic, _poly([(4, y - 4), (46, y - 4), (46, y - 12), (60, y), (46, y + 12), (46, y + 4), (4, y + 4)]))


def repeat_none(ic):
    """Repeat off: the repeat loop in grey, struck through in red."""
    from actions import _curl_points, _mpath
    pts = _curl_points(32, 32, 19, 4.4, 300, 300, 13, 10, taper=40, N=60)
    d = _poly(pts)
    ic.shadow(d, 2, 1.7)
    _mpath(ic, d, ic.lg([(0, "#f2f2f2"), (.4, "#b4b9c0"), (1, "#5c6168")], 0, 0, .35, 1), LW * 1.2)
    ic.add(f'<path d="M10,54L54,10" stroke="{INK}" stroke-width="7.4" stroke-linecap="round"/>'
           '<path d="M10,54L54,10" stroke="#e0281a" stroke-width="4.6" stroke-linecap="round"/>')


EL = {
    "apps": {"elisa": elisa},
    "actions": {"view-media-track": view_media_track, "view-media-artist": view_media_artist,
                "view-media-lyrics": view_media_lyrics, "view-media-playlist": view_media_playlist,
                "media-playlist-append-next": playlist_append_next, "media-playlist-no-shuffle": no_shuffle,
                "media-repeat-none": repeat_none},
    "devices": {"radio": radio},
}

EL_ALIASES = {
    "org.kde.elisa": "apps/elisa", "elisa-symbolic": "apps/elisa", "media-playlist-append-next-symbolic": "actions/media-playlist-append-next",
    "view-media-album-cover": "media-album-cover", "view-media-favorite": "starred", "view-media-genre": "tag",
    "media-playlist-play": "media-playback-start", "view-media-playcount": "office-chart-bar", "audio-radio": "devices/radio",
    "radio-symbolic": "devices/radio", "media-playlist-normal": "actions/media-playlist-no-shuffle",
    "media-playlist-no-shuffle-symbolic": "actions/media-playlist-no-shuffle", "media-playlist-normal-symbolic": "actions/media-playlist-no-shuffle",
    "media-playlist-consecutive": "actions/media-playlist-no-shuffle", "media-playlist-consecutive-symbolic": "actions/media-playlist-no-shuffle",
    "media-repeat-none-symbolic": "actions/media-repeat-none", "media-repeat-all": "media-playlist-repeat",
    "media-repeat-all-symbolic": "media-playlist-repeat", "repeat": "media-playlist-repeat", "repeat-symbolic": "media-playlist-repeat",
    "media-random-albums-amarok": "media-playlist-shuffle", "media-random-tracks-amarok": "media-playlist-shuffle",
    "media-repeat-track-amarok": "media-playlist-repeat-song", "media-repeat-playlist-amarok": "media-playlist-repeat",
    "media-repeat-album-amarok": "media-playlist-repeat", "shuffle": "media-playlist-shuffle", "shuffle-symbolic": "media-playlist-shuffle",
}
for _n in ("view-media-track", "view-media-artist", "view-media-lyrics", "view-media-playlist"):
    EL_ALIASES[_n + "-symbolic"] = "actions/" + _n


def _find(out, name):
    for ctx in os.listdir(f"{out}/scalable"):
        if os.path.lexists(f"{out}/scalable/{ctx}/{name}.svg"):
            return ctx
    return None


def write(out):
    n = 0
    for ctx, icons in EL.items():
        d = f"{out}/scalable/{ctx}"
        for name, fn in icons.items():
            p = f"{d}/{name}.svg"
            if os.path.lexists(p):
                os.remove(p)
            open(p, "w").write(_ic(fn)().svg(64))
            n += 1
    missing = []
    for a, t in EL_ALIASES.items():
        ctx, name = t.split("/") if "/" in t else (_find(out, t), t)
        if ctx is None or not os.path.exists(f"{out}/scalable/{ctx}/{name}.svg"):
            missing.append(t)
            continue
        if _find(out, a) is None:
            os.symlink(f"{name}.svg", f"{out}/scalable/{ctx}/{a}.svg")
    if missing:
        print("elisa: alias targets missing:", missing)
    return n
