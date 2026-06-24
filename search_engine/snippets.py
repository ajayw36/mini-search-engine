from search_engine.tokenizer import tokenize
import re
from pathlib import Path

def make_snippet(text, query, window=50):
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

def get_title(doc_path, text):
    """Returns the title of a document, either from the title in the document or the filename"""
    for line in text.splitlines():
        if line.startswith('#'):
            return line[2:].strip()

    return Path(doc_path).stem.replace("-", " ").title()