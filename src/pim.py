"""KDE Classic Vector: the Kontact suite (KMail, KOrganizer, KAddressBook, Akregator, KNotes, Kleopatra) -
mail states, calendar views, meeting roles, certificates and the PIM app icons.

Most of these are an existing drawing with a small marker, so they are composed by embedding icons that are
already in the built theme (`_embed`), with their gradient ids renamed so several can share one file.
Runs last, after every other module has written its icons.
"""
import glob, math, os, re
from gen import Icon, INK, LW, circle, rrect
from settingstrace import _teal, _arrow_pts, _badge, _ok, _no, _poly

OUT = None          # set by write(); the preview script sets it to the last build
_n = [0]


def _ic(fn):
    def f():
        ic = Icon()
        fn(ic)
        return ic
    return f


def _src(name):
    root = OUT or os.path.join(os.path.dirname(os.path.abspath(__file__)), "KDE-Classic-Vector")
    hits = glob.glob(f"{root}/scalable/*/{name}.svg")
    if not hits:
        raise FileNotFoundError(name)
    return open(os.path.realpath(hits[0])).read()


def _embed(ic, name, tf=""):
    """Draw an icon that is already in the theme, under transform `tf`."""
    _n[0] += 1
    p = f"e{_n[0]}_"
    s = _src(name)
    defs = re.search(r"<defs>(.*?)</defs>", s, re.S)
    body = s[s.index("</defs>") + 7: s.rindex("</svg>")] if defs else s[s.index(">", s.index("<svg")) + 1: s.rindex("</svg>")]
    fix = lambda t: re.sub(r'url\(#([^)]+)\)', rf'url(#{p}\1)', re.sub(r'id="([^"]+)"', rf'id="{p}\1"', t)).replace('href="#', f'href="#{p}')
    if defs:
        ic.defs.append(fix(defs.group(1)))
    ic.add(f'<g transform="{tf}">{fix(body)}</g>')


def _mini(ic, name, x=34, y=34, s=.47):
    """A small copy of another icon in the lower right, on a white tile, as a marker."""
    w = 64 * s
    t = rrect(x - 1, y - 1, w + 2, w + 2, 4)
    ic.shadow(t, 1.8, 1.5)
    ic.path(t, ic.lg([(0, "#ffffff"), (1, "#d9dce0")], 0, 0, 1, 1), INK, 1.2)
    _embed(ic, name, f"translate({x},{y}) scale({s})")


def _q_badge(ic, x, y, r, colour):
    """A badge with a question mark drawn as a slim hook and a separate dot (like the ! badges)."""
    _badge(ic, x, y, r, colour, "")
    hook = (f"M{x - r * .34:.2f},{y - r * .3:.2f}Q{x - r * .34:.2f},{y - r * .66:.2f} {x:.2f},{y - r * .66:.2f}"
            f"Q{x + r * .36:.2f},{y - r * .66:.2f} {x + r * .36:.2f},{y - r * .34:.2f}"
            f"Q{x + r * .36:.2f},{y - r * .1:.2f} {x:.2f},{y + r * .02:.2f}V{y + r * .16:.2f}")
    for dx, col, op in ((.7, "#000", ' stroke-opacity=".3"'), (0, "#ffffff", "")):
        ic.add(f'<path d="{hook}" fill="none" stroke="{col}" stroke-width="{r * .24:.2f}" stroke-linecap="round" '
               f'stroke-linejoin="round" transform="translate({dx},{dx})"{op}/>')
        ic.path(circle(x + dx, y + r * .5 + dx, r * .15), col, None, op.replace("stroke", "fill"))


# ------------------------------------------------------------------ the envelope and its states
def _env(ic, open_=False):
    from desktoptrace import _envelope
    if not open_:
        _envelope(ic, 2, 8, 52, 38)
        return
    x, y, w, h = 2, 16, 52, 34
    flap = f"M{x},{y}L{x + w / 2},{y - 14}L{x + w},{y}Z"
    ic.path(flap, ic.lg([(0, "#f4ecd8"), (1, "#c8b898")], 0, 0, 0, 1), INK, LW)
    ic.path(f"M{x + 6},{y - 2}H{x + w - 6}V{y + 14}H{x + 6}Z", "#ffffff", INK, .8)
    for k in range(3):
        ic.add(f'<path d="M{x + 10},{y + 2 + k * 3.6}H{x + w - 12}" stroke="#3c4148" stroke-width="1.1" stroke-dasharray="2.6 1"/>')
    e = f"M{x},{y}L{x + w / 2},{y + h * .55}L{x + w},{y}V{y + h}H{x}Z"
    ic.shadow(e, 2.4, 2)
    ic.path(e, ic.lg([(0, "#fffdf6"), (1, "#e8dcc4")], 0, 0, 1, 1), INK, LW)
    ic.add(f'<path d="M{x + .6},{y + h - .6}L{x + w * .4},{y + h * .45}M{x + w - .6},{y + h - .6}L{x + w * .6},{y + h * .45}" '
           'fill="none" stroke="#8a7a5c" stroke-width="1.2"/>')


