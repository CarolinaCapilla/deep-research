# Deep Research AI Agent

An intelligent research assistant powered by AI agents that performs comprehensive web research, generates reports, and sends email summaries. Built with Gradio for an intuitive web interface.

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
python agents/deep_research.py
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
├── agents/
│   ├── __init__.py
│   ├── deep_research.py      # Main Gradio app
│   ├── research_manager.py   # Orchestrates research pipeline
│   ├── planner_agent.py      # Plans research queries
│   ├── search_agent.py       # Performs web searches
│   ├── writer_agent.py       # Generates reports
│   └── email_agent.py        # Sends email summaries
├── pyproject.toml           # Project dependencies
├── .gitignore              # Git ignore rules
└── README.md               # This file
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

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Troubleshooting

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

- [ ] Add support for multiple AI providers (Anthropic, Google)
- [ ] Implement research result caching
- [ ] Add export options (PDF, DOCX)
- [ ] Create a REST API endpoint
- [ ] Add user authentication
- [ ] Implement research history and favorites

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/CarolinaCapilla/deep-research/issues) page
2. Create a new issue with detailed information
3. Include error messages and steps to reproduce

---

**Made with ❤️ using AI agents and Gradio**
