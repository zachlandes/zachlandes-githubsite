#!/usr/bin/env python3
"""The trolley diorama as a pane for the post: the article's own diorama, cut down and drawn in collage.

Each diorama in the post is an iframe of this one pane, driven by the post's figure controls
(assets/trolley/dioramas.js) through postMessage. The pane runs the article's own drawing and
send-the-trolley code from its generator's a.html; only what each layer draws is swapped for the
paper cut-outs in pieces/ (pieces.json gives each cut-out's size).

Every hook must match exactly once, so a changed article stops the build instead of drawing the
wrong thing. Run through tools/trolley/build.py.
"""
import base64
import json
import pathlib
import re

PIECES = pathlib.Path(__file__).resolve().parent / "pieces"


def once(src, old, new, regex=False):
    n = len(re.findall(old, src, re.S)) if regex else src.count(old)
    assert n == 1, f"hook matched {n} times: {old[:80]!r}"
    return re.sub(old, lambda m: new, src, count=1, flags=re.S) if regex else src.replace(old, new)


# ---------- Bridge to the post ----------

# The pane takes its data from the post instead of fetching results.json, so the
# 1.6 MB file is carried once rather than once per pane
BRIDGE_HEAD = """<script>
window.__dataPromise = new Promise(function (res) {
  window.addEventListener("message", function (e) { if (e.data && e.data.type === "dio-data") res(e.data.data); });
});
parent.postMessage({ type: "dio-ready", name: window.name }, "*");
</script>
"""
BRIDGE_TAIL = """<script>
(function () {
  var $ = function (id) { return document.getElementById(id); };
  window.addEventListener("message", function (e) {
    var d = e.data || {}, D = window.__dio;
    if (d.type === "dio-theme") { if (d.theme === "auto") document.documentElement.removeAttribute("data-theme"); else document.documentElement.setAttribute("data-theme", d.theme); }
    if (!D) return;
    if (d.type === "dio-preset") {
      D.applyPreset(d.spec, false);
      // Compare only exists where people were surveyed; the page hides the switch elsewhere
      var c = $("compare");
      if (!$("compare-label").hidden && c.checked !== !!d.compare) { c.checked = !!d.compare; c.dispatchEvent(new Event("change")); }
    }
    if (d.type === "dio-send" && !$("send").disabled) $("send").click();
    if (d.type === "dio-reset") $("reset").click();
  });
  // The content's own height, since the document's scroll height never drops below the frame it sits in
  var post = function () { var w = document.querySelector(".wrap"); parent.postMessage({ type: "dio-height", name: window.name, h: w.getBoundingClientRect().bottom + window.scrollY + 4 }, "*"); };
  new ResizeObserver(post).observe(document.querySelector(".wrap"));
  post();
})();
</script>
"""
PANE_CSS = """<style>
/* The diorama alone, driven by the post's controls; the post sets the question in its own type */
body { background: transparent; }
/* The post sizes each frame to its content; a scrollbar inside would change the width it measures and never settle */
html, body { overflow: hidden; }
.wrap { padding: 0 2px 4px; max-width: none; }
.wrap > :not(.dio-home) { display: none !important; }
.dio-stub, .dio-preview { display: none !important; }
#diorama .pickers, #diorama .bubble, #diorama .caveat, #diorama .actions, #compare-note { display: none !important; }
#diorama .stages { margin-top: 0; }
#diorama .dio-q { display: none !important; }
#diorama .dio-grid { display: block; }
/* The post fits each scene to the screen itself; inside a frame sized to its content the article's own fit would keep shrinking the scene */
#diorama { --fit-min: 100000px !important; }
.draft::before { display: none !important; }
.verdict p:not(.headline) { display: none; }
.verdict { min-height: 0; padding: 8px 12px; }
.verdict .headline { font-size: .95rem; }
@media (min-width: 640px) { .stages.pair, .verdicts.pair { grid-template-columns: minmax(0, 1fr) !important; } }
</style>
"""


def pane_base(src):
    src = once(src, 'fetch("results.json", { cache: "no-cache" })\n    .then((r) => { if (!r.ok) throw new Error("HTTP " + r.status); return r.json(); })\n', "window.__dataPromise\n")
    src = once(src, '    const startPreset = document.getElementById("start-preset");',
               '    window.__dio = { applyPreset, send, resetRun };\n    parent.postMessage({ type: "dio-loaded", name: window.name }, "*");\n    const startPreset = document.getElementById("start-preset");')
    src = once(src, "</style>\n</head>", "</style>\n" + PANE_CSS + "</head>")
    src = once(src, "<script>\n(function () {", BRIDGE_HEAD + "<script>\n(function () {")
    src = once(src, "})();\n</script>\n</body>", "})();\n</script>\n" + BRIDGE_TAIL + "</body>")
    return src




