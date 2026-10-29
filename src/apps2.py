"""KDE Classic Vector: app icons reported falling back to Breeze after release - ISO Image Writer, KWatchGnuPG
(GnuPG log viewer) and LibreOffice (start centre, the six apps and LibreOffice's own document-type names).
Runs after updates, so it can embed and alias anything already built.
"""
import os
from gen import Icon, INK, LW


def _ic(fn):
    def f():
        ic = Icon()
        fn(ic)
        return ic
    return f


def iso_writer(ic):
    """ISO Image Writer: a disc image being written to the blue USB stick."""
    from pim import _embed
    from settingstrace import _teal, _arrow_pts, _poly
    _embed(ic, "application-x-cd-image", "translate(-4,-5) scale(.7)")
    # the stick was enlarged 1.55x on 2026-10-27; undo that here so this icon keeps its layout
    _embed(ic, "drive-removable-media-usb-pendrive", "translate(18,18) scale(.74) translate(33,34) scale(.64516) translate(-32,-33)")
    _teal(ic, _poly(_arrow_pts(38, 6, 56, 24, 3.6, 8.5, 9)))


def gnupg_log(ic):
    """GnuPG log viewer (KWatchGnuPG): the log viewer with the padlock."""
    from pim import _embed, _mini
    _embed(ic, "utilities-log-viewer", "translate(-2,-2) scale(.95)")
    _mini(ic, "object-locked", 36, 2, .4)


def kmag(ic):
    """KMag (screen magnifier): KDE Classic's magnifier held over a monitor."""
    from pim import _embed
    from actions import _magnifier
    _embed(ic, "video-display", "translate(-2,-2) scale(.9)")
    _magnifier(ic, 36, 30, 12, 10)


def _embed_icon(ic, other, tf):
    """Like pim._embed, for an Icon built here rather than one already written to the theme."""
    import re
    from pim import _n
    _n[0] += 1
    p = f"e{_n[0]}_"
    fix = lambda t: re.sub(r'url\(#([^)]+)\)', rf'url(#{p}\1)', re.sub(r'id="([^"]+)"', rf'id="{p}\1"', t))
    ic.defs += [fix(d) for d in other.defs]
    ic.add(f'<g transform="{tf}">' + "".join(fix(b) for b in other.body) + "</g>")


def _lo_doc(kind):
    """The app's document, without the file-type tag its mime icon carries (an app icon shouldn't say ODB)."""
    from filetypes import mime, m_formula, e_database, lines, TEXT
    if kind == "math":
        return mime(m_formula)()
    if kind == "base":
        return mime(e_database, lambda ic: lines(ic, 40, 52, 22, 8))()
    return None


def libreoffice(doc, tool):
    """LibreOffice apps: the app's document with its tool in front - so the app differs from its files."""
    def f(ic):
        from pim import _embed
        d = _lo_doc(doc)
        if d is None:
            _embed(ic, doc, "translate(-1,-2) scale(.82)")
        else:
            _embed_icon(ic, d, "translate(-1,-2) scale(.82)")
        _embed(ic, tool, "translate(27,25) scale(.57)")
    return f


def lo_start(ic):
    """LibreOffice start centre: the three main document kinds fanned out."""
    from pim import _embed
    for name, deg, x in (("x-office-presentation", -16, -14), ("x-office-spreadsheet", 0, 0), ("x-office-document", 16, 14)):
        _embed(ic, name, f"translate({x},4) rotate({deg} 32 44) translate(12.8,8) scale(.6)")


# ---------------------------------------------------------------- apps the community asked for (2026-10-26)
# Third-party logos (Firefox, mpv) are not copied: those launchers get a KDE Classic style picture of what the
# program does instead. Firefox is left out of the theme altogether (2026-10-27): a theme icon named "firefox"
# hides the logo Firefox installs, so its generic browser picture ships only as the optional add-on in
# addon-kit/generic-browser (see web_browser_window below).
def _window(ic, x, y, w, h):
    from gen import rrect
    ic.shadow(rrect(x, y, w, h, 2), 2.8, 2.4)
    ic.path(rrect(x, y, w, h, 2), ic.lg([(0, "#ffffff"), (1, "#c3c7cd")], 0, 0, 1, 1), INK, LW)
    ic.path(f"M{x + 1},{y + 1}H{x + w - 1}V{y + 8}H{x + 1}Z", ic.lg([(0, "#5a8ad8"), (1, "#1a3a8a")], 0, 0, 1, 0), None)
    ic.add(f'<path d="M{x},{y + 8.5}H{x + w}" stroke="{INK}" stroke-width="1"/>')


