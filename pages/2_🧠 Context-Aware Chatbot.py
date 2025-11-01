import utils
import streamlit as st
from streaming import StreamHandler

from langchain.chains.conversation.base import ConversationChain
from langchain.memory import ConversationBufferMemory


# -------------------- Cache Management --------------------
# Clear any residual OpenAI sessions when starting
if "openai_api_key_input" in st.session_state:
    del st.session_state["openai_api_key_input"]

# Set default to Ollama if not set
if "llm_provider_selection" not in st.session_state:
    st.session_state.llm_provider_selection = "Ollama (Local)"

# -------------------- Page Config --------------------
st.set_page_config(page_title="Context Aware Chatbot", page_icon="⭐", layout="wide")

# -------------------- Custom Styling --------------------
st.markdown("""
    <style>
    /* Header styling */
    .title {
        font-size: 2.2rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.2em;
        color: #ffffff;
        background: linear-gradient(90deg, #FFB300, #FF6F00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: fadeInDown 1s ease;
    }

    /* Subtitle */
    .subtitle {
        text-align: center;
        font-size: 1.1rem;
        color: #d0d0d0;
        margin-bottom: 2rem;
        animation: fadeIn 1.2s ease;
    }

    /* Chat area container */
    .chat-card {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 0 15px rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(8px);
        margin: 1rem auto;
        width: 85%;
        animation: fadeInUp 1s ease;
    }

    /* Animations */
    @keyframes fadeIn {
        from {opacity: 0; transform: translateY(10px);}
        to {opacity: 1; transform: translateY(0);}
    }

    @keyframes fadeInDown {
        from {opacity: 0; transform: translateY(-15px);}
        to {opacity: 1; transform: translateY(0);}
    }

    @keyframes fadeInUp {
        from {opacity: 0; transform: translateY(15px);}
        to {opacity: 1; transform: translateY(0);}
    }

    </style>
""", unsafe_allow_html=True)

# -------------------- Header --------------------
st.markdown("<h1 class='title'>⭐ Context Aware Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Enhancing Chatbot Interactions through Context Awareness</p>", unsafe_allow_html=True)

# -------------------- Chat Container --------------------
with st.container():
    st.markdown("<div class='chat-card'>", unsafe_allow_html=True)

    class ContextChatbot:
        def __init__(self):
            utils.sync_st_session()
            self.llm = utils.configure_llm()
        
        @st.cache_resource
        def setup_chain(_self):
            memory = ConversationBufferMemory()
            chain = ConversationChain(llm=_self.llm, memory=memory, verbose=False)
            return chain
        
        @utils.enable_chat_history
        def main(self):
            chain = self.setup_chain()
            user_query = st.chat_input(placeholder="Ask me anything! 💬")
            if user_query:
                utils.display_msg(user_query, 'user')
                with st.chat_message("assistant"):
                    st_cb = StreamHandler(st.empty())
                    result = chain.invoke(
                        {"input": user_query},
                        {"callbacks": [st_cb]}
                    )
                    response = result["response"]
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    utils.print_qa(ContextChatbot, user_query, response)

    if __name__ == "__main__" or True:
        obj = ContextChatbot()
        obj.main()

    st.markdown("</div>", unsafe_allow_html=True)

