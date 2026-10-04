# zachlandes.com

Zach Landes's blog: a plain Jekyll site that GitHub Pages builds from the root of `master`.
There's no theme; `_layouts`, `_includes` and `assets/site.css` are the whole design.

## Writing a post

Add `_posts/YYYY-MM-DD-short-name.md` (or `.html`) with a title and a one-line description:

```yaml
---
title: The post's title
description: One line that appears under the title, on the home page, in link previews and in the feed.
---
```

The address is `/short-name/`.
Section headings (`##`) become the contents list in the left margin on wide screens.
Posts can hold raw HTML and scripts, so interactive figures work; `figure.wide`, `.table-box`, `details` and the margin-note markup in `_unlisted/placeholder.md` show the patterns the stylesheet supports.

To share a post without listing it, put it in `_unlisted/short-name.md` instead (a `date:` goes in its front matter).
It gets the same layout and a working address, but stays off the home page, the feed and `llms.txt`, and asks search engines not to index it.
Moving it into `_posts` with a dated file name publishes it.

## Previewing

`bundle install && bundle exec jekyll serve` builds the site locally with the same gems GitHub Pages uses.
Every pull request is also built by `.github/workflows/pages-build.yml`, so a broken build shows on the PR before it merges.

## What else is here

- `feed.xml`, `robots.txt` and `llms.txt` are generated from the posts; every crawler and AI agent is allowed.
- The email link is assembled by a script as the page loads, so the address never appears in the page source.
- `assets/fonts` holds Newsreader under the SIL Open Font License.
- `design/` records how the design was made; it isn't part of the built site.
