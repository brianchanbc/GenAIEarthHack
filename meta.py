import streamlit as st
import base64


def get_base64_of_bin_file(bin_file):
    with open(bin_file, "rb") as file:
        return base64.b64encode(file.read()).decode()


def meta():
    st.set_page_config(page_icon="🤖", page_title="Chicago-Machine", layout="wide")
    st.write("# The Chicago Machine Idea Evaluator 🤖")
    st.write("## Harness AI to evaluate ideas for a sustainable future")

    # Custom CSS to hide a specific Streamlit class
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
