from sqlite3 import connect
import pandas as pd

df = pd.read_csv('./data/cell-count.csv')
# print(df.head())

# Create project table
project_df = df[["project", "sample_type"]].drop_duplicates()
# print(project_df.head())

# Create subject table
subject_df = df[["subject", "condition", "age", "sex", "treatment", "response"]].drop_duplicates()
#print(subject_df.head())

# Make sure we're creating indices on treatment table
sample_df = df[["project", "subject", "sample", "time_from_treatment_start", "b_cell", "cd8_t_cell", "cd4_t_cell", "nk_cell", "monocyte"]].drop_duplicates()

# Load into database
conn = connect(r'./cell-count.db')
# TODO: Look into establishing keys here
project_df.to_sql('projects', conn, if_exists='replace', index=False)
subject_df.to_sql('subjects', conn, if_exists='replace', index=False)
sample_df.to_sql( 'samples',  conn, if_exists='replace', index=False)
conn.close()
