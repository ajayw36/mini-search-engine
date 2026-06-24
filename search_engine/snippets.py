"""Generate short text snippets around query matches for search results.

Not yet implemented. The intent is: given a document's text and the query,
return a short excerpt centered on the first matching term so it can be shown
beneath each search result.
"""


def make_snippet(text, query, max_length=200):
    """Return a short excerpt of `text` around the first query-term match.

    TODO: implement snippet extraction (find a query term in `text`, slice a
    window of roughly `max_length` characters around it, trim to word
    boundaries, and optionally highlight the match).
    """
    raise NotImplementedError("snippet generation is not implemented yet")
