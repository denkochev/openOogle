from fastapi import FastAPI
from storage_db import DBStorage
from filter import Filter
from search import search
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json

app = FastAPI()

# CORS POLICY
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # permission for ALL DOMEN
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

class Ranking(BaseModel):
    query: str
    link: str
    score: int

def run_search(query):
    results = search(query)
    # filtering AND ReRank the results
    fi = Filter(results)
    results = fi.filter()
    results = results.drop(["html", "created", "relevance"], axis=1)
    results = results.to_dict(orient='records')
    json_results = json.dumps(results, ensure_ascii=False)
    return json_results


@app.get("/search")
def find(q: str):
    # print('USER QUERY ---->',q)
    search_results = run_search(q)
    return search_results

@app.post("/evaluate")
def mark_relevant(rank: Ranking):
    evaluated_query = rank.query
    evaluated_link = rank.link
    evaluated_score = rank.score

    storage = DBStorage()
    storage.update_relevance(evaluated_query, evaluated_link, evaluated_score)

    return {"success":True}