#!/usr/bin/env python3
"""Build an optional add-on icon theme that overrides a few icons of KDE Modern Classic (or any theme),
like the "KDE Modern Classic (Dolphin)" add-on.

You supply the icon files and their licences; the add-on inherits everything else from the base theme.
People choose the add-on in System Settings > Colours & Themes > Icons, and go back by choosing the base theme.

Usage:
    python3 make_addon.py ADDON_DIR

ADDON_DIR holds:
    addon.ini          settings (see the example below)
    icons/             the override icons, each named after the icon it replaces:
                       firefox.svg, org.mozilla.firefox.svg ... (SVG, or PNG named NAME-SIZE.png, e.g. firefox-48.png)
    CREDITS.md         optional: author, source and licence of each icon - copied into the add-on

addon.ini example:
    [addon]
    folder = KDE-Modern-Classic-Extras
    name = KDE Modern Classic (Extras)
    comment = KDE Modern Classic with a few apps' own icons
    base = KDE-Modern-Classic
    inherits = KDE-Modern-Classic,kdeclassic,breeze,hicolor
    example = firefox
    licence = Each icon keeps its own licence; see CREDITS.md.

    [aliases]
    # extra names that should show the same icon
    firefox-esr = firefox
    org.mozilla.firefox = firefox

Writes ADDON_DIR/<folder>/ and ADDON_DIR/<folder>-<date>.tar.gz.
"""
import configparser, datetime, os, re, shutil, sys, tarfile

src = sys.argv[1]
cfg = configparser.ConfigParser(delimiters=("=",))
cfg.optionxform = str
cfg.read(os.path.join(src, "addon.ini"))
a = cfg["addon"]
folder = a.get("folder", "KDE-Modern-Classic-Extras")
out = os.path.join(src, folder)
shutil.rmtree(out, ignore_errors=True)

svgs, pngs = {}, {}
for f in sorted(os.listdir(os.path.join(src, "icons"))):
    p = os.path.join(src, "icons", f)
    m = re.fullmatch(r"(.+)-(\d+)\.png", f)
    if f.endswith(".svg"):
        svgs[f[:-4]] = p
    elif m:
        pngs.setdefault(m.group(1), {})[int(m.group(2))] = p
if not svgs and not pngs:
    sys.exit("No icons found in icons/")

dirs = []
if svgs:
    d = os.path.join(out, "scalable", "apps")
    os.makedirs(d, exist_ok=True)
    for n, p in svgs.items():
        shutil.copy(p, os.path.join(d, n + ".svg"))
    dirs.append(("scalable/apps", "Size=64\nMinSize=8\nMaxSize=512\nContext=Applications\nType=Scalable"))
sizes = sorted({s for v in pngs.values() for s in v})
for s in sizes:
    d = os.path.join(out, f"{s}x{s}", "apps")
    os.makedirs(d, exist_ok=True)
    for n, v in pngs.items():
        if s in v:
            shutil.copy(v[s], os.path.join(d, n + ".png"))
    dirs.insert(0, (f"{s}x{s}/apps", f"Size={s}\nContext=Applications\nType=Fixed"))

# aliases: relative links beside the icon they point to
if cfg.has_section("aliases"):
    for alias, target in cfg["aliases"].items():
        for dpath, _ in dirs:
            d = os.path.join(out, dpath)
            for ext in (".svg", ".png"):
                if os.path.exists(os.path.join(d, target + ext)) and not os.path.lexists(os.path.join(d, alias + ext)):
                    os.symlink(target + ext, os.path.join(d, alias + ext))

with open(os.path.join(out, "index.theme"), "w") as fh:
    fh.write("[Icon Theme]\n"
             f"Name={a.get('name', folder)}\n"
             f"Comment={a.get('comment', 'Optional icon overrides')}\n"
             f"Inherits={a.get('inherits', a.get('base', 'KDE-Modern-Classic') + ',breeze,hicolor')}\n"
             f"Example={a.get('example', next(iter(svgs or pngs)))}\n"
             f"Directories={','.join(d for d, _ in dirs)}\n")
    for d, body in dirs:
        fh.write(f"\n[{d}]\n{body}\n")

names = sorted(set(svgs) | set(pngs))
with open(os.path.join(out, "README.md"), "w") as fh:
    fh.write(f"# {a.get('name', folder)}\n\n"
             f"An optional add-on to {a.get('base', 'KDE Modern Classic')}. It replaces these icons and uses the base theme "
             "for everything else:\n\n" + "".join(f"- `{n}`\n" for n in names) +
             f"\nInstall {a.get('base', 'the base theme')} first, then install this the same way (System Settings > Colours & "
             f"Themes > Icons > Install from File) and choose \"{a.get('name', folder)}\". To undo, choose the base theme again.\n\n"
             f"Licence: {a.get('licence', 'see CREDITS.md')}\n")
if os.path.exists(os.path.join(src, "CREDITS.md")):
    shutil.copy(os.path.join(src, "CREDITS.md"), os.path.join(out, "CREDITS.md"))

tgz = os.path.join(src, f"{folder}-{datetime.date.today():%Y%m%d}.tar.gz")
with tarfile.open(tgz, "w:gz") as t:
    t.add(out, arcname=folder)
print(f"{len(names)} icons -> {tgz}")
