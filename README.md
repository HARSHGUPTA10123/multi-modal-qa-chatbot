Here's your updated README.md with all the correct information:

```markdown
# 🤖 MultiModal Q&A Chatbot with LangChain & Tavily

## 📋 Overview
A comprehensive multimodal question-answering chatbot with 6 different functionalities powered by LangChain, Streamlit, OpenAI, and Tavily AI search.

## ✨ Features
- **6 Different Chat Modes**:
  1. 🤖 Basic Chatbot - Standard AI conversations
  2. 🧠 Context-Aware Chatbot - Memory-enabled chats
  3. 🌐 Internet-Enabled Chatbot - Real-time web search via Tavily
  4. 📄 Chat with Documents - PDF and document processing
  5. 🗄️ Chat with SQL Database - Database querying (Chinook.db)
  6. 🌍 Chat with Websites - Website content analysis

- **Streamlit Multi-page App** with beautiful UI
- **Secure API Management** via Streamlit secrets
- **SQL Database Integration** with Chinook sample database

## 🛠️ Technologies Used
- **LangChain** - AI framework and orchestration
- **Streamlit** - Web application framework
- **OpenAI** - GPT models for natural language processing
- **Tavily AI** - Intelligent web search and research
- **SQLAlchemy** - Database operations
- **PyPDF** - Document processing
- **FastEmbed** - Efficient text embeddings

## 📦 Installation & Setup

```bash
# Clone repository
git clone https://github.com/HARSHGUPTA10123/Multi_Modal_Q&A_Chatbot.git

# Navigate to project directory
cd Multi_Modal_Q&A_Chatbot

# Create virtual environment (recommended)
python -m venv multimodal_chatbot_environment

# Activate virtual environment
# Windows:
multimodal_chatbot_environment\Scripts\activate
# macOS/Linux:
source multimodal_chatbot_environment/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run Home.py
```

## 🔑 Environment Setup

Create `.streamlit/secrets.toml` file:
```toml
OPENAI_API_KEY = "your_openai_api_key_here"
TAVILY_API_KEY = "your_tavily_api_key_here"
```

## 📁 Project Structure

```
Multi_Modal_Q&A_Chatbot/
│
├── 📄 Home.py                    # Main homepage application
├── 📄 utils.py                   # Utility functions and helpers
├── 📄 streaming.py               # Streaming response handlers
├── 📄 download_chinook.py        # Database download utility
├── 📄 Chinook.db                 # Sample SQL database
├── 📄 requirements.txt           # Project dependencies
│
├── 📁 pages/                     # Streamlit multi-page modules
│   ├── 1. Basic Chatbot.py
│   ├── 2. Context-Aware Chatbot.py
│   ├── 3. Internet-Enabled Chatbot.py
│   ├── 4. Chat with Your Documents.py
│   ├── 5. Chat with SQL Database.py
│   └── 6. Chat with Websites.py
│
├── 📁 .streamlit/                # Streamlit configuration
│   └── secrets.toml              # API keys (excluded from git)
│
├── 📁 assets/                    # Static assets
├── 📁 tmp/                       # Temporary files
└── 📄 README.md                  # Project documentation
```

## 🚀 Usage

1. **Setup API Keys**: Add your keys to `.streamlit/secrets.toml`
2. **Run Application**: `streamlit run Home.py`
3. **Choose Chat Mode**: Navigate through the sidebar to access different functionalities

### Available Chat Modes:
- **Basic Chatbot**: Standard AI conversations using OpenAI
- **Context-Aware**: Chats with memory and context preservation
- **Internet-Enabled**: Real-time web search using Tavily AI
- **Document Chat**: Upload and query PDF documents
- **SQL Chat**: Natural language queries against Chinook database
- **Website Chat**: Analyze and chat about website content

## 🔧 Configuration

- **OpenAI API**: Required for all AI functionalities
- **Tavily API**: Required for internet search functionality
- **Streamlit Secrets**: Secure API key management

## 👨‍💻 Developer

**Harsh Gupta**  
🎓 Computer Science Engineering Student  
📧 hg932003@gmail.com  
🔗 [GitHub Profile](https://github.com/HARSHGUPTA10123)

---

*Built with ❤️ using LangChain, Streamlit, OpenAI, and Tavily for intelligent multi-modal conversations*


