"""KDE Classic Vector: the last generic icons Plasma asked for that still fell back to Breeze (save all,
install / uninstall, tags, grid and guides, scale, contrast, ruler, licence, partitions ...), drawn in the
theme's style, plus aliases for names that mean the same as icons already in the set.
Runs after every other module, so its aliases can point anywhere.
"""
import math, os
from gen import Icon, INK, LW, circle, rrect
from actions import _mpath
from settingstrace import _teal, _arrow_pts, _double_arrow, _badge, _ok, _no, _poly, _page


def _ic(fn):
    def f():
        ic = Icon()
        fn(ic)
        return ic
    return f


def bookmark_remove(ic):
    from uitrace import _ribbon
    _ribbon(ic)
    _badge(ic, 47, 47, 12, "red", "M41,47H53")


def save_all(ic):
    """Save all: three floppy disks fanned one behind another."""
    from actions import save
    for k, (dx, dy) in enumerate(((14, 0), (7, 7), (0, 14))):
        ic.add(f'<g transform="translate({dx},{dy}) scale(.78)">')
        save(ic)
        ic.add("</g>")


def open_remote(ic):
    """Open remote: the open-document folder with the globe in front."""
    from actions import open_document
    from gen import e_globe
    open_document(ic)
    e_globe(ic, 34, 34, 13)


def multipartition(ic):
    """Partitioned disk: the hard disk with its space split into coloured parts."""
    from devices import harddisk
    harddisk(ic)
    bar = "M8,50H56V58H8Z"
    ic.shadow(bar, 1.8, 1.5)
    for x0, x1, c in ((8, 28, ("#c8ffb0", "#14920a")), (28, 44, ("#c8dcff", "#1a3aa0")), (44, 56, ("#fffbc0", "#a89004"))):
        ic.path(f"M{x0},50H{x1}V58H{x0}Z", ic.lg([(0, c[0]), (1, c[1])]), INK, 1.1)


def install(ic):
    """Install: the parcel with a green arrow going down into it."""
    from discover import parcel
    ic.add('<g transform="translate(0,6) scale(.9)">')
    parcel(ic)
    ic.add("</g>")
    d = _poly(_arrow_pts(50, 2, 50, 32, 4, 10, 11))
    ic.shadow(d, 1.8, 1.5)
    _mpath(ic, d, ic.lg([(0, "#c8f8a8"), (.45, "#3fae2a"), (1, "#145a0c")], 0, 0, 1, 0), 1.3)


def uninstall(ic):
    """Uninstall: the parcel with a red cross."""
    from discover import parcel
    ic.add('<g transform="translate(0,4) scale(.9)">')
    parcel(ic)
    ic.add("</g>")
    _no(ic, 48, 48, 12)


def tag_new(ic):
    """New tag: the yellow luggage tag (tip and hole at the top right) with a green plus badge at the lower right."""
    from uitrace import _new_badge
    from kdeapps import _tag
    _tag(ic, 1.0, 0, 2)
    _new_badge(ic, 50, 48, 14)


def layer_duplicate(ic):
    from desktoptrace import _layers
    _layers(ic)
    _badge(ic, 48, 48, 11, "green", "M48,42V54M42,48H54")


def _window(ic):
    w = "M4,6H60V58H4Z"
    ic.shadow(w, 2.4, 2)
    ic.path(w, ic.lg([(0, "#ffffff"), (1, "#e4e6e9")], 0, 0, 1, 1), INK, LW)
    ic.path("M4,6H60V14H4Z", ic.lg([(0, "#e4e6e9"), (1, "#8a9098")]), INK, LW)


def show_grid(ic):
    _window(ic)
    for k in range(1, 6):
        ic.add(f'<path d="M{4 + k * 9.33:.2f},14V58M4,{14 + k * 7.33:.2f}H60" stroke="#8a9cc0" stroke-width="1"/>')


def show_guides(ic):
    _window(ic)
    ic.add('<path d="M22,14V58M4,40H60" stroke="#2a6ae0" stroke-width="1.6" stroke-dasharray="4 2.6"/>')
    for x, y in ((22, 14), (4, 40)):
        ic.path(f"M{x - 3},{y - 1}L{x + 3},{y - 1}L{x},{y + 4}Z" if y == 14 else f"M{x - 1},{y - 3}V{y + 3}L{x + 4},{y}Z", "#2a6ae0", INK, .8)


def transform_scale(ic):
    """Scale: a small square growing into a larger dashed one, with a teal arrow out to the corner."""
    ic.add(f'<path d="M6,6H58V58H6Z" fill="none" stroke="{INK}" stroke-width="1.4" stroke-dasharray="4 3"/>')
    s = "M6,34H30V58H6Z"
    ic.shadow(s, 2, 1.7)
    ic.path(s, ic.lg([(0, "#ffffff"), (1, "#c3c7cd")], 0, 0, 1, 1), INK, LW)
    _teal(ic, _poly(_arrow_pts(28, 36, 56, 8, 3.4, 9, 11)))


