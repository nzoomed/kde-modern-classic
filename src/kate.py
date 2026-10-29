"""KDE Classic Vector: Kate - its symbol-outline glyphs, git panel, debugger toolbar and the other icons its
plugins ask for. Runs after okular, so aliases can point anywhere.
"""
import math, os
from gen import Icon, INK, LW, circle, rrect
from settingstrace import _teal, _arrow_pts, _badge, _poly
from okular import _pg


def _ic(fn):
    def f():
        ic = Icon()
        fn(ic)
        return ic
    return f


VIOLET = ("#ead4ff", "#b07ae8", "#7a3ac8", "#3c1478")
YELLOW = ("#fff6c0", "#f0d040", "#c8a010", "#6a5404")
BLUE = ("#8ac8ff", "#2a7ae8", "#0a4ac0", "#062a78")
GREEN = ("#d0f5c8", "#5cc05a", "#2a8a2a", "#0e4a10")


def _cube(ic, x, y, s, cols):
    from uitrace import _iso_cube
    _iso_cube(ic, x, y, s, cols)


# ------------------------------------------------------------------ symbol outline (same block language as code-class)
def code_function(ic):
    """Function: a violet block."""
    _cube(ic, 32, 6, 26, VIOLET)


def code_typedef(ic):
    """Type definition: a yellow block standing on a blue one."""
    _cube(ic, 32, 30, 16, BLUE)
    _cube(ic, 32, 6, 16, YELLOW)


def code_variable(ic):
    """Variable: a small green gem."""
    d = "M32,6L52,24L32,58L12,24Z"
    ic.shadow(d, 2.2, 1.8)
    ic.path(d, ic.lg([(0, GREEN[0]), (.45, GREEN[1]), (1, GREEN[3])], 0, 0, 1, 1), INK, LW)
    ic.path("M12,24H52M22,24L32,6L42,24L32,58Z", "none", GREEN[3], 1)
    ic.add('<path d="M18,22L30,10" stroke="#fff" stroke-opacity=".8" stroke-width="2" stroke-linecap="round"/>')


def _braces(ic, x0=4, x1=60, y0=6, y1=58):
    m = (y0 + y1) / 2
    for s, x in ((1, x0), (-1, x1)):
        d = (f"M{x + s * 12},{y0}Q{x + s * 5},{y0} {x + s * 5},{y0 + 8}V{m - 6}Q{x + s * 5},{m} {x},{m}"
             f"Q{x + s * 5},{m} {x + s * 5},{m + 6}V{y1 - 8}Q{x + s * 5},{y1} {x + s * 12},{y1}")
        ic.add(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"/>'
               f'<path d="{d}" fill="none" stroke="#3c4148" stroke-width="4.2" stroke-linejoin="round" stroke-linecap="round"/>')


def code_block(ic):
    """Block: a pair of curly braces round a few lines of code."""
    _braces(ic)
    for k, (x, w) in enumerate(((20, 22), (24, 18), (24, 12), (20, 20))):
        ic.add(f'<path d="M{x},{18 + k * 9}H{x + w}" stroke="#3c4148" stroke-width="2.4" stroke-dasharray="4 1.6"/>')


def code_context(ic):
    """Context (namespace / scope): curly braces holding a blue block."""
    _braces(ic)
    _cube(ic, 32, 16, 16, BLUE)


# ------------------------------------------------------------------ git
def _node(ic, x, y, r=7, cols=("#ffffff", "#ec9a3a", "#ae5e10")):
    ic.path(circle(x, y, r), ic.rg([(0, cols[0]), (.5, cols[1]), (1, cols[2])], .4, .35, .8), INK, LW)


def _rail(ic, d):
    ic.add(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
           f'<path d="{d}" fill="none" stroke="#8a9098" stroke-width="3.4" stroke-linecap="round"/>')


def vcs_commit(ic):
    """Commit: an orange commit on the history line."""
    _rail(ic, "M4,32H60")
    _node(ic, 32, 32, 12)


def vcs_push(ic):
    _rail(ic, "M20,30V62")
    _node(ic, 20, 44, 9)
    _teal(ic, _poly(_arrow_pts(46, 60, 46, 4, 5, 13, 15)))


