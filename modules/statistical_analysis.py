import csv, os
import plotly.graph_objects as go
from scipy.stats import ttest_ind

from modules.utils import query_db, OUT_DIR
from modules.initial_analysis import get_samples_df


def statistical_analysis(
    samples_df=None,
) -> tuple[dict[str, float], go.Figure]:
    if samples_df is None:
        samples_df = get_samples_df()

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
    query_df = query_db(query)

    filtered_df = samples_df.merge(query_df, on="sample", how="inner")
    cell_types = filtered_df["population"].unique()
    responders_df = filtered_df.query('response == "yes"')
    nonresponders_df = filtered_df.query('response == "no"')

    p_vals = dict()
    # figures = dict()
    fig = go.Figure()
    for i, population in enumerate(cell_types):
        responder_pop = responders_df.query("population == @population")
        nonresponder_pop = nonresponders_df.query("population == @population")

        fig.add_trace(
            go.Box(
                x=[population] * len(responder_pop["percentage"]),
                y=responder_pop["percentage"],
                name="Responders",
                legendgroup="Responders",
                marker_color="#636EFA",
                showlegend=(i == 0),
            )
        )
        fig.add_trace(
            go.Box(
                x=[population] * len(nonresponder_pop["percentage"]),
                y=nonresponder_pop["percentage"],
                name="Non-Responders",
                legendgroup="Non-Responders",
                marker_color="#EF553B",
                showlegend=(i == 0),
            )
        )

        # Report which cell populations have a significant difference in relative frequencies between responders and non-responders. Statistics are needed to support any conclusion to convince Yah of Bob’s findings.
        test_result = ttest_ind(
            responder_pop["percentage"], nonresponder_pop["percentage"]
        )
        p_vals[population] = test_result.pvalue

        with open(
            os.path.join(OUT_DIR, f"{population}_analysis.csv"), mode="w", newline=""
        ) as file:
            writer = csv.writer(file)
            writer.writerow(p_vals.keys())
            writer.writerow(p_vals.values())

    fig.update_layout(
        boxmode="group",
        title="Responders vs. Non-Responders by Population",
        yaxis_title="Relative Frequency (%)",
    )
    fig.write_html(os.path.join(OUT_DIR, "responders_box.html"))
    return p_vals, fig


if __name__ == "__main__":
    stats_results, _ = statistical_analysis()
    for population, p_val in stats_results.items():
        print(f"{population}: {p_val}")
