import csv, os
import pandas as pd
from modules.utils import query_db, OUT_DIR


def subset_analysis() -> dict[str, pd.DataFrame]:
    # "Identify all melanoma PBMC samples at baseline (time_from_treatment_start is 0) from patients who have been treated with miraclib."
    query = """
        SELECT sa.*, su.response, su.sex
        FROM samples sa
        JOIN projects pr ON sa.project = pr.project 
        JOIN subjects su ON sa.subject = su.subject 
        WHERE 1=1
            AND su.condition   = 'melanoma'
            AND su.treatment   = 'miraclib' 
            AND pr.sample_type = 'PBMC'
            AND sa.time_from_treatment_start = 0
    """
    subset_df = query_db(query)

    queries = dict()
    queries["1. How many samples are from each project?"] = subset_df.groupby(
        ["project"]
    ).size()
    queries["2. How many subjects were responders/non-responders?"] = subset_df.groupby(
        ["response"]
    ).size()
    queries["3. How many subjects were males/females?"] = subset_df.groupby(
        ["sex"]
    ).size()

    with open(
        os.path.join(OUT_DIR, "subset_analysis.csv"), mode="w", newline=""
    ) as file:
        writer = csv.writer(file)
        writer.writerow(queries.keys())
        writer.writerow(queries.values())

    return queries


if __name__ == "__main__":
    results = subset_analysis()
    for query, table in results.items():
        print(query, "\n", table, end="\n\n")