def ktorrent(ic):
    """KTorrent: a big blue download arrow plunging down into a splash, drops flying up either side."""
    pool = "M32,45A25,8 0 1 0 32.01,45Z"
    ic.shadow(pool, 2, 1.6)
    ic.path("M7,53A25,8 0 1 0 57,53A25,8 0 1 0 7,53Z", ic.lg([(0, "#d8f2ff"), (.5, "#5ab4ec"), (1, "#1a5ab0")], 0, 0, 0, 1), INK, 1.2)
    ic.path("M17,53A15,4.4 0 1 0 47,53A15,4.4 0 1 0 17,53Z", ic.lg([(0, "#1a5ab0"), (1, "#8fd0f4")], 0, 0, 0, 1), INK, .8)

    def drop(x, y, s, tilt):
        d = "M0,-6C1.5,-3 3.2,-1 3.2,1.4A3.2,3.2 0 1 1 -3.2,1.4C-3.2,-1 -1.5,-3 0,-6Z"
        ic.add(f'<g transform="translate({x},{y}) rotate({tilt}) scale({s},{-s})">')   # tail down: flying up
        ic.path(d, ic.lg([(0, "#ffffff"), (.5, "#7ac4f4"), (1, "#1a5ab0")], 0, 0, 1, 1), INK, 1 / s * .8)
        ic.add('<path d="M-1.4,0.4Q-1.4,-1.6 0,-3" fill="none" stroke="#fff" stroke-width=".7"/></g>')
    for x, y, s, t in ((8, 31, 1, -38), (17, 40, .75, -30), (56, 31, 1, 38), (47, 40, .75, 30)):
        drop(x, y, s, t)
    arrow = "M24,4H40V28H50L32,50L14,28H24Z"
    ic.shadow(arrow, 2.8, 2.4)
    ic.path(arrow, ic.lg([(0, "#bfe6ff"), (.45, "#3d8ee0"), (1, "#0e3a8a")], 0, 0, 1, 1), INK, LW)
    ic.add('<path d="M26.5,7V30" stroke="#fff" stroke-opacity=".75" stroke-width="1.6" stroke-linecap="round"/>')


def gwenview(ic):
    """Gwenview (image viewer): a simple eye in KDE Classic's style - white almond, blue iris, black pupil."""
    from gen import circle
    eye = "M3,32Q32,4 61,32Q32,60 3,32Z"
    ic.shadow(eye, 2.6, 2.2)
    ic.path(eye, ic.rg([(0, "#ffffff"), (.7, "#eef0f2"), (1, "#a8aeb6")], .5, .5, .55), INK, LW)
    ic.add('<clipPath id="gwv"><path d="M3,32Q32,4 61,32Q32,60 3,32Z"/></clipPath><g clip-path="url(#gwv)">')
    ic.path(circle(32, 32, 14), ic.rg([(0, "#bfe4ff"), (.55, "#2a7ad8"), (1, "#0a2a6a")], .42, .38, .7), INK, 1.4)
    ic.path(circle(32, 32, 6.2), ic.rg([(0, "#3a3f46"), (1, "#000000")], .4, .35, .8), None)
    ic.add('<path d="M3,32Q32,4 61,32" fill="none" stroke="#5a6068" stroke-opacity=".35" stroke-width="4"/></g>')
    ic.path(circle(27.5, 27, 2.8), "#ffffff", None, 0, ' fill-opacity=".9"')
    ic.path(circle(36.5, 37, 1.3), "#ffffff", None, 0, ' fill-opacity=".6"')
    ic.add('<path d="M3,32Q32,4 61,32" fill="none" stroke="%s" stroke-width="3" stroke-linecap="round"/>' % INK)