def contrast(ic):
    """Contrast: a disc half white, half black."""
    o = circle(32, 32, 26)
    ic.shadow(o, 2.6, 2.2)
    ic.path(o, "#ffffff", INK, LW * 1.2)
    ic.path("M32,6A26,26 0 0 1 32,58Z", ic.lg([(0, "#4c5158"), (1, "#000000")], 0, 0, 1, 1), None)
    ic.path(o, "none", INK, LW * 1.2)


def measure(ic):
    """Measure: a wooden ruler lying diagonally with its marks."""
    ic.add('<g transform="translate(32,32) rotate(-40)">')
    r = "M-30,-8H30V8H-30Z"
    ic.shadow(r, 2.4, 2)
    ic.path(r, ic.lg([(0, "#fff0c0"), (.5, "#e8c060"), (1, "#a87a20")], 0, 0, 0, 1), INK, LW)
    for k in range(-27, 28, 3):
        h = 6 if k % 15 == 0 else (4.4 if k % 6 == 0 else 3)
        ic.add(f'<path d="M{k},-8V{-8 + h}" stroke="{INK}" stroke-width=".9"/>')
    ic.add("</g>")


def licence(ic):
    """Licence: a certificate page with a red wax seal and ribbons."""
    _page(ic, 8, 4, 44, 54)
    for k in range(4):
        ic.add(f'<path d="M14,{20 + k * 6}H{44 - (k % 2) * 8}" stroke="#7b818a" stroke-width="1.6"/>')
    ic.add('<path d="M14,13H40" stroke="#1a3aa0" stroke-width="2.6"/>')
    for d in ("M38,48L33,62L38,59L42,62Z", "M46,48L44,62L48,59L52,62Z"):
        ic.path(d, ic.lg([(0, "#ff8a7a"), (1, "#a8180a")]), INK, 1)
    ic.shadow(circle(42, 46, 9), 1.8, 1.5)
    ic.path(circle(42, 46, 9), ic.rg([(0, "#ffb0a0"), (.55, "#d8180a"), (1, "#6a0402")], .4, .35, .8), INK, LW)
    ic.path(circle(42, 46, 5), "none", "#ffd0c0", 1)


def user_online(ic):
    """Online user: a KDE Classic cartoon face in profile with the green online light."""
    from settings import _profile
    _profile(ic, 9, 4, 1.75, ("#5a5048", "#14100c"))
    ic.shadow(circle(50, 50, 8), 1.6, 1.4)
    ic.path(circle(50, 50, 8), ic.rg([(0, "#d8ffc8"), (.5, "#3fd02a"), (1, "#0e6a08")], .4, .35, .8), INK, 1.3)


