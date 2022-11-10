import streamlit as st
from functions.css import include_custom_styling, card 

st.set_page_config(page_title='Grind', page_icon=":shark:", layout="wide")

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
            #st.image('https://s3.amazonaws.com/prod.skimble/assets/1727358/image_iphone.jpg')
        )
    with r1_col2:
        card(
            "Pushups",
            "XXxxxxxxxxxxxxxxxx",
            "#",
        )
    with r1_col3:
        card(
            "Exercise1",
            "Some XYZ exercies",
            "#",
        )

with row2:
    with r2_col1:
        card(
            "Exercise2",
            "Some exerciess",
            "#",
        )
    with r2_col2:
        card(
            "Exercise3",
            "Exercise1Exercise1Exercise1Exercise1",
            "#",
        )
    with r2_col3:
        card(
            "Exercise4",
            "Exercise1Exercise1Exercise1Exercise1Exercise1Exercise1",
            "#",
        )
