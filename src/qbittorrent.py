"""KDE Classic Vector: qBittorrent's own icon names (2026-10-27).

qBittorrent asks the icon theme for these when "Use icons from system theme" is on. None of them are in Breeze,
so without this module it fell back to its own flat icons. Also three KDE names it borrows: kt-magnet (KTorrent's
magnet), view-statistics and document-edit-verify.

Safety rule: this module only ADDS names. If a name already exists in the theme it is left alone and reported, so
nothing else in KDE Modern Classic can change. qBittorrent's logos (qbittorrent, qbittorrent-tray,
qbittorrent-tray-mono) are deliberately not drawn: third-party logos stay the app's own.
Runs after apps2.py (it embeds icons that are already built).
"""
import math, os
from gen import Icon, INK, LW, circle, rrect
from actions import _mpath, GREEN
from settingstrace import _badge, _ok, _no
from settings import _person
import pim
from pim import _embed

BLUE = ("#d0e6ff", "#5a9ae8", "#2a64c8", "#0c2a6a")
RED = ("#ffc8b8", "#ec5a3a", "#c01e0e", "#5a0804")
PALE_GREEN = ("#eef8e8", "#a8d898", "#6aa85a", "#3a5a32")
PALE_BLUE = ("#eef4fc", "#a8c4e8", "#6a8ec0", "#34465e")


def _ic(fn):
    def f():
        ic = Icon()
        fn(ic)
        return ic
    return f


def _grad(ic, col):
    return ic.lg([(0, col[0]), (.35, col[1]), (.7, col[2]), (1, col[3])], 0, 0, .35, 1)


# ------------------------------------------------------------------ transfer direction: double chevrons
def _chevrons(ic, up, col):
    """Two stacked chevrons pointing down (or up), like the theme's arrow-down-double but in a status colour."""
    ic.add(f'<g transform="rotate({180 if up else 0} 32 32)">')
    for y in (6, 28):
        d = f"M6,{y}H19L32,{y + 13}L45,{y}H58L32,{y + 26}Z"
        ic.shadow(d, 2, 1.7)
        _mpath(ic, d, _grad(ic, col), LW * 1.2)
    ic.add("</g>")


def _pause_badge(ic, x=49, y=49, r=11):
    """The theme's amber pause emblem as a badge: stalled (no data moving)."""
    k = 2 * r / 64 * 1.18
    _embed(ic, "emblem-pause", f"translate({x - 32 * k:.2f},{y - 32 * k:.2f}) scale({k:.3f})")


def downloading(ic): _chevrons(ic, False, GREEN)
def upload(ic): _chevrons(ic, True, BLUE)


def stalled_dl(ic):
    _chevrons(ic, False, PALE_GREEN)
    _pause_badge(ic)


def stalled_up(ic):
    _chevrons(ic, True, PALE_BLUE)
    _pause_badge(ic)


# ------------------------------------------------------------------ status filters: a down and an up arrow side by side
def _pair(ic, down, up):
    for x0, y0, x1, y1, col in ((20, 6, 20, 58, down), (44, 58, 44, 6, up)):
        dy = 1 if y1 > y0 else -1
        d = (f"M{x0 - 5},{y0}H{x0 + 5}V{y1 - dy * 16}H{x0 + 13}L{x0},{y1}L{x0 - 13},{y1 - dy * 16}H{x0 - 5}Z")
        ic.shadow(d, 2, 1.7)
        _mpath(ic, d, _grad(ic, col), LW * 1.1)


def filter_active(ic): _pair(ic, GREEN, BLUE)
def filter_inactive(ic): _pair(ic, RED, RED)


def filter_stalled(ic):
    _pair(ic, PALE_GREEN, PALE_BLUE)
    _pause_badge(ic, 32, 50, 10)


# ------------------------------------------------------------------ peers
def peers(ic):
    """Peers: two people, one behind the other."""
    _person(ic, 40, 8, 1.15, ("#ffd28a", "#c8781a"))
    _person(ic, 24, 20, 1.2)


def peers_add(ic):
    peers(ic)
    _badge(ic, 50, 50, 10, "green", "M45,50H55M50,45V55")


