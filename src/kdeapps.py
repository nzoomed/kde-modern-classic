"""KDE Classic Vector: names found by sweeping the source of Plasma, Dolphin, KIO, the KDE Frameworks, Gwenview,
Ark and Spectacle for every icon they ask for. Most map onto drawings already in the set; the rest
(tags, double arrows, fill and stroke colour, text direction, charts, selection, package states, the
Gwenview app icon ...) are drawn here. Runs last, so its aliases can point anywhere.
"""
import math, os
from gen import Icon, INK, LW, circle, rrect
from actions import _mpath
from settingstrace import _teal, _arrow_pts, _badge, _ok, _no, _poly


def _ic(fn):
    def f():
        ic = Icon()
        fn(ic)
        return ic
    return f


# ------------------------------------------------------------------ tags
def _tag(ic, s=1.0, dx=0, dy=0):
    """The yellow luggage tag with its punched hole in the top left corner."""
    ic.add(f'<g transform="translate({dx},{dy}) scale({s}) translate(56,0) scale(-1,1)">')
    t = "M6,22L22,6H50V34L34,50Z"
    ic.shadow(t, 2.4, 2)
    ic.path(t, ic.lg([(0, "#fffbd0"), (.5, "#ffe050"), (1, "#c89a10")], 0, 0, 1, 1), INK, LW / s)
    ic.path(circle(41, 15, 3.2), "#ffffff", INK, 1.1)
    ic.add("</g>")


def tag(ic):
    """Tag: the yellow luggage tag, moved to fill the canvas."""
    _tag(ic, 1.12, 2, 6)


def mail_tagged(ic):
    """Tagged mail: the plain envelope with the yellow tag tied on."""
    from desktoptrace import _envelope
    _envelope(ic, 2, 6, 48, 34)
    _tag(ic, .62, 28, 28)


# ------------------------------------------------------------------ Gwenview
MAGENTA = [(0, "#ffb8ee"), (.4, "#e82ac0"), (1, "#7a0660")]


def gwenview_kview(ic):
    """Alternative kept on record: KDE Classic's KView-style image viewer (sheet, magnifier, cup of brushes)."""
    ic.add('<g transform="rotate(-24 32 30)">')
    sheet = "M12,8H44L52,16V56H12Z"
    ic.shadow(sheet, 2.4, 2)
    ic.path(sheet, ic.lg([(0, "#ffffff"), (.6, "#f6f2ea"), (1, "#cfc6b4")], 0, 0, 1, 1), INK, LW)
    ic.path("M44,8V16H52", "#e4ddd0", INK, 1)
    ic.add("</g>")
    for x, top, c in ((43, 30, "#2a6ac8"), (48, 27, "#3fae2a"), (53, 31, "#e8c43a"), (57, 34, "#e0281a")):
        d = f"M{x - 2.2},{top + 5}Q{x},{top - 4} {x + 2.2},{top + 5}V48H{x - 2.2}Z"
        ic.path(d, ic.lg([(0, "#ffffff"), (.4, c), (1, c)], 0, 0, 1, 0), INK, 1)
    cup = "M39,44H61L59,62H41Z"
    ic.shadow(cup, 2, 1.7)
    ic.path(cup, ic.lg([(0, "#5c6168"), (.3, "#ffffff"), (.6, "#c3c7cd"), (1, "#4c5158")], 0, 0, 1, 0), INK, LW)
    ic.path("M39,44H61V47H39Z", ic.lg([(0, "#ffffff"), (1, "#8a9098")], 0, 0, 0, 1), INK, 1)
    from actions import _magnifier
    ic.add('<g transform="translate(56,0) scale(-1,1)">')
    _magnifier(ic, 28, 27, 14, 13)
    ic.add("</g>")


