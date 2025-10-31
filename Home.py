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

# ---------- Feature Cards ----------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h4>🤖 Basic Chatbot</h4>
        <p>Engage in interactive conversations with an LLM-powered chatbot.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-card">
        <h4>🧠 Context-Aware Chatbot</h4>
        <p>Remembers previous interactions and responds with context-aware intelligence.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h4>🌐 Internet-Enabled Chatbot</h4>
        <p>Accesses live web data to answer current and real-time event-based queries.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-card">
        <h4>📄 Chat with Your Documents</h4>
        <p>Query your own PDFs, notes, or Word files to extract precise insights.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <h4>🗄️ Chat with SQL Database</h4>
        <p>Talk directly to your databases using natural language — no SQL needed!</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-card">
        <h4>🌍 Chat with Websites</h4>
        <p>Extract, summarize, or analyze data directly from websites.</p>
    </div>
    """, unsafe_allow_html=True)

# ---------- Footer ----------
st.markdown("""
    <div class="footer">
        Built with ❤️ using <b>Streamlit</b> & <b>LangChain</b> | Designed by <b>Harsh Gupta</b> 🚀
    </div>
""", unsafe_allow_html=True)
