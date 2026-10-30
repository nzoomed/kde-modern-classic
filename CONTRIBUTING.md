# Contributing

Thanks for helping. The easiest ways in are reporting a missing icon and saying when an icon looks wrong.

## Request an icon

1. Find the icon name the app asks for. For an app's own icon it's the `Icon=` line of its `.desktop` file
   (`/usr/share/applications/…` or `~/.local/share/applications/…`). For icons inside an app, run
   `check-app-icons.sh` or ask in the issue and we'll look it up in the app's source.
2. [Open an icon request](../../issues/new?template=icon-request.yml) with the app's name, that icon name and a
   line on what the app does.

Want to draw one yourself? [docs/WANTED-ICONS.md](docs/WANTED-ICONS.md) lists the app icons still wanted.

## Report a problem

[Open a bug report](../../issues/new?template=bug-report.yml) with a screenshot, the icon name if you know it, your
Plasma version and your colour scheme (light or dark matters for some icons).

## Change or add an icon

Icons are Python functions in `src/` that draw on a 64×64 canvas with a few helpers from `src/gen.py`:

    def my_icon(ic):
        """What the icon shows, in one line."""
        ic.shadow(path, 2.4, 2)                     # soft drop shadow to the lower right
        ic.path(path, ic.lg([(0, "#fff"), (1, "#c3c7cd")]), INK, LW)   # fill + dark outline
        pim._embed(ic, "folder", "translate(8,8) scale(.75)")          # reuse another icon

Each module has a dictionary that maps icon names to drawings, and an `…_ALIASES` dictionary for extra names that
should show the same picture. Read [docs/STYLE.md](docs/STYLE.md) first: it sets the canvas, lighting, outline and
colour rules every icon follows.

Before sending a pull request:

    make build          # redraw the theme
    make test           # must pass
    python3 tools/compare_builds.py <copy of the old KDE-Modern-Classic> KDE-Modern-Classic

The comparison should list only the icons you meant to change (plus any icon that embeds one of them). Commit the
`src/` change **and** the rebuilt `KDE-Modern-Classic/` folder together; CI rebuilds from `src/` and fails if they
don't match.

### Rules

- New names are added, never silently replaced: a module that adds names skips any name the theme already has.
- An app's logo may be redrawn in the theme's style, if the app's trademark or logo terms allow it; say in the pull
  request which terms you checked. Never paste in an app's own icon file. The main theme must not ship `firefox`,
  `firefox-esr` or `org.mozilla.firefox` (`make test` checks this).
- New app icons will go into an optional add-on theme, not the main theme.
- Old designs that users might want back are kept in `src/alt/` with a note in its README.
- Finished SVGs supplied as they are go in `src/supplied/` (see its README), not into the theme folder directly.
- Note user-visible changes in `KDE-Modern-Classic/CHANGELOG.md`.
