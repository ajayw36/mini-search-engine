from collections import defaultdict

from search_engine.tokenizer import tokenize


def build_index(documents):
    """Build a frequency counter index, {token: {doc_id: frequency_count}}
     from documents. Also build a document tracker with {doc_id : doc_length}"""
    document_lengths = {}
    frequency_counter = {}

    for doc_id, text in documents.items():
        tokenized_text = tokenize(text)

        if not tokenized_text:
            continue

        document_lengths[doc_id] = len(tokenized_text)

        for token in tokenized_text:
            if token not in frequency_counter:
                frequency_counter[token] = {}
            frequency_counter[token][doc_id] = frequency_counter[token].get(doc_id, 0) + 1

    return frequency_counter, document_lengths
