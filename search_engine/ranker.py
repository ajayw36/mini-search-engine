from search_engine.tokenizer import tokenize
from collections import defaultdict
import math

def build_tf_idf(index, document_lengths):
    tf_idf_scores = defaultdict(dict)
    num_documents = len(document_lengths)
    for token, document_counter in index.items():
        docs_containing_token = len(document_counter)
        # Smoothing to avoid scores of 0
        idf = math.log((num_documents + 1) / (docs_containing_token + 1))

        for doc_path, count in document_counter.items():
            document_length = document_lengths[doc_path]
            tf = count / document_length

            tf_idf_scores[token][doc_path] = tf * idf

    return tf_idf_scores

def build_bm_25(index, document_lengths):
    num_documents = len(document_lengths)
    avg_length = sum(document_lengths.values()) / num_documents
    bm_25_scores = defaultdict(dict)
    k = 2
    b = 0.75
    
    for token, document_counter in index.items():
        docs_containing_token = len(document_counter)
        idf = math.log((num_documents - docs_containing_token + 0.5)/(docs_containing_token + 0.5))

        for doc_path, count in document_counter.items():
            document_length = document_lengths[doc_path]
            tf = (count * (k + 1)) / (count + k * (1 - b + b * document_length / avg_length))

            bm_25_scores[token][doc_path] = tf * idf

    return bm_25_scores


def rank(query, scored_index):
    """Rank documents for `query` by summed ranking score, highest first.

    `scored_index` is a precomputed {token: {doc_path: score}} mapping
    (e.g. from `build_tf_idf`), so this function only sums and sorts.
    """
    query_tokens = set(tokenize(query))
    scores = defaultdict(float)

    for token in query_tokens:
        if token not in scored_index:
            continue
        for doc, score in scored_index[token].items():
            scores[doc] += score

    ranked_results = sorted(
        scores.items(),
        key=lambda item: item[1],
        reverse=True,
    )

    return ranked_results