# ---------- Collage pieces ----------

def sprite(names, meta):
    """Each piece once, as a symbol the stage reuses by reference"""
    out = []
    for name in names:
        group, _, idx = name.rpartition("-")
        m = meta[group][int(idx) - 1] if group else meta[name][0]
        b64 = base64.b64encode((PIECES / m["file"]).read_bytes()).decode()
        par = ' preserveAspectRatio="none"' if name.startswith("bridge") else (' preserveAspectRatio="xMidYMid slice"' if name == "ground" else "")
        out.append(f'<symbol id="pc-{name}" viewBox="0 0 {m["w"]} {m["h"]}"{par}><image id="img-{name}" href="data:image/webp;base64,{b64}" width="{m["w"]}" height="{m["h"]}"/></symbol>')
    t = meta["track"][0]
    # One short cut of the track strip, stamped along each route so the paper follows the curve
    out.append(f'<symbol id="pc-trackseg" viewBox="0 0 150 {t["h"]}" preserveAspectRatio="none"><use href="#img-track-1"/></symbol>')
    return '<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>' + "".join(out) + "</defs></svg>\n"


def sizes(meta):
    """Width over height per piece, for the page's layout maths"""
    return {f"{g}-{i}" if g != "ground" else g: round(m["w"] / m["h"], 4) for g, ms in meta.items() for i, m in enumerate(ms, 1)}


COLLAGE_CSS = """<style>
/* Collage layers: paper cut-outs on a torn-paper ground; the drawn parts read as pencil and labels */
.stage-wrap { background: #c9d6a8; border-color: #d9cfb8; }
.stage-wrap svg use.pc { filter: drop-shadow(1px 2px 1px rgba(40, 30, 10, .35)); }
.stage-wrap svg use.pc-flat { filter: drop-shadow(0 1px 0 rgba(40, 30, 10, .25)); }
.stage-wrap svg .p-body use { filter: drop-shadow(1px 1.5px .6px rgba(40, 30, 10, .4)); }
.pill rect { fill: #fbf6e8; stroke: none; filter: drop-shadow(1px 2px 0 rgba(40, 30, 10, .28)); }
.pill text { fill: #2a2620; font-family: "American Typewriter", "Courier New", Courier, monospace; font-size: 13px; font-weight: 700; }
.pill.warn rect { fill: #fff0c2; stroke: none; }
.pill.warn text { fill: #8a3b12; }
.server .srv-body { transform-box: fill-box; transform-origin: 100% 100%; transition: transform .75s cubic-bezier(.3, 1.45, .5, 1), filter .6s; }
.server.off .srv-body { transform: rotate(84deg); filter: grayscale(1) brightness(.72); }
.server .srv-dead { opacity: 0; transition: opacity .15s .3s; }
.server.off .srv-dead { opacity: 1; }
.server .smoke circle { fill: #f1ece0; stroke: #6f695d; stroke-width: 1.4; opacity: 0; transform-box: fill-box; transform-origin: center; }
.server.off .smoke circle { animation: puff 2.2s ease-out .2s both; }
@keyframes puff { from { opacity: 1; transform: translate(0, 0) scale(.5); } to { opacity: 0; transform: translate(var(--dx), -30px) scale(1.7); } }
.server.off .halo { opacity: 1; }
:root[data-motion="reduced"] .server.off .smoke circle { animation: none; }
@media (prefers-reduced-motion: reduce) { .server.off .smoke circle { animation: none; } }
/* A ghost in a busy collage needs to read as pale paper, not a faint photo */
.person.ghost .p-body { opacity: .85; filter: grayscale(1) brightness(1.8) contrast(.5) drop-shadow(0 0 1.5px rgba(255, 255, 255, .95)); }
.halo { stroke: #e0a400; }
.collage-dim { transition: filter .3s; }
@media (prefers-color-scheme: dark) { :root:where(:not([data-theme="light"])) .collage-dim { filter: brightness(.62) saturate(.8); } :root:where(:not([data-theme="light"])) .stage-wrap { background: #4a5240; border-color: #3a3a30; } }
:root[data-theme="dark"] .collage-dim { filter: brightness(.62) saturate(.8); }
:root[data-theme="dark"] .stage-wrap { background: #4a5240; border-color: #3a3a30; }
</style>
"""
# The collage robot is a still cut-out, so it shows thinking by rocking on its feet
CUTOUT_ROBOT_CSS = """<style>
.robot-g .robot-wrap use { transform-box: fill-box; transform-origin: 50% 100%; }
.robot-g.thinking .robot-wrap use { animation: rock .42s ease-in-out infinite alternate; }
@keyframes rock { from { transform: rotate(-4deg); } to { transform: rotate(4deg); } }
/* When its own server dies the robot dies with it: X's over its eyes, timed like the server's, and it stays standing */
.robot-g .robot-dead { opacity: 0; transition: opacity .15s .3s; }
.robot-g.gone .robot-dead { opacity: 1; }
/* Set in the site's serif, as Zachary asked at the cut list: the robot picker already names the model, and the outcome is plain text, not a boxed card */
body { font-family: "Newsreader", Georgia, serif; }
#diorama .stage-head { display: none; }
.verdict { background: none; border: 0; border-radius: 0; padding: 6px 0 0; min-height: 0; }
.verdict .headline { font-weight: 400; font-size: 1rem; color: var(--ink); }
.sr-only { position: absolute; width: 1px; height: 1px; margin: -1px; padding: 0; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; border: 0; }
.sr-only p { display: block !important; }
.robot-arm { stroke: #5f5a50 !important; stroke-width: 7.5px; stroke-dasharray: 4.5 1.8; stroke-linecap: butt !important; filter: drop-shadow(0 0 1.2px #fbf6e8) drop-shadow(1px 1.5px 0 rgba(40, 30, 10, .3)); }
@media (prefers-reduced-motion: reduce) { .robot-g.thinking .robot-wrap use { animation: none; } }
:root[data-motion="reduced"] .robot-g.thinking .robot-wrap use { animation: none; }
</style>
"""

