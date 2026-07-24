from sqlite3 import connect
import pandas as pd

CSV_FILE = r'./data/cell-count.csv'
DB_FILE  = r'./cell-count.db'

def query_db(query: str) -> str:
    conn = connect(DB_FILE)
    result = pd.read_sql(query, conn)
    conn.close()
    return result
