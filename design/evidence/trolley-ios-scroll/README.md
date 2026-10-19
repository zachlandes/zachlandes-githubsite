# Stable diorama size through toolbar scrolling

The host scene fit previously used `innerHeight`, which changes when Safari's toolbar expands or collapses.
The same fit now measures `100svh`, retaining real window resizing and the reserved run verdict height.

## Before and after

These are isolated Chromium captures at 393×852 CSS pixels, DPR 3.
The toolbar states are simulated by changing `innerHeight` from 852 to 664 and dispatching `resize`, separated by an 8px scroll near the first diorama.
There is no native Safari toolbar in these captures.
The first iframe shrank from 361px to 300px wide before the fix and remains 361px wide afterward.

| | Taller innerHeight | Shorter innerHeight after scroll |
| --- | --- | --- |
| Before | ![Before, taller viewport](before-collapsed.png) | ![Before, shorter viewport](before-expanded.png) |
| After | ![After, taller viewport](after-collapsed.png) | ![After, shorter viewport](after-expanded.png) |

## Browser regression

Run the committed WebKit tests:

```sh
cd tools/trolley
npm ci
npx playwright install webkit
npm test
```

The tests serve the real article, layout, styles, scripts and pane without Jekyll.
They model toolbar-related `innerHeight` changes and resize events while keeping the layout viewport stable, since headless WebKit has no native Safari toolbar.
They cover all five scenes at iPhone 14 Pro width and DPR, the running and completed first scene, reset, rotation, and desktop height/width resizing.
The mobile assertions fail on the original fit and pass with the stable viewport measurement.
Physical-device Safari toolbar behavior remains unverified.
