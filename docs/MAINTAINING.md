# Maintaining KDE Modern Classic

## Layout

| Folder | What it is |
|---|---|
| `KDE-Modern-Classic/` | The built theme, installable as it is. Also holds README, AUTHORS, licences, CHANGELOG and `check-app-icons.sh`. |
| `src/` | The generator: one Python module per area, each icon a drawing function. `gen.py` runs them all. |
| `src/traced/` | Shapes traced from KDE Classic originals (JSON paths) and the KDE 2 logo source. |
| `src/alt/` | Earlier or alternative designs kept on record (not built). |
| `src/supplied/` | Finished SVGs supplied by the author, copied in as they are by `apps2.write()`. |
| `src/brand/` | Optional official logos a user can drop in (none shipped). |
| `addon-kit/` | Builds small add-on themes that override a few icons (e.g. the Generic Browser add-on). |
| `tools/` | Checks (`check_theme.py`), build comparison (`compare_builds.py`), the qBittorrent icon checker, and the xBRZ loader used only when tracing new shapes. |
| `docs/` | Style guide, roadmap, icon-name requests for KDE, this file. |

## Where things live in `src/`

- Community app icons: `apps2.py` (`COMMUNITY`, `COMMUNITY_ALIASES`): ktorrent, kid3, qdbusviewer,
  utilities-terminal_su, mpv. Firefox's generic browser picture (`web_browser_window`) is only for the add-on.
- Supplied SVGs: `apps2.py` `SUPPLIED` (Gwenview). The drawn eye `gwenview()` is kept on record.
- qBittorrent's own icon names: `qbittorrent.py` (`QB` drawings, `QB_ALIASES` links). It runs after `apps2` and only
  adds names.
- Share (`document-share`): `apps2.share_document` (page with linked nodes) at 32 px and up, `apps2.share_nodes`
  (nodes alone) at 16/22 px via `SMALL`. The plug stays on `emblem-shared` / `emblem-share` (shared folders).
- Icons settings page: `settings.icons_kcm` (two stamps, the author's queen outline, `QUEEN`). Emoji Selector:
  `settings.emoji_selector`.
- Add/Remove: `dolphin.list_add`, `shell.minus` (green/red badges); old black glyphs kept as `list_add_dark`,
  `minus_dark` and in `src/alt/`.
- "New" actions: `uitrace._new_badge` (green plus). `uitrace._sparkle` stays for Wizard, Class, Enum.
- Speaker: `gen.e_speaker` / `gen.speaker_parts`. Panel volume icons draw it 25% larger: `VOL_SPEAKER`,
  `VOL_WAVES` in `traytrace.py`; waves are `traytrace._waves`.
- Notification bell: `settings.notifications` (all tray bells and reminders reuse it).
- Printer: `devices.printer` (final). Network and globe: `gen.network`, `gen.plain_globe`. Dolphin's small view
  modes: `dolphin.small_view`. Konsole: `uitrace.terminal_monitor`, `uitrace.utilities_terminal`.

## Changing an icon

1. Keep a copy of the current theme: `cp -a KDE-Modern-Classic /tmp/before`.
2. Edit the drawing in `src/`, then `make build`.
3. `python3 tools/compare_builds.py /tmp/before KDE-Modern-Classic` — only the intended icons should change.
   Icons that embed others (`pim._embed`) can show as changed when an embed earlier in the build shifts their
   gradient numbering; they look identical (check by rendering them, or by stripping the `eNN_` prefixes).
4. `make test`, then add a line to `KDE-Modern-Classic/CHANGELOG.md`.

To preview one icon as SVG:

    cd src && python3 -c "import gen, settings; ic = gen.Icon(); settings.notifications(ic); open('/tmp/x.svg','w').write(ic.svg())"

## Release

1. `make build && make test && make check-build`
2. Date the CHANGELOG entry, commit, and tag the release with the date: `git tag YYYYMMDD && git push --tags`.
3. `make dist` (and `make addon-generic-browser` if it changed) and attach the archives to the GitHub release and
   the KDE Store page.
4. Users clear `~/.cache/icon-cache.kcache` after installing a new version (the README says so).

## Agreed rules

- App logos may be redrawn in the theme's style where the app's trademark or logo terms allow it (the pull request
  says which terms were checked); never paste in an app's own icon file. New app icons go in an optional add-on,
  so the main theme stays as released. The main theme must not ship `firefox`, `firefox-esr` or
  `org.mozilla.firefox` (`make test` checks this). Rule changed 2026-10-30; before that, app logos were not drawn.
- When a name's meaning is shared (e.g. `window-close` for both menus and notification popups), the theme can only
  draw one picture; ask KDE for a separate name instead (`docs/KDE-icon-name-requests.md`).
- Modules that add names only add; anything already in the theme is skipped and reported.
