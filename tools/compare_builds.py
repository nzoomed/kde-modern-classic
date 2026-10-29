#!/usr/bin/env python3
"""Compare two builds of the theme file by file: what was added, removed or changed. Standard library only.

    python3 tools/compare_builds.py OLD_THEME_DIR NEW_THEME_DIR [--quiet]

Use it before every release: a change to one icon should show only that icon (and anything that embeds it).
Exits 1 if anything differs, so `make check-build` can use it to prove the committed theme matches the source.
"""
import os, sys, hashlib
A, B = sys.argv[1], sys.argv[2]
QUIET = "--quiet" in sys.argv
def scan(root):
    out = {}
    for sub in ("scalable", "16x16", "22x22"):
        for dp, dn, fn in os.walk(os.path.join(root, sub)):
            for f in fn:
                p = os.path.join(dp, f); rel = os.path.relpath(p, root)
                out[rel] = ("link:" + os.readlink(p)) if os.path.islink(p) else hashlib.sha1(open(p, "rb").read()).hexdigest()
    out["index.theme"] = hashlib.sha1(open(os.path.join(root, "index.theme"), "rb").read()).hexdigest()
    return out
a, b = scan(A), scan(B)
added = sorted(set(b) - set(a)); removed = sorted(set(a) - set(b))
changed = sorted(k for k in set(a) & set(b) if a[k] != b[k])
print(f"before {len(a)} files, after {len(b)}: added {len(added)}, removed {len(removed)}, changed {len(changed)}")
if QUIET:
    sys.exit(1 if (added or removed or changed) else 0)
for k in removed: print("REMOVED", k)
for k in changed: print("CHANGED", k)
for k in added: print("  added", k, "->", b[k] if b[k].startswith("link:") else "drawing")

sys.exit(1 if (added or removed or changed) else 0)
