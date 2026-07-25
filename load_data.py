from sqlite3 import connect
import pandas as pd

import modules.utils as utils

df = pd.read_csv(utils.CSV_FILE)

# Create project table
project_df = df[["project", "sample_type"]].drop_duplicates()

# Create subject table
subject_df = df[
    ["subject", "condition", "age", "sex", "treatment", "response"]
].drop_duplicates()

# Make sure we're creating indices on treatment table
sample_df = df[
    [
        "project",
        "subject",
        "sample",
        "time_from_treatment_start",
        "b_cell",
        "cd8_t_cell",
        "cd4_t_cell",
        "nk_cell",
        "monocyte",
    ]
].drop_duplicates()

conn = connect(utils.DB_FILE)
# Load tables into database
project_df.to_sql("projects", conn, if_exists="replace", index=False)
subject_df.to_sql("subjects", conn, if_exists="replace", index=False)
sample_df.to_sql("samples", conn, if_exists="replace", index=False)
conn.close()
