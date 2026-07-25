from sqlite3 import connect
import pandas as pd

CSV_FILE = r"./data/cell-count.csv"
DB_FILE = r"./cell-count.db"
OUT_DIR = r"./outputs/"


def query_db(query: str) -> pd.DataFrame:
    conn = connect(DB_FILE)
    result = pd.read_sql(query, conn)
    conn.close()
    return result