def gwenview(ic):
    """Gwenview: its classic eye - magenta lids sweeping round a dark camera-lens iris, redrawn in the
    theme's style (bold outline, glossy gradients, top-left light)."""
    white = "M4,33Q22,7 59,9Q57,43 34,51Q14,50 4,33Z"
    ic.path(white, ic.lg([(0, "#ffffff"), (.55, "#e6eef8"), (1, "#9ab8e0")], 0, 0, 1, 1), INK, LW)
    # the lens
    cx, cy = 33, 30
    ic.shadow(circle(cx, cy, 17), 2, 1.7)
    ic.path(circle(cx, cy, 17), ic.lg([(0, "#8a9098"), (.45, "#2a2e33"), (1, "#050607")], 0, 0, 1, 1), INK, LW)
    ic.path(circle(cx, cy, 13), ic.rg([(0, "#40524a"), (.6, "#121a17"), (1, "#020303")], .5, .55, .7), INK, 1)
    ic.add(f'<path d="M{cx - 10},{cy + 5}Q{cx - 4},{cy + 13} {cx + 6},{cy + 12}Q{cx + 11},{cy + 9} {cx + 12},{cy + 4}Q{cx + 6},{cy + 10} {cx - 1},{cy + 10}Q{cx - 6},{cy + 9} {cx - 10},{cy + 5}Z" fill="#3ad08a" fill-opacity=".75"/>'
           f'<path d="M{cx + 4},{cy + 9}Q{cx + 9},{cy + 7} {cx + 11},{cy + 2}Q{cx + 10},{cy + 7} {cx + 4},{cy + 9}Z" fill="#f0c040" fill-opacity=".8"/>'
           f'<path d="M{cx + 6},{cy - 9}Q{cx + 12},{cy - 5} {cx + 12},{cy + 1}Q{cx + 9},{cy - 5} {cx + 4},{cy - 7}Z" fill="#58c8f0" fill-opacity=".65"/>')
    ic.path(circle(cx, cy, 5), "#000000", None)
    ic.add(f'<path d="M{cx - 10},{cy - 2}Q{cx - 9},{cy - 10} {cx - 1},{cy - 11}Q{cx - 5},{cy - 7} {cx - 6},{cy - 1}Z" fill="#ffffff" fill-opacity=".9"/>'
           f'<path d="M{cx - 4},{cy + 3}a1.7,1.7 0 1,0 .01,0" fill="#ffffff" fill-opacity=".7"/>')
    # magenta lids
    upper = "M1,35C1,13 27,0 63,3C44,8 24,16 12,39Q3,43 1,35Z"
    lower = "M9,45C24,57 45,56 63,44C51,62 24,66 7,55Q4,47 9,45Z"
    for d in (upper, lower):
        ic.shadow(d, 2.2, 1.8)
        ic.path(d, ic.lg(MAGENTA, 0, 0, .3, 1), INK, LW)
    ic.add('<path d="M5,31Q10,13 34,6" fill="none" stroke="#fff" stroke-opacity=".75" stroke-width="1.8" stroke-linecap="round"/>'
           '<path d="M14,52Q30,59 50,54" fill="none" stroke="#fff" stroke-opacity=".55" stroke-width="1.4" stroke-linecap="round"/>')


# ------------------------------------------------------------------ double arrows (date picker, scrolling)
def _chevrons(ic, rot):
    ic.add(f'<g transform="rotate({rot} 32 32)">')
    for x in (4, 26):
        _teal(ic, f"M{x},32L{x + 18},12H{x + 31}L{x + 13},32L{x + 31},52H{x + 18}Z")
    ic.add("</g>")


def arrow_left_double(ic):  _chevrons(ic, 0)
def arrow_up_double(ic):    _chevrons(ic, 90)
def arrow_right_double(ic): _chevrons(ic, 180)
def arrow_down_double(ic):  _chevrons(ic, 270)


# ------------------------------------------------------------------ colours and text formatting
def _colour_bar(ic, col="#e0281a"):
    ic.path("M4,52H60V61H4Z", ic.lg([(0, "#ffffff"), (.3, col), (1, col)], 0, 0, 0, 1), INK, LW)


def format_fill_color(ic):
    """Fill colour: a tipped paint tin pouring red paint, over a red colour bar."""
    ic.add('<g transform="rotate(-30 26 26)">')
    body = "M10,14H40V40Q40,44 36,44H14Q10,44 10,40Z"
    ic.shadow(body, 2.4, 2)
    ic.path(body, ic.lg([(0, "#5c6168"), (.3, "#ffffff"), (.6, "#c3c7cd"), (1, "#4c5158")], 0, 0, 1, 0), INK, LW)
    ic.path("M10,14Q25,9 40,14Q25,19 10,14Z", "#e0281a", INK, 1.2)
    ic.add(f'<path d="M12,14Q12,0 25,2Q38,0 38,14" fill="none" stroke="{INK}" stroke-width="2.2"/>')
    ic.add("</g>")
    drip = "M44,24Q52,30 52,40Q52,46 47,46Q42,46 42,40Q42,32 44,24Z"
    ic.path(drip, ic.lg([(0, "#ffb0a0"), (.45, "#e0281a"), (1, "#7a0804")], 0, 0, 1, 0), INK, 1.2)
    _colour_bar(ic)


