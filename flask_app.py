"""Flask web interface for the mini search engine."""

from flask import Flask, render_template, request, jsonify
from search_engine.search import SearchEngine
from search_engine.snippets import make_snippet, get_title

app = Flask(__name__)
engine = SearchEngine()

@app.route("/")
def index():
    return render_template("index.html", doc_count=len(engine.documents))

@app.route("/api/search", methods=["POST"])
def search():
    data = request.json
    query = data.get("query", "").strip()

    if not query:
        return jsonify({"results": []})

    results = engine.search(query)
    formatted_results = []

    for doc_id, score in results:
        doc_metadata = engine.get_doc(doc_id)
        text = doc_metadata["text"]
        doc_path = doc_metadata["path"]
        snippet = make_snippet(text, query)
        title = get_title(doc_path, text)

        formatted_results.append({
            "title": title,
            "path": doc_path,
            "score": round(score, 4),
            "snippet": snippet
        })

    return jsonify({"results": formatted_results})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
