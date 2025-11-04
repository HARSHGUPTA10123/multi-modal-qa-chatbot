# import streamlit as st

# st.set_page_config(
#     page_title="LangChain Chatbots 💬",
#     page_icon="💬",
#     layout="wide"
# )

# # ---------- Custom Styling ----------
# st.markdown("""
#     <style>
#         /* 🌈 Background gradient */
#         .stApp {
#             background-color: #000000;  /* Solid black background */
#             color: #FFFFFF;
#         }


#         /* 🔷 Remove harsh black from Streamlit top header */
#         header[data-testid="stHeader"] {
#             background: rgba(255, 255, 255, 0.05);
#             backdrop-filter: blur(10px);
#             border-bottom: 1px solid rgba(255,255,255,0.1);
#         }

#         /* 🔹 Sidebar style */
#         section[data-testid="stSidebar"] {
#             background: linear-gradient(180deg, #333333, #1e1e2f);
#             color: #e6e6fa;
#         }

#         /* 🎯 Main title */
#         .main-title {
#             font-size: 3rem;
#             font-weight: 800;
#             text-align: center;
#             color: #7df9ff;
#             margin-bottom: 0.5rem;
#             text-shadow: 0px 0px 10px rgba(125, 249, 255, 0.5);
#         }

#         /* ✨ Subtitle */
#         .sub-title {
#             text-align: center;
#             color: #c0d9ff;
#             font-size: 1.2rem;
#             margin-bottom: 2rem;
#         }

#         /* 📦 Feature card styling */
#         .feature-card {
#             background: rgba(255, 255, 255, 0.07);
#             border: 1px solid rgba(255, 255, 255, 0.15);
#             border-radius: 18px;
#             padding: 1.5rem;
#             text-align: left;
#             box-shadow: 0 8px 25px rgba(0,0,0,0.3);
#             transition: transform 0.25s ease, box-shadow 0.25s ease;
#         }
#         .feature-card:hover {
#             transform: translateY(-5px);
#             box-shadow: 0 10px 30px rgba(0,0,0,0.4);
#             border-color: rgba(125, 249, 255, 0.3);
#         }

#         .feature-card h4 {
#             color: #b0e0e6;
#             font-size: 1.3rem;
#         }

#         .feature-card p {
#             color: #e0e0e0;
#             font-size: 1.05rem;
#         }

#         /* 💖 Footer */
#         .footer {
#             text-align: center;
#             margin-top: 2.5rem;
#             font-size: 0.95rem;
#             color: #b0e0e6;
#         }

#         .footer b {
#             color: #00e5ff;
#         }
#     </style>
# """, unsafe_allow_html=True)

# # ---------- Header Section ----------
# st.markdown('<h1 class="main-title">💬 LangChain Chatbot Hub</h1>', unsafe_allow_html=True)
# st.markdown('<p class="sub-title">A unified platform showcasing intelligent chatbot implementations using LangChain and LLMs.</p>', unsafe_allow_html=True)

# # ---------- Feature Cards ----------
# col1, col2, col3 = st.columns(3)

# with col1:
#     st.markdown("""
#     <div class="feature-card">
#         <h4>🤖 Basic Chatbot</h4>
#         <p>Engage in interactive conversations with an LLM-powered chatbot.</p>
#     </div>
#     """, unsafe_allow_html=True)

#     st.markdown("""
#     <div class="feature-card">
#         <h4>🧠 Context-Aware Chatbot</h4>
#         <p>Remembers previous interactions and responds with context-aware intelligence.</p>
#     </div>
#     """, unsafe_allow_html=True)

# with col2:
#     st.markdown("""
#     <div class="feature-card">
#         <h4>🌐 Internet-Enabled Chatbot</h4>
#         <p>Accesses live web data to answer current and real-time event-based queries.</p>
#     </div>
#     """, unsafe_allow_html=True)

#     st.markdown("""
#     <div class="feature-card">
#         <h4>📄 Chat with Your Documents</h4>
#         <p>Query your own PDFs, notes, or Word files to extract precise insights.</p>
#     </div>
#     """, unsafe_allow_html=True)

# with col3:
#     st.markdown("""
#     <div class="feature-card">
#         <h4>🗄️ Chat with SQL Database</h4>
#         <p>Talk directly to your databases using natural language — no SQL needed!</p>
#     </div>
#     """, unsafe_allow_html=True)

#     st.markdown("""
#     <div class="feature-card">
#         <h4>🌍 Chat with Websites</h4>
#         <p>Extract, summarize, or analyze data directly from websites.</p>
#     </div>
#     """, unsafe_allow_html=True)

# # ---------- Footer ----------
# st.markdown("""
#     <div class="footer">
#         Built with ❤️ using <b>Streamlit</b> & <b>LangChain</b> | Designed by <b>Harsh Gupta</b> 🚀
#     </div>
# """, unsafe_allow_html=True)