def _arrow_badge(ic, kind):
    """A teal arrow badge in the lower right: reply (curls back left), reply-all (two), forward (right),
    receive (down into), queue (clock)."""
    if kind == "forward":
        _teal(ic, _poly(_arrow_pts(30, 50, 62, 50, 5, 12, 13)))
    elif kind == "receive":
        _teal(ic, _poly(_arrow_pts(50, 26, 50, 62, 5, 11, 12)))
    else:
        from actions import _curl_points
        for k, dx in enumerate((0, 10) if kind == "reply-all" else (0,)):
            pts = _curl_points(48 - dx, 50, 11, 3.6, 270, 160, 10, 8, taper=30, N=24)
            _teal(ic, _poly(pts))


def mail_read(ic):            _env(ic, True)
def mail_replied(ic):         _env(ic); _arrow_badge(ic, "reply")
def mail_reply_all(ic):       _env(ic); _arrow_badge(ic, "reply-all")
def mail_forward(ic):         _env(ic); _arrow_badge(ic, "forward")
def mail_forwarded_replied(ic):
    _env(ic)
    _arrow_badge(ic, "forward")
    from actions import _curl_points
    _teal(ic, _poly(_curl_points(16, 50, 10, 3.4, 270, 160, 9, 7.5, taper=30, N=24)))
def mail_receive(ic):         _env(ic); _arrow_badge(ic, "receive")
def mail_flag(ic):            _env(ic); _mini(ic, "flag")
def mail_important(ic):
    from shell import _bang_badge
    _env(ic); _bang_badge(ic, 48, 48, 13, "red")
def mail_junk(ic):            _env(ic); _mini(ic, "user-trash-full")
def mail_notjunk(ic):         _env(ic); _ok(ic, 48, 48, 13)
def mail_deleted(ic):         _env(ic); _no(ic, 48, 48, 13)
def mail_task(ic):            _env(ic); _mini(ic, "view-pim-tasks")
def mail_invitation(ic):      _env(ic); _mini(ic, "view-calendar-day")
def mail_queued(ic):          _env(ic); _mini(ic, "clock")
def mail_encrypted(ic):       _env(ic); _mini(ic, "object-locked")
def mail_signed(ic):          _env(ic); _mini(ic, "document-edit-sign")
def mail_signed_verified(ic): _env(ic); _mini(ic, "document-edit-sign"); _ok(ic, 52, 22, 9)
def mail_thread_watch(ic):    _env(ic); _mini(ic, "view-visible")
def mail_thread_ignored(ic):  _env(ic); _mini(ic, "view-hidden")
def find_mail(ic):            _env(ic); _mini(ic, "edit-find")


# ------------------------------------------------------------------ documents and certificates
def _cert(ic):
    _embed(ic, "application-pkcs7-signature", "translate(-4,-2) scale(.95)")


def document_encrypt(ic):     _embed(ic, "text-plain", "translate(-4,-2) scale(.95)"); _mini(ic, "object-locked")
def document_decrypt(ic):     _embed(ic, "text-plain", "translate(-4,-2) scale(.95)"); _mini(ic, "object-unlocked")
def cert_add(ic):             _cert(ic); _badge(ic, 48, 48, 13, "green", "M48,41V55M41,48H55")
def cert_import(ic):          _cert(ic); _teal(ic, _poly(_arrow_pts(62, 50, 32, 50, 5, 12, 13)))
def cert_export(ic):          _cert(ic); _teal(ic, _poly(_arrow_pts(30, 50, 62, 50, 5, 12, 13)))
def cert_sign(ic):            _cert(ic); _mini(ic, "document-edit-sign")


