"""KDE Classic Vector: the odds and ends left by the app sweep - KWallet's wallets, KSystemLog, Konsole's
scrolling page, Discover's git folder, KDE Connect's reply, and aliases for the rest. Runs after elisa.
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


LEATHER = [(0, "#e8b080"), (.45, "#a8622a"), (1, "#4a2408")]


def wallet_closed(ic):
    """KWallet (closed): a brown leather wallet, folded shut, with its stitched edge and a brass stud."""
    body = "M4,18Q4,12 10,12H54Q60,12 60,18V52Q60,58 54,58H10Q4,58 4,52Z"
    ic.shadow(body, 2.6, 2.2)
    ic.path(body, ic.lg(LEATHER, 0, 0, 1, 1), INK, LW)
    ic.add('<path d="M8,18Q8,16 10,16H54Q56,16 56,18V52Q56,54 54,54H10Q8,54 8,52Z" fill="none" stroke="#ffe0c0" '
           'stroke-opacity=".55" stroke-width="1" stroke-dasharray="2.4 1.6"/>')
    flap = "M30,28Q30,24 34,24H60V44H34Q30,44 30,40Z"
    ic.path(flap, ic.lg([(0, "#d89a60"), (.5, "#8a4a1a"), (1, "#4a2408")], 0, 0, 1, 1), INK, LW)
    ic.path(circle(40, 34, 4), ic.rg([(0, "#fff6c0"), (.5, "#e8c43a"), (1, "#7a5a08")], .4, .35, .8), INK, 1)


def wallet_open(ic):
    """KWallet (open): the wallet opened out, a card and a gold key showing in its pockets."""
    body = "M4,24Q4,18 10,18H54Q60,18 60,24V54Q60,60 54,60H10Q4,60 4,54Z"
    card = "M12,6H44Q46,6 46,8V30H10V8Q10,6 12,6Z"
    ic.shadow(card, 2, 1.7)
    ic.path(card, ic.lg([(0, "#c4ecff"), (.5, "#3d9ad8"), (1, "#1a5c9e")], 0, 0, 1, 1), INK, 1.2)
    ic.path("M10,12H46V16H10Z", "#14171c", None)
    ic.shadow(body, 2.6, 2.2)
    ic.path(body, ic.lg(LEATHER, 0, 0, 1, 1), INK, LW)
    ic.add('<path d="M32,20V58" stroke="#3a1a04" stroke-width="1.6"/>'
           '<path d="M8,30H28M36,30H56" stroke="#ffe0c0" stroke-opacity=".5" stroke-width="1" stroke-dasharray="2.4 1.6"/>')
    # a gold key in the right pocket
    ic.path(circle(44, 42, 6), ic.rg([(0, "#fff6c0"), (.5, "#e8c43a"), (1, "#7a5a08")], .4, .35, .8), INK, 1.2)
    ic.path(circle(44, 42, 2), "#5a3a10", None)
    ic.path("M44,48V58H47V55H50V52H47V48Z", ic.lg([(0, "#fff6c0"), (1, "#a8840e")], 0, 0, 1, 0), INK, 1)


def log_viewer(ic):
    """Log viewer: a long printed log - timestamped lines, one flagged red - under the magnifier."""
    from okular import _pg
    from actions import _magnifier
    _pg(ic, 4, 2, 42, 58, lines=False)
    for k in range(9):
        y = 16 + k * 4.6
        ic.add(f'<path d="M8,{y}H14" stroke="#2a6ac8" stroke-width="1.6"/>'
               f'<path d="M16,{y}H{40 - (k % 3) * 5}" stroke="{"#e0281a" if k == 4 else "#3c4148"}" stroke-width="{2.2 if k == 4 else 1.3}" stroke-dasharray="2.4 1"/>')
    _magnifier(ic, 44, 42, 10, 8)


def preferences_scroll(ic):
    """Scrolling: a window of text with a scroll bar and its thumb."""
    w = rrect(4, 6, 56, 52, 3)
    ic.shadow(w, 2.4, 2)
    ic.path(w, ic.lg([(0, "#ffffff"), (1, "#dfe2e6")], 0, 0, 1, 1), INK, LW)
    for k in range(8):
        ic.add(f'<path d="M9,{14 + k * 5.4}H{40 - (k % 3) * 5}" stroke="#3c4148" stroke-width="1.4" stroke-dasharray="2.6 1"/>')
    ic.path("M46,6H60V58H46Z", ic.lg([(0, "#c3c7cd"), (1, "#eef0f2")], 0, 0, 1, 0), INK, 1.2)
    ic.path(rrect(48, 20, 10, 18, 2), ic.lg([(0, "#c4ecff"), (.5, "#3d9ad8"), (1, "#1a5c9e")], 0, 0, 1, 0), INK, 1.1)
    for y, d in ((9, "M53,9L57,14H49Z"), (55, "M53,55L57,50H49Z")):
        ic.path(d, "#3c4148", None)


def folder_git(ic):
    """Git folder: the blue folder with Kate's branch symbol on it."""
    from gen import folder
    from kate import _rail, _node
    folder(ic, "blue")
    tile = rrect(2, 30, 30, 30, 4)
    ic.shadow(tile, 2, 1.7)
    ic.path(tile, ic.lg([(0, "#ffffff"), (1, "#d9dce0")], 0, 0, 1, 1), INK, LW)
    ic.add('<g transform="translate(5,32) scale(.42)">')
    _rail(ic, "M16,4V60")
    _rail(ic, "M16,40Q18,20 44,18")
    _node(ic, 16, 52, 7)
    _node(ic, 16, 30, 7)
    _node(ic, 44, 18, 7, ("#ffffff", "#4fae5a", "#22703a"))
    ic.add("</g>")


