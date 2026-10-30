# Wanted icons

App icons KDE Modern Classic doesn't have yet. Pick one, say so in an issue so nobody doubles up, draw it, and send
a pull request. Finished app icons will go into an optional add-on theme (see "Where new icons go" below), not
the main theme.

The list was made by comparing the theme's icon names with the names the Papirus icon theme answers to (Papirus
covers a great many apps). Only names were taken from Papirus, never its artwork.

| List | Rows | What to do |
|---|---|---|
| [`wanted-icons.csv`](wanted-icons.csv) | 3380 icons (128 KDE apps first) | Draw a new icon |
| [`wanted-links.csv`](wanted-links.csv) | 2010 names | Check, then add a link to an icon the theme already has |

Left out on purpose: Papirus's folder colour variants, its monochrome panel icons, Steam game IDs and Wine
shortcut IDs.

## How to read `wanted-icons.csv`

- **icon**: the name to draw it under.
- **also known as**: other names the same app (or the same kind of app) asks for. One drawing covers them all as
  links. A row with many names, such as `accessories-notes`, is a general picture for a whole kind of app.
- **status** / **contributor**: fill these in when you take an icon on, so others can see it's being done.

## How to read `wanted-links.csv`

These names can probably show an icon the theme already has (for example `7z` showing Ark's icon). Check each one
makes sense in this theme before adding it; the suggestion comes from what Papirus shows.

## Drawing an icon

- Follow [STYLE.md](STYLE.md): 64×64 canvas, top-left lighting, dark outlines, glossy KDE 3 colours.
- Where a KDE Classic (KDE 3) icon exists for the app or the program it replaced, redraw from that.
- An app's logo may be redrawn in the theme's style. Check the app's trademark or logo terms first: some
  projects don't allow changed versions of their logo. Say in the pull request which terms you checked.
- New icons are Python drawing functions in `src/` (see [CONTRIBUTING.md](../CONTRIBUTING.md)). A finished SVG can
  also be supplied as it is (`src/supplied/`).

## Where new icons go

App icons that KDE Modern Classic doesn't ship will go into an optional add-on theme ("KDE Modern Classic (Apps)",
being set up now), so the main theme stays as it is and people choose whether they want the extra app icons.

## KDE apps still wanted

`alligator`, `amarok`, `arianna`, `artikulate`, `atlantik`, `blinken`, `bomber`, `bovo`, `cantor`, `cervisia`, `digikam`, `dragonplayer`, `falkon`, `gcompris`, `ghostwriter`, `granatier`, `haruna`, `heaptrack`, `juk`, `kaffeine`, `kaidan`, `kajongg`, `kalgebra` (drawn), `kalzium` (drawn), `kamoso` (drawn), `kanagram`, `kapman`, `kapptemplate`, `karbon`, `kasts`, `katomic`, `kbackup`, `kbibtex`, `kblackbox`, `kblocks`, `kbounce`, `kbreakout`, `kbruch` (drawn), `kcachegrind`, `kdenlive`, `kdesvn`, `kdiamond`, `keurocalc`, `kexi`, `keysmith`, `kfloppy`, `kfourinline`, `kgeography`, `kget`, `kgoldrunner`, `kgraphviewer`, `khangman` (drawn), `kig` (drawn), `kigo`, `kile`, `killbots`, `kimagemapeditor`, `kiriki`, `kiten`, `kjumpingcube`, `klickety`, `klines`, `kmahjongg`, `kmines`, `kmouth`, `kmplot` (drawn), `kmymoney`, `knavalbattle`, `knemo`, `knights`, `kollision`, `kolourpaint`, `kompare`, `konquest`, `konversation`, `kpatience`, `kphotoalbum`, `kregexpeditor`, `krename`, `kreversi`, `kronometer`, `kruler`, `ksame`, `kshisen`, `ksirk`, `ksnakeduel`, `kspaceduel`, `ksquares`, `ksudoku`, `kteatime`, `ktechlab`, `ktimer`, `ktimetracker`, `ktuberling`, `kturtle`, `kubrick`, `kuiviewer`, `kwave`, `kwordquiz`, `kxstitch`, `labplot`, `lskat`, `marble`, `minuet`, `okteta` (drawn), `org.kde.audiotube`, `org.kde.karp`, `org.kde.kontrast`, `org.kde.marknote`, `org.kde.neochat`, `palapeli`, `parley`, `peruse`, `rkward`, `rocs`, `rsibreak`, `skanlite`, `skanpage`, `skrooge`, `step`, `subtitlecomposer`, `symboleditor`, `tellico`, `tokodon`, `trojita`, `umbrello`, `yakuake`, `zanshin`
