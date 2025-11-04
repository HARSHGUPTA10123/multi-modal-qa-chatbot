import os
import openai
import streamlit as st
from datetime import datetime
import logging
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_core.utils import convert_to_secret_str

# Set up logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('Langchain-Chatbot')

def clear_llm_cache_on_provider_change():
    """Clear LLM cache when user switches between OpenAI and Ollama"""
    # Always initialize with OpenAI as default
    if "previous_llm_provider" not in st.session_state:
        st.session_state.previous_llm_provider = "OpenAI (Cloud - Recommended)"

    if "llm_provider_selection" not in st.session_state:
        st.session_state.llm_provider_selection = "OpenAI (Cloud - Recommended)"

    
    current_provider = st.session_state.get("llm_provider_selection", None)
    previous_provider = st.session_state.previous_llm_provider
    
    # If provider changed, clear relevant caches
    if current_provider != previous_provider:
        # Clear API key inputs when switching away from OpenAI
        if previous_provider == "OpenAI (Cloud - Recommended)":  # FIXED: Match the exact option
            keys_to_clear = ["openai_api_key_input", "openai_model_selection", "openai_temperature"]
            for key in keys_to_clear:
                if key in st.session_state:
                    del st.session_state[key]
        
        # Clear model cache
        if "configure_llm" in st.session_state:
            del st.session_state["configure_llm"]
        
        st.session_state.previous_llm_provider = current_provider

def sync_st_session():
    """
    Sync streamlit session state if needed.
    This is a placeholder function that can be used for session synchronization.
    """
    pass

def set_default_openai():
    """
    Set OpenAI as default provider only if no provider has been selected yet.
    Prevents overwriting user's choice on every rerun.
    """
    if "llm_provider_selection" not in st.session_state:
        st.session_state.llm_provider_selection = "OpenAI (Cloud - Recommended)"


#decorator
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
        st.session_state["messages"] = [{"role": "assistant", "content": "Hey! 🤖 Ready for some AI magic? Ask me anything! ✨"}]
    
    # Display chat messages
    for msg in st.session_state["messages"]:
        st.chat_message(msg["role"]).write(msg["content"])

    def execute(*args, **kwargs):

        return func(*args, **kwargs)
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

def configure_openai_llm():
    """Configure OpenAI LLM with user-provided API key"""
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔑 OpenAI Configuration")
    
    # Get default key from secrets (optional)
    default_key = st.secrets.get("OPENAI_API_KEY", "")
    
    openai_api_key = st.sidebar.text_input(
        label="OpenAI API Key",
        type="password",
        value=default_key,
        placeholder="sk-...",
        help="Enter your OpenAI API key",
        key="openai_api_key_input"
    )
    
    if not openai_api_key:
        st.sidebar.warning("Please enter your OpenAI API key to use GPT models")
        return None

    # Model selection
    model = st.sidebar.selectbox(
        label="OpenAI Model",
        options=["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo-preview", "gpt-4o"],
        index=0,
        help="Choose which OpenAI model to use",
        key="openai_model_selection"
    )
    
    # Temperature setting
    temperature = st.sidebar.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        help="Higher values = more creative, Lower values = more deterministic",
        key="openai_temperature"
    )
    
    try:
        # Test the API key
        client = openai.OpenAI(api_key=openai_api_key)
        client.models.list()  # Simple test call
        
        # Convert string to SecretStr for LangChain
        llm = ChatOpenAI(
            model=model,
            temperature=temperature,
            streaming=True,
            api_key=convert_to_secret_str(openai_api_key)
        )
        st.sidebar.success("✅ OpenAI connected!")
        return llm
        
    except openai.AuthenticationError:
        st.sidebar.error("❌ Invalid API key. Please check your OpenAI API key.")
        return None
    except Exception as e:
        st.sidebar.error(f"❌ OpenAI error: {str(e)}")
        return None

