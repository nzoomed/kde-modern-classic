#!/usr/bin/env python3
"""Check the built KDE Modern Classic theme folder for problems. Standard library only.

    python3 tools/check_theme.py [THEME_DIR]        (default: KDE-Modern-Classic)

Exit status is 1 if any check fails. Warnings are printed but don't fail.

Checks:
  links       every symlink resolves, and stays inside the theme folder
  names       icon file names use only a-z A-Z 0-9 . _ - + @
  xml         every SVG parses as XML and has an <svg> root
  refs        every url(#id) / href="#id" points to an id defined in the same file  (Qt paints a missing
              gradient solid black, which is how "black square" icons happen)
  ids         no id is defined twice in one file
  embedded    no <image> or <object> (bitmaps hidden inside SVGs)
  filters     <filter>/<mask> only in files listed in ALLOW_FILTERS (Qt older than 6.7 ignores them)
  firefox     the theme must not ship firefox / firefox-esr / org.mozilla.firefox (it would hide Firefox's own
              logo; the generic browser picture is the optional add-on in addon-kit/generic-browser)
  index       every folder listed in index.theme exists, and every icon folder is listed
"""
import os, re, sys
import xml.etree.ElementTree as ET

THEME = sys.argv[1] if len(sys.argv) > 1 else "KDE-Modern-Classic"
FORBIDDEN = {"firefox", "firefox-esr", "org.mozilla.firefox"}
ALLOW_FILTERS = {"gwenview.svg"}          # supplied by the author (src/supplied/), uses blur for its glow
NAME_OK = re.compile(r"^[A-Za-z0-9._+@-]+\.svg$")

fails, warns = [], []
def fail(check, msg): fails.append(f"[{check}] {msg}")
def warn(check, msg): warns.append(f"[{check}] {msg}")

root = os.path.realpath(THEME)
if not os.path.isfile(os.path.join(root, "index.theme")):
    sys.exit(f"{THEME}: no index.theme here")

seen = {}
icon_dirs = set()
for dp, dn, fn in os.walk(root):
    for f in fn:
        p = os.path.join(dp, f)
        rel = os.path.relpath(p, root)
        if not f.endswith(".svg"):
            continue
        icon_dirs.add(os.path.relpath(dp, root))
        if not NAME_OK.match(f):
            fail("names", rel)
        if f[:-4] in FORBIDDEN:
            fail("firefox", f"{rel}: the theme must not ship this name")
        if os.path.islink(p):
            tgt = os.path.realpath(p)
            if not os.path.exists(tgt):
                fail("links", f"{rel} -> {os.readlink(p)} (broken)")
                continue
            if not tgt.startswith(root + os.sep):
                fail("links", f"{rel} -> {os.readlink(p)} (points outside the theme)")
            continue
        seen[rel] = p

for rel, p in sorted(seen.items()):
    s = open(p, encoding="utf-8", errors="replace").read()
    try:
        r = ET.fromstring(s)
        if not r.tag.endswith("svg"):
            fail("xml", f"{rel}: root element is <{r.tag}>")
    except ET.ParseError as e:
        fail("xml", f"{rel}: {e}")
        continue
    ids = re.findall(r'\bid="([^"]+)"', s)
    dup = sorted({i for i in ids if ids.count(i) > 1})
    if dup:
        fail("ids", f"{rel}: defined more than once: {', '.join(dup[:5])}")
    refs = set(re.findall(r"url\(#([^)]+)\)", s)) | set(re.findall(r'href="#([^"]+)"', s))
    missing = sorted(refs - set(ids))
    if missing:
        fail("refs", f"{rel}: points to missing {', '.join(missing[:5])}")
    if re.search(r"<(image|object)\b", s):
        fail("embedded", f"{rel}: contains <image> or <object>")
    if re.search(r"<(filter|mask)\b", s):
        (warn if os.path.basename(rel) in ALLOW_FILTERS else fail)("filters", f"{rel}: uses <filter>/<mask>")

idx = open(os.path.join(root, "index.theme"), encoding="utf-8").read()
m = re.search(r"^Directories=(.*)$", idx, re.M)
listed = set(filter(None, (m.group(1) if m else "").split(",")))
m2 = re.search(r"^ScaledDirectories=(.*)$", idx, re.M)
listed |= set(filter(None, (m2.group(1) if m2 else "").split(",")))
for d in sorted(listed):
    if not os.path.isdir(os.path.join(root, d)):
        warn("index", f"index.theme lists {d}, which doesn't exist")
    if f"[{d}]" not in idx:
        fail("index", f"index.theme lists {d} but has no [{d}] section")
for d in sorted(icon_dirs - listed):
    fail("index", f"{d} holds icons but isn't in index.theme's Directories")

n_files = len(seen)
print(f"{THEME}: {n_files} drawings checked, {len(fails)} problem(s), {len(warns)} warning(s)")
for w in warns:
    print("  warning", w)
for f in fails:
    print("  FAIL", f)
sys.exit(1 if fails else 0)
