#!/usr/bin/env python3
"""qBittorrent icon check for KDE Modern Classic.

For every icon name qBittorrent asks for (when "Use icons from system theme" is on), shows which installed icon
theme answers it and which file, and flags files likely to draw as a black or empty square.

Run:  python3 qbt-icon-check.py            (uses the icon theme set in System Settings)
      python3 qbt-icon-check.py THEME      (check another theme folder name)
"""
import configparser, os, re, struct, sys, zlib

NAMES = [('application-exit', ''), ('application-rss', ''), ('application-url', ''), ('browser-cookies', ''), ('chart-line', ''), ('checked-completed', 'completed'), ('configure', ''), ('connected', ''), ('dialog-warning', ''), ('directory', ''), ('disconnected', ''), ('download', ''), ('downloading', ''), ('edit-clear', ''), ('edit-copy', ''), ('edit-find', ''), ('edit-rename', ''), ('error', ''), ('filter-active', 'filteractive'), ('filter-all', 'filterall'), ('filter-inactive', 'filterinactive'), ('filter-stalled', 'filterstalled'), ('firewalled', ''), ('folder-documents', ''), ('folder-new', ''), ('folder-remote', ''), ('force-recheck', 'checking'), ('go-bottom', ''), ('go-down', ''), ('go-top', ''), ('go-up', ''), ('hash', 'edit-copy'), ('help-about', ''), ('help-contents', ''), ('insert-link', ''), ('ip-blocked', 'view-filter'), ('list-add', ''), ('list-remove', ''), ('loading', ''), ('mail-inbox', ''), ('name', 'edit-copy'), ('network-connect', 'network-wired'), ('network-server', ''), ('object-locked', ''), ('pause-session', 'media-playback-pause'), ('peers', ''), ('peers-add', ''), ('peers-remove', ''), ('plugins', ''), ('preferences-advanced', 'preferences-other'), ('preferences-bittorrent', 'preferences-system-network'), ('preferences-desktop', ''), ('preferences-webui', 'network-server'), ('qbittorrent', ''), ('qbittorrent-tray', ''), ('qbittorrent-tray-mono', ''), ('queued', ''), ('reannounce', 'document-edit-verify'), ('rss_read_article', 'sphere'), ('rss_unread_article', 'sphere'), ('set-location', ''), ('slow', ''), ('slow_off', ''), ('speedometer', ''), ('stalledDL', ''), ('stalledUP', ''), ('stopped', 'media-playback-pause'), ('tags', 'inode-directory'), ('task-complete', 'application-exit'), ('task-reject', 'unavailable'), ('torrent-creator', 'document-edit'), ('torrent-magnet', 'kt-magnet'), ('torrent-start', 'media-playback-start'), ('torrent-start-forced', 'media-playback-start'), ('torrent-stop', 'media-playback-pause'), ('tracker-error', 'dialog-error'), ('tracker-warning', 'dialog-warning'), ('trackerless', 'network-server'), ('trackers', 'network-server'), ('upload', 'seeding'), ('view-categories', ''), ('view-preview', ''), ('view-refresh', ''), ('view-statistics', ''), ('wallet-open', '')]   # (icon name, qBittorrent's fallback name) taken from qBittorrent's source

home = os.path.expanduser("~")
data_dirs = [os.environ.get("XDG_DATA_HOME", os.path.join(home, ".local/share"))] + \
            os.environ.get("XDG_DATA_DIRS", "/usr/local/share:/usr/share").split(":")
bases = [os.path.join(home, ".icons")] + [os.path.join(d, "icons") for d in data_dirs]


def current_theme():
    if len(sys.argv) > 1:
        return sys.argv[1]
    cfg = configparser.ConfigParser(strict=False, interpolation=None)
    cfg.read(os.path.join(home, ".config/kdeglobals"))
    return cfg.get("Icons", "Theme", fallback="breeze")


def theme_info(t):
    for b in bases:
        idx = os.path.join(b, t, "index.theme")
        if os.path.exists(idx):
            cfg = configparser.ConfigParser(strict=False, interpolation=None)
            cfg.optionxform = str
            cfg.read(idx)
            sec = cfg["Icon Theme"] if cfg.has_section("Icon Theme") else {}
            dirs = [d for d in (sec.get("Directories", "") + "," + sec.get("ScaledDirectories", "")).split(",") if d]
            inh = [i for i in sec.get("Inherits", "").split(",") if i]
            roots = [os.path.join(bb, t) for bb in bases if os.path.isdir(os.path.join(bb, t))]
            return dirs, inh, roots
    return None


