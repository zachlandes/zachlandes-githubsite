---
title: Placeholder post
description: A stand-in that exercises every part of the post layout before the first real post.
date: 2026-10-03
---

This page is a placeholder.
It isn't listed on the home page, in the feed or in llms.txt, and it asks search engines not to index it.
It exists to check that the post layout holds every kind of block a post can use: prose with [links](https://zachlandes.com/), *emphasis*, `inline code` and margin notes, headings, quotes, lists, figures, a table, a collapsible section and an interactive block.

## Prose and lists

A section heading is an H2; the contents in the left margin are built from these headings on wide screens.

<div class="has-note">
<p>A paragraph can carry a margin note.<sup class="ref"><a href="#note-1" id="ref-1" aria-label="Note 1">1</a></sup><span class="sidenote" aria-hidden="true"><span class="n">1</span>On a wide screen the note hangs in the right margin beside its line.</span> On a phone the same note drops below the paragraph as a numbered footnote.</p>
<aside class="note" id="note-1"><span class="n" aria-hidden="true">1</span>On a wide screen the note hangs in the right margin beside its line.</aside>
</div>

1. An ordered list
2. with a second item

- An unordered list
- with a second item

> A block quote is set out from the prose, boxed with an offset block behind it.

### A subsection

An H3 sits under its section in the contents.

## Figures

<figure class="wide">
<svg viewBox="0 0 760 390" role="img" aria-label="A placeholder figure: three bars of increasing height">
  <rect x="0" y="0" width="760" height="390" fill="none" stroke="currentColor" stroke-opacity=".2"/>
  <rect x="120" y="230" width="120" height="120" fill="currentColor" fill-opacity=".25"/>
  <rect x="320" y="150" width="120" height="200" fill="currentColor" fill-opacity=".45"/>
  <rect x="520" y="70" width="120" height="280" fill="var(--accent)"/>
</svg>
<figcaption>A wide figure is an inline SVG with a caption; it may run wider than the text on desktop.</figcaption>
</figure>

<figure class="wide" id="toggle-figure">
<svg viewBox="0 0 760 200" role="img" aria-label="A placeholder figure: a circle that moves when a button is pressed">
  <line x1="80" y1="100" x2="680" y2="100" stroke="currentColor" stroke-opacity=".3" stroke-width="2"/>
  <circle id="toggle-dot" cx="80" cy="100" r="22" fill="var(--accent)"/>
</svg>
<div class="dio-actions">
  <button class="go" type="button" id="toggle-go">Move the dot</button>
</div>
<figcaption>An interactive block: a script in the post drives the figure.</figcaption>
</figure>
<script>
(()=>{
  const dot=document.getElementById('toggle-dot');
  document.getElementById('toggle-go').addEventListener('click',()=>dot.setAttribute('cx',dot.getAttribute('cx')==='80'?'680':'80'));
})();
</script>

## Table and details

<div class="table-box scroller" tabindex="0" role="region" aria-label="Placeholder table">
<table>
  <thead><tr><th scope="col">Row</th><th scope="col">First</th><th scope="col">Second</th><th scope="col">Third</th></tr></thead>
  <tbody>
    <tr><td>One</td><td>1</td><td>10</td><td>100</td></tr>
    <tr><td>Two</td><td>2</td><td>20</td><td>200</td></tr>
    <tr><td>Three</td><td>3</td><td>30</td><td>300</td></tr>
    <tr><td>Four</td><td>4</td><td>40</td><td>400</td></tr>
    <tr><td>Five</td><td>5</td><td>50</td><td>500</td></tr>
  </tbody>
</table>
</div>

<details>
  <summary>A collapsible section</summary>
  <div class="details-body">
    <p>Secondary material stays folded until a reader opens it.</p>
  </div>
</details>