def mail_reply_sender(ic):
    """Reply: the envelope with a teal arrow curling back to the left."""
    from desktoptrace import _envelope
    from actions import _curl_points
    _envelope(ic, 12, 22, 48, 34)
    pts = _curl_points(30, 22, 15, 4.4, 270, 160, 12, 9.5, taper=30, N=30)
    _teal(ic, _poly(pts))


def chevrons_left(ic):
    from systray import _chevrons
    _chevrons(ic, "M28,13L12,32L28,51M54,13L38,32L54,51")


def chevrons_right(ic):
    from systray import _chevrons
    _chevrons(ic, "M10,13L26,32L10,51M36,13L52,32L36,51")


OD = {
    "status": {"wallet-closed": wallet_closed, "wallet-open": wallet_open},
    "apps": {"utilities-log-viewer": log_viewer},
    "actions": {"preferences-scroll": preferences_scroll, "mail-reply-sender": mail_reply_sender,
                "arrow-left-symbolic": chevrons_left, "arrow-right-symbolic": chevrons_right},
    "places": {"folder-git": folder_git},
}

OD_ALIASES = {
    "kwalletmanager": "status/wallet-closed", "org.kde.kwalletmanager": "status/wallet-closed", "kwalletmanager2": "status/wallet-closed",
    "wallet-closed-symbolic": "status/wallet-closed", "wallet-open-symbolic": "status/wallet-open",
    "org.kde.ksystemlog": "apps/utilities-log-viewer", "ksystemlog": "apps/utilities-log-viewer",
    "folder-git-symbolic": "places/folder-git", "translate": "set-language", "translate-symbolic": "set-language",
    "help-contextual-symbolic": "help-contextual", "question-symbolic": "question",
    "go-jump-locationbar": "go-jump", "ksnapshot": "spectacle", "player-volume": "audio-volume-high",
    "favorites": "starred", "irc-voice": "im-user", "tools-media-optical-burn": "media-write-cd",
    "tools-media-optical-copy": "media-write-cd", "tools-media-optical-burn-image": "media-write-cd",
    "kcmdf": "drive-multidisk", "kdf": "drive-multidisk", "org.kde.kdf": "drive-multidisk",
    "kwikdisk": "drive-multidisk", "org.kde.kwikdisk": "drive-multidisk",
    "mail-reply-sender-symbolic": "actions/mail-reply-sender", "mail-reply": "actions/mail-reply-sender",
}


# Names that already point somewhere but should point elsewhere. The system tray's show/hide-hidden-icons
# button asks for arrow-<dir>-symbolic; the double chevrons suit it better than the plain go-up arrow.
# (Also used by the keyboard layouts page's move up/down buttons and Discover's carousel - chevrons work there too.)
# The slim expand/collapse chevrons from the tray are used (up = collapse, down = expand); left and right are
# the same drawing turned, below.
OD_OVERRIDE = {"arrow-up-symbolic": "status/collapse", "arrow-down-symbolic": "status/expand"}


# Small sizes (16 and 22 px): Home and Downloads show just their emblem, filling the icon, as KDE 3's
# home did at 16 px. Documents, Music, Pictures and Videos keep the folder so they can't be mistaken for files
# (they also appear in Dolphin's Details view at these sizes).
SMALL_EMBLEM_ONLY = {"user-home": ("home", (2.25, 28.25, 32.25, 59.0)),
                     "folder-download": ("download", (4.25, 27.25, 33.0, 55.75))}


