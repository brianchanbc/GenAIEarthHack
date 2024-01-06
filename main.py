import json
import os
import dotenv
import streamlit as st
from backend.threads import create_assistant
import backend.instructions_and_prompts as ip

# Load OpenAI API key
dotenv.load_dotenv(".env")

def main():
    # Initialize session state variables if they don't exist
    if "show_report" not in st.session_state:
        st.session_state["show_report"] = False
    if 'uploaded_button_clicked' not in st.session_state:
        st.session_state['uploaded_button_clicked'] = False
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []
    if 'thread' not in st.session_state:
        st.session_state['thread'] = None
    if 'assistant' not in st.session_state:
        st.session_state['assistant'] = None

    # Create layout for Problem and Solution input
    col1, col2 = st.columns(2)
    with col1:
        problem_text = st.text_area("Describe the Problem:", height=150)
    with col2:
        solution_text = st.text_area("Propose a Solution:", height=150)

    # File uploader for PDFs
    uploaded_files = st.file_uploader("Upload PDF files here:", type=["pdf"], accept_multiple_files=True)

    # Process input
    if st.button('Process Input'):
        if not problem_text and not solution_text and len(uploaded_files) == 0:
            st.error("Please upload or input contents.")
        else:
            flag = True
            file_ids = []
            uploaded_logs = []
            st.session_state["show_report"] = True
            st.session_state['uploaded_button_clicked'] = True
            st.session_state['messages'] = []

            with st.spinner("Processing Input..."):
                # Handle file uploads
                create_assistant(
                    uploaded_files,
                    problem_text,
                    solution_text,
                    ip.OVERVIEW_INSTRUCTIONS,
                    ip.OVERVIEW_PROMPT,
                    "general_assistant",
                )

            # Display JSON Data
            st.title("Project Evaluation Report")
            print(st.session_state["general_assistant"])

            Overview = json.loads(st.session_state["general_assistant"])
            st.header("Report Overview")
            st.subheader("Overview")
            st.write(Overview["Overview"])
            st.subheader("Relevant Industries")
            st.write(Overview["Relevant Industries"])

            with st.spinner("Processing Input..."):
                # Handle file uploads
                create_assistant(
                    uploaded_files,
                    problem_text,
                    solution_text,
                    ip.SUSTAINABILITY_INSTRUCTIONS,
                    ip.SUSTAINABILITY_PROMPT,
                    "sus_assistant",
                )
            # Rest of your code for JSON Data Definitions, Display, and Chat Interaction goes here
            print(st.session_state["sus_assistant"])
            Sustainability = json.loads(st.session_state["sus_assistant"])

            with st.expander("Sustainability"):
                st.markdown(f'<span style="font-size: 20px;"><b>Eliminate waste and pollution:</b></span> {Sustainability["Eliminate waste and pollution"]}', unsafe_allow_html=True)
                st.markdown(f'<span style="font-size: 20px;"><b>Circulate products and materials:</b></span> {Sustainability["Circulate products and materials"]}', unsafe_allow_html=True)
                st.markdown(f'<span style="font-size: 20px;"><b>Regenerate nature:</b></span> {Sustainability["Regenerate nature"]}', unsafe_allow_html=True)


                for i, question in enumerate(Sustainability['Follow-Up Questions']):
                    st.markdown(f'<span style="font-size: 20px;"><b>Follow-Up Question {i+1}:</b></span> {question}', unsafe_allow_html=True)
            
                rating = Sustainability['Rating']
                star_emoji_string = "⭐" * int(rating)

                st.markdown(f'<span style="font-size: 20px;"><b>Rating:</b></span> {star_emoji_string}', unsafe_allow_html=True)

            with st.spinner("Processing Input..."):
                # Handle file uploads
                create_assistant(
                    uploaded_files,
                    problem_text,
                    solution_text,
                    ip.BUSINESS_INSTRUCTIONS,
                    ip.BUSINESS_PROMPT,
                    "bus_assistant",
                )

            print(st.session_state["bus_assistant"])
            Business = json.loads(st.session_state["bus_assistant"])

            with st.expander("Business Assessment"):
                for i, assessment in enumerate(Business['Assessment']):
                    st.markdown(f'<span style="font-size: 20px;"><b>Assessment {i+1}:</b></span> {assessment}', unsafe_allow_html=True)
                for i, question in enumerate(Business['Follow-Up Questions']):
                    st.markdown(f'<span style="font-size: 20px;"><b>Follow-Up Question {i+1}:</b></span> {question}', unsafe_allow_html=True)
                rating = Business['Rating']
                star_emoji_string = "⭐" * int(rating)
                st.markdown(f'<span style="font-size: 20px;"><b>Rating:</b></span> {star_emoji_string}', unsafe_allow_html=True)

            with st.spinner("Processing Input..."):
                # Handle file uploads
                create_assistant(
                    uploaded_files,
                    problem_text,
                    solution_text,
                    ip.IMPACT_INNOVATION_INSTRUCTIONS,
                    ip.IMPACT_INNOVATION_PROMPT,
                    "imp_assistant",
                )

            print(st.session_state["imp_assistant"])
            Impact_Innovation = json.loads(st.session_state["imp_assistant"])

            with st.expander("Impact and Innovation"):
                st.markdown(f'<span style="font-size: 20px;"><b>Impact:</b></span> {Impact_Innovation["Impact"]}', unsafe_allow_html=True)
                st.markdown(f'<span style="font-size: 20px;"><b>Innovation:</b></span> {Impact_Innovation["Innovation"]}', unsafe_allow_html=True)
                for i, question in enumerate(Impact_Innovation['Follow-Up Questions']):
                    st.markdown(f'<span style="font-size: 20px;"><b>Follow-Up Question {i+1}:</b></span> {question}', unsafe_allow_html=True)
                rating = Impact_Innovation['Rating']
                star_emoji_string = "⭐" * int(rating)
                st.markdown(f'<span style="font-size: 20px;"><b>Rating:</b></span> {star_emoji_string}', unsafe_allow_html=True)


            Recommendation = {
                "1": "xxxxxxx",
                "2": "xxxxxxxx",
                "3": "xxxxxxxx"
            }


            with st.expander("Recommendations"):
                for key, value in Recommendation.items():
                    st.markdown(f'Recommendation {key}: {value}', unsafe_allow_html=True)

        # Chat Interaction
    for message in st.session_state.messages:
        if message["role"] == "assistant":
            st.chat_message("assistant").write(message["content"])
        else:
            st.chat_message("user").write(message["content"])

    if st.session_state['assistant']:
        if prompt := st.chat_input("Enter your message here"):
            user_message = {
                "role": "user",
                "content": prompt
            }
            st.session_state.messages.append(user_message)
            
            st.chat_message("user").write(prompt)

            message = client.beta.threads.messages.create(
                thread_id=st.session_state['thread'].id,
                role="user",
                content=prompt
            )

            with st.chat_message("assistant"):
                with st.spinner("Waiting for the assistant's response..."):
                    run = client.beta.threads.runs.create(
                        thread_id=st.session_state['thread'].id,
                        assistant_id=st.session_state['assistant'].id
                    )

                    while run.status != "completed":
                        run = client.beta.threads.runs.retrieve(
                            thread_id=st.session_state['thread'].id,
                            run_id=run.id
                        )

                    messages = client.beta.threads.messages.list(thread_id=st.session_state['thread'].id)
                    assistant_response = messages.data[0].content[0].text.value

                    st.session_state.messages.append(
                        {"role": "assistant", "content": assistant_response}
                    )
                    st.write(assistant_response.replace("$", "\$"))
if __name__ == "__main__":
    main()