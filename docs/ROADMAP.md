# Roadmap

Three Plasma 6 icon themes built from one toolkit:

- **KDE Classic**: the KDE 2/3 icons, ported.
- **Nuvola**: David Vignoni's KDE 3 set, ported.
- **Crystalline**: a new theme in the glossy style of early-2000s KDE.

This file tracks what's done, what's next, and how to help.

## Where things stand

Coverage = the share of icon names Plasma 6.3 asks for that each theme answers with its own art
instead of falling back to Breeze. Regenerate with `./build.sh` (it writes `build/coverage.md`).

| Theme | System Settings | Discover | Panel, tray & applets | Desktop shell & other | All Breeze names |
|---|---|---|---|---|---|
| Crystalline | 48% (201/416) | 24% (19/79) | 43% (417/963) | 19% (37/192) | 15% (1040/7111) |
| KDE Classic | 77% (319/416) | 51% (40/79) | 53% (510/963) | 52% (99/192) | 29% (2048/7111) |
| Nuvola | 73% (304/416) | 46% (36/79) | 52% (501/963) | 36% (70/192) | 26% (1862/7111) |

The System Settings sidebar and module icons (162 names) are fully covered in KDE Classic and Nuvola.

### Done

- **Porting.** KDE Classic and Nuvola now run on Plasma 6:
  - folder layout and `index.theme` rebuilt
  - the old `filesystems` context merged into `places`
  - stray files cleaned out
  - white-background PNGs made transparent