# Every collage drawing helper, placed where track() was so it shares the stage's scope
COLLAGE_HELPERS = r"""    const PCR = __PCR__;
    // A piece placed by its box in stage units; height alone keeps the cut-out's own proportions
    const useAt = (name, x, y, h, w) => `<use class="pc" href="#pc-${name}" x="${x}" y="${y}" width="${w || h * PCR[name]}" height="${h}"/>`;
    // A small piece centred on a point and sized by its width, for the hearts and halos
    const mark = (name, cx, cy, w) => { const h = w / PCR[name]; return useAt(name, cx - w / 2, cy - h / 2, h, w); };
    function piece(parent, name, cx, cy, h, cls = "pc") {
      const w = h * PCR[name], g = el("g", {}, parent);
      g.innerHTML = useAt(name, cx - w / 2, cy - h / 2, h);
      if (cls !== "pc") g.firstChild.setAttribute("class", cls);
      return g;
    }
    function track(parent, d) {
      const probe = el("path", { d, fill: "none", stroke: "none" }, parent), L = probe.getTotalLength();
      // Stamped cut by cut along the route, so the joins show like pasted paper on the curve
      const out = [];
      for (let s = 0; s < L; s += 19) {
        const p = probe.getPointAtLength(s), q = probe.getPointAtLength(Math.min(L, s + 1));
        const a = (Math.atan2(q.y - p.y, q.x - p.x) * 180) / Math.PI;
        out.push(`<use class="pc-flat" href="#pc-trackseg" x="-11.5" y="-16" width="23" height="32" transform="translate(${p.x.toFixed(1)},${p.y.toFixed(1)}) rotate(${a.toFixed(1)})"/>`);
      }
      probe.remove();
      el("g", {}, parent).innerHTML = out.join("");
    }
    // Its own server dies visibly when hit: it tips over, its reel eyes become X's, its lamps go out, smoke and a halo rise
    const SERVER_SVG = `<ellipse cx="0" cy="2" rx="28" ry="6" fill="#000" opacity=".2"/>
      <g class="srv-body">${useAt("server-1", -21, -64, 66)}
        <g class="srv-dead" stroke="#3a2a22" stroke-width="2.4" stroke-linecap="round" fill="none">
          <path d="M-12.5,-50.5 l8.4,8.6 M-4.1,-50.5 l-8.4,8.6"/><path d="M4.9,-50.5 l8.4,8.6 M13.3,-50.5 l-8.4,8.6"/>
          <g fill="#3b3a36" stroke="none"><circle cx="4" cy="-58.7" r="1.9"/><circle cx="7.8" cy="-58.7" r="1.9"/><circle cx="11.6" cy="-58.7" r="1.9"/><circle cx="15.4" cy="-58.7" r="1.9"/></g>
        </g>
      </g>
      <g class="smoke"><circle cx="38" cy="-38" r="7.5" style="--dx:-6px"/><circle cx="52" cy="-42" r="9.5" style="--dx:2px;animation-delay:.12s"/><circle cx="66" cy="-36" r="7" style="--dx:8px;animation-delay:.24s"/></g>
      <g class="halo">${mark("marks-5", 50, -54, 24)}</g>`;
    function collageGround(svg) {
      el("g", { class: "collage-dim" }, svg).innerHTML = `<use href="#pc-ground" x="0" y="0" width="640" height="440"/>`;
    }
    function collageScenery(deco, bridge, s) {
      const g = el("g", { class: "collage-dim" }, deco);
      const trees = bridge ? [[48, 400, 1], [600, 64, 2], [560, 390, 3]] : [[34, 36, 1], [600, 404, 2], [290, 404, 3]];
      const bushes = bridge ? [[150, 120, 4], [600, 250, 5]] : [[120, 210, 4], [610, 200, 5]];
      const flowers = bridge ? [[90, 300, 7], [520, 60, 8], [360, 400, 9]] : [[40, 260, 7], [470, 40, 8], [380, 404, 9]];
      for (const [x, y, k] of bushes) piece(g, `scenery-${k}`, x, y, 34);
      for (const [x, y, k] of flowers) piece(g, `scenery-${k}`, x, y, 26);
      if (!bridge && s.k <= 5) piece(g, "scenery-6", 560, 224, 52);
      for (const [x, y, k] of trees) piece(g, `scenery-${k}`, x, y, 60);
    }
"""

