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

Update email settings in your `.env` file:

```env
FROM_EMAIL=noreply@yourdomain.com
TO_EMAIL=research@yourcompany.com
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

##  Troubleshooting

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

---

## Hugging Face Spaces metadata

The following metadata is provided for convenience when deploying to Spaces.

```yaml
title: Deep Research Agent
emoji: "🔎"
colorFrom: indigo
colorTo: green
sdk: gradio
sdk_version: "5.47.2"
app_file: app.py
python_version: "3.11"
pinned: false
```
