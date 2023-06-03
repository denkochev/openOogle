from credentials import *
import requests
from requests.exceptions import RequestException
import pandas as pd
from storage_db import DBStorage
from urllib.parse import quote_plus
from datetime import datetime

# method to get response from Google Custom Search
def search_api(query, pages=int(RESULT_COUNT / 10)):
    results = []
    for i in range(0, pages):
        start = i * 10 + i
        url = SEARCH_URL.format(
            key=SEARCH_KEY,
            cx=SEARCH_ID,
            # quote_plus is formatting our query to url format (without space etc), "hello world" -> "hello+world"
            query=quote_plus(query),
            start=start
        )
        response = requests.get(url)
        data = response.json()

        results += data["items"]
    res_df = pd.DataFrame.from_dict(results)
    res_df["rank"] = list(range(1, res_df.shape[0] + 1))

    res_df = res_df[["link", "rank", "snippet", "title"]]
    return res_df

# method for downloading html from each page from query
def scrape_page(links):
    html = []
    for link in links:
        try:
            data_page = requests.get(link, timeout=5)
            html.append(data_page.text)
        except RequestException:
            html.append("")
    return html

# MAIN SEARCH METHOD
# How it works:
# 1. Checking the Database to see if this query already been searched
# 2. If it is return results
# 3. If it isn't:
#                   - querying the Google API
#                   - get new results
#                   - format them properly
#                   - save them to the DB
#                   - return them
def search(query):
    columns = ["query", "rank", "link", "title", "snippet", "html", "created"]
    # initializing of class from storage_db
    # instance of class DBStorage
    storage = DBStorage()

    stored_results = storage.query_results(query)
    if stored_results.shape[0] > 0:
        stored_results["created"] = pd.to_datetime(stored_results["created"])
        return stored_results[columns]
    # querying Google API if db doesn't have this results
    results = search_api(query)
    results["html"] = scrape_page(results["link"])
    results = results[results["html"].str.len() > 0].copy()

    results["query"] = query
    results["created"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    results = results[columns]

    rows_to_insert = []
    results.apply(lambda x: rows_to_insert.append(tuple(x)), axis=1)
    storage.insert_row(rows_to_insert)

    return results