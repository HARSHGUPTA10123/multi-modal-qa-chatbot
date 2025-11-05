import utils
import sqlite3
import streamlit as st
from pathlib import Path
from sqlalchemy import create_engine
import pandas as pd

from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_community.utilities.sql_database import SQLDatabase



utils.set_default_openai()

# -------------------- Page Setup --------------------
st.set_page_config(page_title="ChatSQL", page_icon="🛢", layout="wide")

# -------------------- CSS Styling --------------------
st.markdown("""
    <style>
    /* Title Gradient */
    .title {
        font-size: 2.2rem;
        font-weight: 700;
        text-align: center;
        color: #ffffff;
        background: linear-gradient(90deg, #00DBDE, #FC00FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2em;
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

    /* Main Card */
    .chat-card {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 0 20px rgba(0, 219, 222, 0.2);
        backdrop-filter: blur(10px);
        margin: 1rem auto;
        width: 88%;
        animation: fadeInUp 1s ease;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: rgba(20, 20, 20, 0.7) !important;
        color: #fff !important;
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
st.markdown("<h1 class='title'>🛢 Chat with Your SQL Database</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Interact with any SQLite database through simple, conversational commands.</p>", unsafe_allow_html=True)

# -------------------- Main Container --------------------
with st.container():
    st.markdown("<div class='chat-card'>", unsafe_allow_html=True)

    class SqlChatbot:
        def __init__(self):
            utils.sync_st_session()
            self.llm = utils.configure_llm()

        def setup_db(_self, db_uri):
            st.sidebar.write("---")
            st.sidebar.subheader("🧩 Database Connection Status")
            
            if db_uri == 'USE_SAMPLE_DB':
                db_filepath = (Path(__file__).parent.parent / "assets" / "Chinook.db").absolute()
                st.sidebar.write(f"📂 Using sample DB: `{db_filepath.name}`")
                db_uri = f"sqlite:///{db_filepath}"
            else:
                db_path = db_uri.replace('sqlite:///', '')
                st.sidebar.write(f"📍 Custom Path: {db_path}")
                
                if not Path(db_path).exists():
                    st.error(f"❌ Database not found: {db_path}")
                    st.stop()
            
            # Direct SQLite check
            try:
                conn = sqlite3.connect(db_uri.replace('sqlite:///', ''))
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                direct_tables = [t[0] for t in cursor.fetchall()]
                st.sidebar.success("✅ SQLite connection successful")
                st.sidebar.write(f"📊 Tables: {direct_tables}")
                conn.close()
            except Exception as e:
                st.sidebar.error(f"❌ SQLite connection failed: {e}")
                st.stop()
            
            # LangChain SQL setup
            try:
                db = SQLDatabase.from_uri(
                    database_uri=db_uri,
                    include_tables=direct_tables,
                    sample_rows_in_table_info=1
                )
                st.sidebar.success("✅ LangChain SQLDatabase connected")
            except Exception as e:
                st.sidebar.error(f"❌ LangChain setup failed: {e}")
                st.stop()
            
            return db

        def setup_sql_agent(_self, db):
            prefix = """
            You are a SQL expert assisting with mental health survey data.
            ONLY use existing tables: Answer, Question, Survey.
            Never invent or assume columns or tables.
            If uncertain, respond with: "I cannot answer with the available data."
            """
            agent = create_sql_agent(
                llm=_self.llm,
                db=db,
                agent_type="openai-tools",
                prefix=prefix,
                verbose=False,
                handle_parsing_errors=True,
                max_iterations=3
            )
            return agent

        def run_direct_query(self, db, query):
            try:
                result = db.run(query)
                return f"✅ Query successful:\n{result}"
            except Exception as e:
                return f"❌ Query failed: {e}"

        @utils.enable_chat_history
        def main(self):
            radio_opt = ['Use sample db - Chinook.db', 'Connect your own SQLite DB']
            selected_opt = st.sidebar.radio("Choose option", radio_opt)
            
            if selected_opt == radio_opt[1]:
                db_uri = st.sidebar.text_input(
                    "Enter Database URI",
                    value='sqlite:///C:\\Users\\hg932\\Downloads\\archive (1)\\mental_health.sqlite',
                    placeholder='sqlite:///path/to/your/database.sqlite'
                )
            else:
                db_uri = 'USE_SAMPLE_DB'
            
            if not db_uri:
                st.error("Please enter a valid database URI.")
                st.stop()
            
            db = self.setup_db(db_uri)
            
            # Quick queries section
            st.sidebar.write("---")
            st.sidebar.subheader("🧠 Quick Query Tests")
            test_queries = [
                "SELECT name FROM sqlite_master WHERE type='table';",
                "SELECT COUNT(*) FROM Question;",
                "SELECT questiontext FROM Question LIMIT 3;"
            ]
            for i, q in enumerate(test_queries):
                if st.sidebar.button(f"Run Test {i+1}"):
                    result = self.run_direct_query(db, q)
                    st.sidebar.code(result)
            
            agent = self.setup_sql_agent(db)
            user_query = st.chat_input("💬 Ask about your database...")

            if user_query:
                st.chat_message("user").write(user_query)
                st.session_state.messages.append({"role": "user", "content": user_query})

                with st.chat_message("assistant"):
                    simple_queries = {
                        'tables': "SELECT name FROM sqlite_master WHERE type='table';",
                        'questions': "SELECT questiontext FROM Question LIMIT 10;",
                        'surveys': "SELECT * FROM Survey LIMIT 5;",
                        'count answers': "SELECT COUNT(*) FROM Answer;"
                    }
                    used_direct = False
                    for key, query in simple_queries.items():
                        if key in user_query.lower():
                            result = self.run_direct_query(db, query)
                            st.write(result)
                            st.session_state.messages.append({"role": "assistant", "content": result})
                            used_direct = True
                            break
                    
                    if not used_direct:
                        try:
                            st_cb = StreamlitCallbackHandler(st.container())
                            result = agent.invoke({"input": user_query}, {"callbacks": [st_cb]})
                            response = result["output"]
                            st.write(response)
                            st.session_state.messages.append({"role": "assistant", "content": response})
                            utils.print_qa(SqlChatbot, user_query, response)
                        except Exception as e:
                            st.error(f"Agent failed: {e}")
                            tables = self.run_direct_query(db, "SELECT name FROM sqlite_master WHERE type='table';")
                            st.write(f"Available tables: {tables}")

    if __name__ == "__main__" or True:
        obj = SqlChatbot()
        obj.main()

    st.markdown("</div>", unsafe_allow_html=True)
