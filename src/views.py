"""Embedded Jinja2 templates + CSS for the blog (no runtime filesystem).

Reuses the site's visual tokens (black/azure/gainsboro, #page-wrapper frame,
#lang-switch, back-link header) but tuned for long-form reading.
"""

from datetime import datetime

from jinja2 import Environment, DictLoader, select_autoescape

_MESES = [
    "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
]


def format_es(iso):
    """ISO 8601 -> '1 de junio de 2026'. '' si falta o es invalida.

    Sin locale (no garantizado en Pyodide): nombres de mes embebidos.
    """
    if not iso:
        return ""
    try:
        dt = datetime.fromisoformat(iso)
    except (ValueError, TypeError):
        return ""
    return f"{dt.day} de {_MESES[dt.month - 1]} de {dt.year}"

_CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body { background-color: black; color: azure; overflow-wrap: break-word; }
#lang-switch { display: flex; justify-content: flex-end; padding: 8px 20px; }
#page-wrapper { width: 90%; max-width: 760px; margin: 0 auto;
  border: 1px solid gainsboro; padding: 1.5rem; }
header { width: 100%; display: flex; justify-content: space-between;
  align-items: center; margin-bottom: 2rem; }
header a { color: azure; }
.post-body { line-height: 1.7; }
.post-body h1, .post-body h2, .post-body h3 { margin: 1.5rem 0 0.75rem; }
.post-body p { margin: 0 0 1rem; }
.post-body ul, .post-body ol { margin: 0 0 1rem 1.5rem; }
.post-body blockquote { border-left: 3px solid gainsboro; padding-left: 1rem;
  color: bisque; margin: 0 0 1rem; }
.post-body pre { background: #111; border: 1px solid gainsboro; padding: 1rem;
  overflow-x: auto; margin: 0 0 1rem; }
.post-body code { background: #111; padding: 1px 4px; }
.post-body pre code { background: none; padding: 0; }
.post-meta { color: bisque; font-size: small; margin-bottom: 1.5rem; }
.post-list { list-style: none; }
.post-list li { border-bottom: 1px solid gainsboro; padding: 1rem 0; }
.post-list a { color: azure; text-decoration: none; font-size: 1.2rem; }
.post-list .excerpt { color: bisque; font-size: small; margin-top: 4px; }
.pager { display: flex; justify-content: space-between; margin-top: 2rem; }
.pager a { color: azure; }
footer { width: 100%; text-align: center; margin-top: 3rem; }
.footer-text { font-size: small; color: bisque; }
"""

_BASE = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{% block title %}Blog — Javier Fuenzalida{% endblock %}</title>
  {% block head %}{% endblock %}
  <style>""" + _CSS + """</style>
</head>
<body>
  <div id="lang-switch"><button>ES</button><button>EN</button></div>
  <div id="page-wrapper">
    <header>
      <div class="izquierda">{% block back %}<a href="/"><strong>BLOG</strong></a>{% endblock %}</div>
      <div class="derecha"><a href="https://javierfuenzam.com"><strong>VOLVER AL SITIO</strong></a></div>
    </header>
    {% block content %}{% endblock %}
    <footer><p class="footer-text">Javier Fuenzalida Martinez</p></footer>
  </div>
</body>
</html>
"""

_LIST = """{% extends "base.html" %}
{% block content %}
<ul class="post-list">
  {% for p in items %}
  <li>
    <a href="/{{ p.slug }}">{{ p.title or "Sin titulo" }}</a>
    {% if p.published_at %}<div class="post-meta">{{ p.published_at | fmt_date }}</div>{% endif %}
    {% if p.excerpt %}<div class="excerpt">{{ p.excerpt }}</div>{% endif %}
  </li>
  {% endfor %}
</ul>
<div class="pager">
  {% if has_prev %}<a href="?page={{ page - 1 }}">&larr; Anteriores</a>{% else %}<span></span>{% endif %}
  {% if has_next %}<a href="?page={{ page + 1 }}">Siguientes &rarr;</a>{% else %}<span></span>{% endif %}
</div>
{% endblock %}
"""

_POST = """{% extends "base.html" %}
{% block title %}{{ post.title or "Sin titulo" }} — Blog{% endblock %}
{% block head %}
<meta name="description" content="{{ description }}">
<meta property="og:type" content="article">
<meta property="og:title" content="{{ post.title or 'Sin titulo' }}">
<meta property="og:description" content="{{ description }}">
<meta property="og:url" content="{{ url }}">
<meta name="twitter:card" content="summary">
{% endblock %}
{% block back %}<a href="/"><strong>VOLVER AL BLOG</strong></a>{% endblock %}
{% block content %}
<article>
  <h1>{{ post.title or "Sin titulo" }}</h1>
  {% if post.published_at %}<div class="post-meta">{{ post.published_at | fmt_date }}</div>{% endif %}
  <div class="post-body">{{ body_html | safe }}</div>
</article>
{% endblock %}
"""

_404 = """{% extends "base.html" %}
{% block content %}<p>Esta entrada no existe o no esta publicada.</p>{% endblock %}
"""

_MESSAGE = """{% extends "base.html" %}
{% block content %}<p>{{ message }}</p>{% endblock %}
"""

_env = Environment(
    loader=DictLoader({
        "base.html": _BASE,
        "list.html": _LIST,
        "post.html": _POST,
        "404.html": _404,
        "message.html": _MESSAGE,
    }),
    autoescape=select_autoescape(["html", "xml"]),
)
_env.filters["fmt_date"] = format_es


def render_list(items, page, has_prev, has_next):
    return _env.get_template("list.html").render(
        items=items, page=page, has_prev=has_prev, has_next=has_next)


def render_post(post, body_html, description, url):
    return _env.get_template("post.html").render(
        post=post, body_html=body_html, description=description, url=url)


def render_404():
    return _env.get_template("404.html").render()


def render_message(message):
    return _env.get_template("message.html").render(message=message)