def peers_remove(ic):
    peers(ic)
    _badge(ic, 50, 50, 10, "red", "M45,50H55")


# ------------------------------------------------------------------ connection status (status bar)
def connected(ic):
    _embed(ic, "globe", "translate(0,0) scale(.92)")
    _ok(ic, 49, 49, 11)


def disconnected(ic):
    _embed(ic, "globe", "translate(0,0) scale(.92)")
    _no(ic, 49, 49, 11)


# ------------------------------------------------------------------ alternative speed limits (status bar toggle)
def _dial(ic, deg):
    """The theme's speedometer (shell.speedometer) with the needle at `deg`."""
    cx, cy, r = 32, 40, 27
    ic.shadow(f"M{cx - r},{cy}A{r},{r} 0 0 1 {cx + r},{cy}V{cy + 10}H{cx - r}Z", 2.6, 2.2)
    ic.path(f"M{cx - r},{cy + 8}V{cy}A{r},{r} 0 0 1 {cx + r},{cy}V{cy + 8}Q{cx + r},{cy + 12} {cx + r - 4},{cy + 12}H{cx - r + 4}Q{cx - r},{cy + 12} {cx - r},{cy + 8}Z",
            ic.lg([(0, "#5c6168"), (1, "#14171c")]), INK, LW)
    for a0, a1, col in ((180, 240, "#3fae2a"), (240, 300, "#e8c43a"), (300, 360, "#e0281a")):
        p0 = (cx + (r - 6) * math.cos(math.radians(a0)), cy + (r - 6) * math.sin(math.radians(a0)))
        p1 = (cx + (r - 6) * math.cos(math.radians(a1)), cy + (r - 6) * math.sin(math.radians(a1)))
        ic.add(f'<path d="M{p0[0]:.2f},{p0[1]:.2f}A{r - 6},{r - 6} 0 0 1 {p1[0]:.2f},{p1[1]:.2f}" fill="none" stroke="{col}" stroke-width="5"/>')
    a = math.radians(deg)
    ic.add(f'<path d="M{cx},{cy}L{cx + 19 * math.cos(a):.2f},{cy + 19 * math.sin(a):.2f}" stroke="#fff" stroke-width="2.6" stroke-linecap="round"/>')
    ic.path(circle(cx, cy, 3.4), ic.rg([(0, "#ffffff"), (1, "#8a9098")]), INK, 1)


def slow(ic):
    """Alternative speed limits on: the needle held down in the green (slow_off is the normal speedometer)."""
    _dial(ic, 205)


# ------------------------------------------------------------------ queue, location, verify, magnet
def queued(ic):
    """Queued: a wall clock with an amber rim (waiting its turn)."""
    ic.shadow(circle(32, 32, 26), 2.6, 2.2)
    ic.path(circle(32, 32, 26), ic.rg([(0, "#ffe8a0"), (.6, "#ec9a1a"), (1, "#7a4404")], .4, .32, .8), INK, LW)
    ic.path(circle(32, 32, 20), ic.rg([(0, "#ffffff"), (1, "#dfe2e6")], .4, .3, .8), INK, 1)
    for k in range(12):
        a = 2 * math.pi * k / 12
        r0 = 15.5 if k % 3 else 13.5
        ic.add(f'<path d="M{32 + r0 * math.cos(a):.2f},{32 + r0 * math.sin(a):.2f}L{32 + 18 * math.cos(a):.2f},{32 + 18 * math.sin(a):.2f}" stroke="{INK}" stroke-width="{1.6 if k % 3 == 0 else 1}"/>')
    ic.add(f'<path d="M32,32V18M32,32L42,37" fill="none" stroke="{INK}" stroke-width="2.6" stroke-linecap="round"/>')
    ic.path(circle(32, 32, 2), "#c01e0e", INK, .8)


def set_location(ic):
    """Set location: a folder with a teal arrow going into it (move the download somewhere else)."""
    _embed(ic, "inode-directory", "translate(10,12) scale(.82)")
    _embed(ic, "go-jump-locationbar", "translate(0,0) scale(.55)")


def verify(ic):
    """document-edit-verify (qBittorrent: Force recheck): a page with a green tick badge."""
    _embed(ic, "text-plain", "translate(-4,0)")
    _ok(ic, 47, 47, 12)


