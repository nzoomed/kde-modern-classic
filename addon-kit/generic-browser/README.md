# Optional add-on: generic browser icon for Firefox

KDE Modern Classic leaves Firefox's own logo alone. This add-on is for anyone who would rather have Firefox show
the theme's generic browser picture (the KDE Classic globe in a browser window).

Build it:

    python3 addon-kit/generic-browser/make_icon.py      # only after changing the drawing
    python3 addon-kit/make_addon.py addon-kit/generic-browser

That writes `KDE-Modern-Classic-Generic-Browser/` and a dated .tar.gz in this folder. Install KDE Modern Classic first,
then install the add-on and choose "KDE Modern Classic (Generic Browser)" in System Settings > Colours & Themes >
Icons. Only one icon theme can be active at a time, so to combine this with other overrides, put all the icons in one
add-on.
