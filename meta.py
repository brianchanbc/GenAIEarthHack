# define meta information of the app
import streamlit as st

def meta():
    st.set_page_config(page_icon="⚗️", page_title="Omnigpt", layout="wide") # or layout='centered'
    st.write("# I am a Chicago Machine 🤖")

    # Hide the made with Streamlit footer
    hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    # Hide the specific class of deploy and connect to streamlit.io
    st.markdown(
        """
        <style>
            .st-emotion-cache-zq5wmm.ezrtsby0 {
                display: none !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
