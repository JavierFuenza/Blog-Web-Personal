from src import views

ITEMS = [
    {"slug": "hola", "title": "Hola", "published_at": "2026-06-01T10:00:00",
     "excerpt": "primer post"},
]
POST = {"slug": "hola", "title": "Hola Mundo",
        "published_at": "2026-06-01T10:00:00"}


def test_render_list_links_to_posts():
    html = views.render_list(ITEMS, page=1, has_prev=False, has_next=True)
    assert 'href="/hola"' in html
    assert "Hola" in html


def test_render_list_next_prev_visibility():
    first = views.render_list(ITEMS, page=1, has_prev=False, has_next=True)
    assert "?page=2" in first
    assert "?page=0" not in first  # no prev on page 1

    mid = views.render_list(ITEMS, page=3, has_prev=True, has_next=False)
    assert "?page=2" in mid       # prev -> page 2
    assert "?page=4" not in mid    # no next


def test_render_post_includes_body_and_meta():
    html = views.render_post(
        POST, body_html="<p>cuerpo</p>",
        description="resumen", url="https://blog.javierfuenzam.com/hola")
    assert "<p>cuerpo</p>" in html
    assert "<title>Hola Mundo" in html
    assert '<meta name="description" content="resumen"' in html
    assert 'property="og:title" content="Hola Mundo"' in html
    assert 'property="og:url" content="https://blog.javierfuenzam.com/hola"' in html


def test_render_post_escapes_title_in_meta():
    post = {"slug": "x", "title": 'A "quote" & amp', "published_at": ""}
    html = views.render_post(post, "<p>b</p>", "d", "https://blog.javierfuenzam.com/x")
    assert 'A "quote" & amp' not in html  # autoescaped by jinja


def test_format_es_formats_iso():
    assert views.format_es("2026-06-01T10:00:00") == "1 de junio de 2026"


def test_format_es_blank_for_missing_or_invalid():
    assert views.format_es(None) == ""
    assert views.format_es("") == ""
    assert views.format_es("no-es-fecha") == ""


def test_render_list_formats_date():
    html = views.render_list(ITEMS, page=1, has_prev=False, has_next=True)
    assert "1 de junio de 2026" in html
    assert "2026-06-01T10:00:00" not in html  # no se muestra el ISO crudo


def test_render_list_hides_meta_when_no_date():
    items = [{"slug": "x", "title": "X", "published_at": None, "excerpt": "e"}]
    html = views.render_list(items, page=1, has_prev=False, has_next=False)
    assert "None" not in html       # no imprime None/null crudo
    assert 'class="post-meta"' not in html  # div de fecha omitido si no hay fecha


def test_render_404_has_message():
    html = views.render_404()
    assert "no existe" in html.lower()


def test_render_message_shows_text():
    html = views.render_message("No se pudieron cargar las entradas.")
    assert "No se pudieron cargar las entradas." in html