def anchor(ic):
    """Anchor: a dark iron ship's anchor."""
    d = "M32,16V54M18,28H46M10,40Q14,56 32,56Q50,56 54,40"
    ic.add(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="7.4" stroke-linecap="round"/>')
    ic.add(f'<path d="{d}" fill="none" stroke="#5c6168" stroke-width="4.4" stroke-linecap="round"/>')
    ic.add(f'<path d="{d}" fill="none" stroke="#c3c7cd" stroke-width="1.2" stroke-linecap="round" transform="translate(-.8,-.8)"/>')
    for x, s in ((10, -1), (54, 1)):
        ic.path(f"M{x},34L{x - s * 3},44L{x + s * 6},42Z", "#5c6168", INK, 1.1)
    ic.path(circle(32, 10, 6), "none", INK, 4.4)
    ic.path(circle(32, 10, 6), "none", "#5c6168", 2.4)


def red_eye(ic):
    """Red-eye removal: an eye with its red pupil, being corrected."""
    eye = "M4,32Q32,6 60,32Q32,58 4,32Z"
    ic.shadow(eye, 2.2, 1.8)
    ic.path(eye, "#ffffff", INK, LW * 1.2)
    ic.path(circle(32, 32, 13), ic.rg([(0, "#a8d0ff"), (.6, "#1a4ae0"), (1, "#0a1a60")], .4, .35, .8), INK, 1.1)
    ic.path(circle(32, 32, 6.4), ic.rg([(0, "#ff8a7a"), (.6, "#e0200a"), (1, "#7a0402")], .4, .35, .8), None)
    ic.path(circle(28.6, 28.4, 2.4), "#ffffff", None)


def beer(ic):
    """Beer: a frothy glass mug of beer."""
    ic.add(f'<path d="M44,22Q58,22 58,34Q58,46 44,46" fill="none" stroke="{INK}" stroke-width="7"/><path d="M44,22Q58,22 58,34Q58,46 44,46" fill="none" stroke="#e4eef4" stroke-width="4"/>')
    g = "M10,14H46V56Q46,60 42,60H14Q10,60 10,56Z"
    ic.shadow(g, 2.4, 2)
    ic.path(g, ic.lg([(0, "#ffe08a"), (.5, "#f0a810"), (1, "#a86404")], 0, 0, 1, 0), INK, LW)
    ic.add('<path d="M16,22V54M38,22V54" stroke="#fff" stroke-opacity=".45" stroke-width="2.4"/>')
    ic.path("M7,16Q8,6 18,8Q22,2 30,6Q38,2 42,8Q50,8 49,16Q46,22 40,18Q34,24 28,19Q22,24 16,19Q10,22 7,16Z", "#ffffff", INK, LW)


def car(ic):
    """Car: a little red car seen from the side."""
    body = "M4,42V34Q4,30 10,29L18,18Q20,16 24,16H40Q44,16 46,19L52,29Q60,30 60,36V42Q60,44 58,44H6Q4,44 4,42Z"
    ic.shadow(body, 2.4, 2)
    ic.path(body, ic.lg([(0, "#ff9a8a"), (.45, "#e0200a"), (1, "#7a0402")], 0, 0, 0, 1), INK, LW)
    ic.path("M21,20L15,29H31V20Z", ic.lg([(0, "#e8f6ff"), (1, "#7aaacc")], 0, 0, 1, 1), INK, 1)
    ic.path("M34,20V29H49L44,21Q43,20 41,20Z", ic.lg([(0, "#e8f6ff"), (1, "#7aaacc")], 0, 0, 1, 1), INK, 1)
    for x in (16, 48):
        ic.path(circle(x, 44, 7.4), ic.rg([(0, "#5c6168"), (1, "#0a0c10")], .4, .35, .8), INK, 1.2)
        ic.path(circle(x, 44, 3), ic.lg([(0, "#ffffff"), (1, "#8a9098")]), INK, .8)


def play_rtl(ic):
    """Play for right-to-left layouts: the play triangle pointing left."""
    from uitrace import media_playback_start
    ic.add('<g transform="translate(64,0) scale(-1,1)">')
    media_playback_start(ic)
    ic.add("</g>")


def _ghost_page(ic, x, y, w, h):
    """Where the page used to be: a dashed outline only."""
    ic.add(f'<path d="M{x},{y}H{x + w - 9}L{x + w},{y + 9}V{y + h}H{x}Z" fill="#ffffff" fill-opacity=".35" stroke="#5a6068" '
           f'stroke-width="1.6" stroke-dasharray="3.2 2.2" stroke-linejoin="round"/>')


def edit_move(ic):
    """Move: the page has left its dashed outline behind, a teal arrow carrying it across."""
    from actions import _page as apage
    _ghost_page(ic, 3, 4, 30, 38)
    apage(ic, 28, 20, 32, 40)
    _teal(ic, _poly(_arrow_pts(10, 50, 30, 50, 4.4, 11, 11)))


def edit_link(ic):
    """Link: a page with KDE Classic's link tile (curved teal arrow) on its bottom left corner."""
    from actions import _page as apage
    from settingstrace import link_emblem
    apage(ic, 18, 4, 40, 52)
    ic.add('<g transform="translate(1,29) scale(.52)">')
    link_emblem(ic)
    ic.add("</g>")


def mail_message(ic):
    """A plain envelope, no badge: one email message."""
    from desktoptrace import _envelope
    _envelope(ic, 4, 13, 56, 40)


LO = {
    "actions": {"bookmark-remove": bookmark_remove, "document-save-all": save_all, "document-open-remote": open_remote,
                "tag-new": tag_new, "layer-duplicate": layer_duplicate, "show-grid": show_grid, "show-guides": show_guides,
                "transform-scale": transform_scale, "media-playback-start-rtl": play_rtl, "contrast": contrast, "measure": measure, "redeyes": red_eye,
                "edit-move": edit_move, "edit-link": edit_link, "mail-message": mail_message},
    "devices": {"drive-multipartition": multipartition},
    "apps": {"install": install, "uninstall": uninstall, "license": licence, "anchor": anchor, "drink-beer": beer, "car": car},
    "status": {"im-user-online": user_online},
}
LO_ALIASES = {
    "bookmark-remove-symbolic": "actions/bookmark-remove", "document-save-all-symbolic": "actions/document-save-all",
    "document-open-remote-symbolic": "actions/document-open-remote", "tag-new-symbolic": "actions/tag-new",
    "transform-scale-symbolic": "actions/transform-scale", "drive-multipartition-symbolic": "devices/drive-multipartition",
    "drive-partition": "devices/drive-multipartition", "drive-partition-symbolic": "devices/drive-multipartition",
    "install-symbolic": "apps/install", "uninstall-symbolic": "apps/uninstall", "im-user-online-symbolic": "status/im-user-online",
    "call-start-symbolic": "status/call-start", "computer-laptop-symbolic": "devices/computer-laptop",
    "tablet-symbolic": "apps/input-tablet", "document-preview": "actions/view-preview",
    "distribute-horizontal-x": "actions/distribute-horizontal", "flag-red": "actions/mark-location",
    "pointer": "actions/transform-browse", "player-time": "apps/clock", "gtk-add": "actions/list-add",
    "gtk-close": "actions/window-close", "gtk-stop": "actions/process-stop", "gtk-cdrom": "devices/media-optical",
    "dialog-align-and-distribute-symbolic": "actions/align-horizontal-left", "dialog-filters-symbolic": "actions/view-filter",
    "dialog-object-properties-symbolic": "actions/document-properties", "show-grid-symbolic": "actions/show-grid",
    "show-guides-symbolic": "actions/show-guides", "donate": "actions/help-donate-symbolic", "donate-symbolic": "actions/help-donate-symbolic",
    "help-donate-aud": "actions/help-donate-symbolic", "help-donate-aud-symbolic": "actions/help-donate-symbolic", "help-donate-brl": "actions/help-donate-symbolic", "help-donate-brl-symbolic": "actions/help-donate-symbolic", "help-donate-cad": "actions/help-donate-symbolic", "help-donate-cad-symbolic": "actions/help-donate-symbolic", "help-donate-chf": "actions/help-donate-symbolic", "help-donate-chf-symbolic": "actions/help-donate-symbolic", "help-donate-cny": "actions/help-donate-symbolic", "help-donate-cny-symbolic": "actions/help-donate-symbolic", "help-donate-eur": "actions/help-donate-symbolic", "help-donate-eur-symbolic": "actions/help-donate-symbolic", "help-donate-gbp": "actions/help-donate-symbolic", "help-donate-gbp-symbolic": "actions/help-donate-symbolic", "help-donate-inr": "actions/help-donate-symbolic", "help-donate-inr-symbolic": "actions/help-donate-symbolic", "help-donate-jpy": "actions/help-donate-symbolic", "help-donate-jpy-symbolic": "actions/help-donate-symbolic", "help-donate-mxn": "actions/help-donate-symbolic", "help-donate-mxn-symbolic": "actions/help-donate-symbolic", "help-donate-pln": "actions/help-donate-symbolic", "help-donate-pln-symbolic": "actions/help-donate-symbolic", "help-donate-rub": "actions/help-donate-symbolic", "help-donate-rub-symbolic": "actions/help-donate-symbolic", "help-donate-sek": "actions/help-donate-symbolic", "help-donate-sek-symbolic": "actions/help-donate-symbolic", "help-donate-try": "actions/help-donate-symbolic", "help-donate-try-symbolic": "actions/help-donate-symbolic", "help-donate-uah": "actions/help-donate-symbolic", "help-donate-uah-symbolic": "actions/help-donate-symbolic", "help-donate-usd": "actions/help-donate-symbolic", "help-donate-usd-symbolic": "actions/help-donate-symbolic", "help-donate-nzd": "actions/help-donate-symbolic", "help-donate-nzd-symbolic": "actions/help-donate-symbolic", "help-donate-krw": "actions/help-donate-symbolic", "help-donate-krw-symbolic": "actions/help-donate-symbolic", "help-donate-zar": "actions/help-donate-symbolic", "help-donate-zar-symbolic": "actions/help-donate-symbolic", "media-playback-start-rtl-symbolic": "actions/media-playback-start-rtl",
    "media-playback-pause-rtl": "actions/media-playback-pause", "media-playback-pause-rtl-symbolic": "actions/media-playback-pause", "inode-blockdevice": "apps/drive-multidisk", "layer-duplicate-symbolic": "actions/layer-duplicate",
    "edit-move-symbolic": "actions/edit-move", "edit-link-symbolic": "actions/edit-link", "mail-message-symbolic": "actions/mail-message",
}


def write(out):
    n = 0
    for ctx, icons in LO.items():
        d = f"{out}/scalable/{ctx}"
        os.makedirs(d, exist_ok=True)
        for name, fn in icons.items():
            open(f"{d}/{name}.svg", "w").write(_ic(fn)().svg(64))
            n += 1
    missing = []
    ctxs = os.listdir(f"{out}/scalable")
    for a, t in LO_ALIASES.items():
        ctx, name = t.split("/")
        d = f"{out}/scalable/{ctx}"
        if not os.path.exists(f"{d}/{name}.svg"):
            missing.append(t)
            continue
        if not any(os.path.lexists(f"{out}/scalable/{c}/{a}.svg") for c in ctxs):
            os.symlink(f"{name}.svg", f"{d}/{a}.svg")
    if missing:
        print("leftovers: alias targets missing:", missing)
    return n