- **Alias engine** (`tools/aliases.py`). Maps modern icon names onto art each theme already has:
  - ~790 legacy KDE 3/4 names, Breeze's own synonyms, and `-symbolic` names.
  - Guarded fallbacks: an "off" or "low" state never borrows an "on" or "full" icon.
  - Each name is decided once and applied at every size, so a module never shows different art at
    different sizes.
  - Blank or misleading icons (e.g. KDE 3's white `view`) can never stand in for anything.
- **Large sizes.** Every KDE Classic and Nuvola icon drawn at 32 px or larger also gets a 128 and
  256 px version, made with xBRZ pixel-art upscaling (`tools/upscale.py`).
- **Tray and status icons.** About 170 icons, each drawn once and rendered in all three styles
  (`tools/tray_icons.py`):
  - network: Bluetooth, Wi-Fi, wired, VPN, flight mode, mobile
  - sound: volume, microphone
  - battery 0–100% plus charging
  - other tray icons: brightness, notifications, clipboard, updates, night light
  - power and session
  - input: touchpad, virtual keyboard, caps lock
  - System Settings modules that never had KDE 3 art
- **Crystalline.** About 135 original SVG icons: places, devices, file types, apps and every System
  Settings module.
- **Tooling:**
  - coverage report (`tools/coverage.py`)
  - contact sheets that resolve icons the way Plasma does (`tools/sheet.py`)
  - full-theme catalogue (`tools/catalog.py`)
  - store preview images and logo (`tools/showcase.py`, `tools/logo.py`)

## Known issues

- **Small icons look rough at modern sizes.** Many KDE Classic icons only exist at 16/22 px and were
  drawn for 1024×768 CRT screens. `tools/refit.py` now helps:
  - It fits 598 wrong-sized KDE Classic images (e.g. 24 px art in the 22 px folder) to their folder.
  - It enlarges about 180 over-padded toolbar icons so the drawing fills its canvas.
  - It rebuilds the 22 px navigation arrows from the bolder 32 px art, without the old grey disc.

  Small glyphs are still limited by their original pixels, so these remain the first candidates for
  the SVG redraw below.
- **Pixel art doesn't enlarge well.** Icons that only exist at 16/22 px aren't upscaled, so with
  display scaling at 150–200% they look soft or chunky.
- **No art yet for some areas.** Weather (about 110 names), media-player controls, Discover
  categories and most toolbar actions still fall back to Breeze in all three themes.
- **Weaker tray designs.** A few tray icons (network connect/disconnect, fingerprint) would benefit
  from a second design pass.

## Next steps

### 1. Toolbar and menu actions (all three themes)

This is the biggest remaining gap. Copy, paste, cut, add, remove, back/forward, up, refresh,
zoom, find, save, open, print, undo/redo, properties and so on.
- Draw them with the tray renderer so one design covers all three styles.
- Draw dedicated 16 and 22 px versions, not shrunk 48 px ones.
- Start with what Dolphin, Kate, Konsole and System Settings show.

### 2. Remaining families

- Weather (clear, clouds, rain, snow, storm, fog, day/night variants).
- Media controls and playlist states.
- Discover categories.
- The remaining `network-mobile-*` technology variants (LTE/5G/EDGE badges).

### 3. KDE Classic redrawn in SVG

**Status: started.** The style guide is written (`src/STYLE.md`) and the first batch is done:
25 folders and places, trash, network and computer, with dedicated 16/22 px drawings for the
folders. The devices batch is also done: hard disk, CD, DVD, HD disc, floppy, USB, printer, scanner,
camera, keyboard, mouse and PDA, each traced from the original (`src/traceart.py`) and redrawn.
File types are done too: 31 icons (documents, spreadsheets, presentations, images, audio, video,
archives, scripts, source, PDF and more) covering about 250 MIME type names. Brand logos in the
originals (Acrobat, Debian, RPM) were replaced with generic emblems. Since then: corner tags with the file extension (source, scripts, audio, video, images, archives,
packages, office), dedicated 16/22 px pixel-font versions of every tagged type, and our own
OpenDocument and Microsoft Office icons (done and approved).
- Image formats: done. Generic images and every tagged format (png, jpg, gif, tif, webp, psd, ico, tga,
  xcf, kra, heic, avif, jxl, ppm) use a framed-photo scene (sky, sun, cloud, hills, tree); bitmaps keep
  their own pixel-mosaic picture. **Open for community feedback:** suggestions to improve the scene,
  the tag colours or the bitmap design are welcome.
- Plain text (pencil): done; pencil moved clear of the left edge.
- Session and power buttons: new matching set (lock, log out, switch user, sleep, hibernate, restart,
  shut down) as glossy KDE 3-style tiles, with 16/22 px versions. Open for community feedback.
- Gears (executables, makefiles): tilted version chosen. The flat redraw is kept: set `GEAR_STYLE = "flat"`
  in `src/filetypes.py` to switch back; copies are in `src/alt/`.
- Archive formats: done. 47 formats, each with its own coloured tag. Compressed ones keep both magenta
  corner marks with the tag above the lower one; uncompressed ones (tar, cpio, ar, shar, asar, jar, msi)
  use the plain box. Comic-book archives (cbr, cbz, cb7, cbt) move to the e-books batch.
- System Settings: all 84 module icons drawn. Users and Personalisation keep the side-profile faces
  (style A) for now. **Future revision:** look again at the faces. Three alternatives were drafted and are kept
  in `src/alt/face_styles.py`, with a preview in `src/alt/users-face-styles.png`: B classic cartoon (big nose,
  rosy cheek, smile), C three-quarter faces with coloured shirts (clearest at 22 px), D flat glossy
  silhouettes. Community opinions welcome.
- Locations (System Settings) shares the name `system-file-manager` with the file manager itself, so it now shows the
  KDE Classic filing cabinet. The approved fanned-folder drawing (green, yellow, blue) is kept as `locations()` in
  `src/settings.py` for a future use.
- Dolphin: first pass done and approved (`src/dolphin.py`). App icon is the traced KDE Classic dolphin; the file manager
  (`system-file-manager`) is the classic filing cabinet. Ten folder variants have their own emblems (new, bookmark,
  cloud, games, important, mail, stash, temp, saved search, brown). View controls use KDE Classic's cream pane with a
  navy border. Selection/edit actions, version-control badges, padlocks, star, date and character-set icons added in
  a new `scalable/emblems` folder. Dolphin's sidebar, toolbar and menus no longer fall back to Breeze. All of Dolphin is now
  vector: the core toolbar actions are redrawn in `src/actions.py`, and the rest (bookmarks, configure, warnings
  and errors, tabs, playback, text format, help, terminal, calendar, print and development folders) in
  `src/uitrace.py`. Possible follow-up: a separate "Empty Trash" icon.
- Network: server tower (network-server, network-server-database), plug (emblem-shared), green and grey mount
  wedges (emblem-mounted/unmounted) and folder-sync done. **Revisit in future:** `drive-remote` (mounted network
  drive) is a first try: the hard disk with the KDE Classic cable junction in front. Not yet right; ideas and community
  suggestions welcome (`drive_remote()` in `src/dolphin.py`).
- Discover: first pass done and approved (`src/discover.py`). All sidebar categories redrawn after the KDE 3 K-menu icons
  (games box and joystick, arcade, checkers, cards, tank, typewriter, hammer and spanner, mortarboard, Konqueror gear,
  KMail, KGhostview, K gear, ladybird) plus new ones for development, engineering, science, maths, headphones, chat,
  astronomy and drawing. App page: rating stars (full, half, empty), update priority tiles (down arrows as in the
  originals), upgrade / restart-to-update / shut-down-to-update, download, add-ons, handbook, donate, send, sort,
  maximise/restore, offline, error, prune, SIM card and virtual machine. Left to Breeze on purpose: Steam (a brand
  logo) and Discover's test-only dummy icons. **Revisit in future:** Strategy games (`strategy()` in
  `src/discover.py`) is near final: isometric tank, gun drawn over the curved red arrow, red move arrow and blue
  target cross. It's marked for one more revision (tank proportions and shading against the KDE 3 original).
  Utilities (`utilities()`): claw hammer over the pale blue spanner, accepted for now; may need another pass on
  the hammer head's shape and the spacing between the two tools.
