import streamlit as st
from utils.file_utils import save_uploaded_file, load_file_content
from splitter.HybridTextSplitter import HybridTextSplitter
from retriever.retriever_utils import hybrid_retriever
from memory.memory_manager import MemoryManager

st.set_page_config(page_title="Advanced Semantic RAG Engine", page_icon="🧠")
st.title("Welcome to the Advanced Semantic RAG Engine 🧠")
st.subheader("Built for robust ingestion and advanced semantic retrieval 🚀")

# Upload sidebar
st.sidebar.header("📄 Upload your documents")
# Reset conversation button
if st.sidebar.button("🧹 Reset Conversation"):
    st.session_state.memory.clear()
    st.session_state.chunks = []
    st.sidebar.success("🧹 Conversation and chunks cleared!")

uploaded_files = st.sidebar.file_uploader(
    "Choose multiple files (PDF, DOCX, TXT, XLSX)", type=["pdf", "docx", "txt", "xlsx"], accept_multiple_files=True
)

# Initialize memory and chunks
if "memory" not in st.session_state:
    st.session_state.memory = MemoryManager()

if "chunks" not in st.session_state:
    st.session_state.chunks = []

# Handle file uploads
if uploaded_files:
    for uploaded_file in uploaded_files:
        try:
            file_path = save_uploaded_file(uploaded_file)
            file_content = load_file_content(file_path)
            splitter = HybridTextSplitter(chunk_size=500, overlap=50)
            chunks = splitter.split_text(file_content)
            st.session_state.chunks.extend(chunks)

            st.sidebar.success(f"✅ Uploaded {uploaded_file.name} ({len(chunks)} chunks)")
        except Exception as e:
            st.sidebar.error(f"❌ Failed to process {uploaded_file.name}: {str(e)}")

# Display conversation history
for role, content in st.session_state.memory.get_history():
    if role == "user":
        st.chat_message("user").markdown(content)
    else:
        st.chat_message("assistant").markdown(content)

# Chat input
user_query = st.chat_input("Ask a question about your documents...")

if user_query:
    st.session_state.memory.add_user_message(user_query)

    try:
        response = hybrid_retriever(
            query=user_query,
            chunks=st.session_state.chunks
        )
        answer = response if response else "🤔 Sorry, I could not find an exact answer in the uploaded documents."

    except Exception as e:
        answer = f"⚠️ An error occurred: {str(e)}"

    st.session_state.memory.add_assistant_message(answer)
    st.chat_message("assistant").markdown(answer)

# Footer
st.markdown("---")
st.caption("🔵 Engine ready for Semantic RAG - Unstructured Data, Zero Fear.")
