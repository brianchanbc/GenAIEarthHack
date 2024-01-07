from openai import OpenAI
import dotenv
import os
import streamlit as st
import time
from .utils import extract_json

dotenv.load_dotenv(".env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL")

client = OpenAI()

def create_assistant_file(uploaded_file, a):
    assistant_file = client.files.create(
        file=uploaded_file,
        prupose="assistants"
        )
    return assistant_file

def create_assistant(
        name,
        instructions,
        problem,
        solution, 
        model=OPENAI_MODEL, 
        assistant_files=[]
):
    if len(assistant_files) != 0:
        assistant = client.beta.assistants.create(
            instructions=instructions.format(problem_text=problem, solution_text=solution),
            name=name,
            tools=[{"type": "retrieval"}],
            model=model,
            file_ids=[file.id for file in assistant_files]
        )
    else:
        assistant = client.beta.assistants.create(
            instructions=instructions.format(problem_text=problem, solution_text=solution),
            name=name,
            model=model
        )
    return assistant

def get_assistant_id(assistant_name):
    all_assistants = client.beta.assistants.list(limit="10")
    for assistant in all_assistants.data:
        if assistant.name == assistant_name:
            return assistant.id
    return None
    
def retrieve_assistant(assistant_id):
    assistant = client.beta.assistants.retrieve(assistant_id)
    return assistant

def create_thread():
    thread = client.beta.threads.create()
    return thread

def create_message(message, thread):
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=message,
    )
    return message

def retrieve_latest_message_content(thread):
    message = client.beta.threads.messages.list(
        thread_id=thread.id,
        limit=1
    )
    message_content = message.data[0].content[0].text.value
    return message_content

def create_run(thread, assistant_id):
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )
    return run

def retrieve_run(thread, run):
    run = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )
    return run

def process_uploaded_files(uploaded_files):
    assistant_files = [create_assistant_file(file) for file in uploaded_files]
    return assistant_files

def generate_response(
        assistant_name, 
        problem, 
        solution, 
        instructions, 
        message,
        thread=None
    ):
    
    assistant_id = get_assistant_id(assistant_name)
    
    if not assistant_id:
        assistant = create_assistant(assistant_name, instructions, problem, solution)
        assistant_id = assistant.id

    if not thread:
        thread = create_thread()
    
    message = create_message(message, thread)
    run = create_run(thread, assistant_id)

    while run.status != "completed":
        run = retrieve_run(thread, run)
    
    response = retrieve_latest_message_content(thread)

    return thread, response