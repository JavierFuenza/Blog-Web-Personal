from src import render


def test_to_html_renders_markdown():
    html = render.to_html("# Hola\n\nun **parrafo**.")
    assert "<h1>Hola</h1>" in html
    assert "<strong>parrafo</strong>" in html


def test_to_html_escapes_raw_html():
    html = render.to_html("hola <script>alert(1)</script>")
    assert "<script>" not in html
    assert "&lt;script&gt;" in html


def test_make_excerpt_truncates_and_strips_newlines():
    text = "Linea uno\nLinea dos\n\n" + ("x" * 300)
    out = render.make_excerpt(text, n=50)
    assert "\n" not in out
    assert len(out) <= 51  # 50 chars + optional ellipsis char


def test_make_excerpt_empty():
    assert render.make_excerpt("") == ""


def test_excerpt_from_markdown_strips_syntax():
    out = render.excerpt_from_markdown(
        "## Hola\n\nun texto **fuerte** y un [link](http://ej.com)")
    assert "#" not in out
    assert "*" not in out
    assert "http://ej.com" not in out   # link target dropped, text kept
    assert "Hola" in out
    assert "fuerte" in out
    assert "link" in out


def test_excerpt_from_markdown_empty():
    assert render.excerpt_from_markdown("") == ""
