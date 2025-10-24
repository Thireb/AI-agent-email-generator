# 🤖 Job Application Email Agent with CrewAI

An AI-powered agent system that helps write personalized job application emails using local Ollama models and CrewAI.

## 🚀 Features

- **Multi-Agent System**: Uses CrewAI to orchestrate specialized agents for research, writing, and review
- **Local AI Models**: Powered by Ollama with local model support (no API costs)
- **Smart Job Analysis**: Automatically extracts key information from job descriptions
- **Personalized Templates**: Generates customized emails based on job requirements and your background
- **Multiple Role Types**: Supports various job types (Software Engineer, Data Scientist, Product Manager, etc.)
- **Quality Review**: Built-in email review and improvement system

## 📁 Project Structure

```
google_aut_submit/
├── requirements.txt              # Python dependencies
├── jd_agent.py                  # Main CrewAI orchestration script
├── test_ollama_connection.py    # Test script for setup verification
├── agents/                      # CrewAI agent definitions
│   ├── __init__.py
│   ├── researcher.py           # Job research specialist
│   ├── writer.py               # Email writing expert
│   └── reviewer.py             # Email quality reviewer
├── tools/                       # Custom tools for agents
│   ├── __init__.py
│   ├── job_analyzer.py         # Job description analysis
│   └── email_templates.py      # Email template management
├── config/                      # Configuration files
│   ├── __init__.py
│   ├── ollama_config.py        # Ollama model configuration
│   └── personal_info.py        # Your personal information
└── data/                        # Sample data and templates
    ├── job_descriptions/        # Sample job descriptions
    └── email_templates/         # Email template examples
```

## 🛠️ Setup Instructions

### 1. Prerequisites

- Python 3.8+
- Ollama installed and running
- `deepseek-r1:1.5b` model available (or modify config for your preferred model)

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Verify Ollama Setup

Make sure Ollama is running and your model is available:

```bash
# Start Ollama (if not already running)
ollama serve

# Check available models
ollama list

# Ensure deepseek-r1 is available
ollama pull deepseek-r1:1.5b
```

### 4. Customize Personal Information

Edit `config/personal_info.py` with your details:

```python
PERSONAL_INFO = {
    "your_name": "Your Actual Name",
    "phone": "+1 (555) 123-4567",
    "email": "your.email@example.com",
    "linkedin": "linkedin.com/in/yourprofile",
    "github": "github.com/yourusername",
    "portfolio": "yourportfolio.com",
    "key_skills": ["Python", "JavaScript", "AWS", "..."],
    "relevant_experience": "building scalable web applications",
    # ... customize other fields
}
```

### 5. Test the Setup

Run the test script to verify everything is working:

```bash
python test_ollama_connection.py
```

### 6. CV Parser

Put CV in CV folder. Accepts PDF and Docs files.

## 🎯 Usage

### Basic Usage

1. **Run the main agent**:
   ```bash
   python jd_agent.py
   ```

2. **The system will**:
   - Analyze the hardcoded job description
   - Research company and role requirements
   - Generate a personalized email
   - Review and improve the email
   - Output the final result

### Custom Job Descriptions

To use your own job descriptions, modify the `job_description` variable in `jd_agent.py` or create a new script that reads from files.

### Advanced Customization

- **Add new email templates**: Extend `tools/email_templates.py`
- **Modify job analysis**: Customize `tools/job_analyzer.py`
- **Adjust agent behavior**: Modify agent files in the `agents/` directory
- **Change AI model**: Update `config/ollama_config.py`

## 🔧 Configuration

### Ollama Models

The system is configured to use `deepseek-r1:1.5b` by default. You can change this in `config/ollama_config.py`:

```python
def get_ollama_llm(model_name: str = "your-preferred-model"):
    # ... configuration
```

### Agent Behavior

Each agent has configurable:
- **Role**: What the agent does
- **Goal**: What the agent aims to achieve
- **Backstory**: Context and expertise
- **Tools**: Available tools for the agent

### Email Templates

Templates are available for:
- Software Engineer
- Data Scientist
- Product Manager
- Designer
- Marketing
- Sales
- General (fallback)

## 🧪 Testing

### Run All Tests

```bash
python test_ollama_connection.py
```

### Individual Component Tests

```bash
# Test Ollama connection
python -c "from config.ollama_config import test_ollama_connection; test_ollama_connection()"

# Test tools
python -c "from tools.job_analyzer import JobDescriptionAnalyzer; JobDescriptionAnalyzer()._run('test')"

# Test agents
python agents/researcher.py
```

## 🚨 Troubleshooting

### Common Issues

1. **Ollama Connection Failed**
   - Ensure Ollama is running: `ollama serve`
   - Check if the model is available: `ollama list`
   - Verify the model name in `config/ollama_config.py`

2. **Import Errors**
   - Install dependencies: `pip install -r requirements.txt`
   - Check Python path and working directory

3. **Model Not Responding**
   - The `deepseek-r1:1.5b` model is relatively small (1.5B parameters)
   - Consider using a larger model for better quality
   - Check Ollama logs for errors

4. **Memory Issues**
   - Smaller models like `all-minilm:latest` use less memory
   - Close other applications to free up RAM

### Performance Tips

- **Faster responses**: Use smaller models like `all-minilm:latest`
- **Better quality**: Use larger models like `deepseek-r1:1.5b` or larger
- **Balanced approach**: Use smaller models for testing, larger for production

## 🔮 Future Enhancements

- **Web Interface**: Add a simple web UI for easier interaction
- **Multiple Job Types**: Support for cover letters, follow-up emails, etc.
- **Email Tracking**: Track application status and follow-up timing
- **A/B Testing**: Test different email versions for effectiveness
- **Integration**: Connect with job boards and application systems
- **Learning**: Improve templates based on success rates

## 📝 License

This project is open source. Feel free to modify and distribute as needed.

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Better job description parsing
- More email templates
- Enhanced AI agent capabilities
- Performance optimizations
- Additional tools and integrations

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify your Ollama setup
3. Run the test script to identify problems
4. Check the CrewAI and Ollama documentation

---

**Happy job hunting! 🎯**