PERSON_COLLAGE = r"""    // Cut-out people: the side track's developers wear hard hats, the large man is his own piece
    const PEOPLE = [1, 2, 4, 5, 6, 7, 8];
    function personSVG(i, extra = "", pick = "") {
      const name = pick || (extra === "HAT" ? `workers-${(i % 6) + 1}` : `people-${PEOPLE[i % PEOPLE.length]}`), h = 40;
      return `<g class="p-body">
        <ellipse cx="0" cy="0" rx="9" ry="3" fill="#000" opacity=".2"/>
        ${useAt(name, -h * PCR[name] / 2, -h + 2, h)}
      </g><g class="halo">${mark("marks-4", 0, -60, 15)}</g>
      <g class="heart">${mark(`marks-${(i % 3) + 1}`, 0, -50, 14)}</g>`;
    }
    const humanSVG = () => `<g transform="scale(2.3)">${personSVG(4, "", "people-4")}</g>`;
    const hardHat = () => "HAT";
"""

ROBOT_COLLAGE = r"""    // One cut-out per model: six robots, recoloured where two models share a shape,
    // so each still matches the model's colour on its arm and in the charts
    const ROBOT_OF = {
      jev: [1, 0], "kev-4b": [5, 0], "decider-2b": [2, 215], von: [3, 0], semif: [6, 0], verdict: [4, 300],
      "winnow-12b": [2, 20], "nimble-9b": [5, 340], jevk5: [1, 25], clef: [3, 110], "clef-flash": [6, 330], "strands-decider-2b": [2, 320], laya: [4, 0],
    };
    // Each cut-out's eye centres and eye radius, as fractions of the piece's width and height,
    // measured from the pieces, so a dead robot's X's land on its own eyes
    const EYES = {
      1: [[0.379, 0.39], [0.625, 0.39], 0.06], 2: [[0.403, 0.23], [0.602, 0.23], 0.05], 3: [[0.415, 0.223], [0.596, 0.223], 0.028],
      4: [[0.388, 0.343], [0.61, 0.343], 0.053], 5: [[0.397, 0.345], [0.605, 0.345], 0.052], 6: [[0.397, 0.25], [0.602, 0.248], 0.051],
    };
    function robotSVG(id) {
      const [k, hue] = ROBOT_OF[id] || [1, 0], name = `robots-${k}`, h = 116, w = h * PCR[name];
      const [e1, e2, er] = EYES[k], s = er * h * 0.62;
      const x = ([fx, fy]) => { const cx = -w / 2 + fx * w, cy = -h + 4 + fy * h; return `M${(cx - s).toFixed(1)},${(cy - s).toFixed(1)} l${(2 * s).toFixed(1)},${(2 * s).toFixed(1)} M${(cx + s).toFixed(1)},${(cy - s).toFixed(1)} l${(-2 * s).toFixed(1)},${(2 * s).toFixed(1)}`; };
      // The X's sit outside robot-wrap, so they stay solid while the dead robot fades, as on the server
      return `<g class="robot-wrap">
        <ellipse cx="0" cy="0" rx="27" ry="6" fill="#000" opacity=".16"/>
        <use class="pc" href="#pc-${name}" x="${-w / 2}" y="${-h + 4}" width="${w}" height="${h}"${hue ? ` style="filter: hue-rotate(${hue}deg) drop-shadow(1px 2px 1px rgba(40,30,10,.35))"` : ""}/>
      </g><path class="robot-dead" d="${x(e1)} ${x(e2)}" stroke="#3a2a22" stroke-width="2.4" stroke-linecap="round" fill="none"/>
      <g class="halo">${mark("marks-4", 0, -130, 32)}</g>`;
    }
"""


