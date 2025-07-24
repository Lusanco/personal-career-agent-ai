# Personal Career Agent AI

[![Live Demo](https://img.shields.io/badge/Live-Demo-blue)](https://lasc1026-personal-career-agent-ai.hf.space/)

A custom AI chatbot that represents **me** in a professional context. It is designed to answer recruiter questions based on my real experience, resume, and past interviews using a structured set of markdown files and a streamlined chat interface.

## 🔗 Live App

👉 [Try it here](https://lasc1026-personal-career-agent-ai.hf.space/)

## 💡 Features

- Simulates me during recruiter interactions
- Pulls from resume, LinkedIn, interview, and prompt files
- Lightweight agentic logic with no framework overhead
- Gradio chat interface

## 🛠️ Tech Stack

- **Python**
- **Gradio** – for building the web interface
- **OpenAI Python SDK** (`openai`) – to interact with LLMs
- **dotenv** – for environment variable management
- **Markdown** – stores resume, prompt, and context data

## 📁 Context Files Used

Located in the `./luis-santiago/` folder:

- `master_prompt.md`
- `resume.md`, `refined_resume.md`, `old_resume.md`
- `linkedin.md`
- `simulated_interview.md`, `refined_simulated_interview.md`

These files are loaded and injected into the system prompt.

I intend to iterate over this in the future!
