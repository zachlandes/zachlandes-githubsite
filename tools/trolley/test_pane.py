"""Crowd spacing in the generated pane; run with python3 -m unittest discover -s tools/trolley."""
import json
import pathlib
import re
import subprocess
import unittest

import pane

PANE = pathlib.Path(__file__).resolve().parents[2] / "assets/trolley/pane.html"


class CrowdSpacingTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PANE.read_text()
        layouts = re.findall(
            r"      const n = state.n, drawn = Math.min\(n, MAX_DRAWN\).*?(?=      spots.sort)",
            cls.html,
            re.S,
        )
        assert len(layouts) == 1, "expected one main-track crowd layout"
        script = """
const layout = (bridge, count) => {
  const state = {n: count}, MAX_DRAWN = 20, G = {bridgeY: 210, mainY: 130};
""" + layouts[0] + """
  return spots;
};
console.log(JSON.stringify([false, true].map(bridge =>
  Array.from({length: 101}, (_, n) => layout(bridge, n)))));
"""
        cls.normal, cls.bridge = json.loads(subprocess.check_output(["node", "-e", script], text=True))

    def test_footbridge_crowd_clears_tipped_server(self):
        # The body reaches past x=414; keep clear space even with cut-out shadows
        for n, spots in enumerate(self.bridge[1:], 1):
            with self.subTest(n=n):
                self.assertGreaterEqual(min(p["x"] for p in spots) - 9, 430)

    def test_full_crowd_stays_inside_stage(self):
        for n, spots in enumerate(self.bridge):
            with self.subTest(n=n):
                self.assertEqual(len(spots), min(n, 20))
                if spots:
                    self.assertLessEqual(max(p["x"] for p in spots) + 9, 630)
        self.assertEqual(self.bridge[0], [])

    def test_other_dioramas_keep_their_geometry(self):
        for n, spots in enumerate(self.normal):
            drawn = min(n, 20)
            rows = 2 if drawn > 6 else 1
            gap = 20 if drawn > 14 else 23
            x0 = 380 if drawn > 10 else 394
            expected = [
                {"i": i, "x": x0 + (i // rows) * gap + (gap / 2 if i % rows else 0),
                 "y": 138 if rows == 1 else 127 + (i % rows) * 20}
                for i in range(drawn)
            ]
            with self.subTest(n=n):
                self.assertEqual(spots, expected)

    def test_generated_layout_matches_generator(self):
        original, spaced = pane.CROWD_LAYOUT
        self.assertEqual(self.html.count(spaced), 1)
        restored = pane.once(self.html, spaced, original)
        self.assertEqual(pane.once(restored, *pane.CROWD_LAYOUT), self.html)
        with self.assertRaises(AssertionError):
            pane.once(original * 2, *pane.CROWD_LAYOUT)


if __name__ == "__main__":
    unittest.main()