- Desktop shell: first pass done (`src/shell.py`). Panel edit mode (fit width/height, custom size), the
  desktop's edit-mode and arrange menus, filter funnel, Folder View / system tray / clipboard (KDE 3's Klipper) /
  analog clock widgets, hamburger and vertical menu dots, login user list, keyboard-layout and power OSDs, phone
  battery, software-rendering and out-of-memory notices, private browsing, welcome smiley, split top/bottom,
  recent and root folders; Spectacle's whole annotation toolbar redrawn as one family; System Monitor's table
  controls. Not drawn on purpose: other apps' own icons (Falkon, VLC, Kontact, htop, Kdenlive) and names that only
  appear in code tables (the GTK menu-icon mapping, weather data, cursor names).
- System Settings pages: window-rule icons (keep above/below, shade, pin, skip taskbar, pager, opacity, block
  compositing, torn-off menu, splash), the display on-screen menu (mirror, extend left/right, screen off), Get New
  Stuff, left click, crosshairs, equaliser, logs, map zoom and more (`src/shell.py`).
- Weather: all 57 Weather Report conditions plus their -symbolic names, composed from a kit of parts (sun, moon,
  clouds, rain, snow, hail, lightning, wind, fog) in `src/weather.py`. KDE 3 had no weather set; open for
  community feedback.
- Panel and tray (`src/systray.py`): power profiles, disk quota, camera and microphone indicators, headset,
  Caps/Num Lock, timer, Vault, unread mail, calls, printer and computer problems, CD/DVD burning, album art,
  task manager / kicker / global menu widgets. **Plasma Style note:** Breeze's Plasma Style ships its own copies of
  some tray icons (network, media, Vault, keyboard indicator); with a style that doesn't, e.g. Nova7, these show.
  Mobile broadband: all signal levels x network types x SIM lock generated in `src/mobile.py` (five green
  bars, a G/E/3G/H/H+/4G/5G tag, a padlock when locked). Left alone: Amarok-specific media names,
  Krita-style dialog names and GTK leftovers that Plasma never shows.