def kid3(ic):
    """Kid3 (audio tag editor): KDE Classic's loudspeaker with a wide yellow tag tied on, a note and a scribbled
    line written on the tag."""
    from gen import e_speaker, circle
    from elisa import _note
    ic.add('<g transform="rotate(-14 26 26)">')
    e_speaker(ic, cx=30, cy=25, ry=21)
    ic.add("</g>")
    ic.add('<g transform="translate(36,44) rotate(-28) scale(.8) translate(-24,-12)">')
    t = "M0,12L12,0H48V24H12Z"
    ic.shadow(t, 2.4, 2)
    ic.path(t, ic.lg([(0, "#fff8b0"), (.5, "#f4d020"), (1, "#b88a04")], 0, 0, 1, 1), INK, LW)
    ic.add('<path d="M13,2H46" stroke="#fff" stroke-opacity=".7" stroke-width="1"/>')
    ic.path(circle(9, 12, 2.6), "#ffffff", INK, 1)
    ic.add('<path d="M9,12C2,10 -2,4 4,-2" fill="none" stroke="#7b818a" stroke-width="1.2"/>')   # the string
    _note(ic, 20, 18, .34)
    ic.add('<path d="M27,9Q29,6 31,9T35,9T39,9T43,9M27,17Q29,14 31,17T35,17T38,16" fill="none" stroke="#1a3a8a" '
           'stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/>')   # handwriting
    ic.add("</g>")


def qdbusviewer(ic):
    """QDBusViewer (D-Bus Viewer): "DV" in a green box with two chamfered corners."""
    box = "M14,4H58V48L46,60H6V16Z"
    ic.shadow(box, 3, 2.6)
    ic.path(box, ic.lg([(0, "#b8f0a0"), (.45, "#3cae3a"), (1, "#0e5a10")], 0, 0, 1, 1), INK, LW)
    ic.add('<path d="M15,6.5H55.5" stroke="#fff" stroke-opacity=".7" stroke-width="1.6"/>')
    ic.add('<path d="M8.5,17V57" stroke="#fff" stroke-opacity=".3" stroke-width="1.2"/>')
    letters = "M13,20V44H19C27,44 30,38 30,32C30,26 27,20 19,20Z M34,20L42,44L50,20"
    ic.add(f'<path d="{letters}" fill="none" stroke="{INK}" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"/>')
    ic.add(f'<path d="{letters}" fill="none" stroke="#ffffff" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"/>')


def terminal_su(ic):
    """Root terminal: Konsole's monitor (without the seashell) with KDE Classic's padlock."""
    from pim import _embed
    from uitrace import terminal_monitor
    terminal_monitor(ic)
    _embed(ic, "object-locked", "translate(32,30) scale(.5)")


def web_browser_window(ic):
    """A web browser: the KDE Classic globe in a browser window. Not in the theme; it is the icon of the optional
    generic-browser add-on (addon-kit/generic-browser), which replaces Firefox's own logo."""
    from gen import e_globe
    _window(ic, 4, 6, 54, 48)
    e_globe(ic, 17, 18, 15)


def video_player(ic):
    """mpv: a purple play button in KDE Classic's style."""
    from gen import circle
    ic.shadow(circle(31, 31, 27), 3, 2.6)
    ic.path(circle(31, 31, 27), ic.rg([(0, "#f0d0ff"), (.45, "#9a4ad8"), (1, "#3a0a6a")], .38, .32, .8), INK, LW)
    ic.path(circle(31, 31, 21.5), ic.rg([(0, "#d8a8f8"), (.6, "#7a2ab8"), (1, "#4a127a")], .4, .35, .8), INK, 1)
    ic.add('<path d="M14,22Q22,8 40,9" fill="none" stroke="#fff" stroke-opacity=".7" stroke-width="2.2" stroke-linecap="round"/>')
    ic.path("M24,17V45L46,31Z", ic.lg([(0, "#ffffff"), (1, "#d8d0e8")], 0, 0, 1, 1), INK, 1.4)


