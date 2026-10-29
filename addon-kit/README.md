# Add-on builder for KDE Modern Classic

Makes a small optional icon theme that replaces a few icons and uses KDE Modern Classic for everything else
(the same way as the "KDE Modern Classic (Dolphin)" add-on).

1. Copy the `example` folder and rename it.
2. Put your icon files in `icons/`, named after the icon they replace (`firefox.svg`; PNGs as `firefox-48.png` etc.).
3. Edit `addon.ini` (name, folder, extra names under [aliases]) and fill in `CREDITS.md`.
4. Run:  `python3 make_addon.py your-folder`
   It writes the theme folder and a dated .tar.gz ready to install or upload.

Only one icon theme can be active at a time, so put all your overrides (Firefox, Dolphin ...) in one add-on.
You are responsible for having the right to distribute the icons you add.
