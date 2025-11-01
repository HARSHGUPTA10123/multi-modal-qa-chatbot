import utils
import streamlit as st
import os
from tavily import TavilyClient


# -------------------- Cache Management --------------------
# Clear any residual OpenAI sessions when starting
if "openai_api_key_input" in st.session_state:
    del st.session_state["openai_api_key_input"]

# Set default to Ollama if not set
if "llm_provider_selection" not in st.session_state:
    st.session_state.llm_provider_selection = "Ollama (Local)"

# -------------------- Page Config --------------------
st.set_page_config(page_title="ChatNet", page_icon="🌐", layout="wide")

# -------------------- Custom Styling --------------------
st.markdown("""
    <style>
    /* Title Styling */
    .title {
        font-size: 2.2rem;
        font-weight: 700;
        text-align: center;
        color: #ffffff;
        background: linear-gradient(90deg, #3DB2FF, #0078FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2em;
        animation: fadeInDown 1s ease;
    }

    /* Subtitle Styling */
    .subtitle {
        text-align: center;
        font-size: 1.1rem;
        color: #d0d0d0;
        margin-bottom: 2rem;
        animation: fadeIn 1.2s ease;
    }

    /* Card container */
    .chat-card {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 0 15px rgba(0, 120, 255, 0.1);
        backdrop-filter: blur(8px);
        margin: 1rem auto;
        width: 85%;
        animation: fadeInUp 1s ease;
    }

    /* Search result block styling */
    .search-results {
        background-color: rgba(255, 255, 255, 0.06);
        border-left: 4px solid #0078FF;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin-top: 1rem;
        font-size: 0.95rem;
        line-height: 1.5;
        color: #e0e0e0;
        animation: fadeIn 0.8s ease;
    }

    /* Animations */
    @keyframes fadeIn {
        from {opacity: 0; transform: translateY(10px);}
        to {opacity: 1; transform: translateY(0);}
    }

    @keyframes fadeInUp {
        from {opacity: 0; transform: translateY(15px);}
        to {opacity: 1; transform: translateY(0);}
    }

    @keyframes fadeInDown {
        from {opacity: 0; transform: translateY(-15px);}
        to {opacity: 1; transform: translateY(0);}
    }
    </style>
""", unsafe_allow_html=True)

# -------------------- Header --------------------
st.markdown("<h1 class='title'>🌐 ChatNet</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Equipped with Internet Access — Ask questions about recent events in real-time.</p>", unsafe_allow_html=True)

# -------------------- Chat Container --------------------
with st.container():
    st.markdown("<div class='chat-card'>", unsafe_allow_html=True)

    class InternetChatbot:

        def __init__(self):
            utils.sync_st_session()
            self.llm = utils.configure_llm()
            # Initialize Tavily client directly
            self.tavily_client = TavilyClient(api_key=st.secrets.get("TAVILY_API_KEY"))

        def search_web(self, query):
            """Simple web search function"""
            try:
                results = self.tavily_client.search(query=query, max_results=3)
                return results.get('results', [])
            except Exception as e:
                return f"Search failed: {str(e)}"

        @utils.enable_chat_history
        def main(self):
            user_query = st.chat_input(placeholder="Ask me anything! 🌍")
            if user_query:
                utils.display_msg(user_query, 'user')
                with st.chat_message("assistant"):
                    # First, search the web
                    search_results = self.search_web(user_query)

                    # Show search context
                    if isinstance(search_results, list) and search_results:
                        with st.expander("🔎 Web Search Results", expanded=False):
                            for result in search_results[:3]:
                                st.markdown(f"**{result.get('title', 'No Title')}**  \n{result.get('content', '')}")

                        # Combine results into enhanced prompt
                        context = "\n".join([
                            f"- {result.get('title', '')}: {result.get('content', '')}"
                            for result in search_results[:2]
                        ])
                        enhanced_query = f"""Based on the following search results, answer the question: {user_query}

Search Results:
{context}

Please provide a comprehensive answer:"""
                    else:
                        enhanced_query = user_query

                    # Get LLM response
                    response = self.llm.invoke(enhanced_query)
                    final_response = response.content

                    st.session_state.messages.append({"role": "assistant", "content": final_response})
                    st.markdown(f"<div class='search-results'>{final_response}</div>", unsafe_allow_html=True)
                    utils.print_qa(InternetChatbot, user_query, final_response)

    if __name__ == "__main__" or True:
        obj = InternetChatbot()
        obj.main()

    st.markdown("</div>", unsafe_allow_html=True)
