from openai import OpenAI
import dotenv
import os
import streamlit as st

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    dotenv.load_dotenv(".env")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
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

    # Add a Message to a Thread
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="""
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
        """,
    )
    # print(message)

    # Run the assistant
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )
    
    while run.status != "completed":
    # Check the run status
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
    
    # Display the assistant's response
    messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )
    assistant_response = messages.data[0].content[0].text.value
    print(assistant_response)