def configure_ollama_llm():
    """Configure Ollama LLM - Keep errors for demonstration"""
    st.sidebar.markdown("---")
    st.sidebar.subheader("🦙 Ollama Configuration")
    
    # Only show tinyllama as available with (Recommended) tag
    ollama_models = ["tinyllama (Recommended)", "llama2", "mistral", "codellama"]
    selected_ollama_model = st.sidebar.selectbox(
        label="Ollama Model",
        options=ollama_models,
        index=0,
        help="Only 'tinyllama' is installed. Other models will show errors for demonstration",
        key="ollama_model_selection"
    )
    
    # Remove the "(Recommended)" tag for processing
    model_name = selected_ollama_model.replace(" (Recommended)", "").strip()
    
    # Temperature control
    ollama_temperature = st.sidebar.slider(
        "Creativity Level (Temperature)",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        help="0.0 = Precise, 0.7 = Balanced, 1.0 = Creative",
        key="ollama_temperature"
    )
    
    ollama_endpoint = st.secrets.get("OLLAMA_ENDPOINT", "http://localhost:11434")
    
    try:
        # Check if the selected model is available
        if model_name != "tinyllama":
            # For demonstration - show custom error message
            st.sidebar.error(f"❌ '{model_name}' model is not pulled or installed locally.")
            st.sidebar.info(f"💡 Kindly use 'tinyllama (Recommended)' or run: `ollama pull {model_name}`")
            return None
        
        # Only tinyllama should work
        llm = ChatOllama(
            model=model_name,
            base_url=ollama_endpoint,
            temperature=ollama_temperature,
            num_gpu=0,
            timeout=60,
        )
        st.sidebar.success(f"✅ {model_name} connected!")
        return llm
        
    except Exception as e:
        # Fallback error handling
        st.sidebar.error(f"❌ {model_name} not available: {str(e)}")
        st.sidebar.info(f"💡 Only 'tinyllama (Recommended)' is installed. Run: `ollama pull {model_name}`")
        return None

def configure_llm():
    """Main LLM configuration with automatic cache management"""
    
    # Clear cache on provider change
    clear_llm_cache_on_provider_change()
    
    st.sidebar.header("🤖 Choose Your AI Model")
    
    # LLM type selection
    llm_type = st.sidebar.radio(
        label="Select AI Provider",
        options=["OpenAI (Cloud - Recommended)", "Ollama (Local)"],  # FIXED: Added the labels back
        index=0,  
        help="Choose between cloud-based OpenAI or local Ollama",
        key="llm_provider_selection"
    )
    
    
    if llm_type == "OpenAI (Cloud - Recommended)":  # FIXED: Match the exact option
        llm = configure_openai_llm()
        if llm is None:
            st.sidebar.info("🔑 Enter your OpenAI API key above to start chatting")
            st.stop()
    else:  # Ollama
        llm = configure_ollama_llm()
        if llm is None:
            st.sidebar.info("🦙 Start Ollama service or switch to OpenAI")
            st.stop()
    
    return llm

def clear_chat_history():
    """Clear chat history"""
    if "messages" in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "How can I help you?"}]
    st.rerun()

# Add clear button to sidebar in your main apps
def add_clear_button():
    """Add clear chat history button to sidebar"""
    st.sidebar.markdown("---")
    if st.sidebar.button("🗑️ Clear Chat History", use_container_width=True):
        clear_chat_history()
        
        
