"""Async HTTP client over the Worker runtime's js.fetch.

requests/httpx (sync) are unsupported on Python Workers; only async fetch works.
"""

from js import fetch


async def _get_json(url):
    resp = await fetch(url)
    if resp.status == 404:
        return None
    if not resp.ok:
        raise RuntimeError(f"upstream {resp.status} for {url}")
    data = await resp.json()
    return data.to_py()


async def get_posts(base, limit, offset):
    url = f"{base}/api/posts?limit={limit}&offset={offset}"
    rows = await _get_json(url)
    return rows or []


async def get_post_by_slug(base, slug):
    return await _get_json(f"{base}/api/entries/by-slug/{slug}")
