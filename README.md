# Mini search engine :)

A small search engine over a local corpus of Markdown files implemented with
TF-IDF and BM25 Ranking. It loads the documents under `corpus/`, builds a TF-IDF or BM25
index in memory, and ranks documents against a query.

Available as a command-line interface or web interface.

## Running

### Command-line interface

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

### Web interface

Start the Flask web server:

```bash
python flask_app.py
```

Then open `http://localhost:5000` in your browser. Search results display with snippets and relevance scores.

## How it works

The pipeline separates the *facts* about the corpus from the *formula* used to
score them, so the ranking method can be swapped without touching the rest:

```
load_documents  →  build_index   →  build_dm_25   →  rank
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
   `{token: {doc_path: tf-idf score}}` index. There are functions built in for both TF-IDF and DM25 ranking.
   This runs **once** when the engine starts.
6. **`ranker.rank`** — for a query, sums the precomputed scores of each query
   token across documents and returns them sorted high-to-low. It is
   formula-agnostic: it just sums whatever scores it's given.

`search.SearchEngine` wires these together — it loads, indexes, and scores the
corpus in `__init__`, then answers queries via `search(query, top_k=10)`.
`app.py` is the command-line front end on top of it.

Because scoring is a single, swappable step (`build_tf_idf` in `__init__`),
adding another ranking method means writing a new scorer and
changing one line — `rank` stays the same.

## Deployment

The web interface is deployed on Render's free tier at:
https://mini-search-engine-po9p.onrender.com

To deploy your own:
1. Create a Render account and connect your GitHub repo
2. Add a Web Service with Start Command: `gunicorn flask_app:app`
3. Render auto-deploys on each push to main

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
│   ├── ranker.py        TF-IDF and BM25 scoring + sum/sort ranking
│   ├── search.py        SearchEngine orchestration
│   └── snippets.py      result snippets and titles
├── templates/
│   └── index.html       web interface
├── static/
│   └── style.css        web interface styling
├── tests/               a complete test suite
├── app.py               command-line entry point
├── flask_app.py         web server entry point
├── Procfile             deployment config
├── render.yaml          Render deployment config
├── requirements.txt
└── README.md
```

## Not implemented yet

- storing index once it is created so you don't recompute every time you run
- adding phrase search
- web crawler integration
