from openai import OpenAI
import streamlit as st

client = OpenAI()


def create_main_assistant(
    uploaded_files,
    problem_text,
    solution_text,
):
    file_ids = []
    uploaded_logs = []
    for uploaded_file in uploaded_files:
        file_content = uploaded_file.read()
        oai_uploaded_file = client.files.create(file=file_content, purpose="assistants")
        uploaded_log = {
            "file_name": uploaded_file.name,
            "file_id": oai_uploaded_file.id,
        }
        uploaded_logs.append(uploaded_log)
        file_ids.append(oai_uploaded_file.id)

    # Create assistant with context from Problem, Solution, and uploaded files
    context_log = (
        f"Problem: {problem_text}\nSolution: {solution_text}"
        if problem_text or solution_text
        else ""
    )
    file_context_log = f"File Context: {str(uploaded_logs)}"
    assistant = client.beta.assistants.create(
        instructions=f"""
        You are a helpful assistant for answering questions based on Problem, Solution, and uploaded files.
        {context_log}
        {file_context_log}
        Please use this information to understand the context of the user's questions.
        """,
        model="gpt-4-1106-preview",
        tools=[{"type": "retrieval"}],
        file_ids=file_ids,
    )

    # Create a new thread
    thread = client.beta.threads.create()
    st.session_state["assistant"] = assistant
    # Create a new thread
    st.session_state["thread"] = thread
