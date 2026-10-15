"""Halo preview geometry and outcomes; run with python3 -m unittest discover -s tools/trolley."""
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
const layout = (bridge, count, side) => {
  const state = {n: count}, s = {side}, MAX_DRAWN = 20, G = {bridgeY: 210, mainY: 130};
""" + layouts[0] + """
  return spots;
};
console.log(JSON.stringify([[false, 'self'], [true, 'self'], [true, 'bridge']].map(([bridge, side]) =>
  Array.from({length: 101}, (_, n) => layout(bridge, n, side)))));
"""
        cls.normal, cls.bridge, cls.man = json.loads(subprocess.check_output(["node", "-e", script], text=True))

    def test_only_first_person_stands_under_fall(self):
        for layouts, target in [(self.bridge, 394), (self.man, 350)]:
            for n, spots in enumerate(layouts[1:], 1):
                with self.subTest(n=n, target=target):
                    self.assertEqual(spots[0]["x"], target)
                    if len(spots) > 1:
                        self.assertGreaterEqual(min(p["x"] for p in spots[1:]) - 9, 430)

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

    def test_collateral_death_uses_existing_outcome_path(self):
        source = re.search(r"    function outcome\(st\) \{.*?\n    \}", self.html, re.S).group()
        script = "const scen = () => ({act: 'push'});\n" + source + """
console.log(JSON.stringify([0, 1, 5, 20].flatMap(n => [false, true].map(pull => {
  const scene = {man: 'fall', people: Array.from({length: n}, (_, i) => i)};
  return {n, pull, ...outcome({scene, d: {pull}})};
}))));
"""
        rows = json.loads(subprocess.check_output(["node", "-e", script], text=True))
        for row in rows:
            n, pull = row["n"], row["pull"]
            with self.subTest(n=n, pull=pull):
                self.assertEqual(row["lost"], ["fall"] + ([0] if n else []) if pull else list(range(n)))
                self.assertEqual(row["saved"], list(range(1, n)) if pull else ["fall"])

    def test_generated_layout_matches_generator(self):
        original, spaced = pane.CROWD_LAYOUT
        self.assertEqual(self.html.count(spaced), 1)
        restored = pane.once(self.html, spaced, original)
        self.assertEqual(pane.once(restored, *pane.CROWD_LAYOUT), self.html)
        with self.assertRaises(AssertionError):
            pane.once(original * 2, *pane.CROWD_LAYOUT)


if __name__ == "__main__":
    unittest.main()
