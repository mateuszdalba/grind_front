import streamlit as st
from functions.css import include_custom_styling, card 

st.set_page_config(page_title='Grind', page_icon="brain", layout="wide")

include_custom_styling()


header = st.container()

#st.sidebar.header('Virtual Gym')

with header:
    st.markdown(
    """
    <div class="page-title">
        <h1> Welcome to Virtual Gym</h1>
    </div>
    """,
        unsafe_allow_html=True)


row1 = st.container()
r1_col1, r1_col2, r1_col3 = st.columns([1, 1, 1])
row2 = st.container()
r2_col1, r2_col2, r2_col3 = st.columns([0.5, 0.5, 0.5])



with row1:
    with r1_col1:
        card(
            "Squats",
            "Learn how to make squats ..",
            "Gym",
        )
    with r1_col2:
        card(
            "Pushups",
            "XXxxxxxxxxxxxxxxxx",
            "#",
        )
    with r1_col3:
        card(
            "NLP",
            "Detect positive, neutral or negative sentiment of a text based on a number of prepared datasets",
            "NLP",
        )

with row2:
    with r2_col1:
        card(
            "Time Series",
            "Visualize, understand and create an analytical model of a time series for your study",
            "Time_Series",
        )
    with r2_col2:
        card(
            "Spatial",
            "Investigate a GIS dataset with an interactive map and advanced geospatial analysis tools",
            "Spatial",
        )
    with r2_col3:
        card(
            "Clustering",
            "Determine the most relevant words using an unsupervised learning approach and wordclouds",
            "Clustering",
        )