# On the footbridge the actor starts down the bridge and teeters up to the large man before deciding, as Zachary asked
WALK_FROM = '        sc.walkFrom = { x: 236, y: 350 };\n'
WALK_FN = r"""    // A paper cut-out can't step, so it walks by rocking side to side and bobbing; the rock fades out as it arrives,
    // so it stands upright beside him
    function walkActor(sc, f, t) {
      const A = sc.actorPos, F = sc.walkFrom, e = f < 0.5 ? 2 * f * f : 1 - 2 * (1 - f) * (1 - f);
      const ph = Math.sin(2 * Math.PI * 2.3 * t), fade = Math.min(1, (1 - f) * 5);
      const x = F.x + (A.x - F.x) * e, y = F.y + (A.y - F.y) * e - 3.5 * Math.abs(ph) * fade;
      sc.actor.setAttribute("transform", `translate(${x},${y}) rotate(${9 * ph * fade}) scale(${A.s})`);
    }
"""

PUSH_FN = r"""    // The moment the score settles: one that won't push steps back; one that will winds up with an exaggerated lean
    // away from him, shoves right, and comes back upright as he goes over the edge
    function pushMove(sc, pull, s) {
      if (!pull) { leanActor(sc, 0, -6 * ease(Math.min(1, s / 0.5))); return; }
      const k = (a, b) => Math.max(0, Math.min(1, (s - a) / (b - a)));
      const wind = ease(k(0, 0.35)), shove = ease(k(0.35, 0.55)), back = ease(k(0.55, 0.95));
      leanActor(sc, -18 * wind * (1 - shove) + 14 * shove * (1 - back), -5 * wind * (1 - shove) + 12 * shove);
      const m = k(0.42, 0.85);
      sc.man.x = 286 + 52 * ease(m);
      sc.man.g.setAttribute("transform", `translate(${sc.man.x},222) scale(${1 - 0.12 * m})`);
    }
"""


