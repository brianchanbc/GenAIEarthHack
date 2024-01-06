import os
import dotenv
import streamlit as st
from openai import OpenAI

# Load OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    dotenv.load_dotenv(".env")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def main():
    # Initialize session state variables if they don't exist
    if 'uploaded_button_clicked' not in st.session_state:
        st.session_state['uploaded_button_clicked'] = False
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []
    if 'thread' not in st.session_state:
        st.session_state['thread'] = None
    if 'assistant' not in st.session_state:
        st.session_state['assistant'] = None

    client = OpenAI()

    # Create two columns for the layout
    col1, col2 = st.columns(2)

    # Text area for user to type in context or ideas in the first column
    with col1:
        typed_text = st.text_area("Type in your ideas here:", height=150)

    # File uploader for PDFs in the second column
    with col2:
        uploaded_files = st.file_uploader("Upload PDF files here:", 
                                          type=["pdf"], 
                                          accept_multiple_files=True,
                                          label_visibility='visible')

    # Process input (files or typed text)
    if st.button('Process Input'):
        file_ids = []
        uploaded_logs = []
        st.session_state['uploaded_button_clicked'] = True

        # Reset messages to avoid re-sending old messages
        st.session_state['messages'] = []

        with st.spinner('Processing Input...'):
            # Handle file uploads
            for uploaded_file in uploaded_files:
                file_content = uploaded_file.read()
                oai_uploaded_file = client.files.create(
                    file=file_content,
                    purpose='assistants'
                )
                uploaded_log = {"file_name": uploaded_file.name, "file_id": oai_uploaded_file.id}
                uploaded_logs.append(uploaded_log)
                file_ids.append(oai_uploaded_file.id)

            # Create assistant with context from uploaded files and/or typed text
            typed_text_log = f"Typed Text Context: {typed_text}" if typed_text else ""
            assistant = client.beta.assistants.create(
                instructions=f"""
                You are a helpful assistant for answering questions based on uploaded files and/or typed text context. 
                Here's your file_id and file_name mapping:
                {str(uploaded_logs)}

                {typed_text_log}

                Please use this information to understand the context of the user's questions.
                """,
                model="gpt-4-1106-preview",
                tools=[{"type": "retrieval"}],
                file_ids=file_ids
            )
            st.session_state['assistant'] = assistant

            # Create a new thread
            thread = client.beta.threads.create(
                messages=st.session_state.messages
            )
            st.session_state['thread'] = thread

    # Display chat history
    for message in st.session_state.messages:
        if message["role"] == "assistant":
            st.chat_message("assistant").write(message["content"])
        else:
            st.chat_message("user").write(message["content"])

    # Chat input for interaction
    if st.session_state['assistant']:
        if prompt := st.chat_input("Enter your message here"):
            user_message = {
                "role": "user",
                "content": prompt
            }
            st.session_state.messages.append(user_message)
            
            # Display user message immediately in the chat history
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
