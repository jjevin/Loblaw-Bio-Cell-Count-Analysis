import streamlit as st

import modules.initial_analysis as init
import modules.statistical_analysis as stat
import modules.subset_analysis as sub
import modules.b_cell_calculation as b_cell

st.set_page_config(page_title="Loblaw Bio Cell Count Analysis", layout="wide")
st.title("Cell Count Analysis - Bob's Dashboard")


@st.cache_data
def load_all():
    samples_df = init.get_samples_df()
    p_vals, figures = stat.statistical_analysis(samples_df)
    subset_results = sub.subset_analysis()
    avg_b_cells = b_cell.calc_avg_b_cells()
    return samples_df, p_vals, figures, subset_results, avg_b_cells


samples_df, p_vals, figures, subset_results, avg_b_cells = load_all()

tab2, tab3, tab4, tab_bcell = st.tabs(
    ["Part 2: Overview", "Part 3: Statistics", "Part 4: Subsets", "B-Cell Calc"]
)

with tab2:
    st.subheader("Relative frequency of each cell population per sample")
    st.dataframe(samples_df, use_container_width=True)

with tab3:
    st.subheader("Responders vs. non-responders by population")
    sig = {pop: p for pop, p in p_vals.items() if p < 0.05}
    if sig:
        st.write(f"Significant populations (p < 0.05): {', '.join(sig.keys())}")
    else:
        st.write("No populations reach significance at p < 0.05.")
    for population, fig in figures.items():
        st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.subheader("Baseline melanoma PBMC samples, miraclib-treated")
    for query_label, table in subset_results.items():
        st.write(query_label)
        st.dataframe(table)

with tab_bcell:
    st.metric("Average B cells (melanoma, male, responder, baseline)", avg_b_cells)