def format_stroke_color(ic):
    """Stroke colour: the orange pencil drawing a line, over a red colour bar."""
    from uitrace import _pencil
    _pencil(ic, "translate(46,4) rotate(40 6 26) scale(.86)")
    ic.add(f'<path d="M6,44Q16,30 26,38T44,40" fill="none" stroke="{INK}" stroke-width="4.4" stroke-linecap="round"/>'
           f'<path d="M6,44Q16,30 26,38T44,40" fill="none" stroke="#e0281a" stroke-width="2.4" stroke-linecap="round"/>')
    _colour_bar(ic)


def _pilcrow(ic, x):
    p = (f"M{x + 10},4H{x + 30}V9H{x + 26}V40H{x + 21}V9H{x + 17}V40H{x + 12}V24Q{x},24 {x},14Q{x},4 {x + 10},4Z")
    ic.shadow(p, 2, 1.7)
    ic.path(p, ic.lg([(0, "#5c6168"), (1, "#141414")], 0, 0, 1, 1), INK, 1)


def format_text_direction_ltr(ic):
    """Left-to-right text: the paragraph mark with a teal arrow pointing right underneath."""
    _pilcrow(ic, 16)
    _teal(ic, _poly(_arrow_pts(6, 51, 60, 51, 4, 10, 12)))


def format_text_direction_rtl(ic):
    _pilcrow(ic, 18)
    _teal(ic, _poly(_arrow_pts(58, 51, 4, 51, 4, 10, 12)))


def insert_horizontal_rule(ic):
    """Horizontal rule: a page of text cut across by a bold grey rule."""
    from actions import _page
    _page(ic, 8, 2, 46, 60, lines=False)
    for y in (12, 17, 22, 42, 47, 52):
        ic.add(f'<path d="M13,{y}H{46 - (y % 3) * 4}" stroke="#3c4148" stroke-width="1.6" stroke-dasharray="3 1.2"/>')
    ic.path("M4,29H58V35H4Z", ic.lg([(0, "#ffffff"), (.4, "#a8adb4"), (1, "#4c5158")], 0, 0, 0, 1), INK, LW)


# ------------------------------------------------------------------ charts
def _axes(ic):
    ic.path("M4,4H60V60H4Z", ic.lg([(0, "#ffffff"), (1, "#dfe2e6")], 0, 0, 1, 1), INK, LW)
    for y in (16, 28, 40):
        ic.add(f'<path d="M8,{y}H56" stroke="#b4b9c0" stroke-width="1"/>')
    ic.add(f'<path d="M10,8V54H58" fill="none" stroke="{INK}" stroke-width="2"/>')


def office_chart_bar(ic):
    """Bar chart: four glossy bars in the theme's band colours."""
    _axes(ic)
    for x, h, c in ((14, 22, "#3d9ad8"), (25, 36, "#4fae5a"), (36, 16, "#e8c43a"), (47, 30, "#d8573d")):
        d = f"M{x},{54 - h}H{x + 8}V54H{x}Z"
        ic.path(d, ic.lg([(0, "#ffffff"), (.35, c), (1, c)], 0, 0, 1, 0), INK, 1.2)


def office_chart_line(ic):
    """Line chart: a red line through dotted data points."""
    _axes(ic)
    pts = ((14, 44), (24, 30), (34, 36), (44, 18), (54, 24))
    d = "M" + "L".join(f"{x},{y}" for x, y in pts)
    ic.add(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="4.6" stroke-linejoin="round"/>'
           f'<path d="{d}" fill="none" stroke="#e0281a" stroke-width="2.6" stroke-linejoin="round"/>')
    for x, y in pts:
        ic.path(circle(x, y, 2.8), "#ffffff", INK, 1.2)


# ------------------------------------------------------------------ selection
def select_rectangular(ic):
    """Rectangular selection: a dashed marquee with square handles at the corners."""
    ic.add('<path d="M8,10H56V54H8Z" fill="#3d9ad8" fill-opacity=".14" stroke="#fff" stroke-width="2.4"/>'
           f'<path d="M8,10H56V54H8Z" fill="none" stroke="{INK}" stroke-width="2.4" stroke-dasharray="5 3"/>')
    for x, y in ((8, 10), (56, 10), (8, 54), (56, 54)):
        ic.path(f"M{x - 4},{y - 4}H{x + 4}V{y + 4}H{x - 4}Z", ic.lg([(0, "#ffffff"), (1, "#9aa0a8")], 0, 0, 1, 1), INK, 1.2)


