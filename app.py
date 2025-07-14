# Imports
import os
import json
import gradio as gr
from typing import cast
from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader

# OpenAI types
from openai.types.chat import ChatCompletionMessageParam

# Markdown output display
from IPython.display import Markdown, display


# Cast to String
def env_to_str(env: str) -> str:
    return cast(str, os.getenv(env))


# Load Environment Variables
load_dotenv(override=True)

# Gemini Environment Variables
gemini_api_key = env_to_str("GEMINI_API_KEY")
gemini_base_url = env_to_str("GEMINI_BASE_URL")
model_gemini_flash = env_to_str("MODEL_GEMINI_FLASH")

# Gemini Client
gemini = OpenAI(api_key=gemini_api_key, base_url=gemini_base_url)
# List for storing notifications instead of using Pushover
notifications = []


# Push Function
def push(message):
    """
    Prints a message and adds it to the global notifications list.
    """
    print(f"Notification: {message}")
    notifications.append(message)


# Example of the new push function
push("New Notification!")
# Notebook Printing
notifications
# Tool for the LLM's


def record_user_details(email, name="Name not provided", notes="not provided"):
    """
    Records user interest and saves a notification to a list.
    """
    push(f"Recording interest from {name} with email {email} and notes {notes}")
    return {"recorded": "ok"}


# Tool for the LLM's


def record_unknown_question(question):
    """
    Records a question that could not be answered and saves a notification to a list.
    """
    push(f"Recording an unanswered question: {question}")
    return {"recorded": "ok"}


# JSON definitions for the tool
record_user_details_json = {
    "name": "record_user_details",
    "description": "Use this tool to record that a user is interested in being in touch and provided an email address",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "description": "The email address of this user",
            },
            "name": {
                "type": "string",
                "description": "The user's name, if they provided it",
            },
            "notes": {
                "type": "string",
                "description": "Any additional information about the conversation that's worth recording to give context",
            },
        },
        "required": ["email"],
        "additionalProperties": False,
    },
}
# JSON definitions for the tool
record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Always use this tool to record any question that couldn't be answered as you didn't know the answer",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The question that couldn't be answered",
            }
        },
        "required": ["question"],
        "additionalProperties": False,
    },
}
# Tools for the tools call
tools = [
    {"type": "function", "function": record_user_details_json},
    {"type": "function", "function": record_unknown_question_json},
]
# Notebook Printing
tools


# This function can take a list of tool calls, and run them.
def handle_tool_calls(tool_calls):
    results = []
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        print(f"Tool called: {tool_name}", flush=True)

        # This elegant way of calling the function
        tool = globals().get(tool_name)
        result = tool(**arguments) if tool else {}
        results.append(
            {
                "role": "tool",
                "content": json.dumps(result),
                "tool_call_id": tool_call.id,
            }
        )
    return results


# Read PDF
try:
    reader = PdfReader("./other/linkedin.pdf")
    linkedin = ""
    for page in reader.pages:
        text = page.extract_text()
        if text:
            linkedin += text

    with open("./other/summary.txt", "r", encoding="utf-8") as f:
        summary = f.read()

    name = "Luis Santiago"

    system_prompt = f"""You are acting as {name}. You are answering questions on {name}'s website, \
    particularly questions related to {name}'s career, background, skills and experience. \
    Your responsibility is to represent {name} for interactions on the website as faithfully as possible. \
    You are given a summary of {name}'s background and LinkedIn profile which you can use to answer questions. \
    Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
    If you don't know the answer to any question, use your record_unknown_question tool to record the question that you couldn't answer, even if it's about something trivial or unrelated to career. \
    If the user is engaging in discussion, try to steer them towards getting in touch via email; ask for their email and record it using your record_user_details tool. 

    ## Summary:
    {summary}

    ## LinkedIn Profile:
    {linkedin}

    With this context, please chat with the user, always staying in character as {name}."""

except FileNotFoundError:
    print(
        "Warning: './other/linkedin.pdf' or './other/summary.txt' not found. Using a default system prompt."
    )
    name = "AI Assistant"
    system_prompt = "You are a helpful AI assistant. Since your personal context is not available, please inform the user and answer their questions generally."


# Chat Function
def chat(message, history):
    messages = (
        [{"role": "system", "content": system_prompt}]
        + history
        + [{"role": "user", "content": message}]
    )
    done = False
    while not done:
        response = gemini.chat.completions.create(
            model=model_gemini_flash, messages=messages, tools=tools
        )
        finish_reason = response.choices[0].finish_reason

        if finish_reason == "tool_calls":
            message = response.choices[0].message
            tool_calls = message.tool_calls
            results = handle_tool_calls(tool_calls)
            messages.append(message)
            messages.extend(results)
        else:
            done = True
    return response.choices[0].message.content


# Launch the Gradio Interface
gr.ChatInterface(chat, type="messages").launch()
notifications
