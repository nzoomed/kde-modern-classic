# Contributing to KDE Modern Classic

Thank you for helping preserve and expand the classic KDE aesthetic! Rebuilding a massive 3,182+ icon library for modern desktops is a monumental task. 

While AI-assisted tooling helped lay the groundwork and build the initial foundation for this project, **human refinement is the ultimate goal**. If you want to replace an AI-assisted icon with a 100% human-crafted design, or just help clean up the code, your contributions are incredibly valuable.

The easiest ways to get involved are reporting a missing icon, pointing out when an icon looks wrong, or diving into the source code to draw or tweak icons yourself.

## Request an icon

1. Find the icon name the app asks for. For an app's own icon, look at the `Icon=` line of its `.desktop` file (`/usr/share/applications/…` or `~/.local/share/applications/…`). For icons inside an app, run `check-app-icons.sh` or ask in an issue and we'll look it up in the app's source.
2. [Open an icon request](../../issues/new?template=icon-request.yml) with the app's name, that icon name, and a quick line on what the app does.

Want to draw one yourself? Check out [docs/WANTED-ICONS.md](docs/WANTED-ICONS.md) for a list of app icons we still need.

## Report a problem

[Open a bug report](../../issues/new?template=bug-report.yml) with a screenshot, the icon name (if you know it), your Plasma version, and your color scheme (light or dark matters for some icons).

## Change or add an icon

Icons are Python functions in `src/` that draw on a 64×64 canvas using a few helpers from `src/gen.py`:

```python
def my_icon(ic):
    """What the icon shows, in one line."""
    ic.shadow(path, 2.4, 2)                     # soft drop shadow to the lower right
    ic.path(path, ic.lg([(0, "#fff"), (1, "#c3c7cd")]), INK, LW)   # fill + dark outline
    pim._embed(ic, "folder", "translate(8,8) scale(.75)")          # reuse another icon
```

Each module has a dictionary that maps icon names to drawings, and an `…_ALIASES` dictionary for extra names that should show the same picture. 

**Before writing code:** Please read [docs/STYLE.md](docs/STYLE.md) first. It sets the canvas, lighting, outline, and color rules every icon must follow to ensure visual consistency.

### Build and Test

Before sending a pull request, run the following verification steps:

```bash
make build          # redraw the theme
make test           # must pass
python3 tools/compare_builds.py <copy of the old KDE-Modern-Classic> KDE-Modern-Classic
```

The comparison should list only the icons you meant to change (plus any icon that embeds one of them). Commit the `src/` change **and** the rebuilt `KDE-Modern-Classic/` folder together. CI rebuilds from `src/` and will fail if they do not match.

### Rules & Guidelines

- **No Silent Replacements:** New names are added, never silently replaced. A module that adds names skips any name the theme already has.
- **App Logos & Trademarks:** An app's logo may be redrawn in the theme's style *if* the app's trademark or logo terms allow it. Please state in your pull request which terms you checked. Never paste in an app's own icon file. The main theme must not ship `firefox`, `firefox-esr`, or `org.mozilla.firefox` (`make test` checks this).
- **Add-on Theme for New Apps:** New modern app icons will go into an optional add-on theme, keeping the main theme strictly focused on core desktop environments.
- **Alternative Visuals:** Old designs that users might want back are kept in `src/alt/` with a note in its dedicated README.
- **Raw SVG Submissions:** Finished SVGs supplied exactly as they are go into `src/supplied/` (see its README), rather than into the final theme folder directly.
- **Changelog:** Please note all user-visible changes in `KDE-Modern-Classic/CHANGELOG.md`.
