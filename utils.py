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
    """
    Decorator to handle Streamlit chat history display properly.
    Shows previous messages once, then lets the main function
    handle new messages without repeating them.
    """
    # Initialize chat history if not present
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "Hey! 🤖 Ready for some AI magic? Ask me anything! ✨"}
        ]

    # Display **existing messages** only once at the start
    for msg in st.session_state["messages"]:
        st.chat_message(msg["role"]).write(msg["content"])

    def wrapper(*args, **kwargs):
        # Call the original function (handles new messages)
        return func(*args, **kwargs)

    return wrapper


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
    """Configure OpenAI LLM with persistent connection inside sidebar."""
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔑 OpenAI Configuration")

    # Initialize connection flags
    if "openai_connected" not in st.session_state:
        st.session_state.openai_connected = False
    if "openai_connect_clicked" not in st.session_state:
        st.session_state.openai_connect_clicked = False

    # API key input
    openai_api_key = st.sidebar.text_input(
        "Enter OpenAI API Key",
        type="password",
        key="openai_api_key_input",
        placeholder="sk-...",
        help="Enter your OpenAI API key here"
    )

    # Connect button (persistent click handler)
    if st.sidebar.button("🔗 Connect to OpenAI", use_container_width=True):
        if not openai_api_key:
            st.sidebar.warning("⚠️ Please enter your API key first.")
        else:
            st.session_state.openai_connect_clicked = True

    # When button was clicked, attempt to connect
    if st.session_state.openai_connect_clicked and not st.session_state.openai_connected:
        try:
            client = openai.OpenAI(api_key=openai_api_key)
            client.models.list()  # Test key
            st.session_state.openai_connected = True
            st.sidebar.success("✅ Successfully connected to OpenAI!")
            st.rerun()
        except Exception as e:
            st.sidebar.error(f"❌ Failed to connect: {e}")
            st.session_state.openai_connected = False
            st.session_state.openai_connect_clicked = False

    # Stop early if not connected
    if not st.session_state.openai_connected:
        st.sidebar.info("⬆️ Enter your API key and click 'Connect to OpenAI' to continue.")
        st.stop()

    # --- Once connected, show model + temperature ---
    st.sidebar.success("✅ OpenAI Connected!")

    model = st.sidebar.selectbox(
        "Select Model",
        ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo-preview", "gpt-4o"],
        key="openai_model_selection"
    )

    temperature = st.sidebar.slider(
        "Creativity (Temperature)",
        min_value=0.0, max_value=1.0,
        value=0.7, step=0.05,
        key="openai_temperature"
    )

    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(
        model=model,
        temperature=temperature,
        streaming=True,
        api_key=convert_to_secret_str(openai_api_key)
    )

    return llm


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
    Configures and returns a valid (llm, tavily_client).
    """
    st.sidebar.header("🌐 Internet-Enabled Chatbot")
    
    # Initialize Tavily client first
    tavily_api_key = st.sidebar.text_input(
        "Enter Tavily API Key",
        type="password",
        key="tavily_api_key_input",
        placeholder="Your Tavily API key...",
        help="Get your API key from https://tavily.com"
    )
    
    tavily_client = None
    if tavily_api_key:
        try:
            tavily_client = TavilyClient(api_key=tavily_api_key)
            st.sidebar.success("✅ Tavily connected!")
        except Exception as e:
            st.sidebar.error(f"❌ Tavily connection failed: {e}")
    else:
        st.sidebar.warning("⚠️ Add Tavily API key for web search")
    # LLM Provider Selection
    provider = st.sidebar.radio(
        "Select LLM Provider:",
        ["OpenAI", "Ollama"],
        key="internet_llm_provider_selection"
    )

    # ------------------ OPENAI ------------------
    if provider == "OpenAI":
        api_key = st.sidebar.text_input(
            "Enter OpenAI API Key",
            type="password",
            key="openai_internet_api_key",
            placeholder="sk-..."
        )

        if not api_key:
            st.sidebar.info("👆 Enter your OpenAI API key to continue")
            return None, tavily_client

        try:
            from langchain_openai import ChatOpenAI
            llm = ChatOpenAI(
                model="gpt-3.5-turbo",
                api_key=convert_to_secret_str(api_key),
                temperature=0.7,
                streaming=True
            )
            # Test the connection
            llm.invoke("Hello")
            st.sidebar.success("✅ OpenAI is ready!")
            return llm, tavily_client
        except Exception as e:
            st.sidebar.error(f"❌ OpenAI initialization failed: {e}")
            return None, tavily_client

    # ------------------ OLLAMA ------------------
    else:
        # Allow user to select from available Ollama models
        ollama_models = ["tinyllama (Recommended)", "llama2", "mistral", "codellama"]
        selected_model = st.sidebar.selectbox(
            "Select Ollama Model",
            options=ollama_models,
            index=0,
            help="Only tinyllama is installed by default; other models may show errors"
        )

        # Remove (Recommended) tag for the model name
        model_name = selected_model.replace(" (Recommended)", "").strip()

        ollama_temperature = st.sidebar.slider(
            "Creativity Level (Temperature)",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            help="0.0 = precise, 0.7 = balanced, 1.0 = creative"
        )

        ollama_endpoint = st.secrets.get("OLLAMA_ENDPOINT", "http://localhost:11434")

        try:
            # Only tinyllama is guaranteed to work by default
            if model_name != "tinyllama":
                st.sidebar.error(f"❌ '{model_name}' model not pulled/installed locally.")
                st.sidebar.info(f"💡 Use 'tinyllama (Recommended)' or run: `ollama pull {model_name}`")
                return None, tavily_client

            llm = ChatOllama(
                model=model_name,
                base_url=ollama_endpoint,
                temperature=ollama_temperature,
                num_gpu=0,
                timeout=60,
            )
            st.sidebar.success(f"✅ {model_name} connected!")
            return llm, tavily_client
        except Exception as e:
            st.sidebar.error(f"❌ {model_name} not available: {str(e)}")
            return None, tavily_client





def configure_openai_direct(api_key):
    """Configure OpenAI directly without sidebar elements"""
    try:
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model="gpt-3.5-turbo",
            api_key=convert_to_secret_str(api_key),  # ← Use convert_to_secret_str() here too
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

def configure_ollama_local():
    """Fallback configuration for local Ollama models."""
    try:
        from langchain_community.chat_models import ChatOllama
        llm = ChatOllama(model="llama3", temperature=0.7)
        return llm
    except Exception as e:
        import streamlit as st
        st.error(f"Ollama setup failed: {e}")
        return None


