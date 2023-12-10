# Google Search Engine API wrapper
Implementation of search engine based on GSE API with additional adds filtering and search result storage.
1. [How to setup project](#setup)
2. [Required credentials](#credentials)
3. [How to run local servers](#run-services)
## Setup
For unix sytem:
```
pip install -r requirements.txt
cd client 
npm i
```
For windows:
```
py -m pip install -r requirements.txt
cd client 
npm i
```
## Credentials
Create credentials file with variables where describe your main configuration settings: API, PosgreSQL login etc.

File .env has to look like this:
```bash
# Google Search API block
SEARCH_KEY = "YOUR-GOOGLE-API-SEARCH-KEY"
SEARCH_ID = "YOUR-SEARCH-ID"

COUNTRY = "ua"
SEARCH_URL = "https://www.googleapis.com/customsearch/v1?key={key}&cx={cx}&q={query}&start={start}&num=10&gl=" + COUNTRY
RESULT_COUNT = 20

# PostgreSQL DB block
DBNAME = "NAME-POSTGRE-DB"
DBUSER = "NAME-ACC-FOR-YOUR-POSTGRE-SERV"
DBPASSWORD = "PASSWORD-ACC-FOR-YOUR-POSTGRE-SERV"
DBHOST = "DB-serv" # < -  your DB serv host 
DBPORT = 5432 # < -  your DB serv port 

```
For the Frontend create .env.local inside `./client` with following value:
```bash
 REACT_APP_BACKEND_URL="YOUR PYTHON BACKEND URL"
```

## Run services
Launch backend.

For unix sytems:
```bash
uvicorn app:app --reload
```
For windows:
```bash
 py -m uvicorn app:app --reload  
```
Launch frontend.

```bash
cd client
npm start
```
