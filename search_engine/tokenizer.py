import re

STOP_WORDS = {
    "the", "and", "is", "in", "of", "to", "a", "an", "for", "on",
    "with", "as", "by", "at", "from", "this", "that", "it", "be",
    "what"
}


def tokenize(text):
    text = text.lower()
    tokens = re.findall(r"[a-z0-9]+", text)
    return [token for token in tokens if token not in STOP_WORDS]
