from collections import defaultdict

from search_engine.tokenizer import tokenize


def build_index(documents):
    """Build a frequency counter index, {token: {doc_path: frequency_count}}
     from documents. Also build a document tracker with {doc_path : doc_length}"""
    document_lengths = {}

    frequency_counter = defaultdict(lambda: defaultdict(int))
    for doc_path, text in documents.items():
        tokenized_text = tokenize(text)

        if not tokenized_text:
            continue

        document_lengths[doc_path] = len(tokenized_text)

        for token in tokenized_text:
            frequency_counter[token][doc_path] += 1
    
    return frequency_counter, document_lengths
