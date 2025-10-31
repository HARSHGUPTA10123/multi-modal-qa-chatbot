import os
import openai
import streamlit as st
from datetime import datetime
from streamlit.logger import get_logger
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_core.utils import convert_to_secret_str

logger = get_logger('Langchain-Chatbot')

def sync_st_session():
    """
    Sync streamlit session state if needed.
    This is a placeholder function that can be used for session synchronization.
    """
    pass

# decorator
def enable_chat_history(func):
    # to clear chat history after switching chatbot
    current_page = func.__qualname__
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = current_page
    if st.session_state["current_page"] != current_page:
        try:
            st.cache_resource.clear()
            del st.session_state["current_page"]
            del st.session_state["messages"]
        except:
            pass

    # to show chat history on ui
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
    for msg in st.session_state["messages"]:
        st.chat_message(msg["role"]).write(msg["content"])

    def execute(*args, **kwargs):
        func(*args, **kwargs)
    return execute

def display_msg(msg, author):
    """Method to display message on the UI

    Args:
        msg (str): message to display
        author (str): author of the message - user/assistant
    """
    st.session_state.messages.append({"role": author, "content": msg})
    st.chat_message(author).write(msg)
    
def print_qa(cls, question, answer):
    """Print question and answer for logging purposes"""
    log_str = f"\nUsecase: {cls.__name__}\nQuestion: {question}\nAnswer: {answer}\n" + "------" * 10
    logger.info(log_str)
    
@st.cache_resource
def configure_embedding_model():
    """Configure and return the embedding model for vector storage"""
    embedding_model = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    return embedding_model

def choose_custom_openai_key():
    openai_api_key = st.sidebar.text_input(
        label="OpenAI API Key",
        type="password",
        placeholder="sk-...",
        key="SELECTED_OPENAI_API_KEY"
    )
    if not openai_api_key:
        st.error("Please add your OpenAI API key to continue.")
        st.info("Obtain your key from this link: https://platform.openai.com/account/api-keys")
        st.stop()

    model = "gpt-3.5-turbo"
    try:
        client = openai.OpenAI(api_key=openai_api_key)
        available_models = [{"id": i.id, "created": datetime.fromtimestamp(i.created)} for i in client.models.list() if str(i.id).startswith("gpt")]
        available_models = sorted(available_models, key=lambda x: x["created"])
        available_models = [i["id"] for i in available_models]

        model = st.sidebar.selectbox(
            label="Model",
            options=available_models,
            key="SELECTED_OPENAI_MODEL"
        )
    except openai.AuthenticationError as e:
        error_message = getattr(e, 'body', {}).get('message', str(e))
        st.error(error_message)
        st.stop()
    except Exception as e:
        print(e)
        st.error("Something went wrong. Please try again later.")
        st.stop()
    return model, openai_api_key

def configure_llm():
    available_llms = [
        "llama3.2:3b",        # fast model
        "use your openai api key"
    ]
    
    llm_opt = st.sidebar.radio(
        label="LLM",
        options=available_llms,
        key="SELECTED_LLM"
    )

    if llm_opt == "llama3.2:3b":
        ollama_endpoint = st.secrets.get("OLLAMA_ENDPOINT", "http://localhost:11434")
        llm = ChatOllama(
            model="llama3.2:3b", 
            base_url=ollama_endpoint,
            temperature=0.7,
            num_predict=768,  # Good balance for detailed but quick responses
            top_p=0.9
        )
    else:
        model, openai_api_key = choose_custom_openai_key()
        llm = ChatOpenAI(model=model, temperature=0, streaming=True, api_key=convert_to_secret_str(openai_api_key))
    return llm