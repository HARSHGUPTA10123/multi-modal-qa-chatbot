Here's the complete README.md file ready to copy and paste:

```markdown
# 🤖 Multi-Modal Q&A Chatbot

A powerful, multi-functional chatbot built with Streamlit and LangChain that supports multiple AI providers and features.

## 🚀 Features

- **🤖 Basic Chatbot** - Simple conversational AI
- **🧠 Context-Aware Chatbot** - Remembers conversation history
- **🌐 Internet-Enabled Chatbot** - Real-time web search capabilities
- **📄 Chat with Documents** - Upload and query PDF documents
- **🗃️ Chat with SQL Databases** - Natural language database queries
- **🔗 Chat with Websites** - Extract and chat with web content

## 🛠️ Installation

### Prerequisites

1. **Python 3.8+** installed
2. **Ollama** installed for local models

### Install Ollama (Required for Local Models)

**Windows:**
```bash
# Download from https://ollama.ai/ and install
# Then run:
ollama pull tinyllama
```

**Mac/Linux:**
```bash
# Install via curl
curl -fsSL https://ollama.ai/install.sh | sh
# Pull a model
ollama pull tinyllama
```

### Clone and Setup

```bash
# Clone the repository
git clone https://github.com/HARSHGUPTA10123/multi-modal-qa-chatbot.git
cd multi-modal-qa-chatbot

# Create virtual environment
python -m venv multimodal_chatbot_environment

# Activate environment
# Windows:
multimodal_chatbot_environment\Scripts\activate
# Mac/Linux:
source multimodal_chatbot_environment/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## 🔑 Configuration

### 1. Create Secrets File

Create `.streamlit/secrets.toml` file:

```toml
# Optional: For default OpenAI API key
OPENAI_API_KEY = ""

# Optional: For custom Ollama endpoint
OLLAMA_ENDPOINT = "http://localhost:11434"

# Required for Internet-Enabled Chatbot
TAVILY_API_KEY = "your_tavily_api_key_here"
```

### 2. Get API Keys

- **OpenAI API Key**: Get from [OpenAI Platform](https://platform.openai.com/account/api-keys)
- **Tavily API Key**: Get from [Tavily AI](https://tavily.com/) for internet search features

## 🎯 Usage

```bash
# Run the main application
streamlit run Home.py
```

### Available Chatbots:

1. **💬 Basic Chatbot** - Simple AI conversations
2. **⭐ Context-Aware Chatbot** - Remembers your chat history
3. **🌐 Internet-Enabled Chatbot** - Real-time web searches (requires Tavily API key)
4. **📄 Chat with Your Documents** - Upload and query PDF files
5. **🗃️ Chat with SQL Databases** - Natural language SQL queries
6. **🔗 Chat with Websites** - Extract and chat with web content

## 🤖 AI Providers

### OpenAI (Cloud - Recommended)
- Requires API key
- More powerful models (GPT-3.5, GPT-4)
- Better accuracy and context handling

### Ollama (Local)
- Free and offline
- Uses local models (tinyllama recommended)
- Good for testing and privacy

## 🎨 Customization

### Temperature Control
Adjust creativity level:
- **0.0**: Precise, deterministic responses
- **0.7**: Balanced, natural conversations  
- **1.0**: Creative, diverse responses

### Model Selection
- Choose between different OpenAI models
- Select from available Ollama models
- Switch providers in real-time

## 📁 Project Structure

```
multi-modal-qa-chatbot/
├── Home.py                 # Main application
├── utils.py               # Utility functions
├── requirements.txt       # Dependencies
├── pages/                # Chatbot modules
│   ├── 1_💬_Basic_Chatbot.py
│   ├── 2_🧠_Context-Aware_Chatbot.py
│   ├── 3_🌐_Internet-Enabled_Chatbot.py
│   ├── 4_📄_Chat_with_Your_Documents.py
│   ├── 5_🗃️_Chat_with_SQL_Databases.py
│   └── 6_🔗_Chat_with_Websites.py
├── .streamlit/           # Configuration
│   └── secrets.toml     # API keys (create this)
└── assets/              # Static files
```

## 🐛 Troubleshooting

### Common Issues

1. **Ollama Connection Error**
   ```bash
   # Make sure Ollama is running
   ollama serve
   ```

2. **API Key Errors**
   - Check if API keys are valid
   - Ensure sufficient quota for OpenAI
   - Verify Tavily API key for internet features

3. **Module Not Found**
   ```bash
   # Reinstall requirements
   pip install -r requirements.txt
   ```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

**Harsh Gupta**
- GitHub: [@HARSHGUPTA10123](https://github.com/HARSHGUPTA10123)

---

⭐ Star this repo if you found it helpful!
```

## 📋 **Also create this .gitignore file:**

Create `.gitignore` file:

```gitignore
# Streamlit
.streamlit/secrets.toml

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Database
*.db
*.sqlite3

# Ollama models
.ollama/
```

## 📝 **And this secrets template file:**

Create `.streamlit/secrets_template.toml`:

```toml
# COPY THIS FILE TO secrets.toml AND ADD YOUR API KEYS

# OpenAI API Key (Optional)
# Get from: https://platform.openai.com/account/api-keys
OPENAI_API_KEY = ""

# Ollama Endpoint (Optional)
# Default is http://localhost:11434
OLLAMA_ENDPOINT = "http://localhost:11434"

# Tavily API Key (Required for Internet Chatbot)
# Get from: https://tavily.com/
TAVILY_API_KEY = "your_tavily_api_key_here"
```

