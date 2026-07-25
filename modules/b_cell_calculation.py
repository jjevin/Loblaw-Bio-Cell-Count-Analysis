import pandas as pd
from modules.utils import query_db


def calc_avg_b_cells() -> float:
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
    b_cell_df = query_db(query)
    b_cell_distr = b_cell_df["b_cell"].tolist()
    b_cell_avg = sum(b_cell_distr) / len(b_cell_distr)
    return round(b_cell_avg, 2)


def get_bcell_context() -> pd.DataFrame:
    query = """
        SELECT su.sex, su.response, sa.b_cell
        FROM samples sa
        JOIN subjects su ON sa.subject = su.subject
        WHERE su.condition = 'melanoma'
          AND sa.time_from_treatment_start = 0
    """
    context_df = query_db(query)
    summary = (
        context_df.groupby(["sex", "response"])["b_cell"].mean().round(2).reset_index()
    )
    summary["group"] = (
        summary["sex"]
        + " / "
        + summary["response"].map({"yes": "responder", "no": "non-responder"})
    )
    return summary


if __name__ == "__main__":
    avg_b_cells = calc_avg_b_cells()
    print(
        f"Average number of b cells for the given condition: {avg_b_cells}", end="\n\n"
    )
