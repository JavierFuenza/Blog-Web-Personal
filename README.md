# Blog-Web-Personal

Server-rendered markdown blog. Cloudflare Python Worker (FastAPI on Pyodide),
served at `blog.javierfuenzam.com`. Consumes the public API
(`api.javierfuenzam.com`) and renders post markdown with mistune.

## Dev

```bash
uv run pytest            # pure-logic tests
uv run pywrangler dev    # local worker
uv run pywrangler deploy
```

Routes: `/` (paginated list), `/{slug}` (post), `/rss.xml` (feed).
