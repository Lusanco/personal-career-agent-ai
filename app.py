# Imports
import os
import gradio as gr
from typing import cast
from dotenv import load_dotenv
from openai import OpenAI

# OpenAI types
from openai.types.chat import ChatCompletionMessageParam


# Cast to String
def env_to_str(env: str) -> str:
    return cast(str, os.getenv(env))


# Main
def main():
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
        # System Prompt
        with open("./luis-santiago/master_prompt.md", "r", encoding="utf-8") as file:
            master_prompt = file.read()

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
        with open(
            "./luis-santiago/simulated_interview.md", "r", encoding="utf-8"
        ) as file:
            simulated_interview = file.read()

        # Refined Simulated Interview
        with open(
            "./luis-santiago/refined_simulated_interview.md", "r", encoding="utf-8"
        ) as file:
            refined_simulated_interview = file.read()

        # Data Set
        system_prompt = f"""
    Master Prompt:
    {master_prompt}

    Refined Resume:
    {refined_resume}

    Old Resume Details:
    {old_resume}

    LinkedIn Details:
    {linkedin}

    Refined Simulated Interview:
    {refined_simulated_interview}
    """

    except FileNotFoundError:
        print("File Not Found. Using default system prompt.")
        name = "AI Assistant"
        system_prompt = "You are a helpful AI assistant. Since your personal context is not available, please inform the user and refrain from answering."

    # Chat Function
    def chat(message, history):
        messages = (
            [{"role": "system", "content": system_prompt}]
            + history
            + [{"role": "user", "content": message}]
        )

        response = gemini.chat.completions.create(
            model=model_gemini_flash, messages=messages
        )
        return response.choices[0].message.content

    # Launch the Gradio Interface
    gr.ChatInterface(chat, type="messages").launch()


if __name__ == "__main__":
    main()
