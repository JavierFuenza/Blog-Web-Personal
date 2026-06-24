"""RSS 2.0 feed builder. Pure string assembly with XML escaping."""

from datetime import datetime
from email.utils import format_datetime
from xml.sax.saxutils import escape


def _rfc822(iso):
    try:
        return format_datetime(datetime.fromisoformat(iso))
    except (ValueError, TypeError):
        return ""


def _item(post, site_url):
    link = f"{site_url}/{post['slug']}"
    pub = _rfc822(post.get("published_at"))
    pubdate = f"<pubDate>{escape(pub)}</pubDate>" if pub else ""
    return (
        "<item>"
        f"<title>{escape(post.get('title') or '')}</title>"
        f"<link>{escape(link)}</link>"
        f"<guid>{escape(link)}</guid>"
        f"{pubdate}"
        f"<description>{escape(post.get('excerpt') or '')}</description>"
        "</item>"
    )


def build_rss(posts, site_url):
    items = "".join(_item(p, site_url) for p in posts)
    return (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<rss version="2.0">'
        "<channel>"
        "<title>Blog — Javier Fuenzalida</title>"
        f"<link>{escape(site_url)}</link>"
        "<description>Notas y escritos.</description>"
        f"{items}"
        "</channel>"
        "</rss>"
    )