# ------------------------------------------------------------------ calendar views (KOrganizer)
def _cal(ic, cols, rows, mark=None, lines=False):
    """A wall calendar page: red top band with rings, then a grid (or lines)."""
    page = rrect(4, 8, 56, 52, 4)
    ic.shadow(page, 2.4, 2)
    ic.path(page, ic.lg([(0, "#ffffff"), (1, "#dfe2e6")], 0, 0, 1, 1), INK, LW)
    ic.path("M4,12Q4,8 8,8H56Q60,8 60,12V20H4Z", ic.lg([(0, "#ffb0a0"), (.5, "#e0281a"), (1, "#8a0c06")], 0, 0, 0, 1), INK, LW)
    for x in (16, 32, 48):
        ic.add(f'<path d="M{x},4V13" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>'
               f'<path d="M{x},4V13" stroke="#c3c7cd" stroke-width="2" stroke-linecap="round"/>')
    if not cols:
        for k in range(lines or 0):
            y = 26 + k * 7.6
            ic.path(f"M9,{y}h6v4h-6Z", "#3d9ad8", None)
            ic.add(f'<path d="M18,{y + 2}H{54 - (k % 3) * 6}" stroke="#3c4148" stroke-width="1.6" stroke-dasharray="3 1.2"/>')
        return
    gw, gh = 50 / cols, 34 / rows
    for r in range(rows):
        for c in range(cols):
            x, y = 7 + c * gw, 23 + r * gh
            hi = mark == (r, c)
            ic.path(f"M{x + .6:.1f},{y + .6:.1f}h{gw - 1.2:.1f}v{gh - 1.2:.1f}h{-(gw - 1.2):.1f}Z",
                    "#e0281a" if hi else ("#c3c7cd" if c >= cols - 2 and cols == 7 else "#e4e6e9"), None)


def cal_month(ic):      _cal(ic, 7, 5, (2, 3))
def cal_week(ic):       _cal(ic, 7, 1, (0, 3))
def cal_workweek(ic):   _cal(ic, 5, 1, (0, 2))
def cal_agenda(ic):     _cal(ic, 0, 0, lines=4)


def cal_timeline(ic):
    _cal(ic, 0, 0, lines=0)
    for y, x0, x1, c in ((26, 8, 30, "#3d9ad8"), (34, 18, 46, "#4fae5a"), (42, 12, 38, "#e8c43a"), (50, 30, 56, "#d83a9a")):
        ic.path(rrect(x0, y, x1 - x0, 5, 2), ic.lg([(0, "#ffffff"), (.4, c), (1, c)], 0, 0, 0, 1), INK, .9)


def _gift(ic, x=0, y=0, s=1.0):
    ic.add(f'<g transform="translate({x},{y}) scale({s})">')
    box = "M8,28H56V58H8Z"
    ic.shadow(box, 2.4, 2)
    ic.path(box, ic.lg([(0, "#c4ecff"), (.5, "#3d9ad8"), (1, "#1a5c9e")], 0, 0, 1, 1), INK, LW)
    ic.path("M4,20H60V30H4Z", ic.lg([(0, "#d8ecff"), (.5, "#5aaae8"), (1, "#1a5c9e")], 0, 0, 0, 1), INK, LW)
    ic.path("M28,20H36V58H28Z", ic.lg([(0, "#ffb0a0"), (.5, "#e0281a"), (1, "#8a0c06")], 0, 0, 1, 0), INK, 1.2)
    for s_ in (1, -1):
        ic.path(f"M32,20Q{32 + s_ * 6},4 {32 + s_ * 18},8Q{32 + s_ * 22},16 32,20Z", ic.lg([(0, "#ffb0a0"), (1, "#a8180a")], 0, 0, 1, 1), INK, 1.2)
    ic.add("</g>")


def cake(ic):
    """Birthday: a cake with pink icing and three lit candles."""
    for x in (20, 32, 44):
        ic.path(f"M{x - 2},16H{x + 2}V30H{x - 2}Z", ic.lg([(0, "#ffffff"), (1, "#9ad0f0")], 0, 0, 1, 0), INK, 1)
        ic.path(f"M{x},6Q{x + 4},11 {x},15Q{x - 4},11 {x},6Z", ic.rg([(0, "#fffbe0"), (.5, "#ffd23a"), (1, "#e88a10")], .5, .6, .7), "#a05a08", .8)
    body = "M8,32Q8,28 12,28H52Q56,28 56,32V56H8Z"
    ic.shadow(body, 2.4, 2)
    ic.path(body, ic.lg([(0, "#fff0d8"), (1, "#c89a60")], 0, 0, 0, 1), INK, LW)
    ic.path("M8,32Q8,28 12,28H52Q56,28 56,32V38Q50,44 44,38Q38,44 32,38Q26,44 20,38Q14,44 8,38Z",
            ic.lg([(0, "#ffd0e8"), (1, "#e868a8")], 0, 0, 0, 1), INK, 1.2)
    ic.path("M4,56H60V61H4Z", ic.lg([(0, "#ffffff"), (1, "#a8adb4")], 0, 0, 0, 1), INK, 1.2)


