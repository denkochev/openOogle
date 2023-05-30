from fastapi import FastAPI
from storage_db import DBStorage
from filter import Filter
from search import search
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

# CORS POLICY
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adress of React client
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

def run_search(query):
    results = search(query)
    # filtering AND ReRank the results
    fi = Filter(results)
    results = fi.filter()
    results = results.drop(["html", "created"], axis=1)
    results = results.to_dict(orient='records')
    json_results = json.dumps(results, ensure_ascii=False)
    return json_results

@app.get("/search")
def find(q: str):
    # print('USER QUERY ---->',q)
    search_results = run_search(q)
    return search_results