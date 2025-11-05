# import streamlit as st
# import utils 
# from tavily import TavilyClient

# # -------------------- Page Config --------------------
# st.set_page_config(page_title="ChatNet", page_icon="🌐", layout="wide")

# # -------------------- Sidebar Configuration --------------------
# # REMOVED THE DUPLICATE HEADER - configure_llm_internet() already adds one

# # Use new helper that handles provider + API key logic
# config = utils.configure_llm_internet()
# if not config:
#     st.warning("⚠️ Please connect to a model provider first from the sidebar.")
#     st.stop()

# llm, tavily_client = config


# # -------------------- Custom Styling --------------------
# st.markdown("""
#     <style>
#     /* Your existing styles remain the same */
#     .title {
#         font-size: 2.2rem;
#         font-weight: 700;
#         text-align: center;
#         color: #ffffff;
#         background: linear-gradient(90deg, #3DB2FF, #0078FF);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#         margin-bottom: 0.2em;
#         animation: fadeInDown 1s ease;
#     }

#     .subtitle {
#         text-align: center;
#         font-size: 1.1rem;
#         color: #d0d0d0;
#         margin-bottom: 2rem;
#         animation: fadeIn 1.2s ease;
#     }

#     .chat-card {
#         background-color: rgba(255, 255, 255, 0.05);
#         border-radius: 16px;
#         padding: 2rem;
#         box-shadow: 0 0 15px rgba(0, 120, 255, 0.1);
#         backdrop-filter: blur(8px);
#         margin: 1rem auto;
#         width: 85%;
#         animation: fadeInUp 1s ease;
#     }

#     .search-results {
#         background-color: rgba(255, 255, 255, 0.06);
#         border-left: 4px solid #0078FF;
#         padding: 1rem 1.5rem;
#         border-radius: 10px;
#         margin-top: 1rem;
#         font-size: 0.95rem;
#         line-height: 1.5;
#         color: #e0e0e0;
#         animation: fadeIn 0.8s ease;
#     }

#     @keyframes fadeIn {
#         from {opacity: 0; transform: translateY(10px);}
#         to {opacity: 1; transform: translateY(0);}
#     }

#     @keyframes fadeInUp {
#         from {opacity: 0; transform: translateY(15px);}
#         to {opacity: 1; transform: translateY(0);}
#     }

#     @keyframes fadeInDown {
#         from {opacity: 0; transform: translateY(-15px);}
#         to {opacity: 1; transform: translateY(0);}
#     }
#     </style>
# """, unsafe_allow_html=True)

# # -------------------- Header --------------------
# st.markdown("<h1 class='title'>🌐 ChatNet</h1>", unsafe_allow_html=True)
# st.markdown("<p class='subtitle'>Equipped with Internet Access — Ask questions about recent events in real-time.</p>", unsafe_allow_html=True)

# # -------------------- Chat Container --------------------
# with st.container():
#     st.markdown("<div class='chat-card'>", unsafe_allow_html=True)

#     class InternetChatbot:
#         def __init__(self):
#             utils.sync_st_session()
#             self.llm = llm
#             self.tavily_client = tavily_client

#         def search_web(self, query):
#             """Simple web search function"""
#             try:
#                 results = self.tavily_client.search(
#                     query=query,
#                     max_results=3
#                 )
#                 return results.get("results", [])
#             except Exception as e:
#                 return f"Search failed: {str(e)}"

#         @utils.enable_chat_history
#         def main(self):
#             user_query = st.chat_input(placeholder="Ask me anything! 🌍")

#             if user_query:
#                 utils.display_msg(user_query, 'user')

#                 with st.chat_message("assistant"):
#                     search_results = self.search_web(user_query)

#                     # Show search preview
#                     if isinstance(search_results, list) and search_results:
#                         with st.expander("🔎 Web Search Results", expanded=False):
#                             for result in search_results[:3]:
#                                 st.markdown(
#                                     f"**{result.get('title', 'No Title')}**  \n"
#                                     f"{result.get('content', '')}"
#                                 )

#                         # Build contextual prompt
#                         context = "\n".join([
#                             f"- {result.get('title', '')}: {result.get('content', '')}"
#                             for result in search_results[:2]
#                         ])

#                         enhanced_query = f"""Based on the web results below, answer the following user question.

# User Question:
# {user_query}

# Web Search Context:
# {context}

# Provide a clear and helpful answer:
# """
#                     else:
#                         enhanced_query = user_query