- **Community feedback wanted:** if a file format shows the wrong icon or falls back to Breeze, please
  report it with the file extension (and the MIME type from Dolphin's Properties dialog if you can).
  The missing-icon report script (step 5) will make this easier once it exists.
- Still to do (new since KDE 3): fonts, subtitles, databases, e-books, VM disks, torrents, Android/AppImage,
  game ROMs, VPN profiles, feeds, colour profiles.
Next batch after file types: System Settings modules. The preview theme "KDE Classic Vector" inherits KDE Classic, so the original PNGs fill in
everything not yet redrawn.

A modern take on KDE Classic. It doesn't need to match the originals pixel for pixel; it should keep
their character, sharp at any size.

1. **Style guide first.** Measure these from the originals so every contributor draws the same way:
   - outline weight
   - palette (`tools/kdeclassic_palette.json` is a start)
   - perspective: the slight 3/4 tilt on folders and devices
   - light from the top left, shadow direction
   - how much detail appears at each size
2. **Skip what's obsolete.** About 40% of the originals are for KDE 2/3-era apps, formats and hardware that
   nothing in Plasma 6 asks for any more (RealPlayer, Netscape, Applixware, tape backup, PalmPilot…). They
   stay in the PNG theme but aren't redrawn. Review the draft list in `src/LEGACY-SKIP.md`.
3. **Redraw in order of visibility:**
   - folders and places
   - devices
   - common file types
   - System Settings modules
   - core KDE apps
   - toolbar actions
   - long-tail apps and games last

   The original PNGs stay as the fallback for anything not yet redrawn, so the theme is complete at
   every stage.
4. **Hand-tune small sizes.** The most-used icons get dedicated 16 and 22 px versions, kept bold and
   uncluttered. Arrows, close/add/remove and other toolbar glyphs should fill more of the canvas
   than the originals did.
5. **Use the originals as reference, not tracing.** The KDE Classic licence allows modification, but
   redrawing gives the modern look we want. Credit the original artists.
6. **Track progress.** Extend `tools/coverage.py` with a "redrawn in SVG vs. original PNG" count per
   area, so it becomes a checklist contributors can claim items from.

The same approach can follow for Nuvola later.

### 4. Breeze fallbacks in Crystalline and Nuvola (waiting on community feedback)

Both themes still show Breeze icons in places users will notice, more so than KDE Classic, which got
the most mapping work. Collect reports from the store and the community first, then fix in order of
how often each gap comes up.

- **Crystalline** (original art, so every gap needs drawing).
  - Current coverage: about 49% of System Settings, 44% of panel/tray and 24% of Discover names.
  - Biggest gaps: toolbar and menu actions, Discover categories, many app icons, and some System
    Settings page icons.
  - Grow it in the same order of visibility as the KDE Classic redraw, using the generators in
    `gen.py`, `sysset.py` and `tools/tray_icons.py`. Aim for parity with KDE Classic in System
    Settings first, then the panel, then actions.
- **Nuvola** (large original set, so many gaps can be mapped rather than drawn).
  - Current coverage: about 73% of System Settings, 52% of panel/tray and 46% of Discover names.
  - Check each reported gap against Nuvola's own art first. Its names differ from KDE Classic's, so
    some gaps just need an entry in `tools/legacy_names.py`.
  - Draw the rest in the Nuvola style with the tray renderer.
- **For each report:** note the app, the icon size and a screenshot; the missing-icon report script
  (step 5) will make this easy. Then decide: map to existing art, draw new art, or leave it on Breeze
  if it's rarely seen.

### 5. Missing-icon report script (any theme)

A small script users run on their own desktop that lists which icons fall back to Breeze, or to
nothing at all, under their current icon theme. It should work for any installed theme, not just
these three, and give users a clear list to paste into feedback.

- **What it checks:** every icon name their system actually asks for. That means names from installed
  apps (`.desktop` files), Plasma widgets and System Settings modules, plus known tray and toolbar
  names, so it also catches apps and widgets our Plasma source list can't see.
- **How it decides:** it follows the theme's `Inherits=` chain the way Plasma does and reports, per
  name, whether the theme itself, Breeze/hicolor, or nothing supplies it, and at which sizes.
- **Output:** a short summary (counts per area), plus a plain-text list grouped by app or area that
  people can paste into a bug report or store comment. Optionally a contact sheet of the gaps.
- **Constraints:** read-only, no root, nothing installed. Plain Python 3 or shell, so it runs on any
  distro.
- **Uses for us:** feed reports straight into the alias engine (`--suggest` could propose mappings
  from `legacy_names.py`) and into the redraw priority list.

### 6. A community kit for porting any KDE 3 icon theme (future)

The porting tool and alias engine aren't specific to these three themes, so the kit could be shared
for others to revive the large library of KDE 3-era icon themes.

- **Already works on any theme:** folder and `index.theme` rebuild, `filesystems` → `places`, the
  ~790 legacy-name mappings and their safeguards, xBRZ 128/256 px upscaling, refit, white-background
  cleanup, coverage report and contact sheets.
- **Still tuned to our three themes:**
  - Tray and status icons only come in the Crystalline, Nuvola and KDE Classic styles. Add a
    generic style that samples each theme's palette from its own icons.
  - Store gallery tiles and preview images hard-code icon lists and colours per theme. Make them
    generic.
  - The 22 px arrow rebuild is KDE Classic only.
- **To do before sharing:**
  1. One command for any theme, e.g. `port.py THEME_DIR --name "X"`.
  2. A "Port your own KDE 3 theme" guide in the README: steps, licence check, fixing mappings.
  3. Test it on a theme it wasn't built for. Crystal SVG, the KDE 3.x default, is the obvious
     candidate (LGPL, check its licence file).
- **Licences:** only port themes with a clear free licence (GPL, LGPL, CC and similar). Keep the
  original credits and licence files. Many KDE-Look themes list no licence or reuse Windows/Mac
  icons; those can't be republished.

### 7. Optional "retro formats" add-on (asking the community)

Plasma picks icons by file type, and the system's file-type database (shared-mime-info) has no types for
many retro formats, so an icon theme alone can't give them icons. Today they fall back to the 0/1 page
(unknown binary) or the zip box (MAME sets).

- **Idea:** a small optional add-on with a MIME definitions file (the same mechanism the Arduino IDE uses
  for `.ino`) plus an installer script, so the theme can show proper icons for:
  - Commodore 64: `.d64` (floppy), `.t64` / `.tap` (tape), `.prg`, `.crt` (cartridge, detected by content
    so it doesn't clash with certificates)
  - ZX Spectrum: `.tap` / `.tzx` (tape), `.z80` / `.sna` (snapshots)
  - Atari 8-bit and ST: `.atr`, `.st`, `.msa` (floppy), `.xex` (cartridge)
- **Needs:** a new cassette-tape emblem; tags as for the other ROM formats.
- **Ask in the store description / release notes** (draft text in `RELEASE-NOTES-TODO.md`).
- **Status:** waiting on community feedback. These formats aren't widely seen, and an extension may
  already be used by other apps, so definitions must not override existing types.

> Released as "KDE Modern Classic" (theme name, package `KDE-Modern-Classic`); "KDE Classic Vector" / `classicvec`
> remain the project and source folder names.

### 8. KDE Classic Vector: final revision pass (at the end)

Everything drawn so far is accepted for now. Before release, go back over the whole set once more,
compare against the KDE 3 originals and the style guide (including the arrow rules), and refine.
Icons already marked for another look:

- [ ] `drive-remote` (mounted network drive) - not right yet (`dolphin.py`)
- [ ] Strategy games - isometric tank proportions and shading (`discover.py`)
- [ ] Utilities - claw hammer head and spacing from the spanner (`discover.py`)
- [ ] Users / Personalisation faces - alternative styles B/C/D kept in `alt/face_styles.py`
- [ ] Image formats scene and archive tags - open to community suggestions (`filetypes.py`)
- [ ] Weather set - new design (KDE 3 had none); check against the rest once used day to day (`weather.py`)
- [ ] Arrows across the set - bring older arrow icons in line with the arrow rules in `STYLE.md`
- [ ] New shell, System Settings page and tray icons (`shell.py`, `systray.py`) - accepted, but review them
  against the KDE 3 originals' overall style (colours, shading, outline weight, level of detail) so they sit with the
  traced icons

- [ ] Magnifiers - make every magnifying glass match the agreed Find magnifier (`_magnifier()` in
  `actions.py`: grey rim, pale-blue lens with highlight, cyan collar, dark handle straight out at 45 degrees).
  To compare: Search category and Plasma Search / KRunner / File Search in System Settings (`settings.py`),
  `search` in the shell (`shell.py`), saved-search folder (`dolphin.py`), find-a-file and document viewer
  (`discover.py`), and the map zoom badges (`shell.py`, `_map_zoom`).
- [ ] TT fonts icon (`_tt()` in `filetypes.py`: Fonts, Font Management, font-enable/disable) - isometric redraw
  over the traced original, largely good; serif shapes and depth could be refined.
- [ ] Trash can: now straight-sided like KDE Classic (`TRASH_STRAIGHT = True` in `gen.py`). The earlier tapered can is kept on
  record: set `TRASH_STRAIGHT = False` to switch back, or see `alt/user-trash-tapered.svg` and `alt/user-trash-full-tapered.svg`.
- [ ] Discover subcategory icons - waiting on a KDE feature request: Action, Emulators, Puzzles, Role Playing, Sports,
  Launchers and Tools share `applications-games`; Simulation shares `applications-games-strategy`; Biology, Geology,
  IDEs and Profiling (Debian) have no icon. If Discover adopts names like `applications-games-simulation`, draw them.
- [ ] Quick Settings and General Behavior (System Settings) - both ask for `preferences-desktop`, so both show the
  Control Centre icon. Requested separate names (`preferences-desktop-quicksettings`, `preferences-desktop-behavior`);
  draw them if KDE adopts them. Both requests are written up in `KDE-icon-name-requests.md`.
- [x] Speaker and printer icons - done. Printer redrawn 2026-10-26 (`printer()` in `devices.py`; final). Speaker
  refined 2026-10-27 against the user's KDE Classic audio icon (`e_speaker` / `speaker_parts` in `gen.py`): smaller
  back box so the long teal flare shows, pointed dome growing from the cone's left edge, cone shadowed at the top,
  outline 0.9 instead of LW. The rim position is unchanged so the volume waves still line up. Used by 25 drawings
  (audio files, the volume family, audio-speakers, Sound settings, folder-music at all sizes, Kid3).
- [ ] Panel volume icon at 22 px - revisit. After the 2026-10-27 speaker redraw (smaller box, finer 0.9 outline) the
  speaker looked tiny in the panel next to its waves. Current fix: the volume family, Muted and Speakers draw the
  speaker 25% larger and fit the waves beside it (`VOL_SPEAKER` / `VOL_WAVES` in `traytrace.py`). The user called
  it "probably the best we can do"; ideas if it still reads small: a heavier outline for these icons only, or a
  dedicated 22 px drawing with a chunkier speaker and two waves.
- [ ] Curled arrows - `edit-undo` / `edit-redo` and `view-refresh` (`actions.py`, `_curl_points`): acceptable,
  but not a perfect match yet. Compare the curl's thickness and taper, the head size, and where the head sits against the
  originals. Undo/redo have a right-angled head on a 45-degree back edge; refresh is two arrows tilted upright.
- [ ] "Storage Devices" page in System Settings - shows orange, cyan and green cubes that look Crystal-era, not our
  block-device cubes. Probably a KDE Classic bitmap reached through inheritance for a name we don't draw. KDiskFree's
  names (`kdf`, `kcmdf`, `kwikdisk`) now point at our `drive-multidisk` cubes, but the colours reported don't match
  that icon, so find the page's real icon name (check its .desktop/.json Icon=, or the KCM plugin) and alias or redraw it.
- [ ] KDE Classic fallbacks - about 465 app names fall through to the KDE Classic bitmap theme (old KDE 3-era apps).
  Most suit the theme, and apps that ship their own icons won't use them anyway. Render them all on one contact sheet
  for reference (resolve each name the way Plasma does, as `tools/sheet.py` does) and flag any that clash, e.g.
  Crystal-style ones, for redrawing.
- [ ] (Known limitation, low priority) Discover's Installed list shows some apps and widgets (Ark, Dolphin,
  Application Dashboard, Color Picker, Disks & Devices) with Breeze icons: Discover adds the distribution's cached
  AppStream images on top of the theme icon (`AppStreamUtils::iconForComponent`). Not fixable from the theme; a
  possible KDE request is to prefer the stock theme icon when the theme has it.
- [ ] Tray show/hide button: Plasma 6.3 asks for plain `arrow-up/down/left/right` (used ~40 times elsewhere as
  move up/down buttons, so not overridden); newer Plasma asks for `arrow-*-symbolic`, which point at the chevrons.
- [ ] **Full symbolic set (GTK compatibility)** - goal for a future release. GTK/GNOME apps (and Chromium/Electron
  title bars) ask for `*-symbolic` names and expect plain single-colour glyphs they can tint. Today ~775 of our
  ~780 symbolic names point at full-colour icons (aliases added for KDE), so GNOME header bars show colour icons;
  ~200 of those are names GNOME apps use often (open-menu, go-previous/next, edit-copy/paste/find, list-add ...).
  Plan: draw a matching set of plain glyphs (16 px grid, `class="ColorScheme-Text"` + `fill:currentColor` so both
  KDE and GTK tint them - see `SYMBOLIC_WINDOW` / `_sym_svg()` in odds.py, already done for the window buttons),
  covering Adwaita's ~590 symbolic names plus the KDE-specific ones. KDE apps are unaffected either way: when a
  `-symbolic` name is missing KIconLoader falls back to the colour icon in the same theme, while GTK prefers a
  symbolic icon from a parent theme - so removing a colour `-symbolic` alias is always safe for KDE.
  Audit: compare against adwaita-icon-theme/Adwaita/symbolic (cloned from github.com/GNOME/adwaita-icon-theme).
- [ ] **KDE app icons (games, education, utilities)** - not urgent. KDE has ~250 apps; most users only install a few.
  Suggested order: (1) apps the community reports via `check-app-icons.sh`; (2) apps that had a KDE 3 icon -
  trace-and-redraw from the KDE Classic set (`build/kdeclassic`, ~590 app icons), e.g. KPatience, KMahjongg, KMines,
  KRuler, KTeaTime, Kalzium, KBounce, KReversi, KAtomic, KTouch, KGet; (3) newer apps with no classic original,
  drawn new in the style; (4) quick aliases where an existing drawing fits (KTimer -> chronometer, Marble -> globe,
  KGpg -> key, Kompare -> vcs-diff, Dragon Player -> media player, Synaptic -> package ...). Leave third-party brand
  logos (Firefox, GIMP, VLC, Blender ...) alone. The user's own scan (2026-10-20) listed ~60 KDE apps on Breeze and
  ~35 on their own hicolor logos.
  Findings (2026-10-20, icons pulled from 43 app repos): no app still ships its KDE 3 icon (KMouseTool's tiny 16/32 px
  line drawing is the only possible exception). Many games/edu apps still ship KDE 4 Oxygen-era icons (KGoldrunner,
  Killbots, KSnakeDuel, Kigo, KTuberling, KTurtle, KNavalBattle, Kollision, KPatience/LSkat cards ...) - detailed and
  glossy, closer to our style than Breeze. Priority: Breeze apps with a KDE Classic original first (trace + redraw),
  then Breeze apps without one, then the Oxygen-era hicolor ones last. Comparison sheet:
  scratchpad shipped_vs_classic.png; app repos cloned from github.com/KDE/<app>.
Add to this list as icons are flagged during review.

### 9. Ideas from Papirus (studied 2026-10-29)

Papirus advertises 7,000+ icons. Its main folder holds about 3,800 app drawings per size, each with one or two
extra names linked to it (Flatpak IDs, Snap names, old desktop names): half of its ~88,000 files are links. Most of
those drawings are other projects' logos redrawn in Papirus's style, which this theme doesn't do. What does apply:

- [ ] **Name coverage for apps we already draw.** Papirus links every alternative name an app uses (reverse-DNS
  Flatpak IDs such as `org.kde.kate`, distro names, old names). A script that lists, for each app icon we draw,
  the names its `.desktop` files use across distros and Flathub, and adds the missing links, is cheap coverage.
- [ ] **Missing-MIME report.** Like Papirus's `missing_mimetypes.sh`: read the system's shared-mime-info and list
  file types whose icon (or generic icon) the theme doesn't answer.
- [ ] **Missing-app report from Flathub.** Like `missing_flathub_apps.sh`: list popular Flathub apps whose icon
  name isn't in the theme, to choose "what it does" pictures for the most-used ones (no logos).
- [ ] **Symbolic icons that follow the colour scheme.** Papirus's monochrome icons use
  `class="ColorScheme-Text"` with `fill:currentColor` and `FollowsColorScheme=true` in index.theme, so Plasma
  recolours them for light and dark schemes. Our `-symbolic` names link to the full-colour icons; drawing true
  symbolic versions for the few that sit on dark panels and title bars would fix dark-theme contrast for good.
- [ ] **A small dark variant.** Papirus-Dark inherits Papirus and overrides only ~2,400 action and panel icons. An
  add-on "KDE Modern Classic (Dark)" could override just the handful of dark glyphs that vanish on dark schemes.
- [ ] **24 px icons.** Papirus ships 16, 18, 22 and 24 px versions of actions and panel icons. GTK apps ask for
  24 px toolbar icons; we fall back to scalable, which is fine, but tuned 24 px versions of the busiest actions
  would sharpen GTK toolbars.
- [x] **Process:** issue forms for icon requests and bugs, tests in CI on every push, date-based release tags,
  `make install` / `make dist` (done when the GitHub repository was set up).

## How to help

- **Find what's missing on your desktop.** Once the missing-icon report script (Next steps, 5) exists, run it and paste the output. Until then, run the coverage report, or open the contact sheets to see
  which names fall back to Breeze (pink cells in `tools/sheet.py` output).
- **Add a tray or status icon.** Write a short builder in `tools/tray_icons.py`. It renders in all
  three styles automatically. Preview it with `tools/tray_preview.py`.
- **Fix a wrong mapping.** Edit `tools/legacy_names.py` (modern name → legacy names, first match
  wins) and rebuild.
- **Redraw an icon in SVG.** Follow the style guide (once written), keep to Qt-SVG-safe features (no
  filters, masks or clip paths for Crystalline), and check it at 16, 22, 32 and 48 px on both a
  light and a dark panel.
- **Report issues with a screenshot.** Include the app and the icon size. Small-icon problems
  are often size-specific.

## Credits and licences

- **KDE Classic:** the KDE artists of the 2.x/3.x era; maintained by James Richard Tyrer. The
  images are free for any use, including copying, modification and redistribution (see
  `kdeclassic/LICENSE`).
- **Nuvola:** David Vignoni (ICON KING), LGPL 2.1 (see `nuvola/license.txt`).
- **Crystalline and the new tray/settings icons:** original work, created with AI assistance.
- **KDE logo (K menu):** from `KDE_2_logo.svg` on Wikimedia Commons, LGPL like KDE's own artwork; kept as
  `src/traced/KDE_2_logo.svg`. Blur filter replaced with the theme's shadow, outline added.
- **xBRZ upscaler:** Zenju, AGPL-3. This covers the scaler code in `tools/xbrz/src`, not the icons
  it produces.

- Gwenview app icon: needs more work; Breeze's is used meanwhile. Two drafts are kept in kdeapps.py:
  `gwenview` (the Oxygen-era magenta eye, redrawn) and `gwenview_kview` (KDE Classic's KView sheet,
  magnifier and cup of brushes). Re-enable by adding it back to KA["apps"] with the org.kde.gwenview alias.

## KDE apps still falling back to Breeze (sweep of 2026-10-20)
Run `tools/breeze_sweep.py SRC_DIR THEME_DIR BREEZE_ICONS OUT.json` over cloned KDE sources (github.com/KDE/<repo>)
to list every icon name an app asks for that this theme lacks and Breeze has. Plasma, Dolphin, System Settings,
KIO/file dialogs, Frameworks, Ark and Spectacle are clean. Left for 1.1, in suggested order:
- Okular: done (okular.py).
- (was) Okular (~37): page view modes, annotation tools, colour modes, signatures, zoom-fit-width.
- Kate (~42): debug toolbar, git actions, code-outline symbols, kwrite.
- Elisa (~9): app icon, artist/track/lyrics/favourite/playlist views.
- Kontact suite: done (pim.py) - 22 KDE PIM repos swept; only the Facebook/Twitter logos remain on Breeze.
- Odds and ends: Discover (folder-git, translate, view-pages-overview), KWallet open/closed, Konsole
  (preferences-scroll), KDE Connect, KRDC, KSystemLog.
- Leave alone: other services' logos (Google, YouTube, Wine, Kompare ...); window-*-symbolic is left to
  Breeze on purpose (GTK/Firefox/Electron title bars tint those).