def _emblem_only(emblem, box, pad=1.5):
    from gen import EMBLEM
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    s = min((64 - 2 * pad) / w, (64 - 2 * pad) / h)
    tx, ty = (64 - w * s) / 2 - x0 * s, (64 - h * s) / 2 - y0 * s
    ic = Icon()
    ic.add(f'<g transform="translate({tx:.2f},{ty:.2f}) scale({s:.3f})">')
    EMBLEM[emblem](ic)
    ic.add("</g>")
    return ic


def _find(out, name):
    for ctx in os.listdir(f"{out}/scalable"):
        if os.path.lexists(f"{out}/scalable/{ctx}/{name}.svg"):
            return ctx
    return None


def write(out):
    n = 0
    for ctx, icons in OD.items():
        d = f"{out}/scalable/{ctx}"
        for name, fn in icons.items():
            p = f"{d}/{name}.svg"
            if os.path.lexists(p):
                os.remove(p)
            open(p, "w").write(_ic(fn)().svg(64))
            n += 1
    missing = []
    for a, t in OD_ALIASES.items():
        ctx, name = t.split("/") if "/" in t else (_find(out, t), t)
        if ctx is None or not os.path.exists(f"{out}/scalable/{ctx}/{name}.svg"):
            missing.append(t)
            continue
        old = _find(out, a)
        if a.startswith("kwalletmanager") and old:          # was the password key; KWallet is a wallet
            os.remove(f"{out}/scalable/{old}/{a}.svg")
            old = None
        if old is None:
            os.symlink(f"{name}.svg" if ctx == _find(out, name) else f"../{ctx}/{name}.svg", f"{out}/scalable/{ctx}/{a}.svg")
    for name, (emblem, box) in SMALL_EMBLEM_ONLY.items():
        for sub, px in (("16x16", 16), ("22x22", 22)):
            p = f"{out}/{sub}/places/{name}.svg"
            if os.path.lexists(p):
                os.remove(p)
            open(p, "w").write(_emblem_only(emblem, box).svg(px))
            for f in os.listdir(f"{out}/scalable/places"):          # names that share it (folder-desktop ...)
                lp = f"{out}/scalable/places/{f}"
                q = f"{out}/{sub}/places/{f}"
                if os.path.islink(lp) and os.readlink(lp) == f"{name}.svg" and not os.path.lexists(q):
                    os.symlink(f"{name}.svg", q)
    for name, body in SYMBOLIC_WINDOW.items():
        for c in os.listdir(f"{out}/scalable"):
            p = f"{out}/scalable/{c}/{name}.svg"
            if os.path.lexists(p):
                os.remove(p)
        open(f"{out}/scalable/actions/{name}.svg", "w").write(_sym_svg(body))
    a = f"{out}/scalable/actions/window-unmaximize-symbolic.svg"
    if not os.path.lexists(a):
        os.symlink("window-restore-symbolic.svg", a)
    for a, t in OD_OVERRIDE.items():
        ctx, name = t.split("/")
        old = _find(out, a)
        if old:
            os.remove(f"{out}/scalable/{old}/{a}.svg")
        os.symlink(f"{name}.svg", f"{out}/scalable/{ctx}/{a}.svg")
    if missing:
        print("odds: alias targets missing:", missing)
    return n


