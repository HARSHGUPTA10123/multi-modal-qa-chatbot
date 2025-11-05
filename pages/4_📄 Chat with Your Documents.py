import os
import re
import tempfile
import streamlit as st
import utils
from streaming import StreamHandler
from langchain.memory.buffer import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain_text_splitters import RecursiveCharacterTextSplitter



utils.set_default_openai()

# -------------------- Page Config --------------------
st.set_page_config(page_title="ChatPDF", page_icon="📄", layout="wide")

class CustomDocChatbot:
    def __init__(self):
        utils.sync_st_session()
        self.llm = utils.configure_llm()
        self.embedding_model = utils.configure_embedding_model()
        self.uploaded_files_content = []
        # Enhanced URL pattern
        self.url_pattern = r'(?:https?://|www\.)[^\s<>()\"\']+[^\s<>()\"\'\.]'
        # Common platform patterns
        self.platform_patterns = {
            'linkedin': r'(?:linkedin\.com/|LinkedIn)',
            'github': r'(?:github\.com/|GitHub)',
            'leetcode': r'(?:leetcode\.com/|LeetCode)',
            'udemy': r'(?:udemy\.com/|Udemy)',
            'portfolio': r'(?:portfolio|website)'
        }

    def save_file(self, file):
        """Save uploaded file to a temporary file and return path"""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(file.getvalue())
            return tmp_file.name

    def extract_links_from_text(self, text):
        """Extract URLs and platform mentions from text"""
        text = text.replace('\\n', ' ').replace('\\r', ' ')
        
        # Extract actual URLs
        actual_urls = re.findall(self.url_pattern, text)
        
        # Extract platform mentions
        platform_mentions = []
        for platform, pattern in self.platform_patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                platform_mentions.append(platform)
        
        return actual_urls, platform_mentions

    def extract_all_links_from_pdfs(self, docs):
        """Extract all links and platform mentions from documents"""
        all_urls = []
        all_platforms = []
        
        for doc in docs:
            if getattr(doc, 'page_content', None):
                urls, platforms = self.extract_links_from_text(doc.page_content)
                all_urls.extend(urls)
                all_platforms.extend(platforms)
        
        # Remove duplicates while preserving order
        unique_urls = list(dict.fromkeys(all_urls))
        unique_platforms = list(dict.fromkeys(all_platforms))
        
        return unique_urls, unique_platforms

    def setup_qa_chain(self, uploaded_files):
        """Load PDFs and setup QA chain"""
        docs = []
        self.uploaded_files_content = []

        for file in uploaded_files:
            try:
                file_path = self.save_file(file)
                loader = PyPDFLoader(file_path)
                loaded_docs = loader.load()
                docs.extend(loaded_docs)

                # Store text content
                for d in loaded_docs:
                    content = getattr(d, 'page_content', '') or ''
                    self.uploaded_files_content.append(content)

                # Clean up temp file
                try:
                    os.unlink(file_path)
                except Exception:
                    pass

            except Exception as e:
                st.error(f"Error loading {file.name}: {str(e)}")
                continue

        if not docs:
            st.error("No document content could be loaded.")
            st.stop()

        # Extract links and platform mentions
        all_urls, all_platforms = self.extract_all_links_from_pdfs(docs)
        
        # Display findings in sidebar
        with st.sidebar.expander("🔍 Content Analysis", expanded=True):
            if all_urls:
                st.subheader("🌐 URLs Found:")
                for url in all_urls:
                    display_url = url if len(url) <= 60 else url[:57] + '...'
                    st.write(f"• [{display_url}]({url})")
            else:
                st.write("🌐 **No URLs found**")
            
            if all_platforms:
                st.subheader("📱 Platforms Mentioned:")
                for platform in all_platforms:
                    st.write(f"• {platform.title()}")
            else:
                st.write("📱 **No specific platforms mentioned**")

        st.sidebar.success(f"✅ Loaded {len(docs)} pages from {len(uploaded_files)} PDF(s)")

        # Continue with vector store setup
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
        )
        splits = text_splitter.split_documents(docs)
        vectordb = DocArrayInMemorySearch.from_documents(splits, self.embedding_model)

        retriever = vectordb.as_retriever(
            search_type='similarity',
            search_kwargs={'k': 3}
        )

        memory = ConversationBufferMemory(
            memory_key='chat_history',
            output_key='answer',
            return_messages=True
        )

        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=retriever,
            memory=memory,
            return_source_documents=True,
            verbose=False
        )
        
        # Store content for special queries
        st.session_state['uploaded_files_content'] = self.uploaded_files_content
        st.session_state['found_urls'] = all_urls
        st.session_state['found_platforms'] = all_platforms
        
        return qa_chain

    def handle_special_queries(self, user_query):
        """Handle special queries like link extraction"""
        user_query_lower = user_query.lower()

        # Link related queries
        if any(keyword in user_query_lower for keyword in ['link', 'url', 'http', 'website', 'reference', 'platform', 'social media']):
            urls = st.session_state.get('found_urls', [])
            platforms = st.session_state.get('found_platforms', [])
            
            response_lines = []
            
            if urls:
                response_lines.append("🔗 **Actual URLs found in the document:**")
                for i, url in enumerate(urls, 1):
                    response_lines.append(f"{i}. {url}")
            
            if platforms:
                response_lines.append("\n📱 **Platforms mentioned (but no URLs provided):**")
                for i, platform in enumerate(platforms, 1):
                    response_lines.append(f"{i}. {platform.title()}")
            
            if not urls and not platforms:
                return "No links or specific platform URLs were found in the document. The document contains platform names like LinkedIn, GitHub, etc., but no actual web addresses."
            
            return "\n".join(response_lines)

        return None

    @utils.enable_chat_history
    def main(self):
        # File uploader
        uploaded_files = st.sidebar.file_uploader(
            label='📁 Upload your PDF files',
            type=['pdf'],
            accept_multiple_files=True,
            help="Upload one or more PDF files to chat with"
        )

        if not uploaded_files:
            st.info("📂 Please upload one or more PDF documents to begin chatting.")
            st.stop()

        # Show uploaded files
        st.sidebar.write("---")
        st.sidebar.subheader("📋 Uploaded Files")
        for file in uploaded_files:
            size_kb = file.size // 1024
            st.sidebar.write(f"• {file.name} ({size_kb} KB)")

        # Rebuild QA chain when files change
        current_file_names = [f.name for f in uploaded_files]
        needs_setup = (
            "qa_chain" not in st.session_state or
            "current_files" not in st.session_state or
            st.session_state.current_files != current_file_names
        )

        if needs_setup:
            with st.spinner("🔄 Analyzing document content..."):
                try:
                    st.session_state.qa_chain = self.setup_qa_chain(uploaded_files)
                    st.session_state.current_files = current_file_names
                except Exception as e:
                    st.error(f"Failed to setup QA chain: {str(e)}")
                    st.stop()

        user_query = st.chat_input(placeholder="💬 Ask something about your PDFs!")

        if uploaded_files and user_query:
            utils.display_msg(user_query, 'user')

            with st.chat_message("assistant"):
                try:
                    # Handle special queries
                    special_response = self.handle_special_queries(user_query)
                    if special_response:
                        st.write(special_response)
                        st.session_state.messages.append({"role": "assistant", "content": special_response})
                        utils.print_qa(CustomDocChatbot, user_query, special_response)
                        return

                    # Use QA chain for other questions
                    st_cb = StreamHandler(st.empty())
                    result = st.session_state.qa_chain.invoke(
                        {"question": user_query},
                        {"callbacks": [st_cb]}
                    )

                    response = result.get("answer") or "I couldn't find an answer to that question."
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    st.write(response)
                    utils.print_qa(CustomDocChatbot, user_query, response)

                    # Show references
                    src_docs = result.get('source_documents') or []
                    if src_docs:
                        st.write("---")
                        st.subheader("📚 References")
                        for idx, doc in enumerate(src_docs, 1):
                            filename = os.path.basename(doc.metadata.get('source', 'Unknown'))
                            page_meta = doc.metadata.get('page', None)
                            page_num = page_meta + 1 if isinstance(page_meta, int) else 'Unknown'
                            ref_title = f"**Reference {idx}:** *{filename} - Page {page_num}*"
                            with st.expander(ref_title):
                                st.caption(doc.page_content)

                except Exception as e:
                    st.error(f"Error: {str(e)}")

# Initialize and run
obj = CustomDocChatbot()
obj.main()