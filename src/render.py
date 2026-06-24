"""Markdown rendering for the blog.

mistune with escape=True escapes raw inline HTML, so post bodies cannot inject
markup (no separate sanitizer needed on the Pyodide runtime).
"""

import html as _html
import re

import mistune

_TAG_RE = re.compile(r"<[^>]+>")

_md = mistune.create_markdown(escape=True)


# Note: mistune escape=True escapes raw HTML but does NOT neutralize
# javascript: URLs in markdown links. Safe while the author is the sole
# trusted CMS user; revisit (link-scheme allowlist) if authorship widens.
def to_html(body):
    """Render markdown `body` to safe HTML."""
    if not body:
        return ""
    return _md(body)


def make_excerpt(text, n=160):
    """Plain-text summary: collapse whitespace, trim to n chars."""
    if not text:
        return ""
    collapsed = " ".join(text.split())
    if len(collapsed) <= n:
        return collapsed
    return collapsed[:n].rstrip() + "…"


def excerpt_from_markdown(body, n=160):
    """Plain-text summary from a markdown body: render, strip tags, collapse,
    trim. Used for <meta description>/OG cards so markdown syntax never leaks."""
    if not body:
        return ""
    text = _TAG_RE.sub(" ", to_html(body))
    text = _html.unescape(text)
    return make_excerpt(text, n)
