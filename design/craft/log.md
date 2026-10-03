# design-craft run log

Skill: design-craft draft (dotfiles PR #66), first trial on a content site.
Brief: `design/paradigm-brief.md`; requirements: `design/craft/requirements.md`.
Variants, screenshots and review boards live outside this public repository, in firstmate's task folder for this run, because they carry unpublished article text.

## 2026-10-02 Pre-Discover: plan review

The captain asked to see the plan before any variant is built.
Proposed mix: two seed-string variants, three research variants (plain-text essayists; annotated long-form; interactive explainers), and a sixth that is either human-steered or a third seed.
Answers so far:
Captain, on the board: "since this is my personal blog, i may want to have a bio page that has a slightly longer bio, not sure." An About page was added to the requirements, droppable at the copy rewrite.
Captain, on question 3 (human-steered variant): "only if i dont like what we get from the seeds". Variant F becomes a third seed; the steered variant is offered again at the Discover gate.
Captain, on question 1 (brief and requirements): "yes".
Captain, on question 2 (mix): "3 seed variants, steered variant later possibly from foundation laid by seed variants or research variants".
Plan gate passed: variants A, B and F from seed strings; C, D and E research-derived; a steered variant possibly after the side-by-side, built on whichever foundation he likes.

## 2026-10-02 Discover

Every variant was built by a fresh Opus subagent in parallel, from the same requirements and the same content pack (the captain's trolley prose and the real figures, extracted in light and dark).
Each one was checked at 390 × 844 and 1440 × 900, light and dark; none scrolls sideways on a phone, and none needed a fix.

| Variant | Source | Direction |
| --- | --- | --- |
| A | Seed `pG6Pafy6ui3KpEWN5rNNaJoJXsgwjQFednawfch0xfMU8LJ6tKRIuOmWp4n2lRi6` | Newsreader with IBM Plex Mono for numbers; 8-column home; teal links, mint margin note, ten-tick dashed rule |
| B | Seed `ReJGZLMracGFpWbIABuxw1TX88GsggYaVqGdsJKdHA7jzWI7SpDuC0mhJ2eERBe0` | Space Grotesk, Newsreader and JetBrains Mono; double-rule "rails" ornament; burnt-orange accent; sticky name column |
| C | Research: plain-text essayists (danluu.com, lucumr.pocoo.org, eli.thegreenplace.net, hillelwayne.com, simonwillison.net) | One 680px Source Serif column, ISO date gutter, one accent colour from the figures |
| D | Research: annotated long-form (gwern.net, brandur.org, maggieappleton.com) | Kicker and labelled metadata row; 260px right-margin note folding under its paragraph on a phone; figures span column plus margin |
| E | Research: interactive explainers (joshwcomeau.com, overreacted.io, jvns.ca, fasterthanli.me) | Post list as a dotted track; sticky contents rail; overhanging figure panel; offset-block callouts |
| F | Seed `fKMmlLrV2Lq5rH2LHPS7ll0cAA8ogbwVEjZV6JvE4N0GQxGguql1slPHtZTMX1bw` | Atkinson Hyperlegible Next and Mono; 8-column grid; double hairline; teal controls, figure red for data |

The three seed variants converged: each read the 64-character string as an 8 × 8 grid and set the name beside the post list.
No blind critic ranking was run in Discover.

Proposed reference designs for Define: maggieappleton.com essay (desktop), joshwcomeau.com post header (desktop), lucumr.pocoo.org post (desktop), brandur.org essay body (desktop), hillelwayne.com post (phone).

Captain, on the board: "My favourite two are E and A What should we do next?"
Options offered: E's structure with A's type and colour (recommended), E alone, or A alone.
Captain: "Mock uh your first example. I'd be curious to see it"

| G | Combination of E (structure) and A (type and colour) | E's track post list, header, contents rail, overhanging figure panels and margin note; A's Newsreader and Plex Mono, paper and dark backgrounds, teal links, mint note and flat details |

Captain: "Something I liked about H was how it had like a quote that popped out in orange whether we change the highlight colors, uh, I do like being able to have those kind of like set out um quotes."
Read as E, the only variant with a set-out quote in orange; E's boxed quote with an offset block was added to G, shown in teal and orange.

Captain: "if quote is orange, then all highlight color should be that orange"
Built "G in orange": G with every accent (links, track, contents rail, margin note, quote) in the figures' orange-red; G itself stays teal.

Captain: "I like G in orange. A few questions: Whats going on with those "Consequences, JSOn, terse, in words" beige badges that do nothing? and second, should my about section use a photo"
Direction picked: G in orange.
Answered: the badges were the four wording names set as inline code in the content pack; they become plain text in Define. Recommended a small photo on About only; the one real photo of him on the current site is `img/about/main.jpg` (2019), and he was asked for a current head-and-shoulders photo.
Still open at the gate: the reference set, and code-only Define.

Captain: "you can use the photo of me from my old website design". The About page gets `img/about/main.jpg`, cropped to head and shoulders; added to the requirements.

Captain: "why crop it to head and shoulders?" Explained (a full-length shot at a small size leaves the face a few pixels tall) and offered the whole photo shown wider instead; framing left open for Define.

Captain asked what Define is; explained the three stages and restated the two open questions.
Captain: "those two are a good bar yes", read as yes to both.

Gate passed (2026-10-03):
- Direction: G in orange (E's structure, A's type, every accent in the figures' orange-red, E's set-out quote).
- Changes carried into Define: the four wording names become plain text, not code; About page gets `img/about/main.jpg`, framing to be picked in Define.
- References: maggieappleton.com essay (desktop), joshwcomeau.com post header (desktop), lucumr.pocoo.org post (desktop), brandur.org essay body (desktop), hillelwayne.com post (phone).
- Imagery: none; Define is code-only, no key given.
- Steered variant: not needed.
- No blind ranking was run in Discover.
- Captain clarified "sorry, those five": the five references are confirmed.
- Captain: "you can use ai generated images or motion via my openai subscription (not api)". No image-generation route through the subscription exists on this machine: `pi` signs in with it but has no image output, and the Codex CLI is not installed. The requirements also rule out images that are not content. Define stays code-only; imagery can be revisited in Deliver with an API key.

## 2026-10-03 Define

Builder: an Opus subagent continued across rounds, working on a copy of G in orange outside the repository.
Starting point (before round 0): the four wording names became plain text; the About page shows the whole photo (`about-crop.html` holds the cropped alternative).
Template: `prompts/critic-ranked.md`, with the five confirmed references.
Each round screenshots five fixed states, light scheme: home desktop, post top desktop, post mid-article desktop, post top phone, home phone.
Frozen prompt shasum: `a2d52381ec212918b92476ff3e03219cc839f266`.
Full critiques are kept with the variants outside this public repository, because they quote unpublished article text.
Added to the requirements before round 1: the post's figures and copy are the author's content, so the builder frames them and never redraws or rewrites them.

| Round | Fable | Astra | Fable rank | Astra rank | Critique sent to builder | Note |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 6 | 8 | ref-1 > ref-4 > ref-2 > screen-2 > screen-4 > ref-3 > screen-1 > screen-5 > screen-3 > ref-5 | ref-4 > ref-1 > screen-2 > ref-2 > screen-1 > screen-4 > screen-3 > screen-5 > ref-3 > ref-5 | Fable | Astra verified: full prompt with ten full-size screenshots worked first try |
| 1 | 6 | 7 | ref-1 > ref-2 > ref-4 > screen-2 > screen-4 > screen-1 > screen-5 > ref-3 > screen-3 > ref-5 | ref-4 > ref-1 > ref-2 > screen-2 > screen-1 > screen-5 > screen-4 > screen-3 > ref-3 > ref-5 | Fable | Builder had dropped the set-out quote; restored from a new "Decided by Zachary" requirement before scoring. Both critics again rank the chart screen lowest, on the chart's internals, which the builder may not change |
| 2 | 7 | 8 | ref-1 > screen-4 > screen-2 > ref-2 > screen-1 > ref-4 > screen-3 > screen-5 > ref-3 > ref-5 | Reference 1 > Reference 4 > Design under review 1 > Reference 2 > Design under review 2 > Design under review 4 > Design under review 5 > Design under review 3 > Reference 3 > Reference 5 | Fable | Fable rose from round 0 (6 to 7), so the round-2 check passes. Builder could not do three asks: redraw the chart (author's figure), drop the author name (required at rest), true small caps (Newsreader has none) |
| 3 (invalid) | 6 | 7 | ref-2 > ref-1 > ref-4 > screen-2 > screen-3 > screen-4 > screen-1 > screen-5 > ref-3 > ref-5 | Reference 4 > Reference 2 > Reference 1 > Screen 1 > Screen 2 > Screen 3 > Screen 5 > Screen 4 > Reference 3 > Reference 5 | none | screen-3 duplicated screen-2: the redrawn chart changed its viewBox and the screenshot locator missed it; locator fixed and the round re-scored |
| 3 | 7 | 8 | ref-1 > ref-2 > screen-3 > screen-2 > screen-1 > ref-4 > ref-3 > screen-4 > screen-5 > ref-5 | Reference 1 > Reference 4 > Screen 2 > Reference 2 > Screen 1 > Screen 4 > Screen 3 > Screen 5 > Reference 3 > Reference 5 | Fable | Chart restyled with the captain's leave; IM Fell English added as a signature face; both critics flag its swash italic |
- Captain: "i think you need to use codex cli to do it, so let's set that up." Escalated to firstmate (machine-wide tool install); Define continues code-only meanwhile.
- Firstmate, 2026-10-03: Codex CLI installed, audited and signed in on the captain's ChatGPT plan; image generation verified (`codex exec --skip-git-repo-check --model gpt-6.1-sol '$imagegen <prompt>'`). Define stays code-only; imagery only if a direction genuinely calls for it, under the no-images-that-are-not-content requirement.
- Captain, during round 3: "you can improve the trolley chart if it improves the score!" The own-server chart may now be restyled with its data unchanged; its key, which the content pack had left out, was added to the requirements.
- The key line first had the filled and hollow marks swapped; the builder caught it against the figure's own labels, and the line was corrected from the article's styles (stranger hollow, own server filled accent).
- Captain, on Codex imagery: "not sure that's relevant for this". No generated imagery for the site.
