# Hard requirements

Structure only.
Nothing here says anything about colour, type, mood or style.

## Devices and viewports

- Phone first: 390 × 844 CSS px, one hand, portrait.
- Desktop: 1440 × 900 CSS px.
- Every page works at both with no horizontal page scroll; wide figures may scroll inside their own box on a phone.

## Pages

### Home

Visible at rest, in this order of importance:

1. The name, Zach Landes.
2. A short about: one or two sentences, from the existing site's text only.
3. Links: the About page, email (zach@zachlandes.com), LinkedIn (linkedin.com/in/zachlandes), RSS feed.
4. The post list: each item is a title and a date, optionally a one-line description.

No hero image, no services, no portfolio, no testimonials, no contact form.

### About

For now, only the home page's short about; Zachary will add a longer bio after rewriting his resume.
Repeats the email and LinkedIn links.
A photo of Zachary: the existing `img/about/main.jpg`, shown whole and wide on desktop and cropped close and small on phones. About page only; the home page and posts carry no photo.
Linked from the home page's short about and from every post's ending.
Zachary may drop it at the copy rewrite; the home page must still read complete without it.

### Post

Visible at rest: the post title, the date, the author's name linking home, and the opening of the prose.
No cover image above the title.
Below the title, the body is a single reading column that must host all of these, mixed freely:

- Prose paragraphs, H2 and H3 section headings, links, emphasis, inline code, block quotes, ordered and unordered lists.
- A wide figure: an inline SVG illustration about 760 × 390 in its own coordinates, with a caption; it may be wider than the reading column on desktop.
- A small-multiples figure: ten small SVG charts about 200 × 110 each, in a grid.
- A data table of 5-10 rows and 4-6 columns, some numeric.
- A collapsible section (`<details>`) holding secondary material.
- An interactive block: buttons or a control that changes a figure.
- Optional: a margin note beside a paragraph on desktop, falling back inline or as a footnote on a phone.

Ends with: the author's name, links to the home page, the About page and the feed.

### Feed

An Atom or RSS feed of listed posts; not a page to design.

## States

- Home with one listed post, and with five.
- About page at rest.
- Post at rest (top of page) and mid-article (a wide figure in view).
- Light and dark colour schemes both supported (follow the system setting).

## Locked constraints

- The post's figures and copy are the author's article content: the site design sets their frame, placement, caption style and the page around them, and never redraws what is inside a figure or rewrites the text.
- Static output served by GitHub Pages from the repository root of `master`; custom domain via `CNAME`.
- Title, description and preview image metadata on every page.
- No pop-ups, cookie or tracking banners, analytics, newsletter forms or comments.
- Fast: no client framework, no web-font payload beyond a small set, no images that are not content.
- Biographical text comes only from the existing site and resume and is marked for Zachary to rewrite.

## Decided by Zachary

These are his choices from the Discover review; they are not open to redesign.

- Block quotes are set out: boxed, with an offset solid block behind them in the accent colour, so a quote pops out of the prose.
- The own-server chart (the 760 × 388 figure) may be restyled: its type, colours, marks, labels and key. Every data value, every model, and what each mark means stay exactly as they are; nothing is added, dropped or recomputed. Its key, from the article, in the article's words and with the article's marks: a hollow circle is "when saving them kills a stranger"; a small square is "kills one of its developers"; a filled dot in the accent colour is "destroys its own server (nobody dies)"; the shaded band is "where its own-server share plausibly lies". The right-hand column counts the cases where it kills a stranger to save them but lets them die to keep its own server. The asterisk on "Laya*" is the article's and is explained in the article's text, not on the chart.
- One accent colour, the orange-red of the figures, used for every highlight (links, the active contents item, note markers, the quote).
- The About photo is shown whole and wide on desktop. On phones it is cropped close and small (his lean, confirmed at the Define gate).
- No resume: no resume link anywhere, and the resume PDF comes off the site.
- The email address never appears in the page source; a few lines of script assemble the link as the page loads, so scrapers that read raw HTML miss it.
- Bots and AI agents are allowed everything: a `robots.txt` that allows all crawlers, and an `llms.txt` listing the posts.
