import streamlit as st
import base64


def get_base64_of_bin_file(bin_file):
    with open(bin_file, "rb") as file:
        return base64.b64encode(file.read()).decode()


def meta():
    st.set_page_config(
        page_icon="🤖", page_title="Chicago-Machine", layout="wide") # or layout='centered'
    st.write("# I am Chicago Machine 🤖")
    st.write("## *I am here to help you with your project evaluation!*")

    # Hide the made with Streamlit footer
    hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            /* Set text color to black */
            h1, h2, h3, h4, h5, h6, p, .stMarkdown {
                color: #006000;
            }
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

    # Load local image as background
    base64_background = get_base64_of_bin_file(
        "background.png"
    )  # Replace with your image file path
    page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] > .main {{
    background-image: url("data:image/png;base64,{base64_background}");
    background-size: cover;
    background-position: center center;
    background-repeat: no-repeat;
    background-attachment: local;
    }}
    [data-testid="stHeader"] {{
    background: rgba(0,0,0,0);
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)
