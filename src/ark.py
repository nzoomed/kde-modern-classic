"""KDE Classic Vector: Ark, the archiver - its app icon and its archive actions (extract, add files, add folder,
remove), so Ark no longer falls back to Breeze. Built on the open cardboard box from the Games category,
recoloured to KDE Classic Ark's orange, with arrows going in or out.
"""
import os
from gen import Icon, INK, LW
from actions import _mpath
from settingstrace import _teal, _arrow_pts, _poly, _badge

ORANGE = {"#fffbe4": "#fff0dc", "#d8c070": "#f8a050", "#e8d690": "#fcc080", "#a89040": "#c86018",
          "#8a7430": "#a84a10", "#5a4a1a": "#6a2a04", "#3a2e0e": "#3a1402", "#b8a050": "#e88030",
          "#fbf2c4": "#ffe0b8", "#cdb468": "#e8803a"}


def _ic(fn):
    def f():
        ic = Icon()
        fn(ic)
        return ic
    return f


def orange_box(ic, transform="translate(2,3) scale(1.1)"):
    """KDE Classic Ark's open orange box (the Games box, recoloured)."""
    from discover import _open_box
    nb, nd = len(ic.body), len(ic.defs)
    ic.add(f'<g transform="{transform}">')
    _open_box(ic)
    ic.add("</g>")
    for lst, start in ((ic.body, nb), (ic.defs, nd)):
        for i in range(start, len(lst)):
            s = lst[i]
            for a, b in ORANGE.items():
                s = s.replace(a, b)
            lst[i] = s


def _arrow(ic, x0, y0, x1, y1, cols, w=5, hw=12, hl=12):
    d = _poly(_arrow_pts(x0, y0, x1, y1, w, hw, hl))
    ic.shadow(d, 1.8, 1.5)
    _mpath(ic, d, ic.lg(cols, 0, 0, 1, 0), 1.3)


RED = [(0, "#ffb0a0"), (.45, "#e8200a"), (1, "#7a0804")]
GREEN = [(0, "#c8f8a8"), (.45, "#3fae2a"), (1, "#145a0c")]


def ark(ic):
    """Ark: the open orange box with KDE Classic's red arrow coming down into it."""
    orange_box(ic)
    for y in (1, 6):
        ic.path(f"M27,{y}H37V{y + 3}H27Z", ic.lg(RED, 0, 0, 1, 0), INK, 1.1)
    _arrow(ic, 32, 11, 32, 34, RED, 5, 12, 12)


def extract(ic):
    """Extract: a teal arrow rising up out of the open box."""
    orange_box(ic)
    _teal(ic, _poly(_arrow_pts(32, 34, 32, 2, 5, 12, 13)))


def insert(ic):
    """Add files: a green arrow going down into the open box."""
    orange_box(ic)
    _arrow(ic, 32, 1, 32, 34, GREEN, 5, 12, 13)


def insert_dir(ic):
    """Add folder: a small folder with a green arrow taking it down into the open box."""
    from gen import folder
    orange_box(ic, "translate(8,8) scale(1.02)")
    ic.add('<g transform="translate(1,0) scale(.42)">')
    folder(ic, "blue")
    ic.add("</g>")
    _arrow(ic, 40, 1, 40, 34, GREEN, 4.4, 11, 12)


def remove(ic):
    """Remove from archive: the open box with a red minus."""
    orange_box(ic, "translate(1,2) scale(1.04)")
    _badge(ic, 48, 48, 12, "red", "M42,48H54")


ARK = {"apps": {"ark": ark},
       "actions": {"archive-extract": extract, "archive-insert": insert, "archive-insert-directory": insert_dir,
                   "archive-remove": remove}}
ARK_ALIASES = {
    "utilities-file-archiver": "apps/ark", "org.kde.ark": "apps/ark", "ark-symbolic": "apps/ark",
    "archive-extract-symbolic": "actions/archive-extract", "archive-insert-symbolic": "actions/archive-insert",
    "archive-insert-directory-symbolic": "actions/archive-insert-directory", "archive-remove-symbolic": "actions/archive-remove",
    "application-x-archive": "mimetypes/application-x-compressed-tar",
}


def write(out):
    n = 0
    for ctx, icons in ARK.items():
        d = f"{out}/scalable/{ctx}"
        for name, fn in icons.items():
            p = f"{d}/{name}.svg"
            if os.path.lexists(p):
                os.remove(p)          # replaces an earlier alias (archive-remove pointed at edit-delete)
            open(p, "w").write(_ic(fn)().svg(64))
            n += 1
    ctxs = os.listdir(f"{out}/scalable")
    for a, t in ARK_ALIASES.items():
        ctx, name = t.split("/")
        if os.path.exists(f"{out}/scalable/{ctx}/{name}.svg") and not any(os.path.lexists(f"{out}/scalable/{c}/{a}.svg") for c in ctxs):
            os.symlink(f"{name}.svg", f"{out}/scalable/{ctx}/{a}.svg")
    return n
