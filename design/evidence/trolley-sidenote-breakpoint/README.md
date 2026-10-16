# Margin layout from 1280px

Sidenotes, the contents list, the date and the trolley diorama's question now move into the margins from a 1280px viewport instead of 1360px.
A half-width window on a 4K screen is about 1280px wide, so it used to get the narrow layout, with notes under their paragraphs and the question above the scene.
The margin layout needs 1208px (the 640px text column plus a 220px margin column and a 64px gap on each side), so at 1280 each page edge keeps 36px.

The screenshots are from the trolley post, built statically from the live page's layout with this branch's stylesheets, because Jekyll doesn't run on the Mac they were taken on.
Chrome shots were taken with `chrome-devtools-axi` in a headless browser, Firefox shots with headless Firefox's `--screenshot`.

## 1280px, before and after

| Part of the page | Before | After |
| --- | --- | --- |
| Top: contents list and date | ![Top before](chrome-before-1280-top.webp) | ![Top after](chrome-after-1280-top.webp) |
| First diorama: note 2 and the question | ![Diorama before](chrome-before-1280-dio.webp) | ![Diorama after](chrome-after-1280-dio.webp) |
| Appendix B: the who-pays table | ![Appendix before](chrome-before-1280-appendix.webp) | ![Appendix after](chrome-after-1280-appendix.webp) |
| Firefox: note 1 | ![Firefox before](firefox-before-1280-note1.webp) | ![Firefox after](firefox-after-1280-note1.webp) |

## Other widths, unchanged

These screenshots are pixel-identical before and after.

| 1279px | 1366px | 1920px | 390px phone |
| --- | --- | --- | --- |
| ![1279](chrome-after-1279-dio.webp) | ![1366](chrome-after-1366-dio.webp) | ![1920](chrome-after-1920-dio.webp) | ![390](chrome-after-390-dio.webp) |

## Checks

At 1279, 1280, 1366 and 1920px, in Chrome and Firefox, on the trolley post and the unlisted placeholder post:

- the page never scrolls sideways (`scrollWidth` equals the viewport)
- from 1280 all five trolley notes and the placeholder's note are in the margin, with no margin item overlapping the one before it
- at 1279 the notes stay under their paragraphs and the contents list stays hidden, as before
- the leftmost visible text is 36px from the edge at 1280, and nothing visible runs past the right edge
