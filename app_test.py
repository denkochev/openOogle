from flask import Flask, request, jsonify
from search import search
import html
from filter import Filter
from storage_db import DBStorage

app = Flask(__name__)

styles = """
<script>
const relevant = function(query, link){
    fetch("/relevant", {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "query": query,
            "link": link
        })
    })
}
</script>
"""

search_template = styles + """
<form action="/" method="post">
    <input type="text" name="query">
    <input type="submit" value="Search">
</form>
"""

result_template = """
<p class="site">{rank} : {link} <span onClick='relevant("{query}", "{link}");'>Relevant</span></p>
<a href="{link}">{title}></a>
<p class="snippet">{snippet}</p>
"""

def show_search_form():
    return search_template

def run_search(query):
    results = search(query)
    # filtering AND ReRank the results
    fi = Filter(results)
    results = fi.filter()
    rendered = search_template
    # help as to avoid to use html in browser from snippet row
    results["snippet"] = results["snippet"].apply(lambda x: html.escape(x))
    for index, row in results.iterrows():
        rendered += result_template.format(**row)
    return rendered


@app.route("/", methods=["GET", "POST"])
def search_form():
    if request.method == "POST":
        query = request.form["query"]
        return run_search(query)
    else:
        return show_search_form()

@app.route("/relevant", methods=["POST"])
def mark_relevant():
    data = request.get_json()
    query = data["query"]
    link = data["link"]
    storage = DBStorage()
    storage.update_relevance(query, link, 10)
    return jsonify(success=True)