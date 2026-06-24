from src import pagination


def test_page_to_offset_first_page():
    assert pagination.page_to_offset(1, 10) == 0


def test_page_to_offset_third_page():
    assert pagination.page_to_offset(3, 10) == 20


def test_page_to_offset_clamps_below_one():
    assert pagination.page_to_offset(0, 10) == 0
    assert pagination.page_to_offset(-5, 10) == 0


def test_paginate_detects_next_page():
    rows = list(range(11))  # limit+1 rows fetched
    items, has_next = pagination.paginate(rows, 10)
    assert items == list(range(10))
    assert has_next is True


def test_paginate_last_page():
    rows = list(range(4))
    items, has_next = pagination.paginate(rows, 10)
    assert items == list(range(4))
    assert has_next is False
