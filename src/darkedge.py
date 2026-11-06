"""KDE Classic Vector: a white edge round icons drawn mostly in black, so they still show on dark colour schemes and
black backgrounds (2026-11-06). Runs last in the build and rewrites the listed drawings in place: a white copy of
each drawing, every shape widened by 2.6 units, goes underneath it. On light backgrounds the edge disappears into
the background, so they look as before. Chosen icon by icon with the author; see docs/ROADMAP.md.
"""
import os
import re

HALO = [
    "format-text-underline-squiggle", "format-text-strikethrough", "format-text-subscript",
    "format-text-direction-ltr", "format-text-direction-rtl",
    "draw-text", "percent", "edit-line-width", "code-block", "code-context",
    "view-sort", "view-sort-descending", "sort-name", "handle-sort", "help-whatsthis",
]

SHAPES = r"<(path|circle|rect|ellipse|polygon|polyline|line|use)\b([^>]*?)(/?)>"


def _halo_el(m, extra):
    tag, attrs, close = m.group(1), m.group(2), m.group(3)
    op = re.search(r'\b(fill-opacity|opacity)="([\d.]+)"', attrs)
    if op and float(op.group(2)) < .5:
        return ""                                     # drop soft shadows from the halo
    fill = re.search(r'\bfill="([^"]*)"', attrs)
    sw = re.search(r'\bstroke-width="([\d.]+)"', attrs)
    stroke = re.search(r'\bstroke="([^"]*)"', attrs)
    w = (float(sw.group(1)) if sw and stroke and stroke.group(1) != "none" else 0) + extra
    a = re.sub(r'\s(fill|stroke|stroke-width|fill-opacity|stroke-opacity|opacity|stroke-linejoin|stroke-dasharray)="[^"]*"', "", attrs)
    f = "none" if fill and fill.group(1) == "none" else "#fff"
    return f'<{tag}{a} fill="{f}" stroke="#fff" stroke-width="{w:.2f}" stroke-linejoin="round"{" /" if close else ""}>'


def halo_body(body, extra=2.6):
    """A white copy of the drawing, every shape widened by `extra`, to draw underneath it: a white edge all round."""
    return re.sub(SHAPES, lambda m: _halo_el(m, extra), body)


def halo_svg(svg, extra=2.6):
    i = svg.index("</defs>") + len("</defs>")
    j = svg.rindex("</svg>")
    body = svg[i:j]
    return svg[:i] + f'<g>{halo_body(body, extra)}</g>' + body + svg[j:]


def write(out):
    for name in HALO:
        done = 0
        for sub in ("scalable", "16x16", "22x22"):
            for ctx in ("actions", "status", "apps", "places", "mimetypes", "devices", "categories", "emblems"):
                p = f"{out}/{sub}/{ctx}/{name}.svg"
                if os.path.isfile(p) and not os.path.islink(p):
                    s = open(p).read()
                    open(p, "w").write(halo_svg(s))
                    done += 1
        if not done:
            print(f"darkedge: no drawing named {name}")