def magnet(ic):
    """kt-magnet (magnet links): a red horseshoe magnet with silver poles."""
    outer, inner = 24, 11
    cx, cy = 32, 30
    arc = (f"M{cx - outer},{cy}A{outer},{outer} 0 0 1 {cx + outer},{cy}V48H{cx + inner}V{cy}"
           f"A{inner},{inner} 0 0 0 {cx - inner},{cy}V48H{cx - outer}Z")
    ic.shadow(arc + f"M{cx - outer},48H{cx - inner}V60H{cx - outer}ZM{cx + inner},48H{cx + outer}V60H{cx + inner}Z", 2.6, 2.2)
    ic.path(arc, ic.lg([(0, "#ffb0a0"), (.45, "#e0281a"), (1, "#7a0804")], 0, 0, 1, .3), INK, LW)
    for x in (cx - outer, cx + inner):
        ic.path(f"M{x},48H{x + outer - inner}V60H{x}Z", ic.lg([(0, "#ffffff"), (.5, "#c3c7cd"), (1, "#6c727a")], 0, 0, 1, 0), INK, LW)
    ic.add(f'<path d="M{cx - outer + 3},{cy - 2}A{outer - 3},{outer - 3} 0 0 1 {cx - 4},{cy - outer + 3.4}" fill="none" '
           f'stroke="#fff" stroke-opacity=".6" stroke-width="2.4" stroke-linecap="round"/>')


QB = {
    "status": {"downloading": downloading, "upload": upload, "stalledDL": stalled_dl, "stalledUP": stalled_up,
               "connected": connected, "disconnected": disconnected, "slow": slow, "queued": queued},
    "actions": {"filter-active": filter_active, "filter-inactive": filter_inactive, "filter-stalled": filter_stalled,
                "peers": peers, "peers-add": peers_add, "peers-remove": peers_remove, "set-location": set_location,
                "document-edit-verify": verify, "kt-magnet": magnet},
}
# Names that mean the same as an icon the theme already has: linked, not redrawn.
QB_ALIASES = {
    "application-rss": "application-rss+xml", "application-url": "globe", "browser-cookies": "preferences-web-browser-cookies",
    "chart-line": "office-chart-line", "view-statistics": "office-chart-pie", "checked-completed": "task-complete",
    "directory": "inode-directory", "view-categories": "view-list-tree", "filter-all": "media-playlist-shuffle",
    "firewalled": "preferences-security-firewall", "loading": "process-working", "mail-inbox": "mail-unread",
    "rss_read_article": "mail-read", "rss_unread_article": "mail-unread", "task-reject": "dialog-error",
    "slow_off": "speedometer", "force-recheck": "document-edit-verify", "reannounce": "view-refresh",
    "torrent-magnet": "kt-magnet",
    # toolbar: start/stop as the round green play and amber pause badges (qBittorrent-only names; the shared
    # media-playback-* icons other apps use are unchanged)
    "torrent-start": "media-playback-playing", "torrent-start-forced": "media-playback-playing",
    "torrent-stop": "emblem-pause", "pause-session": "emblem-pause", "stopped": "emblem-pause",
}


def _find(out, name):
    for ctx in os.listdir(f"{out}/scalable"):
        if os.path.lexists(f"{out}/scalable/{ctx}/{name}.svg"):
            return ctx
    return None


def write(out):
    pim.OUT = out
    n, skipped = 0, []
    for ctx, icons in QB.items():
        for name, fn in icons.items():
            if _find(out, name):
                skipped.append(name)
                continue
            open(f"{out}/scalable/{ctx}/{name}.svg", "w").write(_ic(fn)().svg(64))
            n += 1
    for a, t in QB_ALIASES.items():
        if _find(out, a):
            skipped.append(a)
            continue
        ctx = _find(out, t)
        if ctx is None:
            skipped.append(f"{a} (target {t} missing)")
            continue
        os.symlink(f"{t}.svg", f"{out}/scalable/{ctx}/{a}.svg")
        n += 1
    if skipped:
        print("qbittorrent: left alone (already in the theme):", skipped)
    return n
