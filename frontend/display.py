import streamlit as st


def display_report():
    Overview = st.session_state["Report"]["Overview"]
    Sustainability = st.session_state["Report"]["Sustainability"]
    Business = st.session_state["Report"]["Business"]
    Impact_Innovation = st.session_state["Report"]["Impact_Innovation"]

    st.header("Report Overview")
    st.subheader("Overview")
    st.write(Overview["Overview"])
    st.subheader("Relevant Industries")
    st.write(Overview["Relevant Industries"])

    with st.expander("Sustainability", expanded=True):
        st.markdown(
            f"**Eliminate waste and pollution:** {Sustainability['Eliminate waste and pollution']}"
        )
        st.markdown(
            f"**Circulate products and materials:** {Sustainability['Circulate products and materials']}"
        )
        st.markdown(f"**Regenerate nature:** {Sustainability['Regenerate nature']}")
        st.write("**Follow-Up Questions**")
        for i, question in enumerate(Sustainability["Follow-Up Questions"]):
            st.markdown(f"- {question}")
        st.markdown(
            """
        <style>
        [dara-testid="stMarkdownContainer"] ul{
                    padding-left:40px;
        }
        </style>
        """,
            unsafe_allow_html=True,
        )

        rating = Sustainability["Rating"]
        star_emoji_string = "⭐" * int(rating)

        st.markdown(f"**Rating:** {star_emoji_string}")

    with st.expander("Business Assessment", expanded=True):
        st.write("Assessments")
        for i, assessment in enumerate(Business["Assessment"]):
            st.markdown(f"- {assessment}")

        st.markdown(
            """
        <style>
        [dara-testid="stMarkdownContainer"] ul{
                    padding-left:40px;
        }
        </style>
        """,
            unsafe_allow_html=True,
        )

        st.write("**Follow-Up Questions**")
        for i, question in enumerate(Business["Follow-Up Questions"]):
            st.markdown(f"- {question}")
        st.markdown(
            """
        <style>
        [dara-testid="stMarkdownContainer"] ul{
                    padding-left:40px;
        }
        </style>
        """,
            unsafe_allow_html=True,
        )
        rating = Business["Rating"]
        star_emoji_string = "⭐" * int(rating)
        st.markdown(f"**Rating:** {star_emoji_string}")

    with st.expander("Impact and Innovation", expanded=True):
        st.markdown(f"**Impact:** {Impact_Innovation['Impact']}")
        st.markdown(f"**Innovation:** {Impact_Innovation['Innovation']}")
        st.write("**Follow-Up Questions**")
        for i, question in enumerate(Impact_Innovation["Follow-Up Questions"]):
            st.markdown(f"- {question}")
        st.markdown(
            """
        <style>
        [dara-testid="stMarkdownContainer"] ul{
                    padding-left:40px;
        }
        </style>
        """,
            unsafe_allow_html=True,
        )
        rating = Impact_Innovation["Rating"]
        star_emoji_string = "⭐" * int(rating)
        st.markdown(f"**Rating:** {star_emoji_string}")
