import pandas
from search import search

df = pandas.read_csv('utils/relatedQueries.csv',
            index_col='query',
            header=0,
            names=['query','rating'])

def searchingTopQueries():
    i = 0
    for index, row in df.iterrows():
        # get query and call search with it
        value = row.name
        print("calculating data for %s query: => %s" % (i, value))
        search(value)
        i = i + 1

searchingTopQueries()


"""
IF SOME ERROR HAPPEND ON THE WAY YOU INSERTING RESULTS INTO DB 
YOU HAVE TO EXECUTE THIS COMMAND INTO YOUR DATABASE :

    DELETE FROM results
    WHERE query IN (SELECT query
                    FROM results
                    GROUP BY query
                    HAVING COUNT(id)<20);

AND TRY TO START searchingTopQueries() AGAIN
DONT WORRY IT DOESN'T QUERYING RESULTS YOU'VE ALREADY HAVE
"""