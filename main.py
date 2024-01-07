import json
import os
from urllib import response
import dotenv
import streamlit as st
from backend.threads import process_uploaded_files, generate_response, get_assistant
import backend.instructions_and_prompts as ip
from backend.utils import extract_json, generate_recommendation_input
from frontend.display import display_report

# Load OpenAI API key
dotenv.load_dotenv(".env")


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def main():
    local_css("style.css")
    # Initialize session state variables if they don't exist
    if "show_report" not in st.session_state:
        st.session_state["show_report"] = False
    if "uploaded_button_clicked" not in st.session_state:
        st.session_state["uploaded_button_clicked"] = False
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    if "assistant" not in st.session_state:
        st.session_state["assistant"] = None
    if "Report" not in st.session_state:
        st.session_state["Report"] = {}
    report_displayed = False

    # Create layout for Problem and Solution input
    col1, col2 = st.columns(2)
    with col1:
        problem_text = st.text_area("Describe the Problem:", height=150)
    with col2:
        solution_text = st.text_area("Propose a Solution:", height=150)

    # File uploader for PDFs
    uploaded_files = st.file_uploader(
        "Upload PDF files here:", type=["pdf"], accept_multiple_files=True
    )
    assistant_files = process_uploaded_files(uploaded_files)

    # Process input
    if st.button("Process Input"):
        if not problem_text and not solution_text and len(assistant_files) == 0:
            st.error("Please upload or input contents.")
        else:
            report_displayed = True
            # flag = True
            # file_ids = []
            # uploaded_logs = []
            st.session_state["show_report"] = True
            st.session_state["uploaded_button_clicked"] = True
            # st.session_state["messages"] = []

            with st.spinner("Processing Input..."):
                st.session_state["assistant"] = get_assistant(
                    "General Assistant",
                    ip.OVERVIEW_INSTRUCTIONS,
                    problem_text,
                    solution_text,
                    assistant_files,
                )

                st.session_state["thread"], general_response = generate_response(
                    st.session_state["assistant"],
                    ip.OVERVIEW_PROMPT,
                )
                print("General Response:", general_response)

            # Display JSON Data
            st.title("Project Evaluation Report")
            # print(st.session_state["general_assistant"])
            Overview = json.loads(extract_json(general_response))
            st.session_state["Report"]["Overview"] = Overview
            st.header("Report Overview")
            st.subheader("Overview")
            st.write(Overview["Overview"])
            st.subheader("Relevant Industries")
            st.write(Overview["Relevant Industries"])

            with st.spinner("Generating Sustainability Report..."):
                sus_assistant = get_assistant(
                    "Sustainability Assistant",
                    ip.SUSTAINABILITY_INSTRUCTIONS,
                    problem_text,
                    solution_text,
                    assistant_files,
                )

                sus_thread, sus_response = generate_response(
                    sus_assistant,
                    ip.SUSTAINABILITY_PROMPT,
                )
                print("Sustainability Response:", sus_response)

            Sustainability = json.loads(
                extract_json(sus_response.replace("```json", "").replace("```", ""))
            )
            st.session_state["Report"]["Sustainability"] = Sustainability
            with st.expander("Sustainability", expanded=True):
                st.markdown(
                    f"**Eliminate waste and pollution:** {Sustainability['Eliminate waste and pollution']}"
                )
                st.markdown(
                    f"**Circulate products and materials:** {Sustainability['Circulate products and materials']}"
                )
                st.markdown(
                    f"**Regenerate nature:** {Sustainability['Regenerate nature']}"
                )
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

            with st.spinner("Generating Business Assessment Report..."):
                bus_assistant = get_assistant(
                    "Business Assistant",
                    ip.BUSINESS_INSTRUCTIONS,
                    problem_text,
                    solution_text,
                    assistant_files,
                )
                bus_thread, bus_response = generate_response(
                    bus_assistant,
                    ip.BUSINESS_PROMPT,
                )
                print("Business Response:", bus_response)

            Business = json.loads(
                extract_json(bus_response).replace("```json", "").replace("```", "")
            )
            st.session_state["Report"]["Business"] = Business

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

            with st.spinner("Generating Impact and Innovation Report..."):
                imp_assistant = get_assistant(
                    "Impact & Innovation Assistant",
                    ip.IMPACT_INNOVATION_INSTRUCTIONS,
                    problem_text,
                    solution_text,
                    assistant_files,
                )
                imp_thread, imp_response = generate_response(
                    imp_assistant,
                    ip.IMPACT_INNOVATION_PROMPT,
                )
                print("Impact & Innovation Response:", imp_response)

            Impact_Innovation = json.loads(
                extract_json(imp_response.replace("```json", "").replace("```", ""))
            )
            st.session_state["Report"]["Impact_Innovation"] = Impact_Innovation

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

            # rec_input = generate_recommendation_input(
            #     Sustainability, Business, Impact_Innovation
            # )

            # rec_input = generate_recommendation_input(
            #     Sustainability, Business, "It is very innovative"
            # )

            # with st.spinner("Processing Input..."):
            #     rec_thread, rec_response = generate_response(
            #         general_assistant,
            #         ip.RECOMMENDATION_PROMPT.format(generated_assessments=rec_input),
            #         general_thread,
            #     )
            #     print("Recommendation Response:", rec_response)

            # Recommendation = json.loads(extract_json(rec_response))
            # st.write("**Recommendations**")
            # for recommendation in Recommendation["Recommendations"]:
            #     st.markdown(f"- {recommendation}")
            # st.markdown(
            #     """
            #     <style>
            #     [dara-testid="stMarkdownContainer"] ul{
            #                 padding-left:40px;
            #     }
            #     </style>
            #     """,
            #     unsafe_allow_html=True,
            # )

    if st.session_state["Report"] and not report_displayed:
        display_report()

    for message in st.session_state.messages:
        if message["role"] == "assistant":
            st.chat_message("assistant").write(message["content"])
        else:
            st.chat_message("user").write(message["content"])

    if st.session_state["assistant"]:
        if prompt := st.chat_input("Enter your message here"):
            user_message = {"role": "user", "content": prompt}
            st.session_state.messages.append(user_message)

            st.chat_message("user").write(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Waiting for the assistant's response..."):
                    _, assistant_response = generate_response(
                        st.session_state["assistant"],
                        prompt,
                        st.session_state["thread"],
                    )

                    st.session_state.messages.append(
                        {"role": "assistant", "content": assistant_response}
                    )
                    st.write(assistant_response.replace("$", "\$"))


if __name__ == "__main__":
    main()
