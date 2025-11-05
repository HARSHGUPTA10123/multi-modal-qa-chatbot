import os
import utils
import requests
import traceback
import validators
import streamlit as st
from streaming import StreamHandler

from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_core.documents.base import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import DocArrayInMemorySearch




utils.set_default_openai()

# --------------------------- #
# 🌑 Streamlit Page Settings
# --------------------------- #
st.set_page_config(page_title="Chat with Website", page_icon="🔗", layout="wide")

st.markdown("""
    <style>
        /* Background and layout */
        .stApp {
            background: radial-gradient(circle at top left, #05070d, #0d1117 80%);
            color: #e5e7eb;
            padding-top: 1rem;
        }

        /* Centered header fix */
        .block-container {
            padding-top: 3rem !important;
            max-width: 900px;
            margin: auto;
        }

        /* Gradient animated heading */
        .main-title {
            font-size: 2.8rem;
            font-weight: 800;
            text-align: center;
            background: linear-gradient(90deg, #60a5fa, #818cf8, #a78bfa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: glow 3s ease-in-out infinite alternate;
            margin-bottom: 0.2em;
        }

        @keyframes glow {
            from { text-shadow: 0 0 10px #3b82f6; }
            to { text-shadow: 0 0 25px #a78bfa; }
        }

        /* Subtitle styling */
        .subtitle {
            text-align: center;
            font-size: 1.1rem;
            color: #9ca3af;
            margin-bottom: 2.5em;
        }

        /* Sidebar styling */
        section[data-testid="stSidebar"] {
            background-color: rgba(17, 24, 39, 0.9);
            border-right: 1px solid #1e293b;
        }

        /* Sidebar headers */
        .sidebar .sidebar-content, .stSidebar h2, .stSidebar h3, .stSidebar h4 {
            color: #f9fafb !important;
        }

        /* Input and button styling */
        .stTextInput>div>div>input {
            background-color: #1f2937 !important;
            color: #f3f4f6 !important;
            border: 1px solid #374151 !important;
            border-radius: 0.5rem !important;
        }

        .stButton>button {
            background: linear-gradient(135deg, #2563eb, #4f46e5);
            color: white;
            border: none;
            border-radius: 0.6rem;
            font-weight: 600;
            transition: 0.3s ease;
            box-shadow: 0 0 8px rgba(59, 130, 246, 0.4);
        }

        .stButton>button:hover {
            background: linear-gradient(135deg, #3b82f6, #6366f1);
            transform: translateY(-2px);
            box-shadow: 0 0 12px rgba(99, 102, 241, 0.6);
        }

        /* Chat message bubbles */
        div[data-testid="stChatMessage"] {
            border-radius: 1rem;
            padding: 0.7rem 1rem;
            margin-bottom: 0.6rem;
        }

        [data-testid="stChatMessage"][data-testid="user"] {
            background: linear-gradient(135deg, #1e3a8a, #3b82f6);
            color: #f9fafb;
        }

        [data-testid="stChatMessage"][data-testid="assistant"] {
            background: linear-gradient(135deg, #111827, #1f2937);
            color: #d1d5db;
        }

        /* Chat input box */
        [data-testid="stChatInput"] textarea {
            background-color: #1e293b !important;
            color: #f3f4f6 !important;
            border-radius: 0.8rem !important;
            border: 1px solid #374151 !important;
        }

        /* Reference popovers */
        .popover-content {
            background-color: #111827;
            color: #e5e7eb;
            border-radius: 0.8rem;
            padding: 1rem;
        }
    </style>
""", unsafe_allow_html=True)


# --------------------------- #
# 🌟 Page Header
# --------------------------- #
st.markdown("<h1 class='main-title'>🔗 Chat with Website</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Ask anything about the contents of any website — all processed with real-time AI context understanding.</p>", unsafe_allow_html=True)


# --------------------------- #
# 💬 Chatbot Class
# --------------------------- #
class ChatbotWeb:

    def __init__(self):
        utils.sync_st_session()
        self.llm = utils.configure_llm()
        self.embedding_model = utils.configure_embedding_model()

    def scrape_website(self, url):
        """Fetch website content via jina.ai proxy."""
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            final_url = "https://r.jina.ai/" + url
            res = requests.get(final_url, headers=headers, timeout=25)
            res.raise_for_status()
            return res.text
        except Exception as e:
            st.sidebar.error(f"⚠️ Failed to fetch: {url}\n\n{e}")
            traceback.print_exc()
            return ""

    @st.cache_resource(show_spinner='🔍 Analyzing website...', ttl=3600)
    def setup_vectordb(_self, websites):
        """Scrape and store website text embeddings."""
        docs = []
        for url in websites:
            docs.append(Document(page_content=_self.scrape_website(url), metadata={"source": url}))
        
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = splitter.split_documents(docs)
        vectordb = DocArrayInMemorySearch.from_documents(splits, _self.embedding_model)
        return vectordb

    def setup_qa_chain(self, vectordb):
        retriever = vectordb.as_retriever(search_type='mmr', search_kwargs={'k': 2, 'fetch_k': 4})
        memory = ConversationBufferMemory(memory_key='chat_history', output_key='answer', return_messages=True)

        return ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=retriever,
            memory=memory,
            return_source_documents=True,
            verbose=False
        )

    @utils.enable_chat_history
    def main(self):
        # --------------------------- #
        # 🧭 Sidebar Inputs
        # --------------------------- #
        st.sidebar.markdown("## 🌍 Website Settings")
        if "websites" not in st.session_state:
            st.session_state["websites"] = []

        web_url = st.sidebar.text_input("Enter Website URL", placeholder="https://example.com")

        col1, col2 = st.sidebar.columns([1, 1])
        with col1:
            if st.button("➕ Add Website"):
                if not (web_url.startswith("http") and validators.url(web_url)):
                    st.sidebar.error("Invalid URL! Please check your input.", icon="⚠️")
                else:
                    st.session_state["websites"].append(web_url)
        with col2:
            if st.button("🧹 Clear All"):
                st.session_state["websites"] = []

        websites = list(set(st.session_state["websites"]))
        if not websites:
            st.warning("Please add a website to start chatting.")
            st.stop()
        else:
            st.sidebar.success("✅ Websites Added:")
            for w in websites:
                st.sidebar.write(f"- {w}")

        vectordb = self.setup_vectordb(websites)
        qa_chain = self.setup_qa_chain(vectordb)

        # --------------------------- #
        # 💬 Chat Interface
        # --------------------------- #
        user_query = st.chat_input(placeholder="Ask me anything about the websites...")
        if user_query:
            utils.display_msg(user_query, "user")
            with st.chat_message("assistant"):
                st_cb = StreamHandler(st.empty())
                result = qa_chain.invoke({"question": user_query}, {"callbacks": [st_cb]})
                response = result["answer"]
                st.session_state.messages.append({"role": "assistant", "content": response})
                utils.print_qa(ChatbotWeb, user_query, response)

                # References
                if result.get("source_documents"):
                    st.markdown("#### 📚 References")
                    for idx, doc in enumerate(result["source_documents"], 1):
                        src_url = doc.metadata.get("source", "unknown")
                        ref_title = f":blue[Reference {idx}: *{src_url}*]"
                        with st.popover(ref_title):
                            st.caption(doc.page_content[:800] + "...")


# --------------------------- #
# 🚀 Run App
# --------------------------- #
if __name__ == "__main__":
    obj = ChatbotWeb()
    obj.main()