def vcs_pull(ic):
    _rail(ic, "M20,2V34")
    _node(ic, 20, 20, 9)
    _teal(ic, _poly(_arrow_pts(46, 4, 46, 60, 5, 13, 15)))


def vcs_branch(ic):
    """Branch: the history line with a second line forking off it."""
    _rail(ic, "M16,4V60")
    _rail(ic, "M16,40Q18,20 44,18")
    _node(ic, 16, 52, 7)
    _node(ic, 16, 30, 7)
    _node(ic, 44, 18, 7, ("#ffffff", "#4fae5a", "#22703a"))


def vcs_diff(ic):
    """Diff: two pages side by side, red removed and green added lines between them."""
    _pg(ic, 2, 4, 28, 46, lines=False)
    _pg(ic, 34, 14, 28, 46, lines=False)
    for k in range(5):
        y = 14 + k * 6
        c = "#e0281a" if k in (1, 2) else "#3c4148"
        ic.add(f'<path d="M6,{y}H{24 - (k % 2) * 4}" stroke="{c}" stroke-width="{2.6 if c != "#3c4148" else 1.4}"/>')
    for k in range(5):
        y = 24 + k * 6
        c = "#2a9a2a" if k in (1, 3) else "#3c4148"
        ic.add(f'<path d="M38,{y}H{56 - (k % 2) * 4}" stroke="{c}" stroke-width="{2.6 if c != "#3c4148" else 1.4}"/>')


# ------------------------------------------------------------------ debugger
def _play(ic, x, y, s, cols=("#d0f5c8", "#3fae2a", "#145a0c")):
    d = f"M{x},{y}L{x + s},{y + s * .6}L{x},{y + s * 1.2}Z"
    ic.shadow(d, 1.8, 1.5)
    ic.path(d, ic.lg([(0, cols[0]), (.45, cols[1]), (1, cols[2])], 0, 0, 1, 1), INK, LW)


def debug_run(ic):
    """Debug: the classic ladybird bug with a green play button."""
    from discover import ladybird
    ic.add('<g transform="translate(-2,-2) scale(.82)">')
    ladybird(ic)
    ic.add("</g>")
    _play(ic, 36, 32, 24)


def debug_run_cursor(ic):
    """Run to cursor: a green play button running up to the text cursor."""
    _play(ic, 4, 14, 30)
    ic.add(f'<path d="M48,8H58M53,8V56M48,56H58" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="square"/>'
           '<path d="M48,8H58M53,8V56M48,56H58" fill="none" stroke="#3c4148" stroke-width="2.6"/>')


def _stmt(ic, y, hi=False):
    ic.path(rrect(8, y, 48, 8, 2), ic.lg([(0, "#ffffff"), (1, "#e8c43a" if hi else "#c3c7cd")], 0, 0, 0, 1), INK, 1.2)


def debug_step_over(ic):
    """Step over: a teal arrow arching over a statement to the next one."""
    _stmt(ic, 30)
    _stmt(ic, 50, True)
    d = []
    for i in range(25):
        a = math.radians(180 + 180 * i / 24)
        d.append((32 + 22 * math.cos(a), 30 + 20 * math.sin(a)))
    w = 3
    out = [(32 + (22 + w) * math.cos(math.radians(180 + 180 * i / 24)), 30 + (20 + w) * math.sin(math.radians(180 + 180 * i / 24))) for i in range(25)]
    inn = [(32 + (22 - w) * math.cos(math.radians(180 + 180 * i / 24)), 30 + (20 - w) * math.sin(math.radians(180 + 180 * i / 24))) for i in range(25)]
    out[-1] = (57, 30)
    inn[-1] = (51, 30)
    head = [(61, 30), (54, 44), (47, 30)]
    _teal(ic, _poly(out + head + inn[::-1]))


def debug_step_into(ic):
    """Step into: a teal arrow going down into the statement."""
    _stmt(ic, 50, True)
    _teal(ic, _poly(_arrow_pts(32, 2, 32, 46, 5, 13, 15)))