# ------------------------------------------------------------------ package states (Get New Stuff)
def _small_parcel(ic):
    from discover import parcel
    ic.add('<g transform="translate(0,4) scale(.9)">')
    parcel(ic)
    ic.add("</g>")


def package_installed_updated(ic):
    _small_parcel(ic)
    _ok(ic, 48, 48, 12)


def package_installed_outdated(ic):
    _small_parcel(ic)
    _badge(ic, 48, 48, 12, "amber", "M48,54V42M43,47L48,42L53,47")


# ------------------------------------------------------------------ odds and ends
def sim_missing(ic):
    """SIM missing: the little card with a red cross."""
    from devices import memory_card
    ic.add('<g transform="translate(2,0) scale(.9)">')
    memory_card(ic)
    ic.add("</g>")
    _no(ic, 48, 48, 12)


def thermometer(ic):
    """Temperature: a glass thermometer with a red column and bulb, and a scale beside it."""
    tube = "M24,10Q24,4 30,4Q36,4 36,10V40A11,11 0 1 1 24,40Z"
    ic.shadow(tube, 2.4, 2)
    ic.path(tube, ic.lg([(0, "#ffffff"), (.5, "#eef6fa"), (1, "#b4c4cc")], 0, 0, 1, 0), INK, LW)
    ic.path("M28,24H32V44H28Z", ic.lg([(0, "#ff8a7a"), (1, "#c0180a")], 0, 0, 1, 0), None)
    ic.path(circle(30, 49, 7.4), ic.rg([(0, "#ffb0a0"), (.5, "#e0281a"), (1, "#7a0804")], .38, .32, .8), INK, 1)
    for k, y in enumerate(range(10, 40, 5)):
        ic.add(f'<path d="M38,{y}H{44 if k % 2 == 0 else 41}" stroke="{INK}" stroke-width="1.4"/>')
    ic.add('<path d="M26.4,10V38" stroke="#fff" stroke-width="1.6" stroke-linecap="round"/>')


def exchange_positions(ic):
    """Exchange positions (Konsole's Switch Profile): two teal arrows passing each other, top one right,
    bottom one left."""
    _teal(ic, _poly(_arrow_pts(4, 20, 60, 20, 5.5, 13, 15)))
    _teal(ic, _poly(_arrow_pts(60, 44, 4, 44, 5.5, 13, 15)))


KA = {
    "actions": {"tag": tag, "arrow-left-double": arrow_left_double, "arrow-right-double": arrow_right_double,
                "arrow-up-double": arrow_up_double, "arrow-down-double": arrow_down_double,
                "format-fill-color": format_fill_color, "format-stroke-color": format_stroke_color,
                "format-text-direction-ltr": format_text_direction_ltr, "format-text-direction-rtl": format_text_direction_rtl,
                "insert-horizontal-rule": insert_horizontal_rule, "select-rectangular": select_rectangular,
                "office-chart-bar": office_chart_bar, "exchange-positions": exchange_positions, "office-chart-line": office_chart_line},
    "status": {"mail-tagged": mail_tagged, "package-installed-updated": package_installed_updated,
               "package-installed-outdated": package_installed_outdated, "auth-sim-missing": sim_missing,
               "temperature-normal": thermometer},
    # Gwenview's app icon is left to Breeze for now: both drafts (gwenview = Oxygen eye, gwenview_kview =
    # KDE Classic sheet + magnifier) are kept here for the revision pass - see ROADMAP.md.
}

