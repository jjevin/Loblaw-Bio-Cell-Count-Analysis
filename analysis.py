from sqlite3 import connect
import pandas as pd

def __query_db(db: str, query: str) -> str:
    conn = connect(db)
    result = pd.read_sql(query, conn)
    conn.close()
    return result

def initial_analysis() -> pd.DataFrame:
    query = """
        SELECT 
            sample
            ,b_cell
            ,cd8_t_cell
            ,cd4_t_cell
            ,nk_cell
            ,monocyte
        FROM samples
    """
    samples_df = __query_db(r'./cell-count.db', query)

    # [x] sample: the sample id as in column sample in cell-count.csv
    # [x] total_count: total cell count of sample
    # TODO: This is ugly
    samples_df["total_count"] = samples_df["b_cell"] + samples_df["cd8_t_cell"] + samples_df["cd4_t_cell"] + samples_df["nk_cell"] + samples_df["monocyte"]
    # [x] population: name of the immune cell population (e.g. b_cell, cd8_t_cell, etc.)
    # [x] count: cell count
    samples_df = samples_df.melt(id_vars=["sample", "total_count"],
                                 var_name="population",
                                 value_name="count")

    # [ ] percentage: relative frequency in percentage
    samples_df["percentage"] = samples_df["count"] * 100 / samples_df["total_count"]

    # TODO: remove response from final table
    return samples_df

def statistical_analysis(samples_df):
    # Get sample IDs of melanoma patients receiving miraclib in PBMC samples
    query = """
        SELECT DISTINCT(sa.sample), su.response
        FROM samples sa
        JOIN projects pr ON sa.project = pr.project 
        JOIN subjects su ON sa.subject = su.subject 
        WHERE 1=1
            AND su.condition   = 'melanoma' 
            AND su.treatment   = 'miraclib' 
            AND pr.sample_type = 'PBMC'
    """
    query_df = __query_db(r'./cell-count.db', query)

    filtered_df = samples_df.merge(query_df, on='sample', how='inner')
    responders_df = filtered_df.query('response == "yes"')
    nonresponders_df = filtered_df.query('response == "no"')

    # "Visualize the population relative frequencies comparing responders versus non-responders using a boxplot of for each immune cell population"

    # "Report which cell populations have a significant difference in relative frequencies between responders and non-responders. Statistics are needed to support any conclusion to convince Yah of Bob’s findings."

    return 0

def subset_analysis():
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
    subset_df = __query_db(r'./cell-count.db', query)

    # "Among these samples, extend the query to determine:
    # 1. How many samples from each project
    per_project_df = subset_df.groupby(["project"]).size()
    # 2. How many subjects were responders/non-responders 
    responders_df  = subset_df.groupby(["response"]).size()
    # 3. How many subjects were males/females"
    sex_df         = subset_df.groupby(["sex"]).size()

def avg_b_cells() -> float:
    # Melanoma males 
    # All sample and treatment types
    # average number of B cells 
    # responders 
    # time=0? Use two decimals (XXX.XX).
    query = """
        SELECT sa.b_cell
        FROM samples sa
        JOIN projects pr ON sa.project = pr.project 
        JOIN subjects su ON sa.subject = su.subject 
        WHERE 1=1
            AND su.condition = 'melanoma'
            AND su.sex       = 'M'
            AND su.response  = 'yes'
            AND sa.time_from_treatment_start = 0
    """
    b_cell_df    = __query_db(r'./cell-count.db', query)
    b_cell_distr = b_cell_df['b_cell'].tolist()
    b_cell_avg   = sum(b_cell_distr) / len(b_cell_distr)
    return round(b_cell_avg, 2)

def main():
    samples_df = initial_analysis()
    statistical_analysis(samples_df)
    subset_analysis()

    print(f'Average number of b cells for the given condition: {avg_b_cells()}')

if __name__ == "__main__":
    main()