def chain(t):
    out, todo = [], [t]
    while todo:
        x = todo.pop(0)
        if x in out:
            continue
        info = theme_info(x)
        if info is None:
            out.append(x + " (NOT INSTALLED)")
            continue
        out.append(x)
        todo += info[1]
    if not any(x.split()[0] == "hicolor" for x in out):
        out.append("hicolor")
    return out


def find(name, themes):
    for t in themes:
        info = theme_info(t)
        if not info:
            continue
        dirs, _, roots = info
        hits = []
        for r in roots:
            for d in dirs:
                for ext in (".svg", ".png", ".svgz", ".xpm"):
                    p = os.path.join(r, d, name + ext)
                    if os.path.lexists(p):
                        hits.append(p)
        if hits:
            small = [h for h in hits if re.search(r"/(16|22)x(16|22)(@\dx)?/", h)]
            return t, (small or hits)[0], len(hits)
    for d in ("/usr/share/pixmaps",):
        for ext in (".svg", ".png", ".xpm"):
            p = os.path.join(d, name + ext)
            if os.path.exists(p):
                return "pixmaps", p, 1
    return None


def png_problem(p):
    with open(p, "rb") as fh:
        raw = fh.read()
    if raw[:8] != b"\x89PNG\r\n\x1a\n":
        return "not a real PNG file"
    w, h, depth, ctype = struct.unpack(">IIBB", raw[16:26])
    has_trns = b"tRNS" in raw
    if ctype in (0, 2) and not has_trns or ctype == 3 and not has_trns:
        return "PNG has NO transparency: draws as a solid square"
    try:
        from PIL import Image
        im = Image.open(p).convert("RGBA")
        px = list(im.getdata())
        vis = [q for q in px if q[3] > 30]
        if not vis:
            return "PNG is fully transparent (shows as nothing)"
        dark = sum(1 for q in vis if max(q[:3]) < 40)
        if len(vis) > .85 * len(px) and dark > .6 * len(vis):
            return "PNG is mostly solid black"
    except ImportError:
        pass
    return ""


def svg_problem(p):
    try:
        raw = open(p, "rb").read()
        s = (zlib.decompress(raw, 31) if p.endswith(".svgz") else raw).decode("utf-8", "replace")
    except Exception as e:
        return f"cannot read ({e})"
    ids = set(re.findall(r'\bid="([^"]+)"', s))
    miss = sorted(set(re.findall(r"url\(#([^)]+)\)", s)) - ids)
    if miss:
        return "SVG points to missing gradient(s) " + ", ".join(miss[:3]) + ": Qt fills them black"
    if "<filter" in s or "<mask" in s:
        return "SVG uses filter/mask, which Qt may draw wrongly"
    if not re.search(r"<(path|rect|circle|ellipse|polygon|image|use|g)\b", s):
        return "SVG has nothing to draw"
    return ""


theme = current_theme()
themes = [t for t in chain(theme) if "NOT INSTALLED" not in t]
print("Icon theme:", theme)
print("Lookup order:", " -> ".join(chain(theme)))
print()
flagged = 0
rows = []
for name, fb in NAMES:
    r = find(name, themes)
    used = name
    if not r and fb:
        r, used = find(fb, themes), fb
    if not r:
        rows.append(("qBittorrent's own", name, "", ""))
        continue
    t, p, n = r
    note = ""
    if os.path.islink(p) and not os.path.exists(p):
        note = "BROKEN LINK"
    elif os.path.getsize(os.path.realpath(p)) == 0:
        note = "EMPTY FILE"
    elif p.endswith(".png"):
        note = png_problem(os.path.realpath(p))
    elif ".svg" in p:
        note = svg_problem(os.path.realpath(p))
    flagged += bool(note)
    shown = name if used == name else f"{name} (via {used})"
    rows.append((t, shown, p, note))
for t, shown, p, note in sorted(rows, key=lambda r: (not r[3], r[0], r[1])):
    print(f"{'!! ' if note else '   '}{shown:34} {t:22} {p}" + (f"\n      -> {note}" if note else ""))
print(f"\n{flagged} suspicious file(s). Lines starting !! are the likely black squares.")
