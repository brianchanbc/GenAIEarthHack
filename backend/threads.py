from openai import OpenAI
import dotenv
import os
import streamlit as st
import time

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    dotenv.load_dotenv(".env")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI()

def create_assistant(
    uploaded_files,
    problem_text,
    solution_text,
    instruction,
    prompt,
    assistant_id
):
    start_time = time.time()
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
    file_context_log = f"File Context: {str(uploaded_logs)}"
    
    # Create assistant with context from Problem, Solution, and uploaded files
    assistant = client.beta.assistants.create(
        instructions=instruction.format(problem_text=problem_text, solution_text=solution_text, uploaded_logs=file_context_log),
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
        content=prompt,
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
    st.session_state[assistant_id] = assistant_response.replace("```json","").replace("```","")
    
    
    print(f"Time eplapsed: {time.time() - start_time}")
    

