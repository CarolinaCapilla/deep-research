---
title: Deep Research Agent
emoji: 🔎
colorFrom: indigo
colorTo: green
sdk: gradio
sdk_version: "5.47.2"
app_file: app.py
python_version: "3.11"
pinned: false
---

# Deep Research AI Agent

An intelligent research assistant powered by AI agents that performs comprehensive web research, generates reports, and sends email summaries. Built with Gradio for an intuitive web interface.

## ⚡ Quickstart

Run with Docker (recommended):

1. Copy env template and set your key(s)

```bash
cp .env.example .env
# edit .env and set OPENAI_API_KEY (required). Optionally set SENDGRID_API_KEY, FROM_EMAIL, TO_EMAIL.
```

2. Start the app

```bash
# using docker compose (auto-loads .env)
docker compose up --build

# or plain Docker
docker build -t deep-research .
docker run --rm -p 7860:7860 --env-file .env deep-research
```

3. Open the UI
   http://localhost:7860

Try these queries:

- What are the key differences between GPT-4.1, GPT-4o, and Claude 3.7 Sonnet for research tasks?
- Summarize the latest developments in small language models (SLMs) and how they compare to LLMs in 2025.
- What are the best practices for Retrieval-Augmented Generation (RAG) vs fine-tuning for domain-specific QA?
- What happened in the [YOUR TOPIC] space over the last 12 months? Provide sources and links.
- Compare leading vector databases for production RAG (performance, cost, ecosystem) with references.

Note about how this agent works:
- This agent doesn’t “know” about itself or your environment. It plans web searches, gathers information from the web, and writes a report from found sources.
- It won’t answer personal questions about the app or the user. Ask topic-oriented questions that can be researched online.

Run locally (without Docker):

```bash
# optional but recommended
python -m venv .venv && source .venv/bin/activate

# install deps
pip install -r requirements.txt

# env vars
cp .env.example .env
# edit .env and set OPENAI_API_KEY (required)

# run
python app.py
```

## 🚀 Features

- **AI-Powered Research Planning**: Uses specialized agents to plan and execute research queries
- **Multi-Agent Architecture**: Separate agents for planning, searching, writing, and email delivery
- **Web Interface**: Clean Gradio UI for easy interaction
- **Automated Email Reports**: Automatically sends research summaries via email
- **Trace Integration**: OpenAI trace support for debugging and monitoring
- **Modular Design**: Easy to extend with additional agent types

## 🏗️ Architecture

The system consists of several specialized AI agents:

- **Planner Agent**: Analyzes queries and creates research plans
- **Search Agent**: Performs web searches based on research plans
- **Writer Agent**: Generates comprehensive research reports
- **Email Agent**: Formats and sends email summaries
- **Research Manager**: Orchestrates the entire research pipeline

## 📋 Prerequisites

- Python 3.12+
- OpenAI API key
- Email service credentials (SendGrid recommended)

## 🛠️ Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/CarolinaCapilla/deep-research.git
   cd deep-research
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   # or if using uv
   uv sync
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   SENDGRID_API_KEY=your_sendgrid_api_key_here
   FROM_EMAIL=your_email@example.com
   TO_EMAIL=recipient@example.com
   ```

## 🚀 Usage

### Running the Web App

```bash
python app.py
```

This will launch a Gradio web interface where you can:

1. Enter your research query
2. Click "Run" to start the research process
3. View real-time progress updates
4. Receive the final research report

### Programmatic Usage

```python
from agents.research_manager import ResearchManager
import asyncio

async def main():
    manager = ResearchManager()
    async for update in manager.run("What are the latest developments in quantum computing?"):
        print(update)

asyncio.run(main())
```

## 📁 Project Structure

```
deep-research/
├── app/
│   ├── __init__.py
│   ├── deep_research.py      # Gradio UI (loads .env)
│   ├── research_manager.py   # Orchestrates research pipeline (email optional)
│   ├── planner_agent.py      # Plans research queries
│   ├── search_agent.py       # Performs web searches
│   ├── writer_agent.py       # Generates reports
│   └── email_agent.py        # Sends email summaries (optional)
├── archive/
│   └── legacy_agents/        # Archived older implementation
├── app.py                    # Entrypoint that serves Gradio on 0.0.0.0:$PORT
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── requirements.txt
├── pyproject.toml
└── README.md
```

## 🔧 Configuration

### Agent Configuration

Each agent can be configured in its respective file:

- **Planner Agent**: Modify `HOW_MANY_SEARCHES` in `planner_agent.py`
- **Search Agent**: Customize search behavior in `search_agent.py`
- **Writer Agent**: Adjust report formatting in `writer_agent.py`

### Email Configuration

You can deliver email in two ways: SendGrid (recommended for production) or SMTP (great for local testing with MailHog/Mailtrap).

#### Option A — SendGrid (production)

1. Create a SendGrid account and verify a sender (single sender or domain).
2. Add the following to your `.env` (or HF Spaces Secrets):

```env
SENDGRID_API_KEY=your_sendgrid_api_key
FROM_EMAIL=verified_sender@example.com
TO_EMAIL=recipient@example.com
```

Notes:
- FROM_EMAIL must be verified in your SendGrid account.
- If `SENDGRID_API_KEY` is set, the app uses SendGrid automatically.

#### Option B — SMTP (MailHog/Mailtrap)

If `SENDGRID_API_KEY` is not set but `SMTP_SERVER` is set, the app sends via SMTP.

- Local testing with Docker Compose + MailHog:
   ```env
   SMTP_SERVER=mailhog
   SMTP_PORT=1025
   SMTP_STARTTLS=0
   FROM_EMAIL=test@example.com
   TO_EMAIL=someone@example.com
   ```
   - Start with `docker compose up --build`
   - View emails: http://localhost:8025

- Local app (venv) + MailHog running on your Mac:
   ```env
   SMTP_SERVER=127.0.0.1
   SMTP_PORT=1025
   SMTP_STARTTLS=0
   FROM_EMAIL=test@example.com
   TO_EMAIL=someone@example.com
   ```

- App in Docker container, MailHog on your host (macOS):
   ```env
   SMTP_SERVER=host.docker.internal
   SMTP_PORT=1025
   SMTP_STARTTLS=0
   FROM_EMAIL=test@example.com
   TO_EMAIL=someone@example.com
   ```

- Mailtrap (cloud inbox via SMTP):
   ```env
   SMTP_SERVER=smtp.mailtrap.io
   SMTP_PORT=2525
   SMTP_USERNAME=your_mailtrap_user
   SMTP_PASSWORD=your_mailtrap_pass
   SMTP_STARTTLS=1
   FROM_EMAIL=anything@example.com
   TO_EMAIL=your_inbox@in.mailtrap.io
   ```

The app will display status messages like “Email sent (code: …)” or a clear skip/error reason.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## Troubleshooting

### Common Issues

1. **Import errors**: Make sure all dependencies are installed with `pip install -r requirements.txt`
2. **OpenAI API errors**: Verify your API key is correct in the `.env` file
3. **Email delivery issues**: Check your SendGrid configuration and API key
4. **Gradio not starting**: Ensure port 7860 is available

### Debug Mode

Enable debug logging by setting the environment variable:

```bash
export DEBUG=1
```

## 🔄 Future Enhancements

- [ ] Implement research result caching
- [ ] Add export options (PDF, DOCX)
- [ ] Implement research history and favorites

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/CarolinaCapilla/deep-research/issues) page
2. Create a new issue with detailed information
3. Include error messages and steps to reproduce

---

**Made with ❤️ using AI agents and Gradio**
