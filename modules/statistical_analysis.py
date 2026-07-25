import plotly.graph_objects as go
from scipy.stats import ttest_ind

from modules.utils import query_db
from modules.initial_analysis import get_samples_df


def statistical_analysis(
    samples_df=None,
) -> tuple[dict[str, float], dict[str, go.Figure]]:
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
    figures = dict()
    for population in cell_types:
        responder_pop = responders_df.query("population == @population")
        nonresponder_pop = nonresponders_df.query("population == @population")

        # Visualize the population relative frequencies comparing responders versus non-responders using a boxplot of for each immune cell population
        # TODO: This figure needs a lot of work -> combine to one figure?
        fig = go.Figure()
        fig.add_trace(go.Box(y=responder_pop["percentage"], name="Responders"))
        fig.add_trace(go.Box(y=nonresponder_pop["percentage"], name="Non-Responders"))
        fig.update_layout(title=population, yaxis_title="Relative Frequency (%)")
        figures[population] = fig

        # Report which cell populations have a significant difference in relative frequencies between responders and non-responders. Statistics are needed to support any conclusion to convince Yah of Bob’s findings.
        test_result = ttest_ind(
            responder_pop["percentage"], nonresponder_pop["percentage"]
        )
        p_vals[population] = test_result.pvalue

    return p_vals, figures


if __name__ == "__main__":
    stats_results, _ = statistical_analysis()
    for population, p_val in stats_results.items():
        print(f"{population}: {p_val}")