def rings(ic):
    """Wedding anniversary: two gold rings, linked."""
    for cx, cy in ((24, 36), (40, 30)):
        ic.add(f'<path d="{circle(cx, cy, 15)}" fill="none" stroke="{INK}" stroke-width="8.4"/>'
               f'<path d="{circle(cx, cy, 15)}" fill="none" stroke="url(#gold{cx})" stroke-width="6"/>'
               f'<path d="M{cx - 11},{cy - 8}A14,14 0 0,1 {cx - 2},{cy - 14}" fill="none" stroke="#fff" stroke-opacity=".8" stroke-width="1.8" stroke-linecap="round"/>')
        ic.defs.append(f'<linearGradient id="gold{cx}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff6c0"/>'
                       f'<stop offset=".5" stop-color="#e8c43a"/><stop offset="1" stop-color="#7a5a08"/></linearGradient>')
    ic.path("M36,10L40,4L44,10L40,14Z", ic.lg([(0, "#ffffff"), (1, "#9ad0f0")], 0, 0, 1, 1), INK, 1)


def gift(ic):           _gift(ic)


def appointment_recurring(ic): _embed(ic, "view-calendar-day", "translate(-2,-2) scale(.95)"); _mini(ic, "media-playlist-repeat")
def appointment_reminder(ic):  _embed(ic, "view-calendar-day", "translate(-2,-2) scale(.95)"); _mini(ic, "preferences-desktop-notification")
def task_new(ic):
    from uitrace import _new_badge
    _embed(ic, "view-pim-tasks", "translate(-2,-2) scale(.95)"); _new_badge(ic, 48, 48, 15)
def task_reminder(ic):  _embed(ic, "view-pim-tasks", "translate(-2,-2) scale(.95)"); _mini(ic, "preferences-desktop-notification")
def journal(ic):        _embed(ic, "office-calendar")
def journal_new(ic):
    from uitrace import _new_badge
    _embed(ic, "office-calendar", "translate(-2,-2) scale(.95)"); _new_badge(ic, 48, 48, 15)
def contact_new(ic):
    from uitrace import _new_badge
    _embed(ic, "x-office-contact", "translate(-2,-2) scale(.95)"); _new_badge(ic, 48, 48, 15)
def group_new(ic):      _embed(ic, "system-users", "translate(-2,-2) scale(.95)"); _badge(ic, 48, 48, 13, "green", "M48,41V55M41,48H55")
def knotes_alarm(ic):   _embed(ic, "knotes", "translate(-2,-2) scale(.95)"); _mini(ic, "preferences-desktop-notification")


def address_book(ic):
    """Address book: a spiral-bound book with A-Z index tabs and a contact card on the cover."""
    book = "M10,4H52Q54,4 54,6V58Q54,60 52,60H10Z"
    for k, c in enumerate(("#e0281a", "#e8c43a", "#4fae5a", "#3d9ad8", "#9a62d8")):
        ic.path(f"M53,{8 + k * 10}H60Q61,{8 + k * 10} 61,{9 + k * 10}V{15 + k * 10}Q61,{16 + k * 10} 60,{16 + k * 10}H53Z",
                ic.lg([(0, "#ffffff"), (.4, c), (1, c)], 0, 0, 1, 0), INK, 1)
    ic.shadow(book, 2.6, 2.2)
    ic.path(book, ic.lg([(0, "#d8b07a"), (.5, "#a8722a"), (1, "#5a3a10")], 0, 0, 1, 1), INK, LW)
    for y in range(8, 58, 6):
        ic.add(f'<path d="M6,{y}H14" stroke="{INK}" stroke-width="3.4" stroke-linecap="round"/>'
               f'<path d="M6,{y}H14" stroke="#c3c7cd" stroke-width="1.6" stroke-linecap="round"/>')
    card = rrect(20, 18, 28, 20, 2)
    ic.path(card, ic.lg([(0, "#ffffff"), (1, "#e4e6e9")], 0, 0, 1, 1), INK, 1.2)
    ic.path(circle(28, 26, 4), "#f0c8a0", INK, .8)
    ic.path("M22,36Q22,30 28,30Q34,30 34,36Z", "#3d9ad8", INK, .8)
    for y in (24, 28, 32):
        ic.add(f'<path d="M37,{y}H45" stroke="#3c4148" stroke-width="1.4"/>')


