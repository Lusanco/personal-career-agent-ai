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


# Read PDF
try:
    # Do the following for system_prompt, summary, linkedin,
    # and all materials in the luis-santiago directory

    # System Prompt
    with open("./luis-santiago/system_prompt.md", "r", encoding="utf-8") as file:
        system_prompt = file.read()

    # Resume
    with open("./luis-santiago/resume.md", "r", encoding="utf-8") as file:
        resume = file.read()

    # Refined Resume
    with open("./luis-santiago/refined_resume.md", "r", encoding="utf-8") as file:
        refined_resume = file.read()

    # Old Resume Details
    with open("./luis-santiago/old_resume.md", "r", encoding="utf-8") as file:
        old_resume = file.read()

    # LinkedIn Details
    with open("./luis-santiago/linkedin.md", "r", encoding="utf-8") as file:
        linkedin = file.read()

    # Simulated Interview
    with open("./luis-santiago/simulated_interview.md", "r", encoding="utf-8") as file:
        simulated_interview = file.read()

    # Refined Simulated Interview
    with open(
        "./luis-santiago/refined_simulated_interview.md", "r", encoding="utf-8"
    ) as file:
        refined_simulated_interview = file.read()

    # Data Set
    data_set = f"""
Master Prompt:
{system_prompt}

Refined Resume:
{refined_resume}

Resume:
{resume}

Old Resume Details:
{old_resume}

LinkedIn Details:
{linkedin}

Simulated Interview:
{simulated_interview}
"""

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
