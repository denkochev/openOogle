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