def debug_step_out(ic):
    """Step out: a teal arrow coming up out of the statement."""
    _stmt(ic, 50, True)
    _teal(ic, _poly(_arrow_pts(32, 46, 32, 2, 5, 13, 15)))


# ------------------------------------------------------------------ misc
def media_playlist_append(ic):
    """Append to list: a list of lines with the green plus."""
    for k in range(5):
        ic.path(rrect(6, 6 + k * 10, 40, 7, 1.5), ic.lg([(0, "#ffffff"), (1, "#c3c7cd")], 0, 0, 0, 1), INK, 1.1)
    _badge(ic, 48, 48, 12, "green", "M48,42V54M42,48H54")


def distribute_vertical_y(ic):
    from settingstrace import distribute_horizontal
    ic.add('<g transform="rotate(90 32 32)">')
    distribute_horizontal(ic)
    ic.add("</g>")


KT = {
    "actions": {"code-function": code_function, "code-typedef": code_typedef, "code-variable": code_variable,
                "code-block": code_block, "code-context": code_context, "vcs-commit": vcs_commit, "vcs-push": vcs_push,
                "vcs-pull": vcs_pull, "vcs-branch": vcs_branch, "vcs-diff": vcs_diff, "debug-run": debug_run,
                "debug-run-cursor": debug_run_cursor, "debug-step-over": debug_step_over,
                "debug-step-into": debug_step_into, "debug-step-out": debug_step_out,
                "media-playlist-append": media_playlist_append, "distribute-vertical-y": distribute_vertical_y},
}

KT_ALIASES = {
    "vcs-stash": "actions/archive-insert", "vcs-stash-pop": "actions/archive-extract", "kdiff3": "actions/vcs-diff",
    "exception": "dialog-warning", "auto-type": "input-keyboard", "document-export-table": "x-office-spreadsheet",
    "quickopen": "system-search", "quickopen-class": "code-class", "quickopen-function": "actions/code-function",
    "go-next-view-page": "go-next-view", "go-previous-view-page": "go-previous-view", "folder-txt": "folder-documents",
    "folder-windows": "folder", "project-open": "folder-development", "texcompiler": "text-x-tex",
    "run-build-clean": "edit-clear", "select": "edit-select-all", "korg-todo": "checkbox",
    "database-index-symbolic": "server-database", "note-symbolic": "knotes", "format-text-code": "text-x-script",
    "kwrite": "accessories-text-editor", "org.kde.kwrite": "accessories-text-editor", "modified": "document-edit",
    "output_win": "utilities-terminal", "document-swap": "document-open-recent", "view-close": "tab-close",
    "autocorrection": "tools-check-spelling", "debug-step-instruction": "actions/debug-step-into",
    "media-playlist-append-symbolic": "actions/media-playlist-append",
}
for _n in ("vcs-commit", "vcs-push", "vcs-pull", "vcs-branch", "vcs-diff", "debug-run", "code-function", "code-variable",
           "code-typedef", "code-block", "code-context"):
    KT_ALIASES[_n + "-symbolic"] = "actions/" + _n


def _find(out, name):
    for ctx in os.listdir(f"{out}/scalable"):
        if os.path.lexists(f"{out}/scalable/{ctx}/{name}.svg"):
            return ctx
    return None


def write(out):
    n = 0
    for ctx, icons in KT.items():
        d = f"{out}/scalable/{ctx}"
        for name, fn in icons.items():
            p = f"{d}/{name}.svg"
            if os.path.lexists(p):
                os.remove(p)
            open(p, "w").write(_ic(fn)().svg(64))
            n += 1
    missing = []
    for a, t in KT_ALIASES.items():
        ctx, name = t.split("/") if "/" in t else (_find(out, t), t)
        if ctx is None or not os.path.exists(f"{out}/scalable/{ctx}/{name}.svg"):
            missing.append(t)
            continue
        if _find(out, a) is None:
            os.symlink(f"{name}.svg", f"{out}/scalable/{ctx}/{a}.svg")
    if missing:
        print("kate: alias targets missing:", missing)
    return n
