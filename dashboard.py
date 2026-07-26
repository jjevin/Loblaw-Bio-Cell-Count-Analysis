import pandas as pd
import plotly.graph_objects as go
import streamlit as st

import modules.initial_analysis as init
import modules.statistical_analysis as stat
import modules.subset_analysis as sub
import modules.b_cell_calculation as b_cell

st.set_page_config(page_title="Loblaw Bio Cell Count Analysis", layout="wide")
st.title("Cell Count Analysis - Bob's Dashboard")


@st.cache_data  # load function to allow caching
def load_all():
    samples_results = init.get_samples_df()
    stats_results = stat.statistical_analysis(samples_results[0])
    subset_results = sub.subset_analysis()
    avg_b_cells = b_cell.calc_avg_b_cells()
    b_cell_context = b_cell.get_bcell_context()
    return samples_results, stats_results, subset_results, avg_b_cells, b_cell_context


# Called in stats tab to denote significant differences
def _highlight_significant(row: pd.Series) -> list[str]:
    color = "background-color: #d4f4dd" if row["Significant (p < 0.05)"] else ""
    return [color] * len(row)


samples_results, stats_results, subset_results, avg_b_cells, b_cell_context = load_all()

tab2, tab3, tab4, tab_bcell = st.tabs(
    ["Part 2: Overview", "Part 3: Statistics", "Part 4: Subsets", "B-Cell Calc"]
)

with tab2:
    samples_df, overview_fig = samples_results
    st.subheader("Relative frequency of each cell population per sample")

    populations = sorted(samples_df["population"].unique())
    selected_pop = st.selectbox(
        "Filter by population", options=["All populations"] + populations
    )

    if selected_pop == "All populations":
        filtered_df = samples_df
    else:
        filtered_df = samples_df.query("population == @selected_pop")

    col1, col2, col3 = st.columns(3)
    col1.metric("Samples shown", len(filtered_df["sample"].unique()))
    col2.metric("Mean relative frequency", f"{filtered_df['percentage'].mean():.2f}%")
    col3.metric(
        "Median relative frequency", f"{filtered_df['percentage'].median():.2f}%"
    )

    st.dataframe(filtered_df, width="stretch")
    st.plotly_chart(overview_fig, width="stretch")

with tab3:
    p_vals, combined_fig = stats_results
    st.subheader("Responders vs. non-responders by population")

    p_df = pd.DataFrame(
        {"Population": list(p_vals.keys()), "p-value": list(p_vals.values())}
    )
    p_df["Significant (p < 0.05)"] = p_df["p-value"] < 0.05

    st.dataframe(p_df.style.apply(_highlight_significant, axis=1), width="stretch")
    st.plotly_chart(combined_fig, width="stretch")

with tab4:
    st.subheader("Baseline melanoma PBMC samples, miraclib-treated")
    for query_label, table in subset_results.items():
        st.write(f"**{query_label}**")
        cols = st.columns(len(table))
        for col, (idx, val) in zip(cols, table.items()):
            col.metric(str(idx), int(val))
        st.divider()

with tab_bcell:
    st.subheader("B cell counts, melanoma patients at baseline")
    st.metric("Average B cells (melanoma, male, responder, baseline)", avg_b_cells)

    st.caption(
        "For context, average B cell counts across sex/response subgroups "
        "(melanoma, baseline) are shown below. This is supplementary and "
        "doesn't change the required metric above."
    )
    bcell_context = b_cell.get_bcell_context()
    bcell_fig = go.Figure(go.Bar(x=bcell_context["group"], y=bcell_context["b_cell"]))
    bcell_fig.update_layout(
        title="Average B cell count by sex & response (melanoma, baseline)",
        yaxis_title="Average B cell count",
    )
    st.plotly_chart(bcell_fig, width="stretch")