# gwenview: the drawn eye (gwenview() above) is kept on record; the theme now installs the supplied SVG instead
# (SUPPLIED below, 2026-10-27).
COMMUNITY = {"ktorrent": ktorrent, "kid3": kid3, "qdbusviewer": qdbusviewer,
             "utilities-terminal_su": terminal_su, "mpv": video_player}
COMMUNITY_ALIASES = {"org.kde.ktorrent": "ktorrent", "org.kde.gwenview": "gwenview", "kid3-qt": "kid3", "org.kde.kid3": "kid3",
                     "kid3-cli": "kid3", "qdbusviewer6": "qdbusviewer", "qdbusviewer-qt6": "qdbusviewer",
                     "utilities-terminal-su": "utilities-terminal_su", "konsole-su": "utilities-terminal_su",
                     "io.mpv.Mpv": "mpv", "mpv-icon": "mpv"}


LO_APPS = {"writer": ("x-office-document", "draw-freehand"), "calc": ("x-office-spreadsheet", "office-chart-pie"),
           "impress": ("x-office-presentation", "view-presentation"), "draw": ("x-office-drawing", "draw-brush"),
           "base": ("base", "edit-find"), "math": ("math", "accessories-calculator")}
A2 = {"apps": {"org.kde.isoimagewriter": iso_writer, "kwatchgnupg": gnupg_log, "kmag": kmag,
               "libreoffice-startcenter": lo_start}}
for _app, (_doc, _tool) in LO_APPS.items():
    A2["apps"]["libreoffice-" + _app] = libreoffice(_doc, _tool)
A2["apps"].update(COMMUNITY)
from classicapps import CLASSIC_APPS, CLASSIC_ALIASES
A2["apps"].update(CLASSIC_APPS)

LO = {app: "apps/libreoffice-" + app for app in LO_APPS}
LO["startcenter"] = LO["main"] = "apps/libreoffice-startcenter"
A2_ALIASES = {"isoimagewriter": "apps/org.kde.isoimagewriter", "org.kde.kwatchgnupg": "apps/kwatchgnupg",
              # Elementary Configuration (EFL toolkit settings, elementary_config.desktop: Icon=elementary)
              "org.kde.kmag": "apps/kmag", "kmag-symbolic": "apps/kmag", "elementary": "configure", "elementary_config": "configure", "elementary-config": "configure",
              # KIO's Create New > Empty File template asks for Icon=none (kio/src/new_file_templates/EmptyFile.desktop);
              # nothing else in the swept KDE sources uses that name. Show the theme's blank page (2026-10-27).
              "none": "application-x-zerosize"}
for a, t in COMMUNITY_ALIASES.items():
    A2_ALIASES[a] = "apps/" + t
A2_ALIASES.update(CLASSIC_ALIASES)
for app, target in LO.items():
    for prefix in ("libreoffice-", "libreoffice6.4-", "libreoffice7.0-", "libreoffice24.2-", "libreoffice25.2-"):
        if prefix + app != target.split("/")[1]:
            A2_ALIASES[prefix + app] = target
# LibreOffice's own document-type icon names (its mime packages use these)
for kind, target in {"oasis-text": "x-office-document", "oasis-spreadsheet": "x-office-spreadsheet",
                     "oasis-presentation": "x-office-presentation", "oasis-drawing": "x-office-drawing",
                     "oasis-formula": "application-vnd.oasis.opendocument.formula",
                     "oasis-database": "application-vnd.oasis.opendocument.database",
                     "oasis-master-document": "x-office-document", "oasis-text-template": "x-office-document-template",
                     "oasis-spreadsheet-template": "x-office-spreadsheet-template",
                     "oasis-presentation-template": "x-office-presentation-template",
                     "oasis-drawing-template": "x-office-drawing", "oasis-web-template": "text-html",
                     "text": "x-office-document", "spreadsheet": "x-office-spreadsheet",
                     "presentation": "x-office-presentation", "drawing": "x-office-drawing",
                     "formula": "application-vnd.oasis.opendocument.formula", "database": "application-vnd.oasis.opendocument.database",
                     "master-document": "x-office-document", "extension": "package-x-generic",
                     "ms-word": "x-office-document", "ms-excel": "x-office-spreadsheet", "ms-powerpoint": "x-office-presentation"}.items():
    A2_ALIASES["libreoffice-" + kind] = target


