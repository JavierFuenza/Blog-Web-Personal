import xml.etree.ElementTree as ET
from src import feed

POSTS = [
    {"slug": "hola-mundo", "title": "Hola & Mundo",
     "published_at": "2026-06-01T10:00:00", "excerpt": "primer post"},
    {"slug": "segundo", "title": "Segundo",
     "published_at": "2026-06-02T12:30:00", "excerpt": "otro"},
]


def test_build_rss_is_well_formed():
    xml = feed.build_rss(POSTS, "https://blog.javierfuenzam.com")
    root = ET.fromstring(xml)  # raises if malformed
    assert root.tag == "rss"


def test_build_rss_has_item_per_post():
    xml = feed.build_rss(POSTS, "https://blog.javierfuenzam.com")
    root = ET.fromstring(xml)
    items = root.findall("./channel/item")
    assert len(items) == 2


def test_build_rss_links_use_slug():
    xml = feed.build_rss(POSTS, "https://blog.javierfuenzam.com")
    assert "https://blog.javierfuenzam.com/hola-mundo" in xml


def test_build_rss_escapes_titles():
    xml = feed.build_rss(POSTS, "https://blog.javierfuenzam.com")
    assert "Hola &amp; Mundo" in xml
    assert "Hola & Mundo" not in xml