import streamlit as st

st.set_page_config(
    page_title="LangChain Chatbots 💬",
    page_icon="💬",
    layout="wide"
)

# ---------- Custom Styling ----------
st.markdown("""
    <style>
        /* 🌈 Background gradient */
        .stApp {
            background-color: #000000;  /* Solid black background */
            color: #FFFFFF;
        }

        /* 🔷 Remove harsh black from Streamlit top header */
        header[data-testid="stHeader"] {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }

        /* 🔹 Sidebar style */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #333333, #1e1e2f);
            color: #e6e6fa;
        }

        /* 🎯 Main title */
        .main-title {
            font-size: 3rem;
            font-weight: 800;
            text-align: center;
            color: #7df9ff;
            margin-bottom: 0.5rem;
            text-shadow: 0px 0px 10px rgba(125, 249, 255, 0.5);
        }

        /* ✨ Subtitle */
        .sub-title {
            text-align: center;
            color: #c0d9ff;
            font-size: 1.2rem;
            margin-bottom: 2rem;
        }

        /* 📦 Feature card styling */
        .feature-card {
            background: rgba(255, 255, 255, 0.07);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 18px;
            padding: 1.5rem;
            text-align: left;
            box-shadow: 0 8px 25px rgba(0,0,0,0.3);
            transition: transform 0.25s ease, box-shadow 0.25s ease;
        }
        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.4);
            border-color: rgba(125, 249, 255, 0.3);
        }

        .feature-card h4 {
            color: #b0e0e6;
            font-size: 1.3rem;
        }

        .feature-card p {
            color: #e0e0e0;
            font-size: 1.05rem;
        }

        /* 💡 Info box styling */
        .info-box {
            background: linear-gradient(135deg, rgba(125, 249, 255, 0.1), rgba(192, 217, 255, 0.1));
            border: 1px solid rgba(125, 249, 255, 0.3);
            border-radius: 15px;
            padding: 1.5rem;
            margin: 2rem auto;
            text-align: center;
            box-shadow: 0 8px 25px rgba(0,0,0,0.3);
            max-width: 900px;
        }

        .info-box h3 {
            color: #7df9ff;
            font-size: 1.5rem;
            margin-bottom: 1rem;
        }

        .info-box p {
            color: #e0e0e0;
            font-size: 1.05rem;
            line-height: 1.6;
            margin-bottom: 1rem;
        }

        .info-box a {
            color: #00e5ff;
            text-decoration: none;
            font-weight: bold;
        }

        .info-box a:hover {
            text-decoration: underline;
        }

        /* 🚀 Button styling */
        .action-button {
            background: linear-gradient(135deg, #7df9ff, #00e5ff);
            color: #000000 !important;
            border: none;
            border-radius: 10px;
            padding: 0.8rem 1.5rem;
            font-weight: bold;
            text-decoration: none;
            display: inline-block;
            margin: 0.5rem;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            cursor: pointer;
        }

        .action-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(125, 249, 255, 0.4);
            color: #000000 !important;
            text-decoration: none;
        }

        /* 💖 Footer */
        .footer {
            text-align: center;
            margin-top: 2.5rem;
            font-size: 0.95rem;
            color: #b0e0e6;
        }

        .footer b {
            color: #00e5ff;
        }
    </style>
""", unsafe_allow_html=True)

# ---------- Header Section ----------
st.markdown('<h1 class="main-title">💬 LangChain Chatbot Hub</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">A unified platform showcasing intelligent chatbot implementations using LangChain and LLMs.</p>', unsafe_allow_html=True)

# ---------- Usage Instructions ----------
st.markdown("""
<div class="info-box">
    <h3>🚀 Getting Started</h3>
    <p><strong>🌐 Cloud Usage (Recommended):</strong></p>
    <p>Use all chatbots with OpenAI API for best performance:</p>
    <p>1. Get your OpenAI API Key </p>
    <p>2. Add your API key in the sidebar of any chatbot page</p>
    <p>3. Select "OpenAI" as the provider and start chatting!</p>
</div>
""", unsafe_allow_html=True)