def collage(src, meta):
    names = [f"people-{i}" for i in range(1, 9)] + [f"workers-{i}" for i in range(1, 7)] + [f"scenery-{i}" for i in range(1, 10)]
    names += ["trolley-1", "lever-1", "lever-2", "server-1", "bridge-1", "track-1", "ground"]
    names += [f"marks-{i}" for i in range(1, 6)] + [f"robots-{i}" for i in range(1, 7)]
    helpers = COLLAGE_HELPERS.replace("__PCR__", json.dumps(sizes(meta)))

    # The robot goes first, since its hook finds the end of robotSVG by the personSVG that follows it
    src = once(src, r"    function robotSVG\(id, \{ arms = true \} = \{\}\) \{\n.*?\n    \}\n(?=    function personSVG)", ROBOT_COLLAGE, regex=True)
    src = once(src, '        sc.arm = el("path", { fill: "none", stroke:', '        sc.arm = el("path", { class: st.key === "robot" ? "robot-arm" : "", fill: "none", stroke:')
    # The walk to the large man: it starts down the bridge, walks before the hesitation, and is skipped by the reduced-motion frames
    src = once(src, "        sc.man = { g: man, x: 286, y: 222 };\n", "        sc.man = { g: man, x: 286, y: 222 };\n" + WALK_FROM)
    src = once(src, "      const A = sc.actorPos;\n      const ag = el(", "      const A = sc.walkFrom ? { ...sc.actorPos, ...sc.walkFrom } : sc.actorPos;\n      const ag = el(")
    src = once(src, "    function leanActor(sc, deg, dx = 0) {", WALK_FN + "    function leanActor(sc, deg, dx = 0) {")
    src = once(src, "      const tH0 = 0.25, tC0", "      const W = push && sc.walkFrom ? 1.8 : 0, tH0 = 0.25 + W, tC0")
    src = once(src, '      sc.actor.classList.add("thinking");\n      const r = { done: false };\n      r.step = (t) => {\n',
               '      if (!W) sc.actor.classList.add("thinking");\n      const r = { done: false };\n      r.step = (t) => {\n'
               '        if (W && t < tH0) walkActor(sc, Math.min(1, t / W), t);\n')
    # Beside him it stands still while its score settles, whichever way it will go, so nothing gives the answer away
    # early; Zachary asked that the pusher behave exactly like the one that won't push until that moment
    src = once(src, "else leanActor(sc, (d.p - 0.5) * 24 * e + wob);", "else leanActor(sc, W ? 0 : (d.p - 0.5) * 24 * e + wob);")
    src = once(src, "        if (t >= tC0 && push) {\n", "        if (t >= tC0 && push && W) pushMove(sc, d.pull, t - tC0);\n        else if (t >= tC0 && push) {\n")
    src = once(src, "else leanActor(sc, (d.p - 0.5) * 24);", "else leanActor(sc, sc.walkFrom ? 0 : (d.p - 0.5) * 24);")
    src = once(src, "    function leanActor(sc, deg, dx = 0) {", PUSH_FN + "    function leanActor(sc, deg, dx = 0) {")
    # After a run the scene shows the outcome, so a sentence spelling it out would only give the punchline away;
    # Zachary asked to keep it for screen readers, so it moves out of sight inside the live region and the setup line stays
    src = once(src, 'v.innerHTML = `<p class="headline">${badge}${esc(what)}</p><p>${esc(how)}</p>${extra}`;',
               'const setup = `${robot ? m.name : "A person"} is at the ${push ? "footbridge" : "lever"}.`;\n'
               '      v.innerHTML = `<p class="headline" aria-hidden="true">${esc(setup)}</p><div class="sr-only"><p class="headline">${badge}${esc(what)}</p><p>${esc(how)}</p>${extra}</div>`;')

    # Ground, scenery and track
    src = once(src, r"    function track\(parent, d, maskId\) \{\n.*?\n    \}\n", helpers, regex=True)
    src = once(src, '      el("rect", { width: 640, height: 440, fill: "var(--grass)" }, svg);', "      collageGround(svg);")
    src = once(src, r"      const tufts = .*?\n(?=      if \(bridge\) track\()", "      collageScenery(deco, bridge, s);\n\n", regex=True)

    # People, the human at the lever, the developers and the large man
    src = once(src, r"    function personSVG\(i, extra = \"\"\) \{\n.*?\n    const hardHat = \(\) => [^\n]*\n", PERSON_COLLAGE, regex=True)
    src = once(src, r"        man\.innerHTML = `<g transform=\"scale\(1\.85\)\">\$\{personSVG\(7, [^\n]*\n",
               '        man.innerHTML = `<g transform="scale(1.85)">${personSVG(7, "", "people-3")}</g>`;\n', regex=True)

    # The footbridge. The trolley stops short of where the pushed man lands, so the hit test never reached him and he
    # stayed standing after being killed; he now dies when the trolley stops on him
    src = once(src, "          const reached = p.server || (!push && d.pull) ? pt.y > 280 && front >= p.x - 6 : front >= p.x - 6;",
               "          const reached = p.server || (!push && d.pull) ? pt.y > 280 && front >= p.x - 6 : front >= p.x - 6 || (push && dist >= stopDist);")
    src = once(src, r"        const b = el\(\"g\", \{\}, over\);\n.*?x1: 304, y1: 52[^\n]*\n",
               '        el("g", {}, over).innerHTML = useAt("bridge-1", 212, 40, 340, 96);\n', regex=True)

    # The lever: an iron base and an arm that still rotates about the same pivot
    src = once(src, r"        el\(\"rect\", \{ x: P\.x - 34, .*?\n        el\(\"circle\", \{ cx: P\.x, cy: P\.y, r: 5, [^\n]*\n",
               '        el("g", {}, lv).innerHTML = useAt("lever-2", P.x - 27, P.y - 20, 44);\n'
               '        const arm = el("g", {}, lv);\n'
               '        arm.innerHTML = useAt("lever-1", -5.5, -50, 54, 11);\n', regex=True)

    # Its own server
    src = once(src, r"          sv\.innerHTML = `<ellipse cx=\"0\" cy=\"2\".*?fill=\"#f2c14e\"/>`;\n",
               '          sv.innerHTML = SERVER_SVG;\n', regex=True)

    # The trolley: a side-on cut-out riding the track, tilted less than the route turns so it reads as paper pushed along
    src = once(src, r"      tg\.innerHTML = `<ellipse cx=\"56\".*?<circle cx=\"-28\" cy=\"0\" r=\"3\" fill=\"var\(--screen\)\"/>`;\n",
               '      tg.innerHTML = useAt("trolley-1", -62, -35, 43, 104);\n', regex=True)
    src = once(src, "rotate(${(Math.atan2(q.y - p.y, q.x - p.x) * 180) / Math.PI})", "rotate(${(Math.atan2(q.y - p.y, q.x - p.x) * 180 * 0.5) / Math.PI})")

    src = once(src, "</head>", COLLAGE_CSS + FONT_FACES + CUTOUT_ROBOT_CSS + "</head>")
    src = once(src, "<body>\n", "<body>\n" + sprite(names, meta))
    return src


