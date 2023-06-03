import psycopg2
from psycopg2.extras import execute_values
import pandas as pd

from credentials import *

class DBStorage():
    def __init__(self):
        # connection to PostgreSQL
        self.con = psycopg2.connect(
            dbname=DBNAME,
            user=DBUSER,
            password=DBPASSWORD,
            host=DBHOST,
            port=DBPORT
        )
        self.create_tables()

    def create_tables(self):
        cursor = self.con.cursor()
        results_table = '''
            CREATE TABLE IF NOT EXISTS results (
                id SERIAL PRIMARY KEY,
                query TEXT,
                rank INTEGER,
                link TEXT,
                title TEXT,
                snippet TEXT,
                html TEXT,
                created TIMESTAMP,
                relevance INTEGER,
                UNIQUE(query, link)
            );
        '''
        cursor.execute(results_table)
        self.con.commit()
        cursor.close()

    # method to get results on query from DB
    def query_results(self, query):
        cursor = self.con.cursor()
        cursor.execute(f"SELECT * FROM results WHERE query = %s ORDER BY rank ASC;", (query,))
        rows = cursor.fetchall()
        cursor.close()
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(rows, columns=columns)
        return df

    def insert_row(self, values):
        cursor = self.con.cursor()
        try:
            insert_query = '''
                INSERT INTO results (query, rank, link, title, snippet, html, created)
                VALUES %s
            '''
            # cleaning from NUL
            cleaned_values = []
            for row in values:
                cleaned_row = []
                for value in row:
                    if isinstance(value, str):
                        cleaned_row.append(value.replace('\x00', ''))
                    else:
                        cleaned_row.append(value)
                cleaned_values.append(tuple(cleaned_row))

            execute_values(cursor, insert_query, cleaned_values)
            self.con.commit()
        except psycopg2.IntegrityError:
            pass
        cursor.close()

    def update_relevance(self, query, link, relevance):
        cursor = self.con.cursor()
        update_query = '''
            UPDATE results
            SET relevance = %s
            WHERE query = %s AND link = %s
        '''
        cursor.execute(update_query, (relevance, query, link))
        self.con.commit()
        cursor.close()

    def __del__(self):
        # CLOSE CONNECTION TO DB
        self.con.close()




# also we can add machine learning based on relevance (sql row):