KA_ALIASES = {
    # drawn above
    "tag-symbolic": "actions/tag", "tag-people": "actions/tag", 
    "fill-color": "actions/format-fill-color", "color-fill": "actions/format-fill-color",
    "region": "actions/select-rectangular", "select-rectangular-symbolic": "actions/select-rectangular",
    "office-chart-bar-symbolic": "actions/office-chart-bar", "office-chart-line-symbolic": "actions/office-chart-line",
    "temperature-normal-symbolic": "status/temperature-normal", "auth-sim-missing-symbolic": "status/auth-sim-missing",
    # -symbolic names of icons already in the set
    "draw-number-symbolic": "draw-number", "folder-documents-symbolic": "folder-documents", "viewimage-symbolic": "viewimage",
    "offline-symbolic": "offline", "edit-comment-symbolic": "edit-comment",
    "preferences-desktop-display-randr-symbolic": "preferences-desktop-display-randr", "edit-entry-symbolic": "edit-entry",
    "system-run-symbolic": "system-run", "mail-send-symbolic": "mail-send", "view-more-horizontal-symbolic": "view-more-horizontal",
    "view-process-system-symbolic": "view-process-system", "delete-symbolic": "delete", "plasma-symbolic": "plasma",
    "info-symbolic": "info", "edit-none-symbolic": "edit-none", "input-touchscreen-symbolic": "input-touchscreen",
    "input-keyboard-virtual-off-symbolic": "input-keyboard-virtual-off", "preferences-security-symbolic": "preferences-security",
    "edit-select-none-symbolic": "edit-select-none", "code-class-symbolic": "code-class",
    # same meaning as an existing drawing
    "go-first-view": "go-first", "go-last-view": "go-last", "go-jump-today": "view-calendar-day",
    "restoration": "edit-undo", "image-navigator-symbolic": "zoom-fit-best", "document-preview-archive": "view-preview",
    "sidebar-show-symbolic": "view-split-left-right", "document-scan": "scanner", "help-hint": "hint",
    "hide_table_row": "view-hidden", "quickwizard": "checkbox", "followmouse": "transform-browse",
    "table": "x-office-spreadsheet", "baloo": "preferences-desktop-search", "kfind": "system-search",
    "filelight": "office-chart-pie", "sweeper": "edit-clear-history", "krdc": "krfb",
    "insert-link": "edit-link", "bookmark-new-list": "bookmark-new", "open-for-editing": "document-edit", "text-wiki": "text-html",
    "package-available": "package-x-generic", "upload-media": "document-export",
    "filename-divider": "distribute-horizontal", "distribute-horizontal-margin": "distribute-horizontal",
    "input-keyboard-virtual-show-symbolic": "input-keyboard-virtual", "input-keyboard-virtual-hide-symbolic": "input-keyboard-virtual-off",
    "languages-symbolic": "preferences-desktop-locale", "lighttable": "redshift-status-on", "question": "dialog-question",
    "image-invert-symbolic": "contrast", "view-readermode": "text-plain", "text-speak": "preferences-desktop-text-to-speech",
    "input-mouse-click-middle": "input-mouse", "input-mouse-click-right": "input-mouse",
    "dialog-messages": "dialog-question", "filter-symbolic": "view-filter", "paper-color": "preferences-desktop-color",
    "paper-color-symbolic": "preferences-desktop-color", "task-process-1-symbolic": "process-working",
    "folder-activities": "activities", "phone-apple-iphone": "smartphone",
    "preferences-system-network-share-windows": "network-workgroup", "data-success": "dialog-ok",
    "edit-clear-list": "edit-clear-all", "user-properties": "user-identity",
    "accessories-dictionary": "help-contents", "accessories-dictionary-symbolic": "help-contents",
    "folder-comic-symbolic": "folder-image", "insert-image": "image-x-generic", "insert-image-symbolic": "image-x-generic",
    "kalarm": "chronometer", "preferences-web-browser-shortcuts": "internet-web-browser", "preferences-plugin": "plugins",
    "tab-duplicate": "tab-new", "preferences-tabs": "tab-new", "kcolorchooser": "preferences-desktop-color",
    "exchange-positions-symbolic": "actions/exchange-positions", "mail-message-new-list": "mail-message-new", "view-conversation-balloon": "mail-message",
    "preferences-desktop-screensaver": "preferences-desktop-display", "dialog-input-devices": "input-keyboard",
}


def _find(out, name):
    for ctx in os.listdir(f"{out}/scalable"):
        if os.path.lexists(f"{out}/scalable/{ctx}/{name}.svg"):
            return ctx
    return None


def write(out):
    n = 0
    for ctx, icons in KA.items():
        d = f"{out}/scalable/{ctx}"
        os.makedirs(d, exist_ok=True)
        for name, fn in icons.items():
            open(f"{d}/{name}.svg", "w").write(_ic(fn)().svg(64))
            n += 1
    missing = []
    for a, t in KA_ALIASES.items():
        ctx, name = t.split("/") if "/" in t else (_find(out, t), t)
        if ctx is None or not os.path.exists(f"{out}/scalable/{ctx}/{name}.svg"):
            missing.append(t)
            continue
        if _find(out, a) is None:
            os.symlink(f"{name}.svg", f"{out}/scalable/{ctx}/{a}.svg")
    if missing:
        print("kdeapps: alias targets missing:", missing)
    return n