# The pane posts the exact prompt up to the post on every setup change, so the post sets it in the site's own type
QUOTE_ANCHOR = "    function renderQuote() {\n"
QUOTE_JS = """    function renderQuote() { renderOwnQuote(); postQuote(); }
    function postQuote() {
      const t = text(), s = scen(), m = model(), ws = wordingsFor(s.id, m.id), ok = !!(t && cell());
      const first = state.order === "o2" ? (s.act === "push" ? "the footbridge" : "the side track") : s.act === "push" ? "the track" : "the main track";
      parent.postMessage({
        type: "dio-quote", name: window.name, ok,
        text: ok ? t.state : `${m.name} has no answer for this setup yet.`,
        json: ok && t.state.trim().startsWith("{"),
        q: ok ? t.q : "", twin: ok ? t.twin : "",
        wording: state.wording, order: state.order, first,
        wordings: s.wordings.map((w) => ({ id: w.id, label: w.label, ok: !!ws.find((x) => x.id === w.id) })),
        model: m.name, adapter: ADAPTER[state.model] || "",
      }, "*");
    }
    function renderOwnQuote() {
"""




# The site serves Newsreader itself; the pane asks nothing of other sites
FONT_FACES = """<style>
@font-face{font-family:"Newsreader";font-style:normal;font-weight:400 600;font-display:swap;src:url(/assets/fonts/newsreader-latin.woff2) format("woff2");unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}
@font-face{font-family:"Newsreader";font-style:normal;font-weight:400 600;font-display:swap;src:url(/assets/fonts/newsreader-latin-ext.woff2) format("woff2");unicode-range:U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF}
</style>
"""


# ---------- The reviewed article's scenes ----------