#                     # ✅ Correct invoke format for langchain 0.3.x
#                     response = self.llm.invoke(enhanced_query)

#                     # Some models return .content, some return raw string
#                     final_response = response.content if hasattr(response, "content") else response

#                     st.session_state.messages.append({
#                         "role": "assistant",
#                         "content": final_response
#                     })

#                     st.markdown(
#                         f"<div class='search-results'>{final_response}</div>",
#                         unsafe_allow_html=True
#                     )

#                     utils.print_qa(InternetChatbot, user_query, final_response)

#     if __name__ == "__main__" or True:
#         obj = InternetChatbot()
#         obj.main()

#     st.markdown("</div>", unsafe_allow_html=True)



import streamlit as st
import utils
from tavily import TavilyClient
from langchain_core.messages import HumanMessage
from langchain_core.language_models import BaseChatModel

# -------------------- Page Config --------------------
st.set_page_config(page_title="ChatNet", page_icon="🌐", layout="wide")

# -------------------- Sidebar Configuration --------------------
config = utils.configure_llm_internet()
if not config:
    st.warning("⚠️ Please connect to a model provider first from the sidebar.")
    st.stop()

llm, tavily_client = config

# -------------------- Custom Styling --------------------
st.markdown("""
    <style>
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
    .subtitle {
        text-align: center;
        font-size: 1.1rem;
        color: #d0d0d0;
        margin-bottom: 2rem;
    }
    .chat-card {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 2rem;
        width: 85%;
        margin: auto;
    }
    .search-results {
        background-color: rgba(255, 255, 255, 0.06);
        padding: 1rem 1.5rem;
        margin-top: 1rem;
        border-left: 4px solid #0078FF;
        border-radius: 10px;
        color: #e0e0e0;
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
            self.llm = llm
            self.tavily_client = tavily_client

        def search_web(self, query):
            """Search the web using Tavily API"""
            try:
                if self.tavily_client:
                    # Correct Tavily API call
                    results = self.tavily_client.search(query=query, max_results=3)
                    return results.get('results', [])
                return []
            except Exception as e:
                st.error(f"Search failed: {str(e)}")
                return []

        def ask_llm(self, prompt: str) -> str:
            """Send a prompt to the LLM and return its response safely."""
            from langchain_core.messages import HumanMessage

            # Ensure LLM is not None
            assert self.llm is not None, "LLM is not initialized"

            try:
                # Safe call
                response = self.llm([HumanMessage(content=prompt)])
                if isinstance(response, list) and len(response) > 0:
                    first_msg = response[0]
                    return getattr(first_msg, "content", str(first_msg))
                return str(response)
            except Exception as e:
                return f"Error generating response: {str(e)}"



        @utils.enable_chat_history
        def main(self):
            user_query = st.chat_input("Ask me anything! 🌍")

            if user_query:
                utils.display_msg(user_query, 'user')

                with st.chat_message("assistant"):
                    search_results = self.search_web(user_query)

                    if search_results:  # Check if we have results
                        with st.expander("🔎 Web Search Results", expanded=False):
                            for i, result in enumerate(search_results, 1):
                                st.markdown(f"**{i}. {result.get('title', 'No Title')}**")
                                st.markdown(f"{result.get('content', '')}")
                                if result.get('url'):
                                    st.markdown(f"*Source: {result.get('url')}*")
                                st.divider()

                        # Prepare context from search results
                        context = "\n".join([
                            f"- **{result.get('title', 'No Title')}**: {result.get('content', '')}"
                            for result in search_results[:2]  # Use first 2 results for context
                        ])

                        enhanced_prompt = f"""Based on these recent web search results, answer the user's question clearly and accurately:

Search Results:
{context}

User Question: {user_query}

Provide a comprehensive answer based on the search results:"""
                    else:
                        # No search results available
                        enhanced_prompt = f"""Answer the following question: {user_query}

Note: I couldn't access current web information, so I'll answer based on my general knowledge."""

                    # Generate response from LLM
                    final_response = self.ask_llm(enhanced_prompt)

                    # Store and display response
                    st.session_state.messages.append({"role": "assistant", "content": final_response})
                    st.markdown(f"<div class='search-results'>{final_response}</div>", unsafe_allow_html=True)

                    # Log the Q&A
                    utils.print_qa(InternetChatbot, user_query, final_response)

    obj = InternetChatbot()
    obj.main()

    st.markdown("</div>", unsafe_allow_html=True)
