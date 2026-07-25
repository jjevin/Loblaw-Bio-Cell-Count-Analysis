import os
import pandas as pd
from modules.utils import query_db, OUT_DIR
from plotly import graph_objects as go


def get_samples_df() -> tuple[pd.DataFrame, go.Figure]:
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
    samples_df = query_db(query)

    # sample: the sample id as in column sample in cell-count.csv
    # total_count: total cell count of sample
    samples_df["total_count"] = (
        samples_df["b_cell"]
        + samples_df["cd8_t_cell"]
        + samples_df["cd4_t_cell"]
        + samples_df["nk_cell"]
        + samples_df["monocyte"]
    )
    # population: name of the immune cell population (e.g. b_cell, cd8_t_cell, etc.)
    # count: cell count
    samples_df = samples_df.melt(
        id_vars=["sample", "total_count"], var_name="population", value_name="count"
    )

    # percentage: relative frequency in percentage
    samples_df["percentage"] = samples_df["count"] * 100 / samples_df["total_count"]

    samples_df.to_csv(os.path.join(OUT_DIR, "samples.csv"))

    # Visualization for pipeline
    fig = go.Figure()
    for population in samples_df["population"].unique():
        pop_df = samples_df[samples_df["population"] == population]
        fig.add_trace(go.Box(y=pop_df["percentage"], name=population))
    fig.update_layout(
        title="Distribution of relative frequency by population",
        yaxis_title="Relative Frequency (%)",
        showlegend=False,
    )
    fig.write_html(os.path.join(OUT_DIR, "samples_overview.html"))

    return samples_df, fig


if __name__ == "__main__":
    samples_df, _ = get_samples_df()
    print(samples_df)