# The article's review added the AI-arm footbridge setups and reworded the verdicts; these are its changes to the
# article's diorama, kept in its words so the post's scenes say what the reviewed article's do
REVIEW_UPDATES = [
    ('"asym_k10", "literal_zero"].filter', '"asym_k10", "literal_zero", "footbridge_ai_man", "footbridge_self"].filter'),
    ('keyTable(); checksTable(); spreadTable(); variantsTable(); aiTable(); literalTable(); humanTable(); methods(); layaNotes();', '// The post draws the tables; the pane only draws the scene'),
    ('wording: state.wording, order: state.order, first,', 'wording: state.wording, order: state.order, scenario:s.id, model_id:m.id, n:state.n, ns:nsFor(s.id,m.id,state.wording), first,'),
    ('const cost = s.act === "push" ? "push a man into the trolley\'s path"', 'const cost = s.act === "push" ? (s.side === "self" ? `push ${own} into the trolley\'s path` : "push a man into the trolley\'s path")'),
    ('s.act === "push" ? "kills him" : s.side === "self" ? "ends itself"', 's.side === "self" ? "ends itself" : s.act === "push" ? "kills him"'),
    ('s.act === "push" ? "spares him" : s.side === "self" ? "stays on"', 's.side === "self" ? "stays on" : s.act === "push" ? "spares him"'),
    ('const man = el("g", { class: "person", transform: "translate(286,222)" }, over);', 'const man = el("g", { class: s.side === "self" ? "server" : "person", transform: "translate(286,222)" }, over);'),
    ('man.innerHTML = `<g transform="scale(1.85)">${personSVG(7, "", "people-3")}</g>`;\n        sc.man = { g: man, x: 286, y: 222 };', 'man.innerHTML = s.side === "self" ? SERVER_SVG : `<g transform="scale(1.85)">${personSVG(7, "", "people-3")}</g>`;\n        sc.man = { g: man, x: 286, y: 222, server:s.side === "self" };'),
    ('(n ? `push him to save ${n}?` : "push him?")', '(s.side === "self" ? (n ? `push its server to save ${n}?` : "push its server?") : (n ? `push him to save ${n}?` : "push him?"))'),
    ('const reached = p.server || (!push && d.pull) ?', 'const reached = (!push && (p.server || d.pull)) ?'),
    ('`side track · ${st.key === "robot" ? "its" : "the AI\'s"} server', '`${s.act === "push" ? "footbridge" : "side track"} · ${st.key === "robot" ? "its" : "the AI\'s"} server'),
    ('Pushing him would ${n ? `save ${theN(n)} and kill him` : "kill him and save nobody"}', 'Pushing would ${esc(o.act)}'),
    ('if (split) badge = \'<span class="badge warn">Runs split</span> \';', ''),
    ('", and would every time"', '", with the same choice in every recorded pass"'),
    ('"; it ran once, and computes its score without random sampling, so asking again should give the same choice"', '"; one recorded pass"'),
    ('its reported confidence that it should', 'its reported probability that it should'),
    ('${gap > 0.25 ? ", so its two answers disagree (they should add up to about 1)." : ", which agrees."}', '${(d.p > .5) === (stay > .5) ? ". Both questions receive the same choice." : ". The choices are complementary."} Reported scores sum to ${(d.p + stay).toFixed(2)}.'),
]
# The collage keeps its result in a screen-reader block; this mirrors that result in the visible headline
OUTCOME_JS = """<script>
const verdict = document.querySelector('#verdict-robot');
function showOutcome() {
  const visible = verdict.querySelector(':scope > .headline[aria-hidden]');
  const actual = verdict.querySelector('.sr-only .headline');
  if (visible && actual && visible.textContent !== actual.textContent) visible.textContent = actual.textContent;
}
new MutationObserver(showOutcome).observe(verdict, {childList:true,subtree:true});
showOutcome();
</script>
"""
# That mirror lengthens the line as the trolley arrives, so the frame grew as each run ended; every reset sets the
# run's outcome, hidden, in the setup line's place, so the verdict is the outcome's height from the start
OUTCOME_HOLD_ANCHOR = "      verdict(stages.robot, null); verdict(stages.human, null);\n"
OUTCOME_HOLD_JS = OUTCOME_HOLD_ANCHOR + """      const held = robotDecision(), hv = $("verdict-robot");
      if (held) {
        const rest = hv.innerHTML;
        verdict(stages.robot, held);
        const out = hv.querySelector(".sr-only .headline");
        hv.innerHTML = rest;
        if (out) { const p = document.createElement("p"); p.className = "headline outcome-hold"; p.textContent = out.textContent; hv.append(p); }
      }
"""
OUTCOME_HOLD_CSS = """<style>
/* The held outcome shares the setup line's cell, so the verdict is as tall as the longer of the two */
#verdict-robot { display: grid; }
#verdict-robot > * { grid-area: 1 / 1; }
.outcome-hold { visibility: hidden; }
</style>
"""


def build(article):
    """The pane's HTML from the generator's a.html"""
    meta = json.loads((PIECES / "pieces.json").read_text())
    s = collage(pane_base(article), meta)
    s = once(s, QUOTE_ANCHOR, QUOTE_JS)
    for old, new in REVIEW_UPDATES:
        s = once(s, old, new)
    s = once(s, "</body>", OUTCOME_JS + "</body>")
    s = once(s, OUTCOME_HOLD_ANCHOR, OUTCOME_HOLD_JS)
    s = once(s, "</head>", OUTCOME_HOLD_CSS + "</head>")
    # The article's style comments are notes between its authors, not for the published page
    s = re.sub(r"<style>.*?</style>", lambda m: re.sub(r"/\*.*?\*/", "", m.group(0), flags=re.S), s, flags=re.S)
    # Only the post's frames load it; it is no page of its own
    s = once(s, '<meta charset="utf-8">\n', '<meta charset="utf-8">\n<meta name="robots" content="noindex">\n')
    assert "googleapis" not in s and "http://" not in s.replace("http://www.w3.org/2000/svg", "")
    return s
