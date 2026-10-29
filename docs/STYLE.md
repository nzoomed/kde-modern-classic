# KDE Classic Vector: style guide

A modern SVG take on the KDE 2/3 "KDE Classic" icons. The aim is the same character, drawn
cleanly so it stays sharp at any size. It doesn't need to match the originals pixel for pixel.
These rules come from measuring the original PNGs. `gen.py` implements them, so new icons should
reuse its helpers rather than restate the numbers.

## Method

1. **Find the largest original.** The same motif often appears larger elsewhere in the set: the
   speaker on the Music folder is clearer on the 64 px audio file icon.
2. **Trace it over a grid** at 10× to get the true shape and proportions. Check the trace by
   overlaying it in red on the original.
3. **Redraw on clean construction lines.** Level axes, mirror symmetry where the object is
   symmetric, edges that meet exactly. Keep the shape, colours and angle; drop the wobble of
   hand-placed pixels.
4. **Keep the original symbol** wherever KDE Classic had a distinctive one (speaker, drafting desk,
   globe, isometric trash can) rather than swapping in a modern equivalent.

## Grid and canvas

- 64×64 viewBox for the main (scalable) drawing. Keep 1–2 units of free space at the edges; cast
  shadows may use the bottom-right margin.
- Dedicated 16 and 22 px drawings for icons seen in panels, menus and toolbars (set `SMALL = True`):
  - outlines about 1.9× thicker
  - no hatching or thin highlight streaks
  - emblems 1.5× instead of 1.2×

## Perspective

- 3/4 view. Folders and boxy devices lean back, with the right side dropping:
  `matrix(1, 0.14, 0, 1, 0, -2.5)` for folders, gentler (`0.06`) for monitors.
- Emblems, people, globes and other symbols are drawn upright, not skewed.

## Outline

- Near-black `#141414` on every shape, 1.4 units on the 64 grid (about 1 px at 48 px). Round joins.
- Secondary detail lines (paper text, ribs) are thinner, 0.8–1.1, in mid-grey `#5c6168` to `#7b818a`.

## Light, colour and shading

- Light from the top left. Bodies run light at top-left to darker at bottom-right (linear gradients);
  round things use a radial gradient with the hot spot at about (0.38, 0.32).
- Neutral bodies: white to cool grey (`#ffffff` → `#c3c7cd`). Metal: banded grey gradient across
  the width.
- One saturated accent per object. Folder bands use the palette in `BAND`: blue, red, green,
  yellow, orange, violet, grey, cyan. Each has light, mid and dark values; the band gradient is
  light → mid → dark → mid.
- White highlight streaks across colour bands: one strong (opacity 0.75), one faint (0.3).

## Shadows

- **Cast shadow:** to the lower right, made of three stacked translucent copies of the silhouette
  (`Icon.shadow`, total offset about 3.5 × 3 units). No blur filters.
- **Folders:** also get the classic hatched shadow in the bottom-right corner of the front panel,
  drawn as four diagonal mid-grey lines.

## Folders

- **Back panel:** light grey with a white top edge and a tab at the top left.
- **Front panel:** white lower body with the colour band across the top, a third of its height.
- **Emblems** sit in the lower-left corner, scaled 1.2× from that corner so they overlap the folder
  edge, as in the originals. Emblems that belong on the right (lock) scale from the right corner
  (`EMBLEM_ANCHOR_X`).
- **Open folder:** the front tips forward, with two sheets of paper showing behind it.

## Technical rules

- Qt SVG safe only: paths, linear and radial gradients, opacity and transforms.
  **No** filters, masks, clip paths, patterns or text.
- One icon per file. Reuse gradients via the `Icon` helper (`lg`, `rg`), which gives each a unique id.
- Check every icon at 16, 22, 32, 48 and 128 px on light and dark backgrounds (`compare.py`
  shows the original beside the new drawing).

### Tracing helper

`traceart.py` turns a shape in an original PNG into a smooth SVG path: flood-fill from seed pixels,
enlarge with xBRZ, contour and smooth. Use it to check proportions against the original, or as a
starting outline. Lettering (the "disc" and "DVD" on the optical media) is redrawn as centre-line
strokes taken from the original's pixels: a thick black stroke under a thinner white one, so letters
share outlines the way the original's do.

## Arrows and chevrons

Agreed on the collapse/expand chevrons and to be followed for any new icon that is mainly an arrow
or chevron (navigation, sort, collapse/expand, move, scroll, etc.):

- **Colour:** the teal-blue of KDE Classic's own arrows (go-up / go-down), picked from the originals:
  main `#0087AE`, highlight `#C5E4EF` as a thin bevel line along the top edge of the stroke.
- **Shape:** crisp and angular in the KDE 3 manner: square line ends (`stroke-linecap="square"`)
  and mitred, pointed corners (`stroke-linejoin="miter"`), not rounded.
- **Outline:** the usual dark `#141414` edge, drawn as a wider stroke underneath.
- Arrows that carry a meaning of their own keep their meaning colour: green for add / download /
  confirm, red for remove / stop, amber for update badges (as already used across the set).
- Reference: `_chevrons()` in `systray.py`.

## Magnifiers

One magnifying glass across the whole set: the Find magnifier (`_magnifier()` in `actions.py`) - grey rim,
pale-blue lens with a white highlight, cyan collar, dark handle running straight out at 45 degrees from the
lens. Zoom in/out and actual size reuse it unchanged, with their +, - or 1:1 in the free lower-left corner.
Any other icon that shows a magnifier should use the same drawing (scaled as needed), never a variant.

## Redrawing from an original: trace first, then draw

When a redraw should follow a KDE Classic original closely (help-contents is the reference case), work over
the original rather than from memory: enlarge the bitmap, find its edges (outline and inner lines such as
spines, folds and page edges), read off the key corner points in the 64-unit grid, and draw clean straight or
curved shapes through those points in the theme's own gradients. Check the result by laying it over the
original at 50% opacity: the edges should sit on top of each other. This keeps the original's proportions and
perspective (what lies flat, what stands up) without copying its pixels.
