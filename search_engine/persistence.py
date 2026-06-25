"""Persist and load index/scores to avoid recomputation."""

import pickle
import os
from pathlib import Path

CACHE_DIR = Path(__file__).parent.parent / ".search_cache"
INDEX_FILE = CACHE_DIR / "index.pkl"
DOC_LENGTHS_FILE = CACHE_DIR / "doc_lengths.pkl"
SCORES_FILE = CACHE_DIR / "scores.pkl"
METADATA_FILE = CACHE_DIR / "metadata.pkl"


def ensure_cache_dir():
    """Create cache directory if it doesn't exist."""
    CACHE_DIR.mkdir(exist_ok=True)


def save_index(index, document_lengths, scores, metadata):
    """Save index, document lengths, scores, and metadata to disk."""
    ensure_cache_dir()
    with open(INDEX_FILE, "wb") as f:
        pickle.dump(index, f)
    with open(DOC_LENGTHS_FILE, "wb") as f:
        pickle.dump(document_lengths, f)
    with open(SCORES_FILE, "wb") as f:
        pickle.dump(scores, f)
    with open(METADATA_FILE, "wb") as f:
        pickle.dump(metadata, f)


def load_index():
    """Load index, document lengths, scores, and metadata from disk.

    Returns (index, document_lengths, scores, metadata) or (None, None, None, None) if not cached.
    """
    if not all(f.exists() for f in [INDEX_FILE, DOC_LENGTHS_FILE, SCORES_FILE, METADATA_FILE]):
        return None, None, None, None

    with open(INDEX_FILE, "rb") as f:
        index = pickle.load(f)
    with open(DOC_LENGTHS_FILE, "rb") as f:
        document_lengths = pickle.load(f)
    with open(SCORES_FILE, "rb") as f:
        scores = pickle.load(f)
    with open(METADATA_FILE, "rb") as f:
        metadata = pickle.load(f)

    return index, document_lengths, scores, metadata


def clear_cache():
    """Clear the cached index."""
    for f in [INDEX_FILE, DOC_LENGTHS_FILE, SCORES_FILE, METADATA_FILE]:
        if f.exists():
            f.unlink()
