import utils
import streamlit as st
from streaming import StreamHandler

from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

# ---------- Page Configuration ----------
st.set_page_config(page_title="Chatbot 💬", page_icon="💬", layout="wide")

# ---------- Custom Styling ----------
st.markdown("""
    <style>
        /* Main app background - keep dark theme */
        .stApp {
            background-color: #000000;
            color: #FFFFFF;
            font-family: 'Segoe UI', sans-serif;
        }

        /* Header title */
        .main-header {
            text-align: center;
            font-size: 2.8rem;
            font-weight: 800;
            color: #7df9ff;
            text-shadow: 0 0 12px rgba(125, 249, 255, 0.6);
            margin-bottom: 0.4rem;
            margin-top: -1rem;
        }

        /* Subtitle */
        .sub-header {
            text-align: center;
            font-size: 1.15rem;
            color: #c0d9ff;
            margin-bottom: 1.8rem;
        }

        /* Chat input bar */
        div[data-testid="stChatInput"] > div {
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(125, 249, 255, 0.25);
            border-radius: 12px;
            padding: 0.5rem 1rem;
            transition: box-shadow 0.2s ease-in-out;
        }

        div[data-testid="stChatInput"] > div:focus-within {
            box-shadow: 0 0 10px rgba(125, 249, 255, 0.4);
        }

        /* Chat bubbles */
        .stChatMessage {
            border-radius: 16px;
            padding: 0.9rem 1.2rem;
            margin-bottom: 0.5rem;
            background-color: rgba(255,255,255,0.06);
            box-shadow: 0 3px 10px rgba(0,0,0,0.3);
        }

        /* User bubble */
        [data-testid="stChatMessage"][data-testid="stChatMessage-user"] {
            background: linear-gradient(135deg, #141421, #1e1e2f);
        }

        /* Assistant bubble */
        [data-testid="stChatMessage"][data-testid="stChatMessage-assistant"] {
            background: rgba(255, 255, 255, 0.07);
        }

        /* Scrollbar for chat */
        ::-webkit-scrollbar {
            width: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #111;
        }
        ::-webkit-scrollbar-thumb {
            background: #555;
            border-radius: 10px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #888;
        }

        /* Footer */
        .footer {
            text-align: center;
            color: #b0e0e6;
            margin-top: 2rem;
            font-size: 0.9rem;
        }
        .footer b {
            color: #00e5ff;
        }
    </style>
""", unsafe_allow_html=True)

# ---------- Header Section ----------
st.markdown('<h1 class="main-header">💬 Basic Chatbot</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Interact with a conversational LLM in real-time</p>', unsafe_allow_html=True)

# ---------- Chatbot Class ----------
class BasicChatbot:

    def __init__(self):
        utils.sync_st_session()
        self.llm = utils.configure_llm()
    
    def setup_chain(self):
        prompt = PromptTemplate(
            input_variables=["history", "input"],
            template="""You are a helpful AI assistant.

Current conversation:
{history}
Human: {input}
AI:"""
        )
        
        memory = ConversationBufferMemory()
        chain = LLMChain(
            llm=self.llm,
            prompt=prompt,
            memory=memory,
            verbose=False
        )
        return chain
    
    @utils.enable_chat_history
    def main(self):
        chain = self.setup_chain()
        user_query = st.chat_input(placeholder="Ask me anything...")
        if user_query:
            utils.display_msg(user_query, 'user')
            with st.chat_message("assistant"):
                st_cb = StreamHandler(st.empty())
                result = chain.invoke(
                    {"input": user_query},
                    {"callbacks": [st_cb]}
                )
                response = result["text"]
                st.session_state.messages.append({"role": "assistant", "content": response})
                utils.print_qa(BasicChatbot, user_query, response)

# ---------- Run App ----------
if __name__ == "__main__":
    obj = BasicChatbot()
    obj.main()

# ---------- Footer ----------
st.markdown("""
    <div class="footer">
        Built with ❤️ using <b>Streamlit</b> & <b>LangChain</b> | Designed by <b>Harsh Gupta</b> 🚀
    </div>
""", unsafe_allow_html=True)
