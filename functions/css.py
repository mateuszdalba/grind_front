import streamlit as st



def include_custom_styling():
    #Bootstrap
    bootstrap_css = """
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-iYQeCzEYFbKjA/T2uDLTpkwGzCiq6soy8tYaI1GyVh/UjpbCx/TYkiZhlZB6+fzT" crossorigin="anonymous">
    """
    bootstrap_js = """
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.1/dist/js/bootstrap.bundle.min.js" integrity="sha384-u1OknCvxWvY5kfmNBILK2hRnQC3Pr17a+RTT6rIHI7NnikvbZlHgTPOOmMi466C8" crossorigin="anonymous"></script>
    """
    st.markdown(bootstrap_css, unsafe_allow_html=True)
    st.markdown(bootstrap_js, unsafe_allow_html=True)


    #Custom CSS
    with open('assets/styles.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def card(header, content, link, img='<p></p>'):
    return st.markdown(f"""
    <a href="http://localhost:8501/{link}" target="_self">
        <div class="card">
            <div class="card-img-top">
                {img}
            </div>
            <div class="card-body">
                <h5 class="card-title">{header}</h5>
                <p class="card-text">{content}</p>
            </div>
        </div>
    </a>
    """, unsafe_allow_html=True)