import sqlite3
import pandas as pd

class GroupTable:
    def __init__(self, database: str, df: pd.DataFrame, table_name: str, group_key):

        self.database = database
        self.df = df
        self.group_key = group_key
        self.table_name = table_name

    def upsert(self):
        conn = sqlite3.connect(database)
        
        self._delete(conn)
        self._insert(conn)

        conn.commit()
        conn.close()


    def _delete(self, conn):
        self.cursor = conn.cursor()
        cursor.execute(f"""
        DELETE FROM {self.table_name}
        WHERE group_key = :group_key
        """,
        {"group_key" : self.group_key}
        )

    def _insert(self, conn):
        self.df["group_key"] = self.group_key
        self.df.to_sql(name, conn, if_exists="append", method="multi")