# ------------------------------------------------------------------ KDE 2/3 Control Centre
def control_centre(ic):
    """KDE Control Centre, as in KDE 2/3: a grey monitor showing a colour chart, with a green circuit board
    standing in front of its left side (traced from KDE Classic's preferences-desktop, then redrawn)."""
    # stand
    base = "M10,53Q10,52 11,52H49Q50,52 50,53V57Q50,58 49,58H11Q10,58 10,57Z"
    ic.shadow(base, 2.4, 2)
    ic.path("M17,47H43V53H17Z", ic.lg([(0, "#5c6168"), (.4, "#d9dce0"), (1, "#5c6168")], 0, 0, 1, 0), INK, LW)
    ic.path(base, ic.lg([(0, "#ffffff"), (.5, "#c3c7cd"), (1, "#6c727a")], 0, 0, 0, 1), INK, LW)
    # monitor
    mon = "M28,4Q28,2 30,2H56Q58,2 58,4V46Q58,48 56,48H30Q28,48 28,46Z"
    ic.shadow(mon, 2.6, 2.2)
    ic.path(mon, ic.lg([(0, "#ffffff"), (.5, "#c3c7cd"), (1, "#7b818a")], 0, 0, 1, 1), INK, LW)
    ic.path("M31,7H55V40H31Z", "#0a0b0d", INK, 1.2)
    rows = (("#1a7a7a", "#1a7a1a", "#7a7a1a", "#b0560a", "#7a0a0a"),
            ("#1aa0a0", "#1ab01a", "#b0b01a", "#e87a1a", "#c01a1a"),
            ("#3ae8e8", "#3ae83a", "#f0f03a", "#ffa860", "#ff2a2a"),
            ("#c0f8f8", "#c8f8c0", "#f8f8c8", "#f8e0c8", "#f8c8c8"))
    for r, cols in enumerate(rows):
        for c, col in enumerate(cols):
            x, y = 32.6 + c * 4.4, 9.6 + r * 7.6
            ic.path(f"M{x:.1f},{y:.1f}h3.2v6h-3.2Z", ic.lg([(0, "#ffffff"), (.35, col), (1, col)], 0, 0, 1, 1), None)
    ic.path(rrect(49, 43, 4, 2.2, .6), ic.lg([(0, "#c8f8a8"), (1, "#2a9a1a")], 0, 0, 0, 1), INK, .6)
    # the circuit board
    board = "M5,2H30V48H5Z"
    ic.shadow(board, 2.6, 2.2)
    ic.path("M2,18H5V46H2Z", ic.lg([(0, "#ffffff"), (1, "#8a9098")], 0, 0, 1, 0), INK, 1)     # mounting bracket
    for k in range(6):                                                                          # gold edge fingers
        ic.path(f"M2,{4.6 + k * 2.2:.1f}H5.4V{6 + k * 2.2:.1f}H2Z", ic.lg([(0, "#fff6c0"), (1, "#c8a010")], 0, 0, 1, 0), INK, .5)
    ic.path(board, ic.lg([(0, "#a8e870"), (.5, "#4aa83a"), (1, "#1e6a1e")], 0, 0, 1, 1), INK, LW)
    traces = ("M8,8H14V18M8,12H12M8,28H11V22M14,18V30H18V36M26,10H22V14M26,16V34M20,24H24M8,40H12M17,14H20V20H24"
              "M12,30H8M20,30V36")
    ic.add(f'<path d="{traces}" fill="none" stroke="#e8e070" stroke-width="1" stroke-linejoin="round"/>')
    for x, y, w, h in ((15, 7, 9, 7), (10, 19, 5, 5), (12, 35, 5, 5), (19, 35, 5, 5)):
        ic.path(rrect(x, y, w, h, .6), ic.lg([(0, "#6c727a"), (1, "#14171c")], 0, 0, 1, 1), INK, .8)
        ic.add(f'<path d="M{x + 1},{y + 1}H{x + w - 1.6}" stroke="#a8adb4" stroke-width=".7"/>')
    for y, c in ((18, "#e0281a"), (24, "#2a4ae8"), (29, "#2a4ae8")):
        ic.path(rrect(24.4, y, 2.2, 4, 1), c, INK, .5)
    ic.path("M9,4.6H12V6.2H9Z", "#e0281a", INK, .4)
    ic.path("M9,44H28V46H9Z", ic.lg([(0, "#ffffff"), (1, "#7b818a")], 0, 0, 0, 1), INK, .7)


# ------------------------------------------------------------------ symbolic window buttons
# Apps that draw their own title bars (GTK, Firefox, Chromium/Electron) ask for window-*-symbolic and tint the
# result. Chromium also falls back to window-close etc. in the same theme when the -symbolic name is missing,
# which picked up our full-colour icons - so these plain single-colour glyphs are supplied instead. They use the
# ColorScheme-Text class so KDE tints them too.
def _sym_svg(body):
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">'
            '<style type="text/css" id="current-color-scheme">.ColorScheme-Text { color:#2e3436; }</style>'
            f'<g class="ColorScheme-Text" fill="currentColor" style="fill:currentColor">{body}</g></svg>\n')


SYMBOLIC_WINDOW = {
    "window-close-symbolic": '<path d="M4.4,3.3L8,6.9L11.6,3.3L12.7,4.4L9.1,8L12.7,11.6L11.6,12.7L8,9.1L4.4,12.7L3.3,11.6L6.9,8L3.3,4.4Z"/>',
    "window-minimize-symbolic": '<path d="M4,10.5H12V12H4Z"/>',
    "window-maximize-symbolic": '<path d="M4,4H12V12H4ZM5.5,5.5V10.5H10.5V5.5Z" fill-rule="evenodd"/>',
    "window-restore-symbolic": '<path d="M6,3H13V10H11.5V4.5H6Z"/><path d="M3,6H10V13H3ZM4.5,7.5V11.5H8.5V7.5Z" fill-rule="evenodd"/>',
}