# -------------------- Internet Chat LLM Config --------------------
import streamlit as st
from tavily import TavilyClient
def configure_llm_internet():
    """
    Configures the LLM (OpenAI or Ollama) specifically for the Internet Chat page.
    Returns: (llm, tavily_client)
    """
    # Use separate session state keys for Internet chatbot
    if "internet_llm_provider_selection" not in st.session_state:
        st.session_state.internet_llm_provider_selection = "OpenAI"
    else:
        # keep the current selection persistent across reruns
        pass


    with st.sidebar:
        st.header("⚙️ Model Configuration")

        # Let user choose the LLM provider - use separate key
        st.session_state.internet_llm_provider_selection = st.selectbox(
            "Select LLM Provider:",
            ["OpenAI", "Ollama"],
            index=0 if st.session_state.internet_llm_provider_selection == "OpenAI" else 1,
            key="internet_llm_provider_selectbox"  # Unique key
        )

        # OpenAI Configuration - SIMPLE (only API key)
        if st.session_state.internet_llm_provider_selection == "OpenAI":
            openai_api_key = st.text_input(
                "🔑 Enter OpenAI API Key:",
                key="internet_openai_api_key_input",  # Unique key
                type="password",
                placeholder="sk-...",
            )
            st.info("Using **OpenAI API** — Internet access handled automatically.", icon="💡")
            
            if not openai_api_key:
                st.error("⚠️ Please enter your OpenAI API Key.")
                st.stop()
            
            llm = configure_openai_direct(openai_api_key)
            tavily_client = TavilyClient(api_key=st.secrets.get("TAVILY_API_KEY", ""))
            return llm, tavily_client

        # Ollama Configuration - WITH MODEL SELECTION
        else:
            st.markdown("---")
            st.subheader("🦙 Ollama Configuration")
            
            # Model selection with recommended tag - use unique keys
            ollama_models = ["tinyllama (Recommended)", "llama2", "mistral", "codellama"]
            selected_ollama_model = st.selectbox(
                label="Ollama Model",
                options=ollama_models,
                index=0,
                help="Only 'tinyllama' is installed. Other models will show errors for demonstration",
                key="internet_ollama_model_selection"  # Unique key
            )
            
            # Remove the "(Recommended)" tag for processing
            model_name = selected_ollama_model.replace(" (Recommended)", "").strip()
            
            # Temperature control - use unique key
            ollama_temperature = st.slider(
                "Creativity Level (Temperature)",
                min_value=0.0,
                max_value=1.0,
                value=0.7,
                help="0.0 = Precise, 0.7 = Balanced, 1.0 = Creative",
                key="internet_ollama_temperature"  # Unique key
            )
            
            # Tavily API Key - use unique key
            tavily_key = st.text_input(
                "🌐 Enter Tavily API Key:",
                key="internet_tavily_api_key_input",  # Unique key
                type="password",
                placeholder="tvly-...",
            )
            st.info("Using **Ollama (Local)** — Tavily API Key required for web access.", icon="⚙️")
            
            if not tavily_key:
                st.error("⚠️ Please enter your Tavily API Key to enable internet access.")
                st.stop()
            
            # Check if the selected model is available
            if model_name != "tinyllama":
                st.error(f"❌ '{model_name}' model is not pulled or installed locally.")
                st.info(f"💡 Kindly use 'tinyllama (Recommended)' or run: `ollama pull {model_name}`")
                st.stop()
            
            llm = configure_ollama_direct(model_name, ollama_temperature)
            tavily_client = TavilyClient(api_key=tavily_key)
            return llm, tavily_client

def configure_openai_direct(api_key):
    """Configure OpenAI directly without sidebar elements"""
    try:
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model="gpt-3.5-turbo",
            api_key=api_key,
            temperature=0.7,
            streaming=True
        )
    except Exception as e:
        st.error(f"❌ Error initializing OpenAI: {e}")
        st.stop()

def configure_ollama_direct(model_name="tinyllama", temperature=0.7):
    """Configure Ollama directly with model selection"""
    try:
        from langchain_community.chat_models import ChatOllama
        return ChatOllama(
            model=model_name,
            temperature=temperature,
            base_url="http://localhost:11434",
            
        )
    except Exception as e:
        st.error(f"❌ Error initializing Ollama: {e}")
        st.error("Make sure Ollama is running on http://localhost:11434")
        st.stop()



