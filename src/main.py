"""Blog Worker: FastAPI on Pyodide. SSR list/post pages + RSS, consuming the
public API over async fetch."""

from workers import WorkerEntrypoint
import asgi
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, Response

import api_client
import render
import pagination
import feed
import views

app = FastAPI()

PAGE_SIZE = 10
RSS_SIZE = 20
SITE_URL = "https://blog.javierfuenzam.com"


def _base(request):
    return request.scope["env"].API_BASE


@app.get("/", response_class=HTMLResponse)
async def list_page(request: Request, page: int = 1):
    page = max(1, page)
    offset = pagination.page_to_offset(page, PAGE_SIZE)
    rows = await api_client.get_posts(_base(request), PAGE_SIZE + 1, offset)
    items, has_next = pagination.paginate(rows, PAGE_SIZE)
    return HTMLResponse(views.render_list(items, page, page > 1, has_next))


@app.get("/rss.xml")
async def rss(request: Request):
    rows = await api_client.get_posts(_base(request), RSS_SIZE, 0)
    xml = feed.build_rss(rows, SITE_URL)
    return Response(content=xml, media_type="application/rss+xml")


@app.get("/{slug}", response_class=HTMLResponse)
async def post_page(request: Request, slug: str):
    post = await api_client.get_post_by_slug(_base(request), slug)
    if post is None:
        return HTMLResponse(views.render_404(), status_code=404)
    body_html = render.to_html(post.get("body"))
    description = render.make_excerpt(post.get("body") or "")
    url = f"{SITE_URL}/{slug}"
    return HTMLResponse(views.render_post(post, body_html, description, url))


class Default(WorkerEntrypoint):
    async def fetch(self, request):
        return await asgi.fetch(app, request, self.env)
