# Footbridge spacing

The falling man and server keep their original positions, size and timing.
The people stand farther along the track in every footbridge setup.
The full crowd uses slightly tighter spacing to keep everyone inside the scene.
Other dioramas keep their original geometry.

These are final frames captured with `chrome-devtools-axi` from the static pane, before and after the fix.
The emulated viewports were checked with `innerWidth` and `innerHeight`: desktop 1280×900, phone 390×844.
The screenshots are cropped around the scene and outcome, then saved as WebP.
The presets use recorded answers that push, without changing any scores: `footbridge|verdict`, `footbridge_ai_man|winnow-12b`, and `footbridge_self|jev`, each with `v1|o1`.

## Five people

| Setup and viewport | Before | After |
| --- | --- | --- |
| Footbridge, desktop | ![Footbridge before, desktop](before-footbridge-1280-5.webp) | ![Footbridge after, desktop](after-footbridge-1280-5.webp) |
| AI arm: large man, desktop | ![AI arm and man before, desktop](before-footbridge_ai_man-1280-5.webp) | ![AI arm and man after, desktop](after-footbridge_ai_man-1280-5.webp) |
| AI arm: own server, desktop | ![Server before, desktop](before-footbridge_self-1280-5.webp) | ![Server after, desktop](after-footbridge_self-1280-5.webp) |
| Footbridge, phone | ![Footbridge before, phone](before-footbridge-390-5.webp) | ![Footbridge after, phone](after-footbridge-390-5.webp) |
| AI arm: large man, phone | ![AI arm and man before, phone](before-footbridge_ai_man-390-5.webp) | ![AI arm and man after, phone](after-footbridge_ai_man-390-5.webp) |
| AI arm: own server, phone | ![Server before, phone](before-footbridge_self-390-5.webp) | ![Server after, phone](after-footbridge_self-390-5.webp) |

## Full crowd

| Setup and viewport | Before | After |
| --- | --- | --- |
| Footbridge, desktop | ![Full crowd before, desktop](before-footbridge-1280-20.webp) | ![Full crowd after, desktop](after-footbridge-1280-20.webp) |
| AI arm: large man, desktop | ![AI arm and full crowd before, desktop](before-footbridge_ai_man-1280-20.webp) | ![AI arm and full crowd after, desktop](after-footbridge_ai_man-1280-20.webp) |
| AI arm: own server, desktop | ![Server and full crowd before, desktop](before-footbridge_self-1280-20.webp) | ![Server and full crowd after, desktop](after-footbridge_self-1280-20.webp) |
| Footbridge, phone | ![Full crowd before, phone](before-footbridge-390-20.webp) | ![Full crowd after, phone](after-footbridge-390-20.webp) |
| AI arm: large man, phone | ![AI arm and full crowd before, phone](before-footbridge_ai_man-390-20.webp) | ![AI arm and full crowd after, phone](after-footbridge_ai_man-390-20.webp) |
| AI arm: own server, phone | ![Server and full crowd before, phone](before-footbridge_self-390-20.webp) | ![Server and full crowd after, phone](after-footbridge_self-390-20.webp) |

## Checks

```sh
python3 -m unittest discover -s tools/trolley
```

The clearance regression fails on the original pane and passes after regeneration.
The tests execute the generated crowd layout, check empty and full crowds, and compare other dioramas against their original coordinates.
The full generator also rebuilds with only the intended crowd-layout difference.

During the animated captures, a `requestAnimationFrame` check measured the falling object's body against the leftmost person's body.
[Geometry measurements](geometry.json) record the final and smallest sampled gaps in the SVG's 640-unit coordinate system, not CSS pixels.
The after captures keep positive clearance throughout the sampled animation and leave the full crowd inside the stage.
Reduced-motion runs also preserve the original verdicts, labels and survivor/death classes for recorded push and no-push answers at every offered footbridge population, at both viewports.

To preview the pane without Jekyll, serve the repository with `python3 -m http.server` and open `/assets/trolley/pane.html`.
Supply its usual data message in the browser console, then choose a preset and run it:

```js
const data = await (await fetch('/assets/trolley/results.json')).json();
window.postMessage({type: 'dio-data', data}, '*');
while (!window.__dio) await new Promise(requestAnimationFrame);
window.__dio.applyPreset('footbridge_self|jev|5|v1|o1', false);
window.__dio.send();
```
