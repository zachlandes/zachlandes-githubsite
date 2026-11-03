#!/usr/bin/env python3
# Fail if the built site's crawl files disagree with its pages
# The sitemap must list exactly the pages search engines may index, robots.txt must point at it,
# and the home page's structured data must parse and name the Person and WebSite
# Usage: check-built-site.py [built site directory]   (default: _site)
import json
import os
import re
import sys
from urllib.parse import urlparse
from xml.etree import ElementTree

NOINDEX = re.compile(r'<meta name="robots" content="[^"]*noindex', re.I)
CANONICAL = re.compile(r'<link rel="canonical" href="([^"]+)"')
JSON_LD = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)
SITEMAP_NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def page_path(rel):
    path = "/" + rel.replace(os.sep, "/")
    return path[: -len("index.html")] if path.endswith("/index.html") else path


def indexable_paths(root):
    paths = set()
    for dirpath, _, names in os.walk(root):
        for name in names:
            if not name.endswith(".html"):
                continue
            rel = os.path.relpath(os.path.join(dirpath, name), root)
            html = read(os.path.join(dirpath, name))
            # GitHub Pages serves 404.html for missing addresses, never at its own address
            if rel == "404.html" or NOINDEX.search(html):
                continue
            canonical = CANONICAL.search(html)
            paths.add(urlparse(canonical.group(1)).path if canonical else page_path(rel))
    return paths


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "_site"
    problems = []

    try:
        sitemap = ElementTree.parse(os.path.join(root, "sitemap.xml"))
    except (OSError, ElementTree.ParseError) as e:
        sys.exit(f"sitemap.xml is missing or unreadable: {e}")
    listed = [urlparse(loc.text).path for loc in sitemap.iter(SITEMAP_NS + "loc")]
    indexable = indexable_paths(root)
    for path in sorted(set(listed) - indexable):
        problems.append(f"sitemap.xml lists {path}, which is missing or asks not to be indexed")
    for path in sorted(indexable - set(listed)):
        problems.append(f"sitemap.xml leaves out {path}, which search engines may index")

    if not re.search(r"^Sitemap: \S+/sitemap\.xml$", read(os.path.join(root, "robots.txt")), re.M):
        problems.append("robots.txt does not name the sitemap")

    blocks = JSON_LD.findall(read(os.path.join(root, "index.html")))
    types = set()
    for block in blocks:
        try:
            data = json.loads(block)
        except json.JSONDecodeError as e:
            problems.append(f"the home page's JSON-LD does not parse: {e}")
            continue
        types.update(node.get("@type") for node in data.get("@graph", [data]))
    for wanted in ("Person", "WebSite"):
        if wanted not in types:
            problems.append(f"the home page's JSON-LD has no {wanted}")

    for problem in problems:
        print(problem, file=sys.stderr)
    if problems:
        sys.exit(1)
    print(f"sitemap.xml lists the {len(listed)} indexable pages; robots.txt and the home page's JSON-LD are in place")


if __name__ == "__main__":
    main()