def _find(out, name):
    for ctx in os.listdir(f"{out}/scalable"):
        if os.path.lexists(f"{out}/scalable/{ctx}/{name}.svg"):
            return ctx
    return None


# ---------------------------------------------------------------- Share (document-share), 2026-10-27
# The Share menu/button (Purpose: send to KDE Connect, email, Imgur ...) used KDE Classic's plug, which means
# "shared on the network" and stays on emblem-shared / emblem-share for shared folders.
def share_nodes(ic):
    """The general 'share' sign: three glossy teal balls joined by links (option B; kept on record and in
    alt/document-share-nodes.svg in case D does not read well)."""
    from gen import circle
    pts = [(46, 12), (16, 32), (46, 52)]
    for (ax, ay), (bx, by) in ((pts[1], pts[0]), (pts[1], pts[2])):
        ic.add(f'<path d="M{ax},{ay}L{bx},{by}" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>'
               f'<path d="M{ax},{ay}L{bx},{by}" stroke="#10a8c8" stroke-width="4" stroke-linecap="round"/>')
    for x, y in pts:
        ic.shadow(circle(x, y, 9), 2, 1.7)
        ic.path(circle(x, y, 9), ic.rg([(0, "#ffffff"), (.45, "#7ad8f0"), (1, "#0a5a78")], .38, .32, .8), INK, LW)


def share_document(ic):
    """Share (option D): the document page with the share nodes laid over its lower right."""
    from pim import _embed
    _embed(ic, "text-plain", "translate(-6,-2) scale(.95)")
    ic.add('<g transform="translate(27,25) scale(.66) translate(-7,-3)">')
    share_nodes(ic)
    ic.add("</g>")


A2["actions"] = {"document-share": share_document}
A2_ALIASES["document-share-symbolic"] = "actions/document-share"
# At 16 and 22 px (menus, toolbars) the page leaves the nodes too small, so those sizes show the nodes alone.
SMALL = {"actions": {"document-share": share_nodes}}
SMALL_ALIASES = {"actions": {"document-share-symbolic": "document-share"}}


# Finished SVGs supplied by the author, copied in as they are (see supplied/README.md).
SUPPLIED = {"apps": {"gwenview": "supplied/gwenview.svg"}}


def write(out):
    import pim, shutil
    pim.OUT = out
    n = 0
    here = os.path.dirname(os.path.abspath(__file__))
    for ctx, files in SUPPLIED.items():
        for name, rel in files.items():
            p = f"{out}/scalable/{ctx}/{name}.svg"
            if os.path.lexists(p):
                os.remove(p)
            shutil.copyfile(os.path.join(here, rel), p)
            n += 1
    for ctx, icons in A2.items():
        for name, fn in icons.items():
            p = f"{out}/scalable/{ctx}/{name}.svg"
            if os.path.lexists(p):
                os.remove(p)
            open(p, "w").write(_ic(fn)().svg(64))
            n += 1
    missing = []
    for a, t in A2_ALIASES.items():
        ctx, name = t.split("/") if "/" in t else (_find(out, t), t)
        if ctx is None or not os.path.exists(f"{out}/scalable/{ctx}/{name}.svg"):
            missing.append(t)
            continue
        if _find(out, a) is None:
            os.symlink(f"{name}.svg", f"{out}/scalable/{ctx}/{a}.svg")
    for size in (16, 22):
        for ctx, icons in SMALL.items():
            d = f"{out}/{size}x{size}/{ctx}"
            os.makedirs(d, exist_ok=True)
            for name, fn in icons.items():
                if os.path.lexists(f"{d}/{name}.svg"):
                    os.remove(f"{d}/{name}.svg")
                open(f"{d}/{name}.svg", "w").write(_ic(fn)().svg(size))
                n += 1
            for a, t in SMALL_ALIASES.get(ctx, {}).items():
                if not os.path.lexists(f"{d}/{a}.svg"):
                    os.symlink(f"{t}.svg", f"{d}/{a}.svg")
    if missing:
        print("apps2: alias targets missing:", missing)
    return n
