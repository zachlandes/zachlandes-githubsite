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

Gate: pending.
