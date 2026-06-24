from search_engine.tokenizer import tokenize
import re

def make_snippet(text, query, window=200):
    """Return a short excerpt of `text` around the first query-term match."""
    query_tokens = tokenize(query)
    lower_text = text.lower()

    for token in query_tokens:
        match = re.search(rf"\b{re.escape(token)}\b", lower_text)
        if match:
            start = max(0, match.start() - window)
            end = min(len(text), match.end() + window)

            snippet = text[start:end].replace("\n", " ")
            return "..." + snippet + "..."

    return text[:120].replace("\n", " ") + "..."
