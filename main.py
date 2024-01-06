import os
import dotenv
import streamlit as st
from backend.threads import create_assistant
import backend.instructions_and_prompts as ip

# Load OpenAI API key


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
            print("yo" + st.session_state["general_assistant"])
        # JSON Data Definitions
    if st.session_state["show_report"] == True:
        Overview = {
            "Overview": {
                "Overview": "This section provides a general summary and overall context.",
                "Relevant Industries": "This is a section for industry"
            }
        }

        Sustainability = {
            "Sustainability": {
                "Eliminate waste and pollution:": "1",
                "Circulate products and materials": "Your question and answer content here",
                "Regenerate natural": "Your question and answer content here",
                "Follow-Up Questions": ["XXXX", "yyyyy"],
                "Rating": "3",
            }
        }

        Business = {
            "Business": {
                "Assessment": "XXXXXXXX",
                "Follow-Up Questions": "XXXXXXXx",
                "Rating": "1"
            }
        }

        Impact_Innovation = {
            "Impact": "XXXXXXX",
            "Innovation": "XXXXXXXXX",
            "Q&A": "XXXXX"
        }

        Recommendation = {
            "1": "xxxxxxx",
            "2": "xxxxxxxx",
            "3": "xxxxxxxx"
        }

        # Display JSON Data
        st.title("Project Evaluation Report")

        st.header("Report Overview")
        st.subheader("Overview")
        st.write(Overview["Overview"]["Overview"])
        st.subheader("Relevant Industries")
        st.write(Overview["Overview"]["Relevant Industries"])

        with st.expander("Sustainability"):
            st.markdown(f"**Eliminate waste and pollution:** {Sustainability['Sustainability']['Eliminate waste and pollution:']}")
            st.markdown(f"**Circulate products and materials:** {Sustainability['Sustainability']['Circulate products and materials']}")
            st.markdown(f"**Regenerate nature:** {Sustainability['Sustainability']['Regenerate natural']}")

            for i, question in enumerate(Sustainability['Sustainability']['Follow-Up Questions']):
                st.markdown(f"**Follow-Up Question {i+1}:** {question}")
            
            rating = Sustainability['Sustainability']['Rating']
            star_emoji_string = "⭐" * int(rating)

            st.markdown(f"**Rating:** {star_emoji_string}")

        with st.expander("Business Insights"):
            st.markdown(f"**Assessment::** {Business['Business']['Assessment']}")
            st.markdown(f"**Follow-Up Questions:** {Business['Business']['Follow-Up Questions']}")
            rating = Sustainability['Sustainability']['Rating']
            star_emoji_string = "⭐" * int(rating)
            st.markdown(f"**Rating:** {star_emoji_string}")

        with st.expander("Impact and Innovation"):
            st.markdown(f"**Impact:** {Impact_Innovation['Impact']}")
            st.markdown(f"**Innovation:** {Impact_Innovation['Innovation']}")
            st.markdown(f"**Q&A:** {Impact_Innovation['Q&A']}")

        with st.expander("Recommendations"):
            for key, value in Recommendation.items():
                st.markdown(f"- **Recommendation {key}:** {value}")

    # Chat Interaction
    # Display chat history
    for message in st.session_state.messages:
        if message["role"] == "assistant":
            st.chat_message("assistant").write(message["content"])
        else:
            st.chat_message("user").write(message["content"])

    # Chat input for interaction
    if st.session_state["assistant"]:
        if prompt := st.chat_input("Enter your message here"):
            user_message = {"role": "user", "content": prompt}
            st.session_state.messages.append(user_message)

            # Display user message immediately in the chat history
            st.chat_message("user").write(prompt)

            message = client.beta.threads.messages.create(
                thread_id=st.session_state["thread"].id, role="user", content=prompt
            )

            with st.chat_message("assistant"):
                with st.spinner("Waiting for the assistant's response..."):
                    run = client.beta.threads.runs.create(
                        thread_id=st.session_state["thread"].id,
                        assistant_id=st.session_state["assistant"].id,
                    )

                    while run.status != "completed":
                        run = client.beta.threads.runs.retrieve(
                            thread_id=st.session_state["thread"].id, run_id=run.id
                        )

                    messages = client.beta.threads.messages.list(
                        thread_id=st.session_state["thread"].id
                    )
                    assistant_response = messages.data[0].content[0].text.value

                    st.session_state.messages.append(
                        {"role": "assistant", "content": assistant_response}
                    )
                    st.write(assistant_response.replace("$", "\$"))


if __name__ == "__main__":
    main()
