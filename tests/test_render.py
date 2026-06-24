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
