"""Pagination helpers. The route fetches `limit + 1` rows and uses paginate()
to decide whether a next page exists without a separate count query."""


def page_to_offset(page, limit):
    page = max(1, page)
    return (page - 1) * limit


def paginate(rows, limit):
    """Given up to limit+1 rows, return (items[:limit], has_next)."""
    has_next = len(rows) > limit
    return rows[:limit], has_next
