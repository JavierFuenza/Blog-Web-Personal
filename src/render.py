"""Markdown rendering for the blog.

mistune with escape=True escapes raw inline HTML, so post bodies cannot inject
markup (no separate sanitizer needed on the Pyodide runtime).
"""

import mistune

_md = mistune.create_markdown(escape=True)


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
