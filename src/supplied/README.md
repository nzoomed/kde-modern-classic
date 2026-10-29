# Supplied icons

Finished SVGs supplied by the theme's author, installed as they are instead of being drawn by the Python modules.
`apps2.write()` copies each one into the theme (see `SUPPLIED` in `apps2.py`); names that link to it keep working.

| File | Installed as | Added | Notes |
|---|---|---|---|
| `gwenview.svg` | `scalable/apps/gwenview.svg` (+ `org.kde.gwenview`) | 2026-10-27 | Replaces the drawn eye (`apps2.gwenview`, kept on record). Only change from the supplied file: a `viewBox` added. Uses Gaussian-blur filters for its soft shadows and glows, which Qt 6.7 and later render. |
