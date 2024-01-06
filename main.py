import os
import dotenv
import streamlit as st
from backend.threads import create_assistant

# Load OpenAI API key

OVERVIEW_PROMPT = """
            Based on the information provided, generate a short Overview of the user's PROBLEM and 
            its circular economy SOLUTION, and identify the Relevant Industries. You MUST adhere to
            the following:
            - Overview should be a brief but meaningful summary of the user's PROBLEM and its circular
            economy SOLUTION
            - Overview MUST be between 1-2 sentences long.
            - If possible, identify between 1-3 Relevant Industries. If no specific industry is mentioned,
            respond with "None".
            You MUST format your response as a JSON object, using the following format:
            {{Overview:'', Relevant Industries:''}}.
            """

SUSTAINABILITY_PROMPT = """Based on the information provided, you MUST do the following:
                        1. Provide a comprehensive evaluation on how well the user's SOLUTION adheres to 
                        each of the 3 principles of circular economy: 1) Eliminate waste and pollution, 
                        2) Circulate products and materials (at their highest value), and 3) Regenerate nature.
                        2. Provide a series of follow-up questions investors may ask the user with regard to
                        their PROBLEM and SOLUTION.
                        3. Provide a rating between 1 and 5 (highest) on how sustainable the user's SOLUTION is.
                        You MUST format your response as a JSON object, using the following format:
                        {{Eliminate waste and pollution:'', Circulate products and materials'', Regenerate nature, 
                        Follow-Up Questions: '', Rating:''}}.
                        """

BUSINESS_PROMPT = ""
IMPACT_INNOVATION_PROMPT = ""

def main():
    # Initialize session state variables if they don't exist
    if "uploaded_button_clicked" not in st.session_state:
        st.session_state["uploaded_button_clicked"] = False
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    if "thread" not in st.session_state:
        st.session_state["thread"] = None
    if "assistant" not in st.session_state:
        st.session_state["assistant"] = None

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

    # Process input
    if st.button("Process Input"):
        st.session_state["uploaded_button_clicked"] = True
        st.session_state["messages"] = []

        with st.spinner("Processing Input..."):
            # Handle file uploads
            create_assistant(uploaded_files, problem_text, solution_text, OVERVIEW_PROMPT)
            create_assistant(uploaded_files, problem_text, solution_text, SUSTAINABILITY_PROMPT)


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
