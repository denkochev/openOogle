1. Install packages

For unix sytem:
```
pip install -r packages.txt
cd client 
npm i
```
For windows:
```
py -m pip install -r packages.txt
cd client 
npm i
```

2. Create credentials.py file with variables where describe your main configuration settings: API, PosgreSQL login etc.

File credentials.py has to look like this:
```angular2html
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
DBHOST = "DB-serv" # < -  your DB serv port 
DBPORT = 5432 # < -  your DB serv port 

```
3. Launch backend.

For unix sytems:
```
uvicorn app:app --reload
```
For windows:
```
 py -m uvicorn app:app --reload  
```
4. Launch frontend.

```angular2html
cd client
npm start
```