def kontact(ic):
    """Kontact: the address book, calendar and an envelope gathered together - all of KDE's PIM in one."""
    _embed(ic, "view-calendar-day", "translate(22,0) scale(.62)")
    _embed(ic, "x-office-contact", "translate(0,4) scale(.6)")
    from desktoptrace import _envelope
    _envelope(ic, 10, 32, 46, 28)


def sim_locked(ic):
    from devices import memory_card
    ic.add('<g transform="translate(2,0) scale(.9)">')
    memory_card(ic)
    ic.add("</g>")
    _mini(ic, "object-locked")


def _face(ic, grey=False):
    from settings import _profile
    if grey:
        _profile(ic, 9, 4, 1.75, ("#a8adb4", "#5c6168"), ("#f2f2f2", "#c3c7cd", "#8a9098"))
    else:
        _profile(ic, 9, 4, 1.75, ("#5a5048", "#14100c"))


def _meeting(ic, badge):
    _face(ic)
    badge(ic)


def user_offline(ic):
    """Offline user: the cartoon face in grey with a grey light."""
    _face(ic, True)
    ic.shadow(circle(50, 50, 8), 1.6, 1.4)
    ic.path(circle(50, 50, 8), ic.rg([(0, "#ffffff"), (.5, "#a8adb4"), (1, "#3c4148")], .4, .35, .8), INK, 1.3)


def meeting_attending(ic):     _meeting(ic, lambda ic: _ok(ic, 48, 48, 13))
def meeting_tentative(ic):     _meeting(ic, lambda ic: _q_badge(ic, 48, 48, 13, "amber"))
def meeting_organizer(ic):     _meeting(ic, lambda ic: _mini(ic, "starred"))
def meeting_no_response(ic):   _meeting(ic, lambda ic: _badge(ic, 48, 48, 13, "grey", "M42,48H54"))
def meeting_request(ic):       _meeting(ic, lambda ic: _q_badge(ic, 48, 48, 13, "blue"))


PIM = {
    "actions": {"mail-replied": mail_replied, "mail-reply-all": mail_reply_all, "mail-forward": mail_forward,
                "mail-forwarded-replied": mail_forwarded_replied, "mail-receive": mail_receive, "mail-flag": mail_flag,
                "mail-mark-important": mail_important, "mail-mark-junk": mail_junk, "mail-mark-notjunk": mail_notjunk,
                "mail-task": mail_task, "edit-find-mail": find_mail, "document-encrypt": document_encrypt,
                "document-decrypt": document_decrypt, "view-certificate-add": cert_add, "view-certificate-import": cert_import,
                "view-certificate-export": cert_export, "view-certificate-sign": cert_sign,
                "view-calendar-month": cal_month, "view-calendar-week": cal_week, "view-calendar-workweek": cal_workweek,
                "view-calendar-agenda": cal_agenda, "view-calendar-timeline": cal_timeline,
                "view-calendar-birthday": cake, "view-calendar-wedding-anniversary": rings,
                "view-calendar-special-occasion": gift, "appointment-recurring": appointment_recurring,
                "appointment-reminder": appointment_reminder, "task-new": task_new, "task-reminder": task_reminder,
                "journal-new": journal_new, "contact-new": contact_new, "user-group-new": group_new,
                "knotes_alarm": knotes_alarm},
    "status": {"mail-read": mail_read, "mail-deleted": mail_deleted, "mail-invitation": mail_invitation,
               "mail-queued": mail_queued, "mail-encrypted": mail_encrypted, "mail-signed": mail_signed,
               "mail-signed-verified": mail_signed_verified, "mail-thread-watch": mail_thread_watch,
               "mail-thread-ignored": mail_thread_ignored, "auth-sim-locked": sim_locked,
               "meeting-attending": meeting_attending, "meeting-attending-tentative": meeting_tentative,
               "meeting-organizer": meeting_organizer, "meeting-participant-no-response": meeting_no_response,
               "meeting-participant-request-response": meeting_request,
               "im-user-offline": user_offline},
    "apps": {"kaddressbook": address_book, "kontact": kontact},
}

