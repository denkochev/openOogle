import sqlite3
import pandas as pd

class DBStorage():
    def __init__(self):
        # connection to my db when class init
        self.con = sqlite3.connect("pages_links.db")
        self.create_tables()

    def create_tables(self):
        cursor = self.con.cursor()
        results_table = r"""
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY,
                query TEXT,
                rank INTEGER,
                link TEXT,
                title TEXT,
                snippet TEXT,
                html TEXT,
                created DATETIME,
                relevance INTEGER,
                UNIQUE(query, link)
            );
        """

        cursor.execute(results_table)
        self.con.commit()
        cursor.close()

    # method to get results on query from DB
    def query_results(self,query):
        # df because pd return DataFrame
        df = pd.read_sql(f"SELECT * FROM results WHERE query='{query}' ORDER BY rank ASC;", self.con)
        return df

    def insert_row(self,values):
        cursor = self.con.cursor()
        try:
            cursor.execute('INSERT INTO results(query,rank,link,title,snippet,html,created) VALUES(?,?,?,?,?,?,?)', values)
            self.con.commit()
        except sqlite3.IntegrityError:
            pass
        cursor.close()

    def update_relevance(self, query, link, relevance):
        cursor = self.con.cursor()
        cursor.execute("UPDATE results SET relevance=? WHERE query=? AND link=?", [relevance, query, link])
        self.con.commit()
        cursor.close()




# also we can add machine learning based on relevance (sql row)