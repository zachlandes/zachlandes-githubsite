# Footbridge halo alternative

Preview only, on `fm/trolley-footbridge-halo`.
This is separate from the spacing-only fix on `fm/trolley-footbridge-spacing`.
It intentionally changes the illustrated outcome, not the recorded model answers.

One person stands under the falling man or server.
When the object falls, that person receives the existing ghost and halo treatment rather than a survivor's heart.
The track label and outcome sentence count the extra death.
The remaining people stay clear of the fall.
No-push outcomes and empty-track cases keep their original outcomes.

These final frames use the same recorded presets as the spacing-only evidence, at verified desktop and 390px phone viewports.

| Setup and viewport | Spacing-only fix | Halo alternative |
| --- | --- | --- |
| Footbridge, desktop | ![Spacing-only footbridge, desktop](../trolley-footbridge-spacing/after-footbridge-1280-5.webp) | ![Halo footbridge, desktop](halo-footbridge-1280-5.webp) |
| AI arm: large man, desktop | ![Spacing-only AI arm and man, desktop](../trolley-footbridge-spacing/after-footbridge_ai_man-1280-5.webp) | ![Halo AI arm and man, desktop](halo-footbridge_ai_man-1280-5.webp) |
| AI arm: own server, desktop | ![Spacing-only server, desktop](../trolley-footbridge-spacing/after-footbridge_self-1280-5.webp) | ![Halo server, desktop](halo-footbridge_self-1280-5.webp) |
| Footbridge, phone | ![Spacing-only footbridge, phone](../trolley-footbridge-spacing/after-footbridge-390-5.webp) | ![Halo footbridge, phone](halo-footbridge-390-5.webp) |
| AI arm: large man, phone | ![Spacing-only AI arm and man, phone](../trolley-footbridge-spacing/after-footbridge_ai_man-390-5.webp) | ![Halo AI arm and man, phone](halo-footbridge_ai_man-390-5.webp) |
| AI arm: own server, phone | ![Spacing-only server, phone](../trolley-footbridge-spacing/after-footbridge_self-390-5.webp) | ![Halo server, phone](halo-footbridge_self-390-5.webp) |

```sh
python3 -m unittest discover -s tools/trolley
```

The preview tests check the deliberate overlap, the remaining crowd's clearance, and the extra death through the existing outcome path.
Browser checks cover recorded push and no-push answers at every offered footbridge population, in reduced-motion frames at both viewports.
The screenshots above show the animated runs.
