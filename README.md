# Mini search engine :)

A small TF-IDF search engine over a local corpus of Markdown files. It loads
the documents under `corpus/`, builds a TF-IDF index in memory, and ranks
documents against a query from an interactive command-line prompt.

No third-party dependencies — it uses only the Python standard library.

## Running

From the project root:

```bash
python app.py
```

It loads and indexes the corpus once at startup, then prompts for queries.
Type a query to see the top 10 matching documents (with their scores), or
type `quit` to exit.

```
Loaded 709 documents.
Type a search query, or type 'quit' to exit.

Search: async def routing
1. corpus/fastapi/docs_ko_docs_async.md — score: 0.4741
...
```

## How it works

The pipeline separates the *facts* about the corpus from the *formula* used to
score them, so the ranking method can be swapped without touching the rest:

```
load_documents  →  build_index   →  build_tf_idf  →  rank
   (loader)         (indexer)        (ranker)        (ranker)
   raw text         counts +         scores,         sum scores
                    doc lengths      computed once    + sort
```

1. **`loader.load_documents`** — recursively reads every `.md` file under
   `corpus/` into `{doc_path: text}`.
2. **`tokenizer.tokenize`** — lowercases text, splits on `[a-z0-9]+`, and drops
   a small set of stop words.
3. **`indexer.build_index`** — tokenizes each document once and returns the raw
   facts: a `{token: {doc_path: count}}` frequency index plus a
   `{doc_path: length}` map of document lengths.
4. **`ranker.build_tf_idf`** — turns those facts into a
   `{token: {doc_path: tf-idf score}}` index. IDF uses `+1` smoothing to avoid
   zero scores. This runs **once** when the engine starts.
5. **`ranker.rank`** — for a query, sums the precomputed scores of each query
   token across documents and returns them sorted high-to-low. It is
   formula-agnostic: it just sums whatever scores it's given.

`search.SearchEngine` wires these together — it loads, indexes, and scores the
corpus in `__init__`, then answers queries via `search(query, top_k=10)`.
`app.py` is the command-line front end on top of it.

Because scoring is a single, swappable step (`build_tf_idf` in `__init__`),
adding another ranking method (e.g. BM25) means writing a new scorer and
changing one line — `rank` stays the same.

## Layout

```
mini-search-engine/
├── corpus/              Markdown corpus, grouped by source repo
│   ├── fastapi/
│   ├── flask/
│   ├── mkdocs/
│   └── rust-book/
├── search_engine/
│   ├── tokenizer.py     text → tokens (with stop words)
│   ├── loader.py        read corpus files
│   ├── indexer.py       raw frequency index + doc lengths
│   ├── ranker.py        TF-IDF scoring + sum/sort ranking
│   ├── search.py        SearchEngine orchestration
│   └── snippets.py      result snippets (not implemented yet)
├── app.py               command-line entry point
├── requirements.txt
└── README.md
```

## Not implemented yet

- **`snippets.py`** — intended to show a short excerpt of each result around the
  first query match. Currently a stub that raises `NotImplementedError`.

- ** tests ** - need to make a folder of tests, will do that eventually