# ✅ Properly render buttons separately so they are not escaped as markdown text
st.markdown(
    """
    <div style="margin: 1.5rem 0; text-align: center;">
        <a href="https://platform.openai.com/api-keys" target="_blank" class="action-button">
            🔑 Get OpenAI API Key
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("""
<div class="info-box">
    <p><strong>💻 Local Usage (Advanced):</strong></p>
    <p>Run locally with TinyLlama for free, private AI:</p>
    <p>1. Clone the repository</p>
    <p>2. Follow setup instructions in README</p>
    <p>3. Run locally with Ollama and TinyLlama</p>
</div>
""", unsafe_allow_html=True)

st.markdown(
    """
    <div style="margin: 1.5rem 0; text-align: center;">
        <a href="https://github.com/HARSHGUPTA10123/multi-modal-qa-chatbot" target="_blank" class="action-button">
            📥 Clone Repository
        </a>
    </div>
    """,
    unsafe_allow_html=True
)


# ---------- Feature Cards ----------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h4>🤖 Basic Chatbot</h4>
        <p>Engage in interactive conversations with an LLM-powered chatbot.</p>
        <small><em>🔑 OpenAI API | 🦙 TinyLlama Local</em></small>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-card">
        <h4>🧠 Context-Aware Chatbot</h4>
        <p>Remembers previous interactions and responds with context-aware intelligence.</p>
        <small><em>🔑 OpenAI API | 🦙 TinyLlama Local</em></small>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h4>🌐 Internet-Enabled Chatbot</h4>
        <p>Accesses live web data to answer current and real-time event-based queries.</p>
        <small><em>🔑 OpenAI API + 🌐 Web Search</em></small>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-card">
        <h4>📄 Chat with Your Documents</h4>
        <p>Query your own PDFs, notes, or Word files to extract precise insights.</p>
        <small><em>🔑 OpenAI API | 🦙 TinyLlama Local</em></small>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <h4>🗄️ Chat with SQL Database</h4>
        <p>Talk directly to your databases using natural language — no SQL needed!</p>
        <small><em>🔑 OpenAI API | 🦙 TinyLlama Local</em></small>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-card">
        <h4>🌍 Chat with Websites</h4>
        <p>Extract, summarize, or analyze data directly from websites.</p>
        <small><em>🔑 OpenAI API | 🦙 TinyLlama Local</em></small>
    </div>
    """, unsafe_allow_html=True)

# ---------- Tech Stack Section ----------
st.markdown("---")
st.markdown("""
<div style="text-align: center; margin: 2rem 0;">
    <h3 style="color: #7df9ff; margin-bottom: 1rem;">🛠️ Powered By</h3>
    <div style="display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap;">
        <div style="text-align: center;">
            <div style="font-size: 2rem;">🦜</div>
            <strong>LangChain</strong>
        </div>
        <div style="text-align: center;">
            <div style="font-size: 2rem;">⚡</div>
            <strong>Streamlit</strong>
        </div>
        <div style="text-align: center;">
            <div style="font-size: 2rem;">🔑</div>
            <strong>OpenAI</strong>
        </div>
        <div style="text-align: center;">
            <div style="font-size: 2rem;">🦙</div>
            <strong>TinyLlama</strong>
        </div>
        <div style="text-align: center;">
            <div style="font-size: 2rem;">🌐</div>
            <strong>Tavily</strong>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------- Footer ----------
st.markdown("""
    <div class="footer">
        Built with ❤️ using <b>Streamlit</b> & <b>LangChain</b> | 
        <b>OpenAI API</b> for cloud usage | 
        <b>TinyLlama</b> for local usage | 
        Designed by <b>Harsh Gupta</b> 🚀
    </div>
""", unsafe_allow_html=True)

# ---------- Sidebar Info ----------
with st.sidebar:
    st.title("ℹ️ About")
    st.markdown("""
    **LangChain Chatbot Hub** showcases various AI chatbot implementations using cutting-edge technologies.
    
    ### 🎯 Usage Options
    
    **🌐 Cloud Usage (Easy):**
    - Use OpenAI API for best performance
    - Add API key in any chatbot's sidebar
    - No setup required
    
    **💻 Local Usage (Advanced):**
    - Clone repository for local setup
    - Use TinyLlama for free, private AI
    - 📖 **[Follow README instructions →](https://github.com/HARSHGUPTA10123/multi-modal-qa-chatbot/blob/main/README.md)**
    
    ### 📚 Pages
    1. **Basic Chatbot** - Simple AI conversations
    2. **Context-Aware** - Memory-enabled chats  
    3. **Web Search** - Real-time information
    4. **Document Q&A** - Chat with PDFs
    5. **SQL Database** - Natural language queries
    6. **Website Chat** - Web content analysis
    """)
    
    st.markdown("---")
    st.subheader("🔗 Quick Links")
    
    # Use markdown with clear link styling
    st.markdown("""
    **📖 Setup Instructions:**
    - [View README Instructions](https://github.com/HARSHGUPTA10123/multi-modal-qa-chatbot/blob/main/README.md)
    
    **🔑 API Keys:**
    - [Get OpenAI API Key](https://platform.openai.com/api-keys)
    
    **📥 Source Code:**
    - [Clone Repository](https://github.com/HARSHGUPTA10123/multi-modal-qa-chatbot)
    
    **🦙 Local AI:**
    - [Ollama Website](https://ollama.ai)
    """)