PIM_ALIASES = {
    # mail
    "mail-mark-read": "status/mail-read", "mail-mark-unread": "mail-unread", "mail-mark-unread-new": "mail-message-new",
    "mail-reply-list": "actions/mail-reply-all", "mail-reply-custom": "actions/mail-reply-sender",
    "mail-reply-custom-all": "actions/mail-reply-all", "mail-forward-custom": "actions/mail-forward",
    "mail-forwarded": "actions/mail-forward", "mail-mark-task": "actions/mail-task", "mail-queue": "status/mail-queued",
    "mail-folder-outbox": "mail-send", "mail-encrypted-full": "status/mail-encrypted", "mail-encrypted-part": "status/mail-encrypted",
    "mail-signed-part": "status/mail-signed", "mail-signed-full": "status/mail-signed", "mail-signed-fully": "status/mail-signed",
    "document-sign": "document-edit-sign", "document-edit-decrypt-verify": "actions/document-decrypt",
    "view-certificate-export-server": "actions/view-certificate-export", "kleopatra": "application-pkcs7-signature",
    "kleopatra-symbolic": "application-pkcs7-signature", "org.kde.kleopatra": "application-pkcs7-signature",
    "ktnef": "mail-attachment", "org.kde.ktnef": "mail-attachment",
    # apps and PIM sections
    "akregator": "feed-subscribe", "org.kde.akregator": "feed-subscribe", "org.kde.kontact": "apps/kontact",
    "org.kde.kaddressbook": "apps/kaddressbook", "x-office-address-book": "apps/kaddressbook", "address-book-new": "apps/kaddressbook",
    "view-pim-calendar": "view-calendar-day", "view-pim-contacts": "apps/kaddressbook", "view-pim-journal": "office-calendar",
    "view-pim-mail": "kmail", "view-pim-news": "feed-subscribe", "view-pim-notes": "knotes",
    # calendar
    "view-calendar-list": "actions/view-calendar-agenda", "view-calendar-upcoming-events": "actions/view-calendar-agenda",
    "view-calendar-upcoming-days": "actions/view-calendar-week", "view-calendar-tasks": "view-pim-tasks",
    "view-calendar-journal": "office-calendar", "knotes_date": "knotes",
    # people
    "group": "system-users", "resource-group-new": "actions/user-group-new", "list-resource-add": "actions/user-group-new",
    "user-online": "im-user-online", "user-offline": "im-user-offline",
    # odds
    "dvipdf": "application-pdf", "editor": "accessories-text-editor", "emblem-success": "emblem-checked",
    "go-next-skip": "media-skip-forward", "map-symbolic": "globe", "password-generate": "dialog-password",
    "project-development-new-template": "document-new", "quickview": "view-preview", "send-to-symbolic": "document-send",
    "show_table_column": "view-visible", "view-media-visualization": "office-chart-bar", "view-process-tree": "view-list-tree",
}
for _ctx in PIM.values():
    for _k in _ctx:
        PIM_ALIASES.setdefault(_k + "-symbolic", _k)


def _find(out, name):
    for ctx in os.listdir(f"{out}/scalable"):
        if os.path.lexists(f"{out}/scalable/{ctx}/{name}.svg"):
            return ctx
    return None


def write(out):
    global OUT
    OUT = out
    n = 0
    for ctx, icons in PIM.items():
        d = f"{out}/scalable/{ctx}"
        for name, fn in icons.items():
            p = f"{d}/{name}.svg"
            svg = _ic(fn)().svg(64)
            if os.path.lexists(p):
                os.remove(p)
            open(p, "w").write(svg)
            n += 1
    missing = []
    for a, t in PIM_ALIASES.items():
        ctx, name = t.split("/") if "/" in t else (_find(out, t), t)
        if ctx is None or not os.path.exists(f"{out}/scalable/{ctx}/{name}.svg"):
            missing.append(t)
            continue
        if _find(out, a) is None:
            os.symlink(f"{name}.svg", f"{out}/scalable/{ctx}/{a}.svg")
    if missing:
        print("pim: alias targets missing:", missing)
    return n
